import urllib.request
from bs4 import BeautifulSoup

# define the site
base_url = "https://bcacciaaudio.com/page/"

# define where to read data from
readArticleFile = open('scrapedArticleLinks.txt', 'r')

# define the path to our output file for the scraped data
writeArticleFile = open('scrapedArticleLinks.txt', 'a+')

# empty list to store previous data loaded from file
oldList = []

# empty list to store scraped data
newList = []

# define the final list of data that has been checked for duplicates
finalList = []


def getLinks(site):

    # query site and store html in variable
    page = urllib.request.urlopen(site)

    # parse the page into bs4 format and store. Set the html parser
    soup = BeautifulSoup(page, "html.parser")

    # print out the entire DOM
    # print(soup.prettify())

    # find all the article h2 elements that contain the links
    articles = soup.find_all('h2', attrs={'class':'entry-title'})

    # print out each href in between the h2 tags to get the links
    for link in articles:
        # print(link.a['href'])
        newList.append(link.a['href'])


def checkForDuplicates(oldList, newList):
    for x in newList:
        if x not in oldList:
            # print(x)
            finalList.append(x)


# load data already in the scrapedArticleLinks.txt file so we can check it for dupes
def readFile():
    for line in readArticleFile:
        oldList.append(line.rstrip())


readFile()
# try to run the loop on each new incremented page URL
try:
    i = 1
    while True:
        getLinks(base_url + str(i))
        i += 1

# once an invalid page number is reached, an exception is thrown and we clean up
except:
    print("No more pages to index.")
    checkForDuplicates(oldList, newList)
    for link in finalList:
        writeArticleFile.write(link + "\n")
    print(str(len(finalList)) + " links were added.")
    writeArticleFile.close()