"""
Output generators that orchestrate prompt building and model inference.
Each generator returns structured output for a specific content type.
"""

import traceback
from prompt_templates import PROMPT_BUILDERS
from model_loader import generate_text


def generate_output(
    output_type: str,
    source_content: str,
    audience: str = "",
    tone: str = "",
    language: str = "English",
    detail_level: str = "",
    objective: str = "",
    style: str = "",
    max_new_tokens: int = 2048,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> dict:
    """
    Generate content for a specific output type.

    Returns:
        dict with keys: 'type', 'content', 'prompt_used', 'status'
    """
    if output_type not in PROMPT_BUILDERS:
        return {
            "type": output_type,
            "content": "",
            "prompt_used": "",
            "status": f"error: Unknown output type '{output_type}'",
        }

    if not source_content.strip():
        return {
            "type": output_type,
            "content": "",
            "prompt_used": "",
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
                "type": output_type,
                "content": "",
                "prompt_used": prompt,
                "status": "error: Model produced empty or too-short output. Try increasing max tokens or lowering temperature.",
            }

        return {
            "type": output_type,
            "content": result,
            "prompt_used": prompt,
            "status": "success",
        }
    except Exception as e:
        tb = traceback.format_exc()
        error_msg = str(e)
        if "out of memory" in error_msg.lower() or "oom" in error_msg.lower():
            error_msg += " Try reducing max tokens or closing other applications."
        elif "index out of range" in error_msg.lower():
            error_msg += " Token limit exceeded. Try shorter source content or fewer output types."
        return {
            "type": output_type,
            "content": "",
            "prompt_used": prompt,
            "status": f"error: {error_msg}",
        }
