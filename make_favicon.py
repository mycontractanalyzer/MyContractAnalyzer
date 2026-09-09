from PIL import Image, ImageDraw
im = Image.open('web/logo.png').convert('RGBA')
w, h = im.size
s = min(w, h)
im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
mask = Image.new('L', (s, s), 0)
ImageDraw.Draw(mask).ellipse((0, 0, s, s), fill=255)
im.putalpha(mask)
im.save('web/favicon.png')
print('FAVICON OK', im.size)