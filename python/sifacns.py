import sys
from datetime import datetime
import requests as rq
import re
import html
import csv

class Sifacns:
    __session = None
    __dtlUrlList = []
    rankingDtls = ['楽曲名,EASY,NORMAL,HARD,EXTREME,CHALLENGE,PLUS,COMBO,SWITCH']

    def __init__(self, user, password):
        self.__user = user
        self.__password = password
        self.__login()

    def __login(self):
        self.log('ログインを開始します')
        # ログインページ
        url = 'https://members.lovelive-sifacns.jp/mypage/login'
        # セッション作成
        self.__session = rq.Session()
        # ログインページへアクセス
        result = self.__session.post(url)
        # ステータスコードをチェック
        if result.status_code != 200:
            self.log('ログインページへアクセスできませんでした')
            self.log('ステータスコード：' + str(result.status_code))
            exit()
        
        # ログインAPI取得
        pattern = '<form id="loginForm" name="login" method="post" action="(.*?)">'
        outhUrl = re.findall(pattern, result.text)

        if outhUrl:
            outhUrl = 'https://secure.square-enix.com/oauth/oa/' + outhUrl[0]
        else:
            self.log('ログインAPIを取得できませんでした')
            exit()
        
        # POSTパラメータを取得
        pattern = '<input type="hidden" name="_STORED_" value="(.*?)"'
        stored = re.findall(pattern, result.text)

        if stored:
            stored = stored[0]
        else:
            self.log('_STORED_を取得できませんでした')
            exit()

        # ログイン
        result = self.__session.post(outhUrl,data={'_STORED_':stored, 'sqexid':self.__user, 'password':self.__password})
        if result.status_code != 200:
            self.log('ログインに失敗しました')
            self.log('ステータスコード：' + str(result.status_code))
            exit()

        self.log('セッションチェック中')
        # セッションチェック
        pattern = '<form name="mainForm" method="post" action="(.*?)">'
        sessionCheckUrl = re.findall(pattern, result.text)
        if sessionCheckUrl:
            sessionCheckUrl = sessionCheckUrl[0]
        else:
            self.log('セッションチェックURLの取得に失敗しました')
            exit()

        pattern = '<input name="cis_sessid" type="hidden" value="(.*?)">'
        cis_sessid = re.findall(pattern, result.text)
        if cis_sessid:
            cis_sessid = cis_sessid[0]
        else:
            self.log('cis_sessidの取得に失敗しました')
            exit()

        pattern = '<input name="provision" type="hidden" value="(.*?)">'
        provision = re.findall(pattern, result.text)
        if provision:
            provision = provision[0]
        else:
            self.log('provisionの取得に失敗しました')
            exit()

        pattern = '<input name="_c" type="hidden" value="(.*?)">'
        _c = re.findall(pattern, result.text)
        if _c:
            _c = _c[0]
        else:
            self.log('_cの取得に失敗しました')
            exit()

        result = self.__session.post(sessionCheckUrl,data={'cis_sessid':cis_sessid, 'provision':provision, '_c':_c})
        if result.status_code != 200:
            self.log('ログインに失敗しました')
            self.log('ステータスコード：' + str(result.status_code))
            exit()
        
        pattern = '<div class="profile_player_name">(.*?)</div>'
        username = re.findall(pattern, result.text, re.S)
        self.log('ログインに成功しました')
        self.log('ユーザ名：' + html.unescape(username[0]))

    def getLiveList(self):
        baseUrl = 'https://members.lovelive-sifacns.jp'
        # μ's
        url1 = '/rank/live?mode=1&c=2&page=1'
        # Aqours
        url2 = '/rank/live?mode=2&c=2&page=1'
        # SaintSnow
        url3 = '/rank/live?mode=3&c=2&page=1'

        self.log('楽曲一覧を取得します')

        # μ'sを取得
        while True:
            # URL作成
            url = baseUrl + url1
            # 取得
            result = self.__session.post(url)
            if result.status_code != 200:
                self.log('楽曲一覧の取得に失敗しました')
                self.log('ステータスコード：' + str(result.status_code))
                exit()
            
            # 詳細URL取得
            pattern = '<div class="table-cell100">(.*?)<a href="(.*?)">'
            list = re.findall(pattern, result.text, re.S)
            if list:
                for l in list:
                    self.__dtlUrlList.append(baseUrl + l[1])
            else:
                self.log('詳細URLの取得に失敗しました')
            # 次のページを取得
            pattern = '<a href="(.*)" rel="next">'
            url1 = re.findall(pattern, result.text)
            if url1:
                if url1[0] == '#':
                    break
                else:
                    url1 = url1[0]
            else:
                self.log('次のページの取得に失敗しました')
                exit()

        # Aqoursを取得
        while True:
            # URL作成
            url = baseUrl + url2
            # 取得
            result = self.__session.post(url)
            if result.status_code != 200:
                self.log('楽曲一覧の取得に失敗しました')
                self.log('ステータスコード：' + str(result.status_code))
                exit()
            
            # 詳細URL取得
            pattern = '<div class="table-cell100">(.*?)<a href="(.*?)">'
            list = re.findall(pattern, result.text, re.S)
            if list:
                for l in list:
                    self.__dtlUrlList.append(baseUrl + l[1])

            # 次のページを取得
            pattern = '<a href="(.*)" rel="next">'
            url2 = re.findall(pattern, result.text)
            if url2:
                if url2[0] == '#':
                    break
                else:
                    url2 = url2[0]
            else:
                self.log('次のページの取得に失敗しました')
                exit()

        # SaintSnowを取得
        while True:
            # URL作成
            url = baseUrl + url3
            # 取得
            result = self.__session.post(url)
            if result.status_code != 200:
                self.log('楽曲一覧の取得に失敗しました')
                self.log('ステータスコード：' + str(result.status_code))
                exit()
            
            # 詳細URL取得
            pattern = '<div class="table-cell100">(.*?)<a href="(.*?)">'
            list = re.findall(pattern, result.text, re.S)
            if list:
                for l in list:
                    self.__dtlUrlList.append(baseUrl + l[1])

            # 次のページを取得
            #pattern = '<a href="(.*)" rel="next">'
            #url3 = re.findall(pattern, result.text)
            #if url3:
            #    if url3[0] == '#':
            #        break
            #    else:
            #        url3 = url3[0]
            #else:
            #    self.log('次のページの取得に失敗しました')
            #    exit()

            break;

        self.log(str(self.getLiveListCount()) + '件取得しました')
    
    def getLiveListCount(self):
        return len(self.__dtlUrlList)

    def getRankingDtl(self):
        self.log('ランキング情報を取得します')
        # 詳細URL
        url = 'https://members.lovelive-sifacns.jp/rank/livedetail'
        # 件数カウント
        i = 1
        # 楽曲一覧ループ
        for dtlUrl in self.__dtlUrlList:
            record = None
            result = self.__session.post(dtlUrl)
            if result.status_code != 200:
                self.log('ランキング詳細の取得に失敗しました')
                self.log('ステータスコード：' + str(result.status_code))
                exit()

            # タイトル取得
            pattern = '<div class="live_data_name">(.*?)</div>'
            title = re.findall(pattern, result.text)
            if title:
                title = html.unescape(title[0])
                record = '"' + title + '"'
            else:
                self.log('タイトルの取得に失敗しました')
                exit()

            # 各難易度の詳細URL作成
            pattern = '<option value="(.*?)"'
            liveidList = re.findall(pattern, result.text)
            if not liveidList:
                self.log('liveidの取得に失敗しました')
                exit()
            pattern = '<input type="hidden" name="music" value="(.*?)">'
            music = re.findall(pattern, result.text)
            if music:
                music = music[0]
            else:
                self.log('musicの取得に失敗しました')
                exit()
            pattern = '<input type="hidden" name="c" value="(.*?)">'
            c = re.findall(pattern, result.text)
            if c:
                c = c[0]
            else:
                self.log('cの取得に失敗しました')
                exit()

            for liveid in liveidList:
                result2 = self.__session.get(url, params={'live_id':liveid, 'music':music, 'c':c})
                if result2.status_code != 200:
                    self.log('ランキング詳細の取得に失敗しました')
                    self.log('ステータスコード：' + str(result2.status_code))
                    exit()
                dtl = self.__parseRankingDtl(result2.text)
                record = record + ',' +dtl['rank'] + '(' + str(dtl['diff']) + ')'

            self.rankingDtls.append(record)
            self.log('(' + format(i,"02d") +'/' + str(self.getLiveListCount()) + ')' + title)
            i = i + 1 
    
    def __parseRankingDtl(self,text):
        # 順位
        pattern = '<span class="fwb">(.*?)</span>位</div>'
        rank = re.findall(pattern, text)
        if rank:
            rank = rank[0]
        else:
            rank = '-'
        # スコア
        pattern = '<span class="fwb fsl">(.*?)</span>'
        score = re.findall(pattern, text)
        if score:
            score = int(score[0])
        else:
            score = 0

        # 1位のスコア
        pattern = '<div class="rankings_live_score">(.*?)<'
        score1st = re.findall(pattern, text)
        if score1st:
            score1st = int(score1st[0])
        else:
            score1st = 0

        # 点差
        diff = score - score1st

        return {'rank':rank, 'score':score, 'diff':diff}


    def exportCSV(self, file, data):
        with open(file,mode='w',encoding='utf8') as f:
            f.write('\n'.join(data))

    @staticmethod
    def log(msg, end="\n"):
        print('[' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ']' + msg, end=end)