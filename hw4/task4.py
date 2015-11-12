import itertools
import math

original_data=[]
with open('mushroom_mine.train') as f:
 for line in f:
  l=line.rstrip().split('\t')
  original_data.append(l)


mapp=[]

with open('featuremap.txt') as f:
 for line in f:
  l=line.split()
  d={}
  for i in range(0,len(l)-1,2):
   d[l[i]]=int(l[i+1])
  mapp.append(d)


mapped_data=[]

for l in original_data:
 m=[]
 for i in range(len(l)):
  m.append(mapp[i][l[i]])
 mapped_data.append(m)

print 'SUBTASK 1'
print

def mean(x):
 
 summ=sum([l[x] for l in mapped_data])
 
 return summ/float(len(mapped_data))

def covar(x,y):
 mean_x=mean(x)
 mean_y=mean(y)
 expxy=sum([l[x]*l[y] for l in mapped_data])
 expxy/=float(len(mapped_data))
 #print 'expxy='+str(expxy)+' mean_x='+str(mean_x)+' mean_y='+str(mean_y)
 #print 'covar='+str(expxy-(mean_x*mean_y))
 return expxy-(mean_x*mean_y)

def var(x):
 expxsq=sum([l[x]*l[x] for l in mapped_data])
 expxsq/=float(len(mapped_data))
 #print 'expxsq='+str(expxsq)
 #print 'mean='+str(mean(x))
 #print 'var='+str(expxsq-(mean(x)**2))
 return expxsq-(mean(x)**2)
  

'''for l in mapped_data:
 print '\t'.join([str(x) for x in l])'''


 
sub1_result={}
for i in range(1,len(mapped_data[0])):
 #print i
 num=covar(i,0)
 den=float((var(i)*var(0))**0.5)
 if den ==0:
  sub1_result[i]=0
 else:
  sub1_result[i]=num/den

sorted_keys=sorted(sub1_result,key=sub1_result.get, reverse=True)

for key in sorted_keys[:5]:
 print str(key)+' '+str(sub1_result[key])

print
print 'SUBTASK 2'
print

#subtask2
#figure out unique feature values for each feature
unique={}
for l in original_data:
 for i in range(len(l)):
  if i not in unique:
   unique[i]=[l[i]]
  else:
   if l[i] not in unique[i]:
    unique[i].append(l[i])

#print unique

def score(x,y):
 pairs=itertools.product(unique[x],unique[y])
 score=0
 for p in pairs:
  conj=0
  px=0
  py=0
  for l in original_data:
   if l[x]==p[0] and l[y]==p[1]:
    conj+=1
   if l[x]==p[0]:
    px+=1
   if l[y]==p[1]:
    py+=1
  pconj=conj/float(len(original_data))
  px=px/float(len(original_data))
  py=py/float(len(original_data))
  '''print x
  print px
  print py
  print pconj'''
  if pconj!=0:
   score+=pconj*math.log(pconj/float(px*py))
 return score

sub2_result={}
#print len(original_data[0])
for i in range(1, len(original_data[0])):
 sub2_result[i]=score(i,0)

sorted_keys=sorted(sub2_result,key=sub2_result.get,reverse=True)
for key in sorted_keys[:5]:
 print str(key)+' '+str(sub2_result[key])

 
