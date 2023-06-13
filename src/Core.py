
import numpy 
from PIL import Image
 
def pretreatment(ima : Image, threshold : int):
    # Generate binary image by setting a threshold
    ima = ima.convert('L') # Convert to grayscale picture
    im = numpy.array(ima) # Convert to numpy array
    for i in range(im.shape[0]):  # Convert to 2D
        for j in range(im.shape[1]):
            if im[i, j] > threshold:
                im[i, j] = 0
            else:
                im[i, j] = 1
    return im


ima = Image.open('BPmeter.png') # Read the image
im = pretreatment(ima)
out = []
for i in im:
    count = 0
    count_1 = ''
    for j in i:
        count += 1
        count_1 = count_1+str(j)
        if count % 8 ==0:
            out.append(int(count_1,2))
            count_1=''
cnt = 0
for i in out:
    cnt += 1
    print('0x%02X'%i,end=",")
    if cnt % 16 == 0:
        print(" ")

