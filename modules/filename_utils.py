import re


def jd_number(filename):
    """Extract JD number from filenames like jd_1.pdf, jd1.pdf, jd_2 (1).pdf."""
    match = re.search(r"jd[_\s-]*(\d+)", filename.lower())
    return int(match.group(1)) if match else None
