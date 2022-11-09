import requests
from bs4 import BeautifulSoup
from pprint import pprint
import schemdraw
from schemdraw import flow
from schemdraw import elements as elm
import json
import random
import ndjson

SPRING_SEM = "1232"
FALL_SEM = "1228"

def getMajors():    
    URL = "https://louslist.org/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    majors_html = soup.find_all(class_="IndexTable4")
    majors = ""

    for m in majors_html:
        majors_href = str(m.find("a"))
        try:
            majors = majors + majors_href.split("Group=")[1].split('"')[0] + "\n"
        except:
            pass
    
    with open("majors.txt", 'w') as f:
        li = majors.split("\n")
        f.writelines(str(li))

def getClasses(major, sem):
    url = f"https://louslist.org/page.php?Semester={sem}&Type=Group&Group={major}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    even_classes = soup.find_all(class_="SectionEven")
    odd_classes = soup.find_all(class_="SectionOdd")
    classes_href = even_classes + odd_classes
    classes = {}
    for href in classes_href:
        a_href = href.find('a')
        try:
            class_id = a_href.get_text()
            href = str(href)
            class_name = href.split('<tr class="Section')[1].split('"')[0].split(" ")[-1]
            try:
                int(class_id)
                classes[class_name] = [class_id, sem]
            except: pass
        except: pass
    
    return classes

def getAllClasses(major):
    classes = getClasses(major, FALL_SEM)
    spring_classes = getClasses(major, SPRING_SEM)
    print(len(classes), len(spring_classes))

    for spring_class in spring_classes:
        if spring_class not in classes:
            classes[spring_class] = spring_classes[spring_class]

    with open(f"classes/{major}.json", "w") as outfile:
        json.dump(classes, outfile)

    return classes

def getPrereqs(major):
    abr = ""
    parents = {}
    classes = readClasses(major)

    for c in classes:
        cid = classes[c][0]
        sem = classes[c][1]

        page = requests.get(f"https://louslist.org/sectiontip.php?Semester={sem}&ClassNumber={cid}")
        soup = BeautifulSoup(page.content, "html.parser")

        if abr =="": abr = getMajorAbr(c)
        info = soup.find(class_="InfoSISDescription")
        splitAt = ""
        if ("Prerequisite:" in str(info)):
            splitAt= "Prerequisite:"
        if ("Prerequisites:" in str(info)):
            splitAt= "Prerequisites:"
        if ("Completed " in str(info)):
            splitAt= "Completed "

        if(splitAt != ""):
            try:
                sentence = str(info).split(splitAt)[1]
                if(";" in sentence):
                    sentence = sentence.split(";")[0]
                sentence = sentence.replace("</td>", "")

                prereqs = processReqs(sentence, abr)
                if(c == "CS3140"):
                    print(c, prereqs)
                parents[c] = prereqs
            except Exception as e: 
                print(e)
                parents[c] = []
        else:
            parents[c] = []
    
    with open(f"prereqs/{major}.json", "w") as outfile:
        json.dump(parents, outfile)

def processReqs(sentence, major):
    li = sentence.split(" ")
    coreq = []
    reqs = []
    cname = ""
    punc = ",./');("
    prev = ""
    for word in li:
        if word == "and" and len(coreq) > 0:
            reqs.append(coreq)
            coreq = []
        for p in punc:
            word = word.replace(p, '')
        try:
            int(word)
            if(len(word) > 3):
                cname = prev + word
                coreq.append(cname)
                # print(cname, sentence)
                cname = ""
        except:
            pass

        if(word.isupper() or word.lower() == major.lower()):
            try:
                int(word)
            except:
                prev = word.upper()
    if len(coreq) > 0:
        reqs.append(coreq)
    # print(reqs)
    # print()
    return list(reqs)

def getMajorAbr(string):
    i = 0
    nums = "1234567890"
    for s in string:
        if s in nums: break
        i += 1
    return string[:i].strip()

def readClasses(major): 
    with open(f"classes/{major}.json", 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def readPrereqs(major): 
    with open(f"prereqs/{major}.json", 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def readRevPrereqs(major): 
    with open(f"rev-prereqs/{major}.json", 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def reverseReqs(major):
    classes = readPrereqs(major)
    reverse = {}
    for key in classes:
        for val in classes[key]:
            for v in val:
                if v not in reverse:
                    reverse[v] = [key]
                else:
                    reverse[v].append(key)

    with open(f"rev-prereqs/{major}.json", "w") as outfile:
        json.dump(reverse, outfile)

def readMajors():
    with open("majors.txt", "r") as f:
        s = f.read()
        li = s.strip('][').replace("'", "").split(', ')
        return li

def getValidFiles(major):
    valid_nodes = {}
    nodes = {}
    loc = {}
    li = []
    keys = []
    parents = readRevPrereqs(major)

    for k in parents:
        if len(parents[k]) != 0:
            valid_nodes[k] = parents[k]
        for child in parents[k]:
            if child not in valid_nodes:
                valid_nodes[child] = []
    
    for k in valid_nodes:
        abrv = getMajorAbr(k)
        keys.append(k)
        li.append([k, valid_nodes[k]])
    li = sorted(li, key=lambda x: x[0])
    keys = sorted(keys, key=lambda x: x[len( getMajorAbr(x)):])
    with open(f"prereqs/{major}-list.txt", "w") as f:
        f.write(str(keys))

def getValidFilesMajors():
    majors = readMajors()
    allClasses = {}
    for major in majors:
        try:
            with open(f"prereqs/{major}-list.txt", "r") as f:
                s = f.read()
                li = s.strip('][').replace("'", "").split(', ')
                allClasses[major] = li
        except Exception as e: print(e)
    with open("All-list.json", "w") as f:
        json.dump(allClasses, f)
    return allClasses

def getPrereqsMajors():
    majors = readMajors()
    allClasses = {}
    for major in majors:
        try:
            with open(f"prereqs/{major}.json", "r") as f:
                allClasses[major] = json.load(f)
        except: pass
    with open("All-prereq.json", "w") as f:
        json.dump(allClasses, f)
    return allClasses

def reverseReqsMajors():
    majors = readMajors()
    allClasses = {}
    for major in majors:
        try:
            with open(f"rev-prereqs/{major}.json", "r") as f:
                allClasses[major] = json.load(f)
        except: pass
    with open("All-rev-prereq.json", "w") as f:
        json.dump(allClasses, f)
    return allClasses

def updateScript():
    all_classes = getValidFilesMajors()
    all_prereqs = getPrereqsMajors()
    rev = reverseReqsMajors()

    places = ["var all_classes =", "var all_prereqs =", "var all_rev_prereqs =", "// START RIGHT HERE"]
    data = [all_classes, all_prereqs, rev]

    with open("scripts/main.js", "r+") as f:
        old = f.read() # read everything in the file

        d1 = all_classes
        s1 = "var all_classes ="
        s2 = "var all_prereqs ="
        p1 = old.index(s1) + len(s1)
        p2 = old.index(s2)
        old = old.replace(old[p1:p2], str(d1) + "\n\n\n")

        d1 = all_prereqs
        s1 = "var all_prereqs ="
        s2 = "var all_rev_prereqs ="
        p1 = old.index(s1) + len(s1)
        p2 = old.index(s2)
        old = old.replace(old[p1:p2], str(d1) + "\n\n\n")

        d1 = rev
        s1 = "var all_rev_prereqs ="
        s2 = "// START RIGHT HERE"
        p1 = old.index(s1) + len(s1)
        p2 = old.index(s2)
        old = old.replace(old[p1:p2], str(d1) + "\n\n\n")

    with open("main.js", "w") as f2:
        f2.write(old)


majors = ["CompSci"]
# majors = readMajors()

# for major in majors:
#     # getAllClasses(major)     
#     # getPrereqs(major)
#     # reverseReqs(major)
#     getValidFiles(major)

updateScript()