from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st

import PyPDF2 as pdf
import google.generativeai as genai
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# def input_pdf_setup(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page in reader(len(reader.pages)):
#         p = reader.pagesp[page]
#         text += str(p.extract_text())
#     return text

def input_pdf_setup(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)  # Properly initialize the PdfReader object
    text = ""
    for page in reader.pages:  # Iterate through pages directly
        text += page.extract_text()
    return text

input_prompt="""
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and the missing keywords with high accuracy. Also explina in detai the areas of improvement in the resume to reach 100% mathing
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)

