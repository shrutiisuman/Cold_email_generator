from PyPDF2 import PdfReader

class Portfolio:
    def __init__(self, file_path="resource/my_resume.pdf"):
        self.file_path = file_path
        self.resume_text = self.extract_resume_text()

    def extract_resume_text(self):
        reader = PdfReader(self.file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def query_links(self, skills):
        matched_skills = []
        for skill in skills:
            if skill.lower() in self.resume_text.lower():
                matched_skills.append(skill)
        # Return matched skills or a string indicating your expertise
        return matched_skills
