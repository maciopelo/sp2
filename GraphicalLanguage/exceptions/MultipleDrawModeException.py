class MultipleDrawModeException(Exception):
    def __init__(self, line):
        self.message = f"Line no. {line}: Multiple draw mode definition found! There can only be one draw mode defined!"
        super().__init__(self.message)