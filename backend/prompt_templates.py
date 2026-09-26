"""
Compact prompt templates for all supported output types.
Kept short to fit TinyLlama's 2048-token context window.
"""


def _ctx(audience, tone, language, detail_level, objective, style):
    parts = []
    if audience:
        parts.append(f"Audience: {audience}")
    if tone:
        parts.append(f"Tone: {tone}")
    if language and language != "English":
        parts.append(f"Language: {language}")
    if detail_level:
        parts.append(f"Detail: {detail_level}")
    if objective:
        parts.append(f"Goal: {objective}")
    if style:
        parts.append(f"Style: {style}")
    return " | ".join(parts) if parts else ""


def _source(content):
    return content[:1400]


def video_prompt(source_content, audience="", tone="", language="English",
                 detail_level="", objective="", style=""):
    ctx = _ctx(audience, tone, language, detail_level, objective, style)
    return f"""Create a video production package from this content. {ctx}

Content: {_source(source_content)}

Generate these sections:

VIDEO SCRIPT:
Write a full narration script with timing markers for each scene.

STORYBOARD:
For each scene: scene number, visual description, camera angle, duration.

SCENE DESCRIPTIONS:
Setting, characters, props, lighting, mood for each scene.

NARRATION TEXT:
Complete voiceover script with natural pauses marked.

SUBTITLES:
SRT-style subtitle text with timestamps.

VISUAL RECOMMENDATIONS:
Color palette, typography, graphics, stock footage suggestions, music/sound effects."""


def linkedin_prompt(source_content, audience="professionals", tone="professional",
                    language="English", detail_level="concise",
                    objective="thought leadership", style="social media"):
    ctx = _ctx(audience, tone, language, detail_level, objective, style)
    return f"""Write a professional LinkedIn post from this content. {ctx}

Content: {_source(source_content)}

Requirements:
- Compelling hook line that stops the scroll
- Short paragraphs with line breaks for readability
- Clear call-to-action or question at end
- 3-5 relevant hashtags
- 150-300 words, ready to publish on LinkedIn"""


def twitter_prompt(source_content, audience="general", tone="concise",
                   language="English", detail_level="very concise",
                   objective="engagement", style="social media"):
    ctx = _ctx(audience, tone, language, detail_level, objective, style)
    return f"""Create Twitter/X posts from this content. {ctx}

Content: {_source(source_content)}

Generate:

SINGLE TWEET: Max 280 characters capturing the key message.

TWEET THREAD (4-6 tweets):
1/ Hook tweet
2-5/ Value-adding tweets
6/ CTA or summary
Each under 280 characters with 2-3 hashtags.

ENGAGEMENT TWEET: A question or bold take to maximize replies."""


def advisory_prompt(source_content, audience="decision makers", tone="authoritative",
                    language="English", detail_level="comprehensive",
                    objective="inform decisions", style="formal advisory"):
    ctx = _ctx(audience, tone, language, detail_level, objective, style)
    return f"""Create a structured advisory document from this content. {ctx}

Content: {_source(source_content)}

Structure:
EXECUTIVE BRIEF: 2-3 sentence overview.
CONTEXT: Background and situational analysis.
KEY FINDINGS: Bullet-pointed findings.
RISK ASSESSMENT: Risks and concerns.
RECOMMENDATIONS: Numbered with priority (High/Medium/Low).
IMPLEMENTATION: Steps to implement recommendations.
CONCLUSION: Closing summary."""


def infographic_prompt(source_content, audience="general", tone="clear",
                       language="English", detail_level="moderate",
                       objective="simplify information", style="infographic"):
    ctx = _ctx(audience, tone, language, detail_level, objective, style)
    return f"""Create infographic content from this content. {ctx}

Content: {_source(source_content)}

Generate:
TITLE: Catchy attention-grabbing title.
KEY DATA: 5-8 key statistics or data points.
SECTIONS: 4-6 visual sections with title, key message, supporting data.
LAYOUT: Layout structure, color scheme, icons, fonts.
MESSAGING: Primary headline, 3 supporting messages, CTA.
DESIGN NOTES: Technical specs and design tips."""


def executive_summary_prompt(source_content, audience="senior leadership",
                             tone="concise", language="English",
                             detail_level="brief", objective="quick overview",
                             style="executive briefing"):
    ctx = _ctx(audience, tone, language, detail_level, objective, style)
    return f"""Create an executive summary from this content. {ctx}

Content: {_source(source_content)}

Structure (under 400 words total):
PURPOSE: One sentence on what this covers.
KEY POINTS: 3-5 bullet points of critical information.
IMPACT: Financial, operational, or strategic impacts.
RECOMMENDATIONS: Top 3 prioritized recommendations.
NEXT STEPS: Immediate actions with owners and timelines."""


def presentation_prompt(source_content, audience="professional audience",
                        tone="engaging", language="English",
                        detail_level="moderate", objective="inform and persuade",
                        style="presentation"):
    ctx = _ctx(audience, tone, language, detail_level, objective, style)
    return f"""Create a presentation deck from this content. {ctx}

Content: {_source(source_content)}

Generate 8-10 slides:
SLIDE 1: Title slide with subtitle
SLIDE 2: Agenda/overview
SLIDES 3-8: For each: Title, 3-5 key bullet points, Speaker notes
FINAL SLIDE: Key takeaways and Q&A prompt

Include design recommendations for each slide."""


PROMPT_BUILDERS = {
    "Video": video_prompt,
    "LinkedIn Post": linkedin_prompt,
    "Twitter/X Post": twitter_prompt,
    "Advisory": advisory_prompt,
    "Infographic": infographic_prompt,
    "Executive Summary": executive_summary_prompt,
    "Presentation": presentation_prompt,
}