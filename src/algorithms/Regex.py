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
            # Generate random date between 1970-01-01 and 2000-12-31
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
            # Generate random phone number in format 08xx-xxxx-xxxx
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

# if __name__ == "__main__":
#     base_folder = "data"
#     regex = Regex()
    
#     # Check if the directory exists
#     if not os.path.isdir(base_folder):
#         print(f"Directory {base_folder} not found")
#     else:
#         # Function to process all PDF files in a directory and its subdirectories
#         def process_directory(directory):
#             for item in os.listdir(directory):
#                 item_path = os.path.join(directory, item)
                
#                 # If the item is a directory, process it recursively
#                 if os.path.isdir(item_path):
#                     print(f"Entering directory: {item_path}")
#                     process_directory(item_path)
                
#                 # Process PDF files
#                 elif os.path.isfile(item_path) and item.endswith('.pdf'):
#                     print(f"Processing {item}...")
#                     regex.setFile(item_path)
                    
#                     extracted_data = regex.extract_all()
#                     print(extracted_data)
#                     print("-" * 50)
        
#         # Start processing from the base folder
#         process_directory(base_folder)
