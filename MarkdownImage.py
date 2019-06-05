# -*- coding: utf-8 -*-
import requests
import re
import os
import sys


def download_imageinfile(origin_url_list):
    global origin_image_name_list
    origin_image_name_list = list()
    for origin_url in origin_url_list:
        origin_image_name = os.path.basename(origin_url)
        origin_image_name_list.append(origin_image_name)
        img_data = requests.get(origin_url)
        if not img_data.ok:
            return img_data
        with open(origin_image_name, 'wb') as handler:
            handler.write(img_data.content)


def open_mdfile(path):
    f = open(path, 'rb')
    file_content = f.read().decode('utf-8')
    f.close()
    return file_content


def save_mdfile(path, content):
    f = open(path, 'w+', encoding='utf8')
    f.write(content)
    f.close()


def find_url_inline(file_content):
    url_list1 = re.findall("(?<=\().*?(?<=.jpg|.png|.gif)", file_content)
    return url_list1


def find_url_reference(file_content):
    url_list2 = re.findall("\]\: (.*?(?<=.jpg|.png|.gif))", file_content)
    return url_list2


def upload_image(origin_image_name_list):
    global new_url_list
    new_url_list = list()
    for origin_image_name in origin_image_name_list:
        file = {'smfile': (origin_image_name, open(origin_image_name, 'rb'), 'image/jpeg')}
        api_post = requests.post('https://sm.ms/api/upload', files=file)
        response = api_post.json()
        print(origin_image_name, ' : ', response['code'])
        new_url_list.append(response['data']['url'])


def replace_url(origin_url_list, content):
    new_url_list_sub = 0
    global new_content
    new_content = content
    for origin_url in origin_url_list:
        new_content = re.sub(origin_url, new_url_list[new_url_list_sub], new_content)
        print(origin_url + ' ----> ' + new_url_list[new_url_list_sub])
        new_url_list_sub = new_url_list_sub + 1


def main(inputfile, outputfile):
    content = open_mdfile(inputfile)
    origin_url_list = find_url_reference(content)
    origin_url_list.extend(find_url_inline(content))
    download_imageinfile(origin_url_list)
    upload_image(origin_image_name_list)
    replace_url(origin_url_list, content)
    save_mdfile(outputfile, new_content)


if len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])
else:
    input_file_list = list()
    for file in os.listdir('.'):
        if file.endswith(".txt") or file.endswith(".md"):
            print("processing: ", file)
            main(file, str.split(file)[0]+"_new.md")
