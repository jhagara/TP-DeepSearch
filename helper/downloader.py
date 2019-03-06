import requests
import re
import os
import errno


class Downloader:
    ROOT_KRAMERIUS = "/kramerius"

    def get_info(cls, url, uuid):
        response = cls.__get_response(url + "/search/api/v5.0/item/" + uuid)
        return response.json()

    def get_siblings(cls, url, uuid):
        response = cls.__get_response(url + "/search/api/v5.0/item/" + uuid + "/siblings")
        return response.json()

    def get_children(cls, url, uuid):
        response = cls.__get_response(url + "/search/api/v5.0/item/" + uuid + "/children")
        return response.json()

    def get_alto(cls, url, uuid):
        response = cls.__get_response(url + "/search/api/v5.0/item/" + uuid + "/streams/ALTO")
        encoding = re.search('encoding="(.*)"', response.text)
        response.encoding = encoding
        return response.text

    def get_image(cls, url, uuid):
        response = cls.__get_response(url + "/search/api/v5.0/item/" + uuid + "/streams/IMG_FULL")
        return response

    def download_xml(cls, url, uuid, dir, info = None):
        if info is None:
            info = cls.get_info(url, uuid)
        if info['datanode'] is False:
            raise ValueError(uuid + " on url " + url + " is not a data node")
        name = info['title']
        name = name.replace("[", "")
        name = name.replace("]", "")
        xml = cls.get_alto(url, uuid)
        with open(dir + "/" + name + "_" + uuid + ".xml", 'w') as file:
            file.write(xml)

    def download_image(cls, url, uuid, dir, info=None):
        if info is None:
            info = cls.get_info(url, uuid)
        if info['datanode'] is False:
            raise ValueError(uuid + " on url " + url + " is not a data node")
        name = info['title']
        name = name.replace("[", "")
        name = name.replace("]", "")
        image = cls.get_image(url, uuid)
        suffix = image.headers['Content-Type'].split('/')[1]
        with open(dir + "/" + name + "_" + uuid + "." + suffix, 'wb') as file:
            file.write(image.content)

    def download_item(cls, url, uuid, dir, path=None):
        item_info = cls.get_info(url, uuid)
        if path is None:
            path = cls.ROOT_KRAMERIUS
            for node in item_info['context'][0]:
                if node['pid'] == uuid:
                    break
                node_info = cls.get_info(url, node['pid'])
                path += "/" + node_info['title']
            path += "/" + item_info['title']
        if os.path.isdir(dir + path):
            return
        cls.__create_directory(dir + path + "/XML")
        cls.__create_directory(dir + path + "/STR")
        children = cls.get_children(url, uuid)
        for child in children:
            streams = cls.__get_response(url + "/search/api/v5.0/item/" + child['pid'] + "/streams").json()
            if streams.get("ALTO") is None:
                raise ValueError(uuid + " does not have ALTO xml")
            if streams.get("IMG_FULL") is None:
                raise ValueError(uuid + " does not have IMG_FULL image")
            child_info =  cls.get_info(url, child['pid'])
            cls.download_xml(url, child['pid'], dir + path + "/XML", child_info)
            cls.download_image(url, child['pid'], dir + path + "/STR", child_info)
        # TODO stiahnutie marc zaznamu

    def download_tree(cls, url, uuid, dir, path=None):
        if path is None:
            path = cls.ROOT_KRAMERIUS
        children = cls.get_children(url, uuid)
        info = cls.get_info(url, uuid)
        path = path + info['title']
        for child in children:
            if child['datanode'] is True:
                cls.download_item(url, uuid, dir, path)
                return
            else:
                cls.download_tree(url, child['pid'], dir, path)

    @classmethod
    def __create_directory(cls, dir):
        try:
            os.makedirs(dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    @classmethod
    def __get_response(cls, url):
        count = 0
        response = None
        while count <= 3:
            response = requests.get(url)

            if response.ok:
                return response
            else:
                count += 1
        response.raise_for_status()

