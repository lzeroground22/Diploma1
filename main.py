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
        """Метод получает имя файла из пути к нему"""
        adr_split = file_path.replace("\\", " ")
        adr_list = adr_split.split()
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
        """Метод выполняет загрузку на Я.Диск по URL"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {
            'path': disk_file_path,
            'url': src,
            'disable_redirects': 'false'}
        response = requests.post(upload_url, headers=headers, params=params)
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
        """Метод позволяет узнать названия альбомов пользователя"""
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
        """Метод выдаёт подробную информацию о фото из альбома 'album_id' """
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
        """Метод сортирует фото по лайкам """
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


def cycle(yandex, vk, album_id):
    """Функция выгружает фото из альбома "album_id" на Я.Диск в папку "Neto", присваивая имена по количеству лайков """
    photo_list = vk.decomposer(album_id)
    for photo in photo_list:
        file_path = "/Neto/" + str(photo["likes"]) + ".jpg"
        yandex.link_upload(photo['src'], file_path)


if __name__ == '__main__':
    uploader = YaUploader('YaToken')
    vk_client = VkUser('VKToken', '5.130')
    cycle(uploader, vk_client, 'profile')


# https://oauth.vk.com/authorize?client_id=7845912&display=page&scope=photos&response_type=token&v=5.130
