import pandas as pd

a = pd.read_csv("train_pet.csv")
b = pd.read_csv("val_pet.csv")
merged = pd.concat([a,b])
merged.to_csv("final_train_pet.csv", index=False)