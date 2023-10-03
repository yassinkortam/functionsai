"""
"""
import inspect
from types import ModuleType
from typing import Callable, List, Tuple
from .functions import Function
from .modules import Module
from .scoring import Scoring


class FunctionsAI:
    """
    The FunctionsAI class is the main class for the FunctionsAI package. It is used to search
    through functions and modules to find the most relevant functions given a prompt.
    """

    _functions: List[Function]
    _modules: List[Module]
    _scoring: Scoring = Scoring()

    def __init__(self, *args) -> None:
        """
        Args:
            *args: A list of modules and functions.
        """
        self._functions = []
        self._modules = []
        for arg in args:
            if isinstance(arg, ModuleType):
                module = Module(arg)
                self._modules.append(module)
                for function in module.functions:
                    self._functions.append(Function(function))
            elif inspect.isfunction(arg):
                self._functions.append(Function(arg))
            else:
                raise TypeError(
                    "FunctionsAI only accepts Modules and Functions"
                )

    def sort(self, prompt: str) -> List[Tuple[Function, float]]:
        """
        Sort the functions by their similarity to the prompt.

        Args:
            prompt (str): The user's prompt.

        Returns:
            List[Tuple[Function, float]]: A list of functions and their similarity scores.
        """

        # Score all functions at once
        similarity_scores = self.scoring.score(self.functions, prompt)

        # Pair functions with their scores
        paired_functions_scores = zip(self.functions, similarity_scores)

        # Sort the pairs by score
        sorted_pairs = sorted(
            paired_functions_scores, key=lambda x: x[1], reverse=True
        )

        return sorted_pairs

    @property
    def functions(self) -> List[Function]:
        """
        Returns:
            List[Function]: A list of functions.
        """
        return self._functions

    @property
    def modules(self) -> List[Module]:
        """
        Returns:
            List[Module]: A list of modules.
        """
        return self._modules

    @property
    def scoring(self) -> Scoring:
        """
        Returns:
            Scoring: The scoring object.
        """
        return self._scoring

    @scoring.setter
    def scoring(self, scoring: Scoring) -> None:
        """
        Args:
            scoring (Scoring): The scoring object.
        """
        self._scoring = scoring


__all__ = ["FunctionsAI", "Function", "Module", "Scoring"]
