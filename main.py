from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from pathlib import Path
import subprocess
import tempfile
from config import HEADERS, SITES
import requests
from datetime import datetime

print(r'''
 _    _                         _
| |  | |                       | |
| |  | |___  ___  __ _ _ __ ___| |__
| |  | / __|/ _ \/ _` | '__/ __| '_ \
| |__| \__ \  __/ (_| | | | (__| | | |
 \____/|___/\___|\__,_|_|  \___|_| |_| v1.0
                                        Made by Dulisor
''')

def save_results_to_file(username: str, results: list[tuple[str, str, str]], method: str):
    """Save search results to a text file."""
    filename = f"{username}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Username Search Results for: {username}\n")
        f.write(f"Search Method: {method}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        found_count = 0
        not_found_count = 0
        error_count = 0
        
        for site, status, url in results:
            if status == "Found":
                f.write(f"[+] {site:15} FOUND     | {url}\n")
                found_count += 1
            elif status == "Not Found":
                f.write(f"[-] {site:15} NOT FOUND | {url}\n")
                not_found_count += 1
            else:
                f.write(f"[?] {site:15} {status}\n")
                error_count += 1
        
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Summary: {found_count} found, {not_found_count} not found, {error_count} errors\n")
        f.write(f"Total sites checked: {len(results)}\n")
    
    print(f"\n[✓] Results saved to: {filename}")

def check_username(
    session: requests.Session, site_name: str, url_template: str, username: str
) -> tuple[str, str, str]:
    url = url_template.format(username)
    try:
        response = session.get(
            url, headers=HEADERS, timeout=8, allow_redirects=True
        )

        if response.status_code == 200:
            return site_name, "Found", url
        elif response.status_code == 404:
            return site_name, "Not Found", url
        else:
            return site_name, f"Error({response.status_code})", url
    except requests.RequestException:
        return site_name, "Error", url


def search_username(username: str) -> list[tuple[str, str, str]]:
    print(f"Searching for: {username}")
    print("-" * 55)

    results = []
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [
                executor.submit(check_username, session, name, url, username)
                for name, url in SITES.items()
            ]

            for future in as_completed(futures):
                site, status, url = future.result()
                results.append((site, status, url))

                if status == "Found":
                    print(f"[+] {site:12} User Found      | {url}")
                elif status == "Not Found":
                    print(f"[-] {site:12} User Not Found  | {url}")
                else:
                    print(f"[?] {site:12} {status}")

    # Save results to file
    save_results_to_file(username, results, "Built-in Site List")
    return results


def find_accounts(username: str) -> list[dict]:
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / f"{username}.csv"

        cmd = [
            "sherlock",
            username,
            "--csv",
            "--folderoutput",
            tmpdir,
            "--print-found",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Sherlock CLI error: {result.stderr or result.stdout}"
            )

        accounts = []
        if csv_path.exists():
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                accounts.extend(iter(reader))

        return accounts


def process_sherlock_results(username: str, results: list[dict]):
    """Process and save Sherlock results."""
    if results:
        # Convert results to the format expected by save_results_to_file
        formatted_results = []
        for site in results:
            name = site.get('name', 'Unknown')
            url = site.get('url_user', '')
            status = "Found" if url else "Not Found"
            formatted_results.append((name, status, url))
        
        save_results_to_file(username, formatted_results, "Sherlock")
        
        # Display results
        for site in results:
            name = site.get('name', 'Unknown')
            url = site.get('url_user', '')
            print(f"[+] {name:12} User Found      | {url}")
    else:
        print(f"No accounts found for {username} using Sherlock.")
        # Still save a file indicating no results
        with open(f"{username}.txt", 'w', encoding='utf-8') as f:
            f.write(f"Username Search Results for: {username}\n")
            f.write(f"Search Method: Sherlock\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"No accounts found for {username} using Sherlock.\n")
        print(f"\n[✓] Results saved to: {username}.txt")


def main():
    while True:
        username = input("Enter username to search: ").strip()
        if len(username) < 4:
            print("Username should be at least 4 characters long. Please try again.")
            continue
        elif len(username) > 15:
            print("Username should not exceed 15 characters. Please try again.")
            continue

        opt = input("Input 'S' for Sherlock or 'B' for Built-In Site list from the config.py file: ").strip().lower()

        if opt == "s":
            print(f"Searching for: {username}")
            print("-" * 55)
            try:
                results = find_accounts(username)
                process_sherlock_results(username, results)
            except RuntimeError as e:
                print(e)
        elif opt == "b":
            search_username(username)
        elif opt != "s" and opt != "b":
            print("Invalid option selected.")
            continue
        
        again = input("The program has ended. Press 'Y' if you want to run the program again: ").strip().lower()
        if again != "y":
            break

if __name__ == "__main__":
    main()