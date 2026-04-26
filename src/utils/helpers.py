from pathlib import Path


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def safe_divide(numerator, denominator, default=0.0):
    try:
        denominator = float(denominator)
        if denominator == 0:
            return default
        return float(numerator) / denominator
    except (TypeError, ValueError, ZeroDivisionError):
        return default


def normalize_packet_type(value):
    mapping = {
        10: "OFPT_PACKET_IN",
        "10": "OFPT_PACKET_IN",
        13: "OFPT_PACKET_OUT",
        "13": "OFPT_PACKET_OUT",
        18: "OFPT_MULTIPART_REQUEST",
        "18": "OFPT_MULTIPART_REQUEST",
        19: "OFPT_MULTIPART_REPLY",
        "19": "OFPT_MULTIPART_REPLY",
    }
    return mapping.get(value, str(value))
