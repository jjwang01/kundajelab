import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import seaborn as sns
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
new_X = sc.fit_transform(new_X)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(new_X)
principalDf = pd.DataFrame(data = principalComponents, 
	columns = ['principal component 1', 'principal component 2'])

# TODO: label all the points separately
colors = pd.read_csv('pca_colors.csv', sep='\t', )
colors

# matplotlib
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
ax.scatter(principalDf['principal component 1'], principalDf['principal component 2'])
ax.grid()

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
"""
plotly_fig = tls.mpl_to_plotly(fig)
py.iplot(plotly_fig, filename = 'gene-matrix-pca')
"""
