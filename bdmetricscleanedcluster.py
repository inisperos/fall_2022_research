import pandas as pd
import csv

df = pd.read_csv(r'C:\Users\anisp\Downloads\csstars\finaledgelist.csv')#citations.csv')
cluster = pd.read_csv(r'C:\Users\anisp\Downloads\csstars\finalclusterlist.csv')#citations.csv')

cited_list = df['cited'].tolist()
citing_list = df['citing'].tolist()

cluster_id = cluster['clusterid'].tolist()
node_id = cluster['nodeid'].tolist()


def createnodelist(uniquecluster):
    nodelist = []
    clusterquery = 'clusterid == ' + str(uniquecluster);
    df2 = cluster.query(clusterquery)['nodeid']
    for items in df2:
        nodelist.append(items)
    return nodelist
    

def focalpubs(publist):
    focal_pub = []
    for citedpubs in publist:
        if citedpubs not in focal_pub:
            focal_pub.append(citedpubs)
    return focal_pub

def createlist(nodes, selectedlist):
    citing = []
    for node in nodes:
        if node in selectedlist:
            citing.append(node)
    return citing

def checkifzero(clusterid,citinglist,bd):
    for citingpubs in citinglist:
        if citingpubs not in cited_list:
            bd.append({"Cluster": clusterid ,"Node" : citingpubs, "Abs_Depth" : 0, "Abs_Breadth" : 0, "Level" : 0, "Rel_Depth" : 0, "Rel_Breadth" : 0})

def findreferences(node, pub_list, citinglist):
    references = []
    pubindex = -1
    for pub in pub_list:
        pubindex += 1
        if node == pub:
            references.append(citinglist[pubindex])
    return references

def calculatemetrics(clusterid, focalpub, citedlist, citinglist, bd):
    for node in focalpub:
        abs_breadth = 0
        abs_depth = 0
        rel_breadth = 0
        rel_depth = 0
        references = findreferences(node, citedlist, citinglist)
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
        bd.append({"Cluster" : clusterid, "Node" : node, "Abs_Depth" : abs_depth, "Abs_Breadth" : abs_breadth, "Level" : level, "Rel_Depth" : rel_depth, "Rel_Breadth" : rel_breadth})
    return bd

def main():
    #creates list of unique cluster ids
    cluster_list = focalpubs(cluster_id);
    bd = []
    for uniquecluster in cluster_list:
        #create node_id list
        node_list = createnodelist(uniquecluster)
        
        #create citing, cited list
        new_cited_list = createlist(cited_list, node_list)
        new_citing_list = createlist(citing_list, node_list)
        #unique ciitng, cited list
        uniqueciting = createlist(node_list, citing_list)
        focal_publications = createlist(node_list, cited_list)
        
        checkifzero(uniquecluster,uniqueciting, bd)
        #calculatesmetrics
        calculatemetrics(uniquecluster, focal_publications, new_cited_list, new_citing_list, bd)
        print(bd)
        field_names = ["Cluster","Node", "Abs_Depth", "Abs_Breadth", "Level", "Rel_Depth", "Rel_Breadth"]
        with open('bdmetricstestclustered.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writeheader()
            writer.writerows(bd)
 
        
main()