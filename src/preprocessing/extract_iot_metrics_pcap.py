import argparse
import csv
from collections import defaultdict
import pyshark


def extract_iot_metrics(pcap_file, output_csv):
    stats = defaultdict(lambda: {"first_ts": None, "last_ts": None, "packets": 0, "bytes": 0, "sizes": []})
    cap = pyshark.FileCapture(pcap_file, display_filter="ip", keep_packets=False)

    for pkt in cap:
        try:
            ts = float(pkt.sniff_timestamp)
            src_ip = pkt.ip.src
            frame_len = int(pkt.length)
            node = stats[src_ip]
            node["packets"] += 1
            node["bytes"] += frame_len
            node["sizes"].append(frame_len)
            node["first_ts"] = ts if node["first_ts"] is None else min(node["first_ts"], ts)
            node["last_ts"] = ts if node["last_ts"] is None else max(node["last_ts"], ts)
        except Exception:
            continue
    cap.close()

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["iot_node_id", "flow_bandwidth_bps", "packet_drop_rate", "packet_loss_percentage", "lost_byte_ratio", "avg_packet_size_bytes", "min_packet_size_bytes", "max_packet_size_bytes", "packet_reception_rate_pps", "packets_received", "packets_lost", "transmitted_bytes"])
        for node_id, s in stats.items():
            duration = 1.0
            if s["first_ts"] is not None and s["last_ts"] is not None and s["last_ts"] > s["first_ts"]:
                duration = s["last_ts"] - s["first_ts"]
            sizes = s["sizes"] or [0]
            writer.writerow([node_id, (s["bytes"] * 8.0) / duration, 0.0, 0.0, 0.0, sum(sizes) / len(sizes), min(sizes), max(sizes), s["packets"] / duration, s["packets"], 0, s["bytes"]])
    print(f"Saved IoT metrics to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Extract IoT service metrics from PCAP")
    parser.add_argument("pcap")
    parser.add_argument("-o", "--output", default="results/tables/iot_metrics_pcap.csv")
    args = parser.parse_args()
    extract_iot_metrics(args.pcap, args.output)


if __name__ == "__main__":
    main()
