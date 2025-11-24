import requests
import urllib3
urllib3.disable_warnings()

# Security headers to check
headers_to_check = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-XSS-Protection"
]

# Ask user for file path
file_path = input("Enter the path of your subdomain list file: ")

# Load domains
with open(file_path, "r") as f:
    subdomains = [x.strip() for x in f.readlines()]

print("\n==============================")
print("   SECURITY HEADER SCANNER   ")
print("==============================\n")

for domain in subdomains:
    url = "https://" + domain
    print(f"\n🔍 Checking: {url}")
    print("------------------------------------")

    try:
        r = requests.get(url, timeout=7, verify=False)
        response_headers = r.headers

        for h in headers_to_check:
            if h in response_headers:
                print(f"🟢 {h}: FOUND")
            else:
                print(f"🔴 {h}: MISSING")

    except Exception as e:
        print(f"⚠️ Error: {e}")

