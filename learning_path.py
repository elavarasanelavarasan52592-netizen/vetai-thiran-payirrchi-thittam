from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    prompt = (
        "Create a personalized learning path for the topic below. Assume the learner "
        "is a beginner unless stated otherwise. Organize it from beginner to advanced. "
        "For each stage include concepts, a suggested time range, a small practice task, "
        "and resource types such as official documentation, articles, videos, or books. "
        "Keep the plan practical and concise. Do not fabricate specific URLs.\n\n"
        f"Topic: {topic}"
    )
    return generate_text(prompt, temperature=0.35, max_output_tokens=1400)
