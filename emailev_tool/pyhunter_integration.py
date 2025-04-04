from pyhunter import PyHunter
import logging

def find_emails_with_hunter(domain, api_key):
    """Finds email addresses associated with a domain using the pyhunter library.

    Args:
        domain (str): The domain name to search.
        api_key (str): The API key for pyhunter.

    Returns:
        list: A list of found email addresses, or an empty list if none are found.
    """
    try:
        hunter = PyHunter(api_key)
        results = hunter.domain_search(domain=domain)
        
        if not results or "emails" not in results:
            logging.info(f"No emails found for domain {domain} using pyhunter.")
            return []

        emails = [email['value'] for email in results.get('emails', []) if 'value' in email]
        logging.info(f"Found {len(emails)} emails for domain {domain} using pyhunter.")
        return emails

    except Exception as e:
        logging.error(f"Error using pyhunter for domain {domain}: {e}")
        return []

