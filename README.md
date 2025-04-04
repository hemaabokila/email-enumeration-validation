# Advanced Email Enumeration & Validation Tool

![EnumURL](https://img.shields.io/badge/Email%20Enumeration-Advanced-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)

This is an advanced tool for email enumeration and validation, designed to help you identify potentially valid email addresses from a given domain. It uses various techniques, including generating email patterns, checking SMTP validity, verifying reputation, and cross-referencing with services like **Have I Been Pwned** and **PyHunter**.

## Features:
- **Email Generation**: Generates potential email addresses based on common naming patterns.
- **SMTP Validation**: Checks if the generated email addresses are valid via SMTP.
- **HaveIBeenPwned Integration**: Checks if the email has been compromised in any known data breaches using the HaveIBeenPwned API.
- **Email Reputation Check**: Validates the reputation of the email addresses to identify potentially risky ones.
- **Tor Integration**: Supports anonymous requests via Tor to ensure privacy.
- **Proxy Support**: Allows you to use a list of proxies for the email validation process.
- **API Integrations**: Supports integration with services like PyHunter for email discovery.

## Installation

### Clone the repository:

```bash
git clone https://github.com/hemaabokila/email-enumeration-validation.git
cd email-enumeration-validation
pip install .
```
### You can install the tool using pip:

```bash
sudo install emailev
```
## Usage
You can run the tool via the command line interface. Below are the available options:

```bash
usage: email [-h] -d DOMAIN -n NAMES
             [-a APIKEY] [--use-tor]
             [--tor-port TOR_PORT]
             [--tor-control-port TOR_CONTROL_PORT]
             [--proxy-file PROXY_FILE]
             [--apikey-pyhunter APIKEY_PYHUNTER]
             [--save {txt,json,csv}]
```
## Options:

`-h, --help`

Show this help message and exit.

`-d DOMAIN, --domain DOMAIN`

Target domain (e.g., example.com). This option is required.

`-n NAMES, --names NAMES`

File containing first and last names (one per line, space-separated). This option is required.

`-a APIKEY, --apikey APIKEY`

API Key for HaveIBeenPwned (optional). If you want to check email addresses against the HaveIBeenPwned database, you need to provide this API key.

`--use-tor`

Use Tor for anonymity. This will route your requests through the Tor network to ensure privacy.

`--tor-port TOR_PORT`

Tor SOCKS port (default: 9050). This is the port used to connect to the Tor network.

`--tor-control-port TOR_CONTROL_PORT`

Tor Control port for IP renewal (default: 9051). This allows you to request a new IP address from the Tor network.

`--proxy-file PROXY_FILE`

File containing a list of HTTP/HTTPS proxies (one per line). This will be used to route requests via the specified proxies.

`--apikey-pyhunter APIKEY_PYHUNTER`

API Key for PyHunter (optional). If you want to search for emails using the PyHunter service, you need to provide this API key.

`--save {txt,json,csv}`

Save results to file in the specified format (txt, json, or csv). If you choose to save the results, they will be written to the corresponding file format.

## Example Usage
### Basic usage with a domain and names file:
```bash
email -d example.com -n names.txt
```
### Using Tor for anonymity:
```bash
email -d example.com -n names.txt --use-tor
```
### Using proxies from a file:
```bash
email -d example.com -n names.txt --proxy-file proxies.txt
```
### Using HaveIBeenPwned API for data breach checks:
```bash
email -d example.com -n names.txt -a YOUR_HIBP_API_KEY
```
### Saving results to a CSV file:
```bash
email -d example.com -n names.txt --save csv
```
## 🔧 Requirements
- Python 3.7+
- `socks`, `requests`, `aiohttp`, `pyhunter`, `stem`

## 📜 License
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
This project is open-source and licensed under the **MIT License**.

## 🤝 Contributing
Contributions are welcome! Feel free to open a **Pull Request** to enhance the tool.

## 📬 Contact
📧 For inquiries and support: [LinkedIn](https://www.linkedin.com/in/ibrahem-abo-kila)

