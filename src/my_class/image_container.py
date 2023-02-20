from src.write.upload_image import upload_image


class ImageContainer:
    def __init__(self):
        self._path_list = []
        self._data_list = []
        self.is_ready = False

    @property
    def content_order(self):
        return ';'.join(map(lambda x: f'img{x}', range(len(self._data_list)))) + ';order_memo'

    @property
    def i_data(self):
        return '^@^'.join(map(lambda x: f'img{x[0]}|{x[1]}', enumerate(self._data_list)))

    def add(self, path):
        self._path_list.append(path)

    def pop(self):
        self._path_list.pop()

    async def load(self, board_id='api'):
        self._data_list = []

        for path in self._path_list:
            data = await upload_image(board_id, path)
            self._data_list.append(data)

        self.is_ready = True

    def unload(self):
        self.is_ready = False
        self._data_list = []