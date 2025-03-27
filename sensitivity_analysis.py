import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define thresholds and baseline
thresholds = np.arange(0.5, 0.7 + 0.02, 0.02)
thresholds = [round(t, 2) for t in thresholds]
baseline_threshold = 0.6

# Store correlation results
correlation_results = []

for th in thresholds:
    if np.isclose(th, baseline_threshold):
        correlation_results.append({"Threshold": th, "Spearman Correlation": 1.0})
    else:
        df_baseline = pd.read_csv(f"course_data_{baseline_threshold:.2f}.csv")
        df_th = pd.read_csv(f"course_data_{th:.2f}.csv")

        merged_df = pd.merge(df_baseline, df_th, on="id", suffixes=(f"_{baseline_threshold:.2f}", f"_{th:.2f}"))
        baseline_ci = merged_df[f"course_influence_{baseline_threshold:.2f}"].astype(float)
        th_ci = merged_df[f"course_influence_{th:.2f}"].astype(float)
        spearman_corr = baseline_ci.corr(th_ci, method="spearman")

        correlation_results.append({"Threshold": th, "Spearman Correlation": spearman_corr})

# Create correlation DataFrame
correlation_df = pd.DataFrame(correlation_results)

# Merge with link density and giant component ratio results
result_df = pd.read_csv("link_density_and_giant_component_ratio.csv")
merged_result_df = result_df.merge(correlation_df, on="Threshold", how="left")

# Extract values as numpy arrays
thresholds = merged_result_df["Threshold"].to_numpy()
link_density = merged_result_df["Link Density"].to_numpy()
gcr = merged_result_df["Giant Component Ratio"].to_numpy()
spearman = merged_result_df["Spearman Correlation"].to_numpy()

# Calculate relative values based on baseline
baseline_values = merged_result_df[merged_result_df["Threshold"] == baseline_threshold].iloc[0]
merged_result_df["Relative Link Density"] = merged_result_df["Link Density"] / baseline_values["Link Density"]
merged_result_df["Relative GCR"] = merged_result_df["Giant Component Ratio"] / baseline_values["Giant Component Ratio"]
merged_result_df["Relative Spearman"] = merged_result_df["Spearman Correlation"]

# Calculate absolute change ratios
merged_result_df["Delta Spearman"] = abs(merged_result_df["Spearman Correlation"] - baseline_values["Spearman Correlation"]) / baseline_values["Spearman Correlation"]
merged_result_df["Delta Link Density"] = abs(merged_result_df["Relative Link Density"] - 1)
merged_result_df["Delta GCR"] = abs(merged_result_df["Relative GCR"] - 1)

# Set colors
color_spearman = "black"
color_density = "red"
color_gcr = "blue"

# (a) Network structure change
plt.figure(figsize=(8, 6))
plt.plot(thresholds, merged_result_df["Relative Link Density"].to_numpy(), marker="o", label="Relative Link Density", color=color_density)
plt.plot(thresholds, merged_result_df["Relative GCR"].to_numpy(), marker="o", label="Relative GCR", color=color_gcr)
plt.xlabel("Threshold", fontsize=16)
plt.ylabel("Value", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.yscale("log")
plt.axhline(y=1, color="black", linestyle="--", linewidth=1)
plt.legend()
plt.savefig("S_fig_5_a.png", dpi=300)
plt.show()

# (b) Course influence ranking change
plt.figure(figsize=(8, 6))
plt.plot(thresholds, merged_result_df["Relative Spearman"].to_numpy(), marker="o", label="Rank Correlation", color=color_spearman)
plt.xlabel("Threshold", fontsize=16)
plt.ylabel("Rank Correlation", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(bottom=0)
plt.savefig("S_fig_5_b.png", dpi=300)
plt.show()

# (c) Absolute value of relative change
plt.figure(figsize=(8, 6))
plt.plot(thresholds, merged_result_df["Delta Spearman"].to_numpy(), marker="o", label="|\u0394ρ / ρ(0.6)|", color=color_spearman)
plt.plot(thresholds, merged_result_df["Delta Link Density"].to_numpy(), marker="o", label="|\u0394d / d(0.6)|", color=color_density)
plt.plot(thresholds, merged_result_df["Delta GCR"].to_numpy(), marker="o", label="|\u0394r / r(0.6)|", color=color_gcr)
plt.xlabel("Threshold", fontsize=16)
plt.ylabel("Absolute Change", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
plt.ylim(0, 2)
plt.savefig("S_fig_5_c.png", dpi=300)
plt.show()
