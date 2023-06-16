
import numpy 
from PIL import Image
 
def pretreatment(ima : Image, threshold : int = 128):
    # Generate binary image by setting a threshold
    ima = ima.convert('L') # Convert to grayscale picture
    im = numpy.array(ima) # Convert to numpy array
    im = numpy.where(im > threshold, 0, 1)
    return im

def numpy2image(im_np : numpy.ndarray, mode='1'):
    # Convert binaray numpy array to pil image
    # https://stackoverflow.com/questions/50134468/convert-boolean-numpy-array-to-pillow-image
    size = im_np.shape[::-1]
    databytes = numpy.packbits(im_np, axis=1)
    return Image.frombytes(mode='1', size=size, data=databytes)

def processImage(ima : Image, threshold : int = 128, sep : str = ", ", line_break_num : int = 16):
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
    out_str = ""
    for num in out:
        cnt += 1
        out_str += '0x%02X' % num
        out_str += sep
        if cnt % line_break_num == 0:
            out_str+='\n'
    out_str = out_str.strip()
    return out_str

if __name__ == '__main__':
    image = Image.open("res/test.png")
    ret = processImage(image, 128)
    print(ret)
    