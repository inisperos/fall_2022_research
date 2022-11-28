import pandas as pd
import csv

df = pd.read_csv(r'C:\Users\anisp\Downloads\csstars\finaledgelist.csv')#citations.csv')

cited_list = df['citing'].tolist()
citing_list = df['cited'].tolist()
print(cited_list)

def focalpubs(publist):
    focal_pub = []
    for citedpubs in publist:
        if citedpubs not in focal_pub:
            focal_pub.append(citedpubs)
    return focal_pub

def checkifzero(citinglist,bd):
    for citingpubs in citinglist:
        if citingpubs not in cited_list:
            bd.append({"Node" : citingpubs, "Abs_Depth" : 0, "Abs_Breadth" : 0, "Level" : 0, "Rel_Depth" : 0, "Rel_Breadth" : 0})

def findreferences(node, pub_list):
    references = []
    pubindex = -1
    for pub in pub_list:
        pubindex += 1
        if node == pub:
            references.append(citing_list[pubindex])
    return references
    
    
def calculatemetrics(focalpub, citedlist, bd):
    for node in focalpub:
        abs_breadth = 0
        abs_depth = 0
        rel_breadth = 0
        rel_depth = 0
        references = findreferences(node, citedlist)
        for pubs in references:
            for citedpubs in citedlist:
                if pubs == citedpubs:
                    level = len(references)
                    abs_depth += 1
                    rel_depth = round(abs_depth / level , 2)
                else:
                    #if a citing pub isnt in cited, and doesn't have any current breadth
                    if abs_breadth == 0:
                        abs_breadth = len(references) - abs_depth
        abs_breadth = level - abs_depth
        if abs_breadth < 0 :
            abs_breadth = 0
        rel_breadth = round (abs_breadth / level , 2)
        bd.append({"Node" : node, "Abs_Depth" : abs_depth, "Abs_Breadth" : abs_breadth, "Level" : level, "Rel_Depth" : rel_depth, "Rel_Breadth" : rel_breadth})
    return bd

def main():
    focalpublications = focalpubs(cited_list)
    uniqueciting = focalpubs(citing_list)
    bd = [
    ]
    checkifzero(uniqueciting, bd)
    calculatemetrics(focalpublications, cited_list, bd)
    print(bd)
    field_names = ["Node", "Abs_Depth", "Abs_Breadth", "Level", "Rel_Depth", "Rel_Breadth"]
    with open('comparebdmetrics.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(bd)

main()