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
    final_image_details = {}

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
                # if image_has_appended_data:
                #     images_ascii_representation[child_file.split('.')[0]] = current_image_ascii_lines[:-1]
                # else:
                #     images_ascii_representation[child_file.split('.')[0]] = current_image_ascii_lines

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
                # new_file_created_time = time.ctime(os.path.getctime(f"{child_file.split('.')[0]}.jpg"))
                # new_file_last_modified = time.ctime(os.path.getmtime(f"{child_file.split('.')[0]}.jpg"))
                # new_file_last_accessed = time.ctime(os.path.getatime(f"{child_file.split('.')[0]}.jpg"))
                final_image_details[child_file.split('.')[0]] = {
                    'filename': f"{child_file.split('.')[0]}.jpg",
                    'hash': md5_hash_func(current_image_path),
                    'timestamps': {
                        'created': time.ctime(os.path.getctime(f"{child_file.split('.')[0]}.jpg")),
                        'last_modified': time.ctime(os.path.getmtime(f"{child_file.split('.')[0]}.jpg")),
                        'last_accessed': time.ctime(os.path.getatime(f"{child_file.split('.')[0]}.jpg")),
                    }
                }

    # get messages
    for encoded_message in cleaned_images_trailer.keys():
        base64_message = cleaned_images_trailer.get(encoded_message)
        decoded_message = b64decode(base64_message)
        decoded_messages[encoded_message] = decoded_message

        # update final table with message plaintext
        final_image_details[encoded_message]['plaintext message'] = decoded_message.decode('ascii')
        final_image_details[encoded_message]['base64 encoded message'] = base64_message

    # output file
    with open('output/output.txt', "w") as output_file:
        for record in final_image_details.keys():
            for detail in final_image_details[record].keys():
                try:
                    output_file.writelines([detail, ': ', final_image_details[record][detail], '\n'])
                except TypeError:
                    for sub_detail in final_image_details[record][detail].keys():
                        output_file.writelines([sub_detail, ': ', final_image_details[record][detail][sub_detail], '\n'])
                    pass
            output_file.writelines('\n\n')


if __name__ == '__main__':
    main('PyCharm')
