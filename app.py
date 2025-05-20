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
                response = requests.post("https://f606-34-125-96-116.ngrok-free.app/generate", json={"query": query})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No response generated.")
                    st.success("✅ Response received.")
                    st.markdown(f"**Answer:** {answer}")
                else:
                    st.error("Failed to fetch response from model.")
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")

# ---- TAB 2: Upload Documents ----
with tab2:
    st.header("📁 Admin: Upload New Information")

    st.markdown("Authorized personnel can upload new documents (FAQs, policies, service updates):")

    uploaded_files = st.file_uploader(
        "Select TXT or PDF or EXCEL files to upload:",
        type=["txt", "pdf", "xlsx"],
        accept_multiple_files=True
    )

    if st.button("Upload"):
        if uploaded_files:
            with st.spinner("Uploading and processing..."):
                files = [("files", (file.name, file.read(), file.type)) for file in uploaded_files]
                response = requests.post("https://f606-34-125-96-116.ngrok-free.app/upload", files=files)
                
                if response.status_code == 200:
                    st.success("✅ Upload and ingestion successful!")
                    st.write(response.json()["message"])
                else:
                    st.error("❌ Upload failed.")
    else:
        st.warning("⚠️ Please select at least one file before uploading.")

# ---- FOOTER ----
st.markdown("---")
st.markdown("""
**🔒 BankBot is secure and compliant.**  
No personal data is stored. Always verify policy updates with official bank sources.
""")
st.caption("© 2025 BankBot | Powered by Open-Source LLMs | Demo UI")
