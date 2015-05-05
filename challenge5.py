import sys
final_island = 'Raftel'

def path_update(path, node, new_gold):
   """ Update path when explore a new node"""
   new_path = path[0][:]
   if node:
      new_path.append(node)   
   if new_gold < 0:
      new_gold = 0
   paths.append((new_path, new_gold))
   
def others_move():
   """ Move others ship, return True if anyone reaches final island""" 
   # Move ship by ship, except the 1st one (our ship)
   for ship in ships[1:]:
      avail_routes = [route for route in routes if route[0] == ships_dict[ship[1]]]
      if ship[0]%2 == 0:
         desire_cost = max([route[2] for route in avail_routes if route[0] == ships_dict[ship[1]]])
      else:
         desire_cost = min([route[2] for route in avail_routes if route[0] == ships_dict[ship[1]]]) 
      moving_routes = [route for route in avail_routes if route[2] == desire_cost]
      if len(moving_routes) > 0:
         moving_route = moving_routes[0]
         ships_dict[ship[1]] = moving_route[1]
         if moving_route[1] == final_island:
            return True
         # Collide with our ship
         for path in paths[:]:
            if path[0][-1] != final_island and path[0][-1] == moving_route[1]:
               path_update(path, None, path[1] - ship[2])
               paths.remove(path) 
   return False 
      
def self_move(path):
   """ Move our ship first"""
   ship = ships[0]
   for route, route_cost in routes_dict.iteritems():
      # Check route[1] a) others ships (???) b) already in path (done)
      if path[1] != 0 and route[0] == path[0][-1] and route[1] not in path[0]:  #and route[1] not in ships_dict.values():
         new_gold = path[1] - route_cost - islands[route[1]]
         path_update(path, route[1], new_gold)
   # Option to pillage 
   path_update(path, path[0][-1], path[1]+10)
   paths.remove(path)     

def move():
   """ Main move, starts with our ship then others, call it again recursively"""
   # Stop looping when every remain paths reach final
   if not all([path[0][-1] == final_island for path in paths]):
      org_paths = paths[:]
      for path in org_paths:
         if path[0][-1] != final_island:
            self_move(path)
      reach_final = others_move()
      # When others reach final before us, remove the paths
      if reach_final:
         for path in paths[:]:
            if path not in org_paths and path[0][-1] != final_island:
               paths.remove(path)
      else:
         move()
      
if __name__=="__main__":
   """ Solution for challenge 5 """
   
   # Read N
   no_islands = int(sys.stdin.readline())
   islands = {}
   # Get the islands' information
   for _ in range(no_islands):
      node_name, node_cost = sys.stdin.readline().split()
      islands[node_name] = int(node_cost)
   
   #Read R
   no_routes = int(sys.stdin.readline())
   routes = list()
   routes_dict = {}
   # Get the routes' information
   for _ in range(no_routes):
      node_name1, node_name2, route_cost = sys.stdin.readline().split()
      routes.append((node_name1, node_name2, int(route_cost)))
      routes_dict[(node_name1, node_name2)] = int(route_cost)
      
   # Read S
   no_ships = int(sys.stdin.readline())  
   ships = list()
   ships_dict = {}
   # Get the ships' information
   for _ in range(no_ships):
      ship_no, ship_name, ship_gold, start_island = sys.stdin.readline().split()
      ships.append((int(ship_no), ship_name, int(ship_gold), start_island))
      ships_dict[ship_name] = start_island
   
   # Initialize the start of paths
   paths = [([ships[0][3]], ships[0][2])]
   
   # Start the moving
   move()

   # Display the result      
   print max([path[1] for path in paths])
      

