"""
Output generation orchestration for the API.
"""

from .prompt_templates import PROMPT_BUILDERS
from .model_service import generate_text


def generate_output(
    output_type: str,
    source_content: str,
    audience: str = "",
    tone: str = "",
    language: str = "English",
    detail_level: str = "",
    objective: str = "",
    style: str = "",
    max_new_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> dict:
    """
    Generate content for a specific output type.

    Returns:
        dict with keys: 'output_type', 'content', 'status'
    """
    if output_type not in PROMPT_BUILDERS:
        return {
            "output_type": output_type,
            "content": "",
            "status": f"error: Unknown output type '{output_type}'",
        }

    if not source_content or not source_content.strip():
        return {
            "output_type": output_type,
            "content": "",
            "status": "error: Source content is empty",
        }

    builder = PROMPT_BUILDERS[output_type]
    prompt = builder(source_content, audience, tone, language, detail_level, objective, style)

    try:
        result = generate_text(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
        )

        if not result or len(result.strip()) < 10:
            return {
                "output_type": output_type,
                "content": "",
                "status": "error: Model produced too little output. Try shorter content or lower temperature.",
            }

        return {
            "output_type": output_type,
            "content": result,
            "status": "success",
        }
    except Exception as e:
        return {
            "output_type": output_type,
            "content": "",
            "status": f"error: {str(e)}",
        }