__author__ = 'mhan'

import os
import re
import xlrd
import time
from dateutil.parser import parse
from bs4 import BeautifulSoup





#==============================================================================
#  Build News Class
#==============================================================================
class News():
    LOAD_DATE = ""
    # LANGUAGE = ""
    # PUBLICATION_TYPE = ""
    CONTENT = ""







#==============================================================================
#  Build Company Leadr Class
#==============================================================================



class CompanyLeader(object):

    FullName = ""
    LastName = ""
    FirstName = ""
    CompanyName = ""
    Title = ""
    NumofNews = 0
    ID = 9999
    def __init__(self, ID):
        self.ID = ID
        self.numofnews = 0
    def set_numofnews(self, numofnews):
        self.NumofNews = numofnews
    # def set_name(self, LastName, FirstName):
    #     self.LastName = LastName
    #     self.FirstName = FirstName

#==============================================================================
#  Build Company 500 Class
#==============================================================================
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


#==============================================================================
#  Build Result Set from Excel
#==============================================================================
start_time = time.time()
XLSFile = "Execlis SP500t_2003_2013_Lnm.xls"
CompanyLeaderList = []

def build_result(XLSFile):
    result = []
    book = xlrd.open_workbook(XLSFile)
    sh = book.sheet_by_index(1)

    num_rows = sh.nrows - 1
    # num_cells = sh.ncols - 1

    curr_row = 0
    while curr_row < num_rows:

        curr_row += 1

        # row = sh.row(curr_row)
        print("ID:", curr_row,"Name:", sh.cell_value(curr_row, 0))
        Leader = CompanyLeader(curr_row)
        Leader.FullName = str.lower(sh.cell_value(curr_row, 0))
        Leader.FirstName = str.lower(sh.cell_value(curr_row, 1))
        Leader.LastName = str.lower(sh.cell_value(curr_row, 3))
        Leader.Title = str.lower(sh.cell_value(curr_row, 4))
        Leader.CompanyName = str.lower(sh.cell_value(curr_row, 5))
        result.append(Leader)
    return result

CompanyLeaderList = build_result(XLSFile)

print("Index leaders time ---", time.time()-start_time, "seconds --- used.")
len(CompanyLeaderList)
CompanyLeaderList[1].FullName
CompanyLeaderList[1].ID



#==============================================================================
#  Build File Index
#==============================================================================
mainDirectory = 'DATA/'

def get_filelist(mainDirectory):
    #mainDirectory =str(mainDirectory)
    result = []
    counter =0
    if not os.path.isdir(mainDirectory):
        print("Illegal Directory! Check it again please!")
    result = os.listdir(mainDirectory)
    for r in range(len(result)):
        result[r] = result[r].lower()

    print("Step 1: Finish the index of files name")
    print("There are", len(result), "files in the folder")
    return result

FileList = get_filelist(mainDirectory)

FileList[1]

CompanyLeaderList[1].CompanyName


#==============================================================================
#  Main Function
#==============================================================================

re.sub(r'yo(u)+($|\W)',"your sister", 'you')
re.sub(r'yo(u)+',"your sister", 'I miss you!')

re.sub(r'^yo(u)+',"your sister", "youuuuu")
re.sub(r'yo(u)+($|\W)',"your sister", "I miss you!")



re.sub(r'^u($|\W)',"your sister", "u!")

re.sub(r'^yo(u)+',"your sister", 'you')

re.sub(r'^u($|\W)',"your sister", "I hate you")

import re
def autocorrect(input):
    try:
        m = re.search(r'^yo(u)+(\W)(?i)', input)
        input = str.replace(input,input[m.start():m.end()-1],"your sister")
    except:
        input = re.sub(r'^yo(u)+($)(?i)',"your sister", input)
    input = re.sub(r'^yo(u)+($)(?i)',"your sister", input)
    input = re.sub(r'^u(\W)(?i)',"your sister ", input)
    input = re.sub(r'^u($)(?i)',"your sister ", input)
    return input
re.sub(r'yo(u)+($|\s)(?i)',"your sister", "youuutube")
re.sub(r'^yo(u)+$(?i)',"your sister", "I miss you")
autocorrect("I miss you")
autocorrect("our sister")
autocorrect("Youuuu want to go to the movies")
autocorrect("Youuuuu")
autocorrect("you")
autocorrect("you!")
autocorrect("youtobu!")


import re, string
s = "string. With. Punctuation?" # Sample string
out = re.sub('[%s]' % re.escape(string.punctuation), '', s)
out


#==============================================================================
#  Analysis of One File
#==============================================================================

fileName = "3M CO_2.HTML"
def AnalyzeSingleFile(fileName):
    start_time = time.time()
    soup = BeautifulSoup(open(fileName).read().lower())

    itemList = soup.find_all("span")
    # len(itemList)
    conStr = "".join(item.text for item in itemList)
    len(conStr)

    # newsList = str.split(conStr,"documents")
    newsStringList = str.split(conStr,"load-date")
    numofnews = len(newsStringList)

    print("There are",numofnews,"news in file ",fileName)
    print("File load time: ---", time.time()-start_time, "seconds --- used.")

    start_time = time.time()
    newsList=[]
    for i in range(numofnews-1):
        news = News()
        try:
            news.LOAD_DATE = str(parse(newsStringList[i+1][2:20], fuzzy=True))
        except:
            news.LOAD_DATE = ""
        m = re.search(r'language:',newsStringList[i])
        if  m.__sizeof__()>16:
            news.CONTENT = newsStringList[i][m.end():]
        else:
            news.CONTENT = newsStringList[i]
        newsList.append(news)

    print("File process time ---", time.time()-start_time, "seconds --- used.")


AnalyzeSingleFile(fileName)






news.LOAD_DATE = parse(newsStringList[1][2:20], fuzzy=True)




m = re.search(r'language:',newsStringList[i])




newsStringList[0]
newsStringList[1]
newsStringList[2]
newsStringList[-1]
parse(newsStringList[-1][2:20], fuzzy=True)
m = re.search(r'language:',newsStringList[1])
newsStringList[1][m.end():]










