import sys
import os
import glob
import imageio
import re
import numpy as np

def main():
    folder_path = input('Enter path of folder with images to convert:\n')
    image_paths = []
    
    status = 'Loading images...'
    print_percent(status)

    os.chdir(folder_path)
    for file in glob.glob('*.png'):
        image_paths.append(file)
    
    image_paths = natural_sort(image_paths)
    images = []
    for i, image_path in enumerate(image_paths):
        image = imageio.imread(image_path)
        image = np.rot90(image)
        images.append(image)
        print_percent(status, i / len(image_paths) * 100)
    print_percent(status)
    print('Done    ')

    status = 'Writing images to video...'
    print_percent(status)
    fps = 60.0
    out = imageio.get_writer('timelapse.mp4', fps=fps)
    for i, image in enumerate(images):
        out.append_data(image)
        print_percent(status, i / len(images) * 100)
    out.close()
    print_percent(status)
    print('Done    ')


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
