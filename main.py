import base64
import binascii
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
                # print('..................................................................................................')
                print(child_file)
                for sting in strings(current_image_path):
                    # get sting
                    # check length
                    current_string_valid = None
                    strings_to_test_for_length = []
                    strings_to_test_for_base64 = []
                    tested_strings_and_plain_text = []
                    allowed_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
                               'P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d',
                               'e','f','g','h','i','j','k','l','m','n','o','p','q','r','s',
                               't','u','v','w','x','y','z','/','=', '+', '0', '1', '2', '3',
                               '4', '5', '6', '7', '8', '9']
                    for character in str(sting):
                        if character not in allowed_chars:
                            current_string_valid = False
                            break
                        else:
                            current_string_valid = True

                    if current_string_valid is True:
                        strings_to_test_for_length.append(sting)


                    # get the modulus4
                    for test_string in strings_to_test_for_length:
                        if len(test_string) >= 4:
                            if len(test_string) % 4 != 0:
                                # slice list from begining with remainder
                                strings_to_test_for_base64.append(test_string[len(test_string) % 4:])
                            elif len(test_string) % 4 != 0:
                                strings_to_test_for_base64.append(test_string)


                    # check if is a base64
                    # if yes, decrypt and save

                    # base64_string = base64.b64decode(byte_string)
                    # reversed_string = base64_string.decode('ascii').encode('ascii')

                    # print(byte_string, reversed_string)
                    # print(strings_to_test_for_base64)
                    # for base_64_test_string in strings_to_test_for_base64:
                    #     byte_string = base_64_test_string.encode('ascii')
                        # try:
                        #     if str(base64.b64encode(base64.b64decode(byte_string)).decode('ascii')) == base_64_test_string:
                        #         print(str(base64.b64encode(base64.b64decode(byte_string))), base_64_test_string)
                        #     else:
                        #         continue
                        # except:
                        #     continue

                        # try:
                        #     base64.b64decode(byte_string)
                        #     print('decoded ', base_64_test_string)
                        # except binascii.Error:
                        #     pass



                    file1.writelines(sting)
                    # image = open(f'child_file.txt', 'a')
                    # image.writelines(f'\n\n{sting}')
                file1.close()


                # DECODING FILES
                # image = open(f"{child_file.split('.')[0]}.txt", 'rb')
                # image_read = image.read()
                # print(image_read)
                # fresh_decoded = image_read.decode('latin1')
                # decoded = base64.b64decode(image_read)
                # image_result = open(f"{child_file.split('.')[0]}_decode.txt", 'wb')  # create a writable image and write the decoding result
                # image_result.write(decoded)
                # print(str(decoded))


                # print("Created: %s" % time.ctime(os.path.getctime(os.path.join(current_directory, child_file))))
                # print("Last Modified: %s" % time.ctime(os.path.getmtime(os.path.join(current_directory, child_file))))
                # print("Last Accessed: %s" % time.ctime(os.path.getatime(os.path.join(current_directory, child_file))))

                img.close()
                # print(strings_to_test_for_base64)
                # try:
                #     base64.b64decode(byte_string)
                #     print('decoded ', base_64_test_string)
                # except binascii.Error:
                #     pass

    return


if __name__ == '__main__':
    main('PyCharm')

# find ascii equiv: strings jpg01
# identify base64
# strings
# echo 'RGVzaWduZWRieUZyZWVwaWs=' | base64 -d
# sys allows to run sytem command
