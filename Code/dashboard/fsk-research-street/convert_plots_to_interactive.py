#!/usr/bin/env python3
"""
Convert static PNG plots to interactive HTML plots using Plotly.
Uses actual Wi-SUN network data from CSV files.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import glob
import os

# Load the actual data
data_path = "../ESW_WiSun/data/"
files = glob.glob(data_path + "*.csv")

if not files:
    print("⚠️  No data files found. Using sample data instead.")
    USE_REAL_DATA = False
else:
    print(f"📂 Found {len(files)} data files")
    USE_REAL_DATA = True
    
    # Load and combine all CSV files
    dfs = []
    for f in files:
        name = os.path.basename(f).split(".")[0]
        temp = pd.read_csv(f)
        temp["location"] = name
        dfs.append(temp)
    
    df = pd.concat(dfs, ignore_index=True)
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # Assign coordinates
    coords = {
        "location1": (120, 220),
        "location2": (350, 280),
        "location3": (450, 400),
        "location4": (200, 480)
    }
    df["x"] = df["location"].map(lambda l: coords.get(l, (0, 0))[0])
    df["y"] = df["location"].map(lambda l: coords.get(l, (0, 0))[1])
    
    # Calculate distance from root node
    x_root, y_root = 100, 150
    df["distance_px"] = np.sqrt((df.x - x_root)**2 + (df.y - y_root)**2)
    df["distance_m"] = df["distance_px"] * 0.5  # Approximate pixel to meter conversion
    
    print(f"✅ Loaded {len(df)} total samples from {len(files)} locations")

def create_pathloss_plot(output_file):
    """Pathloss Fit plot using real Wi-SUN data"""
    if USE_REAL_DATA:
        # Group by location and get mean values
        summary = df.groupby("location").agg({
            "distance_m": "first",
            "RSL_out": "mean"
        }).reset_index()
        
        # Create scatter plot with individual measurements
        fig = go.Figure()
        
        # Add scatter plot for all measurements
        fig.add_trace(go.Scatter(
            x=df["distance_m"], 
            y=df["RSL_out"], 
            mode='markers',
            name='Measured RSL',
            marker=dict(color='#667eea', size=6, opacity=0.6),
            text=df['location'],
            hovertemplate='<b>%{text}</b><br>Distance: %{x:.1f}m<br>RSL: %{y:.1f} dBm<extra></extra>'
        ))
        
        # Add mean values per location
        fig.add_trace(go.Scatter(
            x=summary["distance_m"], 
            y=summary["RSL_out"],
            mode='markers+text',
            name='Mean per Location',
            marker=dict(color='#f56565', size=12, symbol='diamond'),
            text=summary['location'],
            textposition="top center",
            hovertemplate='<b>%{text}</b><br>Distance: %{x:.1f}m<br>Mean RSL: %{y:.1f} dBm<extra></extra>'
        ))
        
        fig.update_layout(
            title='Path Loss: RSL vs Distance from Root Node',
            xaxis_title='Distance (meters)',
            yaxis_title='RSL (dBm)',
            template='plotly_white',
            hovermode='closest',
            height=500,
            showlegend=True
        )
    else:
        # Fallback to sample data
        distance = np.linspace(1, 100, 50)
        pathloss = 40 + 20 * np.log10(distance) + np.random.normal(0, 3, len(distance))
        fit = 40 + 20 * np.log10(distance)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=distance, y=pathloss, mode='markers', name='Measured',
                                 marker=dict(color='#667eea', size=8)))
        fig.add_trace(go.Scatter(x=distance, y=fit, mode='lines', name='Path Loss Model',
                                 line=dict(color='#f56565', width=2)))
        
        fig.update_layout(
            title='Pathloss Fit (meters) - Sample Data',
            xaxis_title='Distance (m)',
            yaxis_title='Path Loss (dB)',
            template='plotly_white',
            hovermode='closest',
            height=500
        )
    
    fig.write_html(output_file)
    print(f"✓ Created {output_file}")

def create_rsl_profile_plot(output_file):
    """RSL 1D Profile plot using real data"""
    if USE_REAL_DATA:
        # Sort by timestamp and create time series
        df_sorted = df.sort_values('created_at')
        df_sorted['time_min'] = (df_sorted['created_at'] - df_sorted['created_at'].min()).dt.total_seconds() / 60
        
        fig = go.Figure()
        
        # Plot RSL_out and RSL_in for each location
        for location in df_sorted['location'].unique():
            loc_data = df_sorted[df_sorted['location'] == location]
            fig.add_trace(go.Scatter(
                x=loc_data['time_min'],
                y=loc_data['RSL_out'],
                mode='lines+markers',
                name=f'{location} (out)',
                line=dict(width=2),
                marker=dict(size=4)
            ))
        
        fig.update_layout(
            title='RSL Time Profile (All Locations)',
            xaxis_title='Time (minutes from start)',
            yaxis_title='RSL (dBm)',
            template='plotly_white',
            hovermode='x unified',
            height=500
        )
    else:
        # Fallback sample data
        distance = np.linspace(0, 100, 100)
        rsl = -40 - 0.3 * distance + np.random.normal(0, 2, len(distance))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=distance, y=rsl, mode='lines+markers',
                                 line=dict(color='#48bb78', width=2),
                                 marker=dict(size=4)))
        
        fig.update_layout(
            title='RSL 1D Profile (meters) - Sample Data',
            xaxis_title='Distance (m)',
            yaxis_title='RSL (dBm)',
            template='plotly_white',
            hovermode='closest',
            height=500
        )
    
    fig.write_html(output_file)
    print(f"✓ Created {output_file}")

def create_humidity_rsl_plot(output_file):
    """Humidity vs RSL scatter plot using real data"""
    if USE_REAL_DATA:
        fig = go.Figure()
        
        # Color code by location
        colors = {'location1': '#667eea', 'location2': '#48bb78', 
                  'location3': '#ed8936', 'location4': '#f56565'}
        
        for location in df['location'].unique():
            loc_data = df[df['location'] == location]
            fig.add_trace(go.Scatter(
                x=loc_data['Humidity'],
                y=loc_data['RSL_out'],
                mode='markers',
                name=location,
                marker=dict(color=colors.get(location, '#667eea'), size=8),
                hovertemplate='<b>%{text}</b><br>Humidity: %{x:.1f}%<br>RSL: %{y:.1f} dBm<extra></extra>',
                text=[location] * len(loc_data)
            ))
        
        fig.update_layout(
            title='Humidity vs. RSL (Outbound)',
            xaxis_title='Humidity (%)',
            yaxis_title='RSL (dBm)',
            template='plotly_white',
            hovermode='closest',
            height=500,
            showlegend=True
        )
    else:
        # Fallback sample data
        humidity = np.random.uniform(30, 80, 100)
        rsl = -50 - 0.2 * humidity + np.random.normal(0, 3, 100)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=humidity, y=rsl, mode='markers',
                                 marker=dict(color='#667eea', size=8)))
        
        fig.update_layout(
            title='Humidity vs. RSL - Sample Data',
            xaxis_title='Humidity (%)',
            yaxis_title='RSL (dBm)',
            template='plotly_white',
            hovermode='closest',
            height=500
        )
    
    fig.write_html(output_file)
    print(f"✓ Created {output_file}")

def create_correlation_matrix_plot(output_file):
    """Environmental Correlation Matrix heatmap using real data"""
    if USE_REAL_DATA:
        # Calculate correlation matrix for environmental and signal parameters
        corr_vars = ["Temperature", "Humidity", "RSL_in", "RSL_out"]
        corr_matrix = df[corr_vars].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_vars,
            y=corr_vars,
            colorscale='RdBu',
            zmid=0,
            text=np.around(corr_matrix.values, decimals=2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title='Correlation')
        ))
        
        fig.update_layout(
            title='Environmental & Signal Correlation Matrix',
            template='plotly_white',
            height=500,
            xaxis={'side': 'bottom'}
        )
    else:
        # Fallback sample data
        variables = ['Temperature', 'Humidity', 'Pressure', 'RSL', 'RSSI']
        corr_matrix = np.random.rand(5, 5)
        corr_matrix = (corr_matrix + corr_matrix.T) / 2
        np.fill_diagonal(corr_matrix, 1.0)
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=variables,
            y=variables,
            colorscale='RdBu',
            zmid=0,
            text=np.around(corr_matrix, decimals=2),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Environmental Correlation Matrix - Sample Data',
            template='plotly_white',
            height=500,
            xaxis={'side': 'bottom'}
        )
    
    fig.write_html(output_file)
    print(f"✓ Created {output_file}")

def create_hopcount_rpl_plot(output_file):
    """Hopcount vs RPL Rank plot using real data"""
    if USE_REAL_DATA:
        fig = go.Figure()
        
        # Color code by location
        colors = {'location1': '#667eea', 'location2': '#48bb78', 
                  'location3': '#ed8936', 'location4': '#f56565'}
        
        for location in df['location'].unique():
            loc_data = df[df['location'] == location]
            fig.add_trace(go.Scatter(
                x=loc_data['Hopcount'],
                y=loc_data['RPL_rank'],
                mode='markers',
                name=location,
                marker=dict(color=colors.get(location, '#ed8936'), size=8),
                hovertemplate='<b>%{text}</b><br>Hopcount: %{x}<br>RPL Rank: %{y}<extra></extra>',
                text=[location] * len(loc_data)
            ))
        
        fig.update_layout(
            title='Hopcount vs. RPL Rank',
            xaxis_title='Hopcount',
            yaxis_title='RPL Rank',
            template='plotly_white',
            hovermode='closest',
            height=500,
            showlegend=True
        )
    else:
        # Fallback sample data
        hopcount = np.repeat(np.arange(1, 6), 20)
        rpl_rank = 256 * hopcount + np.random.normal(0, 50, len(hopcount))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hopcount, y=rpl_rank, mode='markers',
                                 marker=dict(color='#ed8936', size=8)))
        
        fig.update_layout(
            title='Hopcount vs. RPL Rank - Sample Data',
            xaxis_title='Hopcount',
            yaxis_title='RPL Rank',
            template='plotly_white',
            hovermode='closest',
            height=500
        )
    
    fig.write_html(output_file)
    print(f"✓ Created {output_file}")

def create_temperature_anomaly_plot(output_file):
    """Temperature Anomaly time series using real data"""
    if USE_REAL_DATA:
        # Sort by timestamp
        df_sorted = df.sort_values('created_at')
        
        # Calculate baseline (mean temperature)
        baseline = df_sorted['Temperature'].mean()
        
        fig = go.Figure()
        
        # Plot temperature for each location
        colors = {'location1': '#f56565', 'location2': '#48bb78', 
                  'location3': '#ed8936', 'location4': '#667eea'}
        
        for location in df_sorted['location'].unique():
            loc_data = df_sorted[df_sorted['location'] == location]
            fig.add_trace(go.Scatter(
                x=loc_data['created_at'],
                y=loc_data['Temperature'],
                mode='lines+markers',
                name=location,
                line=dict(color=colors.get(location, '#f56565'), width=2),
                marker=dict(size=4)
            ))
        
        # Add baseline
        fig.add_trace(go.Scatter(
            x=df_sorted['created_at'],
            y=[baseline]*len(df_sorted),
            mode='lines',
            name=f'Baseline ({baseline:.1f}°C)',
            line=dict(color='gray', dash='dash', width=2)
        ))
        
        fig.update_layout(
            title='Temperature Variation Over Time',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            template='plotly_white',
            hovermode='x unified',
            height=500,
            showlegend=True
        )
    else:
        # Fallback sample data
        time = pd.date_range('2024-01-01', periods=100, freq='h')
        temp = 25 + 5 * np.sin(np.arange(100) * 2 * np.pi / 24) + np.random.normal(0, 1, 100)
        baseline = 25
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time, y=temp, mode='lines', name='Temperature',
                                 line=dict(color='#f56565', width=2)))
        fig.add_trace(go.Scatter(x=time, y=[baseline]*len(time), mode='lines',
                                 name='Baseline', line=dict(color='gray', dash='dash')))
        
        fig.update_layout(
            title='Temperature Anomaly - Sample Data',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            template='plotly_white',
            hovermode='x unified',
            height=500
        )
    
    fig.write_html(output_file)
    print(f"✓ Created {output_file}")

def create_time_position_heatmap(output_file):
    """Time Position Heatmap using real data"""
    if USE_REAL_DATA:
        # Extract hour from timestamp
        df['hour'] = df['created_at'].dt.hour
        df['minute_bucket'] = (df['created_at'].dt.minute // 5) * 5  # 5-minute buckets
        df['time_label'] = df['created_at'].dt.strftime('%H:%M')
        
        # Create pivot table for heatmap
        # Use RSL_out as the value to display
        pivot_data = df.pivot_table(
            values='RSL_out',
            index='location',
            columns='time_label',
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            colorbar=dict(title='RSL (dBm)'),
            hovertemplate='Location: %{y}<br>Time: %{x}<br>RSL: %{z:.1f} dBm<extra></extra>'
        ))
        
        fig.update_layout(
            title='RSL Heatmap: Location vs Time',
            xaxis_title='Time',
            yaxis_title='Location',
            template='plotly_white',
            height=500,
            xaxis={'tickangle': -45}
        )
    else:
        # Fallback sample data
        hours = list(range(24))
        positions = [f'Node {i}' for i in range(1, 21)]
        data = np.random.rand(20, 24) * 100
        
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=hours,
            y=positions,
            colorscale='Viridis',
            colorbar=dict(title='Activity')
        ))
        
        fig.update_layout(
            title='Time Position Heatmap - Sample Data',
            xaxis_title='Hour of Day',
            yaxis_title='Node Position',
            template='plotly_white',
            height=500
        )
    
    fig.write_html(output_file)
    print(f"✓ Created {output_file}")


def main():
    """
    Generate all interactive plots using real Wi-SUN network data.
    """
    
    print("=" * 60)
    if USE_REAL_DATA:
        print("🎯 Generating interactive plots with REAL Wi-SUN data")
    else:
        print("⚠️  Using sample data (real data files not found)")
    print("=" * 60)
    
    create_pathloss_plot("pathloss_fit_meters.html")
    create_rsl_profile_plot("rsl_1d_profile_meters.html")
    create_humidity_rsl_plot("humidity_vs_rsl.html")
    create_correlation_matrix_plot("env_corr_matrix.html")
    create_hopcount_rpl_plot("hopcount_rpl_rank.html")
    create_temperature_anomaly_plot("temperature_anomaly.html")
    create_time_position_heatmap("time_position_heatmap.html")
    
    print("=" * 60)
    print("\n✅ All interactive plots created!")
    if USE_REAL_DATA:
        print("\n🎉 Your plots now display actual Wi-SUN network data!")
        print(f"   - {len(df)} measurements from {len(df['location'].unique())} locations")
        print(f"   - Temperature: {df['Temperature'].min():.1f}°C to {df['Temperature'].max():.1f}°C")
        print(f"   - Humidity: {df['Humidity'].min():.1f}% to {df['Humidity'].max():.1f}%")
        print(f"   - RSL: {df['RSL_out'].min():.1f} to {df['RSL_out'].max():.1f} dBm")
    print("\n🌐 Refresh your browser to see the updated plots!")

if __name__ == "__main__":
    main()
