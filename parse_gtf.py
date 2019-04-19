import pandas as pd
import re

fo = open('gencode.vM7.annotation.gtf', 'r')
f = fo.readlines()
fo.close()
f = f[25:]
f = [line.strip() for line in f]
gtf = pd.DataFrame(re.split(r'\t|;', line) for line in f)

#gtf = gtf[gtf[1].notnull()]
filtered_gtf = gtf[gtf[2] == 'gene']
filtered_2_gtf = filtered_gtf[filtered_gtf[9] == ' gene_type \"protein_coding\"']

print(filtered_2_gtf.head())
"""
# Input
data_file = "gencode.vM7.annotation.gtf"

# Delimiter
data_file_delimiter = '\t|;'

# The max column count a line in the file could have
largest_column_count = 0

# Loop the data lines
with open(data_file, 'r') as temp_f:
    # Read the lines
    lines = temp_f.readlines()

    for l in lines:
        # Count the column count for the current line
        column_count = len(l.split(data_file_delimiter)) + 1

        # Set the new most column count
        largest_column_count = column_count if largest_column_count < column_count else largest_column_count

# Close file
temp_f.close()

column_names = [i for i in range(0, largest_column_count)]

gtf = pd.read_csv(
    filepath_or_buffer= data_file,
    sep=data_file_delimiter,
    header=None,
    names=column_names,
    skiprows=[i for i in range(25)],
    engine=python)

gtf = gtf[gtf['1'].notnull()]
filtered_gtf = gtf[gtf['2'] == 'gene']
filtered_2_gtf = filtered_gtf[filtered_gtf['9'] == 'gene_type "protein_coding"']

print(filtered_2_gtf.head())
"""
"""
# loop through all rows
for index, row in gtf.iterrows():
	columns = row['attributes'].str.split(';', expand=True)
	gtf.iloc[index] = 



gtf['gene_id', 
	'transcript_id', 
	'gene_type', 
	'others'
	] = gtf['attributes'].str.split(';',expand=True)


print(filtered_gtf.head())
"""
