import pandas as pd

df = pd.read_csv("smart_meter_data_202602141620.csv", low_memory=False)

print("First 20 createdAt values:")
print(df['createdAt'].head(20).tolist())

print("\nLast 20 createdAt values:")
print(df['createdAt'].tail(20).tolist())

print("\nRandom sample:")
print(df['createdAt'].sample(20).tolist())
