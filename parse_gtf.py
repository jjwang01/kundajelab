import os
import gzip
import pandas as pd
import re
import shutil

# predefine file locations, folders
out_dir = "/Users/justinwang/Desktop/kundaje/kundajelab"
file_name = "gencode.vM7.annotation.gtf.gz"
file_url = "ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M7/gencode.vM7.annotation.gtf.gz"

# run code here
download_cmd = " wget {} -O {}/{}".format(file_url, out_dir, file_name)

try:
	gtf = open("{}/{}".format(out_dir, file_name))
	print('found')
except FileNotFoundError:
	print('not found')
	os.system(download_cmd)

f = []
with gzip.open("{}/{}".format(out_dir, file_name)) as f_unz:
	f = f_unz.readlines()
	f_unz.close()

f = f[25:]
f = [line.strip() for line in f]
f = [line.decode("utf-8") for line in f]
gtf = pd.DataFrame(re.split(r'\t|;', line) for line in f)

filtered_gtf = gtf[gtf[2] == 'gene']
filtered_gtf = filtered_gtf[filtered_gtf[9] == ' gene_type \"protein_coding\"']
print(filtered_gtf.head())

# import the gene matrix file
gene_matrix_name = "GSE109125_Gene_count_table.csv"
gene_matrix_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE109125"

# run code here
download_cmd = " wget {} -O {}/{}".format(gene_matrix_url, out_dir, gene_matrix_name)

try:
	gtf = open("{}/{}".format(out_dir, gene_matrix_name))
	print('found')
except FileNotFoundError:
	print('not found')
	os.system(download_cmd)

# header is implicitly the first line of the file
gene_matrix = pd.read_csv("{}/{}".format(out_dir, gene_matrix_name))
print(gene_matrix.head())

gene_matrix_names = set(gene_matrix["Gene_Symbol"].tolist())
gtf_names = []
# gene_names are formatted like "gene_name "...""
for value in filtered_gtf[11].tolist():
    gtf_names.append(value[12:-1])
gtf_names = set(gtf_names)

intersect = set.intersection(gene_matrix_names, gtf_names)
filtered_gene_matrix = gene_matrix[gene_matrix["Gene_Symbol"].isin(intersect)]
print(filtered_gene_matrix.head())

# should be 22032 rows, got 21541
filtered_gene_matrix.to_csv("{}/filtered_gene_matrix.csv".format(out_dir), sep="\t")
# use gzip to compress the file
with open("{}/filtered_gene_matrix.csv".format(out_dir), 'rb') as f_in:
    with gzip.open("{}/filtered_gene_matrix.csv.gz".format(out_dir), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
