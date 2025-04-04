def generate_emails(names, domain):
    """Generates a set of potential email addresses based on name patterns.

    Args:
        names (set): A set of tuples, where each tuple contains (first_name, last_name).
        domain (str): The domain name.

    Returns:
        set: A set of generated email addresses.
    """
    patterns = [
        "{first}.{last}", "{first}{last}", "{first}_{last}", 
        "{first}{l}", "{f}{last}", "{first}", "{last}.{first}"
    ]
    
    emails = []
    for first, last in names:
        first, last = first.lower(), last.lower()
        f, l = first[0], last[0]
        for pattern in patterns:
            emails.append(pattern.format(first=first, last=last, f=f, l=l) + f"@{domain}")

    return set(emails)
