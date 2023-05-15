from src.session.session import Session, acess_session
from src.const.default_header import XML_HTTP_REQ_HEADERS
from src.const.url import HTTPS_DC_URL, DC_URL, DOCUMENT_VIEW_URL, COMMENT_WRITE_AJAX
from src.const.const import GA_COOKIE
from src.useful_function.useful_function import quote, unquote, safe_get

import asyncio
import lxml.html
import json


async def write_comment(board_id='api', document_id=358, contents="안됨...", name="ㅇㅇ", password="1234", parent_comment_id=""):
    async def get_document_info():
        url = DOCUMENT_VIEW_URL(board_id, document_id)
        async with Session().get(url) as res:
            parsed = lxml.html.fromstring(await res.text())

        rand_code = safe_get(parsed.xpath("//input[@name='rand_codeC']"), "value")
        hide_robot = parsed.xpath("//input[@class='hide-robot']")[0].get("name")
        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        title = parsed.xpath("//span[@class='tit']")[0].text.strip()
        board_name = parsed.xpath("//a[@class='gall-tit-lnk']")[0].text.strip()
        con_key = await acess_session("com_submit", url, require_conkey=False, csrf_token=csrf_token)

        return {'hide_robot': hide_robot,
                'csrf_token': csrf_token,
                'title': title,
                'board_name': board_name,
                'con_key': con_key,
                'rand_code': rand_code
                }

    doc_info = await get_document_info()

    header = XML_HTTP_REQ_HEADERS.copy()
    header.update({
        "Referer": DOCUMENT_VIEW_URL(board_id, document_id),
        "Host": DC_URL,
        "Origin": HTTPS_DC_URL,
        "X-CSRF-TOKEN": doc_info['csrf_token'],
    })

    cookies = {
        f"m_downside_{board_id}": board_id,
        "m_dcinside_lately": quote(f"{board_id}|{doc_info['board_name']},"),
        "_ga": GA_COOKIE,
    }

    payload = {
        "comment_memo": contents,
        "comment_nick": name,
        "comment_pw": password,
        "mode": "com_write",
        "comment_no": parent_comment_id,
        "id": board_id,
        "no": document_id,
        "best_chk": "",
        "subject": doc_info['title'],
        "board_id": "",
        "reple_id": "",
        "cpage": "1",
        "con_key": doc_info['con_key'],
        doc_info['hide_robot']: "1",
    }

    if doc_info['rand_code']:
        payload["rand_code"] = doc_info['rand_code']
        payload["captcha_code"] = "adasd"

    async with Session().post(COMMENT_WRITE_AJAX, headers=header, data=payload, cookies=cookies) as res:
        parsed = await res.text()

    return parsed


if __name__ == '__main__':
    value = asyncio.run(write_comment(contents="이게 되나?"))
    print(value)
