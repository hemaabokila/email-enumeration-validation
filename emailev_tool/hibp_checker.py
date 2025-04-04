import aiohttp
import asyncio
import logging

async def fetch_with_proxy(session, url, headers=None, proxy=None, retries=3, delay=1):
    """Fetches a URL using a proxy with retry logic.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        url (str): The URL to fetch.
        headers (dict, optional): Request headers. Defaults to None.
        proxy (str, optional): The proxy URL. Defaults to None.
        retries (int): Number of retries on failure.
        delay (int): Delay in seconds between retries.

    Returns:
        str or None: The response text on success, None on failure.
    """
    for attempt in range(retries):
        try:
            async with session.get(url, headers=headers, proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 404:
                    return None
                else:
                    logging.warning(f"Unexpected status {response.status} while fetching {url}.")
        except aiohttp.ClientError as e:
            logging.warning(f"Attempt {attempt + 1} failed to fetch {url} with error: {e}")
        except asyncio.TimeoutError:
            logging.warning(f"Attempt {attempt + 1} to fetch {url} timed out.")

        if attempt < retries - 1:
            await asyncio.sleep(delay)
            delay *= 2

    logging.error(f"Failed to fetch {url} after {retries} retries.")
    return None

async def get_emails_hibp(api_key, email, proxy=None):
    """Checks if an email address has been pwned using the HaveIBeenPwned API.

    Args:
        api_key (str): The API key for HaveIBeenPwned.
        email (str): The email address to check.
        proxy (str, optional): The proxy URL to use. Defaults to None.

    Returns:
        str or None: The email address if found in a breach, otherwise None.
    """
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "EmailEnumTool"
    }
    
    async with aiohttp.ClientSession() as session:
        response_text = await fetch_with_proxy(session, url, headers=headers, proxy=proxy)
        if response_text:
            logging.info(f"Email {email} found in HaveIBeenPwned breaches.")
            return email
        return None
