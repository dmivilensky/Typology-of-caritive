import numpy as np
import pandas as pd


def pandas_entropy(column, base=2, drop_na=True):
    vc = pd.Series(column).value_counts(normalize=True, sort=False)
    if drop_na:
        vc = vc.dropna()
    return -(vc * np.log(vc)/np.log(base)).sum()


def describe(stats):
    pd.set_option('max_rows', None)

    description = pd.concat([stats.count(), stats.mean(), stats.apply(pandas_entropy, axis=0)], axis=1)
    description.columns = ["count", "mean", "entropy"]
    description = description.sort_values(by="entropy", ascending=False)

    print(description)


if __name__ == "__main__":
    stats = pd.read_csv("stats.csv", na_values="nan")
    describe(stats)
