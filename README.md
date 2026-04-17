# 🔐 Laravel File-Manager Access Control List Checker & Exploit

**Automated tool for detecting access control misconfigurations in Laravel applications and execution**

---

## 🧠 Overview

Laravel ACL Checker & Exploit adalah tool untuk membantu mengidentifikasi potensi **access control vulnerabilities** pada aplikasi Laravel.

Tool ini dirancang untuk:
- Mendeteksi **misconfigured authorization**
- Mengidentifikasi endpoint yang tidak terlindungi
- Membantu proses **security assessment** secara cepat dan efisien
- Automatisasi Exploit

> ⚠️ Tool ini dibuat hanya untuk **educational purposes** dan **authorized security testing**

---

## 🎯 Features

- 🔍 Endpoint scanning
- ⚡ Multi-threaded scanning
- 🔐 Fokus pada **ACL & authorization issues**
- 🧪 Mass scanning

---

## 🛠️ Requirements

- Python 3.x
- requests
- tqdm

Install dependencies:
```bash
pip install -r requirements.txt
```
---
**MASS SCANNING MODE**
---
📌 Basic Command
```bash
$ python scan.py -l list.txt
```
⚡ Advanced Usage
```bash
$ python scan.py -l targets.txt -t 10
```
---
**AUTO EXPLOIT MODE**
---
📌 Usage
```bash
$ python exp.py
Target URL: https://example.com
Cookie Lengkap: Your_Cookie
Csrf Token: Your_Csrf
```


