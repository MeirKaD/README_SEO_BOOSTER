#!/usr/bin/env python
import streamlit as st
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
import warnings
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from readme_seo_booster.crew import ReadmeSeoBooster
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def validate_env():
    """Validate environment variables"""
    required_vars = ["GEMINI_API_KEY", "BRIGHTDATA_API_TOKEN", "GITHUB_PAT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        st.error(f"Missing required environment variables: {', '.join(missing)}")
        st.info("Please set them in your .env file or enter them below")
        return False
    return True

def run_crew(repo_name):
    """Run the README SEO Booster crew"""
    try:
        inputs = {
            "repo_name": repo_name,
            "current_date": datetime.now().strftime("%Y%m%d")
        }
        
        crew = ReadmeSeoBooster()
        with st.spinner(f"Running README SEO Booster on {repo_name}..."):
            result = crew.crew().kickoff(inputs=inputs)
        
        return True, result
    except Exception as e:
        error_msg = f"Error running crew: {e}\n{traceback.format_exc()}"
        return False, error_msg

def main():
    load_dotenv()
    
    st.set_page_config(
        page_title="README SEO Booster",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 README SEO Booster")
    st.subheader("Enhance your GitHub README with AI-powered SEO")
    
    with st.sidebar:
        st.header("Configuration")
        
        st.subheader("API Keys")
        if not os.getenv("GEMINI_API_KEY"):
            gemini_key = st.text_input("Gemini API Key", type="password")
            if gemini_key:
                os.environ["GEMINI_API_KEY"] = gemini_key
        
        if not os.getenv("BRIGHTDATA_API_TOKEN"):
            brightdata_token = st.text_input("BrightData API Token", type="password")
            if brightdata_token:
                os.environ["BRIGHTDATA_API_TOKEN"] = brightdata_token
        
        if not os.getenv("GITHUB_PAT"):
            github_pat = st.text_input("GitHub Personal Access Token", type="password")
            if github_pat:
                os.environ["GITHUB_PAT"] = github_pat
        
        
        st.subheader("Advanced Options")
        verbose = st.checkbox("Verbose Logging", value=True)
    
    st.header("Repository Selection")
    repo_name = st.text_input("GitHub Repository (username/project)", placeholder="e.g., MeirKaD/SBR-MCP")
    
    st.caption("Or choose from examples:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("MeirKaD/SBR-MCP"):
            repo_name = "MeirKaD/SBR-MCP"
    with col2:
        if st.button("MeirKaD/MCP_ADK"):
            repo_name = "MeirKaD/MCP_ADK"
    
    if st.button("Boost README SEO!", disabled=not repo_name):
        if not validate_env():
            st.warning("Please provide all required API keys in the sidebar.")
        else:
            success, result = run_crew(repo_name)
            
            if success:
                st.success("SEO optimization completed successfully!")
                
            else:
                st.error("An error occurred during SEO optimization.")
                st.code(result, language="python")
    
    with st.expander("How it works"):
        st.markdown("""
        ## README SEO Booster
        
        This tool uses AI agents to enhance the SEO of your GitHub README files:
        
        1. **Keyword Miner Agent**: Discovers relevant SEO keywords for your repository
        2. **SEO Refiner Agent**: Optimizes your README content with the discovered keywords
        3. **PR Bot Agent**: Creates a Pull Request with the enhanced README
        
        The agents only modify the first paragraph of your README to maintain your project's unique voice while improving discoverability.
        """)

if __name__ == "__main__":
    main()