#!/usr/bin/env python3
"""
LangSmith Observability Dashboard Link
This script now redirects to LangSmith for comprehensive metrics and evaluation
"""

from langsmith_config import get_project_url

def main():
    """Main function to display LangSmith dashboard information"""
    print("📊 AI MEDICAL RESEARCH AGENT - OBSERVABILITY")
    print("=" * 60)
    print()
    print("🔄 Observability has been migrated to LangSmith!")
    print()
    
    project_url = get_project_url()
    
    if project_url:
        print("🌐 View comprehensive metrics and traces at:")
        print(f"   {project_url}")
        print()
        print("📈 LangSmith provides:")
        print("   • Real-time trace visualization")
        print("   • Performance analytics")  
        print("   • Automatic evaluation metrics")
        print("   • Cost tracking")
        print("   • Error monitoring")
        print("   • Session management")
        print()
        print("💡 Tips:")
        print("   • All queries are automatically traced")
        print("   • Filter traces by tags or metadata")
        print("   • Set up alerts for performance thresholds")
        print("   • Export data for custom analysis")
    else:
        print("⚠️  LangSmith not configured!")
        print()
        print("🔧 Setup Instructions:")
        print("   1. Get API key from: https://smith.langchain.com/")
        print("   2. Add to .env file:")
        print("      LANGSMITH_API_KEY=your_api_key_here")
        print("      LANGSMITH_PROJECT=ai-medical-research-agent")
        print("   3. Restart the application")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()