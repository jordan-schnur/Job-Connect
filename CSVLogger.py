import csv
import datetime
from typing import Dict, Optional, List

from Job import Job
from Recruiter import Recruiter


class CSVLogger:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def _read_csv(self) -> list:
        with open(self.file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def _write_csv(self, data: list):
        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def update_row(self, linkedin_id: str, updated_info: Dict[str, Optional[str]]):
        data = self._read_csv()
        for row in data:
            if row['LinkedIn ID'] == linkedin_id:
                row.update(updated_info)
                break
        self._write_csv(data)

    def add_row(self, new_info: Dict[str, Optional[str]]):
        data = self._read_csv()
        if not any(row['LinkedIn ID'] == new_info['LinkedIn ID'] for row in data):
            data.append(new_info)
            self._write_csv(data)

    def _job_to_dict(self, job: Job) -> Dict[str, str]:
        recruiter_info = job.recruiter.__dict__ if job.recruiter else {f'Recruiter {key}': '' for key in
                                                                       Recruiter().__dict__.keys()}
        return {
            'Date Found': datetime.datetime.now().strftime('%Y-%m-%d'),
            'Time Found': datetime.datetime.now().strftime('%H:%M'),
            'LinkedIn ID': job.id,
            'Location': job.location,
            'Company Name': job.company_name,
            'Company Url': job.company_url,
            'Job Title': job.title,
            'Technologies': ', '.join(job.technologies),
            **recruiter_info
        }

    def _dict_to_job(self, row: Dict[str, str]) -> Job:
        recruiter_keys = ['LinkedIn', 'Name', 'Email', 'Title', 'Company Name']
        recruiter_info = {key: row[f'Recruiter {key}'] for key in recruiter_keys}

        recruiter = Recruiter(**recruiter_info) if any(recruiter_info.values()) else None

        job_info = {
            'job_id': row['LinkedIn ID'],
            'title': row['Job Title'],
            'company_name': row['Company Name'],
            'company_url': row['Company URL'],
            'location': row['Location'],
            'description': "",
            'technologies': set(row['Technologies'].split(', ')),
            'recruiter': recruiter
        }
        return Job(**job_info)

    def add_job(self, job: Job):
        current_datetime = datetime.datetime.now()

        self.add_row({
            'Date Found': current_datetime.strftime('%Y-%m-%d'),
            'Time Found': current_datetime.strftime('%H:%M'),
            'LinkedIn ID': job.id,
            'Location': job.location,
            'Company Name': job.company_name,
            'Company URL': job.company_url,
            'Job Title': job.title,
            'Technologies': ", ".join(job.technologies),
            'Recruiter Name': None,
            'Recruiter Email': None,
            'Recruiter LinkedIn': None,
            'Recruiter Title': None,
            'Recruiter Company Name': None
        })

    def get_jobs(self) -> List[Job]:
        return [self._dict_to_job(row) for row in self._read_csv()]

    def get_job_by_id(self, job_id: str) -> Optional[Job]:
        data = self._read_csv()
        for row in data:
            if row['LinkedIn ID'] == job_id:
                return self._dict_to_job(row)
        return None

    def update_via_with_recruiter(self, linkedin_id: str, recruiter: Job.recruiter):
        self.update_row(linkedin_id, {
            'Recruiter Name': recruiter.name,
            'Recruiter Email': recruiter.email,
            'Recruiter LinkedIn': recruiter.url,
            'Recruiter Title': recruiter.title,
            'Recruiter Company Name': recruiter.company_name
        })

# Update an existing row
# logger.update_row('12345', {'Recruiter Name': 'John Doe', 'Recruiter Email': 'johndoe@example.com'})
#
# # Add a new row
# logger.add_row({
#     'Date Found': '2024-03-04',
#     'Time Found': '10:00',
#     'LinkedIn ID': '67890',
#     'Location': 'Pittsburgh, PA',
#     'Company Name': 'NewTech Inc.',
#     'Company URL': 'https://newtechinc.com',
#     'Technologies': 'JavaScript, PHP',
#     'Recruiter Name': None,
#     'Recruiter Email': None,
#     'Recruiter LinkedIn': None,
#     'Recruiter Title': None,
#     'Recruiter Company Name': None
# })
