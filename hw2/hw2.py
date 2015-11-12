import sys
import random
import operator
def distance(l1,l2):
 return sum((a-b)**2 for a,b in zip(l1,l2))**0.5

def means(l):
 #print("l="+str(l))
 sums=[sum(x) for x in zip(*l)]
 #print("sum="+str(sums))
 mean=[x/len(l) for x in sums]
 #print("mean="+str(mean))
 return mean

def hasThresholdreached(l1,l2,threshold):
 dist=[distance(a,b) for a,b in zip(l1,l2)]
 if max(dist)<threshold:
  return True
 return False

k=int(sys.argv[1])
method=sys.argv[2]
threshold=float(sys.argv[3])
iterno=int(sys.argv[4])
ipfilename=sys.argv[5]
points=[]
centroids=[]
cluster_membership={}
points_clustermap={tuple(x):None for x in points}

with open(ipfilename) as f:
 for line in f:
  l=[float(x) for x in line.split(",")]
  points.append(l)


if(method=="first"):
 centroids=points[:k]
if(method=="rand"):
 centroids=random.sample(points,k)
cluster_membership={i:[centroids[i]] for i in range(k)}
points_clustermap
iterations=0
oldcentroids=centroids
while(iterations<iterno):
 iterations+=1 
 
 for point in points:
  distlist=[distance(point,centroid) for centroid in centroids]
  minindex=distlist.index(min(distlist))
  cluster_membership[minindex].append(point)
  points_clustermap[tuple(point)]=minindex
 oldcentroids=centroids
 centroids=[means(cluster_membership[i]) for i in range(k)]
 cluster_membership={i:[] for i in range(k)}
 if(hasThresholdreached(oldcentroids,centroids,threshold)):
  break

#print ("iterations="+str(iterations))
with open(ipfilename+'.output','w') as f:
 for centroid in centroids:
  f.write(",".join([str(x) for x in centroid ])+'\n')
 for point in points:
  f.write(str(points_clustermap[tuple(point)])+'\n')

 
  
   
