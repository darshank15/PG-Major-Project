import os
import pandas as pd

files = os.listdir("./architecture")

data = []

for f in files:
	tmp = []
	tmp.append(f)
	tmp.append("architecture")
	data.append(tmp)

my_df = pd.DataFrame(data, columns=["post_id","topic"])
my_df.to_csv('train_architecture.csv', index=False)
