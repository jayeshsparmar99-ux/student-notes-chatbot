import streamlit as st
import fitz 
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

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

st.set_page_config(
    page_title="Student Notes Chatbot",
    page_icon="🤖"
)

st.title("AI Notes Chatbot")
st.caption("Upload PDFs, Ask questions, Generate IMP questions and MCQs")

uploaded_files = st.file_uploader(
    "Upload PDF Notes",
    type=["pdf"],accept_multiple_files=True
)

if uploaded_files:

    text = ""

    for uploaded_file in uploaded_files:

        st.write(uploaded_file.name)

        doc = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        for page in doc:
            text += page.get_text() + "\n"

    text = text[:10000]

    st.session_state.notes = text

    with st.expander("View Extracted Notes"):
        st.text_area(
            "PDF Content",
            text,
            height=300
        )

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
    {text}

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

        st.session_state.char_history = st.session_state.chat_history[-10:]           

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

tab1, tab2, tab3  = st.tabs([
    "MCQs",
    "Important Questions",
    "Summary" 
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
        st.download_button(
            "Download MCQ",
            st.session_state.mcq,
            file_name="MCQ.txt"
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
        st.download_button(
            "Download IMP",
            st.session_state.questions,
            file_name="IMP question.txt"
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



