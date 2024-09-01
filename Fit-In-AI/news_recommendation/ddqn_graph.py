import copy

import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

with open("test_result_five1_w.pkl", "rb") as t1:
  t1_result = pickle.load(t1)

with open("test_result_five2_w.pkl", "rb") as t2:
  t2_result = pickle.load(t2)

with open("test_result_five3_w.pkl", "rb") as t3:
  t3_result = pickle.load(t3)

with open("test_result_five4_w.pkl", "rb") as t4:
  t4_result = pickle.load(t4)
with open("test_result_five5_w.pkl", "rb") as t5:
  t5_result = pickle.load(t5)

answer1 = [0] * 5
answer2 = [0] * 5

for i in range(5):
  answer1[i]+=(t1_result[0][i] + t2_result[0][i] + t3_result[0][i] + t4_result[0][i] + t5_result[0][i])
  answer2[i] += (t1_result[1][i] + t2_result[1][i] + t3_result[1][i] + t4_result[1][i] + t5_result[1][i])
  answer1[i] = answer1[i]/5
  answer2[i] = answer2[i]/5


answer3 = copy.deepcopy(answer1)
answer4 = copy.deepcopy(answer2)

category=['Economy','Social','Entertainment','Sports','Weather']

colors=['y'] * 5
colors2=['y'] * 5
colors[4] = 'C2'
colors2[4] = 'C2'

n=np.arange(5)
plt.bar(n,answer1,color=colors)
plt.xticks(n,category)
plt.ylabel('Total Counts')
plt.xlabel('Preferred Category Index')
plt.show()

n=np.arange(5)
plt.bar(n,answer2,color=colors)
plt.xticks(n,category)
plt.ylabel('Total Counts')
plt.xlabel('Category')
plt.show()


for i in range(5):
  answer3[i] = answer3[i]/2000
  answer4[i] = answer4[i]/2000

plt.figure(figsize=(8,4))
n=np.arange(5)
plt.bar(n,answer3,color=colors)
plt.xticks(n,category)
plt.ylabel('Recommended Category Ratio')
plt.xlabel('Category')
plt.show()


plt.figure(figsize=(8,4))
n=np.arange(5)
plt.bar(n,answer4,color=colors2)
plt.xticks(n,category)
plt.ylabel('Recommended Category Ratio')
plt.xlabel('Category')
plt.show()



