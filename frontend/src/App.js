import React, { useState } from "react";

function App() {
  const [resume, setResume] = useState(null);
  const [comments, setComments] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setResume(e.target.files[0]);
  };

  const handleCommentsChange = (e) => {
    setComments(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resume) {
      setResult("Please upload a resume file.");
      return;
    }
    setLoading(true);
    setResult("");
    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("comments", comments);

    try {
      const response = await fetch("http://localhost:5000/review", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data.feedback || "No feedback received.");
    } catch (error) {
      setResult("Error submitting resume. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="container" style={{ maxWidth: 600, margin: "40px auto" }}>
      <h2 className="mb-4">AI-Powered Resume Reviewer</h2>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <div className="mb-3">
          <label htmlFor="resume" className="form-label">
            Upload your resume (PDF or TXT):
          </label>
          <input
            className="form-control"
            type="file"
            id="resume"
            name="resume"
            accept=".pdf,.txt"
            onChange={handleFileChange}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="comments" className="form-label">
            Additional Comments (optional):
          </label>
          <textarea
            className="form-control"
            id="comments"
            name="comments"
            rows="3"
            value={comments}
            onChange={handleCommentsChange}
          />
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Reviewing..." : "Review Resume"}
        </button>
      </form>
      <div className="mt-4" id="result">
        {result && (
          <div className="alert alert-info" style={{ whiteSpace: "pre-line" }}>
            {result}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
