import os
import tqdm
import numpy as np
import pandas as pd


STRICT_MAPPING = False
FEATURES = [
    "level", "member", "limited", "compatible", 
    "productive", "syntax_role", "special", 
    "paraphrase", "etymology", "animated", 
    "reference", "semantic_role", "limited_comember", 
    "state", "involvement", "theme_rheme"
]


if __name__ == "__main__":
    langs = pd.read_csv('langs.csv')

    os.chdir("data")
    result = pd.DataFrame()

    for i, lang_name in tqdm.tqdm(enumerate(langs["language"]), total=len(langs["language"])):
        if os.path.isfile(lang_name + ".xls"):
            table = pd.ExcelFile(lang_name + ".xls")
        elif os.path.isfile(lang_name + ".xlsx"):
            table = pd.ExcelFile(lang_name + ".xlsx")
        else:
            print(lang_name, "not found?")
            continue

        for j, strategy in enumerate(table.sheet_names):
            iso = langs["ISO-639-3"][i]
            
            df = pd.read_excel(table, strategy)
            features_indices = df.index[df.iloc[:, 0].isna()].tolist()
            
            columns = []
            vals = []

            h_features = -1
            number = -1
            for h in range(len(df.index)):
                if h < 1:
                    continue
                
                if pd.isna(df.iloc[h, 0]):
                    if h+1 < len(df.index) and pd.isna(df.iloc[h+1, 0]):
                        continue
                    h_features += 1
                    number = 0
                    continue

                number += 1
                columns.append(f"{FEATURES[h_features]}-{number}")
                vals.append(df.iloc[h, 3])
            
            columns.append("region")
            vals.append(langs["Macroarea (у нас)"][i])

            if len(result.columns.tolist()) == 0:
                result = pd.DataFrame(columns=columns)

            try:
                result.loc[f"{iso}-{j+1}"] = vals
            except:
                pass
                # print(f"{iso}-{j+1}")

    os.chdir("..")
    if STRICT_MAPPING:
        result = result.replace({
            "ND": np.NaN, "n/d": np.NaN, "N/D": np.NaN, "ND?": np.NaN, "?": np.NaN, "ND ": np.NaN,
            "IRR": 0, "irr": 0, "irr?": 0, "IRR?": 0, "IRR ": 0, "0?": 0, "0??": 0, 
            "1?": 1, "1??": 1, "1 или ND?": 1, "1? / IRR": 1, "1? ": 1, "n/d-1": 1, "1?? ": 1,
            "prefix": np.NaN, "1/0": np.NaN, "ewü w-ütö(mö)-a sü'na jadö-'da-nñe [1SG 1S-aller-NPST chien avec-NEG-PL' ": np.NaN})
    else:
        result = result.replace({
            "ND": "ND", "n/d": "ND", "N/D": "ND", "ND?": "ND", "?": "ND", "ND ": "ND",
            "IRR": "IRR", "irr": "IRR", "irr?": "IRR", "IRR?": "IRR", "IRR ": "IRR", "0?": 0, "0??": 0, 
            "1?": 1, "1??": 1, "1 или ND?": 1, "1? / IRR": 1, "1? ": 1, "n/d-1": 1, "1?? ": 1,
            "prefix": "ND", "1/0": "ND", "ewü w-ütö(mö)-a sü'na jadö-'da-nñe [1SG 1S-aller-NPST chien avec-NEG-PL' ": "ND"})

    # for column in result.columns:
    #     print(result[column].unique())

    # with open("stats.pkl", "wb") as file:
    #     pickle.dump(result, file)

    if STRICT_MAPPING:
        result.to_csv("stats.csv", na_rep='nan')
    else:
        result.to_csv("stats_soft.csv", na_rep='ND')
