import subprocess
import re
import os
import json
from datetime import datetime

# Replace these with your chosen target hostnames
targets = ['www.google.com', 'www.bbc.co.uk', 'www.baidu.com', 'www.uol.com.br', 'www.yandex.ru']

# Filename to store results
results_filename = 'traceroute_results.json'

# Load existing results from file or create an empty dictionary
if os.path.exists(results_filename):
    with open(results_filename, 'r') as f:
        results = json.load(f)
else:
    results = {}

for target in targets:
    # Get the IP address of the target
    ip_output = subprocess.check_output(["dig", "+short", target], text=True).strip()
    ip_address = ip_output.split("\n")[-1]  # Get the last resolved IP address

    # Run traceroute using the resolved IP address
    traceroute_output = subprocess.check_output(["traceroute", ip_address], text=True)

    # Process the output to match the desired format
    output_lines = traceroute_output.split("\n")
    processed_output = []
    for line in output_lines:
        line = re.sub(r'\s+', ' ', line).strip()  # Remove extra spaces
        if line:
            processed_output.append(line)

    # Store the traceroute result for this target
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if target not in results:
        results[target] = []
    results[target].append({"timestamp": timestamp, "result": processed_output})

    # Print the current result
    print(f"Traceroute result for {target} ({ip_address}) at {timestamp}:")
    print("\n".join(processed_output))
    print()

# Save the results to file
with open(results_filename, 'w') as f:
    json.dump(results, f, indent=4)
