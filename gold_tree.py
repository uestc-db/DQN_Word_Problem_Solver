class GoldNode:
    def __init__(self, value = '', left_node = None, right_node = None):
        self.value = value
        self.left_node = left_node
        self.right_node = right_node

class GoldTree:
    def __init__(self, gold_ans, equ_str_l):
        self.exp_str = equ_str_l 
        self.rel_quants = self.get_relevance_quant()
        self.gold_ans = gold_ans
        self.root = self.build_tree(0, len(self.exp_str))

    def is_float(self, num_str):
        try:
            float(num_str)
        except:
            return False
        else: 
            return True

    def get_relevance_quant(self):
        l = []
        for elem in self.exp_str:
            if self.is_float(elem):
                l.append(elem)
        return l

    def is_in_rel_quants(self, value):
        for elem in self.rel_quants:
            if abs(float(str(value)) - float(str(elem))) < 1e-5 :
                return True 
        return False 

    def build_tree(self, x, y):
        c1 = -1      
        c2 = -1
        p = 0
        node = GoldNode()
        if y-x == 1:
            node.value = self.exp_str[x]
            return node
        for i in range(len(self.exp_str))[x:y]:
            if self.exp_str[i] == '(':
                p+=1
            elif self.exp_str[i] == ')': 
                p-=1
            elif self.exp_str[i] == '+' or self.exp_str[i] == '-':
                if p == 0:
                    c1 = i
            elif self.exp_str[i] == '*' or self.exp_str[i] == '/':
                if p == 0:
                    c2 = i
        if c1 < 0:
            c1 = c2
        if c1 < 0:
            return self.build_tree(x+1, y-1)
        node.left_node = self.build_tree(x, c1)
        node.right_node = self.build_tree(c1+1, y) 
        node.value = self.exp_str[c1]
        return node

    def pre_order(self, root):
        if root == None:
            return
        print root.value,
        self.pre_order(root.left_node)
        self.pre_order(root.right_node)
    
    def mid_order(self, root):
        if root == None:
            return 
        self.mid_order(root.left_node)
        print root.value,
        self.mid_order(root.right_node)

    def post_order(self, root):
        if root == None:
            return
        self.post_order(root.left_node)
        self.post_order(root.right_node)
        print root.value,

    def is_equal(self, v1, v2):
        if self.is_float(v1) == False or self.is_float(v2) == False:
            return False 
        if abs(float(v1) - float(v2)) < 1e-5 :
            return True
        return False

    def lca(self, root, va, vb, parent):
        left = False
        right = False
        if not self.result and root.left_node:
            left = self.lca(root.left_node, va, vb, root)
        if not self.result and root.left_node:
            right = self.lca(root.right_node, va, vb, root)
        mid = False
        if self.is_equal(root.value, va) or self.is_equal(root.value, vb):
            mid = True
        if not self.result  and (left+right+mid) == 2:
            if mid:
                self.result = parent
            else:
                self.result = root
        return left or mid or right
    
    def query(self, va, vb):
        if self.root == None:
            return None
        self.result = None
        self.lca(self.root, va, vb, None )
        if self.result:
            return self.result.value
        else:
            return self.result
