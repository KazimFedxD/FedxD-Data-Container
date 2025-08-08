from __future__ import annotations

import string
from typing import Any, Generic, Optional, TypeVar

from fxdc.exceptions import FieldError

T = TypeVar("T")

ACCEPTABLECHARACTERS = string.ascii_letters + string.digits + "_"


class Field(Generic[T]):
    def __init__(
        self,
        desc: Optional[str] = None,
        verbose_name: Optional[str] = None,
        default: Optional[Any] = None,
        typechecking: bool = True,
        null: bool = True,
        blank: bool = True,
    ):
        if verbose_name:
            if verbose_name[0] not in string.ascii_letters + "_":
                raise FieldError("Name Should Start With A Letter")
            if any([x not in ACCEPTABLECHARACTERS for x in verbose_name]):
                raise FieldError(
                    "Name Should Only Contain Letters, Digits and Underscore"
                )
        if desc:
            if len(desc) > 50:
                raise FieldError("Description Should Not Be More Than 50 Characters")

        self.__verbose_name = verbose_name
        self.__default = default
        self.__typechecking = typechecking
        self.__null = null
        self.__blank = blank
        self.__desc = desc

    @property
    def desc(self) -> Optional[str]:
        return self.__desc

    @property
    def verbose_name(self) -> Optional[str]:
        return self.__verbose_name

    @property
    def default(self) -> Optional[Any]:
        return self.__default

    @property
    def typechecking(self) -> bool:
        return self.__typechecking

    @property
    def null(self) -> bool:
        return self.__null

    @property
    def blank(self) -> bool:
        return self.__blank

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: object) -> T:
        value: T = instance.__dict__.get(self.name, None)
        return value

    def __set__(self, instance: object, value: Optional[T]) -> None:
        instance.__dict__[self.name] = value

    def __delete__(self, instance: object) -> None:
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]
        else:
            raise AttributeError(
                f"{self.name} not found in {instance.__class__.__name__}"
            )
