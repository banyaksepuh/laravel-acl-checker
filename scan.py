#!/usr/bin/env python3
import requests
import warnings
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# --- SILENCE ---
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()

# Style Palette
GREEN, RED, YELLOW, CYAN, RESET, BOLD = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[0m', '\033[1m'

class InitializeScanner:
    def __init__(self):
        # Header MacBook Pro
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }
        # Endpoint Sakti
        self.endpoint = "/file-manager/initialize"

    def scan(self, url, pbar):
        # Cleaning URL input
        domain = url.strip().replace('http://', '').replace('https://', '').rstrip('/')
        protocols = ['https://', 'http://']
        
        for proto in protocols:
            target = f"{proto}{domain}{self.endpoint}"
            try:
                # allow_redirects=False kunci biar gak ketipu status 200 palsu
                r = requests.get(target, headers=self.headers, verify=False, timeout=10, allow_redirects=False)
                
                if r.status_code == 200:
                    # PERBAIKAN LOGIC:
                    # Normalisasi data mentah biar spasi/quote gak ngerusak deteksi
                    raw_data = r.text.lower().replace(" ", "").replace("'", '"')
                    
                    # Cukup cari acl:false sesuai instruksi lo
                    if '"acl":false' in raw_data:
                        pbar.write(f"{GREEN}{BOLD}[VULN] {target}{RESET}")
                        with open("pwn_acl_found.txt", "a") as f:
                            f.write(f"{target}\n")
                        return True
            except:
                continue
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Initialize ACL Scanner V2")
    parser.add_argument("-l", "--list", required=True, help="Path target list (.txt)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Jumlah thread")
    args = parser.parse_args()

    if not os.path.exists(args.list):
        print(f"{RED}[!] File list {args.list} kaga ada, Tan!{RESET}")
        return

    with open(args.list, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"\n{BOLD}{CYAN}[*] Initialize Scanner - One Line Logic V2{RESET}")
    print(f"{CYAN}[*] Target Domains : {len(urls)}")
    print(f"[*] Logic         : Looking for '\"acl\":false'{RESET}\n")

    scanner = InitializeScanner()

    # Progress bar rapih
    with tqdm(total=len(urls), desc="Hunting", unit="url", bar_format="{l_bar}{bar:30}{r_bar}") as pbar:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = [executor.submit(scanner.scan, url, pbar) for url in urls]
            for _ in as_completed(futures):
                pbar.update(1)

    print(f"\n{GREEN}{BOLD}[+] Scan Selesai!{RESET}")
    print(f"{GREEN}[+] Hasil Valid Disimpan di: pwn_acl_found.txt 🍦🚀{RESET}\n")

if __name__ == "__main__":
    main()
