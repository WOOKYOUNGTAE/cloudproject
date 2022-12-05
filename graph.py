import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

#%config InlineBackend.figure_format='retina'

#!apt -qq -y install fonts-nanum

import matplotlib.font_manager as fm
fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
font = fm.FontProperties(fname=fontpath, size =10)
plt.rc('font', family='NanumBarunGothic')
mpl.font_manager._rebuild()

#!set -x \
#&& pip install konlpy \
#&& curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash -x

#pip install pandas

import urllib.request

raw = urllib.request.urlopen('https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt').readlines()
print(raw[:5])

reviews = raw['text']
result = ' '.join(s for s in reviews)

print(result[:300])


from konlpy.tag import Mecab
tagger = Mecab()

nouns = []
for review in reviews:
  for noun in tagger.nouns(review):
    nouns.append(noun)

nouns[:10]

#pip install konlpy

stop_words = "영화 전 난 일 걸 뭐 줄 만 건 분 개 끝 잼 이거 번 중 듯 때 게 내 말 나 수 거 점 것"
stop_words = stop_words.split(' ')
print(stop_words)

nouns = []
for review in reviews:
  for noun in tagger.nouns(review):
    if noun not in stop_words:
      nouns.append(noun)

nouns[:10]

from collections import Counter

nouns_counter = Counter(nouns)
top_nouns = dict(nouns_counter.most_common(50))
top_nouns

import numpy as np

y_pos = np.arange(len(top_nouns))

plt.figure(figsize=(12,12))
plt.barh(y_pos, top_nouns.values())
plt.title('Word Count')
plt.yticks(y_pos,top_nouns.keys())
plt.show()

#!pip install wordcloud

from wordcloud import WordCloud

wc = WordCloud(background_color='white',font_path='./font/NanumBarunGothic.ttf')
wc.generate_from_frequencies(top_nouns)

figure = plt.figure(figsize=(12,12))
ax = figure.add_subplot(1,1,1)
ax.axis('off')
ax.imshow(wc)
plt.show()

#!pip install squarify

import squarify

norm = mpl.colors.Normalize(vmin = min(top_nouns.values()),
                            vmax = max(top_nouns.values()))
colors = [mpl.cm.Blues(norm(value)) for value in top_nouns.values()]

squarify.plot(label=top_nouns.keys(),
              sizes=top_nouns.values(),
              color=colors,
              alpha=.7);