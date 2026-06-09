#  AI Notes Chatbot

An AI-powered study assistant built with Streamlit and Google Gemini AI.

Students can upload PDF notes, ask questions, generate MCQs, create important exam questions, and generate summaries from their study material.

##  Live Demo

https://student-notes-chatbot-b7fcweobpsmm3swbg3556b.streamlit.app/



##  Features

*  Upload one or multiple PDF notes
*  Ask questions from uploaded notes
*  Generate MCQs automatically
*  Generate important exam questions
*  Generate summaries
*  Multi-PDF support
*  Chat history
*  Clear notes and chat history

##  Tech Stack

* Python
* Streamlit
* Google Gemini API
* PyMuPDF (fitz)
* python-dotenv
* Git & GitHub

##  Installation

Clone the repository:

bash
git clone https://github.com/jayeshparmar99-ux/student-notes-chatbot.git


Install dependencies:

bash
pip install -r requirements.txt


Create a `.env` file:

.env
GEMINI_API_KEY=your_api_key_here


Run the application:

bash
streamlit run app.py


##  Project Structure

student-notes-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── screenshot.png
├── .gitignore
└── .env


##  Author

Jayesh Parmar
