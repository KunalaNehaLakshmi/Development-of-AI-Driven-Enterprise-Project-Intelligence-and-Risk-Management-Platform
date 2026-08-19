"""
chatbot.py — LLM answer generation for the project RAG assistant.

Accepts pre-retrieved context chunks and generates a grounded answer
using the Gemini LLM. No vector DB dependencies here.
"""

from google import genai

from . import config

_client = None

SYSTEM_INSTRUCTION = (
    "You are a project intelligence assistant. Answer the user's question "
    "using ONLY the provided project document excerpts below. "
    "If the excerpts don't contain enough information to answer confidently, "
    "say so clearly rather than guessing. "
    "Cite which source document(s) you used. "
    "Keep answers concise, specific, and grounded in the project data."
)


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        config.validate_config()
        _client = genai.Client(api_key=config.GEMINI_API_KEY)
    return _client


def _build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a labeled context block."""
    blocks = []
    for i, c in enumerate(chunks, start=1):
        blocks.append(
            f"[Source {i}: {c['filename']}, section {c['chunk_index']}]\n{c['text']}"
        )
    return "\n\n".join(blocks)


def _build_prompt(question: str, context: str) -> str:
    return (
        f"Project document excerpts:\n{'-' * 40}\n{context}\n{'-' * 40}\n\n"
        f"Question: {question}\n\n"
        f"Answer based only on the excerpts above."
    )


def answer_with_context(question: str, chunks: list[dict]) -> dict:
    """
    Generate an answer given pre-retrieved chunks.

    Parameters
    ----------
    question : The user's question string.
    chunks   : List of dicts from session_store.retrieve(), each with
               keys: text, filename, chunk_index, score.

    Returns
    -------
    dict with keys:
        answer   : str — the LLM-generated answer
        sources  : list[str] — unique source filenames used
    """
    if not chunks:
        return {
            "answer": (
                "I couldn't find anything in your uploaded documents relevant to that question. "
                "Make sure you have uploaded and processed a project document first."
            ),
            "sources": [],
        }

    context = _build_context(chunks)
    prompt = _build_prompt(question, context)

    client = _get_client()
    response = client.models.generate_content(
        model=config.GEMINI_LLM_MODEL,
        contents=prompt,
        config={"system_instruction": SYSTEM_INSTRUCTION},
    )

    return {
        "answer": response.text,
        "sources": sorted({c["filename"] for c in chunks}),
    }