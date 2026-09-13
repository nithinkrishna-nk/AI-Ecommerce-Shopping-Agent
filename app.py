import streamlit as st
from agent import create_agent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Shopping Agent",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

# Create Gemini agent
if "client" not in st.session_state:
    st.session_state.client, st.session_state.chat = create_agent()


# Store visible conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛒 AI Shopping Agent")

    st.caption("Your intelligent product discovery assistant")


    # New chat
    if st.button("➕ New Chat", use_container_width=True):

        st.session_state.client, st.session_state.chat = create_agent()
        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.subheader("💡 Try asking")

    # Example prompts
    example_prompts = [
        "Find me 4K TVs under ₹50000",
        "Show me wireless headphones under ₹2000",
        "Find highly rated products",
        "Find budget products"
    ]

    for prompt in example_prompts:

        if st.button(prompt, use_container_width=True):

            st.session_state.pending_prompt = prompt
            st.rerun()

    st.divider()

    st.subheader("🔧 Powered By")

    st.write("🤖 Google Gemini")
    st.write("🔍 ChromaDB")
    st.write("🧠 Embeddings")
    st.write("📚 RAG")
    st.write("🛠️ Tool Calling")

    st.divider()

    st.caption("Developed by Nithin Krishna")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🛒 AI Shopping Agent")

st.write(
    "Find products, compare options, and get personalized recommendations."
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:


    st.subheader("🚀 What can I help you find?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📺 **TVs**\n\nFind TVs based on price, rating and requirements.")

    with col2:
        st.info("🎧 **Headphones**\n\nFind headphones that match your budget and needs.")

    with col3:
        st.info("🛍️ **Products**\n\nDiscover products using natural language.")


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# GET USER INPUT
# ============================================================

user_query = st.chat_input(
    "What are you looking for?"
)


# ============================================================
# HANDLE SIDEBAR PROMPT
# ============================================================

if "pending_prompt" in st.session_state:

    user_query = st.session_state.pending_prompt

    del st.session_state.pending_prompt


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_query:

    # --------------------------------------------
    # Save user message
    # --------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )


    # --------------------------------------------
    # Display user message
    # --------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_query)


    # --------------------------------------------
    # Ask Gemini Agent
    # --------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🔍 Searching for the best products..."):

            try:

                response = st.session_state.chat.send_message(
                    user_query
                )

                answer = response.text

            except Exception as e:

                answer = (
                    "❌ Sorry, something went wrong while processing "
                    "your request.\n\n"
                    f"Error: `{str(e)}`"
                )


        # ----------------------------------------
        # Display AI response
        # ----------------------------------------

        st.markdown(answer)


    # --------------------------------------------
    # Save AI response
    # --------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )