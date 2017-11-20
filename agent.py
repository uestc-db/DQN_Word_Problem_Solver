from utils import *
import numpy as np
import time

class Node:
    def __init__(self):
        self.is_compound = False
        self.index = []
    
    def init_node(self, i, value):
        self.index.append(i)
        self.value = value

    def is_belong(self, i):
        if i in self.index:
            return True
        return False
 
    def i_and_j_is_belong(self, i, j):
        if i in self.index and j in self.index:
            return True
        return False

    def compute_val(self, v1, v2, op):
        if op == 0:
             return v1 + v2
        elif op == 1:
             return v1 - v2
        elif op == 2:
             return v2 - v1

    def combine_node(self, node1, node2, op):
        self.is_compound = True
        self.op = op
        self.index.extend(node1.index)
        self.index.extend(node2.index)
        value1 = 0
        value2 = 0
        if node1.is_compound == False:
            value1 = float(node1.value)
        else: 
            value1 = node1.value 
        if node2.is_compound == False:
            value2 = float(node2.value)
        else: 
            value2 = node2.value 
        self.value = self.compute_val(value1, value2, op) 

class State:
    def __init__(self, quant_tokens):
        self.nodes = self.get_nodes(quant_tokens) 
        self.fix_nodes = self.get_nodes(quant_tokens)
        self.length = len(self.nodes)

    def str_2_quant(self, word):
        word = word.lower()
        l = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        return l.index(word)+1

    def quant_str_2_quant(self, word):
        try:
            float(word)
        except:
            return str(self.str_2_quant(word)) 
        else:
            return word 

    def get_nodes(self, quant_tokens):
        nodes = []
        for i in range(len(quant_tokens)):
            quant = self.quant_str_2_quant(quant_tokens[i].word_text)
            node = Node()
            node.init_node(i, quant)
            nodes.append(node)
        return nodes 

    def get_node_via_index(self, index):
        for i in range(len(self.nodes)):
            if self.nodes[i].is_belong(index):
                return self.nodes[i]            

    def is_lca_i_and_j(self, i, j):
        for node in self.nodes:
            if node.i_and_j_is_belong(i, j):
                return True
        return False

    def change(self, i, j, newnode):
        li = []
        for node in self.nodes:
            if node.is_belong(i) or node.is_belong(j):
                pass
            else:
                li.append(node)
        li.append(newnode)
        self.nodes = li

    def remove_node(self, i):
        li = []
        for node in self.nodes:
            if node.is_belong(i):
                pass
            else:
                li.append(node)
        self.nodes = li

    def print_state(self):
        print "state:",
        s = '['
        for i in range(len(self.nodes)): 
            s += '['
            for ind in self.nodes[i].index:
                s += str(self.fix_nodes[ind].value) +', '
            s += '], '
        s+= ']' 
        print s 

class Agent:
    def __init__(self, parse_obj, gold_tree, reject, pick):
        self.parse_obj = parse_obj
        self.gold_tree = gold_tree
        self.reject = reject
        self.pick = pick
        

    def print_agent(self):
        print "index:", self.parse_obj.parse_id
        print self.gold_tree.exp_str

    def get_feat_from_json_and_pair_index(self, l, index):
        feat_list = {} 
        for elem in l:
            if elem["index"] == index:
                feat_list[str(elem["interest"])] = elem["feature"]
        return feat_list

    def get_feat_from_json_and_rel_index(self, l, index):
        feat_list = {}
        for elem in l:
            if elem["index"] == index:
                feat_list[str(elem["interest"])] = elem["feature"]
        return feat_list

    def get_feature_from_schema_info(self):
        self.features = {} 
        pairFile = "./data/PairFeat.json"
        relFile = "./data/RelFeat.json"
        pair_list = readJson(pairFile)
        #rel_list = readJson(relFile)
        self.pair_feat = self.get_feat_from_json_and_pair_index(pair_list, self.parse_obj.parse_id)
        #self.rel_feat = self.get_feat_from_json_and_rel_index(rel_list, self.parse_obj.parse_id)

    def get_possible_features(self):
        features = {} 
        for k, v in self.pair_feat.iteritems():
            temp = {}
            for elem in v:
                temp[elem] = 1.0 
            features.update(temp)
        #for k, v in self.rel_feat.iteritems():
        #    temp = {}
        #    for i in [1,2]:
        #        for elem in v:
        #            temp[str(i)+'_'+elem] = 1.0
        #    features.update(temp)
        return features
                
    def get_feat_vector(self, index1, index2, index_to_feat):
        self.features = {}
        self.feat_dim = len(index_to_feat)
        curr_pair_feat = self.pair_feat[str([index1, index2])]
        #curr_rel_feat_1 = self.rel_feat[str(index1)]
        #curr_rel_feat_2 = self.rel_feat[str(index2)]
        for elem in curr_pair_feat:
            self.features[elem] = 1.0
        #for elem in curr_rel_feat_1:
        #    self.features[str(1)+'_'+elem] = 1.0
        #for elem in curr_rel_feat_2:
        #    self.features[str(2)+'_'+elem] = 1.0
        self.feat_vector = [1 if elem in self.features else 0 for index, elem in enumerate(index_to_feat)]    
        return self.feat_vector

    def select_tuple(self):
        self.candidate_select = []
        if self.pick != []:
            self.candidate_select.append(self.pick)
        for i in range(self.state.length):
            for j in range(self.state.length):
                if i!= j and i<j and (not (i in self.pick and j in self.pick)):
                    self.candidate_select.append([i,j]) 
        self.reject_select = self.reject 

    def select_combine(self):
        for elem_pair in self.candidate_select:
            if elem_pair[0] in self.reject_select or elem_pair[1] in self.reject_select \
                                                   or self.state.is_lca_i_and_j(elem_pair[0], elem_pair[1]):
                continue
            else:
                return elem_pair 
        return []

    def init_state_info(self, index_to_feat):
        self.state = State(get_quantities(self.parse_obj))
        for index in self.reject:
            self.state.remove_node(index)
        self.select_tuple()
        self.breakout = 0
        #print "candidate:", self.candidate_select
        #print "reject", self.reject_select
        elem_pair = self.select_combine()
        if not elem_pair:
            self.breakout = 1
            self.feat_dim = len(index_to_feat)
            self.feat_vector = np.zeros(self.feat_dim)
            return
        self.node_1_index = elem_pair[0] 
        self.node_2_index = elem_pair[1]
        self.index_to_feat = index_to_feat
        self.get_feat_vector(self.node_1_index, self.node_2_index, self.index_to_feat)

    def compound_two_nodes_predict(self, op, loc, prefix="./test/analysis_"):
        filename = prefix + loc 
        start = time.time()
        if self.breakout == 1:
            #self.write_single_info(filename, 1, "parse", "_error")
            return np.zeros(self.feat_dim), 1, 0, time.time() - start

        self.reward = 0
        node1 = self.state.get_node_via_index(self.node_1_index)
        node2 = self.state.get_node_via_index(self.node_2_index)
        fix_node1 = self.state.fix_nodes[self.node_1_index]
        fix_node2 = self.state.fix_nodes[self.node_2_index]
        self.write_info(filename, op)
        newNode = Node()
        newNode.combine_node(node1, node2, op)
        self.state.change(self.node_1_index, self.node_2_index, newNode)
        if len(self.state.nodes) == 1:
            if abs(float(self.state.nodes[0].value) - float(self.gold_tree.gold_ans)) < 1e-4:
                #self.write_single_info(filename, 1, "compute_state_node==1", "_right")
                return np.zeros(self.feat_dim), 1, 1, time.time() - start
            else:
                #self.write_single_info(filename, 1, "compute_state_node==1", "_error")
                return np.zeros(self.feat_dim), 1, 0, time.time() - start
        elif len(self.state.nodes) == 0:
            #self.write_single_info(filename, 1, "state_node==0", "_error")
            return np.zeros(self.feat_dim), 1, 0, time.time() - start
        else:
            elem_pair = self.select_combine()
            self.node_1_index = elem_pair[0]
            self.node_2_index = elem_pair[1]
            next_states = self.get_feat_vector(self.node_1_index, self.node_2_index, self.index_to_feat)
            #self.write_single_info(filename, 1, "next", "_step")
            return next_states, 0, 0, time.time() - start
            
    def compound_two_nodes(self, op):
        self.reward = 0
        if self.breakout == 1:
            return np.zeros(self.feat_dim), 0, 1, 0

        node1 = self.state.get_node_via_index(self.node_1_index)
        node2 = self.state.get_node_via_index(self.node_2_index)
        fix_node1 = self.state.fix_nodes[self.node_1_index]
        fix_node2 = self.state.fix_nodes[self.node_2_index]
        flag1 = False
        flag2 = False
        if node1.is_compound:
            flag1 =  True
        else:
            if self.gold_tree.is_in_rel_quants(fix_node1.value):
                flag1 = True
            else:
                flag1 = False
        if node2.is_compound:
            flag1 =  True
        else:
            if self.gold_tree.is_in_rel_quants(fix_node2.value):
                flag2 = True
            else:
                flag2 = False
        self.flag1 = flag1
        self.flag2 = flag2
        if op == 0:
            if flag1 and flag2:
                if self.gold_tree.query(fix_node1.value, fix_node2.value) == '+':
                    newNode = Node()
                    newNode.combine_node(node1, node2, op)
                    self.state.change(self.node_1_index, self.node_2_index, newNode)
                    if len(self.state.nodes) == 1:
                        if abs(float(self.state.nodes[0].value) - float(self.gold_tree.gold_ans)) < 1e-4:
                            return np.zeros(self.feat_dim), 5, 1, 1
                        else:
                            return np.zeros(self.feat_dim), -1, 1, 0
                    elif len(self.state.nodes) == 0:
                        return np.zeros(self.feat_dim), -1, 1, 0
                    else:
                        elem_pair = self.select_combine()
                        if len(elem_pair) == 0:
                            return np.zeros(self.feat_dim), -1, 2, 0
                        self.node_1_index = elem_pair[0]
                        self.node_2_index = elem_pair[1]
                        self.candidate_select.remove(elem_pair)
                        next_states = self.get_feat_vector(self.node_1_index, self.node_2_index, self.index_to_feat)
                        return next_states, 5, 0, 0
                else:
                    return np.zeros(self.feat_dim), -5, 3, 0
            else:
                return np.zeros(self.feat_dim), -5, 4, 0
        elif op == 1:
            if flag1 and flag2:
                if self.gold_tree.query(fix_node1.value, fix_node2.value) == '-':
                    newNode = Node()
                    newNode.combine_node(node1, node2, op)
                    if newNode.value < 0 :
                        return np.zeros(self.feat_dim), -5, 1, 1
                    self.state.change(self.node_1_index, self.node_2_index, newNode)
                    if len(self.state.nodes) == 1:
                        if abs(float(self.state.nodes[0].value) - float(self.gold_tree.gold_ans)) < 1e-4:
                            return np.zeros(self.feat_dim), 5, 1, 1
                        else:
                            return np.zeros(self.feat_dim), -1, 1, 0
                    elif len(self.state.nodes) == 0:
                        return np.zeros(self.feat_dim), -1, 1, 0
                    else:
                        elem_pair = self.select_combine()
                        if len(elem_pair) == 0:
                            return np.zeros(self.feat_dim), -1, 2, 0
                        self.node_1_index = elem_pair[0]
                        self.node_2_index = elem_pair[1]
                        self.candidate_select.remove(elem_pair)
                        next_states = self.get_feat_vector(self.node_1_index, self.node_2_index, self.index_to_feat)
                        return next_states, 5, 0, 0
                else:
                    return np.zeros(self.feat_dim), -5, 3, 0
            else:
                return np.zeros(self.feat_dim), -5, 4, 0
        else:
            if flag1 and flag2:
                if self.gold_tree.query(fix_node1.value, fix_node2.value) == '-':
                    newNode = Node()
                    newNode.combine_node(node1, node2, op)
                    if newNode.value < 0 :
                        return np.zeros(self.feat_dim), -5, 1, 1
                    self.state.change(self.node_1_index, self.node_2_index, newNode)
                    if len(self.state.nodes) == 1:
                        if abs(float(self.state.nodes[0].value) - float(self.gold_tree.gold_ans)) < 1e-4:
                            return np.zeros(self.feat_dim), 5, 1, 1
                        else:
                            return np.zeros(self.feat_dim), -1, 1, 0
                    elif len(self.state.nodes) == 0:
                        return np.zeros(self.feat_dim), -1, 1, 0
                    else:
                        elem_pair = self.select_combine()
                        if len(elem_pair) == 0:
                            return np.zeros(self.feat_dim), -1, 2, 0
                        self.node_1_index = elem_pair[0]
                        self.node_2_index = elem_pair[1]
                        self.candidate_select.remove(elem_pair)
                        next_states = self.get_feat_vector(self.node_1_index, self.node_2_index, self.index_to_feat)
                        return next_states, 5, 0, 0
                else:
                    return np.zeros(self.feat_dim), -5, 3, 0
            else:
                return np.zeros(self.feat_dim), -5, 4, 0

        

    def test_gate(self, flag):
        self.test_flag = flag

    def write_info(self, filename, op):
        with open(filename, 'a') as f:
            f.write("index: " + str(self.parse_obj.parse_id) + '\n')
            f.write(self.parse_obj.word_problem_text+'\n')
            f.write("equations: " + str(self.gold_tree.exp_str) + '\n' )
            f.write("node_1: " + str((self.state.fix_nodes[self.node_1_index]).value) + ", node_2: " + str((self.state.fix_nodes[self.node_2_index]).value) + '\n')
            f.write("op: " + (['+','-','in-','11','22','33'][op]) + '\n')
            f.write("gold_ans: " + str(self.gold_tree.gold_ans) + '\n')

    def write_single_info(self, filename, flag, prefix, content):
        if flag:
            with open(filename, 'a') as f:
                f.write(prefix + content + '\n\n')

