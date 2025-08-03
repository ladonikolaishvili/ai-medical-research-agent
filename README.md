# AI Medical Research Agent

An advanced AI-powered medical research assistant with GPT-4o, vector search, and semantic document analysis.

## 🏥 Features

- **🧠 GPT-4o Intelligence** - Latest OpenAI model for superior medical analysis
- **📄 PDF Document Analysis** - Semantic chunking and vector similarity search
- **🔍 Smart References** - Human-readable citations with page numbers (Section-X, Page ~Y)
- **📝 Customizable Prompts** - External prompt template for easy customization
- **⚡ ChromaDB Storage** - Persistent vector database for document chunks
- **🎯 Researcher-Focused** - Professional medical analysis and citations

## 🚀 Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ladonikolaishvili/ai-medical-research-agent.git
cd ai-medical-research-agent
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the project root:
```bash
# Copy the template file
cp .env.template .env

# Then edit .env with your actual API keys:
# OpenAI API Key (required)
OPENAI_API_KEY=your_actual_openai_api_key_here

# LangSmith API Key (required for observability) 
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=ai-medical-research-agent
```

**⚠️ Important**: 
- Get OpenAI API key from: https://platform.openai.com/api-keys
- Get LangSmith API key from: https://smith.langchain.com/

**💡 Quick Setup**: Run `python langsmith_config.py` to check configuration

### 5. Run the Application
```bash
streamlit run app.py
```

### 6. Open in Browser
Navigate to: http://localhost:8501

### 7. Monitor with LangSmith 📊
- View comprehensive traces and analytics at your [LangSmith Dashboard](https://smith.langchain.com/)
- Run `python view_metrics.py` for direct dashboard links
- See [SETUP_LANGSMITH.md](SETUP_LANGSMITH.md) for detailed observability setup

## 📋 Requirements

- **Python 3.9+**
- **OpenAI API Key** - Required for GPT-4o model access  
- **LangSmith API Key** - Required for observability and tracing
- **Internet Connection** - For API calls and dependencies

## 🎯 Usage

1. **Upload a PDF** - Medical research papers, clinical studies, etc.
2. **Ask Questions** - Medical questions related to the document
3. **Get Analysis** - Professional responses with citations and references
4. **Customize Prompts** - Edit `default_medical_prompt.txt` for custom instructions

## 🔧 Customization

### Prompt Engineering
Edit `default_medical_prompt.txt` to customize AI behavior:
- Change response style and format
- Add specific medical focus areas
- Adjust citation requirements
- Modify analysis depth

### Configuration
- **Vector Search**: Top 5 most relevant chunks
- **Model**: GPT-4o (latest OpenAI model)
- **Chunking**: 800 characters with 100 overlap
- **Citations**: Section-based with page estimates

## 📁 Project Structure

```
ai-medical-research-agent/
├── app.py                          # Main Streamlit application
├── agent.py                        # LangGraph workflow and AI logic
├── default_medical_prompt.txt      # Customizable prompt template
├── requirements.txt                # Python dependencies
├── config.toml                     # Streamlit configuration
├── README.md                       # This file
├── graph_analysis.md               # Workflow documentation
├── visualize_graph.py              # Workflow visualization
├── medical_agent_workflow.png      # Workflow diagram
└── .env                           # API keys (create this file)
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4o
- **Vector DB**: ChromaDB
- **Text Processing**: LangChain
- **PDF Processing**: PyMuPDF
- **Workflow**: LangGraph
- **Embeddings**: OpenAI Embeddings

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure and private
- The `.env` file is included in `.gitignore` for safety

## 📊 Performance

- **Smart Chunking**: Semantic text splitting for better context
- **Vector Search**: Fast similarity search with ChromaDB
- **Optimized Workflow**: Streamlined LangGraph pipeline
- **Production Ready**: Clean, efficient codebase

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues:

**"OpenAI API key not found" or "StreamlitSecretNotFoundError"**
- Copy template: `cp .env.template .env`
- Edit `.env` file with your actual `OPENAI_API_KEY`
- Check API key is active at https://platform.openai.com/
- Alternative: Create `~/.streamlit/secrets.toml` with your API keys

**"Module not found" errors**
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**App won't start**
- Check Python version: `python --version` (3.9+ required)
- Verify all dependencies installed correctly

---

**🎉 Ready to analyze medical documents with AI!**