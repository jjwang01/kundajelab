import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# assuming that pandas DataFrame is already imported in as "gene_matrix"
# figure out how to convert to numpy array
directory = "/Users/justinwang/Desktop/kundaje/kundajelab"
file_name = "filtered_gene_matrix.csv"

gene_matrix = pd.read_csv("{}/{}".format(directory, file_name), sep='\t')
X = gene_matrix.drop(gene_matrix.columns[[0, 1]], 1)
y = gene_matrix['Gene_Symbol']

# get the top 1000 most variable genes as features to input into PCA
standard_deviations = X.std(axis=1)
X['stdevs'] = standard_deviations
X = X.sort_values(by='stdevs', ascending=0)
features = X[0:1000]
# TODO: figure out how to match y_train and y_test

# standard scaler normalization
sc = StandardScaler()
features = sc.fit_transform(features)

# num_components -> not sure how many dimensions to expect, use Minka's MLE?
pca = PCA(n_components=2)
features_pca = pca.fit_transform(features)
#print(features_pca.shape)

principalDf = pd.DataFrame(data = features_pca, 
	columns = ['principal component 1', 'principal component 2'])

# plot
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize=15)
ax.set_ylabel('Principal Component 2', fontsize=15)
ax.set_title('2 component PCA', fontsize=20)
ax.scatter(principalDf['principal component 1'], principalDf['principal component 2'])
ax.grid()
plt.show()
