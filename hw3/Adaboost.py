import sys
import math
import random




t=int(sys.argv[1])
trainfile=sys.argv[2]
testfile=sys.argv[3]

trainingset=[]
#load training examples
with open(trainfile) as f:
 for line in f:
  l=line.rstrip().split()
  trainingset.append(l)

testset=[]
#load testset
with open(testfile) as f:
 for line in f:
  
  l=line.rstrip().split()
  
  testset.append(l)


num_features=len(trainingset[0])-1

#function to calculate overall entropy
def entropy():
 dpositive=0
 dnegative=0
 npositive=0
 nnegative=0
 for i in range(len(trainingset)):
  #print trainingset[i][0]
  if trainingset[i][0]=='e':
   dpositive+=D[i]
   npositive+=1
  else:
   dnegative+=D[i]
   nnegative+=1
 #print 'positive='+str(npositive)
 #print 'negative='+str(nnegative)
 p1=dpositive/(dpositive+dnegative)
 p2=dnegative/(dpositive+dnegative)
 
 if p1==0:
  if p2==0:
   ans=0
  else:
   ans=p2*math.log(p2,2)
 elif p2==0:
  ans=p1*math.log(p1,2)
 else:
  ans=((p1)*math.log(p1,2))+((p2)*math.log(p2,2))
 return -1*ans

values={x:[] for x in range(1,len(trainingset[0]))}
#populate possible values taken up by different features
for l in trainingset:
 for i in range(1,len(trainingset[0])):
  if l[i] not in values[i]:
   values[i].append(l[i])
  
#function to calculate entropy for particlar value of feature
def entropy_feature_val(index, val):
 
 dpositive=0
 dnegative=0
 for i in range(len(trainingset)):
  if trainingset[i][index]==val:
   if trainingset[i][0]=='e':
    dpositive+=D[i]
   else:
    dnegative+=D[i]
 #print dpositive
 #print dnegative	
 p1=dpositive/(dpositive+dnegative)
 p2=dnegative/(dpositive+dnegative)
 if p1==0:
  if p2==0:
   ans=0
  else:
   ans=p2*math.log(p2,2)
 elif p2==0:
  ans=p1*math.log(p1,2)
 else:
  ans=((p1)*math.log(p1,2))+((p2)*math.log(p2,2))
 return -1*ans

   



#function to calculate feature entropy
def entropy_feature(index):
 entropy_values={}
 for v in values[index]:
  entropy_values[v]=entropy_feature_val(index,v)
 return entropy_values
 



#function to return splitting attribute index
def getsplitting():
 tot_entropy=entropy()
 #print 'entropy='+str(tot_entropy)
 candidate_gain=[]
 
 for i in range(num_features):
  index=1+i #feature index is 1+ ith feature 
  #get entropy for the feature
  feature_entropy=entropy_feature(index)
  #calculate weight ratio of each feature value in dataset
  feature_value_weights={x:0 for x in values[index]}
  for j in range(len(trainingset)):
   feature_value_weights[trainingset[j][index]]+=D[j]
  feature_value_weights_sum=sum(feature_value_weights.values())
  for x in feature_value_weights:
   feature_value_weights[x]/=feature_value_weights_sum  
  candidate_gain.append(tot_entropy-sum([feature_value_weights[v]*feature_entropy[v] for v in feature_entropy]))
 #print 'feature entropies='+str(feature_entropies)
 return 1+candidate_gain.index(max(candidate_gain)) 
  

#initial D
D=[1/float(len(trainingset))]*len(trainingset)


#map e to 1 and p to -1
results_map={'e':1,'p':-1}


#store decision stumps and alphas
decision_stumps=[]
alpha=[]

#main algorithm
for i in range(t):
 #print 
 #print 't='+str(i+1)
 #select splitting attribute
 attindex=getsplitting() 
 #print 'splitting attribute='+str(attindex)
 #figure out the e,p distribution for different feature values
 leaf_values={v:[0,0] for v in values[attindex]}
 for i in range(len(trainingset)):
  if trainingset[i][0]=='e':
   leaf_values[trainingset[i][attindex]][0]+=D[i]
  else:
   leaf_values[trainingset[i][attindex]][1]+=D[i]
 #decide leaf values 
 decision_dict={} #keys=feature values, value=decision (e/p)
 for v in values[attindex]:
  if leaf_values[v][0]>leaf_values[v][1]:
   decision_dict[v]='e'
  else:
   decision_dict[v]='p'
 decision_stumps.append({attindex:decision_dict})
 #classify all training examples using this decision stump for alpha, epsilon
 epsilon=0
 training_results=[]
 incorrect_i=[]
 for i in range(len(trainingset)):
  
  verdict=decision_dict[trainingset[i][attindex]]
  training_results.append(verdict)
  if verdict!=trainingset[i][0]:
   epsilon+=D[i]
   incorrect_i.append(i)
 #print 'no of incorrect='+str(len(incorrect_i))
 #print [(x,D[x]) for x in incorrect_i]
 #print 'epsilon='+str(epsilon)
 temp_alpha= 0.5*math.log((1-epsilon)/epsilon, math.exp(1))
 #print 'alpha='+str(temp_alpha)
 alpha.append(temp_alpha)
 
 #calculate dnext
 dnext=[D[i]*math.exp(-1*temp_alpha*results_map[trainingset[i][0]]*results_map[training_results[i]]) for i in range(len(D))] 
 #normalize dnext
 dnext=[x/float(sum(dnext)) for x in dnext]
 D=dnext




#now classify testset
#store answers
answers=[l[0] for l in testset]
test_results=[]
for l in testset:
 sum_result=0
 for i in range(t):
  splitting_attribute_i=decision_stumps[i].keys()[0]
  feature_value=l[splitting_attribute_i] if l[splitting_attribute_i] in decision_stumps[i][splitting_attribute_i] else random.choice(decision_stumps[i][splitting_attribute_i].keys()) #sometimes a feature value in testset is never seen in trainingset
  #print decision_stumps[i][splitting_attribute_i]
  #print 'feature_value='+feature_value
  result=results_map[decision_stumps[i][splitting_attribute_i][feature_value]]
  #print 'value added to sum_result='+str(alpha[i]*result)
  sum_result+=(alpha[i])*(result)
 #print 'sum_result='+str(sum_result)
 if(sum_result>=0):
  test_results.append('e')
 else:
  test_results.append('p')

#print answers
#print test_results
correct=0
incorrect=[]
for i in range(len(answers)):
 if answers[i]==test_results[i]:
  correct+=1
 else:
  incorrect.append(i)
#print correct
#print len(answers)
#print incorrect
print 100*correct/float(len(answers))
#print alpha
#print [x.keys()[0] for x in decision_stumps]


for x in alpha:
 print x

