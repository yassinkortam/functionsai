from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..functions import Function


def similarity(user_prompt: str, functions: List[Function]) -> List[float]:
    """
    Compare the user prompt to the descriptions of a batch of functions using TF-IDF vectors.

    Args:
        user_prompt (str): The user's prompt.
        functions (List[Function]): The list of functions to be scored.

    Returns:
        List[float]: The similarities between the user prompt and each function's description.
    """

    # Extract all prompts from the list of functions
    all_prompts = [
        prompt for function in functions for prompt in function.prompts
    ]

    # Combine user prompt with all other prompts
    all_texts = [user_prompt] + all_prompts

    vectorizer = TfidfVectorizer().fit(all_texts)
    vectors = vectorizer.transform(all_texts).toarray()

    # Compute cosine similarities between user prompt and all other prompts
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]

    # Group by function and take the max similarity for each function
    num_prompts_per_function = [len(function.prompts) for function in functions]
    max_similarities = []
    start_idx = 0
    for num_prompts in num_prompts_per_function:
        end_idx = start_idx + num_prompts
        max_similarity = max(cosine_similarities[start_idx:end_idx])
        max_similarities.append(max_similarity)
        start_idx = end_idx

    return max_similarities
