# README SEO Booster

## 🚀 AI-Powered GitHub README SEO Optimization

README SEO Booster is an intelligent agent-based system built with CrewAI that automatically enhances the search engine optimization (SEO) of GitHub repository README files, improving discoverability while maintaining your project's unique voice.

## 🤖 How It Works

This tool leverages a crew of specialized AI agents to optimize your GitHub README:

1. **Keyword Miner Agent**: Discovers trending and relevant SEO keywords for your repository using Bright Data's MCP
2. **SEO Refiner Agent**: Intelligently incorporates these keywords into your README file.
3. **PR Bot Agent**: Creates a pull request with the enhanced README for your review.


## 🌟 Key Features

- **Non-intrusive optimization**: Preserving your project's style
- **Data-driven keyword selection**: Uses real search results to identify trending keywords using Bright Data's MCP
- **Streamlined workflow**: Handles the entire process from keyword discovery to PR creation
- **User-friendly interface**: Available both as a command-line tool and a Streamlit web application

## 🔧 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/YourUsername/README_SEO_BOOSTER.git
cd README_SEO_BOOSTER

# Install dependencies through UV
```

### Environment Variables

Create a `.env` file with the following variables:
```
GEMINI_API_KEY=your_gemini_api_key
BRIGHTDATA_API_TOKEN=your_brightdata_token
GITHUB_PAT=your_github_personal_access_token
```

## 📊 Usage

### Command Line Interface
```bash
# Navigate to the project root
cd path/to/README_SEO_BOOSTER

# Run the CLI
crewai run 
```

### Web Interface (Streamlit)
```bash
# Navigate to the UI file location
cd path/to/README_SEO_BOOSTER/src/readme_seo_booster

# Run the Streamlit app
streamlit run ui.py
```

## 🧠 Technical Details

This project is built with:
- [CrewAI](https://github.com/joaomdmoura/crewAI) - Framework for orchestrating role-playing AI agents
- [BrightData MCP](https://github.com/luminati-io/brightdata-mcp) - For web data extraction
- [GitHub MCP](https://github.com/github/github-mcp-server) - For GitHub automation
- [Streamlit](https://streamlit.io/) - For the web interface


## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License

## 🙏 Acknowledgements

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the amazing agent framework
- [Bright Data](https://brightdata.com/) for providing the web data tools
- [GitHub](https://github.com/) for the GitHub automation capabilities
