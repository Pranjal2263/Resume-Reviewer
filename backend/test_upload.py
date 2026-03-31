import requests
import os

def test_file_upload():
    """Test file upload to the backend"""
    url = "http://localhost:5000/review"
    
    # Create a simple test file
    test_content = """
    John Doe
    Software Engineer
    
    Experience:
    - Senior Developer at Tech Corp (2020-2023)
    - Junior Developer at Startup Inc (2018-2020)
    
    Skills:
    - Python, JavaScript, React
    - AWS, Docker, Kubernetes
    """
    
    # Save test content to a file
    with open("test_resume.txt", "w") as f:
        f.write(test_content)
    
    try:
        # Test file upload
        with open("test_resume.txt", "rb") as f:
            files = {"resume": ("test_resume.txt", f, "text/plain")}
            data = {"comments": "This is a test upload"}
            
            print("Sending request to:", url)
            response = requests.post(url, files=files, data=data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Feedback: {result.get('feedback', 'No feedback')}")
                print(f"Resume length: {result.get('resume_length', 'Unknown')}")
            else:
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"Exception occurred: {e}")
    
    finally:
        # Clean up test file
        if os.path.exists("test_resume.txt"):
            os.remove("test_resume.txt")

if __name__ == "__main__":
    test_file_upload() 