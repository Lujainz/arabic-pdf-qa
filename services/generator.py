import logging
from anthropic import Anthropic
from core.config import settings

logger = logging.getLogger(__name__)
client = Anthropic(api_key=settings.anthropic_api_key)

MODEL = "claude-sonnet-4-6"

NO_CONTEXT_MESSAGE = "لم أجد معلومات كافية في الوثيقة للإجابة على هذا السؤال."

# Rough public pricing reference for cost estimate logging (USD per 1M tokens).
# Update if pricing changes — this is just for visibility, not billing accuracy.
INPUT_COST_PER_MILLION = 3.00
OUTPUT_COST_PER_MILLION = 15.00


def generate_answer(prompt: str) -> dict:
    """
    Sends the prompt to Claude and returns the answer along with token usage.
    Logs token counts and an estimated cost for every call.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    answer_text = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    estimated_cost = (
        (input_tokens / 1_000_000) * INPUT_COST_PER_MILLION
        + (output_tokens / 1_000_000) * OUTPUT_COST_PER_MILLION
    )

    logger.info(
        f"Claude call — input_tokens={input_tokens}, output_tokens={output_tokens}, "
        f"estimated_cost=${estimated_cost:.5f}"
    )

    return {
        "answer": answer_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_usd": round(estimated_cost, 5),
    }