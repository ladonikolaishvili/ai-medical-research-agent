# Setup Instructions

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ladonikolaishvili/ai-medical-research-agent.git
   cd ai-medical-research-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```
   
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## API Key Setup

### OpenAI API Key (Required)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

### LangSmith (Optional - for observability)
1. Go to [LangSmith](https://smith.langchain.com/)
2. Create an account and get your API key
3. Add it to your `.env` file

## Alternative: Streamlit Secrets

Instead of `.env`, you can also use Streamlit secrets:

1. Create `~/.streamlit/secrets.toml` or `.streamlit/secrets.toml` in your project
2. Add your keys:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
   LANGSMITH_API_KEY = "your-langsmith-key-here"
   LANGSMITH_PROJECT = "ai-medical-research-agent"
   ```

## Features

- **PDF Analysis**: Upload medical documents for AI analysis
- **Medical Q&A**: Ask medical research questions
- **Observability**: Track usage with LangSmith (optional)

## Troubleshooting

**Error: `StreamlitSecretNotFoundError`**
- Solution: Set up your `.env` file or Streamlit secrets as described above

**Error: `OpenAI API key not found`**
- Solution: Make sure your API key is correctly set in `.env` or secrets.toml