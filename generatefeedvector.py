import feedparser
import collections
import re


def getwords(html):
  text = re.compile(r'<[^>]+>').sub('', html)
  words = re.compile(r'[^A-z^a-z]+').split(text)
  return [word.lower() for word in words if word]


def getwordcounts(url):
  d = feedparser.parse(url)
  print d
  wc = collections.defaultdict(int)

  for e in d.entries:
    if 'summary' in e: summary = e.summary
    else: summary = e.description

    words = getwords('%s %s' % (e.title, summary))
    for word in words:
      wc[word] += 1
  return d.feed.title, wc


def main():
  apcount = collections.defaultdict(int)
  wordcounts = {}
  for url in file('feedlist.txt'):
    title, wc = getwordcounts(url)
    wordcounts[title] = wc
    for word, count in wc.iteritems():
      if count > 1:
        apcount[word] += 1

  wordlist = []
  for w, bc in apcount.iteritems():
    frac = float(bc)/len(feedlist)
    if 0.1 < frac < 0.5: wordlist.append(w)

  out = file('blogdata.txt', 'w')
  out.write('Blog')
  for w in wordlist: out.write('\t' + w)
  out.write('\n')
  for blogname, counts in apcount:
    out.write(blogname)
    for w in wordlist:
      if w in counts: out.write('\t' + w)
      else: out.write('\t0')
    out.write('\n')

if __name__ == '__main__':
  main()
