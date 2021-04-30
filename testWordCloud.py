from wordcloud import WordCloud
import json
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
import MeCab

def get_tweet_timeline(user_id, count):
    result = []
    RESPONSE_STATUS_OK = 200
    CK = "F4CePTFDSzzNPWy1gtroWt0uG"
    CS = "ujQjfMYDiAreIT9z3m1JKmci1s0FgIDKwo8pJzoRpEqw1g2s0U"
    AT = "1407219055-1ZlToB4NmTRs8Wcl9FUZfbH6sWJMFKNhaVV3FPD"
    ATS = "olA7RsVeSOjXO1Z6ULBodJaI6OhsLMAu0FNm4nIkn7x0l"

    twitter = OAuth1Session(CK, CS, AT, ATS)  # 認証処理

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=" + user_id  # タイムライン取得エンドポイント

    params = {'count': count}

    res = twitter.get(url, params=params)

    if res.status_code == RESPONSE_STATUS_OK:
        timelines = json.loads(res.text)
        for line in timelines:
            result.append(line['text'])
    else:
        print("Faild %d" % res.status_code)

    return result

def work_cloud(text):

    wordcloud = WordCloud(font_path="/Users/omori/.font/Noto-unhinted/NotoSansCJKjp-Medium.otf", background_color="white", height=300,
                          width=300).generate(text)
    WordCloud.to_file(wordcloud, "./wordcloud.png")

def create_separate_blank_text(text):
    mecab = MeCab.Tagger("-Ochasen")
    BLANK = " ";
    result = "";
    parse_text = mecab.parseToNode(text)
    while parse_text:
        result += parse_text.surface + BLANK
        parse_text = parse_text.next
    return result

if __name__ == "__main__":
    print("program start")
    FANCREW_ACCOUNT_ID = "85751721"
    get_tweet_count = 100
    timeline = get_tweet_timeline(FANCREW_ACCOUNT_ID, get_tweet_count)
    text = ""
    for line in timeline:
        text += line
    separated_text = create_separate_blank_text(text)
    work_cloud(separated_text)
    print("program end")