import streamlit as st
from datetime import datetime
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def get_greeting():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def create_streamlit_app(llm, portfolio, clean_text):

    col1, col2 = st.columns([0.7, 0.3])  


    with col1:
        st.title("🛒🛍️ SalesScribe AI")

   
    with col2:
        st.markdown(f"<h1 style='text-align: right;'>HI {get_greeting()}</h1>", unsafe_allow_html=True)


    url_input = st.text_input("Enter a URL:" , placeholder="Enter a valid URL to generate a cold email")


    submit_button = st.button("Submit")


    if submit_button:
        if url_input:
            try:
                # Load data from the input URL
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                # Process each job to extract details and generate email
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')

            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        else:
            st.warning("Please enter a valid URL.")  

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    

    st.set_page_config(layout="wide", page_title="🛒🛍️ SalesScribe AI", page_icon="🛒🛍️")
    
    create_streamlit_app(chain, portfolio, clean_text)
