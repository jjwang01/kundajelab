import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# assuming that pandas DataFrame is already imported in as "gene_matrix"
# figure out how to convert to numpy array
directory = "/Users/justinwang/Desktop/kundaje/kundajelab"
file_name = "filtered_gene_matrix.csv"

gene_matrix = pd.read_csv("{}/{}".format(directory, file_name), sep='\t')
X = gene_matrix.drop(gene_matrix.columns[[0, 1]], 1)

# get the top 1000 most variable genes as features to input into PCA
stdevs = X.std(axis=1).tolist()
X['stdevs'] = stdevs 
X = X.sort_values(by='stdevs', axis=0, ascending=False)
new_X = X[0:1000]
del new_X['stdevs']

# swap rows and columns so that rows contain cells (a point on the plot) and columns contain genes (features)
new_X = new_X.T

# standard scaler normalization
sc = StandardScaler()
scaled = sc.fit_transform(new_X)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(scaled)
principalDf = pd.DataFrame(index=new_X.index, data = principalComponents, 
	columns = ['principal component 1', 'principal component 2'])

colors = pd.read_csv('pca_colors.csv', sep='\t', index_col=0)
principalDf['color'] = colors['color']
principalDf['cell type'] = colors['cell type']

# matplotlib
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
ax.scatter(x=principalDf['principal component 1'], 
	y=principalDf['principal component 2'], 
	c=principalDf['color'], 
	label=principalDf['cell type'])
ax.grid()

red_dot = mpatches.Patch(color='xkcd:purple', label='Stroma')
grey_dot = mpatches.Patch(color='xkcd:grey', label='Stem')
orange_dot = mpatches.Patch(color='xkcd:orange', label='abT')
green_dot = mpatches.Patch(color='xkcd:green', label='ILC')
pink_dot = mpatches.Patch(color='xkcd:hot pink', label='MF/GN')
yellow_dot = mpatches.Patch(color='xkcd:yellow', label='B')
blue_dot = mpatches.Patch(color='xkcd:blue', label='cdT')
red_dot = mpatches.Patch(color='xkcd:red', label='Act T')
black_dot = mpatches.Patch(color='xkcd:black', label='DC')
plt.legend(handles=[red_dot, grey_dot, orange_dot, green_dot, pink_dot, yellow_dot, blue_dot, red_dot, black_dot])


plt.show()
"""
# seaborn
plt.figure(figsize=(16,10))
sns.scatterplot(
	x = "principal component 1", y = "principal component 2",
	#hue = "y",
	#palette = sns.color_palette("hls", 10),
	data = principalDf,
	legend = "full",
	alpha = 0.3
)
plt.show()

# plotly w/ matplotlib

plotly_fig = tls.mpl_to_plotly(fig)
py.iplot(plotly_fig, filename = 'gene-matrix-pca')
"""
