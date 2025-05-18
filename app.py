import streamlit as st
from datetime import datetime

st.set_page_config(page_title="BankBot - Secure Customer Support", layout="centered")

# ---- HEADER ----
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        padding: 10px;
    }
    .css-1d391kg {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏦 Welcome to BankBot")
st.subheader("Your Trusted Assistant for Bank Queries and Support")
st.markdown("""
Our AI assistant helps you with all your banking-related questions,  
and allows bank staff to upload new policies, FAQs, or documents to keep the system updated in real-time.
""")

# ---- TABS ----
tab1, tab2 = st.tabs(["💬 Ask a Question", "📁 Upload Documents"])

# ---- TAB 1: Ask a Question ----
with tab1:
    st.header("💬 Customer Chat")

    st.markdown("Enter your banking-related question below and get a helpful response:")

    query = st.text_input("Your Question", placeholder="e.g., How can I apply for a mortgage loan?")
    
    if st.button("Submit"):
        if query.strip() == "":
            st.warning("Please enter a question.")
        else:
            st.info("🔍 Searching the knowledge base...")
            st.success("This is a demo response. Your answer will appear here when the system is fully connected.")
            st.markdown("**Answer:** You can apply for a mortgage loan through our online portal or by visiting your nearest branch with required documents.")

    st.markdown("---")
    st.caption(f"Response generated on: {datetime.now().strftime('%B %d, %Y %H:%M')}")

# ---- TAB 2: Upload Documents ----
with tab2:
    st.header("📁 Admin: Upload New Information")

    st.markdown("Authorized personnel can upload new documents (FAQs, policies, service updates):")

    uploaded_files = st.file_uploader(
        "Select TXT or PDF files to upload:",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )

    if st.button("Upload"):
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} document(s) uploaded successfully (preview only).")
            for file in uploaded_files:
                st.write(f"📄 {file.name}")
        else:
            st.warning("⚠️ Please select at least one file before uploading.")

# ---- FOOTER ----
st.markdown("---")
st.markdown("""
**🔒 BankBot is secure and compliant.**  
No personal data is stored. Always verify policy updates with official bank sources.
""")
st.caption("© 2025 BankBot | Powered by Open-Source LLMs | Demo UI")
