import smtplib
import socket
import logging
import socks
import dns.resolver
import time
from functools import wraps

def get_mx_record(domain):
    """Retrieves the first MX record of a domain."""
    try:
        records = dns.resolver.resolve(domain, "MX")
        return str(records[0].exchange)
    except Exception:
        return None

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function if it fails, with a delay between attempts."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, socket.timeout) as e:
                    logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_failure(retries=3, delay=3)
def check_email_smtp(email, proxy=None):
    """Checks if an email address is likely valid using an SMTP connection with optional proxy support.

    Args:
        email (str): The email address to check.
        proxy (tuple, optional): (proxy_type, proxy_host, proxy_port). Defaults to None.

    Returns:
        str or None: The email address if SMTP check is successful, otherwise None.
    """
    domain = email.split('@')[-1]
    mx_host = get_mx_record(domain)
    
    if not mx_host:
        logging.debug(f"No MX record found for {domain}, skipping SMTP check for {email}")
        return None
    
    original_socket = socket.socket
    try:
        if proxy:
            proxy_type, proxy_host, proxy_port = proxy
            socks.setdefaultproxy(proxy_type, proxy_host, proxy_port)
            socket.socket = socks.socksocket 

        with smtplib.SMTP(mx_host, timeout=5) as server:
            server.set_debuglevel(0)
            server.helo()
            try:
                server.starttls()
            except smtplib.SMTPException:
                pass
            
            server.mail('test@example.com')
            code, _ = server.rcpt(email)
            if code == 250:
                logging.info(f"SMTP check successful for {email}")
                return email
            else:
                logging.debug(f"SMTP check failed for {email} with code: {code}")
                return None
    except Exception as e:
        logging.error(f"An error occurred while checking {email}: {e}")
    finally:
        socket.socket = original_socket
    
    return None
