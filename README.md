# AI-Generative Question Paper Maker (QuestionMaster)

A powerful web application built with Python and Flask that leverages Google's Gemini AI to automatically generate custom university-level Computer Science & Engineering question papers. Teachers can specify subjects, topics, difficulty levels, and the exact mix of question types they need, then download the final output directly as a PDF.

## 🌟 Features

* **User Authentication**: Secure registration, login, and session management for teachers.
* **Personalized Dashboard**: View and manage previously generated question papers.
* **Highly Customizable Generation**:
  * Select from multiple subjects and topics (or add custom topics).
  * Choose the exact number of questions per type:
    * Multiple Choice Questions (MCQs)
    * Fill in the Blanks
    * Match the Following
    * Short Answer Questions
    * Long Answer Questions
  * Set difficulty level.
* **AI-Powered**: Uses Google's modern Generative AI (`gemini-2.0-flash-lite`, `gemini-2.0-flash`, `gemini-2.5-flash`) via the `google-genai` SDK for high-quality, relevant academic questions.
* **PDF Export**: Instantly download the generated paper into a nicely formatted PDF file utilizing `xhtml2pdf`.
* **Mock Data Fallbacks**: Graceful fallbacks using mock data generation if API rate limits or errors are encountered.

## 🛠️ Tech Stack

* **Backend**: Python, Flask, Flask-Login, Flask-WTF
* **Database**: SQLite with SQLAlchemy ORM
* **AI Integration**: `google-genai`
* **PDF Generation**: `xhtml2pdf`
* **Environment Management**: `python-dotenv`

## 🚀 Setup & Installation

Follow these steps to run the application locally:

### 1. Prerequisites
* Python 3.8+ installed
* A Google Gemini API Key. You can get one from the Google AI Studio.

### 2. Clone the Repository
Clone this directory to your local machine.

### 3. Install Dependencies
Open standard terminal or command prompt in the project directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a file named `.env` in the root directory of the project and define the following variables:

```env
SECRET_KEY=your_secure_random_secret_key
GEMINI_API_KEY=your_google_gemini_api_key
```

### 5. Initialize & Run
Start the application. The SQLite database schema and tables will be created automatically upon startup.

```bash
python app.py
```

By default, the application runs on `http://127.0.0.1:5000/`.

## 📁 Project Structure

* `app.py`: Main application entry point, route definitions, and lightweight database auto-migration.
* `utils.py`: Contains the logic for interacting with the Google Gemini API, parsing JSON responses, fallback mock data, and HTML-to-PDF conversion logic.
* `models.py`: Defines the SQLAlchemy database models (`User` and `QuestionPaper`).
* `forms.py`: Flask-WTF form definitions and the default Subject/Topics mapping.
* `extensions.py`: Centralized extension initialization (db, login_manager, csrf).
* `/templates`: HTML templates for rendering views using Jinja2 (Dashboard, Auth, PDF Template, etc.).
* `/static`: Contains CSS styling rules and static assets.
* `/instance/site.db`: The local SQLite database file (created automatically).
