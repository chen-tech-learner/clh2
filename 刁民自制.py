# -*- coding: utf-8 -*-
# TVBox / 影视仓 Python 爬虫
import sys
import re
import json
import base64
import html
from urllib.parse import quote, unquote, urljoin

sys.path.append('..')
try:
    from base.spider import Spider
except Exception:
    class Spider(object):
        pass


class Spider(Spider):
    def getName(self):
        return 'N2影视'

    def init(self, extend=''):
        pass

    host = 'https://www.n2d4z.top'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36 Chrome/120.0 Safari/537.36',
        'Referer': 'https://www.n2d4z.top/index/home.html',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    # 首页分区。图片、小说、博彩、外跳广告类入口未放入影视分类。
    classes = [
        {'type_name': '最新剧情', 'type_id': 'juqing'},
        {'type_name': '最新电影', 'type_id': 'shipin'},
        {'type_name': '最新精选', 'type_id': 'jingpin'},
        {'type_name': '剧情-麻豆传媒', 'type_id': 'juqing|麻豆传媒'},
        {'type_name': '剧情-天美传媒', 'type_id': 'juqing|天美传媒'},
        {'type_name': '剧情-星空果冻', 'type_id': 'juqing|星空果冻'},
        {'type_name': '剧情-蜜桃精东', 'type_id': 'juqing|蜜桃精东'},
        {'type_name': '剧情-韩国伦理', 'type_id': 'juqing|韩国伦理'},
        {'type_name': '剧情-COSPLAY', 'type_id': 'juqing|COSPLAY'},
        {'type_name': '剧情-经典三级', 'type_id': 'juqing|经典三级'},
        {'type_name': '剧情-中文字幕', 'type_id': 'juqing|中文字幕'},
        {'type_name': '电影-日本av', 'type_id': 'shipin|日本av'},
        {'type_name': '电影-韩国热舞', 'type_id': 'shipin|韩国热舞'},
        {'type_name': '电影-欧美精品', 'type_id': 'shipin|欧美精品'},
        {'type_name': '电影-动漫电影', 'type_id': 'shipin|动漫电影'},
        {'type_name': '电影-国产自拍', 'type_id': 'shipin|国产自拍'},
        {'type_name': '电影-岛国无码', 'type_id': 'shipin|岛国无码'},
        {'type_name': '电影-JVID', 'type_id': 'shipin|JVID'},
        {'type_name': '电影-SM调教', 'type_id': 'shipin|SM调教'},
        {'type_name': '精品-软萌福利姬', 'type_id': 'jingpin|软萌福利姬'},
        {'type_name': '精品-黑料头条', 'type_id': 'jingpin|黑料头条'},
        {'type_name': '精品-明星AI', 'type_id': 'jingpin|明星AI'},
        {'type_name': '精品-人妖伪娘', 'type_id': 'jingpin|人妖伪娘'},
        {'type_name': '精品-onlyfans', 'type_id': 'jingpin|onlyfans'},
        {'type_name': '精品-探花系列', 'type_id': 'jingpin|探花系列'},
        {'type_name': '精品-主播大秀', 'type_id': 'jingpin|主播大秀'},
        {'type_name': '精品-韩国主播', 'type_id': 'jingpin|韩国主播'},
    ]

    filters = {
        'juqing': [
            {'key': 'tag', 'name': '剧情筛选', 'value': [
                {'n': '全部', 'v': ''}, {'n': '麻豆传媒', 'v': '麻豆传媒'}, {'n': '天美传媒', 'v': '天美传媒'},
                {'n': '星空果冻', 'v': '星空果冻'}, {'n': '蜜桃精东', 'v': '蜜桃精东'}, {'n': '韩国伦理', 'v': '韩国伦理'},
                {'n': 'COSPLAY', 'v': 'COSPLAY'}, {'n': '经典三级', 'v': '经典三级'}, {'n': '中文字幕', 'v': '中文字幕'},
            ]},
        ],
        'shipin': [
            {'key': 'tag', 'name': '电影筛选', 'value': [
                {'n': '全部', 'v': ''}, {'n': '日本av', 'v': '日本av'}, {'n': '韩国热舞', 'v': '韩国热舞'},
                {'n': '欧美精品', 'v': '欧美精品'}, {'n': '动漫电影', 'v': '动漫电影'}, {'n': '国产自拍', 'v': '国产自拍'},
                {'n': '岛国无码', 'v': '岛国无码'}, {'n': 'JVID', 'v': 'JVID'}, {'n': 'SM调教', 'v': 'SM调教'},
            ]},
        ],
        'jingpin': [
            {'key': 'tag', 'name': '精品筛选', 'value': [
                {'n': '全部', 'v': ''}, {'n': '软萌福利姬', 'v': '软萌福利姬'}, {'n': '黑料头条', 'v': '黑料头条'},
                {'n': '明星AI', 'v': '明星AI'}, {'n': '人妖伪娘', 'v': '人妖伪娘'}, {'n': 'onlyfans', 'v': 'onlyfans'},
                {'n': '探花系列', 'v': '探花系列'}, {'n': '主播大秀', 'v': '主播大秀'}, {'n': '韩国主播', 'v': '韩国主播'},
            ]},
        ],
    }

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    def homeContent(self, filter):
        result = {'class': self.classes}
        if filter:
            result['filters'] = self.filters
        return result

    def homeVideoContent(self):
        html_text = self.fetch(self.host + '/index/home.html')
        return {'list': self.parse_vod_list(html_text)[:30]}

    def categoryContent(self, tid, pg, filter, extend):
        pg = int(pg or 1)
        channel, tag = self.split_tid(tid)
        if extend and extend.get('tag'):
            tag = extend.get('tag')
        url = self.build_list_url(channel, tag, pg)
        html_text = self.fetch(url)
        vods = self.parse_vod_list(html_text)
        total = self.parse_total_page(html_text)
        return {
            'page': pg,
            'pagecount': total if total > 0 else (pg + 1 if vods else pg),
            'limit': 20,
            'total': (total if total > 0 else pg + 1) * 20,
            'list': vods,
        }

    def detailContent(self, ids):
        vod_id = ids[0]
        url = self.abs_url(vod_id)
        html_text = self.fetch(url)
        title = self.parse_detail_title(html_text) or self.title_from_id(vod_id)
        pic = self.parse_detail_pic(html_text)
        date = self.search_first(r'<div class="video-item-date">([^<]+)', html_text)
        vod = {
            'vod_id': vod_id,
            'vod_name': title,
            'vod_pic': pic,
            'type_name': '',
            'vod_year': date or '',
            'vod_area': '',
            'vod_remarks': date or '播放',
            'vod_actor': '',
            'vod_director': '',
            'vod_content': title,
            'vod_play_from': '线路一$$$线路二',
            'vod_play_url': '播放$%s#备用$%s' % (vod_id + '@1', vod_id + '@2'),
        }
        return {'list': [vod]}

    def searchContent(self, key, quick, pg='1'):
        return self.searchContentPage(key, quick, pg)

    def searchContentPage(self, key, quick, pg):
        # 网页搜索入口要求 keyword=encodeString(keyword)，也就是 UTF-8 base64。
        kw = base64.b64encode(key.encode('utf-8')).decode('utf-8')
        url = self.host + '/search/index.html?keyword=' + quote(kw)
        html_text = self.fetch(url)
        vods = self.parse_vod_list(html_text)
        return {'page': int(pg or 1), 'pagecount': 1, 'limit': 20, 'total': len(vods), 'list': vods}

    def playerContent(self, flag, id, vipFlags):
        # id 格式：播放页地址@线路号。网页脚本为：(road == 1 ? m3u8_host : m3u8_host1) + video
        if '@' in id:
            page_id, road = id.rsplit('@', 1)
        else:
            page_id, road = id, '1'
        html_text = self.fetch(self.abs_url(page_id))
        video = self.b64_from_js(html_text, 'video')
        host1 = self.b64_from_js(html_text, 'm3u8_host')
        host2 = self.b64_from_js(html_text, 'm3u8_host1')
        play_host = host1 if str(road) == '1' else (host2 or host1)
        play_url = urljoin(play_host or self.host, video or '')
        return {
            'parse': 0,
            'playUrl': '',
            'url': play_url,
            'header': {
                'User-Agent': self.headers['User-Agent'],
                'Referer': self.abs_url(page_id),
            },
        }

    def localProxy(self, params):
        return [404, 'text/plain', '']

    def fetch(self, url):
        try:
            rsp = super().fetch(url, headers=self.headers)
            if isinstance(rsp, dict):
                return rsp.get('content') or rsp.get('body') or ''
            return rsp.text
        except Exception:
            try:
                import requests
                return requests.get(url, headers=self.headers, timeout=15).text
            except Exception:
                return ''

    def parse_vod_list(self, html_text):
        vods = []
        if not html_text:
            return vods
        blocks = re.findall(r'<a\s+class="video-item"[\s\S]*?</a>', html_text)
        for block in blocks:
            href = self.search_first(r'href="([^"]+)"', block)
            if not href:
                continue
            pic = self.search_first(r'<img[^>]+data-base64="([^"]+)"', block)
            title_enc = self.search_first(r'<div[^>]+video-item-title[^>]+title="([^"]*)"', block)
            title = self.decode_title(title_enc)
            if not title:
                title = self.search_first(r'<div[^>]+video-item-title[^>]*>([\s\S]*?)</div>', block)
                title = self.clean_text(title)
            date = self.search_first(r'<div class="video-item-date">([^<]+)', block)
            if not title:
                title = self.title_from_id(href)
            vods.append({
                'vod_id': href,
                'vod_name': title,
                'vod_pic': self.abs_url(pic),
                'vod_remarks': date or '播放',
            })
        return self.dedupe(vods)

    def parse_detail_title(self, html_text):
        # 详情页主标题通常在 dec-ti 的 title 属性里加密。
        candidates = re.findall(r'class="[^"]*dec-ti[^"]*"[^>]*title="([^"]+)"', html_text)
        for item in candidates:
            txt = self.decode_title(item)
            if txt and len(txt) > 2 and '首页' not in txt:
                return txt
        return ''

    def parse_detail_pic(self, html_text):
        pic = self.search_first(r'<img[^>]+data-base64="([^"]+)"', html_text)
        return self.abs_url(pic)

    def parse_total_page(self, html_text):
        nums = re.findall(r'title=["\']第"?(\d+)"?页["\']', html_text)
        nums += re.findall(r'>(\d+)</a>', html_text)
        arr = []
        for n in nums:
            try:
                arr.append(int(n))
            except Exception:
                pass
        return max(arr) if arr else 0

    def split_tid(self, tid):
        if '|' in tid:
            channel, tag = tid.split('|', 1)
        else:
            channel, tag = tid, ''
        return channel, tag

    def build_list_url(self, channel, tag, pg):
        if tag:
            if int(pg) <= 1:
                path = '/%s/list-%s.html' % (channel, tag)
            else:
                path = '/%s/list-%s-%s.html' % (channel, tag, pg)
        else:
            if int(pg) <= 1:
                path = '/%s/list.html' % channel
            else:
                path = '/%s/list-%s.html' % (channel, pg)
        return self.host + '/' + self.encode_path(path) + '.html'

    def encode_path(self, path):
        return 'cYc' + base64.b64encode(path.encode('utf-8')).decode('utf-8')

    def decode_path(self, encoded):
        try:
            s = encoded
            s = s.split('?', 1)[0]
            s = s.rsplit('.html', 1)[0]
            if '/' in s:
                s = s.rsplit('/', 1)[-1]
            s = unquote(s)
            if s.startswith('cYc'):
                s = s[3:]
            return base64.b64decode(s + '===').decode('utf-8')
        except Exception:
            return encoded

    def b64_from_js(self, html_text, var_name):
        pattern = r'var\s+' + re.escape(var_name) + r'\s*=\s*decodeString\([\'"]([^\'"]+)[\'"]\)'
        enc = self.search_first(pattern, html_text)
        if not enc:
            return ''
        return self.decode_base64_utf8(enc)

    def decode_base64_utf8(self, data):
        try:
            return base64.b64decode(data + '===').decode('utf-8')
        except Exception:
            return ''

    def decode_title(self, data):
        data = html.unescape(data or '').strip()
        if not data:
            return ''
        # 少数内容本身就是明文或普通 base64。
        if self.has_cn(data):
            return data
        txt = self.decode_base64_utf8(data)
        if txt and self.has_readable(txt):
            return txt
        # 页面 decodeString2 使用 AES-CBC 解密，suffix 固定为 883346。
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
            key = base64.b64decode('SWRUSnEwSGtscHVJNm11OGlCJU9PQCF2ZF40SyZ1WFc=')
            iv = base64.b64decode('JDB2QGtySDdWMg==') + b'883346'
            raw = base64.b64decode(data + '===')
            dec = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(raw), AES.block_size)
            return dec.decode('utf-8', 'ignore').replace('"', '').strip()
        except Exception:
            return ''

    def title_from_id(self, href):
        path = self.decode_path(href)
        m = re.search(r'play-(\d+)', path)
        return '视频' + (m.group(1) if m else '')

    def abs_url(self, url):
        if not url:
            return ''
        url = html.unescape(url)
        if url.startswith('//'):
            return 'https:' + url
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return urljoin(self.host, url)

    def clean_text(self, text):
        text = re.sub(r'<[^>]+>', ' ', text or '')
        text = html.unescape(text)
        return re.sub(r'\s+', ' ', text).strip()

    def search_first(self, pattern, text):
        m = re.search(pattern, text or '', re.S)
        return html.unescape(m.group(1).strip()) if m else ''

    def has_cn(self, text):
        return bool(re.search(r'[\u4e00-\u9fff]', text or ''))

    def has_readable(self, text):
        return bool(re.search(r'[\u4e00-\u9fffA-Za-z0-9]', text or ''))

    def dedupe(self, vods):
        seen = set()
        out = []
        for v in vods:
            vid = v.get('vod_id')
            if vid and vid not in seen:
                seen.add(vid)
                out.append(v)
        return out
