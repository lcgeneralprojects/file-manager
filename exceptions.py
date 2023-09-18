class BaseException(Exception):
    # Base class for exceptions in this project
    pass


class EmptyArgsException(BaseException):
    # Exception raised when some of the arguments passed are empty strings or None
    def __init__(self, empty_args):
        self.empty_args = empty_args
        self.message = 'the following necessary fields are empty: ' + ', '.join(empty_args)