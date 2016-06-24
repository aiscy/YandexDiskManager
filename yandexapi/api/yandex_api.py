import requests
from requests_toolbelt import MultipartEncoderMonitor


class YandexAPI:
    def __init__(self, api_key):
        self.api_key = {'Authorization': 'OAuth ' + api_key}

    def user_disk_info(self):
        return requests.get('https://cloud-api.yandex.net/v1/disk/', headers=self.api_key).json()

    def file_meta(self, path):
        return requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                            headers=self.api_key,
                            params={'path': path})

    def is_path_exist(self, path):
        r = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                            headers=self.api_key,
                            params={'path': path})
        return True if r.status_code == 200 else False

    def create_folder(self, path):
        r = requests.put('https://cloud-api.yandex.net/v1/disk/resources/',
                         headers=self.api_key,
                         params={'path': path})
        return True if r.status_code == 201 else False

    def upload_file(self, file_object, path, callback_func):
        r = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                         headers=self.api_key,
                         params={'path': path})
        upload_url = r.json().get('href')
        m = MultipartEncoderMonitor.from_fields(fields={'file': file_object}, callback=callback_func)
        r = requests.put(upload_url, data=m, headers={'Content-Type': m.content_type})
        return True if r.status_code == 201 else False

    def publish_file(self, path):
        r = requests.put('https://cloud-api.yandex.net/v1/disk/resources/publish',
                         headers=self.api_key,
                         params={'path': path})
        return True if r.status_code == 200 else False

    def get_file_url(self, path):
        return self.file_meta(path).json().get('public_url')




    # def files_flat_list(self, media_type='compressed'):
    #     files = []
    #     offset = 0
    #     r = requests.get('https://cloud-api.yandex.net/v1/disk/resources/files', headers=self.api_key,
    #                         params={'limit': 100, 'media_type': media_type, 'offset': 2000}).json()
    #     print(r)

        # while r.get('items') is not None:
        #     r = requests.get('https://cloud-api.yandex.net/v1/disk/resources/files', headers=self.api_key,
        #                     params={'limit': 100, 'media_type': media_type, 'offset': offset}).json()
        #     files.append(r.get('items'))
        #     offset += 100
        #     print(r.get('offset'))
        # return files

if __name__ == '__main__':
    from pprint import pprint
    # print(api.user_disk_info())
    # pprint(api.file_meta('disk:/Загрузка'))
    # pprint(api.is_path_exist('disk:/Загрузка'))
    # pprint(api.upload_file(None, 'disk:/Загрузка/huerga.lol'))