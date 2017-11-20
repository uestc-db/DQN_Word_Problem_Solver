import json

def return_num(num_folds):
  config = []
  for i in range(num_folds):
    filename = "reward_list_"+str(i)+".json"
    data = []
    with open(filename, 'r') as f:
      data = json.load(f)
    config.append(data)
  return config

config = return_num(5)

new = []
reward = []
for i in range(5):
  for j in range(len(config[i])):
    if i == 0:
        reward.append(config[i][j]/5)
    else:
        reward[j] += config[i][j]/5

for elem in reward:
    print elem

with open('reward.json', 'w') as f:
  json.dump(reward, f)

