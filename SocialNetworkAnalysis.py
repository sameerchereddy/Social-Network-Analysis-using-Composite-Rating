import networkx
from operator import itemgetter


# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['SalesRank'] = int(cell[5].strip())
    MetaData['TotalReviews'] = int(cell[6].strip())
    MetaData['AvgRating'] = float(cell[7].strip())
    MetaData['DegreeCentrality'] = int(cell[8].strip())
    MetaData['ClusteringCoeff'] = float(cell[9].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()


print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# Let's first get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks[purchasedAsin]['Title'])
print ("SalesRank = ", amazonBooks[purchasedAsin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[purchasedAsin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[purchasedAsin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[purchasedAsin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[purchasedAsin]['ClusteringCoeff'])
    

purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph,purchasedAsin,radius=1)
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
weightNodeList=[]
for frm, to, edge in purchasedAsinEgoGraph.edges(data=True):
    if edge ['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(frm,to,edge)
        if(frm==purchasedAsin):
            weightNodeList.append([to,edge['weight']])
weightNodeList=sorted(weightNodeList, key = itemgetter(0))
purchasedAsinNeighbors = []
purchasedAsinNeighbors = purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)
purchasedAsinNeighbors = sorted(purchasedAsinNeighbors)
compositeRating =[]
for i in purchasedAsinNeighbors:
    for j in weightNodeList:
        if(j[0]==i):
            compositeRating.append([i,j[1]*j[1]*amazonBooks[i]['AvgRating']*amazonBooks[i]['DegreeCentrality']/((amazonBooks[i]['ClusteringCoeff'])+1)/2])
compositeRating=sorted(compositeRating,key=itemgetter(1),reverse=True)[:5]
 
print()
print("The top 5 recommendations are:")
 
for i in range(len(compositeRating)):
    print()
    print ("ASIN = ", compositeRating[i][0]) 
    print ("Title = ", amazonBooks[compositeRating[i][0]]['Title'])
    print ("SalesRank = ", amazonBooks[compositeRating[i][0]]['SalesRank'])
    print ("TotalReviews = ", amazonBooks[compositeRating[i][0]]['TotalReviews'])
    print ("AvgRating = ", amazonBooks[compositeRating[i][0]]['AvgRating'])
    print ("DegreeCentrality = ", amazonBooks[compositeRating[i][0]]['DegreeCentrality'])
    print ("ClusteringCoeff = ", amazonBooks[compositeRating[i][0]]['ClusteringCoeff'])


