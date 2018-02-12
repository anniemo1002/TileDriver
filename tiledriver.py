# Name: Jiaqing Mo
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  #1
# Term:     Winter 2018

import math
import queue
import copy


class Node:
   def __init__(self, state, distance, step):
      self.state = state
      self.distance = distance
      self.step = step

   def __eq__(self, other):
      return self.state == other.state and \
            len(self.step) == len(other.step)
   def __ne__(self, other):
      return not (self.state == other.state and \
            len(self.step) == len(other.step))
   def __lt__(self, other):
      return (self.distance + len(self.step)) \
            < (other.distance + len(other.step))
      
   def __hash__(self):
      return hash((tuple(self.state), tuple(self.step)))




def solve_puzzle(tiles):
   sidelen = int(math.sqrt(len(tiles)))
   explored = set()
   frontiers = set()
   q = queue.PriorityQueue()
   dist = manhattan_dist(tiles, sidelen)
   n = Node(tiles, dist, [])
   if dist != 0:
      q.put(n)
      frontiers.add(n)
      return solve(explored, frontiers, q, sidelen)
   else:
      return ""
   

def manhattan_dist(state, sidelen): #calculate distance of a list
   dist = 0
   for i in range(sidelen ** 2):
      des = state[i]
      if des == 0:
         continue
      pos = i
      pos_lev = pos // sidelen
      des_lev = des // sidelen
      if (des_lev != pos_lev):
         dist += abs(pos_lev - des_lev)
         pos = (des_lev - pos_lev) * sidelen + pos
      if (des != pos):
         dist += abs(des - pos)
   return dist


def solve(explored, frontiers, q, sidelen):
   while not q.empty():
      n = q.get()
      frontiers.remove(n)
      if tuple(n.state) in explored:
         continue
      new_nodes = []
      new_nodes.append(move_up(n, sidelen))
      new_nodes.append(move_down(n, sidelen))
      new_nodes.append(move_left(n, sidelen))
      new_nodes.append(move_right(n, sidelen))
      for node in new_nodes:
         if node is None:
            continue
         if (tuple(node.state) not in explored) and (node not in frontiers):
            if node.distance == 0:
               return node.step
            frontiers.add(node)
            q.put(node)
      explored.add(tuple(n.state))
   return "h"


def move_up(node, sidelen):
   pos = node.state.index(0)
   if (pos // sidelen) != 0 and (len(node.step) == 0 or node.step[-1] != 'K'):
      n1 = copy.deepcopy(node)
      n1.state[pos] = n1.state[pos - sidelen]
      n1.state[pos - sidelen] = 0
      n1.distance += new_lev_dist(n1.state[pos], pos - sidelen, pos, sidelen)
      n1.step.append('J')
      return n1


def move_down(node, sidelen):
   pos = node.state.index(0)
   if (pos // sidelen) != sidelen - 1 and \
         (len(node.step) == 0 or node.step[-1] != 'J'):
      n2 = copy.deepcopy(node)
      n2.state[pos] = n2.state[pos + sidelen]
      n2.state[pos + sidelen] = 0
      n2.distance += new_lev_dist(n2.state[pos], pos + sidelen, pos, sidelen)
      n2.step.append('K')
      return n2




def move_left(node, sidelen):
   pos = node.state.index(0)
   if (pos % sidelen) != 0 and (len(node.step) == 0 or node.step[-1] != 'H'):
      n1 = copy.deepcopy(node)
      n1.state[pos] = n1.state[pos - 1]
      n1.state[pos - 1] = 0
      n1.distance += new_side_dist(n1.state[pos], pos - 1, pos, sidelen)
      n1.step.append('L')
      return n1


def move_right(node, sidelen):
   pos = node.state.index(0)
   if (pos % sidelen) != sidelen - 1 and \
         (len(node.step) == 0 or node.step[-1] != 'L'):
      n1 = copy.deepcopy(node)
      n1.state[pos] = n1.state[pos + 1]
      n1.state[pos + 1] = 0
      n1.distance += new_side_dist(n1.state[pos], pos + 1, pos, sidelen)
      n1.step.append('H')
      return n1


def new_side_dist(num, orig, new, sidelen):
   dest_pos = num % sidelen
   orig_pos = orig % sidelen
   new_pos = new % sidelen
   if (abs(orig_pos - dest_pos) > abs(new_pos - dest_pos)):
      return -1  #closer to destination
   else:
      return 1


def new_lev_dist(num, orig, new, sidelen):
   dest_lev = num // sidelen
   orig_lev = orig // sidelen
   new_lev = new // sidelen
   if (abs(orig_lev - dest_lev) > abs(new_lev - dest_lev)):
      return -1
   else:
      return 1




