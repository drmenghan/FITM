__author__ = 'Meng'


__author__ = 'Meng'
import os
import xlrd
from bs4 import BeautifulSoup
soup = BeautifulSoup(open("3M CO_1.HTML"))
soup.contents.__sizeof__()

ps = soup("p","c26")

# def news_info(p):


Content = open("3M CO_1.HTML")

Text = Content.read().lower()

#
# Text = """
# <P CLASS="c26"><SPAN CLASS="c2">are not words that often appear in the</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">same sentence. But at the median, where half</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">the packages are higher and half are lower,</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">compensation for the 100 highest-paid Minnesota</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">CEO has been essentially flat since</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">2007, before the financial crisis.</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">&quot;The reason median total pay is flat is that</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">the accumulated weight of proxy disclosure</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">requirements, media scrutiny, pressure from</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">institutional investors and the lagging</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">economic recovery is pushing down</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">on any proposal to significantly increase</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">executive compensation for</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">execs at publicly traded companies,&quot;</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">said V. John Ella, an attorneywho specializes</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">in executive compensation at</SPAN></P>
# <P CLASS="c26"><SPAN CLASS="c2">the Minneapolis firm Jackson Lewis.</SPAN></P>
#
#
# """

# Text.lower()
# soup = BeautifulSoup(Text)


def check_file(Filelist, logfile):
    Dic = "Data/"
    for f in Filelist:
        print("Checking file", f , "which is the", Filelist.index(f), "file in",len(Filelist))
        soup = BeautifulSoup(open(Dic + f).read().lower())
        itemList = soup.find_all("span")
        conStr = "".join(item.text for item in itemList)
        newsList = str.split(conStr,"load-date")



soup = BeautifulSoup(open("3M CO_1.HTML").read().lower())

itemList = soup.find_all("span")
# len(itemList)
conStr = "".join(item.text for item in itemList)
len(conStr)

# newsList = str.split(conStr,"documents")

newsList = str.split(conStr,"load-date")
len(newsList)

# newsList = newsList.encode("GBK", "ignore")
import re
str = "ADOBE_3"
str = "ABBOTT Lab abc def.HTML"
str = "Actavis.HTML"
str = "CAMERON INTERNATIONAL CORP"
str = "CABOT OIL & GAS CORP"
str = "BANK OF AMERICA CORP"
str = "BANK OF NEW YORK MELLON CORP"
try:
    FileName = re.search(r'(\w+\s*\w*\s*\w*\s*\w*)[_,\s,.]',str)
    CompanyAbbName = FileName.group(1).lower()
except:
    pass





newsList[0]

newsList[1]

for news in newsList:
    print(str(news.encode("GBK", "ignore")))

from dateutil.parser import parse
newsList[2]
strnews = newsList[2]
nstrnews = str.replace(strnews,"language"," language")
nstrnews
parse(nstrnews.upper(), fuzzy = True)

parse("the date was the 1st of December 2006 2:30pm".upper(), fuzzy=True)

parse("february 9, 2012".upper(), fuzzy=True)
parse(nstrnews[2:20].upper(), fuzzy=True)
parse(newsList[2][2:20].upper(), fuzzy=True)

nstrnews[2:20].upper()
import time
time.strptime(nstrnews, "%d %b %y")
import re
import dateutil

match = re.search(r'\d{4}-\d{2}-\d{2}', nstrnews[2:20])
print(match)

date = time.strptime(match.group(), '%Y-%m-%d').date()

# for item in itemList:
#     print(item.text)






#tag = soup.

##print(soup.prettify())
# for link in soup.find_all("a"):
#     print(link.get("href"))
#==============================================================================
# Get FileList
#==============================================================================
#mainDirectory = "E:/FI ANA/00_News Articles/"

class CompanyLeader(object):

    LastName = ""
    FirstName = ""
    CompanyName = ""
    def __init__(self, name):
        self.name = name
        self.numofnews = 0
    def set_numofnews(self, numofnews):
        self.numofnews = numofnews
    def set_name(self, LastName, FirstName):
        self.LastName = LastName
        self.FirstName = FirstName


class Company500(object):
    LeaderList = []
    def __init__(self, name):
        self.name = name
        self.numofleader = 0
        #self.LeaderList = []

    def set_numofleader(self, numofleader):
        self.numofleader = numofleader

    def add_Leader(self, leader):
        self.LeaderList.append(leader)


mainDirectory = 'DATA/'

def get_filelist(mainDirectory):
    #mainDirectory =str(mainDirectory)
    result = []
    counter =0
    if not os.path.isdir(mainDirectory):
        print("Illegal Directory! Check it again please!")

    # for root, dirs, list in os.walk(mainDirectory):
    #     listlen = len(list)
    #     for i in list:
    #         dirs = os.path.join(root, i)
    #         result.append(dirs)
    #         counter = counter+1
    #         print(dirs, counter, " out of ",listlen, "which is ",int(counter*100/listlen),"% has been done.")
    result = os.listdir(ProjectData)
    print("Step 1: Finish the index of files name")
    print("There are", len(result), "files in the folder")
    return result


ProjectData = "Y:\Projects\TMalpha\May15_transcripts"
pr = get_filelist(ProjectData)
len(pr)
rr = get_filelist(mainDirectory)
len(rr)



#==============================================================================
#  Build Result Set from Excel
#==============================================================================
XLSFile = "Execlis SP500t_2003_2013_Lnm.xls"
def build_result(XLSFile):
    result = []
    book = xlrd.open_workbook(XLSFile)
    sh = book.sheet_by_index(0)

    num_rows = sh.nrows - 1
    num_cells = sh.ncols - 1

    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = sh.row(curr_row)
        print("ID:", curr_row,"Name:", sh.cell_value(curr_row, 0))

build_result(XLSFile)
#==============================================================================
#  Main Function
#==============================================================================










#book = xlrd.open_workbook("E:/FI ANA/Execlis SP500t_2003_2013_Lnm.xls")

#Obtain basic information
#print("The number of worksheets is", book.nsheets)
#print("Worksheet name(s):", book.sheet_names())






#print (sh.name, sh.nrows, sh.ncols)
#print ("Cell D30 is", sh.cell_value(rowx=29, colx=3) )

# dealnum = sh.cell_value(rowx=1, colx=0)
#print(int(dealnum))
#From the first deal to search file and create final result
#dicDealIndex = {}
#dicKeywordIndex = {}
#Build index
#for i in range(50):
#    dicDealIndex.setdefault(sh.cell_value(rowx = i, colx = 0), sh.cell_value(rowx = i, colx = 2))
#    dicKeywordIndex.setdefault(sh.cell_value(rowx = i, colx = 0), sh.cell_value(rowx = i, colx = 3))
mainDirectory = "E:\FI ANA\00_News Articles\\"
Filelist = get_filelist(mainDirectory)
#
# for i in range(5):#13715
#     ParaToWrite = ""
#     DealID = sh.cell_value(rowx = i+1, colx = 0)  #Name with it
#     TransID = sh.cell_value(rowx = i+1, colx = 2)  #Search file with it
#     Term = sh.cell_value(rowx = i+1, colx = 3)    #Search file content with it
#     FilelistCounter = 0
#     for j in Filelist:
#         if(int(TransID).__str__() in j):#find the file
#             FilelistCounter = FilelistCounter+1
#             aaa = SearchinFile(Filelist[FilelistCounter],Term)
#             if(SearchinFile(Filelist[FilelistCounter],Term) != ""):
#                 NewFileName = mainDirectory + "\\" + int(DealID).__str__()+".txt"
#                 print(NewFileName)
#                 Context = SearchinFile(Filelist[FilelistCounter],Term)
#                 Writeback(NewFileName,Context)