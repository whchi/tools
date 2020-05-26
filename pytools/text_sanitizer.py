# coding=utf-8

from html.parser import HTMLParser
from html import unescape
import unicodedata
import re


class MLStripper(HTMLParser):
    """
        去除 html tag
    """
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def remove_control_characters(s):
    """
        control character: https://en.wikipedia.org/wiki/Control_character
    """
    return ''.join(ch for ch in s if unicodedata.category(ch)[0]!='C')

def strf2h(s):
    """
        全形轉半形
    """
    return unicodedata.normalize('NFKC', s)


def strl2b(s):
    """
        去除空白
    """
    return re.sub(r'\s+', '', s)


def sanitize(s):
    ret = None
    s = unescape(s)
    stripped = MLStripper()
    stripped.feed(s)
    ret = stripped.get_data()
    ret = remove_control_characters(ret)
    ret = strf2h(ret)
    ret = strl2b(ret)
    ret = ret.replace('"', '')

    return ret


if __name__ == "__main__":
    s = """
    <p>比Google和Facebook（臉書）更引人注目的數位時代娛樂帝國Zynga，上週在台灣發表了全球第一款外語版本、繁體中文版的社群網路遊戲德州撲克。</p>
<p>看好亞太區網路社群遊戲的高速成長潛力，成立三年半、總部在美國舊金山的Zynga，今年快手快腳地在日本、印度和北京成立工作室，以收購當地社群遊戲公司的手段，迅速拿下人才和據點。</p>
<p>站在Facebook這個社群網路平台巨人的肩膀上，專門研發社群遊戲的Zynga，只用了兩年半的時間，就拿下了全球一億的使用者，這個紀錄，比Facebook還快了一年半。</p>
<p>根據AppData.com統計，如今每個月有超過二．一億用戶，上線玩它的遊戲，是它最大對手藝電（Electronic Arts）的近四倍。</p>
<p><strong>滑鼠一點　小錢致富<br />

</strong><br />
它的流行程度與主流地位，足以睥睨黃金時段的電視節目。連美國夢工廠動畫公司執行長卡辛伯格（Jeffrey Katzenberg）都說，如果能重新來過，他希望自己能成為Zynga的CEO平克斯（Mark Pincus），「因為他已經
抓住了下一個殺手級應用，將在媒體界掀起濤天巨浪。」</p>
<p>Zynga的遊戲都是免費的，獲利來自於少數玩家願意購買虛擬商品。這些虛擬商品都很便宜，不過幾元幾分美元，可以作為禮物送給朋友，也可以在遊戲中升級，或者僅是裝飾他們的農場或寵物。但每天數以千萬計>的滑鼠點擊累積，讓Zynga今年營收，可望超過五億美元，市值達到四十五億美元。《彭博商業周刊》形容，這家公司正在瘋狂找人，從去年的三百七十五人已激增至一千名員工，而且還有四百個職缺空位在等待。</p>
<p>《時代雜誌》今年曾把Zynga最受歡迎、每月全球用戶近八千萬人的FarmVille農場遊戲，調侃為五十個最糟糕發明的第九名，因為「Zynga這個邪惡天才隱藏在這個令人上癮的遊戲裡，超過十分之一的美國人每天在>搞什麼線上田園，到底有沒有人算過流失了多少生產力？真是對不起『時間』呀！（sorry,TIME!）」</p>
<p>「Zynga遊戲的有趣好玩，在於你仍然能保留你的真實身分，不需要去改換成另一個虛擬人物，你還是在真實世界裡跟你真實的朋友玩、互動；而且，它是休閒的、不是重度的遊戲，是網路生活的一部份，種田、養>魚、開餐廳，主題都很生活化，每天花一點時間看看、玩玩，透過遊戲與人社交，非常自然，」Zynga北京總經理田行智在接受《天下》專訪時表示，社交遊戲牽涉很多心理學因素，這些令人上癮遊戲的背後，是以很強
的數據分析團隊為基礎，以快速分析用戶的行為、喜惡，來做下一步的更新指令，「不斷推出的遊戲新功能，不單是創意，而是有所本的。」<br />
</p>
<p><strong>台灣人超愛玩社群遊戲<br />
</strong><br />
Zynga在台灣沒有據點，但卻選擇繁體中文版為第一個國際版本遊戲，田行智指出，包括中國研發的「開心農場」和Zynga的FarmVille農場遊戲，去年在台灣就曾有每天兩、三百萬人在玩的紀錄，超過Facebook一半以上
的用戶，可見台灣對社群遊戲的接受度非常高，「而且，第一個版本就做有難度的語言，對團隊是很好的鍛鍊。」</p>
<p>曾在Google中國任職兩年多的田行智觀察，和老東家相較，Zynga非常專注，只做最好的遊戲，而且強調速度，「速度是Zynga這家公司六大核心價值裡，最令我印象深刻的一點，沒有公司速度那麼快，光是最近就有
那麼多新聞。」<br />
雖然與Facebook、Google創辦人都是二十多歲就建立起網路帝國相較，四十四歲的平克斯已算大器晚成，但他依然野心勃勃、動作頻頻。</p>
<p>Zynga現在亦開始替雅虎提供遊戲；在iPhone 4的發表會上，平克斯也與蘋果CEO賈伯斯同台宣布，新手機終於可以玩FarmVille了。日本軟銀與Google近期也將挹注其三億美元。《紐約時報》認為，Zynga很可能成為
遊戲界的Google。</p>
<p>Zynga的崛起，像是來自無心插柳的一畝田，但網路社群遊戲的風潮、微利商業模式的應用，都已在新、舊媒體的操盤者與消費者心中，撒下新的種子。<br />
</p>
"""
    print(sanitize(s))
