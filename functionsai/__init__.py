"""
"""
import spacy
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
    _nlp: spacy.language.Language = spacy.load("en_core_web_sm")
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

        for function in self.functions:
            if function.description is not None:
                function.description_vector = self._nlp(
                    function.description
                ).vector

        for function in self.functions:
            if function.prompts is not None:
                function.prompts_vector = [
                    self._nlp(prompt).vector for prompt in function.prompts
                ]

    def sort(self, prompt: str) -> List[Tuple[Function, float]]:
        """
        Sort the functions by their similarity to the prompt.

        Args:
            prompt (str): The user's prompt.

        Returns:
            List[Tuple[Function, float]]: A list of functions and their similarity scores.
        """
        prompt_vector = self._nlp(prompt).vector
        similarity_scores = self.scoring.score(
            prompt, prompt_vector, self.functions
        )
        paired_functions_scores = zip(self.functions, similarity_scores)
        sorted_pairs = sorted(
            paired_functions_scores, key=lambda x: x[1], reverse=True
        )

        return sorted_pairs

    def top(self, prompt: str, top: int = 5) -> List[Function]:
        """
        Search the functions and modules for the most relevant functions.

        Args:
            prompt (str): The user's prompt.
            top (int, optional): The number of functions to return. Defaults to 5.

        Returns:
            List[Function]: A list of the most relevant functions.
        """
        sorted_pairs = self.sort(prompt)
        matches = [pair[0] for pair in sorted_pairs[:top]]
        return [
            {
                "name": match.name,
                "description": match.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        param.name: {
                            "type": param.type,
                            "description": param.description,
                        }
                        for param in match.params
                    },
                    "required": [
                        param.name
                        for param in match.params
                        if param.is_required
                    ],
                },
            }
            for match in matches
        ]

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
