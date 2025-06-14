from pathlib import Path
from models import ApplicantProfile, ApplicationDetail
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.algorithms.Regex import Regex

regex = Regex()
idx = 1
def process_directory(directory: Path):
    global idx
    for item in directory.iterdir():
        if item.is_dir():
            print(f"Entering directory: {item}")
            process_directory(item)
        elif item.is_file() and item.suffix.lower() == '.pdf':
            print(f"Processing {item.name}...")

            try:
                regex.setFile(str(item))
                data = regex.extract_all_profile_information()
                print(idx)

                profile = ApplicantProfile(
                    id=idx,
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    date_of_birth=data["date_of_birth"],
                    address=data["address"],
                    phone_number=data["phone_number"]
                )

                app_detail = ApplicationDetail(
                    detail_id=idx,
                    applicant_id=idx,
                    role=data["application_role"],
                    cv_path=data["cv_path"]
                )
                app_detail.save()

                print(f"Inserted: {data['first_name']} {data['last_name']} as {data['application_role']}")
                print("-" * 50)
                idx += 1

            except Exception as e:
                print(f"Failed to insert data for {item.name}: {e}")



def insert_applicant_profile():
    data_dir = Path("data")
    
    if not data_dir.exists() or not data_dir.is_dir():
        print(f"Error: {data_dir} directory not found")
        return
    
    process_directory(data_dir)

if __name__ == "__main__":
    insert_applicant_profile()
    print("Data insertion completed.")