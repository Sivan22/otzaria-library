import re

def adjust_html_tag_spaces(html):
    # Move spaces from inside the closing tag to after the tag
    html = re.sub(r'([ ]+)(</[^<>]+?>)', r'\2\1', html)

    # Move spaces from the beginning of tags to before the tags
    html = re.sub(r'(<[^/<>]+?>)([ ]+)', r'\2\1', html)
    # Clean up any double spaces created by the previous step
    html = re.sub(r'[ ]{2,}', ' ', html)

    return html

# Example usage
html_content = " <div><p> Some content </p></ div> <p> Another paragraph </ p> "
adjusted_html = adjust_html_tag_spaces(html_content)
print(adjusted_html)
