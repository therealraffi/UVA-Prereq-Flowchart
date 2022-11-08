import requests
from bs4 import BeautifulSoup
from pprint import pprint
import schemdraw
from schemdraw import flow
from schemdraw import elements as elm
import json

SEM = "1232"

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
        f.writelines(majors)

def getClasses(major):
    url = f"https://louslist.org/page.php?Semester={SEM}&Type=Group&Group={major}"
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
            classes[class_name] = class_id
        except: pass
    
    json_object = json.dumps(classes, indent=4)
    with open(f"classes/{major}.json", "w") as outfile:
        outfile.write(json_object)

    return classes

def readClasses(major): 
    with open(f"classes/{major}.json", 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def readPrereqs(major): 
    with open(f"prereqs/{major}.json", 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

def getPrereqs(major, classes):
    url = f"https://louslist.org/sectiontip.php?Semester={SEM}&ClassNumber="
    abr = ""
    parents = {}
    valid_classes = set()
    for c in classes:
        valid_classes.add(c)

    for c in classes:
        page = requests.get(f"https://louslist.org/sectiontip.php?Semester={SEM}&ClassNumber={classes[c]}")
        soup = BeautifulSoup(page.content, "html.parser")

        if abr =="": abr = getMajorAbr(c)
        info = soup.find_all(class_="InfoSIS")
        for i in info:
            s = str(i)
            try:
                prereqs = s.split("Enrollment Requirements")[1].split("Requirement Designation")[0]
                prereqs = prereqs.split("<td>")[1].split("</td>")[0]
                prereqs = processReqs(prereqs, abr, valid_classes)
                parents[c] = prereqs
            except: pass
    
    json_object = json.dumps(parents, indent=4)
    with open(f"prereqs/{major}.json", "w") as outfile:
        outfile.write(json_object)

    return parents

def getMajorAbr(string):
    i = 0
    nums = "1234567890"
    for s in string:
        if s in nums: break
        i += 1
    return string[:i].strip()

def processReqs(sentence, major, valid_classes):
    li = sentence.split(" ")
    reqs = []
    cname = ""
    next = False
    for word in li:
        if next:
            try:
                int(word[-1])
            except:  
                word = word[:-1]
            try:
                int(word)
                cname += word
                if cname in valid_classes:
                    reqs.append(cname)
                next = False
                cname = ""
            except:
                pass
        if word == major:
            cname = major
            next = True
    
    return reqs

def makeFlowChart(major, parents):
    valid_nodes = {}
    nodes = {}
    li = []

    for k in parents:
        if len(parents[k]) != 0:
            valid_nodes[k] = parents[k]
        for child in parents[k]:
            if child not in valid_nodes:
                valid_nodes[child] = []
    
    for k in valid_nodes:
        li.append([k, valid_nodes[k]])

    li = sorted(li, key=lambda x: x[0])
    abrv = getMajorAbr(li[0][0])
    hlevel = 0
    prev_level = 0
    dd = 4

    with schemdraw.Drawing() as dwg:
        for pair in li:
            parent = pair[0]
            vlevel = int(parent.replace(abrv, "")[0])

            if (vlevel != prev_level):
                hlevel = 0
            prev_level = vlevel

            a = flow.Circle(r=1.2).at((hlevel * dd, -vlevel * dd)).label(parent).fill('lightblue')
            nodes[parent] = a
            dwg += a

            hlevel += 1
        
        for pair in li:
            parent = pair[0]
            children = pair[1]

            pnode = nodes[parent]
            plevel = int(parent.replace(abrv, "")[0])

            for child in children:
                if child in nodes:
                    clevel = int(child.replace(abrv, "")[0])
                    cnode = nodes[child]
                    if abs(clevel - plevel) == 1:
                        dwg += elm.Arrow().at(pnode.N).to(cnode.S)
                    elif clevel == plevel:
                        dwg += elm.Arrow().at(pnode.W).to(cnode.E)
                    else:
                        radius = abs(clevel-plevel)
                        dwg += elm.Arc2(arrow='->').at(pnode.N).to(cnode.S)

    dwg.save(fname=f"charts/{major}.svg")

major = "CompSci"                
# getClasses(major)
classes = readClasses(major)
# getPrereqs(major, classes)
parents = readPrereqs(major)
makeFlowChart(major, parents)