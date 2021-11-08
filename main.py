import os
import imghdr
from PIL import Image


def b64decode(name):
    return


def md5_hash_func(content):
    return
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def main(content):
    # user enters directory
    directory_name = input('Please enter directory (C:/Users/sselt/Documents/blog_demo): ')
    # get list of files in current dir: test: /home/ishaq/PycharmProjects/cfrs_hw
    # path_dir_list = os.listdir(directory)

    # traverse the diretory entered
    for current_directory, child_directories, child_files in os.walk(directory_name):
        # loop through the files in each directory traversed
        for child_file in child_files:
            # for each file, check if it is an image
            image_type = imghdr.what(os.path.join(current_directory, child_file))
            if image_type == 'jpeg' or image_type == 'JPEG':
                # check image for appended data
                print(current_directory, child_file)

                img = Image.open(os.path.join(current_directory, child_file))
                img_exif = img._getexif()
                print(img_exif)

    return


if __name__ == '__main__':
    main('PyCharm')
