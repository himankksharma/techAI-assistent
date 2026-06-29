import streamlit as st
import pickle
import numpy as np
from collections import Counter

st.set_page_config(
    page_title="ResearchAI",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, .stApp {
        background-color: #07070f;
        color: #c9d1d9;
        font-family: 'Inter', sans-serif;
    }
    header, footer, #MainMenu { visibility: hidden; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0f0f1e 0%, #12122a 100%);
        border: 1px solid #1e1e3f;
        border-radius: 10px;
        padding: 18px 22px;
        position: relative;
        overflow: hidden;
    }
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #7c3aed, #2563eb);
    }
    [data-testid="stMetricLabel"] {
        color: #6e7681 !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-size: 1.6rem !important;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .stButton > button {
        background: linear-gradient(135deg, #12122a 0%, #1a1a35 100%);
        color: #a78bfa;
        border: 1px solid #2d2d5e;
        border-radius: 8px;
        padding: 9px 16px;
        font-size: 0.82rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e1a3e 0%, #251f4e 100%);
        border-color: #7c3aed;
        color: #c4b5fd;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.2);
        transform: translateY(-1px);
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 1px solid #1a1a2e;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #6e7681;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 10px 22px;
        border-radius: 8px 8px 0 0;
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #a78bfa; background-color: #0f0f1e; }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #12122a 0%, transparent 100%) !important;
        color: #a78bfa !important;
        border-bottom: 2px solid #7c3aed !important;
    }
    [data-testid="stExpander"] {
        background: linear-gradient(135deg, #0d0d1a 0%, #0f0f20 100%);
        border: 1px solid #1a1a2e;
        border-radius: 10px;
    }
    [data-testid="stExpander"] summary { color: #8b949e; font-size: 0.83rem; }
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, #0d0d1a 0%, #0f0f20 100%);
        border: 1px solid #1a1a2e;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea textarea {
        background-color: #0d0d1a !important;
        border: 1px solid #1e1e3f !important;
        border-radius: 8px !important;
        color: #d1d5db !important;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.15) !important;
    }
    .stChatInput > div {
        background-color: #0d0d1a !important;
        border: 1px solid #1e1e3f !important;
        border-radius: 12px !important;
    }
    .stChatInput > div:focus-within {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.15) !important;
    }
    .settings-bar {
        background: linear-gradient(135deg, #0d0d1a 0%, #0f0f20 100%);
        border: 1px solid #1e1e3f;
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .source-card {
        background: linear-gradient(135deg, #0d0d1a 0%, #10101f 100%);
        border: 1px solid #1e1e3f;
        border-left: 3px solid #7c3aed;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        font-size: 0.84rem;
        line-height: 1.6;
    }
    .source-card:hover { border-left-color: #a78bfa; }
    .source-card b { color: #c4b5fd; font-weight: 600; }
    .source-meta {
        color: #4b5563;
        font-size: 0.76rem;
        margin-top: 5px;
        font-family: 'IBM Plex Mono', monospace;
    }
    .product-card {
        background: linear-gradient(135deg, #0a0f1a 0%, #0d1220 100%);
        border: 1px solid #1a2540;
        border-left: 3px solid #2563eb;
        border-radius: 10px;
        padding: 20px 24px;
        margin: 10px 0;
        line-height: 1.8;
        color: #c9d1d9;
        font-size: 0.88rem;
    }
    .product-section-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #2563eb;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .product-section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #1a2540, transparent);
    }
    .page-header {
        padding: 36px 0 20px 0;
        border-bottom: 1px solid #1a1a2e;
        margin-bottom: 28px;
    }
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #e2e8f0 0%, #a78bfa 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .page-subtitle { color: #4b5563; font-size: 0.88rem; margin-top: 6px; }
    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #4b5563;
        margin-bottom: 10px;
    }
    .status-ok   { color: #34d399; font-size: 0.78rem; font-family: 'IBM Plex Mono', monospace; }
    .status-warn { color: #f59e0b; font-size: 0.78rem; font-family: 'IBM Plex Mono', monospace; }
    hr { border: none; border-top: 1px solid #1a1a2e; margin: 20px 0; }
    .stSpinner > div { border-top-color: #7c3aed !important; }
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #07070f; }
    ::-webkit-scrollbar-thumb { background: #1a1a2e; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #2d2d5e; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_data():
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")
    with open("research_data.pkl", "rb") as f:
        data = pickle.load(f)
    return embedder, data

with st.spinner("Loading research database..."):
    embedder, data = load_data()

if isinstance(data["embeddings"], np.ndarray):
    data["embeddings"] = data["embeddings"].tolist()
if isinstance(data["documents"], np.ndarray):
    data["documents"] = data["documents"].tolist()
if isinstance(data["metadatas"], np.ndarray):
    data["metadatas"] = data["metadatas"].tolist()

total_chunks = len(data["documents"])
total_papers = len(set(m.get("title", "") for m in data["metadatas"]))
total_sources = len(set(m.get("source", "") for m in data["metadatas"]))


def search_papers(question, top_k=5):
    question_vec = embedder.encode([question])[0]
    embeddings = np.array(data["embeddings"])
    question_vec = question_vec / np.linalg.norm(question_vec)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    scores = np.dot(embeddings, question_vec)
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in top_indices:
        results.append({
            "text": data["documents"][idx],
            "metadata": data["metadatas"][idx],
            "score": float(scores[idx])
        })
    return [r for r in results if r["score"] > 0.3]


def call_model(system_prompt, user_prompt, model_choice, api_key, max_tokens=1500):
    if model_choice.startswith("Groq"):
        from groq import Groq
        client = Groq(api_key=api_key)
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            max_tokens=max_tokens, temperature=0.3
        )
        return r.choices[0].message.content

    elif model_choice.startswith("Claude"):
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        model = ("claude-opus-4-6" if "Opus" in model_choice
                 else "claude-sonnet-4-6" if "Sonnet" in model_choice
                 else "claude-haiku-4-5-20251001")
        r = client.messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}]
        )
        return r.content[0].text

    elif model_choice.startswith("GPT"):
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        model = ("gpt-4o" if "4o" in model_choice
                 else "gpt-4-turbo" if "4" in model_choice
                 else "gpt-3.5-turbo")
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            max_tokens=max_tokens, temperature=0.3
        )
        return r.choices[0].message.content

    elif model_choice.startswith("Gemini"):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(
            "gemini-1.5-pro" if "Pro" in model_choice else "gemini-1.5-flash"
        )
        return m.generate_content(f"{system_prompt}\n\n{user_prompt}").text


def get_answer(question, results, model_choice, api_key):
    context = "".join(
        f"[{i+1}] Title: {r['metadata'].get('title','N/A')}\n"
        f"     Authors: {r['metadata'].get('authors','N/A')}\n"
        f"     Year: {r['metadata'].get('year','N/A')}\n"
        f"     Text: {r['text']}\n\n"
        for i, r in enumerate(results)
    )
    system = """You are ResearchAI, a precise and professional research assistant.
Answer using ONLY the provided research paper context.
Cite every claim with [1], [2] notation.
Be thorough, structured, and authoritative.
If insufficient context: 'The indexed papers do not contain sufficient information on this topic.'"""
    return call_model(system, f"Context:\n{context}\nQuestion: {question}\nAnswer:", model_choice, api_key)


def get_product_ideas(question, results, model_choice, api_key):
    context = "".join(
        f"[{i+1}] {r['metadata'].get('title','N/A')}\n     {r['text'][:250]}\n\n"
        for i, r in enumerate(results)
    )
    system = """You are a seasoned product strategist and technology executive with 10+ years of experience
taking research insights to market."""
    user = f"""You've just reviewed research papers on: "{question}".
Identify 3 high-potential product opportunities.

Research context:
{context}

For each product:
PRODUCT [N]: [Name]
Opportunity: Market gap and why now?
What it does: 2-3 sentence description.
Target customer: Specific role, company size, industry.
Competitive edge: Why is it defensible?
Tech stack: Core technologies for MVP.
Build complexity: Beginner / Intermediate / Advanced — one-line justification.
Revenue model: How does it make money?"""
    return call_model(system, user, model_choice, api_key, max_tokens=2000)


# ── HEADER ──
st.markdown("""
<div class="page-header">
    <div class="page-title">ResearchAI</div>
    <div class="page-subtitle">
        Semantic search and AI-powered analysis across indexed research papers —
        with product intelligence built in.
    </div>
</div>
""", unsafe_allow_html=True)

# ── SETTINGS BAR (replaces sidebar) ──
with st.expander("⚙️  Settings — Model & API Key", expanded=False):
    col_a, col_b, col_c = st.columns([2, 3, 2])
    with col_a:
        st.markdown('<div class="section-label">AI Model</div>', unsafe_allow_html=True)
        model_choice = st.selectbox("Model", [
            "Groq — Llama 3.3 70B",
            "Claude Haiku", "Claude Sonnet", "Claude Opus",
            "GPT-3.5 Turbo", "GPT-4 Turbo", "GPT-4o",
            "Gemini Flash", "Gemini Pro"
        ], label_visibility="collapsed")
    with col_b:
        provider_map = {
            "Groq":   ("Groq API Key",      "gsk_...",   "console.groq.com"),
            "Claude": ("Anthropic API Key", "sk-ant-...", "console.anthropic.com"),
            "GPT":    ("OpenAI API Key",    "sk-...",     "platform.openai.com"),
            "Gemini": ("Google API Key",    "AIza...",    "aistudio.google.com"),
        }
        prefix = next((k for k in provider_map if model_choice.startswith(k)), "Groq")
        label, placeholder, url = provider_map[prefix]
        st.markdown('<div class="section-label">API Key</div>', unsafe_allow_html=True)
        api_key = st.text_input(label, type="password", placeholder=placeholder, label_visibility="collapsed")
        st.markdown(
            f'<div style="font-size:0.73rem; color:#4b5563; margin-top:4px;">'
            f'Get key → <a href="https://{url}" target="_blank" style="color:#7c3aed;">{url}</a></div>',
            unsafe_allow_html=True
        )
    with col_c:
        st.markdown('<div class="section-label">Status</div>', unsafe_allow_html=True)
        if api_key:
            st.markdown('<div class="status-ok">● API key configured</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warn">● No API key set</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.75rem; color:#4b5563; margin-top:6px;">Model: {model_choice.split("—")[0].strip()}</div>', unsafe_allow_html=True)

# ── METRICS ──
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Papers indexed", f"{total_papers:,}")
with col2: st.metric("Total chunks",   f"{total_chunks:,}")
with col3: st.metric("Sources",        f"{total_sources:,}")
with col4: st.metric("Active model",   model_choice.split("—")[0].strip())

st.markdown("<hr>", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3 = st.tabs(["Search & Ask", "Upload Papers", "Database Info"])

# ── TAB 1 ──
with tab1:
    st.markdown(
        '<div class="section-label" style="margin-bottom:16px;">'
        'Ask a question — answers and product opportunities are returned together'
        '</div>', unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Latest AI breakthroughs"):
            st.session_state.sample_q = "What are the latest breakthroughs in artificial intelligence?"
    with col2:
        if st.button("Cybersecurity trends"):
            st.session_state.sample_q = "What are the latest trends in cybersecurity?"
    with col3:
        if st.button("Quantum computing state"):
            st.session_state.sample_q = "What is the current state of quantum computing research?"

    st.markdown("<hr>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sample_q" not in st.session_state:
        st.session_state.sample_q = None

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                with st.expander(f"View sources — {len(msg['sources'])} papers matched"):
                    for i, r in enumerate(msg["sources"]):
                        relevance = round(r["score"] * 100)
                        st.markdown(f"""
                        <div class="source-card">
                            <b>[{i+1}] {r['metadata'].get('title','N/A')[:85]}</b>
                            <div class="source-meta">
                                {r['metadata'].get('authors','N/A')[:55]}
                                &nbsp;&middot;&nbsp; {r['metadata'].get('year','N/A')}
                                &nbsp;&middot;&nbsp; {r['metadata'].get('source','N/A')}
                                &nbsp;&middot;&nbsp; {relevance}% match
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            if msg.get("ideas"):
                with st.expander("Product opportunities identified from this research"):
                    st.markdown('<div class="product-section-label">Product Intelligence</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-card">{msg["ideas"]}</div>', unsafe_allow_html=True)

    question = st.chat_input("Ask a research question...")
    if st.session_state.sample_q:
        question = st.session_state.sample_q
        st.session_state.sample_q = None

    if question:
        if not api_key:
            st.error("Expand the ⚙️ Settings panel above and enter your API key to continue.")
        else:
            with st.chat_message("user"):
                st.write(question)
            st.session_state.messages.append({"role": "user", "content": question})

            with st.chat_message("assistant"):
                with st.spinner("Searching papers..."):
                    results = search_papers(question)

                if not results:
                    answer = "No relevant papers found. Try rephrasing or broadening your question."
                    st.write(answer)
                    st.session_state.messages.append({
                        "role": "assistant", "content": answer,
                        "sources": [], "ideas": None
                    })
                else:
                    try:
                        with st.spinner(f"Generating answer..."):
                            answer = get_answer(question, results, model_choice, api_key)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("Check your API key in the Settings panel above.")
                        st.stop()

                    try:
                        with st.spinner("Analysing product opportunities..."):
                            ideas = get_product_ideas(question, results, model_choice, api_key)
                    except Exception:
                        ideas = None

                    st.write(answer)

                    with st.expander(f"View sources — {len(results)} papers matched"):
                        for i, r in enumerate(results):
                            relevance = round(r["score"] * 100)
                            st.markdown(f"""
                            <div class="source-card">
                                <b>[{i+1}] {r['metadata'].get('title','N/A')[:85]}</b>
                                <div class="source-meta">
                                    {r['metadata'].get('authors','N/A')[:55]}
                                    &nbsp;&middot;&nbsp; {r['metadata'].get('year','N/A')}
                                    &nbsp;&middot;&nbsp; {r['metadata'].get('source','N/A')}
                                    &nbsp;&middot;&nbsp; {relevance}% match
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    if ideas:
                        with st.expander("Product opportunities identified from this research"):
                            st.markdown('<div class="product-section-label">Product Intelligence</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="product-card">{ideas}</div>', unsafe_allow_html=True)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": results,
                        "ideas": ideas
                    })

    if st.session_state.get("messages"):
        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.rerun()


# ── TAB 2 ──
with tab2:
    st.markdown(
        '<div style="color:#4b5563; font-size:0.85rem; margin-bottom:20px;">'
        'Upload PDF files to extend the search database.'
        '</div>', unsafe_allow_html=True
    )
    uploaded_files = st.file_uploader(
        "Select PDF files", type="pdf",
        accept_multiple_files=True, label_visibility="collapsed"
    )
    if uploaded_files:
        st.markdown(f'<div style="font-size:0.8rem; color:#6e7681; margin:8px 0;">{len(uploaded_files)} file(s) selected</div>', unsafe_allow_html=True)
        if st.button("Process and add to database"):
            import fitz
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            total_added = 0
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    text = "".join(page.get_text() for page in doc)
                    splits = splitter.split_text(text)
                    new_embeddings = embedder.encode(splits).tolist()
                    for chunk, emb in zip(splits, new_embeddings):
                        data["documents"].append(chunk)
                        data["embeddings"].append(emb)
                        data["metadatas"].append({
                            "title": uploaded_file.name,
                            "source": "PDF Upload",
                            "year": "N/A",
                            "journal": "Uploaded",
                            "authors": "N/A"
                        })
                    total_added += len(splits)
                    st.success(f"{uploaded_file.name} — {len(splits)} chunks added.")
            st.success(f"Done. {total_added} chunks added from {len(uploaded_files)} file(s).")


# ── TAB 3 ──
with tab3:
    st.markdown('<div class="section-label">Source breakdown</div>', unsafe_allow_html=True)
    source_counts = Counter(m.get("source", "Unknown") for m in data["metadatas"])
    for source, count in source_counts.items():
        pct = round(count / total_chunks * 100)
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#8b949e; margin-bottom:4px;">
                <span>{source}</span>
                <span style="font-family:'IBM Plex Mono',monospace; color:#6e7681;">{count} chunks ({pct}%)</span>
            </div>
            <div style="background:#1a1a2e; border-radius:3px; height:4px;">
                <div style="background:linear-gradient(90deg,#7c3aed,#2563eb); width:{pct}%; height:4px; border-radius:3px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)