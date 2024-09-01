import gym
import collections
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Hyperparameters
learning_rate = 0.0005
gamma = 0.98
buffer_limit = 50000
batch_size = 32


class ReplayBuffer():
    def __init__(self): # 양방향 que
        self.buffer = collections.deque(maxlen=buffer_limit)

    def put(self, transition): # transition 저장
        self.buffer.append(transition)

    def sample(self, n): # 메모리로 부터 batch size 길이 만큼 list 반환하기
        mini_batch = random.sample(self.buffer, n)
        s_lst, a_lst, r_lst, s_prime_lst, done_mask_lst = [], [], [], [], []

        for transition in mini_batch:
            s, a, r, s_prime, done_mask = transition # state, action, reward
            s_lst.append(s)
            a_lst.append([a])
            r_lst.append([r])
            s_prime_lst.append(s_prime)
            done_mask_lst.append([done_mask])

        return torch.tensor(s_lst, dtype=torch.float), torch.tensor(a_lst), \
               torch.tensor(r_lst), torch.tensor(s_prime_lst, dtype=torch.float), \
               torch.tensor(done_mask_lst)

    def size(self): #buffer size 반환
        return len(self.buffer)


class Qnet(nn.Module): #현재의 입력에 대한 각 행동의 기대값을 예측하기
    def __init__(self):
        super(Qnet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        coin = random.random()
        if coin < epsilon:
            return random.randint(0, 1) #엡실론 그리디 사용하여 random 값 sample 뽑기 -> 초기에 엡실론 크게하여 다양한 경험, 점차 신경망 선택
        else:
            return out.argmax().item() # -> 이부분을 이제 어떻게 sample을 뽑을지 생각해야할듯. 단순히 argmax가 아니라 가장유사한 sample을 뽑아주어야 하므로
                                        # 아마 sample 중 유사도가 높은 값을 뽑을 수 있도록 하기 -> 어떻게 뽑을것인가 ? ex) 유사도 높을 수록 가중치를 높여서 argmax 시키기

# 생각하는 feature  state[0~4 user index][0~5 news feature] [0~2 news feature 별 정보]
# 생각하는 action  action[0~10] 전체 뉴스 중 뽑힌 10개의 뉴스

def train(q, q_target, memory, optimizer): # 메모리에 쌓아둔 경험들을 재학습하며 학습함.
    for i in range(10):
        s, a, r, s_prime, done_mask = memory.sample(batch_size) #sample 값 만들고

        q_out = q(s) #state 바탕으로 q 값 만들고
        q_a = q_out.gather(1, a) # action을 사용할 수 있는 형태로 뽑아서 만들기 -> 현상태 했던 행동 가치(q값)을 q_a로 모음
        max_q_prime = q_target(s_prime).max(1)[0].unsqueeze(1) #에이전트가 보는 행동의 미래 가치(max_q_prime)
        target = r + gamma * max_q_prime * done_mask # 기대 q 값 계산 (reward + 미래 가치)
        loss = F.smooth_l1_loss(q_a, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


def main():
    env = gym.make('CartPole-v1')
    q = Qnet()
    q_target = Qnet()
    q_target.load_state_dict(q.state_dict())
    memory = ReplayBuffer()

    print_interval = 20
    score = 0.0
    optimizer = optim.Adam(q.parameters(), lr=learning_rate)

    for n_epi in range(10000):
        epsilon = max(0.01, 0.08 - 0.01 * (n_epi / 200))  # Linear annealing from 8% to 1%
        s = env.reset()
        done = False

        while not done:
            a = q.sample_action(torch.from_numpy(s).float(), epsilon)
            s_prime, r, done, info = env.step(a)
            done_mask = 0.0 if done else 1.0 #mask 된 것 나누기
            memory.put((s, a, r / 100.0, s_prime, done_mask))
            s = s_prime

            score += r
            if done:
                break

        if memory.size() > 2000:
            train(q, q_target, memory, optimizer)

        if n_epi % print_interval == 0 and n_epi != 0:
            q_target.load_state_dict(q.state_dict())
            print("n_episode :{}, score : {:.1f}, n_buffer : {}, eps : {:.1f}%".format(
                n_epi, score / print_interval, memory.size(), epsilon * 100))
            score = 0.0
    env.close()


if __name__ == '__main__':
    main()