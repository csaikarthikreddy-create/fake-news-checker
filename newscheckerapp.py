import streamlit as st
import yaml
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from crewai.llm import LLM

# ---------------------------
# Load configuration
# ---------------------------
with open("confignew.yaml", "r") as f:
    config = yaml.safe_load(f)

# ---------------------------
# Setup LLM and Tools
# ---------------------------
gemini_llm = LLM(model="gemini/gemini-2.5-flash", temperature=0.7)
serper_dev_tool = SerperDevTool()

# ---------------------------
# Define Agents
# ---------------------------
news_research_agent = Agent(
    role=config["agents"]["news_research_agent"]["role"],
    goal=config["agents"]["news_research_agent"]["goal"],
    backstory=config["agents"]["news_research_agent"]["backstory"],
    tools=[serper_dev_tool],
    llm=gemini_llm,
    verbose=True
)

news_summary_agent = Agent(
    role=config["agents"]["news_summary_agent"]["role"],
    goal=config["agents"]["news_summary_agent"]["goal"],
    backstory=config["agents"]["news_summary_agent"]["backstory"],
    tools=[serper_dev_tool],
    llm=gemini_llm,
    verbose=True
)

authenticity_verifier_agent = Agent(
    role=config["agents"]["authenticity_verifier_agent"]["role"],
    goal=config["agents"]["authenticity_verifier_agent"]["goal"],
    backstory=config["agents"]["authenticity_verifier_agent"]["backstory"],
    tools=[serper_dev_tool],
    llm=gemini_llm,
    verbose=True
)

# ---------------------------
# Define Tasks
# ---------------------------
news_research_task = Task(
    description=config["tasks"]["news_research_task"]["description"],
    agent=news_research_agent,
    tools=[serper_dev_tool],
    expected_output=config["tasks"]["news_research_task"]["expected_output"]
)

news_summary_task = Task(
    description=config["tasks"]["news_summary_task"]["description"],
    agent=news_summary_agent,
    expected_output=config["tasks"]["news_summary_task"]["expected_output"],
)

authenticity_verification_task = Task(
    description=config["tasks"]["authenticity_verification_task"]["description"],
    agent=authenticity_verifier_agent,
    expected_output=config["tasks"]["authenticity_verification_task"]["expected_output"],
)

# ---------------------------
# Create Crew
# ---------------------------
fake_news_crew = Crew(
    agents=[news_research_agent, news_summary_agent, authenticity_verifier_agent],
    tasks=[news_research_task, news_summary_task, authenticity_verification_task],
    process=Process.sequential,
    verbose=True
)

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("📰 Fake News Checker")
st.write("Enter a news claim or article to verify its authenticity.")

# Input box for claim/article
user_input = st.text_area("News Claim/Article", height=150)

if st.button("Check News"):
    if user_input.strip() == "":
        st.warning("Please enter a claim or article to check.")
    else:
        with st.spinner("Analyzing the news..."):
            # Kickoff Crew
            result = fake_news_crew.kickoff(inputs={"article": user_input})
        
        st.success("Analysis Complete!")
        st.subheader("Research Findings")
        st.write(result.tasks_output[0].raw)

        st.subheader("Summary")
        st.write(result.tasks_output[1].raw)

        st.subheader("Final Verdict")
        st.write(result.tasks_output[2].raw)

