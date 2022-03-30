import numpy as np
import pandas as pd
from sklearn import metrics
from describe import describe
from sklearn.cluster import SpectralClustering


stats_ = pd.read_csv("stats.csv", na_values="nan")
stats = stats_.drop(columns=["Unnamed: 0", "region"])
stats.fillna(0.5, inplace=True)

db = SpectralClustering(n_clusters=4, assign_labels="discretize", random_state=0).fit(stats)
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(stats, labels, metric="hamming"))

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
