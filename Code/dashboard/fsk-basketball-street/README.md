# 📡 Wi-SUN FSK Network Analysis Dashboard

> **Basketball Court Street - RF propagation study along IIITH Campus Road**

![Wi-SUN](https://img.shields.io/badge/Wi--SUN-FSK-00f5ff?style=for-the-badge)
![Locations](https://img.shields.io/badge/Nodes-8-ff00ff?style=for-the-badge)
![Data Points](https://img.shields.io/badge/Samples-269-00ff88?style=for-the-badge)

## 🎯 Project Overview

This dashboard visualizes RF signal propagation characteristics of a **Wi-SUN FSK (Frequency Shift Keying)** network deployed for smart grid/IoT applications. Data was collected from **8 measurement points** spaced 10m apart along the IIITH campus road.

## 📊 Key Metrics Analyzed

| Metric | Description | Range Observed | Definition |
|--------|-------------|----------------|------------|
| **RSSI** | Received Signal Strength Indicator | -75 to -95 dBm | A measure of the power present in a received radio signal. Higher (less negative) values indicate stronger signals. |
| **SNR** | Signal-to-Noise Ratio | 2.4 to 8.9 dB | The ratio of signal power to noise power. A higher SNR indicates a cleaner signal. |
| **PER** | Packet Error Rate | 9.7% to 28.6% | The percentage of data packets lost or corrupted during transmission. Lower PER indicates better reliability. |
| **Coverage Probability** | % samples above -90dBm threshold | 37% to 100% | The likelihood that a receiver will successfully decode a signal at a given location. |
| **Fade Margin** | Buffer above receiver sensitivity | 9.0 to 21.3 dB | The additional signal strength available beyond what is minimally required for acceptable communication. Provides a buffer against signal fading. |
| **Jitter** | Signal stability (std deviation) | 1.0 to 2.28 dB | The variation in signal characteristics over time, indicating instability. Lower jitter implies a more stable signal. |

## ⚙️ Calculation and Interpretation of Metrics

### **RSSI (Received Signal Strength Indicator)**
- **Calculation**: Direct measurement from radio hardware. Typically in dBm (decibel-milliwatts).
- **Ranges/Ratios**: Values closer to 0 dBm (e.g., -50 dBm) indicate a very strong signal. More negative values (e.g., -90 dBm) indicate a weaker signal. A general threshold for reliable communication is often around -85 dBm to -90 dBm.

### **SNR (Signal-to-Noise Ratio)**
- **Calculation**: SNR = RSSI - NoiseFloor (where Noise Floor is the power of background noise).
- **Ranges/Ratios**: A higher SNR (e.g., > 10 dB) means the signal is significantly stronger than the noise, leading to better data integrity. Low SNR (< 5 dB) suggests a noisy environment where packet errors are more likely.

### **PER (Packet Error Rate)**
- **Calculation**: PER = (Number of Lost Packets / Total Packets Sent) * 100%.
- **Ranges/Ratios**: A PER of 0% is ideal. Values below 10-15% are generally considered acceptable for many applications, while higher percentages (e.g., > 20%) indicate significant packet loss and unreliable communication.

### **Coverage Probability**
- **Calculation**: Coverage Probability = (Number of Packets with RSSI > Threshold / Total Packets) * 100%.
- **Ranges/Ratios**: This indicates the percentage of time a device can establish a usable link. 100% means full coverage, while lower percentages (e.g., < 50%) indicate intermittent or unreliable connectivity, suggesting a coverage hole or edge-of-range scenario.

### **Fade Margin**
- **Calculation**: Fade Margin = RSSI_actual - RSSI_sensitivity (where RSSI_sensitivity is the minimum signal required for reception).
- **Ranges/Ratios**: A positive fade margin is crucial, providing a buffer against temporary signal drops (fades). A higher fade margin (e.g., > 15 dB) is desirable, indicating robustness. A low or negative fade margin means the link is fragile and susceptible to outages.

### **Jitter**
- **Calculation**: Standard deviation of successive RSSI or latency measurements.
- **Ranges/Ratios**: Lower jitter values indicate a more stable signal and consistent network performance. High jitter suggests signal fluctuations, which can lead to unpredictable behavior and increased packet errors.

## 🔬 Key Findings

1. **Effective Range**: ~70-80m before signal degradation becomes critical
2. **Best Node**: Location 4 (lowest PER at 9.7%, strong RSSI)
3. **Edge Nodes**: Locations 7 & 8 show Grade D performance with reduced coverage
4. **NLOS Impact**: Locations 9-17 experienced complete signal loss due to tree/building obstructions

## 📈 Visualizations Included

- 🌊 **RSSI Signal Propagation Map** - Signal decay with min/max envelope
- 🏆 **Link Quality Grades** - A/B/C/D classification per location
- 📉 **Signal Decay Curve** - Distance vs RSSI with coverage-sized markers
- ⚠️ **Packet Error Rate** - Color-coded reliability analysis
- 🎯 **Coverage Probability** - Threshold-based connectivity assessment
- 📊 **SNR Distribution** - Noise floor analysis
- 🕸️ **Multi-Metric Radar** - Comparative location analysis
- 〰️ **Signal Jitter** - Stability over time
- 🛡️ **Fade Margin Analysis** - Link budget with triple-axis view

## 🚀 Quick Start

```bash
# Local preview
cd Dashboard
python3 -m http.server 8080
# Open http://localhost:8080
```

## 📁 Data Source

- **Files**: `Location1.csv` through `Location 8.csv`
- **Columns**: timestamp, temp, humidity, RSSI, SNR, packet_counter, link_quality, distance
- **Collection**: Street-level measurements, ~30 samples per location

## 🛠️ Tech Stack

- **Plotly.js** - Interactive charts
- **Google Fonts** - Orbitron & Rajdhani
- **Pure HTML/CSS/JS** - No build step required

---

<p align="center">
  <b>IIITH Research Project</b><br>
  Wi-SUN FSK Network Performance Analysis
</p>