# LangSmith Observability Setup

This AI Medical Research Agent now uses LangSmith for comprehensive observability, tracing, and evaluation instead of custom frontend metrics.

## Quick Setup

1. **Get LangSmith API Key**
   - Visit [https://smith.langchain.com/](https://smith.langchain.com/)
   - Sign up or log in
   - Go to Settings → Create API Key

2. **Configure Environment Variables**
   
   Add to your `.env` file:
   ```bash
   # LangSmith Configuration
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_PROJECT=ai-medical-research-agent
   
   # OpenAI Configuration (required)
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Setup**
   ```bash
   python langsmith_config.py
   ```

## What You Get with LangSmith

### 🔍 **Automatic Tracing**
- Every query is automatically traced from start to finish
- View the complete workflow: PDF processing → research → analysis → response
- See individual tool calls and their execution times

### 📊 **Performance Analytics**
- Response times and latency tracking
- Token usage and cost monitoring
- Success/failure rates
- Performance trends over time

### 🎯 **Evaluation Metrics**
- Automatic relevance scoring
- Citation quality assessment
- Response length analysis
- Custom evaluation criteria

### 🚨 **Error Monitoring**
- Real-time error tracking
- Stack traces and debugging info
- Alert notifications for issues
- Performance threshold monitoring

### 📈 **Session Management**
- User session tracking
- Query history and patterns
- Conversation flow analysis
- Usage analytics

## Viewing Your Data

### Dashboard Access
- Visit your project at: `https://smith.langchain.com/projects/{your-project-name}`
- Or run: `python view_metrics.py` for direct links

### Key Features
- **Traces**: Detailed execution flows for each query
- **Datasets**: Organize test cases and evaluations  
- **Playground**: Test and iterate on prompts
- **Analytics**: Performance trends and insights
- **Alerts**: Custom notifications for issues

## Migration from Old System

The previous observability system with sidebar metrics has been removed and replaced with:

- ❌ **Removed**: Streamlit sidebar metrics display
- ❌ **Removed**: Custom file-based logging (`logs/` directory)
- ❌ **Removed**: Manual evaluation tracking
- ✅ **Added**: LangSmith comprehensive tracing
- ✅ **Added**: Automatic evaluation and analytics
- ✅ **Added**: Real-time performance monitoring

## Configuration Options

### Project Settings
```python
# In langsmith_config.py
LANGSMITH_PROJECT = "ai-medical-research-agent"  # Your project name
LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"  # Default endpoint
```

### Advanced Configuration
```bash
# Optional: Custom endpoint (for self-hosted)
LANGSMITH_ENDPOINT=https://your-langsmith-instance.com

# Optional: Enable/disable tracing
LANGSMITH_TRACING=true
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   ⚠️  LangSmith API key not found. Add LANGSMITH_API_KEY to your .env file
   ```
   → Add your API key to the `.env` file

2. **Project Not Created**
   ```
   Project 'ai-medical-research-agent' not found
   ```
   → The project will be created automatically on first use

3. **Traces Not Appearing**
   - Check your API key is valid
   - Verify internet connection
   - Ensure `LANGSMITH_TRACING=true` is set

### Getting Help

- **LangSmith Documentation**: [https://docs.smith.langchain.com/](https://docs.smith.langchain.com/)
- **API Reference**: [https://api.smith.langchain.com/docs](https://api.smith.langchain.com/docs)
- **Support**: [https://github.com/langchain-ai/langsmith-sdk](https://github.com/langchain-ai/langsmith-sdk)

## Development Workflow

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Monitor Traces**
   - Open LangSmith dashboard in browser
   - Watch traces appear in real-time as you use the app

3. **Analyze Performance**
   - Review query patterns and performance
   - Identify slow operations or errors
   - Optimize based on insights

4. **Iterate and Improve**
   - Use trace data to improve prompts
   - Adjust parameters based on evaluation metrics
   - Monitor the impact of changes