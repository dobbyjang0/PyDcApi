from src.session.session import Session, acess_session
from src.const.default_header import XML_HTTP_REQ_HEADERS, POST_HEADERS
from src.const.url import DOCUMENT_WRITE_URL, WRITE_FILTER_AJAX, UPLOAD_HOST_URL, WRITE_PHP
from src.const.const import GA_COOKIE
from src.useful_function.useful_function import quote, unquote, safe_get

import lxml.html
import asyncio


async def write_document(board_id='api', title="도와줘요2", contents="제발요", name="ㅇㅇ", password="1234", image=None):
    if not(image is None or image.is_ready):
        raise Exception('이미지가 준비되있지 않습니다.')

    async def get_write_info():
        url = DOCUMENT_WRITE_URL(board_id)
        async with Session().get(url) as res:
            parsed = lxml.html.fromstring(await res.text())

        rand_code = safe_get(parsed.xpath("//input[@name='code']"), "value")
        user_id = safe_get(parsed.xpath("//input[@name='user_id']"), "value") if not name else None
        mobile_key = parsed.xpath("//input[@id='mobile_key']")[0].get("value")
        hide_robot = parsed.xpath("//input[@class='hide-robot']")[0].get("name")
        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        con_key = await acess_session("dc_check2", url, require_conkey=False, csrf_token=csrf_token)
        board_name = parsed.xpath("//a[@class='gall-tit-lnk']")[0].text.strip()
        is_minor = parsed.xpath("//input[@id='is_minor']")[0].get("value")

        return {
            'rand_code': rand_code,
            'user_id': user_id,
            'mobile_key': mobile_key,
            'hide_robot': hide_robot,
            'csrf_token': csrf_token,
            'con_key': con_key,
            'board_name': board_name,
            'is_minor': is_minor
        }

    write_info = await get_write_info()

    header = XML_HTTP_REQ_HEADERS.copy()
    header.update({
        "Referer": DOCUMENT_WRITE_URL(board_id),
        "X-CSRF-TOKEN": write_info['csrf_token']
    })

    payload = {
        "subject": title,
        "memo": contents,
        "mode": "write",
        "id": board_id,
    }
    if write_info['rand_code']:
        payload.update({
            "code": write_info['rand_code']
        })

    async with Session().post(WRITE_FILTER_AJAX, headers=header, data=payload) as res:
        res_json = await res.json()

    header = POST_HEADERS.copy()
    header.update({
        "Host": UPLOAD_HOST_URL,
        "Referer": DOCUMENT_WRITE_URL(board_id)
    })

    payload = {
        "subject": title,
        "memo": contents,
        write_info['hide_robot']: "1",
        "GEY3JWF": write_info['hide_robot'],
        "id": board_id,
        "contentOrder": image.content_order if image else "order_memo",
        "mode": "write",
        "Block_key": write_info['con_key'],
        "bgm": "",
        "iData": image.i_data if image else "",
        "yData": "",
        "tmp": "",
        "imgSize": "850",
        "is_minor": "1" if write_info['is_minor'] else "",
        "mobile_key": write_info['mobile_key'],
    }

    if write_info['rand_code']:
        payload["code"] = write_info['rand_code']
    if name:
        payload["name"] = name
        payload["password"] = password
    else:
        payload["user_id"] = write_info['user_id']

    cookies = {
        f"m_dcinside_{board_id}": board_id,
        "m_dcinside_lately": quote(f"{board_id}|{write_info['board_name']},"),
        "_ga": GA_COOKIE,
    }

    async with Session().post(WRITE_PHP, headers=header, data=payload, cookies=cookies) as res:
        res_final = await res.text()

    image.unload()

    return res_final


if __name__ == '__main__':
    value = asyncio.run(write_document(title="파이파이파이썬", contents="이거는 왜 됨?"))
    print(value)
