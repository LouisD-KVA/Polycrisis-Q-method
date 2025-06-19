import pandas as pd 
import itertools
from upsetplot import UpSet, from_indicators
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# 1. Load data
data = [
    [1, "Definition", "We are not in ‘the' polycrisis as much as a polycrisis.", -3, 1, -3, -3],
    [2, "Definition", "The world is facing multiple polycrises.", -1, 2, -3, -3],
    [3, "Definition", "The list of crises that make up the current polycrisis is clear.", -1, -3, -3, -4],
    [4, "Definition", "The polycrisis concept captures the complexity of the world.", 2, -2, 3, -2],
    [5, "Drivers", "It is possible to identify the main drivers of the polycrisis.", 2, -1, 1, -2],
    [6, "Drivers", "The polycrisis is the product of human interconnectivity.", 1, 4, 0, -2],
    [7, "Drivers", "A phenomenon underlying the polycrisis is an accumulation of wears and tears.", 2, 2, -2, 2],
    [8, "Drivers", "A phenomenon underlying the polycrisis is the apparition of shocks", 0, 4, -1, 0],
    [9, "Drivers", "The polycrisis is rooted in a geopolitical order constructed by Western colonialism.", 3, -3, -2, 3],
    [10, "Drivers", "A phenomenon underlying the polycrisis is capitalism.", 4, -1, -2, 4],
    [11, "Drivers", "Hyperspecialisation of knowledge is a driving force behind the polycrisis", -2, -3, 1, 1],
    [12, "Cross-scale dynamics", "It is possible to identify the dynamics of a polycrisis.", 1, 2, 1, 0],
    [13, "Cross-scale dynamics", "The polycrisis evolves along different temporal scales.", 4, 3, 4, 3],
    [14, "Cross-scale dynamics", "A polycrisis evolves along different spatial scales.", 3, 4, 2, 4],
    [15, "Cross-scale dynamics", "The polycrisis is here to stay.", 3, -2, 2, -3],
    [16, "Cross-scale dynamics", "The crises are clearly connected.", 4, 3, -3, 2],
    [17, "Cross-scale dynamics", "The polycrisis is unpredictable.", -2, 0, 0, 1],
    [18, "Impacts", "Polycrisis disturbs more severely the Global North than the Global South.", -4, -4, -4, -4],
    [19, "Impacts", "Cooperation will become increasingly regional as the polycrisis develops.", -2, -2, -1, 2],
    [20, "Impacts", "The polycrisis is likely to change how time is thought of", -1, -3, 1, -3],
    [21, "Responses", "A polycrisis is also a source of opportunity", -1, 2, 2, 3],
    [22, "Responses", "Certain responses reinforce the polycrisis", 2, 3, 3, 4],
    [23, "Responses", "Socio-technical barriers hamper the ability to cope with the polycrisis", 0, 1, 3, 2],
    [24, "Responses", "Responses must be local.", -3, -4, -2, -1],
    [25, "Responses", "Responses must be coordinated.", 3, 3, 4, 0],
    [26, "Responses", "A strong intergovernmental institution is needed to manage the polycrisis.", 1, -2, 3, -1],
    [27, "Use", "The concept is a buzzword", -4, -1, -4, -1],
    [28, "Use", "The concept is counter productive.", -4, -4, -4, -2],
    [29, "Use", "Even ill defined, the concept is useful", 1, 0, -1, -4],
    [30, "Understanding", "The integration of indigenous knowledge is a necessary element in understanding the polycrisis.", 0, -1, 2, 3],
    [31, "Understanding", "The current state of knowledge does not allow us to understand the state of the polycrisis", -3, 1, -1, -1],
    [32, "Understanding", "Current methods are inadequate in explaining the mechanisms of the polycrisis", -3, 1, 0, 1],
    [33, "Understanding", "Understanding the polycrisis is beyond what is individually possible.", -2, 0, 4, 1],
]

# 2. Define full factor names with labels
factor_map = {
    "F1": "F1 - Capitalist interdependence",
    "F2": "F2 - Networked shocks",
    "F3": "F3 - Multilateral governance",
    "F4": "F4 - Critical colonial"
}

# 3. Create DataFrame with renamed columns
df = pd.DataFrame(data, columns=[
    "ID", "Dimension", "Statement",
    factor_map["F1"],
    factor_map["F2"],
    factor_map["F3"],
    factor_map["F4"]
])

# 4. Define consensus logic
def is_consensus_group(scores):
    all_agree = all(score >= 3 for score in scores)
    all_disagree = all(score <= -3 for score in scores)
    return (all_agree or all_disagree) and (max(scores) - min(scores) <= 1)

# 5. Identify consensus statements
def get_consensus_statements(df, factors):
    results = []
    for r in range(2, len(factors) + 1):
        for combo in itertools.combinations(factors, r):
            for _, row in df.iterrows():
                scores = [row[f] for f in combo]
                if is_consensus_group(scores):
                    results.append({
                        "ID": row["ID"],
                        "Statement": row["Statement"],
                        "Factors": combo
                    })
    return pd.DataFrame(results)

factors = list(factor_map.values())
consensus_df = get_consensus_statements(df, factors)

# 6. Build participation matrix
base = consensus_df.drop(columns="Factors").drop_duplicates().reset_index(drop=True)
for f in factors:
    base[f] = base["ID"].isin(
        consensus_df[consensus_df["Factors"].apply(lambda x: f in x)]["ID"]
    ).astype(bool)

# 7. Prepare data for UpSet plot
indicator_df = from_indicators(factors, base.set_index("Statement")[factors].astype(bool))

# 8. Plot
plt.figure(figsize=(12, 7))
UpSet(
    indicator_df,
    show_counts=True,
    sort_by="cardinality",
    sort_categories_by="cardinality"
).plot()

plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.savefig("upset_plot.png", dpi=500, bbox_inches="tight")
plt.show()
