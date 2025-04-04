import random
import logging

def load_proxies(file_path):
    """Loads proxies from a file, ensuring no duplicates.

    Args:
        file_path (str): The path to the file containing proxies (one per line).

    Returns:
        list: A list of unique proxy URLs.
    """
    try:
        with open(file_path, "r") as file:
            proxies = {line.strip() for line in file if line.strip()}
        if not proxies:
            logging.warning(f"Proxy file {file_path} is empty.")
        return list(proxies)
    except FileNotFoundError:
        logging.warning(f"Proxy file not found at {file_path}. Not using proxies.")
        return []
    except Exception as e:
        logging.error(f"Error reading proxy file: {e}")
        return []

def get_random_proxy(proxy_list):
    """Returns a random proxy from the provided list.

    Args:
        proxy_list (list): A list of proxy URLs.

    Returns:
        str or None: A random proxy URL or None if the list is empty.
    """
    if not proxy_list:
        logging.warning("No proxies available, proceeding without proxy.")
        return None
    return random.choice(proxy_list)
