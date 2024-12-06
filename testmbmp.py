from microbmp import MicroBMP

im = MicroBMP(240,240,24)
for i in range(240):
    for j in range(240):
        if i == j:
            im[i, j] = 255, 0, 255
im.save('test2.bmp')

im = MicroBMP().load('test1.bmp')
print(im)
im.save("test3.bmp")