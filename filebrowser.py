#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


PICTURE_EXT = [".jpg", ".png"]

TXT_EXT = [".txt"]

ROOT_DIR = os.getcwd()

DESTINATION_DIR = os.path.join(ROOT_DIR, "_site")

HTML_TEMP = r"""<!DOCTYPE html>

<html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8">
    </head>

    <body style="margin: auto; width: 680px;">
        {content}
    </body>
</html>
"""

IMG_STR = '<img style="max-width: 100%; max-height: 100%;" src="file:///{}">\n'

A_STR = '<p><a href="file:///{}">{}</a></p>\n'


def walk_directory(path):
    """返回目录下的图片文件列表、txt文件列表和子文件夹列表。

        Args:
            path: 文件夹绝对路径。

        Returns:
            pictures:    包含所有图片的绝对路径。
            texts:       包含所有txt的绝对路径。
            sub_dirs:    所有子文件夹的绝对路径。
    """

    dir, sub_dirs, files = next(os.walk(path))  # 获取目录的所有子目录和文件，不迭代子目录。

    # 分类要处理的文件
    pictures = []
    texts = []
    for file in files:
        filename_ext = os.path.splitext(file)[1]
        if filename_ext in TXT_EXT:
            texts.append(file)
        elif filename_ext in PICTURE_EXT:
            pictures.append(file)

    # 生成绝对路径
    sub_dirs = [os.path.join(dir, sub_dir) for sub_dir in sub_dirs]
    texts = [os.path.join(dir, text) for text in texts]
    pictures = [os.path.join(dir, pic) for pic in pictures]

    return (pictures, texts, sub_dirs)


def get_destination_path(path):
    """返回一个绝对路径，这个路径是根据文件在ROOT_DIR的路径，与DESTINATION_DIR
    组合得到的在文件在DESTINATION_DIR下的绝对路径。
    例如：/dir/subdir --> /dir/_site/subdir

        Args:
            path:    文件的绝对路径。

        Returns:
            result:    HTML页面要存储的绝对路径。
    """

    relative_path = os.path.relpath(path, ROOT_DIR)
    result = os.path.join(DESTINATION_DIR, relative_path)
    return result


def create_directory(path):
    """判断目录是否存在，如果不存在则创建。"""

    if not os.path.exists(path):
        os.makedirs(path)


def create_picture_html(dest_path, pictures):
    """把目录下所有图片生成一个HTML页面。

       Args:
           dest_path:   目标目录的绝对路径。
           pictures:    目录下所有图片的绝对路径。

       Returns:
           link:    (name, path)，指向生成的HTML页面的链接。
    """

    filename = os.path.basename(dest_path) + "_pic.html"  # 创建的HTML文件名

    content = ''
    for picture in pictures:
        content += IMG_STR.format(picture)
    html = HTML_TEMP.format(title=filename, content=content)
    with open(os.path.join(dest_path, filename), "w", encoding="utf-8") as f:
        f.write(html)
    return (filename, os.path.join(dest_path, filename))


def create_text_html(text):
    pass


def create_index_html(dest_path, links):
    """把目录下所有页面生成一个导航页面。

       Args:
           dest_path:   目标目录的绝对路径。
           links:    目录下所有页面的绝对路径。

       Returns:
           link:    (name, path)，指向生成的HTML页面的链接。
    """

    filename = os.path.basename(dest_path) + "_index.html"  # 创建的HTML文件名

    content = ''
    for link in links:
        content += A_STR.format(link[1], link[0])
    html = HTML_TEMP.format(title=filename, content=content)
    with open(os.path.join(dest_path, filename), "w", encoding="utf-8") as f:
        f.write(html)
    return (filename, os.path.join(dest_path, filename))


def process(path):
    """根据path目录下的文件创建对应的HTML页面，并存储在DESTINATION_DIR下。

        Args:
            path:    目录绝对路径。

        Returns:
            html_link:    (name, path)，单个页面链接或者是导航页面链接。
    """

    pictures, texts, sub_dirs = walk_directory(path)

    if pictures == [] and texts == [] and sub_dirs == []:
        print("Nothing in directory {}".format(path))
        return None

    links = []
    dest_dir = get_destination_path(path)

    create_directory(dest_dir)
    if pictures:
        links.append(create_picture_html(dest_dir, pictures))
#   if texts:
#       for text in texts:
#           links.append(create_text_html(text))
    if sub_dirs:
        for sub_dir in sub_dirs:
            sub_link = process(sub_dir)
            if sub_link:
                links.append(sub_link)

    if len(links) == 1 and path != ROOT_DIR:
        return links[0]
    return create_index_html(dest_dir, links)


if __name__ == "__main__":
    process(ROOT_DIR)