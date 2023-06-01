from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from website_url_fetcher import lookup as company_lookup_agent
from company_scraper import scrape_company_page
import io
from PyPDF2 import PdfReader
import streamlit as st
from constants import TASK_DESCRIPTION_TEMPLATE

def create_cover_letter(company: str, role: str, cover_letter: str):
    print("Hello World")

    company_url = company_lookup_agent(
        company=company, role=role)


    summary_prompt_template = PromptTemplate(
        input_variables=["job_information", "cover_letter", "name_of_company","role"], template=TASK_DESCRIPTION_TEMPLATE
    )
    openai_api_key = #
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    print(f"Company URL: {company_url}")
    company_data = scrape_company_page(company_url=company_url)

    return chain.run(job_information=company_data, cover_letter=cover_letter, name_of_company=company, role=role)


# Streamlit UI starts here

st.image("https://ai-cover.io/assets/images/AIwriting.png", width=300)

st.title('Cover Letter Buddy')

company = st.text_input("Name of Company", placeholder="Enter your preferred company name here...")
role = st.text_input("Role", placeholder="Enter your preferred company role here...")

uploaded_file = st.file_uploader("Upload your cover-letter file (has to be a PDF)", type="pdf")

if uploaded_file is not None:
    bytes_data = io.BytesIO(uploaded_file.getvalue())
    pdf_reader = PdfReader(bytes_data)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # If company, role, and cover letter are provided, call the create_cover_letter function
    if company and role and text:
        with st.spinner("Generating your new cover letter..."):
            generated_response = create_cover_letter(company=company, role=role, cover_letter=text)
            st.success("Your new cover letter has been created.")
            st.text_area("Your new cover_letter:", generated_response, height=400)

            # Provide the generated cover letter as a download
            st.download_button(
                "Download your new cover letter",
                data=generated_response,
                file_name=f"cover_letter_{company}_{role}.txt",
                mime="text/plain"
            )
    else:
        st.info("Please upload a PDF file.")

