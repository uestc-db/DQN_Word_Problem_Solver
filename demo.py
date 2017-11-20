from config import *
from agent import *
from env import *

c = Config()

a = Agent(c.parse_dict[0], c.gold_trees[0])

a.get_feature_from_schema_info()
print a.pair_feat
print a.rel_feat

