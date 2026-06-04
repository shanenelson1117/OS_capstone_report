import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Load data
df = pd.read_csv("perthread_results.csv")

# Extract values
rtt_values = df[df["section"] == "rtt"]["value"].dropna()
stress_values = df[df["section"] == "stress"]["value"].dropna()

# Compute summary statistics
summary = pd.DataFrame({
    "Mean": [
        rtt_values.mean(),
        stress_values.mean()
    ],
    "P50 (Median)": [
        np.percentile(rtt_values, 50),
        np.percentile(stress_values, 50)
    ],
    "P90": [
        np.percentile(rtt_values, 90),
        np.percentile(stress_values, 90)
    ]
}, index=["RTT", "Stress"])

# Create figure with space for table
fig = plt.figure(figsize=(12, 7))
gs = fig.add_gridspec(2, 2, height_ratios=[4, 1])

ax_rtt = fig.add_subplot(gs[0, 0])
ax_stress = fig.add_subplot(gs[0, 1])
ax_table = fig.add_subplot(gs[1, :])

for ax, values, title in [
    (ax_rtt, rtt_values, "RTT"),
    (ax_stress, stress_values, "Stress"),
]:
    # Fit normal distribution
    mu, sigma = norm.fit(values)

    # Histogram
    ax.hist(values, bins="auto", density=True, alpha=0.6, color="#4B0082")

    # Overlay fitted normal curve
    x = np.linspace(values.min(), values.max(), 500)
    ax.plot(x, norm.pdf(x, mu, sigma), linewidth=2)

    ax.set_title(f"{title} Distribution")
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")

# Build statistics table
ax_table.axis("off")
table = ax_table.table(
    cellText=np.round(summary.values, 2),
    rowLabels=summary.index,
    colLabels=summary.columns,
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

plt.tight_layout()
plt.show()
