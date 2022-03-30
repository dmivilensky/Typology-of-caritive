import numpy as np
import pandas as pd
from sklearn import metrics
from describe import describe
from sklearn.cluster import DBSCAN

config_1 = {
    "metric": "hamming",
    "fillna": -1,
    "eps": 0.29,
    "min_samples": 2,
    "dtype": float
}

config_2 = {
    "metric": "jaccard",
    "fillna": 1,
    "eps": 0.5,
    "min_samples": 2,
    "dtype": bool
}

def own(a, b):
    distance = 0
    for i in range(len(a)):
        if a[i] != b[i] and a[i] != -1 and b[i] != -1:
            distance += 1
    return distance / len(a)

config_3 = {
    "metric": own,
    "fillna": -1,
    "eps": 0.06,
    "min_samples": 2,
    "dtype": float
}

config = config_3

stats_ = pd.read_csv("stats.csv", na_values="nan")
stats = stats_.drop(columns=["Unnamed: 0", "region"])
stats.fillna(config["fillna"], inplace=True)
stats = stats.astype(config["dtype"])

pairwise = metrics.pairwise_distances(stats, metric=config["metric"])
# print(pairwise)
db = DBSCAN(eps=config["eps"], min_samples=config["min_samples"], metric="precomputed").fit(pairwise)
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(stats, labels, metric=config["metric"]))

# exit()
for label in set(labels):
    if label == -1:
        continue

    stats_group = stats_[labels == label]
    print("Label =", label, "size =", len(stats_group))
    stats_group = stats_group.replace(-1, np.nan)
    describe(stats_group)

    print("Regions:", ", ".join(sorted(set(stats_group["Unnamed: 0"]))))

    print()

if len(stats_[labels == -1]) > 0:
    print("Strange examples")
    print(stats_[labels == -1])
