import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from ..functions import Function


def similarity(
    user_prompt_vec: np.ndarray,
    functions: List[Function],
) -> np.ndarray:
    """
    Compare the user prompt to a batch of function descriptions.

    Args:
        user_prompt (str): The user's prompt.
        functions (List[Function]): The list of functions to be scored.

    Returns:
        np.ndarray: The similarities between the user prompt and each function description.
    """

    vectors = [function.description_vector for function in functions]
    similarities = cosine_similarity(user_prompt_vec.reshape(1, -1), vectors)[0]

    return similarities
