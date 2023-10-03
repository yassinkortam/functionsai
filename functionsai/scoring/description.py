from typing import List
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ..functions import Function


class SentenceTransformerEmbedder:
    def __init__(self, model_name="paraphrase-distilroberta-base-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, texts: List[str]) -> torch.Tensor:
        """
        Extract SentenceTransformer embeddings for the given texts.

        Args:
            texts (List[str]): The texts to be embedded.

        Returns:
            torch.Tensor: The SentenceTransformer embeddings for the given texts.
        """
        return torch.tensor(self.model.encode(texts))


def similarity(
    user_prompt: str,
    functions: List[Function],
    embedder: SentenceTransformerEmbedder,
) -> List[float]:
    """
    Compare the user prompt to a batch of function descriptions using SentenceTransformer embeddings.

    Args:
        user_prompt (str): The user's prompt.
        functions (List[Function]): The list of functions to be scored.
        embedder (SentenceTransformerEmbedder): An instance of SentenceTransformerEmbedder.

    Returns:
        List[float]: The similarities between the user prompt and each function description.
    """
    descriptions = [function.description for function in functions]
    user_embedding = embedder.get_embedding([user_prompt])
    description_embeddings = embedder.get_embedding(descriptions)
    cosine_similarities = cosine_similarity(
        user_embedding, description_embeddings
    )
    return cosine_similarities[0]
