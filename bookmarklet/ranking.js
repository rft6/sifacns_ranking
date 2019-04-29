javascript: ( function run(){ var baseUrl = 'https://members.lovelive-sifacns.jp'; function httpGet(url){ var html = $.ajax({ url: url, async: false }).responseText; return html; } function getNextUrl(html){ return html.match(/<a href="(.*?)" rel="next">/)[1]; } function downloadCSV(data){ /* BLOBを作成 */ var blob = new Blob([data],{type:"text/csv"}); /* URLを作成 */ var url = URL.createObjectURL(blob); /* UserAgentを取得 */ var agent = window.navigator.userAgent.toLowerCase(); console.log(agent); /* ブラウザ別処理 */ if(agent.indexOf('trident/7') > -1) { console.log("ブラウザ:ie"); window.navigator.msSaveBlob(blob,"ranking.csv"); } else if(agent.indexOf('edge') > -1) { console.log("ブラウザ:edge"); } else if(agent.indexOf('chrome') > -1) { console.log("ブラウザ:chrome"); window.location.href = url; } else if(agent.indexOf('safari') > -1) { console.log("ブラウザ:safari"); } else if(agent.indexOf('firefox') > -1) { console.log("ブラウザ:firefox"); } else { console.log("ブラウザ:その他"); } /* URLを削除 */ URL.revokeObjectURL(url); } /* 曲名を取得する */ function getTitle(html){ return html.match(/<div class="live_data_name">(.*?)<\/div>/)[1] .replace("&ldquo;","“") .replace("&rdquo;","”") .replace("&amp;","&") .replace("&rarr;","→") .replace("&hearts;","♡"); } /* 順位を取得する */ function getRank(html){ var rank = html.match(/<span class="fwb">(.*?)<\/span>位/); if(rank == null){ return "0"; }else{ return rank[1]; } } /* 1位との差を取得する */ function getScoreDiff(html){ var myScore = html.match(/<span class="fwb fsl">(.*?)<\/span>/); if(myScore == null){ myScore = 0; }else{ myScore = parseInt(myScore[1],10); } var firstScore = html.match(/<div class="rankings_live_score">(.*?)<span class="fsxs italic"/); if(firstScore == null){ firstScore = html.match(/<div class="rankings_live_score">(.*?)<\/div>/); } if(firstScore == null){ firstScore = 0; }else{ firstScore = parseInt(firstScore[1],10); } return myScore - firstScore; } /* livecdを取得する */ function getLiveCd(html){ var list1 = html.match(/<option value="(.*?)"/g); var list2 = new Array(); for(var i = 0;i<list1.length; i++){ list2.push(list1[i].match(/<option value="(.*?)"/)[1]); } return list2; } /* 全難易度のランキング詳細を取得 */ function getRankingDtlUrl(url){ var rankingUrl = "https://members.lovelive-sifacns.jp/rank/livedetail?music=10&c=2&live_id="; html = httpGet(baseUrl + url); var list = getLiveCd(html); var title = getTitle(html); var record = ""; record = record + "\"" + title + "\","; for(var i = 0; i < list.length; i++){ html = httpGet(rankingUrl + list[i]); var rank = getRank(html); var diff = getScoreDiff(html); record = record + rank + "(" + diff + ")," } record = record.slice(0,-1); console.log(record); return record; } /* ランキング詳細ページを取得 */ function getRankingDtl(html){ var list1 = html.match(/<div class="table-cell100">((.|[\s\S])*?)<a href="(.*?)">/g); var list2 = new Array(); for(var i = 0; i < list1.length; i++){ /* 楽曲のランキングのURLを取得 */ list2.push(getRankingDtlUrl(list1[i].match(/<a href="(.*?)">/)[1])); } return list2; } /* 楽曲ランキングを取得する */ function getLiveList(url){ var end = "#"; var list = new Array(); var html = ''; do{ /* 楽曲ランキング一覧ページを取得 */ html = httpGet(baseUrl + url); /* 一覧内のレコードリストを取得する */ list = list.concat(getRankingDtl(html)); /* 次のページのURLを取得 */ url = getNextUrl(html); }while(url != end); return list; } /* ランキング情報を取得する */ function getRanking(){ /* テクニカルランキング楽曲一覧ページ */ var urlM = '/rank/live?mode=1&c=2&page=1'; var urlA = '/rank/live?mode=2&c=2&page=1'; var list = ["楽曲名,EASY,NORMAL,HARD,EXTREME,CHALLENGE,PLUS,COMBO,SWITCH"]; /* ランキングデータのレコードリストを取得 */ list = list.concat(getLiveList(urlM)); list = list.concat(getLiveList(urlA)); return list; } setTimeout(downloadCSV(getRanking().join("\r\n")),0); } )()
