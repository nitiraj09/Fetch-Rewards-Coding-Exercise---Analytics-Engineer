import pandas as pd
import json

file_path = "Receipts_beta.csv"
df = pd.read_csv(file_path)
df["rewardsReceiptItemList"] = df["rewardsReceiptItemList"].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
df_exploded = df.explode("rewardsReceiptItemList")
df_expanded = df_exploded.join(pd.json_normalize(df_exploded["rewardsReceiptItemList"], sep="_"), rsuffix="_item")
df_expanded.drop(columns=["rewardsReceiptItemList"], inplace=True)
output_file = "Receipts_final.csv"
df_expanded.to_csv(output_file, index=False)
