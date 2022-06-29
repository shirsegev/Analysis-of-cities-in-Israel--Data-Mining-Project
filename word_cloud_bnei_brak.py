from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from bidi.algorithm import get_display

stopwords = ['אני',
    'את',
    'אתה',
    'אנחנו',
    'אתן',
    'אתם',
    'הם',
    'הן',
    'היא',
    'הוא',
    'שלי',
    'שלו',
    'שלך',
    'שלה',
    'שלנו',
    'שלכם',
    'שלכן',
    'שלהם',
    'שלהן',
    'לי',
    'לו',
    'לה',
    'לנו',
    'לכם',
    'לכן',
    'להם',
    'להן',
    'אותה',
    'אותו',
    'זה',
    'זאת',
    'אלה',
    'אלו',
    'תחת',
    'מתחת',
    'מעל',
    'בין',
    'עם',
    'עד',
    'נגר',
    'על',
    'אל',
    'מול',
    'של',
    'אצל',
    'כמו',
    'אחר',
    'אותו',
    'בלי',
    'לפני',
    'אחרי',
    'מאחורי',
    'עלי',
    'עליו',
    'עליה',
    'עליך',
    'עלינו',
    'עליכם',
    'לעיכן',
    'עליהם',
    'עליהן',
    'כל',
    'כולם',
    'כולן',
    'כך',
    'ככה',
    'כזה',
    'זה',
    'זות',
    'אותי',
    'אותה',
    'אותם',
    'אותך',
    'אותו',
    'אותן',
    'אותנו',
    'ואת',
    'את',
    'אתכם',
    'אתכן',
    'איתי',
    'איתו',
    'איתך',
    'איתה',
    'איתם',
    'איתן',
    'איתנו',
    'איתכם',
    'איתכן',
    'יהיה',
    'תהיה',
    'היתי',
    'היתה',
    'היה',
    'להיות',
    'עצמי',
    'עצמו',
    'עצמה',
    'עצמם',
    'עצמן',
    'עצמנו',
    'עצמהם',
    'עצמהן',
    'מי',
    'מה',
    'איפה',
    'היכן',
    'במקום שבו',
    'אם',
    'לאן',
    'למקום שבו',
    'מקום בו',
    'איזה',
    'מהיכן',
    'איך',
    'כיצד',
    'באיזו מידה',
    'מתי',
    'בשעה ש',
    'כאשר',
    'כש',
    'למרות',
    'לפני',
    'אחרי',
    'מאיזו סיבה',
    'הסיבה שבגללה',
    'למה',
    'מדוע',
    'לאיזו תכלית',
    'כי',
    'יש',
    'אין',
    'אך',
    'מנין',
    'מאין',
    'מאיפה',
    'יכל',
    'יכלה',
    'יכלו',
    'יכול',
    'יכולה',
    'יכולים',
    'יכולות',
    'יוכלו',
    'יוכל',
    'מסוגל',
    'לא',
    'רק',
    'אולי',
    'אין',
    'לאו',
    'אי',
    'כלל',
    'נגד',
    'אם',
    'עם',
    'אל',
    'אלה',
    'אלו',
    'אף',
    'על',
    'מעל',
    'מתחת',
    'מצד',
    'בשביל',
    'לבין',
    'באמצע',
    'בתוך',
    'דרך',
    'מבעד',
    'באמצעות',
    'למעלה',
    'למטה',
    'מחוץ',
    'מן',
    'לעבר',
    'מכאן',
    'כאן',
    'הנה',
    'הרי',
    'פה',
    'שם',
    'אך',
    'ברם',
    'שוב',
    'אבל',
    'מבלי',
    'בלי',
    'מלבד',
    'רק',
    'בגלל',
    'מכיוון',
    'עד',
    'אשר',
    'ואילו',
    'למרות',
    'אס',
    'כמו',
    'כפי',
    'אז',
    'אחרי',
    'כן',
    'לכן',
    'לפיכך',
    'מאד',
    'עז',
    'מעט',
    'מעטים',
    'במידה',
    'שוב',
    'יותר',
    'מדי',
    'גם',
    'כן',
    'נו',
    'אחר',
    'אחרת',
    'אחרים',
    'אחרות',
    'שיש',
    'רבה',
    'שבו',
    'מהם',
    'שזה',
    'המקרה',
    'ראה',
    'אמרו',
    'אשר',
    'ועל',
    'נוסף',
    'זו',"בני ברק", "ברק","בבני","סיפר","הצהריים","דונאלד",
    'או']

lst_tlv = ['https://www.ynet.co.il//articles/0,7340,L-5485893,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5623998,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5623669,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5636184,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5640168,00.html','https://www.ynet.co.il//articles/0,7340,L-5444625,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5453917,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5456057,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5457420,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5458514,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5466969,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5469929,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5486334,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5494135,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5498330,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5502758,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5505674,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5505703,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5509768,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5511089,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5515906,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5521542,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5522367,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5522415,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5525166,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5545465,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5553367,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5555084,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5555196,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5557225,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5561529,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5567513,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5575464,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5579625,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5598033,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5598325,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5615553,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5615761,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5625829,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5635685,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5642984,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5644702,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5647589,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5647858,00.html','https://www.ynet.co.il//articles/0,7340,L-5444403,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5454897,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5489980,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5497462,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5497924,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5498783,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5499380,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5502651,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5502792,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5504151,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5510297,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5521857,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5522063,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5531264,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5539365,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5542024,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5551808,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5553665,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5554706,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5556365,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5557850,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5567963,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5569151,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5575171,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5584954,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5594710,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5602843,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5603190,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5614663,00.html','https://www.ynet.co.il//articles/0,7340,L-5577859,00.html','https://www.ynet.co.il//articles/0,7340,L-5462093,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5465645,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5473565,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5485579,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5495800,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5521184,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5575946,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5618246,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5622660,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5635250,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5648897,00.html']
lst_bnei_brak = ['https://www.ynet.co.il//articles/0,7340,L-5521223,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5521223,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5521160,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5555366,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5558275,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5567597,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5633844,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5638344,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5641338,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5643134,00.html','https://www.ynet.co.il//articles/0,7340,L-5523338,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5558110,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5558363,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5568105,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5571321,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5636200,00.html']
lst_sderot = ['https://www.ynet.co.il//articles/0,7340,L-5619149,00.html','https://www.ynet.co.il//articles/0,7340,L-5475384,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5497653,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5517782,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5564240,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5608736,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5617621,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5617847,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5624763,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5629248,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5631380,00.html','https://www.ynet.co.il//articles/0,7340,L-5484154,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5484345,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5484381,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5487890,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5506749,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5524988,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5525068,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5525181,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5570992,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5574249,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5575495,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5583406,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5592731,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5617566,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5617594,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5617664,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5617880,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5618184,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5618278,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5618999,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5624005,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5624947,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5632307,00.html', 'https://www.ynet.co.il//articles/0,7340,L-5639035,00.html']

comment_words = ''
for url in lst_tlv:
    main_page = requests.get(url)
    webpage_html = main_page.text
    soup = BeautifulSoup(webpage_html, 'html.parser')
    for p in soup.find_all("p"):
        comment_words += p.text
    print(comment_words)

print(comment_words)
tokens = comment_words.split()
comment_words += " ".join(tokens) + " "

bidi_text = get_display(comment_words)

stopwords_flip_set = set()
for word in stopwords:
    new_word = get_display(word)
    stopwords_flip_set.add(new_word)

print(stopwords_flip_set)

wordcloud = WordCloud(
        font_path = 'C:\Windows\Fonts\courbd.ttf',
        background_color='white',
        stopwords=stopwords_flip_set,
        max_words=100,
        max_font_size=50,width=300,height=300,
        scale=5,
        random_state=1).generate(bidi_text)

plt.figure(figsize=(3, 3), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()