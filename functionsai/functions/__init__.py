"""
"""
import numpy as np
import inspect
from typing import Callable, List


class Parameter:
    """
    The Parameter class maps a parameter to a name, description, type, and whether it is required.
    """

    def __init__(
        self, name: str, description: str, type: type, is_required: bool
    ) -> None:
        self._name = name
        self._description = description
        self._type = type
        self._is_required = is_required

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def type(self) -> type:
        return self._type

    @property
    def is_required(self) -> bool:
        return self._is_required


class Function:
    """
    The Function class maps a function to a name, description, and related prompt.
    """

    _name: str
    _description: str
    _function: Callable
    _prompts: List[str] = []
    _params: List[Parameter] = []

    _name_vector: np.ndarray = None
    _description_vector: np.ndarray = None
    _prompts_vector: np.ndarray = None

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

        param_descriptions = {}
        if function.__doc__ is not None:
            for line in function.__doc__.split("\n"):
                if ":" in line:
                    param = line.split()[0].strip()
                    description = line.split(":")[1].strip()
                    param_descriptions[param] = description

        self._params = [
            Parameter(
                name=param.name,
                description=param_descriptions.get(param.name, None),
                type=param.annotation
                if param.annotation != inspect.Parameter.empty
                else None,
                is_required=param.default == inspect.Parameter.empty,
            )
            for param in inspect.signature(function).parameters.values()
            if param.name != "self"
        ]

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

    @property
    def name_vector(self) -> np.ndarray:
        """
        Returns:
            np.ndarray: The vector representation of the function's name.
        """
        return self._name_vector

    @property
    def description_vector(self) -> np.ndarray:
        """
        Returns:
            np.ndarray: The vector representation of the function's description.
        """
        return self._description_vector

    @property
    def prompts_vector(self) -> np.ndarray:
        """
        Returns:
            np.ndarray: The vector representation of the function's prompts.
        """
        return self._prompts_vector

    @property
    def params(self) -> List[Parameter]:
        """
        Returns:
            List[Parameter]: A list of parameters for the function.
        """
        return self._params

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

    @name_vector.setter
    def name_vector(self, name_vector: np.ndarray) -> None:
        """
        Args:
            name_vector (np.ndarray): The vector representation of the function's name.
        """
        self._name_vector = name_vector

    @description_vector.setter
    def description_vector(self, description_vector: np.ndarray) -> None:
        """
        Args:
            description_vector (np.ndarray): The vector representation of the function's description.
        """
        self._description_vector = description_vector

    @prompts_vector.setter
    def prompts_vector(self, prompts_vector: np.ndarray) -> None:
        """
        Args:
            prompts_vector (np.ndarray): The vector representation of the function's prompts.
        """
        self._prompts_vector = prompts_vector


__all__ = ["Function"]
