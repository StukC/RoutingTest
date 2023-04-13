import subprocess
import re
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

# Replace these with your chosen target hostnames
targets = ['www.google.com', 'www.bbc.co.uk', 'www.baidu.com', 'www.uol.com.br', 'www.yandex.ru']

# Filename to store results
results_filename = 'ping_traceroute_results.json'

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

    # Run ping using the resolved IP address
    ping_output = subprocess.check_output(["ping", "-c", "120", ip_address], text=True)

    # Extract loss rate and RTTs from ping output
    loss_rate = float(re.findall(r"(\d+)% packet loss", ping_output)[0])
    min_rtt, max_rtt, avg_rtt = map(float, re.findall(r"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", ping_output)[0])

    # Store the ping result for this target
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if target not in results:
        results[target] = []
    results[target].append({"timestamp": timestamp, "loss_rate": loss_rate, "min_rtt": min_rtt, "max_rtt": max_rtt, "avg_rtt": avg_rtt})

    # Print the current result
    print(f"Ping result for {target} ({ip_address}) at {timestamp}:")
    print(f"Loss rate: {loss_rate}%")
    print(f"RTTs: Min: {min_rtt} ms, Max: {max_rtt} ms, Avg: {avg_rtt} ms")
    print()

# Save the results to file
with open(results_filename, 'w') as f:
    json.dump(results, f, indent=4)

# Function to classify the target based on loss rate
def classify_loss_rate(loss_rate):
    if loss_rate == 0:
        return "loss free"
    elif 0 < loss_rate < 5:
        return "minor losses"
    elif 5 <= loss_rate < 10:
        return "significant losses"
    else:
        return "major losses"

# Plotting
for target in targets:
    timestamps = [datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S") for r in results[target]]
    loss_rates = [r["loss_rate"] for r in results[target]]
    min_rtts = [r["min_rtt"] for r in results[target]]
    max_rtts = [r["max_rtt"] for r in results[target]]
    avg_rtts = [r["avg_rtt"] for r in results[target]]

    plt.figure(figsize=(12, 6))
    plt.subplot(211)
    plt.plot(timestamps, loss_rates, marker='o')
    plt.title(f"{target} - Loss Rate and RTTs")
    plt.ylabel("Loss Rate (%)")
    plt.xticks(rotation=45)
    plt.subplot(212)
    plt.plot(timestamps, min_rtts, marker='o', label="Min")
    plt.plot(timestamps, max_rtts, marker='o', label="Max")
    plt.plot(timestamps, avg_rtts, marker='o', label="Avg")
    plt.ylabel("RTT (ms)")
    plt.legend()

    # Add classification text to plot
    last_loss_rate = loss_rates[-1]
    plt.annotate(classify_loss_rate(last_loss_rate), xy=(1, last_loss_rate), xytext=(8, 0), textcoords=('offset points'), ha='left', va='center')

    # Save plot to file
    plot_filename = f"{target}_plot.png"
    plt.savefig(plot_filename, bbox_inches='tight')

    # Print confirmation
    print(f"Plot for {target} saved to {plot_filename}")
