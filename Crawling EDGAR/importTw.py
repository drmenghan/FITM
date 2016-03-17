class user(object):
    def __init__(self):
        self.id = ""
        self.activity = []


class activity(object):
    def __init__(self):
        self.userA = ""
        self.userB = ""
        self.timestamp = ""
        self.type = ""


act = open("Crawling EDGAR/higgs-activity_time.txt")
activitylist = []
for line in act:
    activityobject = activity()
    activityobject.userA = line.split(" ")[0]
    activityobject.userB = line.split(" ")[1]
    activityobject.timestamp = line.split(" ")[2]
    activityobject.type = line.split(" ")[3]
    activitylist.append(activityobject)

len(activitylist)
for i in range(100):
    print("UserA: " + activitylist[i].userA)
    print("UserB: " + activitylist[i].userB)
    print("TIMESTAMP: " + activitylist[i].timestamp)
    print("TYPE: " + activitylist[i].type)

act.close()
