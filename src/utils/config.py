from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results"
MODEL_DIR = RESULTS_DIR / "model_outputs"
TABLE_DIR = RESULTS_DIR / "tables"
FIGURE_DIR = RESULTS_DIR / "figures"

TARGET_COLUMN = "compromised_controller_state"
DEFAULT_DATASET = DATA_DIR / "processed" / "controller_identification_dataset_extended.csv"

FEATURE_COLUMNS = [
    "packetIN_packetOUT_ratio",
    "message_Request_ratio",
    "cumulative_Reset_Flags",
    "flow_disparity",
    "priority_frequency_spike_index",
    "time_freaquency_spike_index",
    "multipart_message_ratio",
    "idle_timeout_disparity",
]
