from pyfaidx import Fasta
import numpy as np

def generator(chrm_name, coords):
	def sequenceLoader(chrm_name, start, end):
		filename = '/mnt/data/annotations/by_release/hg19/male.hg19.fa'
		chrms = Fasta(filename)

		# TODO: prints out a string of N's as opposed to ACGT
		return chrms[chrm_name][start:end].seq

	def oneHotEncoder(chrm_name, start, end):
		sequence = sequenceLoader(chrm_name, start, end)
		
		# build a numpy array of dimensions (1, seqlen, 4)
		one_hot_encoded = np.zeros((1, end - start, 4))
		for i in range(end - start):
			# alphabetical ordering
			if sequence[i] == 'A':
				one_hot_encoded[0][i][0] = 1
			elif sequence[i] == 'C':
				one_hot_encoded[0][i][1] = 1
			elif sequence[i] == 'G':
				one_hot_encoded[0][i][2] = 1
			elif sequence[i] == 'T':
				one_hot_encoded[0][i][3] = 1
		return one_hot_encoded

	for coord in coords:
		yield oneHotEncoder(chrm_name, coord[0], coord[1])

coords = [(837429,847429)] 
gen = generator('chr11', coords)
for i in range(len(coords)):
	print(next(gen))	 
