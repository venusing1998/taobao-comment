import json
import os

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")


def get_html(url):
    """获取网页源代码

    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = json.dumps(json.loads(
                response.text.strip().strip('()')), indent=4, ensure_ascii=False)
            return result
    except requests.ConnectionError as e:
        print(e)
        return None


def write_into_file(result):
    """写入文件

    """
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    with open("dist/result.json", "w", encoding="utf-8") as f:
        f.write(result)


def main(url):
    """主函数

    """
    if url.find("&id=") != -1:
        id = url[url.find("&id=")+4:url.find("&id=")+16]
    else:
        print("The website isn't correct. Please provide the correct website.")
    # 可以修改的测试值 currentPageNum=1
    currentPageNum = 1
    new_url = "https://rate.taobao.com/feedRateList.htm?auctionNumId={}&currentPageNum={}".format(
        id, currentPageNum)
    result = get_html(new_url)
    write_into_file(result)


if __name__ == "__main__":
    url = "https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w8914283-17367045126.61.1b0274abi0vMaC&id=559274058732"
    main(url)
