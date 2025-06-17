import pandas as pd
scrap= pd.read_html('https://en.wikipedia.org/wiki/Al_Ahly_SC')
print (scrap)
for i, table in enumerate(scrap):
	print ('---')
	print(i)
	print(table)
print (scrap[23])
df= scrap[23]
df.to_csv('league', index=False)
dffile=pd.read_csv('league')
print(dffile)
