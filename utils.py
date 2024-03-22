import re


def normalize_company_name(company_name):
    # Define a regular expression pattern to find legal entity designations
    pattern = r"\s*(LLC|Inc|Corp|Corporation|Limited|Ltd|GmbH|AG|KG|Co)\.?\s*$"
    # Use regex to replace these designations with an empty string
    normalized_name = re.sub(pattern, '', company_name, flags=re.IGNORECASE)
    return normalized_name


def normalize_job_title(job_title):
    # Define a regular expression pattern to trim anything after a dash or similar punctuation
    pattern = r"\s*[-–—]\s*.*"
    # Use regex to trim the extra part of the job title
    normalized_title = re.sub(pattern, '', job_title)
    return normalized_title
