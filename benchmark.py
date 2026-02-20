import os
import csv
import matplotlib.pyplot as plt

def generate_report_files(timestamps, latencies, fps_list):
    if not timestamps:
        print("⚠️ No data to generate a report.")
        return

    # Automatically create the 'result' folder if it doesn't exist
    output_dir = 'result'
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, 'results.csv')
    png_path = os.path.join(output_dir, 'benchmark_charts.png')

    # 1. Export Data to CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time (s)', 'Latency (ms)', 'FPS'])
        for t, l, f_val in zip(timestamps, latencies, fps_list):
            writer.writerow([t, l, f_val])

    # 2. Generate the Charts
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Top plot: FPS Line Chart
    ax1.plot(timestamps, fps_list, color='blue', label='FPS')
    ax1.axhline(y=15, color='red', linestyle='--', label='Target 15 FPS')
    ax1.set_title('Real-Time Frame Rate over Session')
    ax1.set_ylabel('FPS')
    ax1.set_xlabel('Time (s)')
    ax1.legend()

    # Bottom plot: Latency Histogram
    ax2.hist(latencies, bins=20, color='orange', edgecolor='black')
    ax2.axvline(x=200, color='red', linestyle='--', label='Target <200ms Latency')
    ax2.set_title('End-to-End Latency Distribution')
    ax2.set_xlabel('Latency (ms)')
    ax2.set_ylabel('Frame Count')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(png_path)
    
    # Free memory
    plt.close(fig)
    
    print(f"\n📁 Report files successfully saved to the '{output_dir}' folder!")
    print(f"   - {csv_path}")
    print(f"   - {png_path}")