from src.session.session import Session, acess_session
from src.const.default_header import XML_HTTP_REQ_HEADERS, POST_HEADERS
from src.const.url import DOCUMENT_WRITE_URL, IMAGE_FILTER_AJAX, UPLOAD_HOST_URL, UPLOAD_IMG_PHP
from src.const.const import GA_COOKIE
from src.useful_function.useful_function import quote, unquote, safe_get

import lxml.html
import asyncio
import aiohttp
import re


async def upload_image(board_id='api', file_path=''):
    async def get_write_info():
        url = DOCUMENT_WRITE_URL(board_id)
        async with Session().get(url) as res:
            parsed = lxml.html.fromstring(await res.text())

        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        board_name = parsed.xpath("//a[@class='gall-tit-lnk']")[0].text.strip()
        r_key = parsed.xpath("//input[@name='r_key']")[0].get("value")

        return {
            'csrf_token': csrf_token,
            'board_name': board_name,
            'r_key': r_key
        }

    write_info = await get_write_info()

    header = XML_HTTP_REQ_HEADERS.copy()
    header.update({
        "Referer": DOCUMENT_WRITE_URL(board_id),
        "X-CSRF-TOKEN": write_info['csrf_token']
    })

    payload = {
        "id": board_id,
    }

    async with Session().post(IMAGE_FILTER_AJAX, headers=header, data=payload) as res:
        res_json = await res.json()

    header = POST_HEADERS.copy()
    header.update({
        "Host": UPLOAD_HOST_URL,
        "Referer": DOCUMENT_WRITE_URL(board_id)
    })

    payload = aiohttp.FormData({
        "id": board_id,
        "r_key": write_info["r_key"]
    })

    file = open(file_path, 'rb')

    payload.add_field('upload[]',
                      file,
                      filename='test.jpg',
                      content_type='image/jpg')

    cookies = {
        f"m_dcinside_{board_id}": board_id,
        "m_dcinside_lately": quote(f"{board_id}|{write_info['board_name']},"),
        "_ga": GA_COOKIE,
    }
    #
    async with Session().post(UPLOAD_IMG_PHP, headers=header, data=payload, cookies=cookies) as res:
        res_final = await res.text()

    file.close()

    img_data = re.search(r"(?<='img',').*(?=',0\);)", res_final).group()

    return img_data


if __name__ == '__main__':
    value = asyncio.run(upload_image('api', "C:/Users/dobbyjang/Desktop/PyDCApi/test/article.jpg"))
    print(value)