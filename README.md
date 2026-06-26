#  AI Notes Chatbot

An AI-powered study assistant built with **Streamlit**, **Google Gemini AI**, and **Groq AI**.

Students can upload study materials, ask questions, generate summaries, MCQs, important exam questions, and university-style examination papers from their notes.

---

#  Overview

AI Notes Chatbot is a smart study assistant designed to help students learn more efficiently. It allows users to upload notes in multiple formats and interact with them using Artificial Intelligence. The chatbot can answer questions, generate summaries, create MCQs, produce important exam questions, and automatically generate university-style examination papers.

---

#  Features

*  Upload multiple PDF notes
*  Upload DOCX notes
*  OCR support for image-based notes
*  AI Chat with uploaded notes
*  Generate concise summaries
*  Generate important exam questions
*  Generate MCQs with answers
*  Generate Mid Semester Examination Papers
*  Generate End Semester Examination Papers
*  Download generated content as PDF
*  Dual AI Support (Google Gemini + Groq)
*  Automatic API Fallback
*  Chat History
*  Clear Notes & Chat History

---

#  Technology Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Core Programming Language       |
| Streamlit         | Web Application Framework       |
| Google Gemini API | Primary AI Model                |
| Groq API          | Backup AI Model                 |
| PyMuPDF           | PDF Text Extraction             |
| EasyOCR           | Image Text Recognition          |
| python-docx       | DOCX File Reading               |
| ReportLab         | PDF Generation                  |
| NumPy             | Image Processing                |
| Pillow            | Image Handling                  |
| python-dotenv     | Environment Variable Management |
| Git & GitHub      | Version Control                 |

---

#  Working Process
1. User uploads PDF, DOCX, or image notes.
2. The application extracts text from the uploaded files.
3. Extracted text is stored temporarily.
4. User asks a question or selects a study tool.
5. AI processes the request using Google Gemini.
6. If Gemini reaches its quota, the application automatically switches to Groq.
7. The generated response is displayed and can be downloaded as a PDF.

---

#  Live Demo

https://student-notes-chatbot-b7fcweobpsmm3swbg3556b.streamlit.app/

---

#  Installation

```bash
git clone https://github.com/jayeshparmar99-ux/student-notes-chatbot.git

cd student-notes-chatbot

pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

Run the project

```bash
streamlit run app.py
```

---

#  Project Structure

```text
student-notes-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── screenshot.png
├── .gitignore
└── .env
```

---

#  Advantages

* Saves study time
* Makes revision faster
* Automatically generates practice questions
* Supports multiple document formats
* Simple and user-friendly interface
* Automatic AI fallback for uninterrupted service
* Useful for students preparing for examinations

---

#  Future Enhancements

*  RAG (Retrieval-Augmented Generation)
*  Vector Database Integration
*  Voice Input & Voice Output
*  Multi-language Support
*  User Authentication
*  Cloud Database
*  Learning Analytics Dashboard
*  Mobile Responsive UI
*  Previous Year Question Paper Analysis


---

# Conclusion

AI Notes Chatbot simplifies the learning process by combining document processing with Artificial Intelligence. It enables students to quickly understand study material, practice important questions, generate summaries, and prepare examination papers. With dual AI support using Google Gemini and Groq, the application provides a more reliable and uninterrupted learning experience.

---

# Developed By
Jayesh Parmar

Diploma in Information Technology

Gyanmanjari Diploma Engineering College.Bhavnagar

Internship Project – 2026

GitHub: https://github.com/jayeshparmar99-ux
