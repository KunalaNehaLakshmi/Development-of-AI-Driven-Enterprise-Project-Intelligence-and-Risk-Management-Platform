import streamlit as st
from utils.ui import inject_css, page_header, render_domain_banner

inject_css()

page_header(
    "AI Project Knowledge Assistant (RAG)",
    "Conversational assistant grounded strictly in your uploaded project documents, work package specs, and meeting notes."
)

# ============================================================
# GUARD & STATUS
# ============================================================

project = st.session_state.get("selected_project", {})
project_name = project.get("name", "Active Project") if project else "Active Project"
rag_ready = st.session_state.get("rag_ready", False)
documents = st.session_state.get("documents", {})

if not project and not documents:
    st.warning("No project document ingested yet. Please ingest a project document or reference dataset first.")
    st.page_link("pages/2_Document_Upload.py", label="Open Document Ingestion")
    st.stop()

render_domain_banner(
    detected_domain=project.get("project_type_category", "IT") if project else "IT",
    model_used=project.get("model_used", "XGBoost Regressor") if project else "ML Risk Model",
    detection_reason=project.get("domain_detection_reason", "") if project else ""
)

col_info, col_status = st.columns([3, 1])
with col_info:
    st.caption(f"Knowledge Context: **{project_name}** ({len(documents)} document sources)")
with col_status:
    if rag_ready:
        chunk_count = st.session_state.get("rag_chunk_count", 0)
        st.success(f"Vector Index Ready ({chunk_count} chunks)")
    else:
        st.warning("Vector Index Pending")

if documents and not rag_ready:
    st.info("Uploaded project text is available. Build the local vector index to activate conversational query answering.")
    if st.button("Build Vector Knowledge Base", type="primary"):
        from rag_chatbot.session_store import build_index, clear_index
        with st.spinner("Indexing project vectors..."):
            try:
                clear_index()
                num_chunks = build_index(documents)
                st.session_state["rag_ready"] = True
                st.session_state["rag_chunk_count"] = num_chunks
                st.success(f"Knowledge base indexed ({num_chunks} vector chunks).")
                st.rerun()
            except Exception as e:
                st.error(f"Vector indexing error: {e}")
        st.stop()

if not rag_ready:
    st.stop()

st.divider()

# ============================================================
# CHAT HISTORY & STARTERS
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.session_state.chat_history:
    if st.button("Clear Conversation", use_container_width=False):
        st.session_state.chat_history = []
        st.rerun()

if not st.session_state.chat_history:
    st.markdown("**Suggested Technical Inquiries:**")
    starters = [
        "What are the primary risk factors identified in this project?",
        "List all deliverables and their current completion status.",
        "Which work packages or dependencies are delayed?",
        "What is the total budget allocation and cost variance?",
        "Summarize the project scope and key milestones."
    ]
    cols = st.columns(len(starters))
    for col, starter in zip(cols, starters):
        with col:
            btn_label = starter[:32] + "..."
            if st.button(btn_label, use_container_width=True, key=f"q_{starter[:20]}"):
                st.session_state.chat_history.append({"role": "user", "content": starter})
                st.rerun()

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("Grounded Sources", expanded=False):
                for src in message["sources"]:
                    st.caption(f"- {src}")

# ============================================================
# CHAT INPUT & GENERATION
# ============================================================

question = st.chat_input("Ask a technical question regarding this project...")

pending = None
if st.session_state.chat_history:
    last = st.session_state.chat_history[-1]
    if last["role"] == "user":
        pending = last["content"]

active_question = question or (pending if not question else None)

if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    active_question = question

if active_question and (
    not st.session_state.chat_history
    or st.session_state.chat_history[-1]["role"] == "user"
):
    with st.chat_message("assistant"):
        with st.spinner("Retrieving document chunks and synthesizing answer..."):
            try:
                from rag_chatbot.session_store import retrieve
                from rag_chatbot.chatbot import answer_with_context

                chunks = retrieve(active_question)
                result = answer_with_context(active_question, chunks)
                answer = result.get("answer", "No grounded answer could be synthesized.")
                sources = result.get("sources", [])
            except Exception as e:
                # Professional graceful error handling without raw traceback
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    answer = "The AI service is temporarily rate-limited due to API quota. Your project documents are safe in session memory. Please wait a moment and submit your inquiry again."
                else:
                    answer = f"The assistant encountered an operational exception: {err_str}"
                sources = []

        st.write(answer)
        if sources:
            with st.expander("Grounded Sources", expanded=False):
                for src in sources:
                    st.caption(f"- {src}")

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
    st.rerun()