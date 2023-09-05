"""
"""
import spacy
import inspect
from types import ModuleType
from typing import Callable, List, Tuple
from .functions import Function
from .modules import Module


class FunctionsAI:
    """
    The FunctionsAI class is the main class for the FunctionsAI package. It is used to search
    through functions and modules to find the most relevant functions given a prompt.
    """

    _functions: List[Function]
    _modules: List[Module]
    _nlp: spacy.Language

    def __init__(self, *args) -> None:
        """
        Args:
            *args: A list of modules and functions.
        """
        self._functions = []
        self._modules = []
        for arg in args:
            if isinstance(arg, ModuleType):
                self._modules.append(Module(arg))
            elif inspect.isfunction(arg):
                self._functions.append(Function(arg))
            else:
                raise TypeError(
                    "FunctionsAI only accepts Modules and Functions"
                )
        self._nlp = spacy.load("en_core_web_sm")

    def _score_function(self, function: Function, prompt: str) -> float:
        """
        Determine the relevancy score based on the verbs and proper nouns in the prompt.

        Args:
            function (Function): The function to check.
            prompt (str): The user's query or prompt.

        Returns:
            float: Relevancy score between 0 (not relevant) and 1 (highly relevant).
        """
        doc = self._nlp(prompt)

        # Extract verbs and proper nouns from the prompt
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        proper_nouns = [token.lemma_ for token in doc if token.pos_ == "PROPN"]

        # Check if proper nouns match function name
        name_match = (
            1 if any(noun in function.name for noun in proper_nouns) else 0
        )

        # Check for verb matches in function description
        verb_match_score = sum(
            1 for verb in verbs if verb in function.description
        ) / (len(verbs) if verbs else 1)

        # The score is a combination of the name match and verb match
        # The weights (0.7 and 0.3) can be adjusted based on preference
        score = 0.7 * name_match + 0.3 * verb_match_score

        return score

    def _sort_functions(
        self, prompt: str, score: Callable
    ) -> List[Tuple[Function, float]]:
        """
        Search through all functions and modules to find the most relevant functions given a prompt.

        Args:
            prompt (str): The user's query or prompt.
            score_function (Callable): Function to determine relevancy score.

        Returns:
            List[Tuple[Function, float]]: A sorted list of functions with their respective scores.
        """

        scored_functions = []

        def decision_tree(
            module: Module, prompt: str
        ) -> List[Tuple[Function, float]]:
            local_scores = []

            for function in module.functions:
                func_score = score(function, prompt)
                local_scores.append((function, func_score))

            for submodule in module.submodules:
                relevant_functions = decision_tree(submodule, prompt)
                # Combine submodule's score with function scores inside it
                local_scores.extend([(f, s) for f, s in relevant_functions])

            return local_scores

        for function in self._functions:
            func_score = score(function, prompt)
            scored_functions.append((function, func_score))

        for module in self._modules:
            scored_functions.extend(decision_tree(module, prompt))

        # Sort by score in descending order
        scored_functions.sort(key=lambda x: x[1], reverse=True)

        return scored_functions

    def sort_functions(self, prompt: str) -> List[Tuple[Function, float]]:
        """
        Search through all functions and modules to find the most relevant functions given a prompt.

        Args:
            prompt (str): The user's query or prompt.

        Returns:
            List[Tuple[Function, float]]: A sorted list of functions with their respective scores.
        """
        return self._sort_functions(prompt, self._score_function)

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


__all__ = ["FunctionsAI", "Function", "Module"]
