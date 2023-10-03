"""
"""
from typing import List
from types import ModuleType
import inspect
from ..functions import Function


class Module:
    """
    The Module class maps a module to a name, description, and its functions.
    """

    _name: str
    _description: str
    _module: ModuleType
    _functions: List[Function]
    _prompts: List[str] = None

    def __init__(self, module: ModuleType, prompts: List[str] = None) -> None:
        """
        Args:
            module (ModuleType): The module to be analyzed.
            prompts (List[str], optional): A list of prompts related to the module. Defaults to None.
        """
        self._name = module.__name__
        self._description = module.__doc__
        self._module = module
        self._functions = []
        self._functions = self._get_functions(module)
        self._prompts = prompts

    def __eq__(self, other):
        if not isinstance(other, Module):
            return NotImplemented

        functions_equal = all(
            f1 == f2 for f1, f2 in zip(self.functions, other.functions)
        )

        return (
            self.name == other.name
            and self.description == other.description
            and self.module == other.module
            and functions_equal
            and self.prompts == other.prompts
        )

    def _get_functions(self, module):
        """
        Gets all functions in a module.

        Args:
            module (ModuleType): The module to be analyzed.

        Returns:
            List[Function]: A list of functions in the module.
        """
        functions = []

        def get_all_functions(module):
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith("_"):
                    functions.append(obj)
                else:
                    try:
                        if obj.__module__.startswith(module.__name__):
                            get_all_functions(obj)
                    except AttributeError:
                        continue

        get_all_functions(module)
        return functions

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
