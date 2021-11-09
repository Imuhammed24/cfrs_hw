import base64
import os
import string
from hashlib import md5
import imghdr
import time

import PIL
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from exif import Image as ExifImage


def convert_image_to_ascii(image_directory):
    import sys
    from PIL import Image

    # pass the image as command line argument
    # image_path = sys.argv[1]
    img = Image.open(image_directory)

    # resize the image
    # width, height = img.size
    # aspect_ratio = height / width
    # new_width = 120
    # new_height = aspect_ratio * new_width * 0.55
    # img = img.resize((new_width, int(new_height)))
    # new size of image
    # print(img.size)

    # convert image to greyscale format
    # img = img.convert('L')

    pixels = img.getdata()

    # replace each pixel with a character from array
    chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."]
    new_pixels = [chars[pixel // 25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    print(ascii_image, '\n\n\n\n')
    return ascii_image


def strings(filename, minimum=4):
    with open(filename, errors="ignore") as f:  # Python 3.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= minimum:
                yield result
            result = ""
        if len(result) >= minimum:  # catch result at EOF
            yield result


def b64decode(name):
    return


def md5_hash_func(content):
    return
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def main(content):
    # user enters directory
    directory_name = input('Please enter directory (C:/Users/sselt/Documents/blog_demo): ')
    # get list of files in current dir: test: /home/ishaq/PycharmProjects/cfrs_hw

    # traverse the diretory entered
    for current_directory, child_directories, child_files in os.walk(directory_name):
        # loop through the files in each directory traversed
        for child_file in child_files:
            # for each file, check if it is an image
            try:
                img = Image.open(os.path.join(current_directory, child_file))
                image_type = img.format
            except PIL.UnidentifiedImageError:
                image_type = None

            if image_type == 'jpeg' or image_type == 'JPEG':
                # check image for appended data
                file1 = open(f"{child_file.split('.')[0]}.txt", "a")

                current_image_path = os.path.join(current_directory, child_file)
                print(child_file)
                for sting in strings(current_image_path):
                    file1.writelines(sting)
                file1.close()


                # DECODING FILES
                image = open(f"{child_file.split('.')[0]}.txt", 'r')
                image_read = image.read()
                # print(image_read)
                fresh_decoded = image_read.encode('ascii')
                decoded = base64.b64decode(image_read)
                image_result = open(f"{child_file.split('.')[0]}_decode.txt", 'w')  # create a writable image and write the decoding result
                image_result.write(decoded.decode('iso8859_2'))


                # print("Created: %s" % time.ctime(os.path.getctime(os.path.join(current_directory, child_file))))
                # print("Last Modified: %s" % time.ctime(os.path.getmtime(os.path.join(current_directory, child_file))))
                # print("Last Accessed: %s" % time.ctime(os.path.getatime(os.path.join(current_directory, child_file))))

                img.close()
    return


if __name__ == '__main__':
    main('PyCharm')

# find ascii equiv: strings jpg01
# identify base64
# strings
# echo 'RGVzaWduZWRieUZyZWVwaWs=' | base64 -d
# sys allows to run sytem command
