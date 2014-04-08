# encoding: utf-8

import sys
import json
import urllib
import os
from workflow import Workflow, web, ICON_WEB


def get_champ_icon(champ_name):
    url_pre = "http://ossweb-img.qq.com/images/lol/img/champion/"
    icons_path = "champ_icons/"
    champ_icons = os.listdir(icons_path)
    champ_icon = champ_name + ".png"
    if champ_icon in champ_icons:
        return icons_path + champ_icon
    else:
        urllib.urlretrieve(url_pre + champ_icon, icons_path + champ_icon)
        return icons_path + champ_icon


def get_chams():
    url = "http://lol.qq.com/biz/hero/free.js"
    r = web.get(url)
    r.raise_for_status()
    champs = json.loads(r.content.split(";")[1][15:])[u"data"]
    return champs


def main(wf):
    detail_url_pre = "http://lol.qq.com/web201310/info-defail.shtml?id="
    champs = wf.cached_data("champs", get_chams, max_age=3600)
    for champ in champs:
        wf.add_item(title=champs[champ][u"name"]+"-"+champs[champ][u"title"],
                    subtitle=detail_url_pre + champ,
                    arg=detail_url_pre + champ,
                    valid=True,
                    icon=get_champ_icon(champ))
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
