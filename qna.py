from gemini_client import generate_text


def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")

    prompt = (
        "You are EduGenie, an educational question-answering assistant. "
        "Answer the student's question accurately and concisely. "
        "If the question is ambiguous, state the assumption you used. "
        "For calculations, show the important steps. Do not invent sources.\n\n"
        f"Student question: {question}"
    )
    return generate_text(prompt, temperature=0.2, max_output_tokens=900)
