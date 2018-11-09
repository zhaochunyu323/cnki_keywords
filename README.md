# cnki_keywords
Crawl title, year and keywords of papers in CNKI

I used `Selenium+Python3` to crawl keywords of papers in CNKI, some other infos like author and press.

Usage:
---
```python
python3 cnki_test.py -s "the content you want to crawl" -p "total pages"
```

The results are stored in a .csv file

www.cnki.net may have some restricts on crawling data, so when clicking too many pages, you have to input verification code. One trick to solve this problem I think is to select different year in the begining of programming.

Any questions welcome `contact` me (chunyuzhao323@gmail.com)
