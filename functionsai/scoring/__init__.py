"""
"""
from typing import Callable, List
from .description import SentenceTransformerEmbedder
from ..functions import Function
from . import description
from . import name
from . import prompt


class Scoring:
    """
    The Scoring class is used to score the similarity of a function to a prompt.
    """

    _name_scoring: Callable
    _description_scoring: Callable
    _prompt_scoring: Callable
    _name_score: float
    _description_score: float
    _prompt_score: float

    def __init__(
        self,
        name_scoring: Callable = name.similarity,
        description_scoring: Callable = description.similarity,
        prompt_scoring: Callable = prompt.similarity,
    ) -> None:
        self._name_scoring = name_scoring
        self._description_scoring = description_scoring
        self._prompt_scoring = prompt_scoring
        self._embedder = SentenceTransformerEmbedder()

    def score(self, functions: List[Function], prompt: str) -> List[float]:
        """
        Score the similarity of a batch of functions to a prompt.

        Args:
            functions (List[Function]): The list of functions to be scored.
            prompt (str): The user's prompt.

        Returns:
            List[float]: The list of similarity scores for each function.
        """

        # Initialize scores with zeros
        name_scores = [0] * len(functions)
        description_scores = [0] * len(functions)
        prompt_scores = [0] * len(functions)

        # Functions with names
        functions_with_names = [
            func for func in functions if func.name is not None
        ]
        if functions_with_names:
            name_scores_for_named_functions = self._name_scoring(
                prompt, functions_with_names
            )
            for func, score in zip(
                functions_with_names, name_scores_for_named_functions
            ):
                name_scores[functions.index(func)] = score

        # Functions with descriptions
        functions_with_descriptions = [
            func for func in functions if func.description is not None
        ]
        if functions_with_descriptions:
            description_scores_for_described_functions = (
                self._description_scoring(
                    prompt, functions_with_descriptions, self._embedder
                )
            )
            for func, score in zip(
                functions_with_descriptions,
                description_scores_for_described_functions,
            ):
                description_scores[functions.index(func)] = score

        # Functions with prompts
        functions_with_prompts = [
            func
            for func in functions
            if func.prompts is not None and len(func.prompts) > 0
        ]
        if functions_with_prompts:
            prompt_scores_for_prompted_functions = self._prompt_scoring(
                prompt, functions_with_prompts
            )
            for func, score in zip(
                functions_with_prompts, prompt_scores_for_prompted_functions
            ):
                prompt_scores[functions.index(func)] = score

        # Combine scores
        combined_scores = [
            max(name, desc, prompt)
            for name, desc, prompt in zip(
                name_scores, description_scores, prompt_scores
            )
        ]

        return combined_scores

    @property
    def name_scoring(self) -> Callable:
        """
        Returns:
            Callable: The name scoring function.
        """
        return self._name_scoring

    @property
    def description_scoring(self) -> Callable:
        """
        Returns:
            Callable: The description scoring function.
        """
        return self._description_scoring

    @property
    def prompt_scoring(self) -> Callable:
        """
        Returns:
            Callable: The prompt scoring function.
        """
        return self._prompt_scoring

    @name_scoring.setter
    def name_scoring(self, name_scoring: Callable) -> None:
        """
        Args:
            name_scoring (Callable): The name scoring function.
        """
        self._name_scoring = name_scoring

    @description_scoring.setter
    def description_scoring(self, description_scoring: Callable) -> None:
        """
        Args:
            description_scoring (Callable): The description scoring function.
        """
        self._description_scoring = description_scoring

    @prompt_scoring.setter
    def prompt_scoring(self, prompt_scoring: Callable) -> None:
        """
        Args:
            prompt_scoring (Callable): The prompt scoring function.
        """
        self._prompt_scoring = prompt_scoring


__all__ = ["Scoring"]
