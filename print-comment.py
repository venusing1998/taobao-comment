import json

import requests


def get_url(url):
    if url.find("&id=") != -1:
        id = url[url.find("&id=")+4:url.find("&id=")+16]
    else:
        print("The website isn't correct. Please provide the correct website.")
    new_url = "https://rate.taobao.com/feedRateList.htm?auctionNumId={}&currentPageNum=1".format(
        id)
    return new_url


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = json.loads(response.text.strip().strip('()'))
            return result
    except requests.ConnectionError:
        return None


def get_data(json):
    total = json.get("total")
    comments = json.get("comments")
    if comments:
        for item in comments:
            contents = {}
            contents["total"] = total
            contents["nick"] = item.get("user").get("nick")
            contents["content"] = item.get("content")
            yield contents


def main(url):
    new_url = get_url(url)
    json = get_html(new_url)
    count = 1
    currentPageNum = 1
    for item in get_data(json):
        if item["total"] >= 0:
            print("该商品共有评论"+str(item["total"])+"条,具体如下: loading...")
            break
    for item in get_data(json):
        while count < item["total"]:
            next_url = new_url[:-1]+str(currentPageNum)
            json_2 = get_html(next_url)
            currentPageNum += 1
            for item_2 in get_data(json_2):
                print("User", count, ": ", item_2.get("nick"), "\n",
                      "Comment: ", item_2.get("content"), "\n\n", sep="")
                count += 1


if __name__ == "__main__":
    url = "https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w8914283-17367045126.61.1b0274abi0vMaC&id=559274058732"
    main(url)
