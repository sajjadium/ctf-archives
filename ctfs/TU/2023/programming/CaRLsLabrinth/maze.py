import numpy as np

# See solution for source of mdp

class MDP:
  def __init__(self,T,R):
    '''
    Inputs:
    T -- Transition function: |A| x |S| x |S'| array
    R -- Reward function: |A| x |S| array
    '''
    self.nActions = T.shape[0]
    self.nStates = T.shape[1]
    self.T = T
    self.R = R
    self.discount = 0.99
  
  def sampleRewardAndNextState(self,state,action):
    '''
    state -- current state
    action -- action to be executed

    reward -- sampled reward
    nextState -- sampled next state
    '''

    reward = self.R[action,state]
    nextState = np.argmax(np.random.multinomial(1,self.T[action,state,:]))
    return [reward,nextState]
  
  def solve_maze():
    #TODO: can you find the best policy?
    # Return a list of integers refering to the best action at each state. 
    # If more than one action is equal, return the lowest numbered action
    return 1
  
T = np.load("T.npy")
R = np.load("R.npy")

mdp = MDP(T,R)
nActions = 4 # the actions are the integers 0 to 3 inclusive
nStates = 65 # the states are the integers 0 to 64 inclusive
