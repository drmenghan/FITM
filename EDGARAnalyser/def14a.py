# import os
# import re
# import pickle
# from bs4 import BeautifulSoup
# from difflib import SequenceMatcher
import sys
import time

import xlrd

from EDGARAnalyser import analyser


class Company(object):
    def __init__(self):
        self.name = ""
        self.cik = ""
        self.cid = ""
        self.num_def14A = 0
        self.def14a_list = []
        self.meeting_list = []
        self.number_of_period_filling_same_month = 0
        self.number_of_period_later_than_filling = 0
        self.total_number_meeting = 0
        self.number_of_meeting_changed = 0


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
    print("\nGetting leaders list from Excel.\n---\t", get_time(), "\t---")
    sys.stdout = original

    company_list = []
    book = xlrd.open_workbook(XLSFile)

    sh = book.sheet_by_index(sheetflag)
    num_rows = 3300
    num_rows = sh.nrows - 1
    # num_cells = sh.ncols - 1
    curr_row = 1
    # flag = 1 #Old Company
    while curr_row < num_rows:
        company = Company()
        company.cid = str(sh.cell_value(curr_row, 0)).lower()
        company.name = str(sh.cell_value(curr_row, 1)).lower()
        company.cik = str(sh.cell_value(curr_row, 2)).lower()
        company_list.append(company)
        curr_row += 1

    sys.stdout = Tee(sys.stdout, log)
    print("---\tTotal", '{:.2f}'.format(time.time() - start_time), "seconds used.\t---")
    print("---\tThere are", len(company_list), "companies in the Excel.\t---")
    log.close()
    sys.stdout = original
    return company_list


logfile = time.strftime("%H-%M_%m-%d-%Y" + ".log")
XLSFile = "EDGARAnalyser/companylist.xlsx"
XLSFile = "EDGARAnalyser/second.xlsx"
XLSFile = "EDGARAnalyser/error2.xlsx"
XLSFile = "EDGARAnalyser/error3.xlsx"
company_list = build_leader_company_list(XLSFile, logfile, 0)
len(company_list)

logfile2 = time.strftime("%H-%M_%m-%d-%Y" + ".log")
log2 = open(logfile2, 'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, log2)
#
edgar = analyser.EdgarAnalyser()
edgar = EdgarAnalyser()
edgar.welcome
edgar.filing_AnnualMeetingDate(cik="811808")
# error 1 1064015
type(edgar)

for i in range(len(company_list)):
    # for i in range(100):
    print("----------  " + str(i) + "  ----------")
    company_list[i].meeting_list, \
    company_list[i].number_of_period_filling_same_month, \
    company_list[i].number_of_period_later_than_filling, \
    company_list[i].total_number_meeting, \
    company_list[i].number_of_meeting_changed = edgar.filing_AnnualMeetingDate(cik=company_list[i].cik)

log2.close()
sys.stdout = original
company_list[776].cik
company_list[776].meeting_list[0].annual_meeting_date

# result= "result0314"+".txt"
result = "error3statistic" + ".txt"
r2 = open(result, 'a')
original = sys.stdout
sys.stdout = Tee(sys.stdout, r2)
for i in range(len(company_list)):
    for j in company_list[i].meeting_list:
        print(company_list[i].cid + "\t" + company_list[i].name + "\t" + company_list[
            i].cik + "\t" + j.annual_meeting_date + "\t" + j.filling_date
              + "\t" + j.period_of_report)

for i in range(len(company_list)):
    print(company_list[i].cid + "\t" + company_list[i].name + "\t" + company_list[i].cik + "\t"
          + str(len(company_list[i].meeting_list)) + "\t" + str(
        company_list[i].number_of_period_filling_same_month) + "\t"
          + str(company_list[i].number_of_period_later_than_filling) + "\t" + str(company_list[i].total_number_meeting)
          + "\t" + str(company_list[i].number_of_meeting_changed))
r2.close()
sys.stdout = original



# edgar.filing_AnnualMeetingDate(cik = "0000320193")
