import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
                (0, 0) <class 'tuple'> TERMINAL_STATE <class 'str'>

              mdp.getPossibleActions(state)
                ('north', 'west', 'south', 'east') ('exit')

              mdp.getTransitionStatesAndProbs(state, action)
                [ ( (0, 1), 0.8 ) , ((0, 0), 0.1), ((1, 0), 0.1)] for next, prob in ... :

              mdp.getReward(state, action, nextState)
                <int>

              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            result = util.Counter()
            for state in self.mdp.getStates():
                if not self.mdp.isTerminal(state):
                    a = self.computeQValueFromValues(state, self.computeActionFromValues(state))
                    result[state] += a
            self.values = result
                

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        tmp = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            tmp += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
        return tmp

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        # ('north', 'west', 'south', 'east') ('exit')
        actions = self.mdp.getPossibleActions(state)
        tmp = util.Counter()
        if actions != None:
            for a in actions:
                tmp[a] += self.computeQValueFromValues(state, a)
            return tmp.argMax()
        else:
            return None    


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
