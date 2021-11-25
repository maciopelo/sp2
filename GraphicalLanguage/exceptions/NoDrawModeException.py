class NoDrawModeException(Exception):
    def __init__(self, line):
        self.message = f"Line no. {line}: No draw mode was defined! You must define 2D or 3D mode!"
        super().__init__(self.message)
