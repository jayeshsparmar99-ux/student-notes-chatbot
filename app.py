
from reportlab.lib import styles
import streamlit as st
import fitz 
import google.generativeai as genai
from dotenv import load_dotenv
import os

import io
from reportlab.platypus import  SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import easyocr
import numpy as np
from PIL import Image
from docx import Document

from xml.sax.saxutils import escape

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")



def create_pdf(text):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = []
    for line in text.split("\n"):
        try:
            safe_line = escape(line)
            content.append(Paragraph(safe_line, styles["Normal"]))
        except:
            pass
        
    pdf.build(content)
    buffer.seek(0)
    return buffer

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "summary" not in st.session_state:
    st.session_state.summary = "" 

if "mcq" not in st.session_state:
    st.session_state.mcq = ""

if "questions" not in st.session_state:
    st.session_state.questions = "" 
        
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 

if "pdf_texts" not in st.session_state:
    st.session_state.pdf_texts = {}   

if "exam_paper" not in st.session_state:
    st.session_state.exam_paper = ""

if "mid_exam_paper" not in st.session_state:
    st.session_state.mid_exam_paper = ""

if "final_exam_paper" not in st.session_state:
    st.session_state.final_exam_paper = ""     

st.set_page_config(
    page_title="Student Notes Chatbot",
    page_icon="🤖"
)

st.title("AI Study Chatbot")
st.caption("Upload PDFs, Ask questions, Generate IMP questions and MCQs")

uploaded_files = st.file_uploader(
    "Upload notes ",
    type=["pdf","docx",],
    accept_multiple_files=True
)

syllabus_file = st.file_uploader(
    "Upload Syllabus (Optional)",
    type=["pdf", "docx","png","jpg","jpeg"], 
    accept_multiple_files=False
)


if uploaded_files:

   st.session_state.pdf_texts = {}

for uploaded_file in uploaded_files:

    file_type = uploaded_file.name.split(".")[-1].lower()

    extracted_text = ""

    # PDF
    if file_type == "pdf":

        doc = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        for page in doc:
            extracted_text += page.get_text() + "\n"

    # IMAGE
    elif file_type in ["png", "jpg", "jpeg"]:

        reader = easyocr.Reader(['en'])
        
        image = Image.open(uploaded_file)

        result = reader.readtext(
            np.array(image),
            detail=0
        )

        extracted_text = "\n".join(result)

    # DOCX
    elif file_type == "docx":

        doc = Document(uploaded_file)

        for para in doc.paragraphs:
            extracted_text += para.text + "\n"

    st.session_state.pdf_texts[
        uploaded_file.name
    ] = extracted_text[:50000]

combined_text = ""

for pdf_name in st.session_state.pdf_texts:
    combined_text += (
        st.session_state.pdf_texts[pdf_name]
        + "\n\n"
    )

st.session_state.notes = combined_text[:50000]   


syllabus_text = ""
if syllabus_file:

    doc = fitz.open(
        stream=syllabus_file.read(),
        filetype="pdf"
    )

    for page in doc:
        syllabus_text += page.get_text() + "\n"
        
       




with st.sidebar:
    st.header("Tools")        

    if st.button("Clear Notes"):
     st.session_state.notes = ""
     st.rerun()

    if st.button("Clear Chat History"):
     st.session_state.chat_history = []
     st.rerun()

    st.markdown("---")
    st.header("Statistics")

    st.metric(
        "Questions Asked",len(st.session_state.chat_history)
    ) 

    pdf_count = len(uploaded_files) if uploaded_files else 0
    st.metric(
        "PDFs Uploaded",pdf_count
    )

col1, col2 = st.columns([5,1])

with col1:
        question = st.text_input(
        "Ask a question",
        label_visibility="collapsed",
        placeholder="Ask a question from your notes..."
    )

with col2:
    submit = st.button("➤")  

if submit and question:

    prompt = f"""
    you are a helpful study assistant.

    use the notes below to answer.

    
    Notes:
    {st.session_state.notes[:50000]}

    Question:
    {question}
    """

    try:
        with st.spinner("Thinking...."):
            response = model.generate_content(prompt)

            answer = response.text

            st.session_state.chat_history.append({
              "question": question , "answer": answer
              })  
            
            

        st.session_state.chat_history = st.session_state.chat_history[-10:]           

        st.subheader("Answer")
        st.write(response.text)

      

        st.success("Answer generated successfully!")

    except Exception as e:
        st.error(f"Error:{e}")



st.markdown("---")
st.subheader("Chat History")

for chat in reversed(st.session_state.chat_history):
 with st.expander(chat["question"]):
    st.write(chat["answer"])


st.markdown("---")
st.subheader("Study Tools")

tab1, tab2, tab3, tab4  = st.tabs([
    "MCQs",
    "Important Questions",
    "Summary", 
    "Exam Paper"
])

with tab1:
    if st.button("Generate MCQs"):
        try:
            with st.spinner("Generating MCQs..."):
                mcq_response = model.generate_content(
                    f"Generate 20 MCQs with 4 options and correct answers from:\n\n{st.session_state.notes[:8000]}"
                )
                st.session_state.mcq = mcq_response.text
                st.write(st.session_state.mcq)
        except Exception as e:
             st.error(f"Error:{e}")

    if "mcq" in st.session_state:
        pdf_file = create_pdf(st.session_state.mcq)
        st.download_button(
            label="Download MCQ PDF",
            data=pdf_file,
            file_name="MCQ.pdf",
            mime="application/pdf"
        )      

with tab2:
    if st.button("Important Questions"):
        try:
            with st.spinner("Generating Questions..."):
                questions_response = model.generate_content(
                f"Generate the 20 most important exam questions likely to appear in university/diplom exam from:\n\n{st.session_state.notes[:8000]}"
                )

                st.session_state.questions = questions_response.text

            st.write(st.session_state.questions)
            
        except Exception as e:
             st.error(f"Error:{e}")

    if "questions" in st.session_state:
        pdf_file = create_pdf(st.session_state.questions)
        st.download_button(
            label="Download IMP PDF",
            data=pdf_file,
            file_name="IMP_Questions.pdf",
            mime="application/pdf"
        )      

with tab3:
    if st.button("Summary"):
        try:
            with st.spinner("Generating Summary..."):

                summary_response = model.generate_content(
                    f"Summarize these notes:\n\n{st.session_state.notes[:8000]}"
                )

                st.session_state.summary = summary_response.text

            st.write(st.session_state.summary)

        except Exception as e:
             st.error(f"Error:{e}")

if not st.session_state.get("notes"):
    st.warning("please upload PDF notes first.")
    st.stop()  

with tab4:

    st.subheader("Generate Exam Paper")

    col1, col2 = st.columns(2)

    with col1:
        mid_sem = st.button("Mid Semester Paper")

    with col2:
        end_sem = st.button("End Semester Paper")

    
    if mid_sem:

        try:

            with st.spinner("Generating Mid Semester Exam Paper..."):

                exam_response = model.generate_content(
                    f"""
                    Generate a university-style examination paper.

                    You are an expert diploma engineering paper setter.

                    Analyze:
                    1. Syllabus weightage
                    2. Chapter wise Notes
                    3. Important Questions
                    4. Question Pattern

                    Rules:
                    - Total Marks: 60
                    - Cover only first 75% syllabus
                    - Follow diploma engineering exam pattern
                    - Follow OR structure
                    - Include 5 marks and 10 marks questions
                    - Focus on repeated questions
                    - Focus on high-weightage chapters
                    - Create realistic examination paper

                    Pattern:

                    Q1.
                    (a),(b) Attempt compulsory two (5 marks each)
                    (c) Attempt compulsory one (10 marks)

                    Q2.
                    (a),(b) Attempt compulsory two (5 marks each)
                    (c) Attempt Any One of Two (10 marks)

                    Q3.
                    (a),(b),(c) Attempt Any Three
                    ((a),(b) = 5 marks each and (c) = 10 marks)

                    Notes:
                    {st.session_state.notes[:50000]}

                    SYLLABUS:
                    {syllabus_text[:10000]}
                    """
                )

                st.session_state.mid_exam_paper = exam_response.text

                st.success("Mid Semester Paper Generated Successfully!")

                st.write(st.session_state.mid_exam_paper)

        except Exception as e:
            st.error(f"Error: {e}")


    if st.session_state.mid_exam_paper:

        pdf_file = create_pdf(st.session_state.mid_exam_paper)

        st.download_button(
            label="Download Mid Sem PDF",
            data=pdf_file,
            file_name="Mid_Sem_Paper.pdf",
            mime="application/pdf"
        )

    st.markdown("---")

    if end_sem:

        try:

            with st.spinner("Generating End Semester Exam Paper..."):

                exam_response = model.generate_content(
                    f"""
                    Generate a university-style examination paper.

                    You are an expert diploma engineering paper setter.

                    Analyze:
                    1. Syllabus weightage
                    2. Chapter wise Notes
                    3. Important Questions
                    4. Question Pattern

                    Rules:
                    - Total Marks: 100
                    - Cover complete syllabus
                    - Follow diploma engineering exam pattern
                    - Follow OR structure
                    - Include 5 marks and 10 marks questions
                    - Follow chapter weightage
                    - Cover all units
                    - Focus on repeated questions
                    - Create realistic examination paper

                    Pattern:

                    Q1.
                    (a),(b) Attempt compulsory two (5 marks each)
                    (c) Attempt compulsory one (10 marks)

                    Q2.
                    (a),(b) Attempt compulsory two (5 marks each)
                    (c) Attempt Any One of Two (10 marks)

                    Q3.
                    (a),(b),(c) Attempt Any Three
                    ((a),(b)=5 marks each and (c)=10 marks)

                    Q4.
                    (a),(b),(c) Attempt Any Three
                    ((a),(b)=5 marks each and (c)=10 marks)

                    Q5.
                    (a),(b),(c) Attempt Any Three
                    ((a),(b)=5 marks each and (c)=10 marks)

                    Notes:
                    {st.session_state.notes[:50000]}

                    SYLLABUS:
                    {syllabus_text[:10000]}
                    """
                )

                st.session_state.final_exam_paper = exam_response.text

                st.success("End Semester Paper Generated Successfully!")

                st.write(st.session_state.final_exam_paper)

        except Exception as e:
            st.error(f"Error: {e}")

    

    if st.session_state.final_exam_paper:

        pdf_file = create_pdf(st.session_state.final_exam_paper)

        st.download_button(
            label="Download Final Sem PDF",
            data=pdf_file,
            file_name="Final_Sem_Paper.pdf",
            mime="application/pdf"
        )