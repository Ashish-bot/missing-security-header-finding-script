import requests
import urllib3
import socket
import time

urllib3.disable_warnings()

headers_to_check = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-XSS-Protection"
]

file_path = input("Enter the path of your subdomain list file: ")

with open(file_path, "r") as f:
    subdomains = [x.strip() for x in f.readlines()]

print("\n==============================")
print("   SECURITY HEADER SCANNER v2 ")
print("==============================\n")

results = []

def domain_exists(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False

def fetch(url):
    for attempt in range(3):
        try:
            return requests.get(url, timeout=7, verify=False)
        except:
            time.sleep(2)
    return None

for domain in subdomains:

    print(f"\n🔍 Checking: https://{domain}")
    print("------------------------------------")
    results.append(f"\n🔍 Checking: https://{domain}\n------------------------------------")

    if not domain_exists(domain):
        msg = f"⚠️ DNS ERROR: {domain} does not resolve"
        print(msg)
        results.append(msg)
        continue

    r = fetch("https://" + domain)

    if r is None:
        print("⚠️ HTTPS failed. Trying HTTP...")
        r = fetch("http://" + domain)

    if r is None:
        msg = f"❌ Unreachable: Both HTTPS and HTTP failed"
        print(msg)
        results.append(msg)
        continue

    response_headers = r.headers

    for h in headers_to_check:
        if h in response_headers:
            line = f"🟢 {h}: FOUND"
        else:
            line = f"🔴 {h}: MISSING"

        print(line)
        results.append(line)

output_name = input("\nEnter output file name (result.txt): ")

with open(output_name, "w") as f:
    for line in results:
        f.write(line + "\n")

print(f"\n📁 Results saved in: {output_name}")
