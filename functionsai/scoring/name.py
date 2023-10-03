from typing import List
from fuzzywuzzy import fuzz
import string
from ..functions import Function


def similarity(user_prompt: str, functions: List[Function]) -> List[float]:
    """
    Check to see if the function name is mentioned in the prompt for a batch of functions.

    Args:
        user_prompt (str): The user's prompt.
        functions (List[Function]): The list of functions to be scored.

    Returns:
        List[float]: The similarities between the user prompt and each function's name.
    """

    # Preprocess the user prompt
    words = (
        user_prompt.translate(str.maketrans("", "", string.punctuation))
        .lower()
        .split()
    )

    # Compute similarities for each function
    similarities = []
    for function in functions:
        max_similarity = max(
            [fuzz.ratio(word, function.name) for word in words]
        )
        similarities.append(max_similarity)

    return similarities
