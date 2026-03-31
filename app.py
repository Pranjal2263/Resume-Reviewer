from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
import PyPDF2
import io

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST"], allow_headers=["Content-Type"])  # Enable CORS for React frontend

# Configure Google GenAI using API key from OS environment
api_key = os.environ.get('GOOGLE_API_KEY')
if not api_key:
    raise RuntimeError('GOOGLE_API_KEY not found in environment variables.')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        return file.read().decode('utf-8')
    except Exception as e:
        return f"Error reading text file: {str(e)}"

def analyze_resume_with_ai(resume_text, comments=""):
    """Use Google GenAI to analyze the resume"""
    try:
        prompt = f"""
        You are an expert resume reviewer and career coach. Please analyze the following resume and provide constructive feedback.
        
        Resume Content:
        {resume_text}
        
        Additional Comments from User:
        {comments if comments else "None provided"}
        
        Please provide a comprehensive review covering:
        1. Overall structure and formatting
        2. Content quality and relevance
        3. Skills and experience presentation
        4. Areas for improvement
        5. Specific recommendations
        
        Format your response in a clear, professional manner with bullet points where appropriate.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing resume with AI: {str(e)}"

@app.route('/review', methods=['POST'])
def review_resume():
    try:
        print("Received review request")
        print("Files:", request.files)
        print("Form data:", request.form)
        
        # Check if file is present
        if 'resume' not in request.files:
            print("No resume file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        comments = request.form.get('comments', '')
        
        print(f"File received: {file.filename}")
        print(f"Comments: {comments}")
        
        if file.filename == '':
            print("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            print(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type. Please upload PDF or TXT files only.'}), 400
        
        # Extract text from file
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        print(f"File extension: {file_extension}")
        
        if file_extension == 'pdf':
            resume_text = extract_text_from_pdf(file)
        else:  # txt file
            resume_text = extract_text_from_txt(file)
        
        print(f"Extracted text length: {len(resume_text) if resume_text else 0}")
        
        if not resume_text or resume_text.startswith("Error"):
            print(f"Text extraction failed: {resume_text}")
            return jsonify({'error': 'Could not extract text from file'}), 400
        
        # Analyze with AI
        print("Starting AI analysis...")
        ai_feedback = analyze_resume_with_ai(resume_text, comments)
        print("AI analysis completed")
        
        return jsonify({
            'feedback': ai_feedback,
            'resume_length': len(resume_text)
        })
        
    except Exception as e:
        print(f"Exception in review_resume: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Resume Reviewer API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 