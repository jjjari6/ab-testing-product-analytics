import numpy as np
import pandas as pd

np.random.seed(42)

n_users = 50000

groups = np.random.choice(
    ["control", "treatment"],
    size=n_users,
    p=[0.5, 0.5]
)

devices = np.random.choice(
    ["mobile", "desktop", "tablet"],
    size=n_users,
    p=[0.60, 0.32, 0.08]
)

traffic_sources = np.random.choice(
    ["organic", "paid", "email", "social"],
    size=n_users,
    p=[0.35, 0.30, 0.20, 0.15]
)

base_rates = {
    "mobile": 0.105,
    "desktop": 0.145,
    "tablet": 0.115
}

converted = []

for group, device in zip(groups, devices):

    rate = base_rates[device]

    if group == "treatment":
        rate += 0.004

    converted.append(
        np.random.binomial(1, rate)
    )

df = pd.DataFrame({
    "user_id": range(1, n_users + 1),
    "group": groups,
    "device": devices,
    "traffic_source": traffic_sources,
    "converted": converted
})

df.to_csv("data/ab_test_data.csv", index=False)

print("Dataset created successfully.")
print(df.head())
print()
print(df["group"].value_counts())
print()
print(df.groupby("group")["converted"].mean())