import json

def writeJson(filename, data):
    data = json.dumps(data, indent=4)
    with open(filename, 'w') as f:
        f.write(data)

def read_m(filename):
    data = {}
    with open(filename, 'r') as f:
        for line in f:
            if '---' in line:
                line = line.strip().split('\t')
                data[line[1]] = 1
    return data

l_0 = read_m("./m_0")
l_1 = read_m("./m_1")
l_2 = read_m("./m_2")
l_3 = read_m("./m_3")
l_4 = read_m("./m_4")

d = {}
d.update(l_0)
d.update(l_1)
d.update(l_2)
d.update(l_3)
d.update(l_4)


writeJson("./RL_AI2.json",d )

print len(d)

                     
