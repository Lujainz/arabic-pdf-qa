SYSTEM_INSTRUCTION = """أنت مساعد متخصص في الإجابة على الأسئلة بناءً على وثائق محددة.
أجب على السؤال باللغة العربية فقط بناءً على السياق التالي.
إذا لم يكن السياق كافياً للإجابة على السؤال، قل ذلك بوضوح ولا تخترع معلومات.
اذكر رقم الصفحة المستخدمة في إجابتك عند الإمكان."""


def build_prompt(question: str, chunks: list[dict]) -> str:
    """
    Builds the full prompt sent to Claude: system instruction + numbered
    context chunks (with page numbers) + the user's question.
    """
    context_sections = []
    for i, chunk in enumerate(chunks, start=1):
        context_sections.append(
            f"[مقطع {i} - صفحة {chunk['page_number']}]\n{chunk['text']}"
        )

    context_block = "\n\n".join(context_sections)

    return f"""{SYSTEM_INSTRUCTION}

السياق:
{context_block}

السؤال: {question}"""