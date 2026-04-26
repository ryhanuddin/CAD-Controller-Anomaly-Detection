import pandas as pd


def compute_fd_with_flow_surge(df, previous_flow=None, previous_packet_in=None):
    packet_counts = df["Packet_type_details"].value_counts() if "Packet_type_details" in df.columns else pd.Series(dtype=int)
    total_packet_in = packet_counts.get("OFPT_PACKET_IN", 0)
    total_packet_out = packet_counts.get("OFPT_PACKET_OUT", 0)

    fd = None
    fd_defined = False
    if total_packet_in and total_packet_out and total_packet_out <= total_packet_in and total_packet_in >= 5000:
        fd = (total_packet_in - total_packet_out) / total_packet_in
        fd_defined = True

    stat_counts = df["Openflow_stat_details"].value_counts() if "Openflow_stat_details" in df.columns else pd.Series(dtype=int)
    current_flow = stat_counts.get("OFPT_FLOW", 0)

    previous_flow = current_flow if previous_flow is None else previous_flow
    previous_packet_in = total_packet_in if previous_packet_in is None else previous_packet_in

    flow_spike = (current_flow - previous_flow) / max(previous_flow, 1)
    pin_spike = (total_packet_in - previous_packet_in) / max(previous_packet_in, 1)
    flow_surge_flag = int(flow_spike > 0.5 or pin_spike > 0.5)
    fd_warning = int(fd_defined and (fd > 0.85 or flow_surge_flag == 1))

    return {"flow_disparity": fd, "flow_surge_flag": flow_surge_flag, "fd_warning": fd_warning, "current_flow": current_flow, "current_packet_in": total_packet_in}
