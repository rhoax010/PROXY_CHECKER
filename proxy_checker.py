# ----------------------------------------
# 🔌 Free Public Proxy List Sources:
# ----------------------------------------
# https://free-proxy-list.net
# https://www.proxyscrape.com/free-proxy-list
# https://www.sslproxies.org
# https://spys.one/en/
# https://hidemy.name/en/proxy-list/
# https://openproxy.space/list/http
# https://proxylist.geonode.com/
# https://proxylist.download/
# https://raw.githubusercontent.com/TheSpeedX/PROXY-List/main/http.txt
# https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt
# ----------------------------------------

import sys
import time
import re

# --- Dependency check ---
missing = []
try:
    import requests
except ImportError:
    missing.append("requests")

try:
    from colorama import init, Fore
except ImportError:
    missing.append("colorama")

if missing:
    print("\n❌ Missing required modules:")
    for m in missing:
        print(f" - {m}")
    print("\n💡 Install them using:")
    print("   pip install " + " ".join(missing))
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

def get_public_ips(origin):
    """Filter out private IPs like 10.x.x.x, 192.168.x.x, etc."""
    ips = origin.split(",")
    public_ips = [ip.strip() for ip in ips if not re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1]))", ip.strip())]
    return ", ".join(public_ips) if public_ips else origin

def check_proxy(ip_port, protocol):
    ip_port = ip_port.strip()
    if not ip_port:
        return

    proxy = f"{protocol}://{ip_port}"
    proxies = {
        'http': proxy,
        'https': proxy
    }

    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if response.status_code == 200:
            origin_ip = response.json().get("origin", "")
            clean_ip = get_public_ips(origin_ip)
            print(Fore.GREEN + f"[LIVE] {proxy} ➜ {clean_ip}")
        else:
            print(Fore.RED + f"[DEAD] {proxy}")
    except:
        print(Fore.RED + f"[DEAD] {proxy}")

def main():
    file_path = input("Enter path to proxy list file (e.g., proxies.txt): ").strip()
    protocol = input("Enter proxy protocol (http, socks4, socks5): ").strip().lower()

    if protocol not in ['http', 'socks4', 'socks5']:
        print("❌ Invalid protocol! Please choose from http, socks4, or socks5.")
        return

    try:
        with open(file_path, "r") as f:
            proxy_list = f.readlines()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return

    print(f"\n🔎 Checking {len(proxy_list)} proxies using {protocol.upper()}...\n")

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(lambda p: check_proxy(p, protocol), proxy_list)

    print("\n✅ Check complete.")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\n⏱️ Finished in {round(time.time() - start, 2)} seconds.")
