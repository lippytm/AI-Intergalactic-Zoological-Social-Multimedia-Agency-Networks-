"""
NLP Toolkit
===========
Tokenisation, sentence embeddings, zero-shot classification, summarisation,
and a Retrieval-Augmented Generation (RAG) helper.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------------
# Tokenisation helpers
# ---------------------------------------------------------------------------

def simple_tokenize(text: str) -> list[str]:
    """Whitespace tokeniser (no external dependencies)."""
    return text.lower().split()


def ngrams(tokens: list[str], n: int = 2) -> list[tuple[str, ...]]:
    """Return n-gram tuples from *tokens*."""
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


# ---------------------------------------------------------------------------
# Hugging Face wrappers (lazy imports so library is optional)
# ---------------------------------------------------------------------------

def get_summarizer(model: str = "facebook/bart-large-cnn") -> Any:
    """Return a HuggingFace summarization pipeline."""
    from transformers import pipeline  # type: ignore
    return pipeline("summarization", model=model)


def summarize(text: str, max_length: int = 130, min_length: int = 30) -> str:
    summarizer = get_summarizer()
    result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return result[0]["summary_text"]


def zero_shot_classify(text: str, labels: list[str]) -> dict[str, float]:
    """Classify *text* into one of *labels* without fine-tuning."""
    from transformers import pipeline  # type: ignore
    clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    out = clf(text, candidate_labels=labels)
    return dict(zip(out["labels"], out["scores"]))


# ---------------------------------------------------------------------------
# Sentence Embeddings & Semantic Search
# ---------------------------------------------------------------------------

def embed_sentences(sentences: list[str], model: str = "all-MiniLM-L6-v2") -> Any:
    """Return a numpy array of sentence embeddings."""
    from sentence_transformers import SentenceTransformer  # type: ignore
    st = SentenceTransformer(model)
    return st.encode(sentences, normalize_embeddings=True)


def semantic_search(
    query: str,
    corpus: list[str],
    top_k: int = 5,
    model: str = "all-MiniLM-L6-v2",
) -> list[tuple[str, float]]:
    """Return the top-k corpus entries most semantically similar to *query*."""
    import numpy as np
    from sentence_transformers import SentenceTransformer  # type: ignore

    st = SentenceTransformer(model)
    q_emb = st.encode([query], normalize_embeddings=True)
    c_emb = st.encode(corpus, normalize_embeddings=True)
    scores = (c_emb @ q_emb.T).flatten()
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [(corpus[i], float(scores[i])) for i in top_idx]


# ---------------------------------------------------------------------------
# OpenAI LLM wrapper
# ---------------------------------------------------------------------------

def chat_completion(
    messages: list[dict[str, str]],
    model: str = "gpt-4o",
    temperature: float = 0.7,
) -> str:
    """Send *messages* to the OpenAI chat API and return the reply text."""
    import os
    from openai import OpenAI  # type: ignore

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Simple RAG helper
# ---------------------------------------------------------------------------

class RAGPipeline:
    """Minimal Retrieval-Augmented Generation pipeline."""

    def __init__(self, documents: list[str], embed_model: str = "all-MiniLM-L6-v2") -> None:
        import numpy as np
        from sentence_transformers import SentenceTransformer  # type: ignore

        self._docs = documents
        self._st = SentenceTransformer(embed_model)
        self._embeddings = self._st.encode(documents, normalize_embeddings=True)

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        import numpy as np

        q_emb = self._st.encode([query], normalize_embeddings=True)
        scores = (self._embeddings @ q_emb.T).flatten()
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [self._docs[i] for i in top_idx]

    def answer(self, query: str, top_k: int = 3) -> str:
        context = "\n\n".join(self.retrieve(query, top_k=top_k))
        messages = [
            {"role": "system", "content": "Answer using the context below.\n\n" + context},
            {"role": "user", "content": query},
        ]
        return chat_completion(messages)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog."
    tokens = simple_tokenize(text)
    logger.info("Tokens: %s", tokens)
    logger.info("Bigrams: %s", ngrams(tokens, n=2)[:5])

    labels = ["animal", "technology", "politics"]
    logger.info("Zero-shot labels to classify into: %s", labels)
    logger.info(
        "Note: set OPENAI_API_KEY and install 'transformers' to run full NLP examples."
    )
