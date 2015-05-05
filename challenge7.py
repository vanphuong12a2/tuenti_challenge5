import sys
from sets import Set

def get_friends(girl):
   """Find all friends of the girl through chains"""
   fchain = Set([])
   for chain in chains:
      if girl in chain:
         fchain |= chain.copy()
   fchain.discard(girl)
   return fchain

def get_friends_of_friends(girl):
   """Find all friends of friends of the girl through chains"""
   fchain = get_friends(girl)
   ffchain = Set([])
   for friend in fchain:
      ffchain |= get_friends(friend)
   ffchain.discard(girl)
   return ffchain - fchain

def get_chain_groups(chains):
   """Groups all the chains, every 2 chains that have a common girl will be merge until they are all separated"""
   groups = list()
   for chain in chains:
      add = False
      for group in groups:
         if len(chain & group) > 0:
            group |= chain.copy()
            add = True
      if not add:
         groups.append(chain.copy())
   if len(groups) == len(chains):
      return groups
   else: 
      return get_chain_groups(groups)

if __name__=="__main__":
   """ Solution for challenge 7 - Larry perfect matching """
 
   # Read M, N
   M, N = map(int, sys.stdin.readline().split())

   # Set up a list of girls and their answers
   girls = list()
   scores = {}
   for _ in range(M):
      girl = sys.stdin.readline().split()
      girls.append(girl)
      scores[girl[0]] = 0  
    
   # List of friend chains
   chains = list()
   for _ in range(N):
      chains.append(Set(sys.stdin.readline().split()))

   # Groups of acquantains, every one in a group connects to each other in some way
   groups = get_chain_groups(chains)
   
   # List of girls who like cats
   like_cats = Set([girl[0] for girl in girls if girl[4]=='Y'])

   # List of girls who had 4 point due to the fact that they have a friend who loves cats and that friend has no one
   add4s = Set([])

   # For each question, the answer of the girl will affect her score or others.
   # A gril has a friend say yes for a ques === if a girl say yes, every friend of her will has the score
   for girl in girls:
      gname = girl[0]
      if girl[1] == 'Y':
         scores[gname] += 7
      if girl[2] == 'Y': 
         for friend in get_friends(gname):
            scores[friend] += 3
      if girl[3] == 'Y':
         for ffriend in get_friends_of_friends(gname):
            scores[ffriend] += 6
      if girl[4] == 'Y':
         friends = get_friends(gname)
         f_like_cats = get_friends(gname) & like_cats
         if len(f_like_cats) == 0:
            add4s |= friends.copy()
         if len(f_like_cats) == 1:
            add4s |= f_like_cats.copy()
      if girl[5] == 'Y':
         connections = Set([])
         for group in groups:
            if gname in group:
               connections |= group.copy()
               break
         for friend in girls:
            if friend[0] != gname and friend[0] not in connections:
               scores[friend[0]] += 5
         
   # Add score +4
   for girl in girls:
      if girl[0] in add4s:
         scores[girl[0]] += 4

   print max(scores.values())
            
