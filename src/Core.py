
import numpy 
from PIL import Image
 
def pretreatment(ima : Image, threshold : int):
    # Generate binary image by setting a threshold
    ima = ima.convert('L') # Convert to grayscale picture
    im = numpy.array(ima) # Convert to numpy array
    im = numpy.where(im > threshold, 0, 1)
    return im

def processImage(ima : Image, threshold : int = 128):
    # Print the image in the form of bytes
    im = pretreatment(ima, threshold)
    out = []
    for row in im:
        # Traverse each row in the image
        count = 0
        count_1 = ''
        for pix in row:
            count += 1
            count_1 = count_1 + str(pix)
            if count % 8 == 0:
                out.append(int(count_1, 2))
                count_1=''
    cnt = 0
    for num in out:
        cnt += 1
        print('0x%02X' % num, end=",")
        if cnt % 16 == 0:
            print(" ")

if __name__ == '__main__':
    image = Image.open("res/test.png")
    processImage(image, 128)
    