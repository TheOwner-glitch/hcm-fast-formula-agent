def build_prompt(logic, inputs, original):
    return (
        "You are an Oracle HCM Fast Formula expert.\n"
        "Summarize the following Fast Formula in 2-3 key bullet points:\n\n"
        f"{original}\n\n"
        "Each bullet point should focus on what the formula is doing."
    )
