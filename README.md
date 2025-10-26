# Fake News Checker

A Streamlit web application that uses **CrewAI** agents to verify the authenticity of news articles and claims in real-time.

## Features

- Input a news article or claim to verify its authenticity.
- Multi-agent pipeline:
  1. **Research Agent** – Collects relevant information from credible sources.
  2. **Summarization Agent** – Condenses findings into an easy-to-read summary.
  3. **Fact-Checking Agent** – Provides a final verdict on whether the news is genuine or fake.
- Displays results in a clean, interactive Streamlit interface.

## Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [CrewAI](https://crewai.com/)
- SerperDevTool (for online research)
- Gemini LLM

## Setup

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/fake-news-checker.git
cd fake-news-checker

2.Create a virtual environment 
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3.Install the dependencies
pip install -r requirements.txt

4.Run the streamlit app
streamlit run app.py
