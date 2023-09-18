from PIL import Image
import pytesseract
import numpy as np
import os
 
path_dir = 'example_images'


def get_files() -> list:
    files = []
    for path in os.listdir(path_dir):
        file_name = os.path.join(path_dir, path)
        if os.path.isfile(file_name):
            files.append(file_name)

    return files


def get_file_name(relative_file_path: str) -> str:
    return relative_file_path.replace(path_dir, '')


def convert_img_to_grey() -> str:
    im_gray = np.array(Image.open(file).convert('L'))
    filename = get_file_name(file)
    path_img_grey = path_dir + filename + '_grey.png'
    Image.fromarray(np.uint8(im_gray)).save(path_img_grey)

    return path_img_grey


def filter_value(value: str) -> str:
    if value.find(' 1 ') >= 0:
        value = value.replace(' 1 ', '')
    if value.find(' 10 ') >= 0:
        value = value.replace(' 10 ', '')
    if value.find('#€') >= 0:
        value = value.replace('#€', '')
    if value.find('01 ') >= 0:
        value = value.replace('01 ', '')
    if value.find('10( ') >= 0:
        value = value.replace('10( ', '')
    if value.find('K') >= 0:
        value = value.replace('K', '')
    if value.find('#') >= 0:
        value = value.replace('#', '')
    if value.find(' ') >= 0:
        value = value.replace(' ', '')
    if value.find('...'):
        value = value.replace('...', ' ')
    return value


def remove_empty_lines(data: list) -> list:
    for index, value in enumerate(data):
        if value == '':
            data.pop(index)
    return data


def format_data(data: list) -> list:
    for index, value in enumerate(data):
        value = filter_value(value).split('lotde')
        data[index] = value

    return data


for file in get_files():
    grey_img = convert_img_to_grey()

    lines = pytesseract.image_to_string(Image.open(grey_img))
    data = lines.splitlines()
    data = remove_empty_lines(data)
    data = format_data(data)

    print(data)
    os.remove(grey_img)
