from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty.")

    prompt = (
        "Summarize the educational passage below for quick revision. "
        "Retain the core facts and important relationships, remove repetition, "
        "and use clear bullet points followed by a one-sentence recap. "
        "Do not add facts that are not supported by the passage.\n\n"
        f"Passage:\n{text}"
    )
    return generate_text(prompt, temperature=0.2, max_output_tokens=1000)
