# Loads data
from tqdm import tqdm
import json
import re
import praw
downloadFiles = False

# Method to clean strings
def formatStr(inp):
    string = re.sub("[\r\n]+", '\n', inp)
    return string.replace("#**Please do not vote on your own submissions.**", "").replace(",", "%2C").strip()


if downloadFiles:
    # Load country and city list
    with open("data.csv", 'r', encoding='utf-8') as inp:
        countries = []
        cities = []
        lines = inp.readlines()

        for x in range(1, int(lines[0].replace("\n", ""))):
            cities.append(lines[x].split("\t")[0].replace("\n", ""))

        for x in range(int(lines[0].replace("\n", "")), len(lines)):
            countries.append(lines[x].split("\t")[0].replace("\n", ""))


    # Load and create reddit object
    with open("settings.json", 'r') as sett:
        settings = json.loads(sett.read())
        reddit = praw.Reddit(client_id=settings['client_id'],
                            client_secret=settings['client_secret'],
                            user_agent=settings['user_agent'],
                            username=settings['username'],
                            password=settings['password'])

    sub = reddit.subreddit('all')
    print(formatStr(reddit.submission(url="https://www.reddit.com/r/90DayFiance/comments/eeoof4/i_do_pay_taxes_and_i_pay_a_lot_a_loving_recap_of/?utm_source=share&utm_medium=web2x").selftext))
    # Do countries
    with open("countries.csv", 'w+', encoding='utf-8') as out:
        out.write("Country,Upvotes,Date epoch,Link,Comments #,Post title,Post content,Content of the most upvoted comment\n")
        for c in tqdm(range(0,len(countries))):
            itx = 0
            for i in sub.search("{} tap water".format(countries[c]), limit=10):
                if i.is_self and itx < 5:
                    i.comment_sort = "top"
                    try:
                        print("")
                        print(formatStr(i.comments.list()[0].body))
                        print("")
                        out.write("{},{},{},{},{},{},{},{}\n".format(countries[c], i.score, i.created_utc, "https://www.reddit.com" +
                                                                    i.permalink, i.num_comments, formatStr(i.title), formatStr(i.selftext), formatStr(i.comments.list()[0].body)))
                        itx += 1
                    except:
                        continue


    # Do cities
    with open("cities.csv", 'w+', encoding='utf-8') as out:
        out.write("City,Upvotes,Date epoch,Link,Comments #,Post title,Post content,Content of the most upvoted comment\n")
        for c in tqdm(range(0,len(cities))):
            itx = 0
            for i in sub.search("{} tap water".format(cities[c]), limit=10):
                if i.is_self and itx < 5:
                    i.comment_sort = "top"
                    try:
                        out.write("{},{},{},{},{},{},{},{}\n".format(cities[c], i.score, i.created_utc, "https://www.reddit.com" +
                                                                    i.permalink, i.num_comments, formatStr(i.title), formatStr(i.selftext), formatStr(i.comments.list()[0].body)))
                        itx += 1
                    except:
                        continue

for f in ["cities.csv", 'countries.csv']:
    with open(f, 'r', encoding='utf-8') as i:
        lines = i.read()
        with open(f, 'w+', encoding='utf-8') as o:
            o.write(re.sub("[\r\n]+", '\n', lines))