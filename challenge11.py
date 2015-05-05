import sys
import math
 
 
def nCr(n,r):
   """ Calculate nCr """
   f = math.factorial
   return f(n) / f(r) / f(n-r)
     
def get_no_to_kill(need, have):
   """ Minus function, return 0 if negative """
   if have >= need:
      return 0
   return need - have
    
def explore_room(room_name, stamina, factor):
   """ Support function for exploring a room
   factor: combinations of no of killed minions / all minions of a room
   """

   if stamina < room_min_staminas[room_name][0]:
      return 0

   # If the room was explored before
   save = True
   if room_min_staminas[room_name][1]:
      min_nos = [room[1] for room in room_no_sets if room[0] == room_name and room_no_sets[room] != None]
      if len(min_nos) > 0:
         if stamina > min(min_nos):
            return room_no_sets[(room_name, min(min_nos))] * factor
         save = False
   else:
      if (room_name, stamina) in room_no_sets and room_no_sets[(room_name, stamina)]:
         return room_no_sets[(room_name, stamina)] * factor

   no_sets = 0
   doors = rooms[room_name]

   # Loop though all the door
   for door in doors:
      if init_stamina >= door[2] and door[1] <= len(doors):
         # Count minions who is killed for keys
         no_to_kill = door[1] + get_no_to_kill(door[2], stamina + door[1])
          
         if len(doors) >= no_to_kill:
            stamina += no_to_kill
            # When enough keys and stamia, check the door
            # Exit door => increase no_sets by a factor (combinations of no of killed minion (except the default door))
            # Other door => continue to explore
            if stamina >= door[2]:
               if stamina > init_stamina:
                  stamina = init_stamina 
                           
               if no_to_kill != 0:
                  no_to_kill -= 1
               door_factor = factor * nCr(len(doors)-1, no_to_kill)
                
               if door[0] == 'exit':
                  no_sets += door_factor
               else:
                  no_sets += explore_room(door[0], stamina - door[2], door_factor)   
                   
   # Save the no of sets for each room, together with start stamina
   if save: room_no_sets[(room_name, stamina)] = no_sets/factor
   return no_sets
       
       
       
if __name__=="__main__":
   """ Solution for challenge 11 - Crazy Tower """
  
   # Read the scenarios file 
   scenarios = list()
   data_file = sys.argv[1]
   with open(data_file) as f:
      no_scenarios = int(f.readline())
      for _ in range(no_scenarios):
         stamina, no_rooms = map(int, f.readline().split())
         rooms = {}
         for _ in range(no_rooms):
            room = f.readline().split()
            room_name, no_doors = room[0], int(room[1])
            doors = list()
            for _ in range(no_doors):
               door = f.readline().split()
               doors.append((door[0], int(door[1]), int(door[2])))
            rooms[room_name] = doors
         scenarios.append((stamina, rooms))
    
   # Read the input file
   scenario_ids = map(int, sys.stdin.readlines())
 
   # Display the result     
   for i in scenario_ids:
      scenario = scenarios[i]
      init_stamina = scenario[0]
      rooms = scenario[1]
      # Store the sets when explore each room => save time
      room_no_sets = {}
      for room in rooms:
         room_no_sets[(room, init_stamina)] = None
       
      # Store the mininum stamina to start a room
      room_min_staminas = {}
      room_min_staminas['exit'] = [0, True]
      for room in rooms:
         room_min_staminas[room] = [None, None]
      while room_min_staminas['start'][0] == None:
         for room in rooms: 
            if room_min_staminas[room][0] == None:
               if sum([1 for door in rooms[room] if room_min_staminas[door[0]][0] == None]) == 0:
                  room_min_staminas[room][0] = min([room_min_staminas[door[0]][0] + get_no_to_kill(door[2], len(rooms[room])) for door in rooms[room]])
                  if room_min_staminas[room][0] > 0:
                     room_min_staminas[room][1] = False
            if room_min_staminas[room][1] == None:
               if sum([1 for door in rooms[room] if room_min_staminas[door[0]][1] == None]) == 0:
                  room_min_staminas[room][1] = (len([door for door in rooms[room] if room_min_staminas[door[0]][1] == False])==0)

      # Initialize the first room to explore is start
      no_sets = explore_room('start', init_stamina, 1)
      print 'Scenario ' + str(i) + ': ' + str(no_sets%1000000007)
            
