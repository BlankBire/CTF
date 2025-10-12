from PIL import Image
img1 = Image.open("flag_7ae18c704272532658c10b5faad06d74.png").convert("RGB")
img2 = Image.open("lemur_ed66878c338e662d3473f0d98eedbd0d.png").convert("RGB")
w, h = min(img1.width, img2.width), min(img1.height, img2.height)
img1, img2 = img1.crop((0, 0, w, h)), img2.crop((0, 0, w, h))
result = Image.new("RGB", (w, h))
pix1, pix2, pix = img1.load(), img2.load(), result.load()
for x in range(w):
    for y in range(h):
        r1, g1, b1 = pix1[x, y]
        r2, g2, b2 = pix2[x, y]
        pix[x, y] = (r1 ^ r2, g1 ^ g2, b1 ^ b2)
result.save("xor_output.png")