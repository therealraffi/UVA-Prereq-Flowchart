import requests
from bs4 import BeautifulSoup
from pprint import pprint
import schemdraw
from schemdraw import flow
from schemdraw import elements as elm
import json
import random

SPRING_SEM = "1232"
FALL_SEM = "1228"

def getClasses(major, sem):
    url = f"https://louslist.org/page.php?Semester={sem}&Type=Group&Group={major}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    even_classes = soup.find_all(class_="SectionEven")
    odd_classes = soup.find_all(class_="SectionOdd")
    classes_href = even_classes + odd_classes
    classes = {}
    prereqs = []
    abrv = ""

    for href in classes_href:
        a_href = href.find('a')
        try:
            class_id = a_href.get_text()
            href = str(href)
            class_name = href.split('<tr class="Section')[1].split('"')[0].split(" ")[-1]
            prereq_html = soup.find(class_=class_name)
            mouseovers = prereq_html.findAll(onmouseover=True)

            if abrv == "":
                abrv = getMajorAbr(class_name)

            if "1110" in class_name:
                print(prereq_html)
                print(sem, class_name)
                print(sentence)

            for text in mouseovers:
                text = str(text)
                if "Enrollment Requirements" in text:
                    # print(text.split("Requirements:")[1])
                    sentence = text.split("Requirements:")[1].split("'")[0]
                    prereqs = processReqs(sentence, abrv)

            classes[class_name] = prereqs
            prereqs = []
            sentence = ""

        except Exception as e: pass
    
    return classes

def getAllClasses(major):
    classes = getClasses(major, FALL_SEM)
    spring_classes = getClasses(major, SPRING_SEM)
    print(len(classes), len(spring_classes))

    for spring_class in spring_classes:
        if spring_class not in classes:
            classes[spring_class] = spring_classes[spring_class]

    json_object = json.dumps(classes, indent=4)
    with open(f"prereqs/{major}.json", "w") as outfile:
        outfile.write(json_object)

    return classes

def processReqs(sentence, major):
    li = sentence.split(" ")
    reqs = set()
    cname = ""
    next = False
    punc = ",./')("

    for word in li:
        for p in punc:
            word.replace(p, '')
        
        try:
            int(word)
            cname = major + word
            reqs.add(cname)
            next = False
            cname = ""
        except:
            pass
    
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

def makeFlowChart(major):
    valid_nodes = {}
    nodes = {}
    loc = {}
    li = []
    parents = readPrereqs(major)

    for k in parents:
        if len(parents[k]) != 0:
            valid_nodes[k] = parents[k]
        for child in parents[k]:
            if child not in valid_nodes:
                valid_nodes[child] = []
    
    for k in valid_nodes:
        li.append([k, valid_nodes[k]])

    li = sorted(li, key=lambda x: x[0])
    keys = [x[0] for x in li]
    print(keys)
    with open(f"prereqs/{major}-list.txt", "w") as f:
        f.write(str(keys))

    abrv = getMajorAbr(li[0][0])
    hlevel = 0
    prev_level = 0
    dd = 8
    colorint = 0
    colors = ['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet']

    with schemdraw.Drawing() as dwg:
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
# getAllClasses(major)     
makeFlowChart(major)