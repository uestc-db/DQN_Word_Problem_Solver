from env import *
from config import *

config = Config()
env = Env(config)
env.make_env()

env.set_inner_count_zero()
env.count = 182 
env.reset()
env.curr_agent.print_agent()
env.curr_agent.state.print_state()
print env.curr_agent.node_1_index, env.curr_agent.node_2_index
print "hhhh",env.step(8)
env.curr_agent.state.print_state()
print 

print 'hhhh',env.step(1)
env.curr_agent.state.print_state()
print 

