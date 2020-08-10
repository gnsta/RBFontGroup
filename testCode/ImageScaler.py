from PIL import Image
import os

size = (30,30)
originPath = "/Users/sslab/Desktop/image/"
destPath = "/Users/sslab/Desktop/image/resized/"
srcImageList = ["stroke.png"]

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
