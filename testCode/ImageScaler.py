from PIL import Image
import os

size = (30,30)
originPath = "/Users/font/Desktop/image/"
destPath = "/Users/font/Desktop/image/resized/"
srcImageList = ["dependX.png", "dependY.png", "innerFill.png", "penPair.png", "rubbish.png", "select.png"]
new_color = None
if __name__ == "__main__":
    
    try:
        for i in range(len(srcImageList)):
            srcPath = originPath + srcImageList[i]
            image = Image.open(srcPath)
            resizedImage = image.resize((size[0],size[1]))
            resizedImage.save(destPath+srcImageList[i], quality=95)
    
    except FileNotFoundError:
        os.mkdir(destPath)
        i-=1