import streamlit as st
import re
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import vector_store

# =========================
# 🐦 Twitter Chat Theme
# =========================
st.markdown("""
<style>

/* ===== App background ===== */
.stApp {
    background-color: #15202B;
    color: #E7E9EA;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #192734;
    border-right: 1px solid #38444D;
}

/* ===== Chat container spacing ===== */
[data-testid="stChatMessage"] {
    margin-bottom: 12px;
}

/* ===== Tweet card base ===== */
[data-testid="stChatMessage"] > div {
    background: #192734;
    border: 1px solid #38444D;
    border-radius: 16px;
    padding: 14px 16px;
    transition: all 0.15s ease-in-out;
}

/* ===== Hover effect (subtle Twitter feel) ===== */
[data-testid="stChatMessage"] > div:hover {
    background: #1e2a36;
}

/* ===== Assistant messages slightly darker ===== */
[data-testid="stChatMessage"][data-testid*="assistant"] > div {
    background: #22303C;
}

/* ===== Textarea (input) ===== */
textarea {
    background-color: #192734 !important;
    color: #E7E9EA !important;
    border: 1px solid #38444D !important;
    border-radius: 12px !important;
}

/* ===== Primary buttons ===== */
button[kind="primary"] {
    background-color: #1D9BF0 !important;
    border: none !important;
}

/* ===== Title ===== */
h1 {
    color: #E7E9EA;
}

</style>
""", unsafe_allow_html=True)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Support Intelligence",
    page_icon="🟦",
    layout="centered"
)

APP_ICON = "https://img.icons8.com/fluency/96/headset.png"

st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;">
    <img src="{APP_ICON}" width="48">
    <h1 style="margin:0;color:#E7E9EA;">Social Support Intelligence</h1>
</div>
""", unsafe_allow_html=True)
st.write("Analyze customer complaints and generate smart support responses.")

# =========================
# SIDEBAR — TOP-K CONTROL ⭐ FEATURE #3
# =========================
with st.sidebar:
    st.header("⚙️ Retrieval Settings")

    st.markdown("**Model status:** 🟢Online")

    top_k = st.slider(
        "Number of similar complaints",
        min_value=2,
        max_value=10,
        value=4,
        step=1
    )
    st.caption("Higher values = broader context but slower responses.")
    st.divider()
    urgency_filter = st.selectbox(
    "Urgency focus",
    ["All", "🔴High priority", "🟡Medium & High", "🟢Low only"]
    )
    st.divider()
    st.subheader("⚡ Quick tests")
    st.caption("Run common customer complaint scenarios instantly.")
    if st.button("📦 Delayed delivery"):
        st.session_state.quick_prompt = (
        "My order was supposed to arrive last week and I still haven't received it."
        )
        st.rerun()
    if st.button("💸 Refund issue"):
        st.session_state.quick_prompt = (
        "I returned the item two weeks ago and still haven't received my refund."
        )
        st.rerun()
    if st.button("🔐 Login problem"):
        st.session_state.quick_prompt = (
        "I can't log into my account and the password reset isn't working."
        )
        st.rerun()
    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = [
            {
            "role": "assistant",
            "content": "Feed refreshed. Listening for new complaints."
            }
        ]
        st.rerun()
# =========================
# LLM + PROMPT
# =========================
@st.cache_resource
def get_chain():
    model = OllamaLLM(model="gemma3:latest")

    template = """
You are an expert customer support analyst.

Your job:
- Understand the user's complaint
- Use the retrieved past complaints as context
- Identify the core issue
- Classify urgency carefully (Low, Medium, High)
- Suggest a professional and empathetic reply

Urgency guidelines:

HIGH urgency when:
- User shows strong frustration or anger
- Payment/duplicate charge issues
- Account access is blocked
- Order missing with clear frustration
- User asks for urgent help (ASAP, immediately, etc.)

MEDIUM urgency when:
- There is a real problem but tone is calm
- Delays without strong anger
- Status inquiries with mild concern

LOW urgency when:
- Issue is already resolved
- User expresses satisfaction or thanks
- Minor inconvenience without frustration
- User explicitly says "it's fine now" or similar

Important:
- Do NOT overestimate urgency.
- If the user indicates the issue is resolved, urgency must be LOW.
- Base urgency primarily on user sentiment and problem severity.

Tone and sarcasm handling:

- Detect sarcasm or passive-aggressive language carefully.
- If the user uses sarcasm (e.g., "great service…", "amazing if waiting forever was the goal"), treat it as frustration.
- In sarcastic cases, acknowledge the frustration first — do NOT respond as if the feedback is positive.
- Match the emotional tone appropriately while remaining professional and calm.

Rules:
- Use ONLY the provided complaint context
- Do NOT invent company policies
- Be concise but helpful
- Maintain a professional support tone
- When unsure between Medium and Low, prefer the lower urgency unless strong frustration is present.
- When user sentiment is negative or sarcastic, begin the reply by acknowledging the frustration before offering help.
- Prioritize clarity and helpfulness over politeness verbosity.

Reply style guidelines:

- Keep the suggested reply concise and natural.
- Avoid repetitive apologies.
- Use at most ONE apology sentence.
- Prefer clear, direct support language.
- Do not sound overly formal or robotic.
- Keep the reply typically between 2 - 4 sentences.

Retrieved similar complaints:
{records}

User complaint:
{question}

Respond in this format:

**Issue Summary**
...

**Urgency Level**
...

**Suggested Reply**
...
"""
    prompt = ChatPromptTemplate.from_template(template)
    return prompt | model


chain = get_chain()

# =========================
# CHAT HISTORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# HELPER — urgency badge ⭐ FEATURE #2
# =========================
def show_urgency_badge(text):
    match = re.search(r"\*\*Urgency Level\*\*\s*(.*)", text)
    if not match:
        return

    level = match.group(1).lower()

    if "high" in level:
        st.error("🔴 High Urgency")
    elif "medium" in level:
        st.warning("🟡 Medium Urgency")
    elif "low" in level:
        st.success("🟢 Low Urgency")

# =========================
# USER INPUT
# =========================
user_input = st.chat_input("Describe the customer complaint...")

# 🔥 prioritize quick prompt if clicked
if st.session_state.quick_prompt:
    question = st.session_state.quick_prompt
    st.session_state.quick_prompt = None
elif user_input:
    question = user_input
else:
    question = None

if question:
    # user message
    with st.chat_message("user",avatar="verified.png"):
        st.markdown(question)

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    # assistant response
    with st.chat_message("assistant", avatar="bot.png"):
        with st.spinner("Analyzing support signals..."):

            # ⭐ FEATURE #3 — dynamic top-k
            dynamic_retriever = vector_store.as_retriever(
            search_kwargs={"k": top_k}
            )

            docs = dynamic_retriever.invoke(question)

            # build context
            if not docs:
                context = "No similar customer complaints were found in the database."
            else:
                context = "\n\n".join(
                [d.page_content for d in docs]
            )

            # LLM call
            response = chain.invoke({
                "records": context,
                "question": question
            })

            st.markdown(response)

            # ⭐ FEATURE #2 — urgency badge
            show_urgency_badge(response)

            # ⭐ FEATURE #1 — retrieved complaints panel
            with st.expander("🔍 Retrieved similar complaints"):
                for d in docs:
                    st.write("- " + d.page_content[:300])

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
