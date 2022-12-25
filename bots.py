#!/usr/bin/python
import math
import numpy as np
from GoT_problem import *
from GoT_types import CellType
import random
import getch
from sys import maxsize as inf

# import msvcrt


# Throughout this file, ASP means adversarial search problem.
class StudentBot:
    """ Write your student bot here """

    @staticmethod
    def distance(loc1, loc2):
        r1, c1 = loc1
        r2, c2 = loc2
        return (abs(r2-r1) + abs(c2-c1))/2
    
    ## WE SHOULD TRY TO CREATE FUNCTION OR ACCESS ON (GOT_PROBLEM FUNCTION: DETECT_SPACE _INSIDE)
    ##
    def _check_hit_own_trail(self, asp, board, loc, ptm):
        """If the player hit one's own trail, the current player loses"""
        r, c = loc
        if board[r][c] == asp.players[ptm]["TEMP"]:
            return True
        return False

    def _check_ww_hit_my_trail(self, asp, board, loc, ptm):
        """If the ww hit one's own trail, the current player loses"""
        r, c = loc
        if board[r][c] == asp.players[ptm]["TEMP"]:
            return True
        return False

    def _check_hit_other_trail(self, asp, board, loc, ptm):
        """If the player hits the other player's trail, the opponent loses"""
        r, c = loc
        next_ptm = 1 - ptm
        if board[r][c] == asp.players[next_ptm]["TEMP"]:
            return True
        if board[r][c] == asp.get_player_head(next_ptm):
            return True
        return False
    
    def sigmoid(self, total):
        return 1 / (1 + math.exp(-total))


    #use this to keep track of WW movement
    #def __init__(self):
     #   self.
    def __init__(self):
        self.prev_cell_type = None
        self.last_move = None
        self.ptm = None
        self.perm_cell = None
        self.temp_cell = None
        self.opp_temp_cell = None
        self.prevWWDis = 0
        self.prevWWDisTEMP = 0
        self.prevOpp = 0
        self.templength = 0

    def heuristicNoWW(self, asp: GoTProblem, state: GoTState):
            #need a heurisitc that occurs without ww present
        if asp.is_terminal_state(state):
            return asp.evaluate_state(state)[0]
        total = 0
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        next_ptm = asp.get_next_player(ptm)
        opponLoc = locs[next_ptm]
        enclosed_space = GoTProblem._count_space_players(board, state.prev_cell_type, asp.players)
        space_diff = enclosed_space[0] - enclosed_space[1]
        total += space_diff
    
        #tried to do something, where we are emore aggressive the closer we are--not rly working
        across = (len(board), len(board[0]))
        away = self.distance(loc, across)
        opponent = self.distance(loc, opponLoc)
        opponent = self.distance(loc, opponLoc)
        safe = asp.get_safe_actions(board,loc,ptm)
        goHere = asp.move(loc, safe.pop())
        incent = self.distance(loc, goHere)
        
        goback = self.distance(loc, (0,0))


        safe = asp.get_safe_actions(board,loc,ptm)
    # while len(safe) !=0:
        #    goHere = asp.move(loc, safe.pop())
        #   if goHere == asp.players[ptm]["TEMP"]:
        #      incent = self.distance(loc, goHere)

        if opponent > 2:
            if away >= 2:
                total -= 2*away
        else:
            #total-=10
            if self.distance(loc,goHere) == 1 and self._check_hit_own_trail(asp,board,goHere, ptm)==False and self._check_hit_other_trail(asp,board,goHere, ptm)==True:
                print('opp', opponent)
                total+=1000
        return total

    def heuristic(self, asp: GoTProblem, state: GoTState):
        #print('in Hueristic; Is it Terminal', asp.is_terminal_state(state))
        if asp.is_terminal_state(state):
            return asp.evaluate_state(state)[0]
        total = 0
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        next_ptm = asp.get_next_player(ptm)
        opponLoc = locs[next_ptm]

        #setting our instance variables
        self.perm_cell = CellType.TWO_PERM
        self.temp_cell = CellType.TWO_TEMP
        self.opp_temp_cell = CellType.ONE_TEMP
        if ptm == 0:
            self.perm_cell = CellType.ONE_PERM
            self.temp_cell = CellType.ONE_TEMP
            self.opp_temp_cell = CellType.TWO_TEMP
        #useful distance variables
        opponent = self.distance(loc, opponLoc)
        opponToTemp = self.min_dist_to_temp(board, opponLoc, self.temp_cell)
        playerToTemp = self.min_dist_to_temp(board, loc, self.temp_cell)
        playerToPerm = self.min_dist_to_temp(board, loc, self.perm_cell)
        killShot = self.min_dist_to_temp(board, loc, self.opp_temp_cell)
        opponToSelf = self.min_dist_to_temp(board, opponLoc, self.opp_temp_cell)


        self
        goback = self.distance(loc, (0,0))


        safe = asp.get_safe_actions(board,loc,ptm)

        #print("heur: loc", loc)
        #print(self._check_hit_other_trail(asp,board,loc, ptm))


        #trying to see if we can tell if the ww or other player is close to our path--not wokring perfectly
       # if self._check_hit_other_trail(asp,board,loc, ptm):
          #  total += 20.0
        #if self._check_hit_own_trail(asp,board,loc, ptm):
         #   total -= 100.0


        ww_locs = state.ww_locs

        #if self._check_ww_hit_my_trail(asp,board,ww_locs[0], ptm):
         #   total -= 100.0
        # Get the total distance of the player from all White Walkers; choose the distance closest
        #ww_dist 
        #go through each ww
        for i in range(len(ww_locs)):
            distFromWW = self.distance(loc, ww_locs[i])

           #counter = 0
           #white walker to distance to temp:
            wwTemp = self.min_dist_to_temp(board, ww_locs[i], self.temp_cell)
           #ration of ww to temp against player to perm
            if wwTemp < playerToPerm:
                total -= 60
            #dont get hit by ww
            if distFromWW < 2 or wwTemp < 2:
                total -= 20
                #this for some reason allows me to win in small room      
                #if asp.players[ptm]["PERM"] == board[loc[0]][loc[1]]:
                 #   total -= 10
            #dont get hit by ww
            if distFromWW < 1 or wwTemp < 1:
                total -= 30
            #hit other's trail before opp hits mine
            if killShot < opponToSelf and opponToTemp < playerToPerm:
                total += 200

            #this is crazy so idk   
            #print('tjis comp', self.prevWWDisTEMP, wwTemp)  
            #incentivize movement if ww and opp are moving away 
            if self.prevWWDis <= distFromWW and self.prevOpp < opponent:
                    if opponent > 2 and distFromWW > 2 and wwTemp > playerToPerm and opponToTemp > playerToPerm:
                        if self.min_dist_to_temp(board, loc, CellType.SPACE) < (min(distFromWW,opponent)+1) or self.min_dist_to_temp(board, loc, CellType.TWO_PERM ) < (min(distFromWW,opponent)+1):
                            total += 5
                        if len(self.temp_barrier_locs_from_board(board, self.temp_cell))>5:
                            total -= 3*len(self.temp_barrier_locs_from_board(board, self.temp_cell))
    
                  
            #print(self.prevWWDis >= distFromWW)
            #if self.prevWWDisTEMP >= wwTemp:
             #   if wwTemp < playerToPerm:
              #      total -= 100

                #if distFromWW < 2 or wwTemp < 2:
                 #   total -= 30
                #this for some reason allows me to win in small room      
                #if asp.players[ptm]["PERM"] == board[loc[0]][loc[1]]:
                 #   total -= 10
                #if distFromWW < 1 or wwTemp < 1:
                 #   total -= 200
              #  if wwTemp < playerToPerm:
              #      total -=100
               # if playerToPerm <= 1:
                #    total +=100
    
            self.prevWWDis = distFromWW
            self.prevWWDisTEMP = wwTemp
            #if asp.players[ptm]["TEMP"] == board[ww_locs[0][0]][ww_locs[0][1]]:
             #   total -= 1000
            #if self.min_dist_to_temp(board, ww_locs[i], self.temp_cell) <= 2:
             #   total += 1000
                
           ##now try store this distance or point and see where it will go next
            # ww_dist = min([self.distance(loc, ww) for ww in ww_locs])
            # Get the difference in claimed space
            #print("heur ww dist", ww_dist)
       
            #what happens if i am close to white walker, go back to where I was:
        #incentivize taking up perms
        enclosed_space = GoTProblem._count_space_players(board, state.prev_cell_type, asp.players)
        space_diff = enclosed_space[0] - enclosed_space[1]
        total += space_diff 

        #extra, maybe it helps

        # while len(safe) !=0:
        #    goHere = asp.move(loc, safe.pop())
        #   if goHere == asp.players[ptm]["TEMP"]:
        #      incent = self.distance(loc, goHere)

        #decentivize touching my own temp
        #if playerToTemp == 0:
        #    total += 10
        #decentivize my opponent coming near my temp
        #if opponToTemp == 0:
        #    total += 5
        #decentivize touching my own temp
        #if asp.players[ptm]["TEMP"] == board[loc[0]][loc[1]]:
        #    total += 5
        #decentivize my opponent coming near my temp
        #if asp.players[ptm]["TEMP"] == board[opponLoc[0]][opponLoc[1]]:
        #    total += 5
        #incentize me hitting my opponent temp
        #if asp.players[next_ptm]["TEMP"] == board[loc[0]][loc[1]]:
        #    total -= 5
        #incentive going back to my permanent
        #if asp.players[ptm]["PERM"] == board[loc[0]][loc[1]]:
        #    total -= 5

        #if self.min_dist_to_temp(board, loc, self.perm_cell) > 2:
         #   total += 1000



        
        
       
        #if len(self.temp_barrier_locs_from_board(board, self.temp_cell)) == 0:
        #    total += 1000
        #print('my len', len(self.temp_barrier_locs_from_board(board, self.temp_cell)))
        #if len(self.temp_barrier_locs_from_board(board, self.temp_cell)) != 0:
         #   if len(self.temp_barrier_locs_from_board(board, self.temp_cell)) < 5 and len(self.temp_barrier_locs_from_board(board, self.temp_cell)) > 0:
          #      total += 5
           # else:
            #   total -= 3*len(self.temp_barrier_locs_from_board(board, self.temp_cell))
                #if self.min_dist_to_temp(board, loc, self.perm_cell) == 1:
                 #   total -= 10
        #else:
         #   total -=5
        #incentivize movement if no temps
        if len(self.temp_barrier_locs_from_board(board, self.temp_cell)) == 0:
            if self.min_dist_to_temp(board, loc, CellType.SPACE) < (min(distFromWW,opponent)+1) or self.min_dist_to_temp(board, loc, CellType.TWO_PERM ) < (min(distFromWW,opponent)+1):
                total +=25



                #if self.min_dist_to_temp(board, loc, CellType.SPACE) == 0 or self.min_dist_to_temp(board, loc, CellType.TWO_PERM ) == 0:
                 #   total += 25
                #if self.min_dist_to_temp(board, loc, CellType.SPACE) == 1 or self.min_dist_to_temp(board, loc, CellType.TWO_PERM ) == 1:
                #    total += 15
                #if self.min_dist_to_temp(board, loc, CellType.SPACE) == 2 or self.min_dist_to_temp(board, loc, CellType.TWO_PERM ) == 2:
                #    total += 10
                #if self.min_dist_to_temp(board, loc, CellType.SPACE) == 3 or self.min_dist_to_temp(board, loc, CellType.TWO_PERM ) == 3:
                #    total += 5
           # total -= 5
        #print(self.templength == (len(self.temp_barrier_locs_from_board(board, self.temp_cell)) == 0))
        #if self.templength == (len(self.temp_barrier_locs_from_board(board, self.temp_cell)) == 0):
         #   total -=20
        #self.templength = len(self.temp_barrier_locs_from_board(board, self.temp_cell))



    
         #   print('goh', goHere)
          #  print('safe actions',safe)
            #best = 0
           # if asp.players[ptm]["PERM"] == board[loc[0]][loc[1]]:
            #    total -= 14000
               #now incentiveze going
            #if asp.players[ptm]["PERM"] == board[across[0]][across[1]]:
             #   total -= away*(2)
         #  if away > 2:
        #        total -= away*(.5)
         # total -= 20

       
        #total-=10
        #if self.distance(loc,goHere) == 1 and self._check_hit_own_trail(asp,board,goHere, ptm)==False and self._check_hit_other_trail(asp,board,goHere, ptm)==True:
            #print('opp', opponent)
           # total+=1000


        #Do not hit my temp
        if playerToTemp == 0:
            total -= 60

        #ratio of their distance to my temp versus me to my permanent head
        if opponToTemp < playerToPerm:
            total -=60
        #if opponToTemp < 2:
         #   total-= 40

        #if opponent < 3 or opponToTemp < 3:
            #if asp.players[ptm]["PERM"] == board[loc[0]][loc[1]]:
             #       total -= 100000
         #   total -= 10
        #if opponent < 2 or opponToTemp < 2:
            #if asp.players[ptm]["PERM"] == board[loc[0]][loc[1]]:
             #   total -= 10000000
         #   total -= 20
         #stay away from opponent and from opp close to temp
        if opponent < 1 or opponToTemp < 1:
            total -= 60
        

        self.prevOpp = opponent

        #print('loc','space diff','totals:', loc, space_diff, total, self.sigmoid(total)) 
        return self.sigmoid(total)
    
    def attackheur(self, asp: GoTProblem):
        def __init__AT(self):
            self.prev_cell_type = None
            self.last_move = None
            self.ptm = None
            self.perm_cell = None
            self.temp_cell = None
            self.opp_temp_cell = None

        def cleanupAT(self):
            self.prev_cell_type = None
            self.last_move = None
            self.ptm = None
            self.perm_cell = None
            self.temp_cell = None
            self.opp_temp_cell = None

        def dist_from_opp(self, opp_loc, ptm_loc):
            dist = 0
            for i in range(len(opp_loc)):
                dist += abs(opp_loc[i] - ptm_loc[i])
            return dist

        def min_dist_to_temp(self, board, ptm_loc):
            locs = self.temp_barrier_locs_from_board(board)
            min_dist = math.inf
            for loc in locs:
                this_dist = self.dist_from_opp(loc, ptm_loc)
                if this_dist < min_dist:
                    min_dist = this_dist
            return min_dist

        def temp_barrier_locs_from_board(self, board):
            if self.opp_temp_cell is None:
                return []
            loc_dict = {}
            num_temp = 0
            for r in range(len(board)):
                for c in range(len(board[r])):
                    char = board[r][c]
                    if char == self.opp_temp_cell:
                        loc_dict[num_temp] = (r, c)
                        num_temp += 1
            loc_list = []
            for index in range(num_temp):
                loc_list.append(loc_dict[index])
            return loc_list

        def decideAT(self, asp):
            """
            Input: asp, a GoTProblem
            Output: A direction in {'U','D','L','R'}
            """
            state = asp.get_start_state()
            locs = state.player_locs
            board = state.board
            ptm = state.ptm
            loc = locs[ptm]
            possibilities = list(GoTProblem.get_safe_actions(board, loc, ptm))
            opp_loc = locs[(ptm + 1) % 2]
            if self.ptm is None:
                self.ptm = ptm
                self.perm_cell = CellType.TWO_PERM
                self.temp_cell = CellType.TWO_TEMP
                self.opp_temp_cell = CellType.ONE_TEMP
                if ptm == 0:
                    self.perm_cell = CellType.ONE_PERM
                    self.temp_cell = CellType.ONE_TEMP
                    self.opp_temp_cell = CellType.TWO_TEMP

            if not possibilities:
                return "U"

            if self.prev_cell_type is None:
                "Attack bot starting"
                self.prev_cell_type = self.temp_cell
                this_move = possibilities[0]
                self.last_move = this_move
                return this_move

            # if player needs to return to perm area
            must_return_to_perm = False
            if self.prev_cell_type == self.temp_cell:
                this_move = None
                if self.last_move == "U":
                    this_move = "D"
                elif self.last_move == "D":
                    this_move = "U"
                elif self.last_move == "R":
                    this_move = "L"
                elif self.last_move == "L":
                    this_move = "R"
                else:
                    raise Exception

                self.prev_cell_type = self.perm_cell
                self.last_move = this_move
                must_return_to_perm = True

            # else, player is (potentially) leaving perm area
            min_dist = math.inf
            min_dist_to_temp = math.inf
            go_for_temp = False
            decision = possibilities[0]
            min_next_loc = [None] * 2
            for move in possibilities:
                next_loc = GoTProblem.move(loc, move)
                dist_from_opponent = self.dist_from_opp(next_loc, opp_loc)
                this_dist_to_temp = self.min_dist_to_temp(board, next_loc)
                if this_dist_to_temp == 0:
                    return move

                if not must_return_to_perm:
                    # If we are close to temp barrier
                    if this_dist_to_temp <= 5 or go_for_temp:
                        go_for_temp = True
                        if this_dist_to_temp < min_dist_to_temp:
                            min_dist_to_temp = this_dist_to_temp
                            decision = move
                            min_next_loc = next_loc

                    elif dist_from_opponent < min_dist:
                        min_dist = dist_from_opponent
                        decision = move
                        min_next_loc = next_loc
                        min_dist_to_temp = this_dist_to_temp

                    elif dist_from_opponent == min_dist:
                        if this_dist_to_temp < min_dist_to_temp:
                            min_dist_to_temp = this_dist_to_temp
                            decision = move
                            min_next_loc = next_loc

            if not must_return_to_perm:
                if board[min_next_loc[0]][min_next_loc[1]] == self.perm_cell:
                    self.prev_cell_type = self.perm_cell
                else:
                    self.prev_cell_type = self.temp_cell
                self.last_move = decision
            return self.last_move

    def maxvalueAB(self, asp: GoTProblem, currState: GoTState, ptm, board, alpha: int, beta: int, cutoff: int, heuristic):
        move = None
        #print('cutoff',cutoff)
        #print(asp.is_terminal_state(currState))
        if asp.is_terminal_state(currState):
            #evaluate the terminal and index by player
            #print('maxAB evaluate state', (asp.evaluate_state(currState)[ptm], move))
            return (asp.evaluate_state(currState)[ptm], move)
        if cutoff == 0:
            #print('max heur', (heuristic(asp,currState), move))
            return (heuristic(asp,currState), move)
        v = inf*-1
        #go through all action states possible
        for action in asp.get_safe_actions(board, currState.player_locs[ptm], ptm):
            #print('maxvalueAB action', action)
            #pass my the alpha and beta values from this given node into its children 
            v2 = self.minvalueAB(asp, asp.transition(currState,action),ptm, board, alpha, beta, cutoff-1, heuristic)[0] 
            #if I find a greater value than I have currently, update my alpha
            if v2 > v:
                v = v2
                move = action
                #want the max alpha I can get
                alpha = max(alpha,v)
            #check for pruining
            if v >= beta:
                return (v,move)
        #print('max', move)
        return (v,move)

    def minvalueAB(self, asp: GoTProblem, currState: GoTState, ptm, board, alpha: int, beta: int, cutoff: int, heuristic):
        move = None
        #print('cutoff',cutoff)
        if asp.is_terminal_state(currState):
            #evaluate the terminal and index by player
            #print('minAB evaluate state', (asp.evaluate_state(currState)[ptm], move))
            return (asp.evaluate_state(currState)[ptm], move)
        if cutoff == 0:
            #print('min heur', (heuristic(asp,currState), move))
            return (heuristic(asp,currState), move)
        v = inf
        #go through all action states possible
        for action in asp.get_safe_actions(board, currState.player_locs[ptm], ptm):
            #pass my the alpha and beta values from this given node into its children 
            #print('minvalueAB action', action)
            v2 = self.maxvalueAB(asp, asp.transition(currState,action),ptm, board, alpha, beta, cutoff-1, heuristic)[0] 
            #if I find a lesser value than I have currently, update my beta
            if v2 < v:
                v = v2
                move = action
                beta = min(beta,v)
            #check for pruning possibilities
            if v <= alpha:
                return (v,move)
        #print('min', move)
        return (v,move)

    def alpha_beta(self, asp: GoTProblem, currState: GoTState, ptm, board, cutoff_ply, heuristic_func):
        """
        Implement the alpha-beta pruning algorithm on ASPs,
        assuming that the given game is both 2-player and constant-sum.

        Input:
            asp - an AdversarialSearchProblem
        Output:
            an action(an element of asp.get_available_actions(asp.get_start_state()))
        """
            #set my start alpha and betas to then be updated through the recursions
        startalpha = inf*-1
        startbeta = inf
        #print('value, move', self.maxvalueAB(asp, currState, ptm, board, startalpha, startbeta, cutoff_ply, heuristic_func))
        move = self.maxvalueAB(asp, currState, ptm, board, startalpha, startbeta, cutoff_ply, heuristic_func)[1]
        #print('final move', move)
        return move


    def cleanupAT(self):
        self.prev_cell_type = None
        self.last_move = None
        self.ptm = None
        self.perm_cell = None
        self.temp_cell = None
        self.opp_temp_cell = None
        self.prevWWDis = 0
        self.prevWWDisTEMP = 0
        self.prevOpp = 0
        self.templength = 0

    def dist_from_opp(self, opp_loc, ptm_loc):
        dist = 0
        for i in range(len(opp_loc)):
            dist += abs(opp_loc[i] - ptm_loc[i])
        return dist

    def min_dist_to_temp(self, board, ptm_loc, temp):
        locs = self.temp_barrier_locs_from_board(board, temp)
        min_dist = math.inf
        for loc in locs:
            this_dist = self.dist_from_opp(loc, ptm_loc)
            if this_dist < min_dist:
                min_dist = this_dist
        return min_dist

    def temp_barrier_locs_from_board(self, board, temp):
        if self.opp_temp_cell is None:
            return []
        loc_dict = {}
        num_temp = 0
        for r in range(len(board)):
            for c in range(len(board[r])):
                char = board[r][c]
                if char == temp:
                    loc_dict[num_temp] = (r, c)
                    num_temp += 1
        loc_list = []
        for index in range(num_temp):
            loc_list.append(loc_dict[index])
        return loc_list

    def decideAT(self, asp):
        """
        Input: asp, a GoTProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(GoTProblem.get_safe_actions(board, loc, ptm))
        opp_loc = locs[(ptm + 1) % 2]
        if self.ptm is None:
            self.ptm = ptm
            self.perm_cell = CellType.TWO_PERM
            self.temp_cell = CellType.TWO_TEMP
            self.opp_temp_cell = CellType.ONE_TEMP
            if ptm == 0:
                self.perm_cell = CellType.ONE_PERM
                self.temp_cell = CellType.ONE_TEMP
                self.opp_temp_cell = CellType.TWO_TEMP

        if not possibilities:
            return "U"

        if self.prev_cell_type is None:
            "Attack bot starting"
            self.prev_cell_type = self.temp_cell
            this_move = possibilities[0]
            self.last_move = this_move
            return this_move

        # if player needs to return to perm area
        must_return_to_perm = False
        if self.prev_cell_type == self.temp_cell:
            this_move = None
            if self.last_move == "U":
                this_move = "D"
            elif self.last_move == "D":
                this_move = "U"
            elif self.last_move == "R":
                this_move = "L"
            elif self.last_move == "L":
                this_move = "R"
            else:
                raise Exception

            self.prev_cell_type = self.perm_cell
            self.last_move = this_move
            must_return_to_perm = True

        # else, player is (potentially) leaving perm area
        min_dist = math.inf
        min_dist_to_temp = math.inf
        go_for_temp = False
        decision = possibilities[0]
        min_next_loc = [None] * 2
        for move in possibilities:
            next_loc = GoTProblem.move(loc, move)
            dist_from_opponent = self.dist_from_opp(next_loc, opp_loc)
            this_dist_to_temp = self.min_dist_to_temp(board, next_loc)
            if this_dist_to_temp == 0:
                return move

            if not must_return_to_perm:
                # If we are close to temp barrier
                if this_dist_to_temp <= 5 or go_for_temp:
                    go_for_temp = True
                    if this_dist_to_temp < min_dist_to_temp:
                        min_dist_to_temp = this_dist_to_temp
                        decision = move
                        min_next_loc = next_loc

                elif dist_from_opponent < min_dist:
                    min_dist = dist_from_opponent
                    decision = move
                    min_next_loc = next_loc
                    min_dist_to_temp = this_dist_to_temp

                elif dist_from_opponent == min_dist:
                    if this_dist_to_temp < min_dist_to_temp:
                        min_dist_to_temp = this_dist_to_temp
                        decision = move
                        min_next_loc = next_loc

        if not must_return_to_perm:
            if board[min_next_loc[0]][min_next_loc[1]] == self.perm_cell:
                self.prev_cell_type = self.perm_cell
            else:
                self.prev_cell_type = self.temp_cell
            self.last_move = decision
        return self.last_move


    def decide(self, asp):
        """
        Input: asp, a GoTProblem
        Output: A direction in {'U','D','L','R'}
        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        ww_locs = state.ww_locs

        #print(state)
        #possibilities = list(GoTProblem.get_safe_actions(board, loc, ptm))
        #if possibilities:
         #   return random.choice(possibilities)
        #print('return', self.alpha_beta(asp,  state, ptm, board, 2 ,self.heuristic))
        if len(ww_locs) == 0:
             return self.alpha_beta(asp,state,ptm, board, 2 , self.heuristicNoWW)
        return self.alpha_beta(asp,state,ptm, board, 4, self.heuristic)
        

    def cleanup(self):
        """
        Input: None
        Output: None
        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        pass


class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a GoTProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(GoTProblem.get_safe_actions(board, loc, ptm))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        pass


class ManualBot:
    """Bot which can be manually controlled using W, A, S, D"""

    def decide(self, asp: GoTProblem):
        # maps keyboard input to {U, D, L, R}
        dir_map = {'A': 'L', 'W': 'U', 
                   'a': 'L', 'w': 'U', 
                   'S': 'D', 'D': 'R', 
                   's': 'D', 'd': 'R'}
        # Command for mac/unix:
        direction = getch.getch()
        # Command for Windows:
        # direction = msvcrt.getch().decode('ASCII')
        return dir_map[direction]

    def cleanup(self):
        pass

class AttackBot:
    """Aggressive bot which attacks opposing player when possible"""

    def __init__(self):
        self.prev_cell_type = None
        self.last_move = None
        self.ptm = None
        self.perm_cell = None
        self.temp_cell = None
        self.opp_temp_cell = None

    def cleanup(self):
        self.prev_cell_type = None
        self.last_move = None
        self.ptm = None
        self.perm_cell = None
        self.temp_cell = None
        self.opp_temp_cell = None

    def dist_from_opp(self, opp_loc, ptm_loc):
        dist = 0
        for i in range(len(opp_loc)):
            dist += abs(opp_loc[i] - ptm_loc[i])
        return dist

    def min_dist_to_temp(self, board, ptm_loc):
        locs = self.temp_barrier_locs_from_board(board)
        min_dist = math.inf
        for loc in locs:
            this_dist = self.dist_from_opp(loc, ptm_loc)
            if this_dist < min_dist:
                min_dist = this_dist
        return min_dist

    def temp_barrier_locs_from_board(self, board):
        if self.opp_temp_cell is None:
            return []
        loc_dict = {}
        num_temp = 0
        for r in range(len(board)):
            for c in range(len(board[r])):
                char = board[r][c]
                if char == self.opp_temp_cell:
                    loc_dict[num_temp] = (r, c)
                    num_temp += 1
        loc_list = []
        for index in range(num_temp):
            loc_list.append(loc_dict[index])
        return loc_list

    def decide(self, asp):
        """
        Input: asp, a GoTProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(GoTProblem.get_safe_actions(board, loc, ptm))
        opp_loc = locs[(ptm + 1) % 2]
        if self.ptm is None:
            self.ptm = ptm
            self.perm_cell = CellType.TWO_PERM
            self.temp_cell = CellType.TWO_TEMP
            self.opp_temp_cell = CellType.ONE_TEMP
            if ptm == 0:
                self.perm_cell = CellType.ONE_PERM
                self.temp_cell = CellType.ONE_TEMP
                self.opp_temp_cell = CellType.TWO_TEMP

        if not possibilities:
            return "U"

        if self.prev_cell_type is None:
            "Attack bot starting"
            self.prev_cell_type = self.temp_cell
            this_move = possibilities[0]
            self.last_move = this_move
            return this_move

        # if player needs to return to perm area
        must_return_to_perm = False
        if self.prev_cell_type == self.temp_cell:
            this_move = None
            if self.last_move == "U":
                this_move = "D"
            elif self.last_move == "D":
                this_move = "U"
            elif self.last_move == "R":
                this_move = "L"
            elif self.last_move == "L":
                this_move = "R"
            else:
                raise Exception

            self.prev_cell_type = self.perm_cell
            self.last_move = this_move
            must_return_to_perm = True

        # else, player is (potentially) leaving perm area
        min_dist = math.inf
        min_dist_to_temp = math.inf
        go_for_temp = False
        decision = possibilities[0]
        min_next_loc = [None] * 2
        for move in possibilities:
            next_loc = GoTProblem.move(loc, move)
            dist_from_opponent = self.dist_from_opp(next_loc, opp_loc)
            this_dist_to_temp = self.min_dist_to_temp(board, next_loc)
            if this_dist_to_temp == 0:
                return move

            if not must_return_to_perm:
                # If we are close to temp barrier
                if this_dist_to_temp <= 5 or go_for_temp:
                    go_for_temp = True
                    if this_dist_to_temp < min_dist_to_temp:
                        min_dist_to_temp = this_dist_to_temp
                        decision = move
                        min_next_loc = next_loc

                elif dist_from_opponent < min_dist:
                    min_dist = dist_from_opponent
                    decision = move
                    min_next_loc = next_loc
                    min_dist_to_temp = this_dist_to_temp

                elif dist_from_opponent == min_dist:
                    if this_dist_to_temp < min_dist_to_temp:
                        min_dist_to_temp = this_dist_to_temp
                        decision = move
                        min_next_loc = next_loc

        if not must_return_to_perm:
            if board[min_next_loc[0]][min_next_loc[1]] == self.perm_cell:
                self.prev_cell_type = self.perm_cell
            else:
                self.prev_cell_type = self.temp_cell
            self.last_move = decision
        return self.last_move


class SafeBot:
    """Bot that plays safe and takes area"""

    def __init__(self):
        self.prev_move = None
        self.to_empty = []
        self.algo_path = []
        self.path = []
        self.calc_empty = False
        self.order = {"U": ("L", "R"), 
                    "D": ("L", "R"), 
                    "L": ("U", "D"),
                    "R": ("U", "D")}

    def cleanup(self): 
        self.prev_move = None
        self.to_empty = []
        self.algo_path = []
        self.path = []
        self.calc_empty = False
        self.order = {"U": ("L", "R"), 
                    "D": ("L", "R"), 
                    "L": ("U", "D"),
                    "R": ("U", "D")}
    
    def get_safe_neighbors_wall(self, board, loc):
        neighbors = [
                ((loc[0] + 1, loc[1]), D),
                ((loc[0] - 1, loc[1]), U),
                ((loc[0], loc[1] + 1), R),
                ((loc[0], loc[1] - 1), L),
            ]
        return list(filter(lambda m: board[m[0][0]][m[0][1]] != CellType.WALL, neighbors))

    def get_safe_neighbors_no_wall(self, board, loc, wall):
        neighbors = [
                ((loc[0] + 1, loc[1]), D),
                ((loc[0] - 1, loc[1]), U),
                ((loc[0], loc[1] + 1), R),
                ((loc[0], loc[1] - 1), L),
            ]
        return list(filter(lambda m: board[m[0][0]][m[0][1]] != CellType.WALL and board[m[0][0]][m[0][1]] != wall, neighbors))

    def decide(self, asp: GoTProblem):
        state = asp.get_start_state()
        if not self.path:
            if self.calc_empty:
                self.gen_path_to_empty(state)
                self.path += self.to_empty
                self.to_empty = []
                self.calc_empty = False
            else:
                self.gen_space_grab(state)
                self.path += self.algo_path
                self.algo_path = []
                self.calc_empty = True
        move = self.path.pop(0)
        self.prev_move = move
        return move  
        
    def gen_space_grab(self, state : GoTState):
        board = state.board
        loc = state.player_locs[state.ptm]
        if state.ptm == 0:
            player_wall = CellType.ONE_PERM
        else:
            player_wall = CellType.TWO_PERM
        avail_actions = {U, D, L, R}
        prev = self.prev_move
        if prev:
            avail_actions.remove(prev)
        else:
            safe_actions = self.get_safe_neighbors_wall(board, loc)
            random.shuffle(safe_actions)
            loc, move = safe_actions[0]
            self.algo_path.append(move)
            avail_actions.remove(move)
            prev = move
        while avail_actions:
            safe_moves = self.get_safe_neighbors_no_wall(board, loc, player_wall)
            safe_moves_wall = self.get_safe_neighbors_wall(board,loc)
            if not safe_moves and not safe_moves_wall:
                self.algo_path.append(U)
                return
            random.shuffle(safe_moves)
            random.shuffle(safe_moves_wall)
            use_wall = True
            for loc, move in safe_moves:
                board_val = board[loc[0]][loc[1]]
                if move in self.order[prev] and move in avail_actions and board_val != player_wall:
                    self.algo_path.append(move)
                    avail_actions.remove(move)
                    prev = move
                    use_wall = False
                    break
            if use_wall:
               for loc, move in safe_moves_wall:
                    board_val = board[loc[0]][loc[1]]
                    if move in self.order[prev] and move in avail_actions:
                        self.algo_path.append(move)
                        avail_actions.remove(move)
                        prev = move
                        use_wall = False
                        break 
        return

    def gen_path_to_empty(self, state: GoTState):
        board = state.board
        player_loc = state.player_locs[state.ptm]
        to_check = [(player_loc, None)]
        checked = {(player_loc, None): None}
        while to_check:
            loc, m = to_check.pop(0)
            neighbors = [
                ((loc[0] + 1, loc[1]), D),
                ((loc[0] - 1, loc[1]), U),
                ((loc[0], loc[1] + 1), R),
                ((loc[0], loc[1] - 1), L),
            ]
            random.shuffle(neighbors)
            for move in neighbors:
                x, y = move[0][0], move[0][1]
                board_val = board[x][y]
                if move not in checked and board_val != CellType.WALL:
                    checked[move] = (loc, m)
                    if board_val == ' ':
                        path = []
                        while move[1] is not None:
                            path.append(move[1])
                            move = checked[move]
                        self.to_empty += path
                        return
                    else:
                        to_check.append(move)
        self.to_empty += [U]
        return
