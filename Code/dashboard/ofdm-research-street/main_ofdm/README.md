# Wi-SUN OFDM Network Analysis
**Complete analysis of Wi-SUN network using OFDM modulation**

## 📂 Directory Structure

```
main_ofdm/
├── Locations/                      # Raw CSV data files
│   ├── Location1.csv
│   ├── Location2.csv
│   ├── ...
│   └── Location17.csv
├── wisun_website_output/           # Generated website & visualizations
│   ├── index.html                  # Interactive dashboard
│   ├── time_series_analysis.png
│   ├── env_corr_matrix.png
│   ├── link_reciprocity.png
│   ├── hopcount_rpl_rank.png
│   ├── humidity_vs_rsl.png
│   └── summary_statistics.csv
├── generate_website.py             # Website generator script
└── README.md                       # This file
```

## 📊 Dataset Overview

- **Total Locations**: 17 measurement points
- **Total Records**: 551 data points
- **Date Range**: 2025-11-21 (15:48 to 22:07)
- **Network Type**: Wi-SUN OFDM

## 🔬 Measured Parameters

| Field | Parameter | Unit | Description |
|-------|-----------|------|-------------|
| field1 | Temperature | °C | Ambient temperature at measurement location |
| field2 | Humidity | % | Relative humidity |
| field3 | DisconnectedTotal | - | Number of disconnected network nodes |
| field4 | RSL_in | dBm | Received Signal Level (incoming) |
| field5 | RSL_out | dBm | Received Signal Level (outgoing) |
| field6 | RPL_rank | - | Routing Protocol for Low-Power networks rank |
| field7 | Hopcount | - | Number of network hops to reach destination |
| field8 | ConnectedTotal | - | Number of connected network nodes |

## 🚀 Quick Start

### View the Website

**Option 1: Direct Open**
```bash
cd main_ofdm
xdg-open wisun_website_output/index.html
```

**Option 2: Local Server (Recommended)**
```bash
cd main_ofdm/wisun_website_output
python -m http.server 8000
# Open: http://localhost:8000
```

### Regenerate Website

If you update the CSV files in `Locations/` folder:

```bash
cd main_ofdm
python generate_website.py
```

The script will automatically:
- Load all Location*.csv files from the Locations/ folder
- Generate comprehensive analysis and visualizations
- Create interactive HTML dashboard
- Save everything to wisun_website_output/

## 📈 Analysis Features

### Interactive Dashboard (index.html)

**4 Main Tabs:**

1. **🏠 Overview**
   - 3D scatter plot (Temperature × Humidity × Signal Strength)
   - Correlation matrix heatmap
   - Interactive Plotly charts

2. **📈 Time Series**
   - All 7 parameters plotted over time
   - 17 locations with different colors
   - Zoom, pan, and hover features

3. **🔍 Analysis**
   - Link reciprocity (RSL_in vs RSL_out)
   - Signal strength symmetry analysis
   - Network performance metrics

4. **💡 Insights**
   - Download all visualizations
   - Summary statistics export
   - Key findings and observations

### Static Visualizations (PNG)

1. **time_series_analysis.png**
   - 7 subplots showing temporal evolution
   - Temperature, Humidity, RSL signals, RPL rank, Hopcount, Connectivity

2. **env_corr_matrix.png**
   - Correlation heatmap between all parameters
   - Identifies relationships between environmental and network metrics

3. **link_reciprocity.png**
   - 4 comprehensive signal strength analysis plots
   - RSL_in vs RSL_out scatter with perfect reciprocity line
   - Signal distribution histograms
   - Connectivity relationships

4. **hopcount_rpl_rank.png**
   - Network topology analysis
   - Hopcount distribution
   - RPL rank vs Hopcount scatter
   - Connectivity trends over time
   - Average RPL rank by location

5. **humidity_vs_rsl.png**
   - Environmental impact analysis
   - Temperature vs Humidity relationships
   - Environmental effects on signal strength
   - Temperature anomaly detection (>2σ)

### Summary Statistics (CSV)

Comprehensive statistical analysis including:
- Mean, median, standard deviation
- Min/max values
- Data completeness
- For all 8 measured parameters

## 🔧 Technical Details

### Data Collection
- **Source**: ThingSpeak IoT platform
- **Modulation**: OFDM (Orthogonal Frequency-Division Multiplexing)
- **Network Protocol**: Wi-SUN (Wireless Smart Utility Network)
- **Routing**: RPL (Routing Protocol for Low-Power networks)

### CSV File Format
```csv
created_at,entry_id,field1,field2,field3,field4,field5,field6,field7,field8
2025-11-21T15:48:38+00:00,1,25.3,58.2,0,-85.2,-70.1,1250,4,3.5
```

## 📋 Requirements

The generator script requires:
- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- plotly

Install with:
```bash
pip install pandas numpy matplotlib seaborn plotly
```

## 🎯 Use Cases

1. **Network Performance Monitoring**
   - Track signal strength trends
   - Identify connectivity issues
   - Analyze routing efficiency

2. **Environmental Impact Analysis**
   - Correlation between weather and network performance
   - Temperature/humidity effects on signal propagation
   - Anomaly detection

3. **Topology Optimization**
   - Identify optimal node placement
   - Analyze hopcount patterns
   - RPL rank distribution

4. **Research & Development**
   - OFDM vs FSK comparison
   - Wi-SUN protocol analysis
   - Smart grid applications

## 📊 Key Findings

### Signal Strength
- Average RSL_in: Varies by location
- Average RSL_out: Generally better than RSL_in
- Link reciprocity: Good symmetry observed

### Network Topology
- Hopcount: Typically 3-5 hops
- RPL Rank: Varies with network distance
- Connectivity: Generally stable with occasional drops

### Environmental Factors
- Temperature range: ~20-30°C
- Humidity range: ~50-75%
- Minimal correlation with signal strength (expected for OFDM)

## 🔄 Updates

To add new measurement data:
1. Export CSV from ThingSpeak
2. Save as `LocationX.csv` in `Locations/` folder
3. Run `python generate_website.py`
4. Refresh your browser

## 🤝 Comparison with FSK

This OFDM data can be compared with:
- `ESW_WiSun/` - FSK modulation data
- Different network characteristics
- Performance trade-offs

## 📄 License

Data collected for academic/research purposes.

## 📧 Contact

Part of the ESW (Embedded Systems Workshop) project.

---

**Last Updated**: December 2, 2025  
**Data Collection**: November 21, 2025  
**Total Analysis Duration**: ~6 hours of network monitoring
