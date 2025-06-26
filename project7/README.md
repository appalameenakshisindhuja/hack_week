# Python Script

## About
I've created a comprehensive Python CLI tool for resume analysis! Here's what the tool does:

PDF Text Extraction: Uses PyMuPDF (fitz) to extract text from PDF resumes with robust error handling.
Comprehensive Skill Detection: Tracks 50+ skills across 5 categories:

Programming Languages (Python, JavaScript, SQL, Java, etc.)
Data Science & ML (Machine Learning, TensorFlow, Pandas, etc.)
Cloud & DevOps (AWS, Docker, Kubernetes, etc.)
Web Development (HTML/CSS, React, APIs, etc.)
Tools & Platforms (Git, Jira, Tableau, etc.)

Smart Matching: Uses word boundaries and variations (e.g., "js" for JavaScript, "k8s" for Kubernetes) for accurate skill detection.
Role-Specific Suggestions: Provides targeted recommendations for data scientists, software engineers, web developers, DevOps engineers, and ML engineers.
Flexible Output: Supports both human-readable text and JSON formats.

## Requirements

- Python 3.x installed on your system
- install PyMuPDF

## How to Run

1. Open a terminal or command prompt.
2. Navigate to the folder where the script is saved.
3. Run the script 
# for Basic analysis
python resume_analyzer.py resume.pdf

# Role-specific analysis
python resume_analyzer.py resume.pdf --role data_scientist

# Save report to file
python resume_analyzer.py resume.pdf --output analysis.txt

# JSON output
python resume_analyzer.py resume.pdf --format json --output report.json
