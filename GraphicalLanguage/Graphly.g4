grammar Graphly;

WS 				
	:
	'\n' 
	| ' ' 
	| '\t'
	;

CR
	: 
	'\r' -> skip;

COM_SIGN 		
	: 
	'--' ~[\r\n]* -> skip;

MULTILINE_COM
	: '-*' .*? '*-' -> skip
	;

// body of a program

program
	:
	(WS* instruction ('\n')+)*
	(WS* instruction WS*)
	(('\n')+ instruction WS*)* 
	EOF
	;

instruction 
	: canvas
	| drawMode
	| shape 
	| num
	| draw 
	| transformation 
	| group 
	| loop 
	| conditional
	| assign
	| log
	| save
	| WS*
	;

// control statements
block 			
	: 
	(WS* instruction WS* '\n')*
	;

loop
	: 
	'loop' WS+
	name=NAME WS+ 
	'start' WS+ starting=expr WS+ 
	'until' WS+ until=expr WS+ 
	'step' WS+ step=expr WS+ 
	'then' WS* '\n' 
	block WS* 
	'end'
	;

conditional
	: 
	WS* 'if' WS+ condition_block 
	('else' WS+ 'if' WS+ condition_block)* WS* 
	('else' WS+ 'then' '\n' block)? WS* 
	'end'
	;

condition_block 
	: 
	expr WS+ 
	'then' '\n' WS* 
	block
	;

// shapes

shape 
	: 
	point 
	| vector
	| segment 
	| circle 
	| polygon
	| axis
	| sphere
	| box
	| curve
	| pyramid
	| ring
	| cylinder
	;

point 
	: 
	WS* 'point' WS+ NAME WS* ':' 
	WS* x=expr WS* ',' WS* y=expr
	;

vector
	:
	WS* 'vector' WS+ NAME WS* ':'
	WS* x=expr WS* ',' WS* y=expr WS* ',' WS* z=expr
	;

segment 
	: 
	WS* 'segment' WS+ NAME WS* ':' 
	WS* NAME WS* ',' WS+ NAME
	; 

circle 
	: 
	WS*'circle' WS+ NAME WS* ':' 
	WS* NAME WS* ',' WS* expr
	;

polygon 
	: 
	WS* 'polygon' WS+ NAME WS* ':' 
	WS* NAME
	;

axis
	:
	WS* 'axis' WS+ NAME WS* ':'
	WS* NAME WS* ',' WS* NAME
	;

sphere
	:
	WS* 'sphere' WS+ NAME WS* ':'
	WS* NAME WS* ',' WS* radius=expr
	;

box
	:
	WS* 'box' WS+ NAME WS* ':'
	WS* NAME WS* ',' WS* NAME
	;
	
curve
	:
	WS* 'curve' WS+ NAME WS* ':'
	WS* NAME
	;
	
pyramid
	:
	WS* 'pyramid' WS+ NAME WS* ':'
	WS* NAME WS* ',' WS* NAME
	;
	
ring
	:
	WS* 'ring' WS+ NAME WS* ':'
	WS* NAME WS* ',' WS* NAME WS* ',' WS* radius=expr WS* ',' WS* thickness=expr
	;

cylinder
	:
	WS* 'cylinder' WS+ NAME WS* ':'
	WS* NAME WS* ',' WS* NAME WS* ',' WS* radius=expr
	;

groupMember 
	: 
	WS* NAME WS* '[' WS* expr WS* ']'
	;
	
transformable
	:
	NAME 
	|  groupMember
	;

group 
	: 
	WS* 'list' WS* '<' WS* TYPE WS* '>' WS+ NAME WS* ':' 
	WS* NAME WS* (',' WS* NAME WS*)*
	;

// numerical type

num 
	: 
	WS* 'num' WS+ NAME WS* ':' 
	WS* expr
	;


// methods

canvas 
	: 
	WS* 'canvas' WS* ':'
	WS* x=expr WS* ',' WS* y=expr WS* ',' WS* COLOR
	;

drawMode
	:
	WS* 'mode' WS* ':'
	WS* MODE
	;

draw 
	: 
	WS* 'draw' WS+ arg=transformable
	;

log
	:
	WS* 'log' WS+ arg=transformable #shapeLog
	| WS* 'log' WS+ arg=expr		#exprLog
	| WS* 'log' WS+ TEXT            #textLog
	;

save
	:
	'save'	#simpleSave
	| 'save' WS+ TEXT #namedSave
	;

// transformations

transformation 
	: 
	fill 
	| move 
	| place 
	| rotate 
	| scale
	;

fill 
	: 
	WS* 'fill' WS+ arg=transformable WS* ':'
	WS* COLOR
	;

move 
	: 
	WS* 'move' WS+ arg=transformable WS* ':' 
	WS* dx=expr WS* ',' WS* dy=expr
	;
	
move3d 
	: 
	WS* 'move3d' WS+ arg=transformable WS* ':' 
	WS* dx=expr WS* ',' WS* dy=expr WS* ',' WS* dz=expr
	;

place 
	: 
	WS* 'place' WS+ arg1=transformable WS* ':' 
	WS* arg2=transformable
	;

rotate 
	: 
	WS* 'rotate' WS+ arg1=transformable WS* ':' 
	WS* angle=expr WS* ',' WS* arg2=transformable
	;

scale 
	: 
	WS* 'scale' WS+ arg1=transformable WS* ':' 
	WS* k=expr WS* ',' WS* arg2=transformable
	;

scale3d
	: 
	WS* 'scale3d' WS+ arg1=transformable WS* ':' 
	WS* k=expr
	;

assign
	:
	WS* 'assign' WS+ arg1=transformable WS* ':' WS* arg2=transformable #copyAssign
	| WS* 'assign' WS+ arg1=transformable WS* ':' WS* arg2=expr        #numAssign
	;

// expression

expr  
	: 
	'(' WS* expr WS* ')'                                           #parenExpr
    | op=('^'|'_'|'~') WS* expr                                    #roundingOpExpr
    | '-' WS* expr                                                 #minusOpExpr
    | left=expr WS* op=('*'|'/'|'%') WS* right=expr                #arithmeticOpExpr
    | left=expr WS* op=('+'|'-') WS* right=expr                    #arithmeticOpExpr
    | left=expr WS* op=('<='|'>'|'>='|'<'|'='|'!=') WS* right=expr #booleanOpExpr
    | '!' WS* expr                                                 #negationOpExpr
    | left=expr WS* op='&' WS* right=expr                          #booleanOpExpr
    | left=expr WS* op='|' WS* right=expr                          #booleanOpExpr
    | atom                                                         #atomExpr
    ;

atom 
	: 
	ITR    #intAtom
    | FLT  #fltAtom
    | NAME #varAtom
    ;

// terminal

MODE
	:
	'2D' | '3D'
	;

ITR
	: 
	(NONZERO+ DIGIT* | '0')
	;

FLT
	: 
	(NONZERO+ | '0') DOT DIGIT+
	;

TEXT
 : '"' (~[\r\n"])* '"'
 ;

TYPE
	:
	[a-z]+
	;

COLOR 
	:
	'#'[a-z]+
	;

DOT 
	: 
	'.'
	;

DIGIT 
	: 
	[0-9]
	;

NONZERO
	:
	[1-9]
	;

NAME 
	: 
	[A-Z][a-zA-Z0-9_]*
	;
