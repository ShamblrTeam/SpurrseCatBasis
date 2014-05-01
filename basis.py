import os
import numpy as np
from skimage import io
from sklearn.decomposition import SparsePCA
import glob
import re
from random import shuffle
import time

ns = [2,5,25,100,500,1000]
for n in ns:
	for filename in glob.glob("people/*.jpg"):
		print(filename)
		subject = io.imread(filename,as_grey=True).flatten()

		count = 0
		images = np.ndarray((200*200,0)) # a massive tensor (img#, x, y)
		cats = os.listdir("sparse-cats/")
		shuffle(cats)
		# load all images into image tensor
		for f in cats:
			count += 1
			if count > n:
				break
			try:
				cat = io.imread("sparse-cats/"+f,as_grey=True).flatten()
				cat.shape = (40000,1)
				images = np.append(images, cat, axis=1)
			except:
				count -= 1
				continue
		print("loaded cats...")

		tic = time.clock()
		print("starting learning...")
		pca = SparsePCA(n_components=n,max_iter=1000)
		x = pca.fit_transform(images,subject)
		print("learning done...")
		toc = time.clock()
		print(x)

		out = np.zeros(40000)
		print("starting transform...")
		for i in range(40000):
			for j in range(n):
				#out[i] += (x[i,j])
				out[i] += (images[i,j] * x[i,j])

		out.shape = (200,200)
		print(out)
		name = re.match("people/([a-z]*)_small.jpg",filename).group(1)
		io.imsave("pca/pca_cat_{0}_{1}.jpg".format(n,name),out)
		print(n,name,toc-tic)
