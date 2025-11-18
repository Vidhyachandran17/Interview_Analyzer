def generate_summary(text):
    """
    Generates a short summary of the user's interview answer.
    Rule-based simple summary.
    """
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    # If answer is short
    if len(text.split()) < 15:
        return "The response is brief but clearly expresses the main message."

    # If multiple sentences exist
    if len(sentences) > 1:
        return sentences[0] + "."
    
    # Fallback summary
    return "The answer describes the candidate's confidence and intent."
