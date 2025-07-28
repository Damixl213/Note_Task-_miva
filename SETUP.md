# Flask Note-Taking Application Setup Guide

## Prerequisites
- Python 3.7+ installed on your system
- pip (Python package installer)
- Git (for version control)
- Google Gemini API key (for chatbot functionality)

## Installation Steps

### 1. Clone/Download the Project
```bash
git clone <repository-url>
cd Note_website
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
```

### 4. Environment Setup (IMPORTANT for AI Chatbot)
Create a `.env` file in the project root:
```env
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_actual_google_gemini_api_key_here
SECRET_KEY=your_random_secret_key_for_flask_sessions
```

**How to get Google Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it in your .env file

### 5. Run the Application
```bash
# Start the development server
python main.py
```

The application will be available at: http://localhost:5000

## Environment Variables Explained

- **GEMINI_API_KEY**: Required for AI chatbot functionality
- **SECRET_KEY**: Used for Flask session security (generate a random string)
- **DATABASE_URL**: Optional, for production database configuration

## Testing the Chatbot
1. Register/Login to the application
2. Click the blue chat icon in the bottom right
3. Type a message and press Send
4. The AI should respond (requires valid API key)

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

### Chatbot Issues:
- **"API key not configured"**: Check your .env file exists and has correct GEMINI_API_KEY
- **"AI assistant temporarily unavailable"**: API key might be invalid or quota exceeded
- **"You have to login or signup"**: Make sure you're logged in before using the chatbot

### Common Issues:
1. **Module not found**: Activate virtual environment and install requirements
2. **Database errors**: Delete `database.db` and restart app
3. **Environment variables not loading**: Install python-dotenv: `pip install python-dotenv`

## Development Notes
- .env file contains sensitive information - never commit it to version control
- Add .env to your .gitignore file
- Use different API keys for development and production

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
