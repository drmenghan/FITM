__author__ = 'Meng'
import os
import pickle
import re
import sys
import time
from difflib import SequenceMatcher

import xlrd
from bs4 import BeautifulSoup
# pip install -U textblob


from textblob import TextBlob


# from withaop import trace

# nltk.download()


class CompanyLeader(object):
    """
    Define Leader
    """
    def __init__(self):
        # self.LastName = ""

        self.LastName = ""
        self.FirstName = ""
        self.FullName = ""
        self.Title = ""
        self.CompanyName = ""
        self.NumOfNews = 0
        self.NewsList = []
        self.NewsCompanyName = ""
        self.Year = 0



class Company500(object):
    """
    Define Company
    """
    def __init__(self):
        self.LeaderList = []
        self.CompanyName = ""
        self.NewsList = []
        self.NumOfNews = 0


# class CompanyResult(object):
#     """
#     To supply the final result statistic
#     """
#     def __init__(self):
#         self.LeaderList = []
#         self.CompanyName = ""
#         self.NewsList = []
#         self.NumOfNews = 0
#         self.


class Tee(object):
    """
    For output both to log and std
    """
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

def get_time():
    """
    Get the current whole format time
    :return: String format time
    """
    result = ""
    from pytz import reference
    import datetime
    time = reference.LocalTimezone()

    from time import localtime, strftime
    result = strftime("%A, %d %B %Y %I:%M:%S %p ", localtime())

    result += time.tzname(datetime.datetime.now())
    return result


def get_running_time(logfile):
    """
    Get formatted time
    :param logfile:
    :return:
    """
    start_time = time.time()
    original = sys.stdout
    log = open(logfile, 'a')
    sys.stdout = Tee(sys.stdout, log)
    print("\n---\tTotal", '{:.2f}'.format(time.time()-start_time), "seconds used.\t---")
    sys.stdout = original
    log.close()

def get_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_sizeof_file(filename, suffix='B'):
    num = os.stat(filename).st_size
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def save_object(obj, filename, logfile):
    """
    Save object to file
    :param obj:
    :param filename:
    :return:Success or not
    """
    start_time = time.time()
    original = sys.stdout
    log = open(logfile, 'a')
    sys.stdout = Tee(sys.stdout, log)
    with open(filename, 'wb') as output:
        print("\nSaving object to file", filename, "\n---\t",get_time(),"\t---")
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    print("---\tSize of the file", filename, "is",get_sizeof_file(filename),"\t---")
    print("---\tTotal", '{:.2f}'.format(time.time()-start_time), "seconds used.\t---")
    sys.stdout = original
    log.close()


def load_object(filename, logfile):
    """
    Load object from file
    :param filename:
    :return:Object saved to file previously
    """
    start_time = time.time()
    original = sys.stdout
    log = open(logfile, 'a')
    sys.stdout = Tee(sys.stdout, log)
    with open(filename,'rb') as f:
        print("\nLoading object from file", filename, "\n---\t",get_time(),"\t---")
        pic = pickle.load(f)
        print("---\tSize of the file", filename, "is",get_sizeof_file(filename),"\t---")
        print("---\tTotal", '{:.2f}'.format(time.time()-start_time), "seconds used.\t---")
    sys.stdout = original
    log.close()
    return pic


def get_filelist(mainDirectory, logfile):
    """
    Get list for specific Directory
    :param mainDirectory:
    :return:
    """
    #mainDirectory =str(mainDirectory)

    start_time = time.time()

    log = open(logfile, 'a')
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, log)
    print("\nIndex files in ",mainDirectory,"\n---\t",get_time(),"\t---")
    result = []
    counter =0
    if not os.path.isdir(mainDirectory):
        print("---Illegal Directory! Check it again please!---")
    result = os.listdir(mainDirectory)
    for r in range(len(result)):
        result[r] = result[r].lower()


    print("Step 1: Finish the index of files name in folder", mainDirectory, ".")
    print("---\tTotal", '{:.2f}'.format(time.time()-start_time), "seconds used.\t---")
    print("---\tThere are", len(result), "files in the folder.\t---\n\n")
    log.close()
    sys.stdout = original
    return result

def build_leader_company_list(XLSFile, logfile, sheetflag):
    """
    #Build questions buckets
    :param XLSFile:
    :return:List of questions in Excel
    """
    start_time = time.time()
    log = open(logfile, 'a')
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, log)
    print("\nGetting leaders list from Excel.\n---\t",get_time(),"\t---")
    sys.stdout = original

    LeaderList = []
    CompanyList = []
    book = xlrd.open_workbook(XLSFile)
    # xlrd.
    # sh = book.sheet_by_index(0)
    # sh = book.sheet_by_index(1)

    #flag = 0 is the small example, 1 is the whole file
    sh = book.sheet_by_index(sheetflag)

    # text = sh.cell_value(1, 10)
    # int(text)
    # datetime.strptime(text, '%Y')


    num_rows = sh.nrows - 1
    # num_rows = 200
    num_cells = sh.ncols - 1
    curr_row = 1
    flag = 1 #Old Company
    while curr_row < num_rows:
        leader = CompanyLeader()
        leader.CompanyName = str(sh.cell_value(curr_row, 5)).lower()
        leader.FullName = str(sh.cell_value(curr_row, 0)).lower()
        leader.FirstName = str(sh.cell_value(curr_row, 1)).lower()
        leader.LastName = str(sh.cell_value(curr_row, 3)).lower()
        leader.Title = str(sh.cell_value(curr_row, 6)).lower()
        leader.Year = int(sh.cell_value(curr_row, 10))
        LeaderList.append(leader)

        if(len(CompanyList)==0):
            company = Company500()
            company.CompanyName = leader.CompanyName
            company.LeaderList.append(leader)
            print("Add leader",leader.FullName,"to company:",company.CompanyName)
            CompanyList.append(company)
            print("Add the first company")
        else:
            for c in CompanyList:
                if(c.CompanyName == leader.CompanyName):
                    flag = 0 #Exist same name company
                    c.LeaderList.append(leader)
                    print("Add leader",leader.FullName,"to company:",c.CompanyName)
                    break
                    # print("Exist company",leader.CompanyName)
                    # print("i=",i)
                # else:
                #     flag = 1

            if(flag == 1):
                company = Company500()

                company.CompanyName = leader.CompanyName
                company.LeaderList.append(leader)
                print("Add leader",leader.FullName,"to company:",company.CompanyName)
                CompanyList.append(company)
                # print("Add one company",company.CompanyName)
                # flag = 0
            else:
                flag =1
        # print("Company Name:", leader.CompanyName)
        # print("Full Name:", leader.FullName)
        # print("Title:", leader.Title)
        # print("row number",curr_row)
        curr_row = curr_row + 1

    sys.stdout = Tee(sys.stdout, log)

    print("---\tTotal", '{:.2f}'.format(time.time()-start_time), "seconds used.\t---")
    print("---\tThere are", num_rows-1, "company leaders in the Excel.\t---")
    print("---\tThere are", len(CompanyList), "companies in the Excel.\t---")
    log.close()
    sys.stdout = original
    return LeaderList, CompanyList




def check_file(Filelist, CompanyList, Dic, logfile):
    # Dic = "Data/"
    start_time = time.time()

    log = open(logfile, 'a')
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, log)

    for f in Filelist:
        print("Checking file", f , "which is the", Filelist.index(f)+1, "file in",len(Filelist),"files.")
        soup = BeautifulSoup(open(Dic + f).read().lower())
        itemList = soup.find_all("span")
        conStr = "".join(item.text for item in itemList)
        newsList = str.split(conStr,"load-date")
        try:
            # Retest if doesn't work well
            FileName = re.search(r'(\w+\s*\w*\s*\w*\s*\w*)[_\s.]', f)
            CompanyAbbName = FileName.group(1).lower()
            print("The Company Abb Name is:",CompanyAbbName)
        except:
            pass

        for company in CompanyList:

            if get_similarity(CompanyAbbName,company.CompanyName)>0.75:
                print("Checking company:",company.CompanyName,"in the CompanyList.")
                print("Find corresponding Company is",company.CompanyName)
                for news in newsList:
                    for leader in company.LeaderList:
                        if (leader.LastName in news) and (leader.FirstName in news):
                        # if (leader.LastName in news) or (leader.FirstName in news):
                        #     print("Find out both last or first name in the news")
                            leader.NewsList.append(news)
                            leader.NumOfNews = leader.NumOfNews+1
                            # print("The leader's full name is", leader.FullName)
                            # print("The news of this leader is", leader.NumOfNews)

    NewLeaderList = []
    for com in CompanyList:
        for leader in com.LeaderList:
            NewLeaderList.append(leader)
    print("The size of the adjusted New LeaderList is", len(NewLeaderList))


    save_object(NewLeaderList,"NewLeaderList.pkl",logfile)
    save_object(CompanyList,"NewCompanyList.pkl",logfile)

    print("\n---\tFinished file analysis.\t---")
    print("---\tTotal", '{:.2f}'.format(time.time()-start_time), "seconds used.\t---\n")
    log.close()
    sys.stdout = original


    return NewLeaderList



def get_year(news):
    try:
        m = re.match(r'.*\S*\s*(20[01][0-9])',news[:200])
        year = m.group(1)
    except:
        year = 0
    return year

# get_year(news)

def get_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


def ifKeyword(key, news):
    try:
        if (news.find(key)):
            return True
        return False
    except:
        return False

def main():
    """
    Main Function Control the Whole Work Flow of Analysis
    :return:
    """
    logfile = r"D:/LOG20160102.txt"
    # DataDic = "DATA/"

    # DataDic = "H:/FI ANA/00_News Articles/"

    #FileList = get_filelist(DataDic,logfile)
    # [FileList[i] for i in range(len(FileList))]
    #XLSFile = "Execlis SP500t_2003_2013_Lnm1.xls"

    # leaderFile = "LeaderList.pkl"

    # companyFile = "CompanyList.pkl"

    # leaderFile = r"F:\FI ANA\NewLeaderList.pkl"
    # companyFile = r"F:\FI ANA\NewCompanyList.pkl"
    # leaderFile = r"D:\NewLeaderList.pkl"
    companyFile = r"D:\NewCompanyList.pkl"
    XLSFile = "Execlis SP500t_2003_2013_Lnm1.xls"
    #Last parameter control the sample and the whole data 1 for whole
    LeaderList, CompanyList = build_leader_company_list(XLSFile, logfile, 1)

    # save_object(LeaderList,leaderFile,logfile)
    #save_object(CompanyList,companyFile,logfile)


    FLeaderList = load_object(leaderFile,logfile)
    FCompanyList = load_object(companyFile,logfile)

    """

    Final Analysis Begin

    """

    log = open(r"D:\Final Result20160102-2.txt", 'a')
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, log)
    yearlist = {2003:0,2004:0,2005:0,2006:0,2007:0,2008:0,2009:0,2010:0,2011:0,2012:0,2013:0}
    scorelist = {2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0}
    posscorelist = {2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0}
    negscorelist = {2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0}
    keywords = ["scandal"]
    #, "fraud", "false statement", "financial crime", "lawsuit", "insider-trading", "falsify"]
    for company in FCompanyList:
        for leader in company.LeaderList:

            if (leader.NumOfNews > 0):
                # print("\t","\t",leader.FullName,"\t",company.CompanyName,"\t\t",leader.NumOfNews)
                for keyword in keywords:
                    for news in leader.NewsList:
                        # try:
                        #     year = eval(get_year(news))
                        #     if (year in yearlist.keys()):
                        #         # print(year)
                        #         # print("Find year!")
                        #         yearlist[year]+=1
                        #
                        #         scorelist[year] += get_score(news)
                        #         if(get_score(news)>0):
                        #             posscorelist[year]+=1
                        #         else:
                        #             negscorelist[year]+=1
                        # except:
                        #     print("wrong",get_year(news))


                        if (ifKeyword(keyword, news)):
                            print("Sensitive Word \"" + keyword + "\":\n")
                            try:
                                print(leader.FullName, "\t", company.CompanyName, "\t", eval(get_year(news)))
                                print(news)
                            except:
                                print("Code Wrong")
                                # for key,val in yearlist.items():
                                #     #True#val != 0:
                                #     if (key==2003):
                                #         print(key,"\t",leader.FullName,"\t",company.CompanyName,"\t",val,"\t",scorelist[key],"\t",posscorelist[key],"\t",negscorelist[key])
                for key,val in yearlist.items():
                    yearlist[key] = 0
                    scorelist[key] = 0
                    posscorelist[key] = 0
                    negscorelist[key] =0


    sys.stdout = original
    log.close()

    """

    Final Analysis End

    """


if __name__ == "__main__":
    main()