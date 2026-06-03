import pandas as pd
import matplotlib.pyplot as plt

# Load data
naive = pd.read_csv("naive_results.csv")
perthread = pd.read_csv("perthread_results.csv")


def extract_pt_t4(df):
    baseline = df[
        (df["section"] == "pt_t4")
        & (df["metric"] == "baseline")
        & (df["stat"] == "total_ticks")
    ]["value"].iloc[0]

    waiter = df[
        (df["section"] == "pt_t4")
        & (df["metric"] == "with_waiter")
        & (df["stat"] == "total_ticks")
    ]["value"].iloc[0]

    overhead = df[
        (df["section"] == "pt_t4")
        & (df["metric"] == "overhead")
        & (df["stat"] == "pct")
    ]["value"].iloc[0]

    return baseline, waiter, overhead


pt_baseline, pt_waiter, pt_overhead = extract_pt_t4(perthread)
naive_baseline, naive_waiter, naive_overhead = extract_pt_t4(naive)

# Shared y-axis range
ymax = (
    max(
        pt_baseline,
        pt_waiter,
        naive_baseline,
        naive_waiter,
    )
    * 1.1
)

# Figure layout
fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(
    2,
    2,
    height_ratios=[4, 1]
)

ax_pt = fig.add_subplot(gs[0, 0])
ax_naive = fig.add_subplot(gs[0, 1])

# Per-thread chart
ax_pt.bar(
    ["Baseline", "With Waiter"],
    [pt_baseline, pt_waiter],
    color="#4B0082"
)
ax_pt.set_title("Per-Thread LMP")
ax_pt.set_ylabel("Total Ticks")
ax_pt.set_ylim(0, ymax)

# Naive chart
ax_naive.bar(
    ["Baseline", "With Waiter"],
    [naive_baseline, naive_waiter],
    color="#4B0082"
)
ax_naive.set_title("Per-Process LMP")
ax_naive.set_ylim(0, ymax)

# Text under plots
ax_pt_text = fig.add_subplot(gs[1, 0])
ax_pt_text.axis("off")
ax_pt_text.text(
    0.5,
    0.5,
    f"Overhead: {pt_overhead:.0f}%",
    ha="center",
    va="center",
    fontsize=12,
)

ax_naive_text = fig.add_subplot(gs[1, 1])
ax_naive_text.axis("off")
ax_naive_text.text(
    0.5,
    0.5,
    f"Overhead: {naive_overhead:.0f}%",
    ha="center",
    va="center",
    fontsize=12,
)

plt.tight_layout()
plt.show()
