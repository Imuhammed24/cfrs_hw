import datetime
startTime = datetime.datetime.now()
import base64
import hashlib
import os
import string
import time
import PIL
from PIL import Image


# Function to read ascii representation of images
def strings(filename, minimum=4):
    with open(filename, errors="ignore") as image_file:
        result = ""
        for c in image_file.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= minimum:
                yield result
            result = ""
        if len(result) >= minimum:  # catch result at EOF
            yield result


# function that accepts base64 encoded strings and decodes it
def hw64decode(encoded_message):
    # encode message using ascii format
    encoded_message.encode('ascii')
    _decoded_message = base64.b64decode(encoded_message)
    return _decoded_message.decode('ascii')


# function that accepts an image path and returns
def sha256_hash_func(image_directory):
    with open(image_directory, "rb") as image_file:
        # read file as bytes
        image_in_bytes = image_file.read()
        readable_hash = hashlib.md5(image_in_bytes).hexdigest()
    return readable_hash


def main(content):
    # user enters directory
    directory_name = input('Please enter directory (C:/Users/sselt/Documents/blog_demo): ')
    if os.path.exists(directory_name):
        cleaned_images_trailer = {}
        decoded_messages = {}
        all_images_timestamps = {}
        final_image_details = {}

        # traverse the directory entered
        for current_directory, child_directories, child_files in os.walk(directory_name):
            # loop through the files in each directory traversed
            for child_file in child_files:
                # Check if each file is an image
                try:
                    img = Image.open(os.path.join(current_directory, child_file))
                    image_type = img.format
                except (PIL.UnidentifiedImageError, PermissionError):
                    image_type = None

                if image_type == 'jpeg' or image_type == 'JPEG':
                    # variable that determines if image has appended data
                    image_has_appended_data = False
                    # path for file currently being looped through
                    current_image_path = os.path.join(current_directory, child_file)
                    # variable that holds the ascii code representation for current image
                    current_image_ascii_lines = [line for line in strings(current_image_path)]
                    # variable that holds the last portion of the image ascii representation
                    current_image_ascii_trailer = current_image_ascii_lines[-1]

                    # variable that determines if the current image ascii trailer has an encoded base64 message
                    current_string_valid = None
                    # variable that holds all base64 allowed characters
                    allowed_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                                     'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                                     'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                                     't', 'u', 'v', 'w', 'x', 'y', 'z', '/', '=', '+', '0', '1', '2', '3',
                                     '4', '5', '6', '7', '8', '9']
                    for character in str(current_image_ascii_trailer):
                        # check if the characters of the image ascii trailer contains valid base64 characters
                        if character not in allowed_chars:
                            current_string_valid = False
                            break
                        else:
                            current_string_valid = True

                    # if the current ascii trailer contains valid base64 characters
                    if current_string_valid:
                        # ensure length is greater than 4
                        if len(current_image_ascii_trailer) >= 4:
                            # assume there is an appended data since the ascii string meets encoded base 64 requirements
                            if len(current_image_ascii_trailer) % 4 != 0:
                                image_has_appended_data = True
                                if not cleaned_images_trailer.get(child_file.split('.')[0]):
                                    # slice the length of the string so it's modulus of 4 will be 0
                                    cleaned_images_trailer[child_file.split('.')[0]] = current_image_ascii_trailer[
                                                                                       len(current_image_ascii_trailer)% 4:]
                            elif len(current_image_ascii_trailer) % 4 == 0:
                                # assume there is an appended data since ascii string meets encoded base 64 requirements
                                image_has_appended_data = True
                                if not cleaned_images_trailer.get(child_file.split('.')[0]):
                                    cleaned_images_trailer[child_file.split('.')[0]] = current_image_ascii_trailer

                    # get images timestamps (before extracting attached data)
                    all_images_timestamps[child_file.split('.')[0]] = {
                        'created': time.ctime(os.path.getctime(os.path.join(current_directory, child_file))),
                        'last_modified': time.ctime(os.path.getmtime(os.path.join(current_directory, child_file))),
                        'last_accessed': time.ctime(os.path.getatime(os.path.join(current_directory, child_file))),
                    }

                    # create new image without attached data
                    with open(current_image_path, "rb") as existing_file:

                        # create a directory to store all images without attached data
                        if not os.path.exists(f'{os.getcwd()}/CleanedImages'):
                            os.mkdir(os.path.join(os.getcwd(), 'CleanedImages'))

                        with open(f"CleanedImages/{child_file.split('.')[0]}.jpg", "wb") as new_image:
                            # check if the existing image has attached data
                            if image_has_appended_data:
                                # write all lines of the existing image to new image without last line (attached data)
                                new_image.writelines([line for line in existing_file.readlines()[:-1]])
                            else:
                                # write all lines of the existing image to new image if no attached data
                                new_image.writelines([line for line in existing_file.readlines()])

                    # get required information for output file
                    try:
                        new_file_created_time = datetime.datetime.fromtimestamp(os.path.getctime(f"CleanedImages/{child_file.split('.')[0]}.jpg")).strftime('%m-%d-%Y, %I:%M:%S %p')
                        new_file_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(f"CleanedImages/{child_file.split('.')[0]}.jpg")).strftime('%m-%d-%Y, %I:%M:%S %p')
                        new_file_last_accessed = datetime.datetime.fromtimestamp(os.path.getatime(f"CleanedImages/{child_file.split('.')[0]}.jpg")).strftime('%m-%d-%Y, %I:%M:%S %p')
                    except OSError:
                        new_file_created_time = time.ctime(os.path.getctime(f"CleanedImages/{child_file.split('.')[0]}.jpg"))
                        new_file_last_modified = time.ctime(os.path.getmtime(f"CleanedImages/{child_file.split('.')[0]}.jpg"))
                        new_file_last_accessed = time.ctime(os.path.getatime(f"CleanedImages/{child_file.split('.')[0]}.jpg"))

                    final_image_details[child_file.split('.')[0]] = {
                        'old filename': child_file,
                        'new filename': f"{child_file.split('.')[0]}.jpg",
                        'hash': sha256_hash_func(os.path.join(os.getcwd(), f"CleanedImages/{child_file.split('.')[0]}.jpg")),
                        'timestamps': {
                            'created': new_file_created_time,
                            'last_modified': new_file_last_modified,
                            'last_accessed': new_file_last_accessed,
                        }
                    }
            else:
                pass

        # get attached data and corresponding plain text
        for image_name in cleaned_images_trailer.keys():
            base64_message = cleaned_images_trailer.get(image_name)
            decoded_message = hw64decode(base64_message)
            decoded_messages[image_name] = decoded_message

            # update final table with encoded attachment plaintext
            final_image_details[image_name]['plaintext message'] = decoded_message
            final_image_details[image_name]['base64 encoded data'] = base64_message

        # write required information to output file
        with open('BalogunOutput.txt', "w") as output_file:
            for record in final_image_details.keys():
                for detail in final_image_details[record].keys():
                    try:
                        output_file.writelines([detail, ': ', final_image_details[record][detail], '\n'])
                    except TypeError:
                        for sub_detail in final_image_details[record][detail].keys():
                            output_file.writelines(
                                [sub_detail, ': ', final_image_details[record][detail][sub_detail], '\n'])
                        pass
                output_file.writelines('\n\n')

        # print to console
        print('Output file Path: ', os.path.join(os.getcwd(), 'BalogunOutput.txt'))  # path to output file
        print('Completion time: ', datetime.datetime.now() - startTime)  # time script completes execution
    else:
        # if directory is not found
        print('INVALID DIRECTORY')


if __name__ == '__main__':
    main('PyCharm')
