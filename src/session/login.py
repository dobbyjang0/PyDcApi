from src.session.session import Session
from src.const.url import LOGIN_URL, LOGIN_ACCESS_URL, LOGIN_HOST_URL, HTTPS_DC_URL
from src.const.default_header import XML_HTTP_REQ_HEADERS, POST_HEADERS
from src.const.const import GA_COOKIE

import lxml.html
import asyncio

async def login(id, password):
    async def get_login_info():
        async with Session().get(LOGIN_URL) as res:
            parsed = lxml.html.fromstring(await res.text())

        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        con_key = parsed.xpath("//input[@id='conKey']")[0].get("content")
        return {
            'csrf_token': csrf_token,
            'con_key': con_key
        }

    login_info = await get_login_info()

    header = XML_HTTP_REQ_HEADERS.copy()
    header.update({
        "X-CSRF-TOKEN": login_info['csrf_token']
    })

    payload = {
        'token_verify': 'dc_login',
        'conKey': login_info['con_key'],
    }

    async with Session().post(LOGIN_ACCESS_URL, headers=header, data=payload) as res:
        new_con_key = (await res.json())['Block_key']

    header = POST_HEADERS.copy()
    header.update({
        "Host": LOGIN_HOST_URL,
        "Referer": LOGIN_URL
    })

    payload = {
        'code': id,
        'password': password,
        'loginCash': 'on',
        'conKey': new_con_key,
        'r_url': HTTPS_DC_URL
    }

    cookies = {
        "_ga": GA_COOKIE
    }

    async with Session().post(LOGIN_URL, headers=header, data=payload, cookies=cookies) as res:
        res_final = await res.text()

    return res_final

