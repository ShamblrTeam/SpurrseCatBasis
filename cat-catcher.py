import cStringIO
import urllib
import os
from PIL import Image, ImageOps
import pytumblr
import numpy as np

# fill this in first
tumblr = pytumblr.TumblrRestClient(
	'',
	'',
	'',
	''
)

def resize(image, size):
	image.thumbnail(size, Image.ANTIALIAS)

	thumb = ImageOps.fit(image, size, Image.ANTIALIAS, (0.5, 0.5))
	return thumb

def normalize(img):
	"""
	Linear normalization
	http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
	"""
	arr=np.array(np.asarray(img).astype('float'))

	# Do not touch the alpha channel
	for i in range(3):
		minval = arr[...,i].min()
		maxval = arr[...,i].max()
		if minval != maxval:
			arr[...,i] -= minval
			arr[...,i] *= (255.0/(maxval-minval))
	
	new_img = Image.fromarray(arr.astype('uint8'),'RGBA')
	return new_img

def main():
	count = 0
	limit=100
	target=1000
	size=(200,200)
	debugging = True
	seen = []

	while count < target:
		posts = tumblr.tagged("cat",limit=limit)
		for post in posts:
			if post["id"] in seen:
				continue
			if post["type"] == u'photo':
				for photo in post["photos"]:
					try:
						url = photo["original_size"]["url"]
						f = cStringIO.StringIO(urllib.urlopen(url).read())
						img = Image.open(f).convert("RGBA")
						img.save("big-cats/"+str(post["id"])+".jpg", "JPEG")
						img = resize(img,size)
						img = normalize(img)
						img.save("cats/"+str(post["id"])+".jpg", "JPEG")
						count += 1
						seen.append(post["id"])
						print("meow")
					except (KeyboardInterrupt, SystemExit):
						print(count)
						raise
					except:
						print("hiss")
						if debugging:
							raise
						continue
	print(count)
if __name__ == "__main__":
	main()
