import requests


# class YaUploader:
#     def __init__(self, token: str):
#         self.token = token
#
#     def get_headers(self):
#         return {
#             'Content-type': 'application/json',
#             'Authorization': 'OAuth {}'.format(self.token)
#         }
#
#     def adr_parser(self, file_path):
#         """Функция получает имя файла из пути к нему"""
#         # adr = file_path
#         adr_split = file_path.replace("\\", " ")
#         adr_list = adr_split.split()
#         # filename = adr_list[-1]
#         return adr_list[-1]
#
#     def get_upload_link(self, disk_file_path):
#         """Получаем ссылку для загрузки файла на Я.Диск"""
#         upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
#         headers = self.get_headers()
#         params = {'path': disk_file_path, 'overwrite': 'true'}
#         response = requests.get(upload_url, headers=headers, params=params)
#         return response.json()
#
#     def upload(self, file_path):
#         """Метод загруджает файл file_path на Я.Диск"""
#         filename = self.adr_parser(file_path)
#         href = self.get_upload_link(disk_file_path=filename).get('href', '')
#         response = requests.put(href, data=open(file_path, 'rb'))
#         response.raise_for_status()
#         if response.status_code == 201:
#             return f'File "{self.adr_parser(file_path)}" was created successfully'
#
#


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
        # self.account_info = requests.get(self.url + 'account.getInfo', self.params).json()  # ['response'][0]['id']

    def get_albums(self, owner_id=None):
        if owner_id is None:
            owner_id = self.owner_id
        photo_url = self.url + 'photos.getAlbums'
        photo_params = {
            'owner_id': owner_id,
            'need_system': 1,
            'photo_sizes': 1
        }
        res = requests.get(photo_url, params={**self.params, **photo_params})
        print(res.json())


if __name__ == '__main__':
    # uploader = YaUploader('AQAAAAA36m8ZAADLW6XIsrMVfk9ImIKjJD3zTy0')
    # result = uploader.upload("D:\Python\Disk_file.txt")
    # print(result)
    vk_client = VkUser('a7885b2a0024c9e139618ca0ff5be5688dd12f285dcb522ccfe6f0eacc76b59ac5fd6ddc2a89e354acfa0', '5.130')
    # print(vk_client.owner_id)
    # print(vk_client.account_info)
    vk_client.get_albums()
