# AI Notes Chatbot

An AI-powered study assistant built with Streamlit and Google Gemini that allows students to upload PDF notes, ask questions, generate MCQs, important questions, and summaries.

## Features

* Upload one or more PDF notes
* Ask questions from uploaded notes
* Generate MCQs automatically
* Generate important exam questions
* Generate concise summaries
* View chat history

## Technologies Used

* Python
* Streamlit
* Google Gemini API
* PyMuPDF (fitz)
* python-dotenv

## Installation

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/student-notes-chatbot.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your Gemini API key

```env
GEMINI_API_KEY=your_api_key_here
```

4. Run the application

```bash
streamlit run app.py
```

## Project Structure

```text
student-notes-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

## Author

Jayesh Parmar
