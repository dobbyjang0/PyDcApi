import aiohttp
import lxml.html
from src.const.default_header import GET_HEADERS, XML_HTTP_REQ_HEADERS
from src.const.url import ACCESS_AJAX
from src.const.const import GA_COOKIE


class Session:
    # 싱글톤
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = aiohttp.ClientSession(headers=GET_HEADERS, cookies={"_ga": GA_COOKIE})
        return cls._instance


async def acess_session(token_verify, target_url, require_conkey=True, csrf_token=None):
    if require_conkey:
        async with Session().get(target_url) as res:
            parsed = lxml.html.fromstring(await res.text())
        con_key = parsed.xpath("//input[@id='con_key']")[0].get("value")
        payload = {"token_verify": token_verify, "con_key": con_key}
    else:
        payload = {"token_verify": token_verify, }

    headers = XML_HTTP_REQ_HEADERS.copy()
    headers.update({
        "Referer": target_url,
        "X-CSRF-TOKEN": csrf_token
    })

    async with Session().post(ACCESS_AJAX, headers=headers, data=payload) as res:
        return (await res.json())["Block_key"]
