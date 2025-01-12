import re
def remove_urls_line_by_line(text):
    # Define the URL patterns (standard and decomposed URLs)
    text = re.sub(r'Customer\s*Self\s*Service\s*Portal\.', '', text, flags=re.IGNORECASE)

    url_pattern = """
        http[s]?://[^\s\n]+ |                          # Match standard URLs
        (h\s*t\s*t\s*p\s*s?|h\s*t\s*t\s*p)\s*:\s*/\s*/[\w\s\./-]+  # Match decomposed URLs
    """
    # Split the text by '\n'
    lines = text.split('\n')
    # Process each line to remove URLs
    cleaned_lines = [re.sub(url_pattern, '', line, flags=re.VERBOSE).strip() for line in lines]
    # Join the cleaned lines back with '\n'
    return '\n'.join(cleaned_lines)