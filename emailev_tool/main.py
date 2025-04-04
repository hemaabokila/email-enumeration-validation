import argparse
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
import pyfiglet

from .email_generator import generate_emails
from .email_validator import check_email_smtp
from .hibp_checker import get_emails_hibp
from .reputation_checker import get_email_reputation
from .proxy_manager import load_proxies, get_random_proxy
from .tor_manager import renew_tor_ip, use_tor
from .utils import read_names_from_file, save_results
from .pyhunter_integration import find_emails_with_hunter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Advanced Email Enumeration & Validation Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("-n", "--names", required=True, help="File containing first and last names (one per line, space-separated)")
    parser.add_argument("-a", "--apikey", help="API Key for HaveIBeenPwned (optional)")
    parser.add_argument("--use-tor", action="store_true", help="Use Tor for anonymity")
    parser.add_argument("--tor-port", type=int, default=9050, help="Tor SOCKS port")
    parser.add_argument("--tor-control-port", type=int, default=9051, help="Tor Control port for IP renewal")
    parser.add_argument("--proxy-file", help="File containing list of HTTP/HTTPS proxies (one per line)")
    parser.add_argument("--apikey-pyhunter", help="API Key for pyhunter (optional)")
    parser.add_argument("--save", choices=["txt", "json", "csv"], help="Save results to file")
    banner = pyfiglet.figlet_format("EMAILEV")
    print(f"{Fore.BLUE}{banner}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Developed by: Ibrahem abo kila{Style.RESET_ALL}\n")
    return parser.parse_args()

def check_smtp_emails(generated_emails, proxy_list, use_tor):
    valid_emails_smtp = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_email_smtp, email, None if use_tor else get_random_proxy(proxy_list)): email for email in generated_emails}
        for future in as_completed(futures):
            email = futures[future]
            try:
                result = future.result()
                if result:
                    valid_emails_smtp.append(result)
            except Exception as e:
                logging.error(f"Error checking email {email} via SMTP: {e}")
    return valid_emails_smtp

async def check_async_tasks(tasks):
    results = []
    for task in asyncio.as_completed(tasks):
        try:
            results.append(await task)
        except Exception as e:
            logging.error(f"Async operation failed: {e}")
    return results

def main():
    args = parse_arguments()

    proxy_list = load_proxies(args.proxy_file) if args.proxy_file else []
    if proxy_list:
        logging.info(f"Loaded {len(proxy_list)} proxies from {args.proxy_file}.")
    
    if args.use_tor:
        use_tor(args.tor_port)
        logging.info("Using Tor for anonymous requests...")
        renew_tor_ip(args.tor_control_port)
    
    names_list = read_names_from_file(args.names)
    if not names_list:
        logging.error("No valid names found in the provided file!")
        return
    
    logging.info(f"Generating emails for domain: {args.domain}")
    generated_emails = generate_emails(names_list, args.domain)
    logging.info(f"Generated {len(generated_emails)} potential email addresses.")
    
    logging.info("Checking emails via SMTP...")
    valid_emails_smtp = check_smtp_emails(generated_emails, proxy_list, args.use_tor)
    logging.info(f"Found {len(valid_emails_smtp)} potentially valid emails via SMTP.")

    valid_emails = list(valid_emails_smtp)

    if args.apikey_pyhunter:
        logging.info("Searching for emails using pyhunter...")
        pyhunter_emails = find_emails_with_hunter(args.domain, args.apikey_pyhunter)
        if pyhunter_emails:
            valid_emails.extend(pyhunter_emails)
            valid_emails = sorted(set(valid_emails))

    if args.apikey:
        if valid_emails_smtp: 
            logging.info("Checking emails against HaveIBeenPwned...")
            hibp_tasks = [get_emails_hibp(args.apikey, email, get_random_proxy(proxy_list) if not args.use_tor else f"socks5://127.0.0.1:{args.tor_port}") for email in valid_emails_smtp]
            hibp_results = asyncio.run(check_async_tasks(hibp_tasks))
            valid_emails.extend(filter(None, hibp_results))
            valid_emails = sorted(set(valid_emails))
        else:
            logging.warning("Skipping HIBP check as no valid emails were found via SMTP.")

    logging.info("Checking email reputation...")
    if valid_emails_smtp:
        reputation_tasks = [get_email_reputation(email, get_random_proxy(proxy_list) if not args.use_tor else f"socks5://127.0.0.1:{args.tor_port}") for email in valid_emails_smtp]
        reputation_results = asyncio.run(check_async_tasks(reputation_tasks))
        valid_emails.extend(filter(None, reputation_results))
        valid_emails = sorted(set(valid_emails))
    else:
        logging.warning("Skipping reputation check as no valid emails were found.")


    print("\nValid Emails:")
    for email in valid_emails:
        print(email)

    if args.save:
        save_results(valid_emails, args.save)

if __name__ == "__main__":
    main()
