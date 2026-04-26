import argparse
import csv
import pyshark


def get_field(layer, name, default=None):
    try:
        return getattr(layer, name)
    except Exception:
        return default


def extract_openflow_features(pcap_file, output_csv):
    cap = pyshark.FileCapture(pcap_file, keep_packets=False)
    rows = []
    for packet in cap:
        try:
            ip_layer = getattr(packet, "ip", None)
            of_layer = getattr(packet, "OPENFLOW_V4", None)
            tcp_layer = getattr(packet, "tcp", None)
            ip_basic = getattr(packet, "IP", None)
            rows.append([
                get_field(ip_layer, "src") if ip_layer else None,
                get_field(ip_layer, "dst") if ip_layer else None,
                get_field(of_layer, "type") if of_layer else None,
                get_field(of_layer, "type") if of_layer else None,
                get_field(of_layer, "stat_type") if of_layer else None,
                get_field(of_layer, "tcp_flags_reset") if of_layer else get_field(tcp_layer, "flags_reset"),
                get_field(of_layer, "flowmod_priority") if of_layer else None,
                get_field(of_layer, "flowmod_idle_timeout") if of_layer else None,
                get_field(of_layer, "flowmod_hard_timeout") if of_layer else None,
                get_field(of_layer, "ip_flags_mf") if of_layer else None,
                get_field(of_layer, "ip_fragment_count") if of_layer else None,
                get_field(of_layer, "tcp_analysis_out_of_order") if of_layer else None,
                get_field(ip_basic, "flags") if ip_basic else None,
                get_field(ip_basic, "flags_df") if ip_basic else None,
                get_field(tcp_layer, "flags") if tcp_layer else None,
                get_field(tcp_layer, "flags_reset") if tcp_layer else None,
                get_field(tcp_layer, "connection_rst") if tcp_layer else None,
            ])
        except Exception:
            continue
    cap.close()

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["src.ip", "dst.ip", "packet.type", "Packet_type_details", "Openflow_stat_details", "reset.flag", "flowmod.priority", "idle.timeout", "hard.timeout", "more.fragment", "ip.fragment.count", "tcp.analysis.out_of_order", "IP.flags", "dont.fragment", "TCP.flags", "TCP.flags.reset", "connection.reset"])
        writer.writerows(rows)
    print(f"Saved {len(rows)} packet rows to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Extract OpenFlow-related fields from PCAP/PCAPNG")
    parser.add_argument("pcap")
    parser.add_argument("-o", "--output", default="data/raw/openflow_features.csv")
    args = parser.parse_args()
    extract_openflow_features(args.pcap, args.output)


if __name__ == "__main__":
    main()
