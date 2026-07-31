# pyrefly: ignore [missing-import]
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(page_title="AI Document Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AI Document Assistant")
st.caption("Powered by Google Gemini AI")

# Sidebar for Settings
st.sidebar.header("⚙️ Settings")

# Model selection
model_option = st.sidebar.selectbox(
    "Select Gemini Model:",
    ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-flash-latest"],
    index=0
)

env_api_key = os.getenv("GOOGLE_API_KEY", "").strip()

api_key = st.sidebar.text_input(
    "Google Gemini API Key:", 
    value=env_api_key,
    type="password", 
    help="Enter your Gemini API key from Google AI Studio (starts with AIzaSy...)"
)

if api_key:
    if api_key.startswith("AIzaSy"):
        st.sidebar.success("✅ Valid Gemini API key format detected (`AIzaSy...`)")
    else:
        st.sidebar.warning("⚠️ API Key format notice: Standard Gemini API keys start with `AIzaSy...`.")

st.sidebar.info(
    "🔑 **Need a free API Key?**\n"
    "1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)\n"
    "2. Click **Create API key**\n"
    "3. Copy your key and paste it above or update `GOOGLE_API_KEY` in `.env`."
)

# Main content
question = st.text_input("Ask me anything:", placeholder="e.g. Summarize the main features of Python 3.13")

if st.button("Generate Answer", type="primary"):
    if not question.strip():
        st.warning("⚠️ Please enter a question first.")
    elif not api_key.strip():
        st.error("❌ Google API key is missing. Please enter your `GOOGLE_API_KEY` in the sidebar or update `.env`.")
    else:
        try:
            with st.spinner(f"🤔 Thinking with `{model_option}`..."):
                genai.configure(api_key=api_key.strip())
                model = genai.GenerativeModel(model_option)
                response = model.generate_content(question.strip())
                
                st.markdown("---")
                st.subheader("💡 Answer:")
                st.write(response.text)
        except Exception as e:
            err_msg = str(e)
            if "ResourceExhausted" in err_msg or "429" in err_msg or "Quota exceeded" in err_msg:
                st.error(
                    "❌ **Quota Exceeded / Free Tier Limit (429)**\n\n"
                    "The current API key does not have free tier quota available or is linked to a Google Cloud project with rate limits.\n\n"
                    "👉 **Fix**: Get a new free API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and paste it in the sidebar."
                )
            elif "API_KEY_INVALID" in err_msg or "invalid" in err_msg.lower():
                st.error(
                    "❌ **Invalid Google API Key**\n\n"
                    "Please verify your key at [Google AI Studio](https://aistudio.google.com/app/apikey) (keys start with `AIzaSy...`)."
                )
            elif "404" in err_msg or "not found" in err_msg:
                st.error(f"❌ Model `{model_option}` not found for this API version. Try selecting `gemini-2.0-flash` from the sidebar.")
            else:
                st.error(f"❌ Error generating response: {err_msg}")

