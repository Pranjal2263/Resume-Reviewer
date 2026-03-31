# AI-Powered Resume Reviewer - Backend

A Flask-based backend for the AI-Powered Resume Reviewer application that uses Google GenAI to analyze resumes.

## Features

- File upload handling (PDF and TXT formats)
- Text extraction from PDF files
- AI-powered resume analysis using Google GenAI
- RESTful API endpoints
- CORS support for frontend integration

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `env_example.txt` to `.env`
   - Add your Google GenAI API key to the `.env` file:
     ```
     GOOGLE_GENAI_API_KEY=your_actual_api_key_here
     ```

3. **Run the application:**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`

## API Endpoints

### POST /review
Upload and analyze a resume file.

**Request:**
- `resume`: File upload (PDF or TXT)
- `comments`: Optional additional comments (form data)

**Response:**
```json
{
  "feedback": "AI-generated feedback...",
  "resume_length": 1234
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Resume Reviewer API is running"
}
```

## File Structure

```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── env_example.txt     # Environment variables example
├── README.md          # This file
└── uploads/           # Upload directory (created automatically)
```

## Error Handling

The application includes comprehensive error handling for:
- Missing files
- Invalid file types
- PDF parsing errors
- AI API errors
- General server errors

## Security Notes

- Only PDF and TXT files are allowed
- Files are processed in memory (not saved permanently)
- CORS is enabled for frontend integration 