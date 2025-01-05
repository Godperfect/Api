import re

def sanitize_title(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)