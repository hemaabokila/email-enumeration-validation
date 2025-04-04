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
        aiohttp.ClientResponse or None: The response object on success, None on failure after retries.
    """
    for attempt in range(retries):
        try:
            async with session.get(url, headers=headers, proxy=proxy, timeout=10) as response:
                return response
        except aiohttp.ClientError as e:
            logging.warning(f"Attempt {attempt + 1} failed to fetch {url} with error: {e}")
        except asyncio.TimeoutError:
            logging.warning(f"Attempt {attempt + 1} to fetch {url} timed out.")

        if attempt < retries - 1:
            await asyncio.sleep(delay)
            delay *= 2

    logging.error(f"Failed to fetch {url} after {retries} retries.")
    return None

async def get_email_reputation(email, proxy=None):
    """Gets the reputation of an email address using the emailrep.io API.

    Args:
        email (str): The email address to check.
        proxy (str, optional): The proxy URL to use. Defaults to None.

    Returns:
        str or None: The email address if a successful response is received, otherwise None.
    """
    url = f"https://emailrep.io/{email}"
    async with aiohttp.ClientSession() as session:
        response = await fetch_with_proxy(session, url, proxy=proxy)
        if response and response.status == 200:
            logging.info(f"Successfully retrieved reputation for {email}.")
            return email
        elif response:
            logging.warning(f"emailrep.io API returned status {response.status} for {email}.")
        return None
