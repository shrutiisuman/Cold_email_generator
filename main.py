import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

import portfolio2
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # URL input for the job listing
    url_input = st.text_input("Enter a URL:", value="https://jobright.ai/jobs/info/676f463cc8deb60410d61e21?utm_source=1023&utm_campaign=DavidChen")

    # Submit button to trigger the action
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load data from the URL and clean the text content
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Load portfolio links
            # portfolio.load_portfolio()

            # Extract job listings using the llm
            jobs = llm.extract_jobs(data)

            if not jobs:
                st.warning("No jobs found in the provided URL.")
                return

            # For each job, extract relevant skills and generate an email
            for job in jobs:
                skills = job.get('skills', [])
                if skills:
                    # Query the portfolio links based on job skills
                    matched_skills = portfolio.query_links(skills)
                    # Generate the cold email based on job details and portfolio links
                    email = llm.write_mail(job, matched_skills)
                    # Display the generated email
                    st.code(email, language='markdown')
                else:
                    st.warning(f"No skills found for the job: {job.get('title', 'Unknown Job')}")

        except Exception as e:
            # Show an error message in case of an exception
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    # Initialize necessary components
    chain = Chain()
    portfolio = Portfolio()

    # Set page configuration for Streamlit app
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    # Run the app
    create_streamlit_app(chain, portfolio, clean_text)
