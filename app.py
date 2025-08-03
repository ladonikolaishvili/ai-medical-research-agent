import streamlit as st
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)
st.session_state.api_key_loaded = bool(api_key and api_key != "your_openai_api_key_here")
if st.session_state.api_key_loaded:
    os.environ["OPENAI_API_KEY"] = api_key

from agent import process_medical_query, extract_pdf_text

st.set_page_config(page_title="AI Medical Agent", layout="wide")

st.markdown("""
<style>
    .title { font-size: 2rem; color: #333; margin-bottom: 2rem; font-weight: 500; }
    .section { padding: 1rem; margin: 1rem 0; }
    .response { background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
    .setup { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 0.5rem; padding: 1rem; margin: 1rem 0; }
    h3 { color: #333; font-weight: 500; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="title">AI Medical Research Agent</h1>', unsafe_allow_html=True)
    
    # Session management for Streamlit state only
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if not st.session_state.api_key_loaded:
        st.markdown('<div class="setup">', unsafe_allow_html=True)
        st.markdown("### Setup Required")
        st.markdown("Add OpenAI API key to `.env` file or Streamlit secrets")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<h3>PDF Text Extraction</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
        if uploaded_file:
            with st.spinner("Extracting..."):
                extracted_text = extract_pdf_text(uploaded_file)
                if extracted_text:
                    st.text_area("Text:", extracted_text, height=300, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3>📄 Upload PDF Document</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF (Required)", type=['pdf'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3>❓ Ask Medical Question</h3>', unsafe_allow_html=True)
    text_input = st.text_area("Question (Required)", height=100, placeholder="e.g., What are the symptoms of diabetes?")
    st.markdown('</div>', unsafe_allow_html=True)
    
# Removed custom prompt engineering UI for simplified interface
    
    # Single analyze button that requires both inputs
    analyze_button = st.button("🤖 Analyze PDF & Answer Question", type="primary", use_container_width=True)
    
    if analyze_button:
        if not uploaded_file:
            st.error("❌ Please upload a PDF document")
        elif not text_input.strip():
            st.error("❌ Please enter a medical question")
        elif uploaded_file and text_input.strip():
            with st.spinner("🤖 Analyzing PDF and researching question..."):
                try:
                    extracted_text = extract_pdf_text(uploaded_file)
                    if extracted_text and not extracted_text.startswith("Error"):
                        response = process_medical_query(
                            question=text_input.strip(), 
                            pdf_content=extracted_text,
                            filename=uploaded_file.name,
                            session_id=st.session_state.session_id
                        )
                        st.session_state.conversation_history.append({
                            "type": "pdf_question",
                            "content": f"PDF: {uploaded_file.name} | Question: {text_input.strip()}",
                            "response": response
                        })
                        st.markdown('<div class="response">', unsafe_allow_html=True)
                        st.markdown("### 🤖 AI Analysis")
                        st.markdown(response)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Could not extract text from PDF")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.session_state.conversation_history:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<h3>History</h3>', unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.conversation_history):
            with st.expander(f"{item['type'].title()}: {item['content'][:50]}..."):
                st.markdown(item['response'])
        if st.button("Clear"):
            st.session_state.conversation_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Observability sidebar removed - now tracking via LangSmith

if __name__ == "__main__":
    main() 