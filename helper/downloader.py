import requests
import re


class Downloader:

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

    def get_jpeg(cls, url, uuid):
        response = cls.__get_response(url + "/search/api/v5.0/item/" + uuid + "/streams/IMG_FULL")
        return response

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


#r = requests.get('https://kramerius.mzk.cz/search/api/v5.0/item/uuid:f3dee9b0-6ada-11dd-9c52-000d606f5dc6/streams/')
#print(r.text)
downloader = Downloader()
# save alto
#alto = downloader.get_alto("https://kramerius.mzk.cz", "uuid:f3dee9b0-6ada-11dd-9c52-000d606f5dc6")
#with open('alto.xml', 'w') as file:
#    file.write(alto)
# save image
image = downloader.get_jpeg("https://kramerius.mzk.cz", "uuid:f3dee9b0-6ada-11dd-9c52-000d606f5dc6")
suffix = image.headers['Content-Type'].split('/')[1]
with open("img." + suffix, 'wb') as file:
    file.write(image.content)