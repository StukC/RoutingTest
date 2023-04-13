import subprocess

# List of target hostnames
hosts = [
    "www.google.com",
    "www.bbc.co.uk.com",
    "www.baidu.com",
    "www.uol.com.br",
    "www.yandex.ru"
]

# Function to get IP address from a hostname
def get_ip_address(host):
    command = f"dig +short {host}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8').strip()

# Function to perform traceroute using the IP address
def run_traceroute(ip):
    command = f"traceroute {ip}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8')

# Main code
if __name__ == "__main__":
    for host in hosts:
        print(f"Running traceroute for {host}...")
        ip = get_ip_address(host)
        if ip:
            print(f"IP address for {host} is {ip}")
            traceroute_result = run_traceroute(ip)
            print(traceroute_result)
            with open(f"traceroute_{ip}.txt", "w") as f:
                f.write(traceroute_result)
        else:
            print(f"Failed to resolve IP address for {host}")
