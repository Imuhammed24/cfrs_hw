import base64
import hashlib
import os
import string
from hashlib import md5
import time
import PIL
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from exif import Image as ExifImage


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


def b64decode(encoded_message):
    encoded_message.encode('ascii')
    _decoded_message = base64.b64decode(encoded_message)
    _decoded_message.decode('ascii')
    return _decoded_message


def md5_hash_func(image_directory):
    with open(image_directory, "rb") as image_file:
        # read file as bytes
        image_in_bytes = image_file.read()
        readable_hash = hashlib.md5(image_in_bytes).hexdigest()
    return readable_hash


def main(content):
    # user enters directory
    directory_name = input('Please enter directory (C:/Users/sselt/Documents/blog_demo): ')
    all_images_trailer = []
    cleaned_images_trailer = {}
    decoded_messages = {}
    all_images_timestamps = {}
    images_ascii_representation = {}
    md5_hashes_of_image = {}

    # traverse the directory entered
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
                image_has_appended_data = False

                current_image_path = os.path.join(current_directory, child_file)
                print(child_file)
                current_image_ascii_lines = [line for line in strings(current_image_path)]
                current_image_ascii_trailer = current_image_ascii_lines[-1]

                current_string_valid = None
                allowed_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                                 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                                 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                                 't', 'u', 'v', 'w', 'x', 'y', 'z', '/', '=', '+', '0', '1', '2', '3',
                                 '4', '5', '6', '7', '8', '9']
                for character in str(current_image_ascii_trailer):
                    if character not in allowed_chars:
                        current_string_valid = False
                        break
                    else:
                        current_string_valid = True

                if current_string_valid:
                    if len(current_image_ascii_trailer) >= 4:
                        if len(current_image_ascii_trailer) % 4 != 0:
                            image_has_appended_data = True
                            if not cleaned_images_trailer.get(child_file.split('.')[0]):
                                cleaned_images_trailer[child_file.split('.')[0]] = current_image_ascii_trailer[
                                                                                   len(current_image_ascii_trailer) % 4:]
                        elif len(current_image_ascii_trailer) % 4 == 0:
                            image_has_appended_data = True
                            if not cleaned_images_trailer.get(child_file.split('.')[0]):
                                cleaned_images_trailer[child_file.split('.')[0]] = current_image_ascii_trailer

                # get images timestamps
                all_images_timestamps[child_file.split('.')[0]] = {
                    'created': time.ctime(os.path.getctime(os.path.join(current_directory, child_file))),
                    'last_modified': time.ctime(os.path.getmtime(os.path.join(current_directory, child_file))),
                    'last_accessed': time.ctime(os.path.getatime(os.path.join(current_directory, child_file))),
                }

                # save image ascii characters
                if image_has_appended_data:
                    images_ascii_representation[child_file.split('.')[0]] = current_image_ascii_lines[:-1]
                else:
                    images_ascii_representation[child_file.split('.')[0]] = current_image_ascii_lines

                # create image with
                with open(current_image_path, "rb") as file:
                    # lines = file.readline()
                    with open(f"{child_file.split('.')[0]}.jpg", "wb") as new_file:
                        # check if the image has appended data
                        if image_has_appended_data:
                            new_file.writelines([line for line in file.readlines()[:-1]])
                        else:
                            new_file.writelines([line for line in file.readlines()])

                # get md5 hashes of images
                md5_hashes_of_image[child_file.split('.')[0]] = md5_hash_func(current_image_path)

    # get messages
    for encoded_message in cleaned_images_trailer.keys():
        base64_message = cleaned_images_trailer.get(encoded_message)
        decoded_message = b64decode(base64_message)
        decoded_messages[encoded_message] = decoded_message

    print(md5_hashes_of_image)

    # get the modulus4
    # for test_string in strings_to_test_for_length:
    #     if len(test_string) >= 4:
    #         if len(test_string) % 4 != 0:
    #             slice list from begining with remainder
    #             strings_to_test_for_base64.append(test_string[len(test_string) % 4:])
    # elif len(test_string) % 4 != 0:
    #     strings_to_test_for_base64.append(test_string)

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

    # file1.writelines(sting)
    # image = open(f'child_file.txt', 'a')
    # image.writelines(f'\n\n{sting}')
    # file1.close()
    # print(strings_to_test_for_length)

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

    # img.close()
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
