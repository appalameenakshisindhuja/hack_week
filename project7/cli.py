#!/usr/bin/env python3
"""
Resume Analyzer CLI Tool
A tool to extract text from PDF resumes, count skill mentions, and suggest improvements.
"""

import argparse
import sys
import re
from collections import Counter
from pathlib import Path
import json

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not found. Install with: pip install PyMuPDF")
    sys.exit(1)

class ResumeAnalyzer:
    def __init__(self):
        # Comprehensive skill categories with variations
        self.skill_categories = {
            'Programming Languages': {
                'python': ['python', 'py', 'python3'],
                'javascript': ['javascript', 'js', 'node.js', 'nodejs', 'react', 'vue', 'angular'],
                'java': ['java', 'spring', 'hibernate'],
                'sql': ['sql', 'mysql', 'postgresql', 'postgres', 'sqlite', 'oracle', 'mssql'],
                'r': ['r programming', 'r language', 'rstudio'],
                'c++': ['c++', 'cpp', 'c plus plus'],
                'c#': ['c#', 'csharp', 'c sharp', '.net'],
                'go': ['golang', 'go language'],
                'rust': ['rust language', 'rust programming'],
                'scala': ['scala programming'],
                'ruby': ['ruby', 'ruby on rails', 'rails'],
                'php': ['php', 'laravel', 'symfony'],
                'swift': ['swift', 'ios development'],
                'kotlin': ['kotlin', 'android development']
            },
            'Data Science & ML': {
                'machine learning': ['machine learning', 'ml', 'artificial intelligence', 'ai'],
                'deep learning': ['deep learning', 'neural networks', 'tensorflow', 'pytorch', 'keras'],
                'data science': ['data science', 'data scientist', 'data analysis', 'analytics'],
                'statistics': ['statistics', 'statistical analysis', 'statistical modeling'],
                'pandas': ['pandas', 'dataframe'],
                'numpy': ['numpy', 'numerical computing'],
                'scikit-learn': ['scikit-learn', 'sklearn', 'sci-kit learn'],
                'nlp': ['nlp', 'natural language processing', 'text mining', 'sentiment analysis'],
                'computer vision': ['computer vision', 'opencv', 'image processing'],
                'big data': ['big data', 'hadoop', 'spark', 'kafka', 'elasticsearch']
            },
            'Cloud & DevOps': {
                'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda', 'cloudformation'],
                'azure': ['azure', 'microsoft azure', 'azure devops'],
                'gcp': ['gcp', 'google cloud platform', 'google cloud'],
                'docker': ['docker', 'containerization', 'containers'],
                'kubernetes': ['kubernetes', 'k8s', 'orchestration'],
                'ci/cd': ['ci/cd', 'continuous integration', 'continuous deployment', 'jenkins', 'gitlab ci'],
                'terraform': ['terraform', 'infrastructure as code', 'iac'],
                'ansible': ['ansible', 'configuration management'],
                'linux': ['linux', 'unix', 'bash', 'shell scripting']
            },
            'Web Development': {
                'html/css': ['html', 'css', 'html5', 'css3', 'sass', 'less'],
                'frontend': ['frontend', 'front-end', 'ui/ux', 'responsive design'],
                'backend': ['backend', 'back-end', 'api development', 'rest api', 'graphql'],
                'databases': ['database', 'mongodb', 'redis', 'nosql', 'relational database'],
                'web frameworks': ['django', 'flask', 'fastapi', 'express', 'spring boot']
            },
            'Tools & Platforms': {
                'git': ['git', 'github', 'gitlab', 'version control'],
                'jira': ['jira', 'project management', 'agile', 'scrum'],
                'tableau': ['tableau', 'data visualization', 'power bi', 'looker'],
                'excel': ['excel', 'spreadsheet', 'vlookup', 'pivot tables'],
                'jupyter': ['jupyter', 'jupyter notebook', 'ipython']
            }
        }

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    def normalize_text(self, text):
        """Normalize text for better matching"""
        # Convert to lowercase and remove extra whitespace
        text = re.sub(r'\s+', ' ', text.lower().strip())
        # Remove special characters but keep periods for abbreviations
        text = re.sub(r'[^\w\s\.\-\+#]', ' ', text)
        return text

    def count_skills(self, text):
        """Count skill mentions in the text"""
        normalized_text = self.normalize_text(text)
        skill_counts = {}
        
        for category, skills in self.skill_categories.items():
            skill_counts[category] = {}
            for skill_name, variations in skills.items():
                count = 0
                for variation in variations:
                    # Use word boundaries for exact matches
                    pattern = r'\b' + re.escape(variation.lower()) + r'\b'
                    matches = re.findall(pattern, normalized_text)
                    count += len(matches)
                
                if count > 0:
                    skill_counts[category][skill_name] = count
        
        return skill_counts

    def suggest_improvements(self, skill_counts, job_role=None):
        """Suggest improvements based on missing skills"""
        suggestions = []
        
        # Define recommended skills for different roles
        role_recommendations = {
            'data_scientist': ['python', 'sql', 'machine learning', 'statistics', 'pandas', 'scikit-learn'],
            'software_engineer': ['python', 'javascript', 'sql', 'git', 'docker', 'ci/cd'],
            'web_developer': ['javascript', 'html/css', 'frontend', 'backend', 'git', 'databases'],
            'devops_engineer': ['linux', 'docker', 'kubernetes', 'aws', 'ci/cd', 'terraform'],
            'ml_engineer': ['python', 'machine learning', 'deep learning', 'docker', 'aws', 'git']
        }
        
        # Get flat list of found skills
        found_skills = set()
        for category_skills in skill_counts.values():
            found_skills.update(category_skills.keys())
        
        # General suggestions based on common requirements
        common_missing = []
        important_skills = ['python', 'sql', 'git', 'machine learning', 'javascript']
        
        for skill in important_skills:
            if skill not in found_skills:
                common_missing.append(skill)
        
        if common_missing:
            suggestions.append({
                'type': 'missing_common_skills',
                'title': 'Consider adding these commonly sought skills',
                'skills': common_missing
            })
        
        # Role-specific suggestions
        if job_role and job_role in role_recommendations:
            role_missing = []
            for skill in role_recommendations[job_role]:
                if skill not in found_skills:
                    role_missing.append(skill)
            
            if role_missing:
                suggestions.append({
                    'type': 'role_specific',
                    'title': f'Skills recommended for {job_role.replace("_", " ").title()}',
                    'skills': role_missing
                })
        
        # Category balance suggestions
        category_counts = {cat: len(skills) for cat, skills in skill_counts.items() if skills}
        
        if not category_counts.get('Cloud & DevOps', 0):
            suggestions.append({
                'type': 'category_gap',
                'title': 'Consider adding Cloud/DevOps skills',
                'skills': ['docker', 'aws', 'kubernetes', 'ci/cd']
            })
        
        if not category_counts.get('Data Science & ML', 0) and job_role != 'web_developer':
            suggestions.append({
                'type': 'category_gap',
                'title': 'Consider adding Data Science skills',
                'skills': ['pandas', 'machine learning', 'statistics']
            })
        
        return suggestions

    def generate_report(self, pdf_path, job_role=None, output_format='text'):
        """Generate complete analysis report"""
        print(f"Analyzing resume: {pdf_path}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return None
        
        # Count skills
        skill_counts = self.count_skills(text)
        
        # Generate suggestions
        suggestions = self.suggest_improvements(skill_counts, job_role)
        
        # Create report
        report = {
            'file': str(pdf_path),
            'total_skills_found': sum(len(skills) for skills in skill_counts.values()),
            'skill_counts': skill_counts,
            'suggestions': suggestions,
            'text_length': len(text)
        }
        
        if output_format == 'json':
            return json.dumps(report, indent=2)
        else:
            return self.format_text_report(report)

    def format_text_report(self, report):
        """Format report as readable text"""
        output = []
        output.append("=" * 60)
        output.append("RESUME ANALYSIS REPORT")
        output.append("=" * 60)
        output.append(f"File: {report['file']}")
        output.append(f"Total Skills Found: {report['total_skills_found']}")
        output.append(f"Text Length: {report['text_length']} characters")
        output.append("")
        
        # Skill counts by category
        output.append("SKILLS BREAKDOWN")
        output.append("-" * 30)
        
        for category, skills in report['skill_counts'].items():
            if skills:
                output.append(f"\n{category}:")
                for skill, count in sorted(skills.items(), key=lambda x: x[1], reverse=True):
                    output.append(f"  • {skill.title()}: {count} mention(s)")
        
        # Suggestions
        if report['suggestions']:
            output.append("\n" + "=" * 60)
            output.append("IMPROVEMENT SUGGESTIONS")
            output.append("=" * 60)
            
            for i, suggestion in enumerate(report['suggestions'], 1):
                output.append(f"\n{i}. {suggestion['title']}:")
                for skill in suggestion['skills']:
                    output.append(f"   • {skill.title()}")
        
        output.append("\n" + "=" * 60)
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze PDF resumes for skill mentions and improvement suggestions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python resume_analyzer.py resume.pdf
  python resume_analyzer.py resume.pdf --role data_scientist
  python resume_analyzer.py resume.pdf --output report.txt
  python resume_analyzer.py resume.pdf --format json --output report.json
        """
    )
    
    parser.add_argument('pdf_path', help='Path to the PDF resume file')
    parser.add_argument('--role', choices=['data_scientist', 'software_engineer', 'web_developer', 'devops_engineer', 'ml_engineer'],
                       help='Target job role for specific recommendations')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Output file path (default: print to console)')
    
    args = parser.parse_args()
    
    # Validate input file
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: File '{pdf_path}' not found.")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"Error: File '{pdf_path}' is not a PDF file.")
        sys.exit(1)
    
    # Create analyzer and generate report
    analyzer = ResumeAnalyzer()
    report = analyzer.generate_report(pdf_path, args.role, args.format)
    
    if report is None:
        print("Error: Could not analyze the resume.")
        sys.exit(1)
    
    # Output report
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {args.output}")
        except Exception as e:
            print(f"Error saving report: {e}")
            sys.exit(1)
    else:
        print(report)

if __name__ == "__main__":
    main()