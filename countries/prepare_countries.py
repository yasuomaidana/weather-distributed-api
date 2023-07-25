import pandas as pd

countries = pd.read_csv("r0411world_utf8.csv", sep='\t')
to_del = [col for col in countries.columns if "jp" in col]
to_del += ['lat', 'lon']
countries.drop(columns=to_del, inplace=True)
countries.to_csv("countries.csv", index=False)
