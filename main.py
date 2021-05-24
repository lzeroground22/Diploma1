import requests


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

    def link_upload(self, url, disk_file_path):
        """Метод загружает файл по url на Я.Диск по адресу disk_file_path"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'url': url, 'disable_redirects': 'false'}
        response = requests.post(upload_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 202:
            return f'File was created successfully'


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_vk, version):
        self.token = token_vk
        self.version = version
        self.params = {
            'access_token': self.token_vk,
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
            'count': 10
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
                'url': foto['sizes'][-1]['url']
            }
            attrib_list.append(attrib)
        sorted_by_likes_list = sorted(attrib_list, key=lambda i: i['likes'], reverse=True)
        return sorted_by_likes_list


class Cyclone(YaUploader, VkUser):

    def cycle_upload(self, name):
        """Метод перебирает в цикле фото из VkUser.decomposer и передает в YaUploader.link_upload
        имя = foto['likes']['count'], адрес = foto['sizes'][-1]['url']"""
        photos_cycle = self.decomposer(name)
        for photo in photos_cycle:
            return photo['likes'], photo['url']


if __name__ == '__main__':
    # uploader = YaUploader('AQAAAAA36m8ZAADLW6XIsrMVfk9ImIKjJD3zTy0')
    # result = uploader.link_upload('https://sun9-39.userapi.com/c10472/u2571705/-6/w_75259ccf.jpg', '/Neto/50.jpg')
    vk_client = VkUser('592a8b69055f08de859b8cd0a54bb73edc8aa96807c416e33a3d2b027adbab379bb0c6f100ee53cee82b0', '5.130')
    # print(vk_client.decomposer('profile'))
    cycle = Cyclone('AQAAAAA36m8ZAADLW6XIsrMVfk9ImIKjJD3zTy0')
    cycle.cycle_upload('profile')
    print(cycle)

# 'a7885b2a0024c9e139618ca0ff5be5688dd12f285dcb522ccfe6f0eacc76b59ac5fd6ddc2a89e354acfa0' frunde token
#  '592a8b69055f08de859b8cd0a54bb73edc8aa96807c416e33a3d2b027adbab379bb0c6f100ee53cee82b0' photo token
# https://oauth.vk.com/authorize?client_id=7845912&display=page&scope=photos&expires_in=86400&response_type=token&v=5.130
