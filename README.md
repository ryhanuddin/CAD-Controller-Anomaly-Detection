# CAD Controller Anomaly Detection

This repository contains the Controller Anomaly Detection (CAD) workflow for detecting controller-state degradation and SDN architectural bottlenecks. CAD is different from traffic-only detection because it uses controller-side OpenFlow behavior such as Packet-In/Packet-Out imbalance, flow-rule pressure, reset behavior, multipart messages, and timeout irregularity.

## Main Features

| Feature | Meaning |
|---|---|
| PPR | Packet-In / Packet-Out Ratio |
| FD | Flow Disparity between incoming requests and controller responses |
| MRR | Message Request Ratio using OpenFlow statistics patterns |
| CRF | Cumulative Reset Flags |
| PFSI | Priority Frequency Spike Index |
| TFSI | Timeout Frequency Spike Index |
| MMR | Multipart Message Ratio |
| ITD | Idle Timeout Disparity |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For PyShark scripts, install Wireshark/TShark first and make sure `tshark` is available from the terminal.

## Train CAD Models

```bash
python src/models/train_cad_models.py --data data/processed/controller_identification_dataset_extended.csv
```

## Extract OpenFlow Features from PCAP

```bash
python src/preprocessing/pyshark_openflow_extraction.py input.pcapng -o data/raw/openflow_features.csv
python src/preprocessing/build_cad_dataset.py data/raw/openflow_features.csv -o data/processed/cad_features.csv
```

## Extract IoT Service Metrics from PCAP

```bash
python src/preprocessing/extract_iot_metrics_pcap.py input.pcapng -o results/tables/iot_metrics_pcap.csv
```

## Run Ryu App

```bash
ryu-manager ryu_apps/cad_simple_switch_13.py
```

## Note

The processed dataset keeps the original column name `time_freaquency_spike_index` to remain compatible with the consolidated dataset.
