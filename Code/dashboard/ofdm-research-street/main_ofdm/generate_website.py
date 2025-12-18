#!/usr/bin/env python3
"""
Wi-SUN Website Generator - Using Local CSV Files
=================================================
Generates a comprehensive website similar to ESW_Website_KernelKrew
using Location1-Location17 CSV files from main_ofdm folder.

Usage:
    python generate_website.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Field mappings from ThingSpeak
FIELD_NAMES = {
    'field1': 'Temperature',
    'field2': 'Humidity',
    'field3': 'DisconnectedTotal',
    'field4': 'RSL_in',
    'field5': 'RSL_out',
    'field6': 'RPL_rank',
    'field7': 'Hopcount',
    'field8': 'ConnectedTotal'
}

FIELD_UNITS = {
    'field1': '°C',
    'field2': '%',
    'field3': '',
    'field4': 'dBm',
    'field5': 'dBm',
    'field6': '',
    'field7': '',
    'field8': ''
}

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)


def load_location_data(locations_dir='Locations'):
    """Load all Location CSV files"""
    print("="*80)
    print("LOADING DATA FROM CSV FILES")
    print("="*80)
    
    locations_path = Path(locations_dir)
    if not locations_path.exists():
        print(f"✗ Directory not found: {locations_dir}")
        return None
    
    csv_files = sorted(locations_path.glob('Location*.csv'))
    
    if not csv_files:
        print(f"✗ No Location*.csv files found in {locations_dir}")
        return None
    
    data_frames = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            df['timestamp'] = pd.to_datetime(df['created_at'])
            df['location'] = csv_file.stem
            data_frames.append(df)
            print(f"✓ Loaded {csv_file.name}: {len(df)} records")
        except Exception as e:
            print(f"✗ Error loading {csv_file.name}: {e}")
    
    if not data_frames:
        return None
    
    df = pd.concat(data_frames, ignore_index=True)
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    print(f"\n{'='*80}")
    print(f"✓ Total records: {len(df):,}")
    print(f"✓ Total locations: {df['location'].nunique()}")
    print(f"✓ Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"{'='*80}\n")
    
    return df


def generate_summary_stats(df, output_dir):
    """Generate summary statistics"""
    print("Generating summary statistics...")
    
    stats_list = []
    for field in ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'field8']:
        if field in df.columns:
            stats_list.append({
                'Field': FIELD_NAMES[field],
                'Unit': FIELD_UNITS[field],
                'Mean': f"{df[field].mean():.2f}",
                'Median': f"{df[field].median():.2f}",
                'Std': f"{df[field].std():.2f}",
                'Min': f"{df[field].min():.2f}",
                'Max': f"{df[field].max():.2f}",
                'Count': df[field].count()
            })
    
    stats_df = pd.DataFrame(stats_list)
    stats_df.to_csv(output_dir / 'summary_statistics.csv', index=False)
    print("✓ Saved: summary_statistics.csv")
    
    return stats_df


def plot_time_series(df, output_dir):
    """Generate time series plots"""
    print("Generating time series plots...")
    
    fields = ['field1', 'field2', 'field4', 'field5', 'field6', 'field7', 'field8']
    fig, axes = plt.subplots(4, 2, figsize=(18, 20))
    axes = axes.flatten()
    
    colors = plt.cm.tab20(np.linspace(0, 1, df['location'].nunique()))
    
    for idx, field in enumerate(fields):
        if field not in df.columns:
            continue
        
        for loc_idx, location in enumerate(sorted(df['location'].unique())):
            loc_data = df[df['location'] == location].sort_values('timestamp')
            axes[idx].plot(loc_data['timestamp'], loc_data[field],
                         label=location, alpha=0.7, linewidth=1.5, color=colors[loc_idx])
        
        axes[idx].set_title(f'{FIELD_NAMES[field]} ({FIELD_UNITS[field]}) Over Time',
                          fontsize=12, fontweight='bold', pad=10)
        axes[idx].set_xlabel('Time', fontsize=10)
        axes[idx].set_ylabel(f'{FIELD_NAMES[field]} ({FIELD_UNITS[field]})', fontsize=10)
        axes[idx].tick_params(axis='x', rotation=45, labelsize=8)
        axes[idx].grid(True, alpha=0.3)
        
        if idx == 0:
            axes[idx].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7, ncol=2)
    
    fig.delaxes(axes[-1])
    plt.tight_layout()
    plt.savefig(output_dir / 'time_series_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: time_series_analysis.png")
    plt.close()


def plot_correlation_matrix(df, output_dir):
    """Generate correlation heatmap"""
    print("Generating correlation matrix...")
    
    fields = [f'field{i}' for i in range(1, 9) if f'field{i}' in df.columns]
    corr = df[fields].corr()
    
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, linewidths=2, cbar_kws={"shrink": 0.8},
                xticklabels=[FIELD_NAMES[f] for f in fields],
                yticklabels=[FIELD_NAMES[f] for f in fields],
                mask=mask, annot_kws={"size": 9, "weight": "bold"})
    
    plt.title('Environmental & Network Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / 'env_corr_matrix.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: env_corr_matrix.png")
    plt.close()


def plot_signal_analysis(df, output_dir):
    """Signal strength analysis"""
    print("Generating signal strength analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # RSL reciprocity
    scatter = axes[0, 0].scatter(df['field5'], df['field4'],
                                c=df['field8'], cmap='viridis', alpha=0.6, s=30)
    axes[0, 0].set_xlabel('RSL_out (dBm)', fontweight='bold')
    axes[0, 0].set_ylabel('RSL_in (dBm)', fontweight='bold')
    axes[0, 0].set_title('Link Reciprocity: RSL_in vs RSL_out', fontweight='bold')
    plt.colorbar(scatter, ax=axes[0, 0], label='ConnectedTotal')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Add diagonal
    min_val = min(df['field4'].min(), df['field5'].min())
    max_val = max(df['field4'].max(), df['field5'].max())
    axes[0, 0].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, alpha=0.7)
    
    # RSL distribution
    axes[0, 1].hist(df['field4'].dropna(), bins=50, alpha=0.7, color='steelblue', label='RSL_in')
    axes[0, 1].hist(df['field5'].dropna(), bins=50, alpha=0.7, color='coral', label='RSL_out')
    axes[0, 1].set_xlabel('Signal Strength (dBm)', fontweight='bold')
    axes[0, 1].set_ylabel('Frequency', fontweight='bold')
    axes[0, 1].set_title('RSL Distribution', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # RSL over time (aggregate)
    axes[1, 0].plot(df['timestamp'], df['field4'], alpha=0.5, linewidth=0.5, color='steelblue', label='RSL_in')
    axes[1, 0].plot(df['timestamp'], df['field5'], alpha=0.5, linewidth=0.5, color='coral', label='RSL_out')
    axes[1, 0].set_xlabel('Time', fontweight='bold')
    axes[1, 0].set_ylabel('Signal Strength (dBm)', fontweight='bold')
    axes[1, 0].set_title('Signal Strength Over Time', fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Signal vs Connectivity
    scatter = axes[1, 1].scatter(df['field4'], df['field8'],
                                c=df['field7'], cmap='plasma', alpha=0.6, s=30)
    axes[1, 1].set_xlabel('RSL_in (dBm)', fontweight='bold')
    axes[1, 1].set_ylabel('ConnectedTotal', fontweight='bold')
    axes[1, 1].set_title('Signal Strength vs Connectivity', fontweight='bold')
    plt.colorbar(scatter, ax=axes[1, 1], label='Hopcount')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'link_reciprocity.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: link_reciprocity.png")
    plt.close()


def plot_network_topology(df, output_dir):
    """Network topology analysis"""
    print("Generating network topology analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Hopcount vs RPL Rank
    scatter = axes[0, 0].scatter(df['field6'], df['field7'],
                                c=df['field8'], cmap='viridis', alpha=0.6, s=40)
    axes[0, 0].set_xlabel('RPL Rank', fontweight='bold')
    axes[0, 0].set_ylabel('Hopcount', fontweight='bold')
    axes[0, 0].set_title('RPL Rank vs Hopcount', fontweight='bold')
    plt.colorbar(scatter, ax=axes[0, 0], label='ConnectedTotal')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Hopcount distribution
    hopcount_counts = df['field7'].value_counts().sort_index()
    bars = axes[0, 1].bar(hopcount_counts.index, hopcount_counts.values,
                         color='steelblue', alpha=0.8, edgecolor='black')
    axes[0, 1].set_xlabel('Hopcount', fontweight='bold')
    axes[0, 1].set_ylabel('Frequency', fontweight='bold')
    axes[0, 1].set_title('Hopcount Distribution', fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    for bar in bars:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    # Connectivity over time
    ax = axes[1, 0]
    ax.plot(df['timestamp'], df['field8'], color='green', linewidth=1, alpha=0.7, label='Connected')
    ax.set_xlabel('Time', fontweight='bold')
    ax.set_ylabel('ConnectedTotal', color='green', fontweight='bold')
    ax.tick_params(axis='y', labelcolor='green')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    
    ax_twin = ax.twinx()
    ax_twin.plot(df['timestamp'], df['field3'], color='red', linewidth=1, alpha=0.7, label='Disconnected')
    ax_twin.set_ylabel('DisconnectedTotal', color='red', fontweight='bold')
    ax_twin.tick_params(axis='y', labelcolor='red')
    ax.set_title('Network Connectivity Over Time', fontweight='bold')
    
    # RPL Rank by location
    location_rpl = df.groupby('location')['field6'].mean().sort_values()
    axes[1, 1].barh(range(len(location_rpl)), location_rpl.values, color='purple', alpha=0.7)
    axes[1, 1].set_yticks(range(len(location_rpl)))
    axes[1, 1].set_yticklabels(location_rpl.index, fontsize=8)
    axes[1, 1].set_xlabel('Average RPL Rank', fontweight='bold')
    axes[1, 1].set_title('Average RPL Rank by Location', fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'hopcount_rpl_rank.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: hopcount_rpl_rank.png")
    plt.close()


def plot_environmental_analysis(df, output_dir):
    """Environmental analysis"""
    print("Generating environmental analysis...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Temp vs Humidity
    scatter = axes[0, 0].scatter(df['field1'], df['field2'],
                                c=df['field4'], cmap='RdYlGn', alpha=0.6, s=30)
    axes[0, 0].set_xlabel('Temperature (°C)', fontweight='bold')
    axes[0, 0].set_ylabel('Humidity (%)', fontweight='bold')
    axes[0, 0].set_title('Temperature vs Humidity', fontweight='bold')
    plt.colorbar(scatter, ax=axes[0, 0], label='RSL_in (dBm)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Humidity vs RSL
    scatter = axes[0, 1].scatter(df['field2'], df['field4'],
                                c=df['field8'], cmap='viridis', alpha=0.6, s=30)
    axes[0, 1].set_xlabel('Humidity (%)', fontweight='bold')
    axes[0, 1].set_ylabel('RSL_in (dBm)', fontweight='bold')
    axes[0, 1].set_title('Humidity Impact on Signal', fontweight='bold')
    plt.colorbar(scatter, ax=axes[0, 1], label='ConnectedTotal')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Temp vs RSL
    scatter = axes[0, 2].scatter(df['field1'], df['field4'],
                                c=df['field8'], cmap='viridis', alpha=0.6, s=30)
    axes[0, 2].set_xlabel('Temperature (°C)', fontweight='bold')
    axes[0, 2].set_ylabel('RSL_in (dBm)', fontweight='bold')
    axes[0, 2].set_title('Temperature Impact on Signal', fontweight='bold')
    plt.colorbar(scatter, ax=axes[0, 2], label='ConnectedTotal')
    axes[0, 2].grid(True, alpha=0.3)
    
    # Temp over time
    axes[1, 0].plot(df['timestamp'], df['field1'], color='red', linewidth=0.8, alpha=0.7)
    axes[1, 0].set_xlabel('Time', fontweight='bold')
    axes[1, 0].set_ylabel('Temperature (°C)', fontweight='bold')
    axes[1, 0].set_title('Temperature Over Time', fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Humidity over time
    axes[1, 1].plot(df['timestamp'], df['field2'], color='blue', linewidth=0.8, alpha=0.7)
    axes[1, 1].set_xlabel('Time', fontweight='bold')
    axes[1, 1].set_ylabel('Humidity (%)', fontweight='bold')
    axes[1, 1].set_title('Humidity Over Time', fontweight='bold')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(True, alpha=0.3)
    
    # Temperature anomalies
    temp_mean = df['field1'].mean()
    temp_std = df['field1'].std()
    temp_z = np.abs((df['field1'] - temp_mean) / temp_std)
    anomalies = temp_z > 2
    
    axes[1, 2].plot(df['timestamp'], df['field1'], color='green', linewidth=1, alpha=0.7)
    axes[1, 2].scatter(df[anomalies]['timestamp'], df[anomalies]['field1'],
                      color='red', s=50, marker='x', linewidth=2, zorder=5)
    axes[1, 2].axhline(temp_mean, color='blue', linestyle='--', linewidth=2, alpha=0.7)
    axes[1, 2].set_xlabel('Time', fontweight='bold')
    axes[1, 2].set_ylabel('Temperature (°C)', fontweight='bold')
    axes[1, 2].set_title('Temperature Anomaly Detection', fontweight='bold')
    axes[1, 2].tick_params(axis='x', rotation=45)
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'humidity_vs_rsl.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: humidity_vs_rsl.png")
    plt.close()


def generate_interactive_html(df, stats_df, output_dir):
    """Generate interactive HTML dashboard"""
    print("Generating interactive HTML dashboard...")
    
    # Create Plotly figures
    
    # Time series
    fig_ts = make_subplots(rows=4, cols=2, 
                          subplot_titles=[f"{FIELD_NAMES[f'field{i}']} ({FIELD_UNITS[f'field{i}']})" 
                                        for i in [1,2,4,5,6,7,8]],
                          vertical_spacing=0.08)
    
    fields_pos = [(1,1,'field1'), (1,2,'field2'), (2,1,'field4'), (2,2,'field5'),
                  (3,1,'field6'), (3,2,'field7'), (4,1,'field8')]
    
    for row, col, field in fields_pos:
        for location in sorted(df['location'].unique()):
            loc_data = df[df['location'] == location].sort_values('timestamp')
            fig_ts.add_trace(go.Scatter(x=loc_data['timestamp'], y=loc_data[field],
                                       mode='lines', name=location, showlegend=(row==1 and col==1)),
                            row=row, col=col)
    
    fig_ts.update_layout(height=1400, showlegend=True, title_text="Time Series Analysis")
    
    # 3D scatter
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=df['field1'], y=df['field2'], z=df['field4'],
        mode='markers',
        marker=dict(
            size=5, 
            color=df['field8'], 
            colorscale='Viridis', 
            showscale=True,
            opacity=0.8,
            line=dict(width=0.5, color='DarkSlateGrey')
        ),
        text=df['location'],
        hovertemplate='Temp: %{x:.2f}°C<br>Humidity: %{y:.2f}%<br>RSL_in: %{z:.2f} dBm<extra></extra>'
    )])
    fig_3d.update_layout(
        title='3D: Temperature, Humidity & Signal Strength',
        scene=dict(
            xaxis_title='Temperature (°C)',
            yaxis_title='Humidity (%)',
            zaxis_title='RSL_in (dBm)',
            bgcolor='rgba(240,240,240,0.9)'
        ),
        height=700,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    # Correlation heatmap
    fields = [f'field{i}' for i in range(1, 9) if f'field{i}' in df.columns]
    corr = df[fields].corr()
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=[FIELD_NAMES[f] for f in fields],
        y=[FIELD_NAMES[f] for f in fields],
        colorscale='RdBu', 
        zmid=0,
        text=corr.values, 
        texttemplate='%{text:.3f}',
        textfont=dict(size=10),
        colorbar=dict(title="Correlation"),
        hoverongaps=False
    ))
    fig_corr.update_layout(
        title='Correlation Matrix', 
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    # Link reciprocity
    fig_link = go.Figure()
    fig_link.add_trace(go.Scatter(x=df['field5'], y=df['field4'], mode='markers',
                                 marker=dict(size=5, color=df['field8'], colorscale='Viridis', showscale=True)))
    min_val = min(df['field4'].min(), df['field5'].min())
    max_val = max(df['field4'].max(), df['field5'].max())
    fig_link.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val],
                                 mode='lines', line=dict(color='red', dash='dash', width=2),
                                 name='Perfect Reciprocity'))
    fig_link.update_layout(title='Link Reciprocity', xaxis_title='RSL_out (dBm)',
                          yaxis_title='RSL_in (dBm)', height=600)
    
    # Calculate summary stats
    total_records = len(df)
    total_locations = df['location'].nunique()
    date_range = f"{df['timestamp'].min().strftime('%Y-%m-%d')} to {df['timestamp'].max().strftime('%Y-%m-%d')}"
    
    # Create stat cards HTML
    stat_fields = [('field1', '🌡️'), ('field2', '💧'), ('field4', '📡'),
                   ('field5', '📤'), ('field7', '🔄'), ('field8', '🔗')]
    stats_html = ""
    
    for field, icon in stat_fields:
        if field in df.columns:
            mean_val = df[field].mean()
            min_val = df[field].min()
            max_val = df[field].max()
            unit = FIELD_UNITS[field]
            name = FIELD_NAMES[field]
            
            stats_html += f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-title">{name}</div>
                <div class="stat-value">{mean_val:.2f}</div>
                <div class="stat-unit">{unit}</div>
                <div class="stat-range">Range: {min_val:.2f} - {max_val:.2f}</div>
            </div>"""
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wi-SUN Network Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; padding: 20px; }}
        header {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
            margin-bottom: 30px;
        }}
        h1 {{ color: #667eea; font-size: 3em; margin-bottom: 10px; }}
        .subtitle {{ color: #666; font-size: 1.2em; margin-top: 10px; }}
        .info-banner {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-icon {{ font-size: 3em; margin-bottom: 10px; }}
        .stat-title {{ color: #666; font-size: 0.9em; text-transform: uppercase; margin-bottom: 10px; font-weight: 600; }}
        .stat-value {{ color: #667eea; font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }}
        .stat-unit {{ color: #999; margin-bottom: 10px; }}
        .stat-range {{ color: #888; font-size: 0.85em; padding-top: 10px; border-top: 2px solid #f0f0f0; }}
        .tabs {{
            display: flex;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .tab-button {{
            flex: 1;
            padding: 18px 25px;
            background: #f8f9fa;
            border: none;
            cursor: pointer;
            font-size: 1.1rem;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
            border-bottom: 4px solid transparent;
        }}
        .tab-button:hover {{ background: #e9ecef; color: #333; }}
        .tab-button.active {{ background: white; color: #667eea; border-bottom: 4px solid #667eea; }}
        .tab-content {{ display: none; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .tab-content.active {{ display: block; }}
        .chart-container {{ background: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); min-height: 500px; }}
        .section-title {{ color: #667eea; font-size: 2rem; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #667eea; }}
        .description {{ color: #666; font-size: 1.05rem; line-height: 1.8; margin-bottom: 25px; }}
        .insights-box {{
            background: linear-gradient(135deg, #e3f2fd 0%, #e1bee7 100%);
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
        }}
        .insights-box h4 {{ font-size: 1.3rem; margin-bottom: 15px; color: #1976d2; }}
        .insights-box ul {{ margin: 0; padding-left: 25px; color: #0d47a1; }}
        .insights-box li {{ margin-bottom: 10px; font-size: 1rem; }}
        .download-btn {{
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            border-radius: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .download-btn:hover {{ transform: translateY(-3px); }}
        footer {{ background: white; border-radius: 15px; padding: 30px; text-align: center; margin-top: 30px; }}
        @media (max-width: 768px) {{
            .tabs {{ flex-direction: column; }}
            h1 {{ font-size: 2em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌐 Wi-SUN Network Analysis Dashboard</h1>
            <p class="subtitle">Real-time Sensor Data Visualization and Network Performance Analysis</p>
        </header>

        <div class="info-banner">
            <h3>📊 Dataset Overview</h3>
            <p><strong>Total Records:</strong> {total_records:,} | <strong>Locations:</strong> {total_locations} | <strong>Date Range:</strong> {date_range}</p>
        </div>

        <h2 class="section-title">📈 Summary Statistics</h2>
        <div class="stats-grid">{stats_html}
        </div>

        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'overview-tab')">🏠 Overview</button>
            <button class="tab-button" onclick="openTab(event, 'timeseries-tab')">📈 Time Series</button>
            <button class="tab-button" onclick="openTab(event, 'analysis-tab')">🔍 Analysis</button>
            <button class="tab-button" onclick="openTab(event, 'insights-tab')">💡 Insights</button>
        </div>

        <div id="overview-tab" class="tab-content active">
            <h2 class="section-title">🎯 3D Visualization</h2>
            <div class="chart-container" style="text-align:center;">
                <img src="humidity_vs_rsl.png" alt="3D Visualization: Temperature, Humidity & Signal Strength" style="max-width:100%;height:auto;border-radius:8px;">
            </div>
            <h2 class="section-title">🔗 Correlation Analysis</h2>
            <div class="chart-container" style="text-align:center;">
                <img src="env_corr_matrix.png" alt="Correlation Matrix" style="max-width:100%;height:auto;border-radius:8px;">
            </div>
        </div>

        <div id="timeseries-tab" class="tab-content">
            <h2 class="section-title">📈 Time Series Analysis</h2>
            <div class="chart-container"><div id="chart-timeseries" style="width:100%;height:1400px;"></div></div>
        </div>

        <div id="analysis-tab" class="tab-content">
            <h2 class="section-title">📊 Link Reciprocity Analysis</h2>
            <div class="chart-container" style="text-align:center;">
                <img src="link_reciprocity.png" alt="Link Reciprocity Analysis" style="max-width:100%;height:auto;border-radius:8px;">
            </div>
        </div>

        <div id="insights-tab" class="tab-content">
            <h2 class="section-title">💡 Download Data & Visualizations</h2>
            <div style="text-align: center; background: #f8f9fa; padding: 30px; border-radius: 12px;">
                <a href="summary_statistics.csv" class="download-btn" download>📊 Summary Statistics</a>
                <a href="time_series_analysis.png" class="download-btn" download>📈 Time Series</a>
                <a href="env_corr_matrix.png" class="download-btn" download>🔗 Correlation Matrix</a>
                <a href="link_reciprocity.png" class="download-btn" download>📡 Signal Analysis</a>
                <a href="hopcount_rpl_rank.png" class="download-btn" download>🌐 Network Topology</a>
                <a href="humidity_vs_rsl.png" class="download-btn" download>🌡️ Environmental Analysis</a>
            </div>
        </div>

        <footer>
            <p><strong>Wi-SUN Network Analysis Dashboard</strong></p>
            <p style="margin-top: 15px; color: #666;">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>

    <script>
        function openTab(evt, tabName) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            evt.currentTarget.classList.add('active');
            
            // Trigger Plotly resize after tab switch to ensure proper rendering
            setTimeout(function() {{
                window.dispatchEvent(new Event('resize'));
            }}, 100);
        }}

        // Initialize all Plotly charts
        function initCharts() {{
            console.log('Initializing charts...');
            try {{
                console.log('Creating timeseries chart...');
                var timeseriesData = {fig_ts.to_json()};
                Plotly.newPlot('chart-timeseries', timeseriesData.data, timeseriesData.layout, {{responsive: true}}).then(function() {{
                    console.log('Timeseries chart created successfully');
                }}).catch(function(err) {{
                    console.error('Error plotting timeseries:', err);
                }});

                console.log('Creating 3D chart...');
                var data3d = {fig_3d.to_json()};
                Plotly.newPlot('chart-3d', data3d.data, data3d.layout, {{responsive: true}}).then(function() {{
                    console.log('3D chart created successfully');
                    // Check if chart has rendered content
                    setTimeout(function() {{
                        var chart3d = document.getElementById('chart-3d');
                        if (chart3d && chart3d.offsetHeight === 0) {{
                            document.getElementById('fallback-3d').style.display = 'block';
                            chart3d.style.display = 'none';
                        }}
                    }}, 1000);
                }}).catch(function(err) {{
                    console.error('Error plotting 3d:', err);
                    document.getElementById('fallback-3d').style.display = 'block';
                    document.getElementById('chart-3d').style.display = 'none';
                }});

                console.log('Creating correlation chart...');
                var corrData = {fig_corr.to_json()};
                Plotly.newPlot('chart-correlation', corrData.data, corrData.layout, {{responsive: true}}).then(function() {{
                    console.log('Correlation chart created successfully');
                    // Check if chart has rendered content
                    setTimeout(function() {{
                        var chartCorr = document.getElementById('chart-correlation');
                        if (chartCorr && chartCorr.offsetHeight === 0) {{
                            document.getElementById('fallback-corr').style.display = 'block';
                            chartCorr.style.display = 'none';
                        }}
                    }}, 1000);
                }}).catch(function(err) {{
                    console.error('Error plotting correlation:', err);
                    document.getElementById('fallback-corr').style.display = 'block';
                    document.getElementById('chart-correlation').style.display = 'none';
                }});

                console.log('Creating link chart...');
                var linkData = {fig_link.to_json()};
                Plotly.newPlot('chart-link', linkData.data, linkData.layout, {{responsive: true}}).then(function() {{
                    console.log('Link chart created successfully');
                }}).catch(function(err) {{
                    console.error('Error plotting link:', err);
                }});
            }} catch(e) {{
                console.error('Error initializing charts:', e);
            }}
        }}

        // Try multiple initialization methods to ensure charts load
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initCharts);
        }} else {{
            initCharts();
        }}
    </script>
</body>
</html>"""
    
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✓ Saved: index.html")


def main():
    """Main execution"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║       Wi-SUN Website Generator - Using Local CSV Files        ║
║                                                                 ║
║  Generates comprehensive analysis from Location1-17 CSVs       ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    # Load data
    df = load_location_data('Locations')
    
    if df is None:
        print("\n✗ Failed to load data. Exiting.")
        return
    
    # Create output directory
    output_dir = Path('wisun_website_output')
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS AND WEBSITE")
    print("="*80 + "\n")
    
    # Generate all components
    stats_df = generate_summary_stats(df, output_dir)
    plot_time_series(df, output_dir)
    plot_correlation_matrix(df, output_dir)
    plot_signal_analysis(df, output_dir)
    plot_network_topology(df, output_dir)
    plot_environmental_analysis(df, output_dir)
    generate_interactive_html(df, stats_df, output_dir)
    
    print("\n" + "="*80)
    print("✅ WEBSITE GENERATION COMPLETE!")
    print("="*80)
    print(f"\n📁 Output directory: {output_dir.absolute()}")
    print(f"🌐 Main website: {(output_dir / 'index.html').absolute()}")
    print("\n📊 Generated files:")
    for file in sorted(output_dir.glob('*')):
        print(f"   • {file.name}")
    print("\n💡 Open index.html in your web browser to view the interactive dashboard!")


if __name__ == "__main__":
    main()
