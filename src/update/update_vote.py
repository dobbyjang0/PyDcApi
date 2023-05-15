from src.session.session import Session, acess_session
from src.const.default_header import XML_HTTP_REQ_HEADERS
from src.const.url import HTTPS_DC_URL, DC_URL, DOCUMENT_VIEW_URL, COMMENT_WRITE_AJAX
from src.const.const import GA_COOKIE
from src.useful_function.useful_function import quote, unquote, safe_get

import asyncio
import lxml.html
import json


async def update_vote(board_id='api', document_id=358, item_name='ㅇㅇ'):
    async def get_document_info():
        url = DOCUMENT_VIEW_URL(board_id, document_id)
        async with Session().get(url) as res:
            parsed = lxml.html.fromstring(await res.text())

        poll_url = safe_get(parsed.xpath("//iframe[contains(@id,'vote_iframe')]"), "src")

        if poll_url is None:
            return {
                'is_exist' : False
            }
        print(poll_url)
        async with Session().get(poll_url) as res:
            parsed = lxml.html.fromstring(await res.text())

        poll_value = safe_get(parsed.xpath("//input[@name='poll']"), "value")

        vote_dic = {}
        for elem in parsed.xpath("//ul[@class='vote-ask-lst']/li"):
            elem_name = ''.join(elem.itertext()).strip()
            elem_id = elem.get("data-no")
            vote_dic[elem_name] = elem_id
        #
        is_voted = parsed.xpath("//span[@class='vote-sns-txt']") != []

        return {'poll_value': poll_value,
                'vote_list': vote_dic,
                'is_voted' : is_voted,
                'is_exist' : True
                }

    vote_info = await get_document_info()

    if not vote_info['is_exist']:
        return '투표 존재하지 않음'

    if vote_info['is_voted']:
        return '투표 이미 진행됨'

    poll_post_url = "https://m.dcinside.com/poll/vote"

    header = XML_HTTP_REQ_HEADERS.copy()

    payload = {
        "item": vote_info['vote_list'][item_name],
        "poll": vote_info['poll_value']
    }

    async with Session().post(poll_post_url, headers=header, data=payload) as res:
        res_text = await res.text()

    return res_text

if __name__ == '__main__':
    value = asyncio.run(update_vote(board_id='api', document_id=611, item_name='ㅇㅇ'))
    print(value)
