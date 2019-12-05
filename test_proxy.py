from urllib import request


def download(url, retry_count=3, headers={}, proxy=None, data=None):
    if url is None:
        return None
    try:
        req = request.Request(url, headers=headers, data=data)
        opener = request.build_opener()
        if proxy:
            proxies = {"https": proxy}
            opener.add_handler(request.ProxyHandler(proxies))
            print("Using proxy", proxies)
        content = opener.open(req).read()
    except Exception as e:
        print('HtmlDownLoader download error:', e.reason)
        content = None
        if retry_count > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # ??? HTTPError ??? HTTP CODE ? 5XX ???????????????????
                return download(url, retry_count-1, headers, proxy, data)
    return content


print(download("https://api.roiback.com/", proxy="http://localhost:9191"))