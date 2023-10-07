import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from ..functions import Function


def similarity(
    user_prompt_vector: np.ndarray, functions: List[Function]
) -> np.ndarray:
    """
    Compare the user prompt to the descriptions of a batch of functions using TF-IDF vectors.

    Args:
        user_prompt (str): The user's prompt.
        functions (List[Function]): The list of functions to be scored.

    Returns:
        np.ndarray: The similarities between the user prompt and each function's description.
    """

    vectors = [function.prompts_vectors for function in functions]
    similarities = []
    for vectors_list in vectors:
        similarities.append(
            np.max(cosine_similarity(user_prompt_vector, vectors_list))
        )
    return similarities
