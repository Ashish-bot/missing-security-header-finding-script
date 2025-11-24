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

results = []  # store everything

for domain in subdomains:
    url = "https://" + domain
    output_block = f"\n🔍 Checking: {url}\n------------------------------------"
    print(output_block)
    results.append(output_block)

    try:
        r = requests.get(url, timeout=7, verify=False)
        response_headers = r.headers

        for h in headers_to_check:
            if h in response_headers:
                line = f"🟢 {h}: FOUND"
            else:
                line = f"🔴 {h}: MISSING"

            print(line)
            results.append(line)

    except Exception as e:
        error_line = f"⚠️ Error: {e}"
        print(error_line)
        results.append(error_line)

# Ask user for output file name
output_name = input("\nEnter output file name (example: result.txt): ")

# Save results
with open(output_name, "w") as f:
    for line in results:
        f.write(line + "\n")

print(f"\n📁 Results saved successfully in: {output_name}")
