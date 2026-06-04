import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("avg.csv")

# Remove rows with missing section/value
df = df.dropna(subset=["section", "value"])

# Remove rows where section is empty whitespace
df = df[df["section"].astype(str).str.strip() != ""]

# Plot
plt.figure(figsize=(10, 5))
plt.plot(df["section"], df["value"], marker="o", color="#301934")

plt.xlabel("Size of pending_replies array")
plt.ylabel("Total Cycles for All Threads")
plt.title("Effect of pending_replies Size on Concurrent Scalability")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()
