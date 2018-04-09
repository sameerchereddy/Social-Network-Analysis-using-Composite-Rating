import networkx
from operator import itemgetter

# Read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
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

# Read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
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
    
# Now let's look at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past
purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph,purchasedAsin,radius=1)
# Next, recall that the edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So we can use the 
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
weightNodeList=[]
for frm, to, edge in purchasedAsinEgoGraph.edges(data=True):
    if edge ['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(frm,to,edge)
        if(frm==purchasedAsin):
            weightNodeList.append([to,edge['weight']])
weightNodeList=sorted(weightNodeList, key = itemgetter(0))
# Next, recall that given the purchasedAsinEgoTrimGraph you constructed above, 
# you can get at the list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 
purchasedAsinNeighbors = []
purchasedAsinNeighbors = purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)
purchasedAsinNeighbors = sorted(purchasedAsinNeighbors)
# Next, let's pick the Top Five book recommendations from among the 
# purchasedAsinNeighbors based on one or more of the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, 
# and ClusteringCoeff
compositeRating =[]
for i in purchasedAsinNeighbors:
    for j in weightNodeList:
        if(j[0]==i):
            compositeRating.append([i,j[1]*j[1]*amazonBooks[i]['AvgRating']*amazonBooks[i]['DegreeCentrality']/((amazonBooks[i]['ClusteringCoeff'])+1)/2])
compositeRating=sorted(compositeRating,key=itemgetter(1),reverse=True)[:5]

# Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, 
# TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff)
# (5) YOUR CODE HERE:  
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


