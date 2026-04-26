import numpy as np
import pandas as pd


def safe_divide(numerator, denominator, default=0.0):
    if denominator in [0, None] or pd.isna(denominator):
        return default
    return numerator / denominator


def _count_packet(df, label):
    if "Packet_type_details" in df.columns:
        return (df["Packet_type_details"] == label).sum()
    if "packet.type" in df.columns:
        code = 10 if label == "OFPT_PACKET_IN" else 13 if label == "OFPT_PACKET_OUT" else None
        return (df["packet.type"].astype(str) == str(code)).sum()
    return 0


def compute_ppr(df):
    packet_in = _count_packet(df, "OFPT_PACKET_IN")
    packet_out = _count_packet(df, "OFPT_PACKET_OUT")
    return safe_divide(packet_in, packet_out), packet_in, packet_out


def compute_fd(packet_in, packet_out, min_packet_in=5000):
    if packet_in == 0 or packet_out == 0:
        return np.nan
    if packet_out > packet_in or packet_in < min_packet_in:
        return np.nan
    return (packet_in - packet_out) / packet_in


def compute_mrr(df):
    if "Openflow_stat_details" not in df.columns:
        return 0
    counts = df["Openflow_stat_details"].value_counts()
    queue_table_ratio = safe_divide(counts.get("OFPST_QUEUE", 0), counts.get("OFPT_TABLE", 1))
    flow_port_ratio = safe_divide(counts.get("OFPT_FLOW", 0), counts.get("OFPT_PORT", 1))
    return 0 if 0.5 < queue_table_ratio < 1.5 and 0.5 < flow_port_ratio < 1.5 else 1


def compute_crf(df):
    if "reset.flag" not in df.columns:
        return 0
    reset_series = pd.to_numeric(df["reset.flag"], errors="coerce").fillna(0)
    total_reset_flags = int((reset_series == 1).sum())
    packet_in = _count_packet(df, "OFPT_PACKET_IN")

    consecutive_count = 0
    for value in reset_series:
        if value == 1:
            consecutive_count += 1
            if consecutive_count >= 100:
                return 1
        else:
            consecutive_count = 0

    if packet_in > 5000 and total_reset_flags > packet_in * 0.10:
        return 1
    return 0


def compute_frequency_spike(df, column):
    if column not in df.columns:
        return 0
    values = df[column].dropna()
    if values.empty:
        return 0
    counts = values.value_counts()
    mean_count = counts.mean()
    return max(counts.max() - mean_count, mean_count - counts.min())


def compute_mmr(df):
    if "Packet_type_details" not in df.columns:
        return 0
    reply_count = (df["Packet_type_details"] == "OFPT_MULTIPART_REPLY").sum()
    request_count = (df["Packet_type_details"] == "OFPT_MULTIPART_REQUEST").sum()
    return safe_divide(reply_count, request_count)


def compute_itd(df):
    if "idle.timeout" not in df.columns:
        return 0
    idle = pd.to_numeric(df["idle.timeout"], errors="coerce").fillna(0)
    std_deviation = idle.std()
    counts = idle.value_counts()
    high_repetition = any(count > 10000 for value, count in counts.items() if value != 0)
    return 1 if high_repetition and std_deviation < 100 else 0


def extract_window_features(df):
    ppr, packet_in, packet_out = compute_ppr(df)
    fd = compute_fd(packet_in, packet_out)
    return {
        "packetIN_packetOUT_ratio": ppr,
        "message_Request_ratio": compute_mrr(df),
        "cumulative_Reset_Flags": compute_crf(df),
        "flow_disparity": fd,
        "priority_frequency_spike_index": compute_frequency_spike(df, "flowmod.priority"),
        "time_freaquency_spike_index": compute_frequency_spike(df, "hard.timeout"),
        "multipart_message_ratio": compute_mmr(df),
        "idle_timeout_disparity": compute_itd(df),
    }
