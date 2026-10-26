import pandas as pd

# This repository uses a small synthetic sample dataset for demonstration only.
df = pd.read_csv("delivery_data.csv")

for col in ["promised_delivery_time", "actual_delivery_time"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

print("Rows:", len(df))
print("Duplicate order IDs:", df["order_id"].duplicated().sum())
print("Missing values by column:")
print(df.isna().sum())

completed = df[df["delivery_status"].eq("delivered")].copy()
completed["on_time"] = completed["actual_delivery_time"] <= completed["promised_delivery_time"]
print(f"On-time delivery rate: {completed['on_time'].mean() * 100:.1f}%")

route_summary = completed.groupby("route_id").agg(
    deliveries=("order_id", "count"),
    on_time_rate=("on_time", "mean"),
    average_distance_km=("distance_km", "mean")
).reset_index()
route_summary["on_time_rate"] *= 100
print("\nRoute summary:")
print(route_summary.sort_values("on_time_rate"))
