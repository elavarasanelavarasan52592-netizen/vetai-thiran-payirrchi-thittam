from config import settings
from gemini_client import generate_text


def _local_explain(topic: str) -> str:
    # Loaded lazily so the normal lightweight Gemini setup does not download
    # a large model during installation or startup.
    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model=settings.local_explainer_model,
        max_length=300,
    )
    prompt = (
        "Explain the following educational topic simply for a beginner. "
        "Use short paragraphs and one example.\n\n"
        f"Topic: {topic}"
    )
    result = generator(prompt, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    if settings.local_explainer_enabled:
        try:
            return _local_explain(topic)
        except Exception:
            # Keep the application usable if the optional local model is not
            # available on the machine.
            pass

    prompt = (
        "You are EduGenie, a patient educational tutor. Explain the topic below "
        "for a beginner using simple language. Include: definition, 3-5 key points, "
        "one everyday or academic example, and a one-line recap. Avoid unnecessary jargon.\n\n"
        f"Topic: {topic}"
    )
    return generate_text(prompt, temperature=0.25, max_output_tokens=900)
