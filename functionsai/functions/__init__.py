"""
"""
from typing import Callable, List


class Function:
    """
    The Function class maps a function to a name, description, and related prompt.
    """

    _name: str
    _description: str
    _function: Callable
    _prompts: List[str] = None

    def __init__(self, function: Callable, prompts: List[str] = None) -> None:
        """
        Args:
            function (Callable): The function to be called.
            prompts (List[str], optional): A list of prompts related to the function. Defaults to None.
        """
        self._name = function.__name__
        self._description = function.__doc__
        self._function = function
        self._prompts = prompts

    def __eq__(self, other):
        if not isinstance(other, Function):
            return NotImplemented
        return (
            self.name == other.name
            and self.description == other.description
            and self.function == other.function
            and self.prompts == other.prompts
        )

    @property
    def name(self) -> str:
        """
        Returns:
            str: The name of the function.
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Returns:
            str: A description of the function.
        """
        return self._description

    @property
    def function(self) -> Callable:
        """
        Returns:
            Callable: The function to be called.
        """
        return self._function

    @property
    def prompts(self) -> List[str]:
        """
        Returns:
            List[str]: A list of prompts to be used with the function.
        """
        return self._prompts

    @description.setter
    def description(self, description: str) -> None:
        """
        Args:
            description (str): A description of the function.
        """
        self._description = description

    @prompts.setter
    def prompts(self, prompts: List[str]) -> None:
        """
        Args:
            prompts (List[str]): A list of prompts related to the function.
        """
        self._prompts = prompts


__all__ = ["Function"]
