import random
import numpy as np


class Environment:
    def __init__(self,player_is_agent=[True,True,True], display='all'):
        self.cards = ['3','3','3','3', '4','4','4','4', '5','5','5','5', '6','6','6','6', \
                      '7','7','7','7', '8','8','8','8', '9','9','9','9', '10','10','10','10', \
                      'J','J','J','J', 'K','K','K','K', 'Q','Q','Q','Q', 'A','A','A','A', \
                      '2','2','2','2', 'LJ','BJ']
        
        self.display = display
        # Player 0 is always landlord, Players 1 and 2 are peasants
        self.player_is_agent = player_is_agent
        #self.just_played_player = -1
        #self.just_played_hand = [False for i in range(54)]
        self.next_player = 0
        self.winner = -1
        self.history_players = []
        self.history_hands = []
        self.table_str = 'On the table:\n'
        self.game_over = False
        self.deal_cards(seed=seed)

    
    def reset(self,player_is_agent=[True,True,True], seed=0):
        self.player_is_agent = player_is_agent
        #self.just_played_player = -1
        #self.just_played_hand = [False for i in range(54)]
        self.next_player = 0
        self.winner = -1
        self.history_players = []
        self.history_hands = []
        self.table_str = 'On the table:\n'
        self.game_over = False
        self.deal_cards(seed=seed)f
        
        self.render()
        return self.get_state()

    
    def deal_cards(self, seed=0):
        player_current_hands = [[False for i in range(54)] for j in range(3)]
        random.seed(a=seed)
        cardlist = range(54)
        random.shuffle(cardlist)
        for _ in range(17):
            for player in range(3):
                player_current_hands[player][cardlist.pop()] = True
        for _ in range(3):
            player_current_hands[0][cardlist.pop()] = True
        self.player_current_hands = player_current_hands
        

    def render(self):
        if self.display!='none':
            self.render_table()
        if self.display=='all' or self.game_over:
            # print all players
            self.render_player_hand(0)
            self.render_player_hand(1)
            self.render_player_hand(2)
        elif self.display=='next':
            # print only the player for next turn
            self.render_player_hand(self.next_player)

    
    def render_table(self):
        print(self.table_str)


    def render_player_hand(self,playerid):
        print('P' + str(playerid) + ': ' + self.get_player_hand(playerid))

    
    def get_player_hand(self,playerid):
        pstr = []
        for i in range(54):
            pstr.append(self.cards[self.player_current_hands[playerid][i]])
            if (i % 4)==3:
                pstr.append(' ')
        return ''.join(pstr)
            
        
    def add_table_str(self):
        # add the most recently played hand to the table str
        thisstr = ''
        if len(self.history_players)>1 and \
        np.sum(self.history_hands[-1])>0 and \
        np.sum(self.history_hands[-2])==0:
            # put a linebreak before the first hand after pass
            thisstr = thisstr + '\n'
        thisstr = thisstr + '[P' + str(self.history_players[-1]) + ': '
        if np.sum(self.history_hands[-1])==0:
            thisstr = thisstr + 'pass]  '
        else:
            for i in range(54):
                if self.history_hands[-1][i]:
                    thisstr = thisstr + self.cards[i]
            thisstr = thisstr + ']  '
        self.table_str = self.table_str + thisstr
        
    
    def get_state(self,playerid):
        # return a vector as input to NN
        state = 
        return state

    def move_agent(self, action):
        # Map agent action to the correct movement
        moves = {
            0: (-1, 0), # Up
            1: (1, 0),  # Down
            2: (0, -1), # Left
            3: (0, 1)   # Right
        }
        
        previous_location = self.agent_location
        
        # Determine the new location after applying the action
        move = moves[action]
        new_location = (previous_location[0] + move[0], previous_location[1] + move[1])
        
        done = False # The episode is not done by default
        reward = 0   # Initialize reward
            
        # Check for a valid move
        if self.is_valid_location(new_location):
            # Remove agent from old location
            self.grid[previous_location[0]][previous_location[1]] = 0
            
            # Add agent to new location
            self.grid[new_location[0]][new_location[1]] = 1
            
            # Update agent's location
            self.agent_location = new_location
            
            # Check if the new location is the reward location
            if self.agent_location == self.goal_location:
                # Reward for getting the goal
                reward = 100
                
                # Episode is complete
                done = True
            else:
                # Calculate the distance before the move
                previous_distance = np.abs(self.goal_location[0] - previous_location[0]) + \
                                    np.abs(self.goal_location[1] - previous_location[1])
                        
                # Calculate the distance after the move
                new_distance = np.abs(self.goal_location[0] - new_location[0]) + \
                               np.abs(self.goal_location[1] - new_location[1])
                
                # If new_location is closer to the goal, reward = 1, if further, reward = -1
                reward = (previous_distance - new_distance) - 0.1
        else:
            # Slightly larger punishment for an invalid move
            reward = -3
        
        return reward, done
    
    def is_valid_location(self, location):
        # Check if the location is within the boundaries of the grid
        if (0 <= location[0] < self.grid_size) and (0 <= location[1] < self.grid_size):
            return True
        else:
            return False
        
    def step(self, action):
        # Apply the action to the environment, record the observations
        reward, done = self.move_agent(action)
        next_state = self.get_state()
    
        # Render the grid at each step
        if self.render_on:
            self.render()
    
        return reward, next_state, done