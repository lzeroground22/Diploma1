import requests
from pprint import pprint


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def adr_parser(self, file_path):
        """Функция получает имя файла из пути к нему"""
        # adr = file_path
        adr_split = file_path.replace("\\", " ")
        adr_list = adr_split.split()
        # filename = adr_list[-1]
        return adr_list[-1]

    def get_upload_link(self, disk_file_path, src=None):
        """Получаем ссылку для загрузки файла на Я.Диск"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        if src is None:
            params = {'path': disk_file_path, 'overwrite': 'true'}
        else:
            params = {'url': src, 'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path):
        """Метод загруджает файл file_path на Я.Диск"""
        filename = self.adr_parser(file_path)
        href = self.get_upload_link(disk_file_path=filename).get('href', '')
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            return f'File "{self.adr_parser(file_path)}" was created successfully'

    def link_upload(self, src, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        # like_name = VkUser.decomposer('profile')
        params = {'path': disk_file_path, 'url': src, 'disable_redirects': 'false'}
        response = requests.post(upload_url, headers=headers, params=params)
        # print(response)
        response.raise_for_status()
        if response.status_code == 202:
            return f'File was created successfully'


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def get_albums(self, owner_id=None):
        if owner_id is None:
            owner_id = self.owner_id
        album_url = self.url + 'photos.getAlbums'
        album_params = {
            'owner_id': owner_id,
            'need_system': 1,
            'album_ids': -6,
        }
        res = requests.get(album_url, params={**self.params, **album_params})
        return res.json()

    def get_photos(self, album_id, owner_id=None, ):
        """Функция выдаёт подробную информацию о фото из альбома 'album_id' """
        if owner_id is None:
            owner_id = self.owner_id
        photo_url = self.url + 'photos.get'
        photo_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': 1,
            'count': 1000
        }
        photo_info = requests.get(photo_url, params={**self.params, **photo_params})
        return photo_info.json()['response']['items']

    def decomposer(self, album_id):
        """ Функция сортирует фото по лайкам """
        photos_list = self.get_photos(album_id)
        attrib_list = []
        for foto in photos_list:
            attrib = {
                'likes': foto['likes']['count'],
                'size': foto['sizes'][-1]['type'],
                'src': foto['sizes'][-1]['url']
            }
            attrib_list.append(attrib)
        sorted_by_likes_list = sorted(attrib_list, key=lambda i: i['likes'], reverse=True)
        return sorted_by_likes_list


if __name__ == '__main__':
    uploader = YaUploader('AQAAAAA36m8ZAADLW6XIsrMVfk9ImIKjJD3zTy0')
    # result = uploader.upload("D:\Python\Disk_file.txt")
    result = uploader.link_upload('https://sun9-54.userapi.com/impf/HJ0UJYDpADxp1CKD-wmZ8DsEPBugvgTot1smKA/cbmFvAo3bhM.jpg?size=600x797&quality=96&sign=b1034a89f34892cc6b8b139e638e0c24&c_uniq_tag=6g8QxdJtyf5OKfuff460o5VIksDQLyjAhqQOSDooY6g&type=album', '/Neto/50.jpg')
    # vk_client = VkUser('300f6b5d1cfe5dcd44fe9346ff2ce2efc37128d84986afffc85797438a6ff48402983dcb75bcba4501257', '5.130')
    # print(vk_client.decomposer('profile'))

# 'a7885b2a0024c9e139618ca0ff5be5688dd12f285dcb522ccfe6f0eacc76b59ac5fd6ddc2a89e354acfa0' frunde token
#  '300f6b5d1cfe5dcd44fe9346ff2ce2efc37128d84986afffc85797438a6ff48402983dcb75bcba4501257' photo token
# https://oauth.vk.com/authorize?client_id=7845912&display=page&scope=photos&response_type=token&v=5.130
