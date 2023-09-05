"""
"""
from typing import List
from types import ModuleType
import inspect
from ..functions import Function


class Module:
    """
    The Module class maps a module to a name, description, its functions, and its submodules.
    """

    _name: str
    _description: str
    _module: ModuleType
    _functions: List[Function]
    _submodules: List["Module"]
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
        self._submodules = []

        for name, member in inspect.getmembers(module):
            if name.startswith("_"):
                continue
            if inspect.isfunction(member):
                self._functions.append(Function(member))
            elif inspect.ismodule(member) and member.__name__.startswith(
                module.__name__
            ):  # To ensure it's a submodule
                self._submodules.append(Module(member))

        self._prompts = prompts

    def __eq__(self, other):
        if not isinstance(other, Module):
            return NotImplemented

        functions_equal = all(
            f1 == f2 for f1, f2 in zip(self.functions, other.functions)
        )
        submodules_equal = all(
            m1 == m2 for m1, m2 in zip(self.submodules, other.submodules)
        )

        return (
            self.name == other.name
            and self.description == other.description
            and self.module == other.module
            and functions_equal
            and submodules_equal
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
    def submodules(self) -> List["Module"]:
        """
        Returns:
            List[Module]: A list of submodules in the module.
        """
        return self._submodules

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
