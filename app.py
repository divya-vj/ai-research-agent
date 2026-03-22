# app.py — AI Research Assistant Agent
# Streamlit UI for the research agent

import streamlit as st
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # On HF Spaces, secrets are already in environment


# ── Page Config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main { background-color: #0E1117; }
[data-testid="stSidebar"] {
    background-color: #0D2B5E;
    border-right: 2px solid #1A56A8;
}
[data-testid="stSidebar"] * { color: #DCE8FA !important; }
h1 { color: #1A56A8 !important;
     border-bottom: 2px solid #1A56A8;
     padding-bottom: 8px; }
h2, h3 { color: #2A6ED4 !important; }
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1A56A8, #0D2B5E);
    border-radius: 10px;
    padding: 10px 16px;
    border: 1px solid #2A5FC8;
}
[data-testid="metric-container"] label { color: #A0C4FF !important; font-size: 12px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important; font-weight: 700 !important;
}
.stButton button {
    background-color: #1A56A8;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 24px;
    font-weight: 600;
}
.stButton button:hover { background-color: #0D2B5E; color: white; }
.stTextInput input {
    background-color: #1A1A2E;
    color: white;
    border: 1px solid #1A56A8;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────
st.sidebar.title("🔬 AI Research Agent")
st.sidebar.markdown("---")
st.sidebar.markdown("**How it works:**")
st.sidebar.markdown("1. Enter any research topic")
st.sidebar.markdown("2. Agent searches the web 3-5 times")
st.sidebar.markdown("3. Synthesises from multiple sources")
st.sidebar.markdown("4. Produces a structured report")
st.sidebar.markdown("5. Download as PDF or text")
st.sidebar.markdown("---")
st.sidebar.markdown("**Tech Stack:**")
st.sidebar.markdown("LangChain Agents · Tavily")
st.sidebar.markdown("Groq Llama-3.1 · ReAct")
st.sidebar.markdown("FPDF2 · Streamlit")
st.sidebar.markdown("---")

# Example topic buttons in sidebar
st.sidebar.markdown("**Example Topics:**")
examples = [
    "Generative AI trends in India 2026",
    "How do AI agents work?",
    "Best practices for prompt engineering",
    "LLM deployment strategies for production",
    "Explainable AI in healthcare 2026",
    "RAG vs fine-tuning for LLMs",
]
for ex in examples:
    if st.sidebar.button(ex, key=f"ex_{ex}"):
        st.session_state["topic_input"] = ex

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ── Main Page ─────────────────────────────────────────────────────────────
st.title("🔬 AI Research Assistant Agent")
st.markdown(
    "*Enter any topic. The agent autonomously searches the web, "
    "analyses multiple sources, and produces a structured research report.*"
)
st.markdown("---")


# ── Topic Input ───────────────────────────────────────────────────────────
topic = st.text_input(
    "Research Topic:",
    value=st.session_state.get("topic_input", ""),
    placeholder="e.g. Latest developments in agentic AI 2026",
    key="topic_box"
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    research_btn = st.button("🔬 Start Research", use_container_width=True)
with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ── Run Research ──────────────────────────────────────────────────────────
if research_btn and topic:

    st.markdown("---")

    # Progress message
    progress_box = st.empty()
    progress_box.markdown("""
    <div style="background:#0D2B5E; border:1px solid #1A56A8;
                padding:16px; border-radius:8px; margin-bottom:8px;">
    <b style="color:#A0C4FF">🤖 Agent is working...</b><br>
    <span style="color:#ccc; font-size:13px;">
    Searching the web · Reading sources · Synthesising findings<br>
    This takes 30–60 seconds. Watch the terminal to see the agent thinking.
    </span>
    </div>
    """, unsafe_allow_html=True)

    try:
        from agent import research_topic

        with st.spinner("Agent is researching..."):
            report = research_topic(topic)

        progress_box.empty()

        # Store in session state
        st.session_state["report"] = report
        st.session_state["topic"]  = topic

        st.success("✅ Research complete!")

    except Exception as e:
        progress_box.empty()
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure your GROQ_API_KEY and TAVILY_API_KEY are set in .env file")


# ── Display Report ─────────────────────────────────────────────────────────
if "report" in st.session_state:

    report = st.session_state["report"]
    topic  = st.session_state["topic"]

    st.markdown("---")

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Topic",   topic[:25] + "..." if len(topic) > 25 else topic)
    c2.metric("Words",   len(report.split()))
    c3.metric("Sources", report.count("https://"))
    c4.metric("Status",  "Complete ✅")

    st.markdown("---")

    # Report display
    st.subheader(f"📄 Research Report")
    clean_report = report.replace('\\n', '\n')
    st.markdown(clean_report)

    st.markdown("---")

    # Download options
    st.subheader("📥 Download Report")
    dl1, dl2 = st.columns(2)

    with dl1:
        st.download_button(
            label="📄 Download as Text (.txt)",
            data=report,
            file_name=f"research_{topic[:30].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with dl2:
        if st.button("🖨️ Generate PDF Download", use_container_width=True):
            try:
                from agent import save_report_as_pdf
                with st.spinner("Generating PDF..."):
                    pdf_file = save_report_as_pdf(topic, report)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="📥 Click to Download PDF",
                        data=f.read(),
                        file_name=pdf_file,
                        mime="application/pdf",
                        use_container_width=True
                    )
                # Clean up PDF file
                os.remove(pdf_file)
            except Exception as e:
                st.error(f"PDF error: {str(e)}")

    # Question history
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Add to history if not already there
    if not st.session_state["history"] or \
       st.session_state["history"][-1]["topic"] != topic:
        st.session_state["history"].append({
            "topic":  topic,
            "words":  len(report.split()),
            "sources": report.count("https://")
        })

    if len(st.session_state["history"]) > 1:
        st.markdown("---")
        st.subheader("🕐 Research History This Session")
        for i, h in enumerate(reversed(st.session_state["history"])):
            st.markdown(
                f"**{len(st.session_state['history'])-i}.** "
                f"{h['topic']} — "
                f"{h['words']} words · {h['sources']} sources"
            )


# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; font-size:12px; padding:8px'>
    AI Research Assistant · LangChain Agents · Tavily · Groq Llama-3.1 · Built by Divya VJ
</div>
""", unsafe_allow_html=True)