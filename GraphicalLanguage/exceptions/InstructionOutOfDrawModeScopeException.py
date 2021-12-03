class InstructionOutOfDrawModeScopeException(Exception):
    def __init__(self, line, instruction, draw_mode):
        self.message = f"Line no. {line}: You can't use {instruction} in {draw_mode} mode!"
        super().__init__(self.message)
