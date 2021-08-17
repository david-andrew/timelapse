import sys
import os
import glob
import cv2
import imageio
import pdb
import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

if __name__ == '__main__':
    folder_path = input('Enter path of folder with images to convert:\n')
    image_paths = []
    
    print('Loading images...', end='')
    sys.stdout.flush()
    os.chdir(folder_path)
    for file in glob.glob('*.png'):
        image_paths.append(file)
    
    image_paths = natural_sort(image_paths)
    images = [imageio.imread(image_path) for image_path in image_paths]
    print('Done')

    print('Writing images to video...', end='')
    sys.stdout.flush()
    fps = 60.0
    out = imageio.get_writer('timelapse.mp4', fps=fps)
    for image in images:
        out.append_data(image)
    out.close()
    print('Done')
