"""
"""
from typing import List
from types import ModuleType
import inspect
from ..functions import Function


class Module:
    """
    The Module class maps a module to a name, description, and list of functions.
    """

    _name: str
    _description: str
    _module: ModuleType
    _functions: List[Function]
    _prompts: List[str] = None

    def __init__(self, module: ModuleType, prompts: List[str] = None) -> None:
        """
        Args:
            module (ModuleType): The module to be called.
            prompts (List[str], optional): A list of prompts related to the module. Defaults to None.
        """
        self._name = module.__name__
        self._description = module.__doc__
        self._module = module
        self._functions = [
            Function(function)
            for name, function in inspect.getmembers(module, inspect.isfunction)
        ]
        self._prompts = prompts

    def __eq__(self, other):
        if not isinstance(other, Module):
            return NotImplemented
        return (
            self.name == other.name
            and self.description == other.description
            and self.module == other.module
            and self.functions == other.functions
            and self.prompts == other.prompts
        )

    @property
    def name(self) -> str:
        """
        Returns:
            str: The name of the module.
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Returns:
            str: A description of the module.
        """
        return self._description

    @property
    def module(self) -> ModuleType:
        """
        Returns:
            ModuleType: The module.
        """
        return self._module

    @property
    def functions(self) -> List[Function]:
        """
        Returns:
            List[Function]: A list of functions in the module.
        """
        return self._functions

    @property
    def prompts(self) -> List[str]:
        """
        Returns:
            List[str]: A list of prompts to be used with the module.
        """
        return self._prompts

    @description.setter
    def description(self, description: str) -> None:
        """
        Args:
            description (str): A description of the module.
        """
        self._description = description

    @prompts.setter
    def prompts(self, prompts: List[str]) -> None:
        """
        Args:
            prompts (List[str]): A list of prompts related to the module.
        """
        self._prompts = prompts


__all__ = ["Module"]
