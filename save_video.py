import sys
import os
import glob
import imageio
import re
import numpy as np
import time

def main():
    folder_path = input('Enter path of folder with images to convert:\n')
    out_path = f'output/timelapse_{time.time()}.mp4'
    image_paths = []
    fps = 60.0
    out = imageio.get_writer(out_path, fps=fps)
    
    status = 'Converting images to video...'
    print_percent(status)

    #save the starting path, and move to the path of the images
    #load all the images (and apply a 90 deg rotation b/c my camera is sideways) and write to video
    # original_path = os.getcwd()
    # os.chdir(folder_path)
    # for file in glob.glob('*.png'):
    #     image_paths.append(file)
    # os.chdir(original_path)
    image_paths = get_image_paths(folder_path)
    image_paths = natural_sort(image_paths)

    for i, image_path in enumerate(image_paths):
        try:
            image = imageio.imread(image_path)
        except ValueError as e:
            print(f'\nError loading image {image_path}')
            print(e)
            continue
        image = np.rot90(image)
        out.append_data(image)

        print_percent(status, i / len(image_paths) * 100)
    out.close()
    print_percent(status)
    print('Done     ')


def get_image_paths(folder_path):
    image_paths = []
    for file in glob.glob(os.path.join(folder_path, '*.png')):
        image_paths.append(file)
    return image_paths

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


def print_percent(string, percent=None):
    sys.stdout.write(f'\r{string}')
    if percent is not None:
        sys.stdout.write(f'[{percent:.2f}%]')
    sys.stdout.flush()
    pass


if __name__ == '__main__':
    main()
