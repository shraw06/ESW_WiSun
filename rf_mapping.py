# ==============================================================
# Wi-SUN RF Mapping & Analysis Dashboard (Python, WSL-safe)
# ==============================================================

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
from scipy.interpolate import griddata
import plotly.express as px
import glob

# Detect if running in headless mode (like WSL or SSH)
if not os.environ.get("DISPLAY"):
    matplotlib.use('Agg')  # Use non-interactive backend

# Create results directory
os.makedirs("results", exist_ok=True)

# ==============================================================
# 1️⃣ Load & Combine CSVs
# ==============================================================

files = glob.glob("data/*.csv")
if not files:
    sys.exit("❌ No CSV files found in ./data/ — please check your path.")

dfs = []
for f in files:
    name = os.path.basename(f).split(".")[0]
    temp = pd.read_csv(f)
    temp["location"] = name
    dfs.append(temp)

df = pd.concat(dfs, ignore_index=True)
df["created_at"] = pd.to_datetime(df["created_at"])
print(f"📂 Loaded {len(files)} files, {len(df)} total samples")

# ==============================================================
# 2️⃣ Assign Coordinates (edit these!)
# ==============================================================

coords = {
    "location1": (120, 220),
    "location2": (350, 280),
    "location3": (450, 400),
    "location4": (200, 480)
}
df["x"] = df["location"].map(lambda l: coords.get(l, (0, 0))[0])
df["y"] = df["location"].map(lambda l: coords.get(l, (0, 0))[1])

# ==============================================================
# 3️⃣ Summarize & Compute Derived Metrics
# ==============================================================

summary = df.groupby("location").agg({
    "RSL_out": "mean",
    "RSL_in": "mean",
    "Hopcount": "mean",
    "RPL_rank": "mean",
    "ConnectedTotal": "mean",
    "DisconnectedTotal": "mean",
    "Temperature": "mean",
    "Humidity": "mean",
    "x": "first",
    "y": "first"
}).reset_index()

summary["Reliability"] = summary["ConnectedTotal"] / (
    summary["ConnectedTotal"] + summary["DisconnectedTotal"]
)
summary["RSL_diff"] = summary["RSL_out"] - summary["RSL_in"]
summary["RSL_out_dBm"] = summary["RSL_out"] - 174

print("\n📊 Per-location summary:")
print(summary[["location", "RSL_out", "RSL_in", "Reliability"]])

# ==============================================================
# 4️⃣ RF Heatmap Overlay
# ==============================================================

img_path = "mappy.jpg"
if not os.path.exists(img_path):
    sys.exit("❌ Map image not found: mappy.jpg")

img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

points = summary[["x", "y"]].to_numpy()
values = summary["RSL_out"].to_numpy()

grid_x, grid_y = np.mgrid[0:img.shape[1]:300j, 0:img.shape[0]:300j]
grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')

plt.figure(figsize=(8, 6))
plt.imshow(img)
plt.imshow(grid_z.T, extent=(0, img.shape[1], img.shape[0], 0),
           alpha=0.55, cmap="RdYlGn")
plt.scatter(points[:, 0], points[:, 1], c='black', label='Node', s=40)
plt.colorbar(label='RSL_out (dBm)')
plt.title('Wi-SUN RF Coverage Heatmap Overlay')
plt.legend()
plt.tight_layout()
plt.savefig("results/rf_heatmap.png", dpi=300)
plt.close()

# ==============================================================
# 5️⃣ Path Loss Analysis (distance vs RSL_out)
# ==============================================================

x_root, y_root = 100, 150
summary["distance"] = np.sqrt((summary.x - x_root)**2 + (summary.y - y_root)**2)

fig = px.scatter(summary, x="distance", y="RSL_out",
                 trendline="ols", text="location",
                 title="Path Loss Curve (RSL_out vs Distance)")
fig.update_traces(textposition="top center")
fig.write_html("results/path_loss_curve.html")

# ==============================================================
# 6️⃣ Environmental Correlation
# ==============================================================

sns.set(style="whitegrid")
plt.figure(figsize=(6, 4))
sns.scatterplot(data=df, x="Humidity", y="RSL_out", hue="location", s=60)
plt.title("Humidity vs RSL_out")
plt.tight_layout()
plt.savefig("results/humidity_vs_rsl.png", dpi=300)
plt.close()

plt.figure(figsize=(6, 4))
sns.heatmap(df[["Temperature", "Humidity", "RSL_in", "RSL_out"]].corr(),
            annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Environmental Correlation Matrix")
plt.tight_layout()
plt.savefig("results/env_corr_matrix.png", dpi=300)
plt.close()

# ==============================================================
# 7️⃣ Reciprocity Analysis
# ==============================================================

fig = px.scatter(df, x="RSL_out", y="RSL_in", color="location",
                 trendline="ols", title="RSL_in vs RSL_out (Link Reciprocity)")
fig.write_html("results/link_reciprocity.html")

# ==============================================================
# 8️⃣ Reliability Map
# ==============================================================

plt.imshow(img)
for _, r in summary.iterrows():
    plt.scatter(r.x, r.y, s=r.Reliability * 800, c='green', alpha=0.6)
    plt.text(r.x + 10, r.y, f"{r.location}\n{r.Reliability:.2f}", color="black")
plt.title("Connectivity Reliability per Node")
plt.tight_layout()
plt.savefig("results/reliability_map.png", dpi=300)
plt.close()

print("\n✅ RF Mapping Complete!")
print("📁 All visualizations saved in ./results/")
print("🖼️  -> rf_heatmap.png, humidity_vs_rsl.png, reliability_map.png")
print("📈  -> path_loss_curve.html, link_reciprocity.html")
print("\nYou can open the .html files in your browser for interactive plots.")
