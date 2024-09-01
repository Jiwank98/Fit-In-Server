import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import copy
import pickle
from torch.autograd import Variable

class Config(object):
    lr = 0.0001
    discount_factor = 0.98
    reply_buffer_limit = 50000
    update_target_frequency = 20
    initial_epsilon = 0.9
    min_epsilon = 0.0001
    epsilon_discount_rate = 1e-7
    batch_size = 32
    epochs= 20000

class Model(nn.Module):

    def __init__(self, action_num):
        super().__init__()
        self.rf_dim = 10 * 4
        self.cf_dim = 4
        self.action_dim = 1
        self.input_dim = self.rf_dim + self.cf_dim + self.action_dim

        self.fc1 = nn.Linear(self.input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 1)
        self.relu = torch.nn.ReLU()

    def forward(self, state, action):
        state = torch.Tensor(state)
        inputs = torch.cat([state, action], dim=-1)
        x = self.relu(self.fc1(inputs))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.fc4(x)

        return x



from collections import deque
import random
import numpy as np


class Agent:
    def __init__(self, action_set):
        self.action_set = action_set
        self.action_number = len(action_set)
        self.build_network()

    def build_network(self):
        self.Q_network = Model(self.action_number)
        self.target_network = Model(self.action_number)


    def build_optimizer(self,Q):
        self.optimizer = optim.Adam(Q.parameters(), lr=Config.lr)


    def take_action(self, rf, cf, action_num,Q):  # 엡실론 사용해서 random뽑기 / 나머지 확률로 높은거 뽑기
        state = np.concatenate((rf, cf))
        state = torch.from_numpy(state).float()
        state = Variable(state)
        action = np.zeros(action_num)
        for i in range(0, action_num):
            action[i] = i
        action = torch.Tensor(action)
        Q.eval()
        q_list = []
        idx = []
        max = -1

        for i in range(0, action_num):
            out = Q.forward(state, action[i].view(1))
            q_list.append(out.item())
            idx.append(i)
        q_max_list = np.argsort(q_list)

        max = (q_list[q_max_list[action_num - 1]] + q_list[q_max_list[action_num - 2]]) / 2
        return q_max_list[action_num - 1], q_max_list[action_num - 2], max

    def next_take_action(self, next_rf, next_cf, action_num,Q):
        next_state = np.concatenate((next_rf, next_cf))
        next_state = torch.from_numpy(next_state).float()
        next_action = np.zeros(action_num)
        for i in range(0, action_num):
            next_action[i] = i
        next_action = torch.Tensor(next_action)
        Q.eval()
        q_list = []
        for i in range(0, action_num):
            out = Q.forward(next_state, next_action[i].view(1))
            q_list.append(out.item())
        q_max_list = np.argsort(q_list)
        return q_max_list[action_num - 1]



def kakaoFeedback(cf, recommended_news1, recommended_news2, user):  # 선호도 만들기
    favor_news = [1] * 10

    if user == 1:
        for j in range(0, 10):
            if j == 1:
                favor_news[j] = 8  # 80%
            elif j == 2:
                favor_news[j] = 8  # 80%
            else:
                favor_news[j] = 2  # 30%

    elif user == 2:
        for j in range(0, 10):
            if j == 3:
                favor_news[j] = 8  # 80%
            elif j == 4:
                favor_news[j] = 8  # 80%
            else:
                favor_news[j] = 2  # 30%


    if cf[1] == 1 or cf[3]==1:
        favor_news[9] = 10


    users_favor_news = [0] * 10

    for i in range(0, 10):
        k = random.randint(1, 10)
        if (k <= favor_news[i]):
            users_favor_news[i] = 1

    news_read = [-10, -10]
    # 뉴스 선호도 바탕으로 실제 뉴스가 들어왔을 때 뉴스를 읽게 만들기
    if users_favor_news[recommended_news1] == 1:
        news_read[0] = 1
    if users_favor_news[recommended_news2] == 1:
        news_read[1] = 1


    return news_read



# 평균내기 ,전체/개월전/한달전/일주일전 #next state만들기
def s_sp(n_epi, all):
    sum1 = [0] * 10
    start1 = 0
    end1 = n_epi

    for i in range(start1, end1):
        for j in range(10):
            sum1[j] += all[i][j]
    if (n_epi > 0):
        for i in range(10):
            sum1[i] = sum1[i] / (end1 - start1)

    sum2 = [0] * 10
    start2 = n_epi - 30
    end2 = n_epi
    if start2 <= 0:
        start2 = 0

    for i in range(start2, end2):
        for j in range(10):
            sum2[j] += all[i][j]
    if (n_epi > 0):
        for i in range(10):
            sum2[i] = sum2[i] / (end2 - start2)

    sum3 = [0] * 10
    start3 = n_epi - 14
    end3 = n_epi
    if start3 <= 0:
        start3 = 0

    for i in range(start3, end3):
        for j in range(10):
            sum3[j] += all[i][j]
    if (n_epi > 0):
        for i in range(10):
            sum3[i] = sum3[i] / (end3 - start3)

    sum4 = [0] * 10
    for i in range(10):
        sum4[i] += all[n_epi][i]

    # next State
    S_P = np.zeros(40)

    for i in range(10):  # all/epoch
        S_P[i] = sum1[i]

    for i in range(10):  # 3개월
        S_P[10 + i] = sum2[i]

    for i in range(10):  # 한달
        S_P[20 + i] = sum3[i]

    for i in range(10):  # 일주일
        S_P[30 + i] = sum4[i]

    return S_P


def load_users(epochs):
    users = []
    users_rf = []
    users_cf = []
    max_q_list = []
    reward_list = []

    with open("all_list_100000_15.pkl", "rb") as f:
        final_all_list = pickle.load(f)

    with open("users_rf_10000_15.pkl", "rb") as g:
        final_users_rf = pickle.load(g)
    all_list = copy.deepcopy(final_all_list)

    for i in range(1, 3):
        users.append(i)
        max_q_list.append([])
        reward_list.append([])
        users_rf.append(final_users_rf[i-1])

    for i in range(0, epochs + 10):
        E = np.zeros(4)
        if i % 4 == 0:
            E[0] = 1
            users_cf.append(E)
        elif i % 4 == 1:
            E[1] = 1
            users_cf.append(E)
        elif i % 4 == 2:
            E[2] = 1
            users_cf.append(E)
        else:
            E[3] = 1
            users_cf.append(E)

    return users, users_rf, users_cf, all_list, max_q_list, reward_list


def run(users, users_rf, users_cf, all_list, n_epi, answer, recommend, agent,avg_q_list, reward_list,Q):
    n = len(users)
    action1 = [0] * n
    action2 = [0] * n

    isnewsread = [[0] * 3 for _ in range(n)]
    avg_q_value = [0] * n
    rewards = [0] * n

    # 유저별로 추천하는 뉴스 만들기
    for user in range(n):
        action = np.ones(10)
        rf = users_rf[user]
        cf = users_cf[n_epi]
        action1[user], action2[user],avg_q_value[user] = agent.take_action(rf, cf, agent.action_number,Q)
        avg_q_list[user].append(avg_q_value[user])

    # 유저별로 kakao톡에 추천 뉴스 보내주기
    for user in range(n):
        isnewsread[user] = kakaoFeedback(users_cf[n_epi], action1[user],  action2[user],users[user])

    # 유저별로 카카오톡에서 읽은 뉴스들 카테고리 가져와서 학습돌리기
    for user in range(n):
        a_user1_action1_reward = 0
        a_user1_action2_reward = 0


        a_user = [0] * 10

        if isnewsread[user][0] > 0:
            a_user1_action1_reward = 100
            a_user[action1[user]] = 1
            if (n_epi >= 33):
                answer[user][action1[user]] += 1

            if users_cf[n_epi][1] == 1 or  users_cf[n_epi][3]==1:
                if action1[user] == 9:
                    a_user1_action1_reward = 300


        if isnewsread[user][1] > 0:
            a_user1_action2_reward = 100
            a_user[action2[user]] = 1
            if (n_epi >= 33):
                answer[user][action2[user]] += 1
            if users_cf[n_epi][1] == 1 or  users_cf[n_epi][3]==1:
                if action2[user] == 9:
                    a_user1_action2_reward = 300


        recommend[user][action1[user]] += 1
        recommend[user][action2[user]] += 1


        all_list[user].append(a_user)

        S_P = s_sp(n_epi, all_list[user])

        rewards[user] += (a_user1_action1_reward + a_user1_action2_reward )
        reward_list[user].append(rewards[user])

        # state update
        users_rf[user] = S_P

        print("epoch = {} / user {}'s select: {}".format(n_epi, users[user], a_user), end=" ")



    return users_rf, users_cf, all_list, answer, recommend, avg_q_list, reward_list,Q

epochs = 1000
answer = []
recommend = []
for i in range(2):
  a=[0]*10
  answer.append(a)
  recommend.append(a)

path = 'ddqn_model_10000_15_save.pth'
agent= Agent(a)

Q=agent.Q_network
Q.load_state_dict(torch.load(path))
agent.build_optimizer(Q)
Q.eval()

users,users_rf,users_cf, all_list, avg_q_list, reward_list = load_users(epochs)


for n_epi in range(epochs):
  users_rf,users_cf, all_list,answer,recommend, avg_q_list, reward_list,Q =  run(users,users_rf,users_cf, all_list,n_epi,answer,recommend,agent,avg_q_list, reward_list,Q)

for i in range(len(users)):
  print("user{} recommend:{}".format(users[i],recommend[i]))

with open("test_result2_5.pkl", "wb") as t:
    pickle.dump(recommend,t)




user1_result = np.argsort(recommend[0])
user2_result = np.argsort(recommend[1])
print("user 1's most prefer news = {}, {}".format(user1_result[9],user1_result[8]))
print("user 2's most prefer news = {}, {}".format(user2_result[9],user2_result[8]))

import matplotlib.pyplot as plt
import numpy as np
category=['1','2','3','4','5','6','7','8','9','10']
for i in range(2):
  colors=['y'] * 10
  if i==0:
    colors[user1_result[9]]='C2'

  elif i==1:
    colors[user2_result[9]]='C2'




  n=np.arange(10)
  plt.bar(n,recommend[i],color=colors)
  plt.xticks(n,category)
  plt.ylabel('Total Counts')
  plt.xlabel('Preferred Category Index')
  plt.show()
  plt.savefig("Test6 Graph{}.png".format(i+1))

  pd.Series(reward_list[i]).to_csv('final_reward_User_{}.csv'.format(i+1))
  pd.Series(avg_q_list[i]).to_csv('final_avg_Q_list_User_{}.csv'.format(i+1))

reward_user1 = pd.read_csv('final_reward_User_1.csv',index_col=False).iloc[:,1]
reward_user2 = pd.read_csv('final_reward_User_2.csv',index_col=False).iloc[:,1]

q_user1 = pd.read_csv('final_avg_Q_list_User_1.csv',index_col=False).iloc[:,1]
q_user2 = pd.read_csv('final_avg_Q_list_User_2.csv',index_col=False).iloc[:,1]

plt.figure(figsize=(16,8))
plt.plot(reward_user1.cumsum() / (pd.Series(np.arange(reward_user1.shape[0]))+1), label = "Reward_User1")
plt.plot(reward_user2.cumsum() / (pd.Series(np.arange(reward_user2.shape[0]))+1), label = "Reward_User2")
plt.legend()
plt.show()


plt.figure(figsize=(16,8))
plt.plot(q_user1.cumsum() / (pd.Series(np.arange(q_user1.shape[0]))+1), label = "Q_value_User1")
plt.plot(q_user2.cumsum() / (pd.Series(np.arange(q_user2.shape[0]))+1), label = "Q_value_User2")
plt.legend()
plt.show()