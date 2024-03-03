class Recruiter:
    url = None
    name = None
    email = None
    title = None
    company_name = None
    contact_info = None
    description = None

    def __init__(self, url, name, email, title, company_name, contact_info):
        self.url = url
        self.name = name
        self.email = email
        self.title = title
        self.company_name = company_name
        self.contact_info = contact_info
