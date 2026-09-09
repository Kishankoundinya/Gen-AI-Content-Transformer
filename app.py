"""
Gen AI Content Transformer - Main Dashboard Application
A Streamlit-based UI for transforming source content into multiple output formats
using TinyLlama running locally (offline).
"""

import streamlit as st
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model_loader import load_model, get_model_info
from output_generators import generate_output
from prompt_templates import PROMPT_BUILDERS

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gen AI Content Transformer",
    page_icon="transformer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Initialize Session State ────────────────────────────────────────────────
if "generated_results" not in st.session_state:
    st.session_state.generated_results = []
if "generation_history" not in st.session_state:
    st.session_state.generation_history = []
if "generating" not in st.session_state:
    st.session_state.generating = False

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">Gen AI Content Transformer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Transform your source content into multiple professional formats using AI &mdash; runs 100% offline</div>',
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Model & Settings")

    st.subheader("AI Model")
    model_info = get_model_info()
    st.write(f"**Model:** {model_info['name']}")
    st.write(f"**Parameters:** {model_info['parameters']}")
    st.write(f"**Architecture:** {model_info['architecture']}")
    st.write(f"**Precision:** {model_info['quantization']}")
    st.write(f"**Context Window:** {model_info['max_context']}")

    st.divider()

    st.subheader("Generation Parameters")
    max_tokens = st.slider(
        "Max Output Tokens",
        min_value=256,
        max_value=2048,
        value=1024,
        step=128,
        help="Maximum tokens to generate. TinyLlama has 2048 total context.",
    )
    temperature = st.slider(
        "Temperature",
        min_value=0.1,
        max_value=1.5,
        value=0.7,
        step=0.05,
        help="Controls randomness. Lower = more focused, higher = more creative.",
    )
    top_p = st.slider(
        "Top-P",
        min_value=0.1,
        max_value=1.0,
        value=0.9,
        step=0.05,
        help="Nucleus sampling threshold.",
    )

    st.divider()

    st.subheader("Model Status")
    if st.button("Load / Reload Model", use_container_width=True):
        with st.spinner("Loading model into memory..."):
            load_model()
        st.success("Model loaded successfully!")

# ── Main Layout: Two Columns ────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1])

# ══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN: INPUT
# ══════════════════════════════════════════════════════════════════════════════
with col_input:
    st.header("Source Content")

    input_method = st.radio(
        "Input Method",
        ["Text Input", "Upload File"],
        horizontal=True,
    )

    source_content = ""

    if input_method == "Text Input":
        source_content = st.text_area(
            "Enter your source content",
            height=300,
            placeholder="Paste your article, report, prompt, or any text content here...",
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["txt", "pdf", "docx", "md"],
        )
        if uploaded_file is not None:
            st.info(f"Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

            if uploaded_file.name.endswith((".txt", ".md")):
                source_content = uploaded_file.read().decode("utf-8")
            elif uploaded_file.name.endswith(".pdf"):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                    pages = [p.extract_text() for p in reader.pages if p.extract_text()]
                    source_content = "\n\n".join(pages)
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
            elif uploaded_file.name.endswith(".docx"):
                try:
                    from docx import Document
                    doc = Document(io.BytesIO(uploaded_file.read()))
                    source_content = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
                except Exception as e:
                    st.error(f"Error reading DOCX: {e}")

            if source_content:
                with st.expander("Preview extracted content", expanded=False):
                    st.text_area("Content Preview", source_content, height=200, disabled=True)

    st.divider()

    # ── Output Type Selection ────────────────────────────────────────────────
    st.header("Output Types")
    st.write("Select one or more output formats:")

    output_options = list(PROMPT_BUILDERS.keys())
    selected_outputs = []

    cols = st.columns(3)
    for i, option in enumerate(output_options):
        with cols[i % 3]:
            if st.checkbox(option, key=f"cb_{option}"):
                selected_outputs.append(option)

    st.divider()

    # ── Generation Parameters ────────────────────────────────────────────────
    st.header("Content Parameters")

    col_a, col_b = st.columns(2)
    with col_a:
        audience = st.text_input("Target Audience", value="general professional audience")
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Formal", "Conversational", "Authoritative",
             "Friendly", "Persuasive", "Inspirational", "Technical", "Humorous"],
            index=0,
        )
        language = st.text_input("Language", value="English")

    with col_b:
        detail_level = st.selectbox(
            "Level of Detail",
            ["Very Concise", "Concise", "Moderate", "Comprehensive", "Very Detailed"],
            index=2,
        )
        objective = st.text_input("Communication Objective", value="inform and engage")
        style = st.text_input("Content Style", value="professional")

    st.divider()

    # ── Generate Button ──────────────────────────────────────────────────────
    generate_disabled = not source_content.strip() or not selected_outputs

    if st.button(
        "Generate Content",
        type="primary",
        use_container_width=True,
        disabled=generate_disabled,
    ):
        if not source_content.strip():
            st.warning("Please provide source content.")
        elif not selected_outputs:
            st.warning("Please select at least one output type.")
        else:
            st.session_state.generated_results = []

            for output_type in selected_outputs:
                with st.spinner(f"Generating {output_type}..."):
                    result = generate_output(
                        output_type=output_type,
                        source_content=source_content,
                        audience=audience,
                        tone=tone,
                        language=language,
                        detail_level=detail_level,
                        objective=objective,
                        style=style,
                        max_new_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                    )
                    st.session_state.generated_results.append(result)

            success_count = sum(1 for r in st.session_state.generated_results if r["status"] == "success")
            fail_count = len(st.session_state.generated_results) - success_count

            st.session_state.generation_history.append({
                "input_preview": source_content[:200],
                "outputs": [r["type"] for r in st.session_state.generated_results],
                "success": success_count,
                "failed": fail_count,
            })

            if success_count > 0:
                st.success(f"Generated {success_count} output(s) successfully!")
            if fail_count > 0:
                for r in st.session_state.generated_results:
                    if r["status"] != "success":
                        st.error(f"Failed to generate {r['type']}: {r['status']}")

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN: OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
with col_output:
    st.header("Generated Content")

    if not st.session_state.generated_results:
        st.info(
            "No content generated yet. Add source content on the left, "
            "select output types, and click **Generate Content**."
        )

        with st.expander("Supported Output Types", expanded=True):
            capabilities = {
                "Video": "Script, storyboard, scene descriptions, narration, subtitles, visual recommendations.",
                "LinkedIn Post": "Professional post ready to publish.",
                "Twitter/X Post": "Tweet and tweet thread formats.",
                "Advisory": "Structured advisory document with recommendations.",
                "Infographic": "Content, layout recommendations, key messaging.",
                "Executive Summary": "Concise executive briefing.",
                "Presentation": "Slides with speaker notes and design tips.",
            }
            for name, desc in capabilities.items():
                st.markdown(f"**{name}**: {desc}")
    else:
        results = st.session_state.generated_results
        success_results = [r for r in results if r["status"] == "success"]

        if not success_results:
            st.warning("Generation completed but produced no usable output. Try:")
            st.write("- Shorter source content")
            st.write("- Fewer output types at once")
            st.write("- Different temperature setting")
            for r in results:
                if r["status"] != "success":
                    st.error(f"{r['type']}: {r['status']}")
        elif len(success_results) == 1:
            result = success_results[0]
            st.markdown(f"### {result['type']}")
            st.markdown(result["content"])

            with st.expander("View prompt used"):
                st.code(result["prompt_used"], language="text")

            st.download_button(
                label=f"Download {result['type']}",
                data=result["content"],
                file_name=f"{result['type'].lower().replace('/', '_').replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            tabs = st.tabs([r["type"] for r in success_results])
            for tab, result in zip(tabs, success_results):
                with tab:
                    st.markdown(result["content"])

                    with st.expander("View prompt used"):
                        st.code(result["prompt_used"], language="text")

                    st.download_button(
                        label=f"Download {result['type']}",
                        data=result["content"],
                        file_name=f"{result['type'].lower().replace('/', '_').replace(' ', '_')}.md",
                        mime="text/markdown",
                        key=f"dl_{result['type']}",
                        use_container_width=True,
                    )

            # Download all
            st.divider()
            all_content = ""
            for r in success_results:
                all_content += f"# {r['type']}\n\n{r['content']}\n\n---\n\n"
            if all_content:
                st.download_button(
                    label="Download All Outputs",
                    data=all_content,
                    file_name="all_outputs.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        # Show failed results
        failed_results = [r for r in results if r["status"] != "success"]
        if failed_results:
            with st.expander(f"Failed Outputs ({len(failed_results)})", expanded=False):
                for r in failed_results:
                    st.error(f"**{r['type']}**: {r['status']}")

        # Generation History
        if st.session_state.generation_history:
            st.divider()
            with st.expander("Generation History", expanded=False):
                for i, entry in enumerate(reversed(st.session_state.generation_history)):
                    idx = len(st.session_state.generation_history) - i
                    status = f"({entry['success']} ok, {entry['failed']} failed)"
                    st.write(f"**Run {idx}:** {', '.join(entry['outputs'])} {status}")
                    st.caption(f"Input: {entry['input_preview'][:100]}...")

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Powered by TinyLlama-1.1B-Chat-v1.0 | All processing happens locally | No data sent to external servers"
)
