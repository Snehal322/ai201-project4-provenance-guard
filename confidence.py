def combine_scores(llm_score, style_score):

    confidence = round(
        (0.6 * llm_score) +
        (0.4 * style_score),
        2
    )

    return confidence


def get_label(confidence):

    if confidence >= 0.70:

        return (
            "likely_ai",
            "Likely AI-generated. Our system found strong evidence that this content was generated using AI."
        )

    elif confidence <= 0.30:

        return (
            "likely_human",
            "Likely written by a human. Our system found strong evidence that this content was written by a person."
        )

    else:

        return (
            "uncertain",
            "Unable to determine confidently. The available evidence is mixed."
        )