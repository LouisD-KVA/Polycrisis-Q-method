import pandas as pd

# Your original data
data = {
    "Factor 1": [27,20,19,8,9,15,11,18,6,1,26,14,3,7,5,2,25,33,23,22,21,10,16,28,4,13,31,32,12,17,30,29,24],
    "Factor 2": [14,11,27,23,19,3,9,1,30,22,29,8,5,2,25,4,16,33,26,28,10,6,13,31,7,24,21,32,17,20,12,15,18],
    "Factor 3": [27,28,30,6,15,16,26,21,24,25,13,14,3,10,9,29,17,32,22,12,8,7,5,23,1,4,31,33,20,11,19,18,2],
    "Factor 4": [30,28,32,26,23,25,10,16,5,3,13,18,4,1,29,9,14,33,11,27,6,2,8,19,17,22,20,24,31,7,21,15,12]
}

df = pd.DataFrame(data)

# Normalization function (-4 to +4)
def normalize_custom_range(series, min_val=-4, max_val=4):
    ranks = series.rank(method='min', ascending=True)
    normalized = max_val - ((ranks - 1) / (ranks.max() - 1)) * (max_val - min_val)
    return normalized.round(2)

# Apply to all columns
normalized_df = df.apply(normalize_custom_range)

# Save to CSV
normalized_df.to_csv("normalized_rank_table_-4_to_4.csv", index=False)

print(normalized_df)
