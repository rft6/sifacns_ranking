from sifacns import Sifacns 

import sys

if __name__ == '__main__':
    Sifacns.log('カスタマイズサイトへ接続します')
    if(len(sys.argv) >= 2):
        # 引数が2個以上ある場合、引数をユーザIDとパスワードに設定する
        user = sys.argv[1]
        password = sys.argv[2]
    else:
        # それ以外、ユーザIDとパスワードが入力されるまで入力待ち
        while True:
            user = input('ユーザID：')
            if len(user)>0:
                break
        while True:
            password = input('パスワード：')
            if len(password)>0:
                break

    # 処理開始
    sifacns = Sifacns(user, password)
    sifacns.getLiveList()
    sifacns.getRankingDtl()
    sifacns.exportCSV('./ranking.csv', sifacns.rankingDtls)
    