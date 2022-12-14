import requests
from bs4 import BeautifulSoup
from pprint import pprint
import schemdraw
from schemdraw import flow
from schemdraw import elements as elm
import json

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
        f.writelines(majors)

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
            classes[class_name] = [class_id, sem]
        except: pass
    
    return classes

def getAllClasses(major):
    classes = getClasses(major, FALL_SEM)
    spring_classes = getClasses(major, SPRING_SEM)

    for spring_class in spring_classes:
        if spring_class not in classes:
            classes[spring_class] = spring_classes[spring_class]

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
        for i in info:
            s = str(i)
            try:
                prereqs = processReqs(str(info), abr, classes)
                if(cid == "11347"):
                    print(prereqs)
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

def makeFlowChart(major):
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
    return
    abrv = getMajorAbr(li[0][0])
    hlevel = 0
    prev_level = 0
    dd = 8
    colorint = 0
    colors = ['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet']

    with schemdraw.Drawing(show=False) as dwg:
        for pair in li:
            parent = pair[0]
            children = pair[1]

            vlevel = int(parent.replace(abrv, "")[0])

            if (vlevel != prev_level):
                hlevel = 0
            prev_level = vlevel

            s = ""
            lvl = 0
            cutoff = 20
            for child in children:
                s += child + ", "
                if len(s) // cutoff > lvl:
                    s += '\n'
                    lvl = len(s) // cutoff
            children_sentence = s[:-1]

            a = flow.Circle(r=1.4).at((hlevel * dd, -vlevel * dd)).label(parent).fill('lightblue')
            b = flow.Box(w=2.8, h=1.2).at((hlevel * dd, -vlevel * dd-.8)).label(children_sentence, fontsize=8).fill('lightblue')

            nodes[parent] = a
            loc[parent] = [hlevel, vlevel]
            dwg += a
            dwg += b

            hlevel += 1
        
        for pair in li:
            parent = pair[0]
            children = pair[1]

            pnode = nodes[parent]
            plevel = int(parent.replace(abrv, "")[0])
            color = colors[colorint]
            colorint = (colorint + 1) % len(colors)

            for child in children:
                if child in nodes:
                    clevel = int(child.replace(abrv, "")[0])
                    cnode = nodes[child]
                    upper_limit = 5
                    dx = (loc[parent][0] - loc[child][0])
                    dy = (loc[parent][1] - loc[child][1])

                    if abs(dy) == 0 and dx < 0:
                        if abs(dx) <= 1:
                            dwg += elm.Arrow().color(color).at(pnode.E).to(cnode.W)
                        else:
                            dwg += elm.Arc2(arrow='->').color(color).at(pnode.E).to(cnode.W)
                    elif abs(dy) == 0 and dx > 0:
                        if abs(dx) <= 1:
                            dwg += elm.Arrow().at(pnode.W).color(color).to(cnode.E)
                        else:
                            dwg += elm.Arc2(arrow='->').color(color).at(pnode.W).to(cnode.E)
                    elif dy == 1:
                        dwg += elm.Arrow().color(color).at(pnode.N).to(cnode.S)
                    elif dy > 1 and dx <= 2:
                        dwg += elm.Arc2(arrow='->').color(color).at(pnode.N).to(cnode.W)
                    elif dy > 1 and dx > 2:
                        dwg += elm.Arc2( arrow='->').color(color).at(pnode.N).to(cnode.S)
                    else:
                        dwg += elm.Arc2(arrow='->').color(color).at(pnode.N).to(cnode.S)

    dwg.save(fname=f"charts/{major}.svg")

major = "Mathematics"          

getPrereqs(major)