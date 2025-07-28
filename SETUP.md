# Flask Note-Taking Application Setup Guide

## Prerequisites
- Python 3.7+ installed on your system
- pip (Python package installer)
- Git (for version control)

## Installation Steps

### 1. Clone/Download the Project
```bash
# If using Git
git clone <repository-url>
cd Note_website

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Or install individually:
pip install Flask Flask-SQLAlchemy Flask-Login google-generativeai python-dotenv
```

### 4. Environment Setup (Optional)
Create a `.env` file in the project root for API keys:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
SECRET_KEY=your_secret_key_here
```

### 5. Run the Application
```bash
# Start the development server
python main.py
```

The application will be available at: http://localhost:5000

## Project Structure
```
Note_website/
├── main.py              # Application entry point
├── requirements.txt     # Dependencies list
├── Note_website/        # Main package
│   ├── __init__.py     # App factory
│   ├── model.py        # Database models
│   ├── auth.py         # Authentication routes
│   ├── views.py        # Main application routes
│   └── templates/      # HTML templates
└── database.db         # SQLite database (auto-created)
```

## Features
- ✅ User registration and authentication
- ✅ Create, edit, delete notes with subjects
- ✅ Task management with completion tracking
- ✅ Download notes as text files
- ✅ AI chatbot integration (Google Gemini)
- ✅ Responsive design for mobile and desktop
- ✅ Professional gradient UI

## Troubleshooting

### Common Issues:
1. **Module not found**: Make sure virtual environment is activated and dependencies are installed
2. **Database errors**: Delete `database.db` file and restart the app to recreate
3. **AI chatbot not working**: Check if GEMINI_API_KEY is properly configured
4. **Port already in use**: Change port in main.py: `app.run(debug=True, port=5001)`

### Development Mode:
- Debug mode is enabled by default (auto-reload on code changes)
- Database is created automatically on first run
- Flash messages show success/error feedback

## Team Development
- Each developer should create their own virtual environment
- Database file (`database.db`) should not be committed to version control
- Use environment variables for sensitive data (API keys)
- Test all features before pushing changes

## Production Deployment
- Set `debug=False` in main.py
- Use production WSGI server (Gunicorn, uWSGI)
- Configure proper database (PostgreSQL, MySQL)
- Set up environment variables securely
- Enable HTTPS/SSL certificates
