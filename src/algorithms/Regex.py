import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.normalize_pdf import PDFTextConverter
import random
from datetime import datetime, timedelta
import os

class Regex:
    def __init__(self, text: str = ""):
        self.filePath = ""
        self.text = text
        self.pdf_converter = PDFTextConverter()

    def setFile(self, textFilePath: str):
        self.filePath = textFilePath
        self.text = ""
        try:
            self.text = self.pdf_converter.to_text_raw(textFilePath)
        except FileNotFoundError:
            print(f"Error: File {textFilePath} not found.")
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def extract_first_name(self):
        pattern = r"First\s*Name\s*:\s*(.+)"
        match = re.search(pattern, self.text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            first_names = ["Azfa", "Radhiyya", "Hakim", "Rafif", "Farras", 
                           "Barru", "Adi", "Utomo", "Lebron", "Stephen", 
                           "Chinatsu", "Eren", "Smith", "Sarah", "Emma"]
            return random.choice(first_names)
    
    def extract_last_name(self):
        pattern = r"Last\s*Name\s*:\s*(.+)"
        match = re.search(pattern, self.text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            last_names = ["Azfa", "Radhiyya", "Hakim", "Rafif", "Farras", 
                           "Barru", "Adi", "Utomo", "Lebron", "Stephen", 
                           "Chinatsu", "Eren", "Smith", "Sarah", "Emma"]
            return random.choice(last_names)


    def extract_date_of_birth(self):
        pattern = r"Date\s*of\s*Birth\s*:\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})"
        match = re.search(pattern, self.text, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        else:
            start_date = datetime(1970, 1, 1)
            end_date = datetime(2000, 12, 31)
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_days)
            return random_date.strftime("%Y-%m-%d")

    def extract_address(self):
        pattern = r"Address\s*:\s*(.+)"
        match = re.search(pattern, self.text, re.IGNORECASE)
        return match.group(1).strip() if match else "Depok"

    def extract_phone_number(self):
        pattern = r"Phone\s*Number\s*:\s*([\d+\-\s]+)"
        match = re.search(pattern, self.text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            prefix = "08"
            middle = "".join([str(random.randint(0, 9)) for _ in range(2)])
            part1 = "".join([str(random.randint(0, 9)) for _ in range(4)])
            part2 = "".join([str(random.randint(0, 9)) for _ in range(4)])
            return f"{prefix}{middle}-{part1}-{part2}"

    def extract_application_role(self):
        pattern = r"Application\s*Role\s*:\s*(.+)"
        match = re.search(pattern, self.text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        if self.filePath:
            path_parts = self.filePath.split('/')
            if len(path_parts) >= 3:
                return path_parts[-2]
        
        return "Role"
    
    def get_cv_path(self):
        if self.filePath:
            return self.filePath
        return "No CV file provided"

    def extract_all_profile_information(self):
        return {
            "first_name": self.extract_first_name(),
            "last_name": self.extract_last_name(),
            "date_of_birth": self.extract_date_of_birth(),
            "address": self.extract_address(),
            "phone_number": self.extract_phone_number(),
            "application_role": self.extract_application_role(),
            "cv_path": self.get_cv_path()
        }

    def extract_summary(self):
        stop_keywords = [
            "experience", "education", "skills", "qualifications", "achievements",
            "certifications", "projects", "publications", "references",
            "core qualifications", "professional experience", "work history"
        ]
        stop_pattern = "|".join(stop_keywords)
        pattern = re.compile(
            rf"(?i)(?:professional\s+summary|summary|profile)\s*\n(.+?)(?=\n\s*\n|\n\s*(?:{stop_pattern}))",re.DOTALL
        )
        
        match = pattern.search(self.text)
        
        if match:
            summary_text = match.group(1).strip()
            summary_text = re.sub(r'\s*\n\s*', ' ', summary_text)
            return summary_text.strip()
            
        return "Not found"

    def extract_skills(self):
        all_skills = set()
        header_pattern = r"(?i)^\s*(skills|technical\s+skills|core\s+competencies)\s*$"
        end_section_pattern = r"^\s*(professional experience|education|affiliations|interests|languages|additional information|certification)"

        in_skills_section = False
        for line in self.text.split('\n'):
            line = line.strip()

            if re.match(header_pattern, line):
                in_skills_section = True
                continue

            if re.match(end_section_pattern, line, re.IGNORECASE) or not line:
                in_skills_section = False
                continue

            if in_skills_section:
                normalized_line = re.sub(r'\s*[/;•]\s*', ',', line)
                
                normalized_line = re.sub(r'\s*\(.*?\)', '', normalized_line)
                
                skills_list = normalized_line.split(',')
                
                for skill in skills_list:
                    skill = skill.strip()
                    if len(skill) > 2 and not skill.replace('.', '', 1).isdigit():
                        all_skills.add(skill)

        return sorted(list(all_skills))

    def extract_experience(self):
        experiences = []
        lines = self.text.splitlines()
        
        stop_headers = r"(?i)^(education|languages|skills|affiliations|references)"

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            date_pattern = r"(?i)((?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s+to\s+(?:Current|Present|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}))"
            date_match = re.search(date_pattern, line)

            if date_match:
                date_str = date_match.group(1)
                position = line.replace(date_str, "").strip().rstrip(',')

                try:
                    start_date, end_date = [d.strip() for d in date_str.split(" to ")]
                except ValueError:
                    start_date, end_date = date_str, "N/A"

                company_name = ""
                location = ""
                if i + 1 < len(lines):
                    company_line = lines[i+1].strip()
                    parts = company_line.split('–', 1)
                    if len(parts) == 1:
                        parts = company_line.split('-', 1)
                    
                    if len(parts) == 2:
                        company_name = parts[0].strip()
                        location = parts[1].strip()
                    else:
                        company_name = company_line
                
                description_lines = []
                j = i + 2 
                while j < len(lines):
                    desc_line = lines[j].strip()
                    
                    if not desc_line or re.search(date_pattern, desc_line) or re.match(stop_headers, desc_line):
                        break
                    
                    description_lines.append(desc_line.lstrip('• ').strip())
                    j += 1
                
                experiences.append({
                    "position": position,
                    "company": company_name,
                    "location": location,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": description_lines
                })
                
                i = j - 1
            
            i += 1
        
        return experiences

    def extract_education(self):
        educations = []
        
        edu_section_pattern = r"(?i)education\s*\n((?:.|\n)+?)(?=\n\s*\n|\Z|affiliations|certifications|skills)"
        edu_match = re.search(edu_section_pattern, self.text)
        
        if not edu_match:
            return []

        edu_text = edu_match.group(1).strip()
        lines = edu_text.split("\n")
        
        degree_keywords = r"(?i)(MBA|Bachelors\s*Degree|Master|Associate|Ph\.?D)"

        for line in lines:
            line = line.strip()
            
            if re.search(degree_keywords, line):
                entry = {
                    "degree": "N/A",
                    "field": "N/A",
                    "institution": "N/A",
                    "year": "N/A",
                    "location": "N/A"
                }

                location_parts = line.split('-', 1)
                main_part = location_parts[0].strip()
                if len(location_parts) > 1:
                    entry["location"] = location_parts[1].strip()

                degree_match = re.search(degree_keywords, main_part)
                if degree_match:
                    degree_text = degree_match.group(0)
                    entry["degree"] = degree_text.replace(',', '').strip()
                    
                    field_inst_text = main_part.replace(degree_text, "").strip()
                    

                    text_parts = field_inst_text.rsplit(' ', 2)
                    if len(text_parts) > 2 and "college" in text_parts[1].lower():
                        entry["institution"] = f"{text_parts[1]} {text_parts[2]}"
                        entry["field"] = text_parts[0].replace(',', '').strip()
                    else:
                        entry["field"] = field_inst_text
                
                educations.append(entry)
            
        return 
    
# pdf_converter = PDFTextConverter(max_workers=8)
# pdf_converter.set_pdf_path("data/HR/11763983.pdf")
# text = pdf_converter.to_text_raw("data/HR/11763983.pdf")
# regex = Regex(text)
# print(regex.extract_experience())