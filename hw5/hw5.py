#function to create epoch time
import datetime
def epoch(s):
 date=s[:10]
 time=s[11:-1]
 [yy,mm,dd]=[int(x) for x in date.split('-')]
 [h,m,s]=[int(x) for x in time.split(':')]
 return (datetime.datetime(yy,mm,dd,h,m,s)-datetime.datetime(1970,1,1)).total_seconds()

 




#identify users to be considered
users={}
with open('Gowalla_edges.txt') as f:
 lines=[x.rstrip() for x in f.readlines()][:10000]

for line in lines:
 for user in line.split():
  if user not in users:
   users[user]=1

print 'user population done'


#create cascades dictionary
cascades={}
with open('Gowalla_totalCheckins.txt') as f:
 for line in f:
  l=line.rstrip().split()
  if l[0] in users:
   print l[0]
   if int(l[-1]) not in cascades:
    print int(l[-1])
    cascades[int(l[-1])]=[(l[0],l[1])]
   else:
    cascades[int(l[-1])].append((l[0],l[1]))

print 'cascade dict population done'
print len(cascades)
#create cascade file
with open('gowalla_cascade','w') as f:
 for  user in users:
  f.write(user+','+user+'\n')
 f.write('\n')
 diff=[]
 minmax={}
 for key in cascades:
  epochs=[]
  for cascade in cascades[key]:
   epochs.append(epoch(cascade[1]))
  minepoch=min(epochs)
  maxepoch=max(epochs)
  minmax[key]=minepoch
  diff.append(maxepoch-minepoch)
 den=max(diff)
 for key in cascades:
  for cascade in cascades[key][:-1]:
   f.write(cascade[0]+','+str((epoch(cascade[1])-minmax[key])/float(den))+',')
  f.write(cascades[key][-1][0]+','+str((epoch(cascades[key][-1][1])-minmax[key])/float(den))+'\n')

#create ground truth file
with open('gowalla_groundtruth','w') as f:
 for user in users:
  f.write(user+','+user+'\n')
 f.write('\n')
 for line in lines:
  l=line.split()
  f.write(l[0]+','+l[1]+'\n')
  
   
