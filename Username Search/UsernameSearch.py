import requests
from bs4 import BeautifulSoup
import threading
import concurrent.futures
import os
import pyfiglet
from colorama import Fore, init


ascii_banner = pyfiglet.figlet_format("Username Search - Made By Exploits")
print(ascii_banner)


init()
g = Fore.GREEN
r = Fore.RED
w = Fore.RESET


print_lock = threading.Lock()


def google_dork_search(query):

    """Perform a Google dork search and return search results."""

    url = f"https://www.google.com/search?q={query}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    response = requests.get(url, headers=headers)


    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        results = []

        for g in soup.find_all('div', class_='BVG0Nb'):

            link = g.find('a')

            if link and 'href' in link.attrs:

                results.append(link['href'])

        return results


    else:

        print("Error:", response.status_code)

        return []


def check_username_existence(target, url):

    """Check if the username exists on the given URL."""

    try:

        response = requests.get(url)

        if response.status_code == 200:

            if target in response.text:

                return True

        return False

    except Exception as e:

        print(f"Error accessing {url}: {e}")

        return False


def username_lookup(target):

    """Check various social media platforms for the given username."""

    websites = [

        f"https://www.youtube.com/@{target}",

        f"https://www.tiktok.com/@{target}",

        f"https://www.instagram.com/{target}/",

        f"https://www.github.com/{target}",

        f"https://soundcloud.com/{target}",

        f"https://linktr.ee/{target}",

        f"https://pastebin.com/u/{target}",

        f"https://doxbin.com/user/{target}",

        f"https://www.snapchat.com/add/{target}",

        f"https://www.facebook.com/{target}/",

        f"https://steamcommunity.com/id/{target}",

        f"https://x.com/{target}",

    ]



    results_found = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:

        future_to_url = {executor.submit(check_username_existence, target, url): url for url in websites}

        for future in concurrent.futures.as_completed(future_to_url):

            url = future_to_url[future]

            if future.result():  # If the username exists

                with print_lock:

                    print(f"{g}Valid username for: {url}{w}")

                    results_found.append(url)

            else:

                with print_lock:

                    print(f"{r}Invalid username for: {url}{w}")


    if results_found:

        folder_name = "Doxed"

        os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist

        file_path = os.path.join(folder_name, f"{target}.txt")


        with open(file_path, 'w') as file:

            for result in results_found:

                file.write(result + '\n')


        print(f"{g}Results saved to {file_path}{w}\n")

    else:

        print(f"{r}No results found.{w}")


if __name__ == "__main__":

    while True:

        print("\nSelect an option:")

        print("1. Google Dork Search")

        print("2. Username Lookup")

        print("3. Exit")


        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':

            query = input("Enter your Google dork query: ")

            results = google_dork_search(query)

            if results:

                print("\nGoogle Dork Results:")

                for result in results:

                    print(result)

            else:

                print(f"{r}No results found.{w}")


        elif choice == '2':

            target = input("Enter a username to look up: ")

            username_lookup(target)


        elif choice == '3':

            print("Exiting...")

            break


        else:

            print(f"{r}Invalid choice. Please try again.{w}")
