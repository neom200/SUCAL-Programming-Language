class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.error = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def as_string(self):
        result = f'{self.error}: {self.details}'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        super().__init__('Illegal Character Error', details)

class InvalidSyntaxtError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntatx Error', details)