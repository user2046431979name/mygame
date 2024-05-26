from PIL import Image

path = 'images/guns/katana_ultimate_slash.png'

img = Image.open(path)

mimg = img.resize((150,20))
# mimg = img.rotate(2)


mimg.save(path)
