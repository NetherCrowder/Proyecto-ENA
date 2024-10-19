from typing import Generic, TypeVar, List
from .error import Error

T = TypeVar('T')


class Result(Generic[T]):
    NO_FIRST_ERROR = Error.custom(500, "No first error.")
    NO_ERRORS = Error.custom(200, "No errors.")

    def __init__(self, value: T = None, errors: List[Error] = None):
        self.value = value
        self.errors = errors if errors else [self.NO_ERRORS]

    @property
    def is_success(self) -> bool:
        return not self.errors or self.errors[0].__eq__(self.NO_ERRORS)

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @property
    def first_error(self) -> Error:
        return self.errors[0] if self.errors else self.NO_FIRST_ERROR

    @staticmethod
    def success(value: object = None) -> 'Result[T]':
        return Result(value=value, errors=[])

    @staticmethod
    def failure(errors) -> 'Result[T]':
        if not isinstance(errors, list):
            errors = [errors]
        return Result(errors=errors)

    def __eq__(self, other: 'Result[T]') -> bool:
        if not isinstance(other, Result):
            return False
        return (self.value == other.value) and (self.errors == other.errors)
