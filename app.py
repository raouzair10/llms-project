import streamlit as st
from datetime import datetime
import requests
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
import requests
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
            try:
                response = requests.post("ngrokurl/generate", json={"query": query})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No response generated.")
                    st.success("✅ Response received.")
                    st.markdown(f"**Answer:** {answer}")
                else:
                    st.error("Failed to fetch response from model.")
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")

with tab2:
    st.header("📁 Admin: Upload New Information")

    uploaded_file = st.file_uploader(
        "Select TXT or PDF or EXCEL files to upload:",
        type=["txt", "pdf", "xlsx", "json"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        if st.button("Upload"):
            try:
                # Use getvalue() to extract raw bytes
                file_bytes = uploaded_file.getvalue()

                # Form fields (must match FastAPI param names exactly)
                data = {
                    "username": "saleha"
                }

                # Files dict: must match FastAPI field name: 'uploaded_file'
                files = {
                    "uploaded_file": (uploaded_file.name, file_bytes, uploaded_file.type)
                }

                response = requests.post(
                    "ngrokurl/upload/",
                    data=data,
                    files=files
                )

                if response.ok:
                    st.success("Upload Successful")
                else:
                    st.error(f"Upload failed: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Upload failed with exception: {e}")
# ---- FOOTER ----
st.markdown("---")
st.markdown("""
**🔒 BankBot is secure and compliant.**  
No personal data is stored. Always verify policy updates with official bank sources.
""")
st.caption("© 2025 BankBot | Powered by Open-Source LLMs | Demo UI")
