import pygame
import random
from pygame import mixer
from pygame.locals import *
import sys



#Intialization
FPS=60
pygame.init()
screen= pygame.display.set_mode((1170,650))

#Game Icon
pygame.display.set_caption("Chase game")
game_icon = pygame.image.load("Assests/icon.png")
pygame.display.set_icon(game_icon)

#Assets
background_start = pygame.image.load("Assests/background_start.png")
background = pygame.image.load("Assests/background.jpg")
Start_image = pygame.image.load("Assests/pixel.png")
chaser1_image =  pygame.image.load("Assests/dchaser.png")
chaser2_image = pygame.image.load("Assests/rchaser.png")
barrier_image = pygame.image.load("Assests/barrier.png")
objective_image = pygame.image.load("Assests/objective.png")
user_image = pygame.image.load("Assests/user.png")
teleporter_image = pygame.image.load("Assests/teleporter.png")
teleporter_image = pygame.transform.scale(teleporter_image, (50, 50))
user_image = pygame.transform.scale(user_image, (75,75))
chaser1_image = pygame.transform.scale(chaser1_image, (75,75))
objective_image = pygame.transform.scale(objective_image, (75,75))
barrier_image= pygame.transform.scale(barrier_image, (75, 75))
Start_image = pygame.transform.scale(Start_image, (75, 75))
chaser2_image = pygame.transform.scale(chaser2_image, (75,75))

# Text
font_style = pygame.font.Font("freesansbold.ttf", 50)
font_style2 = pygame.font.Font("freesansbold.ttf", 80)
font_style3 = pygame.font.Font("freesansbold.ttf", 20)

#Sound
move = mixer.Sound("Assests/jump.wav")
objective = mixer.Sound("Assests/goal.wav")
end = mixer.Sound("Assests/caught.wav")

#Helper Functions of data structures
def intialize_graph(nodes): #graph helper function
  G={}
  for i in nodes:
    G[i]=[]
  return(G)

def intialize_edge(graph, src, dest, dir, wt): #graph helper function
    new_edge = (dest, dir, wt)
    if src in graph:
        graph[src].append(new_edge)
    else:
        graph[src] = [new_edge]
    return(graph)

def addedges(G, edges): #graph helper function
  for i in edges:
    G = intialize_edge(G, i[0], i[1], i[2], i[3])
  return(G)

def getoutneighbours(G,node): #graph helper function
    lst = []
    edges = G[node]
    for i in edges:
        lst.append(i[0])
    return(lst)

def weight(graph, source, target): #graph helper function for intializing weights
  edges = graph[source]
  for i in edges:
    if i[0] == target:
      x = int(i[2])
      return(x)
  return(None) 

def shortest_path(graph, source, dest): #pathfinding calculations
  parents, node_cost = Dijkstra(graph, source, dest)
  path = []
  node = dest 
  while parents[node] != None:
    path.append(parents[node])
    node = parents[node]
  path.reverse()
  if len(path) == 1:
    return(dest)
  elif len(path) == 0:
    return(source)
  else:
    return(path[1])

def Dijkstra(graph, source, dest): #pathfinding
  prior_que = []
  visited = {} 
  node = {} 
  cost = {} 
  for i in graph:
    visited[i] = False 
    node[i] = None
    if i == source:
      cost[i] = 0
      prior_que.append((0, i))
    else:
      cost[i] = float("inf")
  while len(prior_que) != 0:
    cnode = deque(prior_que)
    visited[cnode] = True
    val = getoutneighbours(graph, cnode)
    for j in val:
      if visited[j] == False:
        ncost = cost[cnode] + weight(graph, cnode, j)
        if cost[j] > ncost:
          node[j] = cnode
          cost[j] = ncost
          prior_que = enque(prior_que, (ncost, j))
      if j == dest:
        break
    if j == dest:
      break
  return(node, cost)

def deque(lst): #queue helper function
  val = lst[0]
  lst.remove(lst[0])
  return(val[1])

def enque(lst, val): #queue helper function
    lst.append(val)
    lst.sort(key=lambda x: x[0])
    return(lst)

#File data access
def adjac_matrix(fileName): #this takes an input from a txt of an adjanency matrix and maps out a graph and its edges 
  lst= []
  filename = open(fileName, "r")
  val = int(filename.readline())
  for i in range(0, val):
    lst.append(filename.readline().split())
  return(lst)

def possible_map(file_name): #this takes input from the location txt and established which locations are traverable or not
    dict = {}
    with open(file_name, "r") as file:
        val = int(file.readline())
        for _ in range(val):
            coord = file.readline().split()
            dict[coord[0]] = (coord[1], coord[2])
    return(dict)

def instialize_graph_data(file_name): #according to the inputs intializes the graph
    edgelst = []
    nodelst = []
    with open(file_name, "r") as file:
        val = int(file.readline())
        for _ in range(val):
            lst = file.readline().split()
            if lst[2] == "Right":
                edgelst.append((lst[0], lst[1], lst[2], lst[3]))
                edgelst.append((lst[1], lst[0], "Left", lst[3]))
            else:
                edgelst.append((lst[0], lst[1], lst[2], lst[3]))
                edgelst.append((lst[1], lst[0], "Up", lst[3]))
            if not (lst[0] in nodelst):
                nodelst.append(lst[0])
            if not (lst[1] in nodelst):
                nodelst.append(lst[1])
    return(addedges(intialize_graph(nodelst), edgelst))

#Files
adj_matrix = adjac_matrix("Assests/pixel_grid.txt")
map = instialize_graph_data("Assests/map.txt")
map_coords = possible_map("Assests/location.txt")

#Game Starting
def display_image_and_text():
    screen.blit(background_start, (1170 // 2 - background_start.get_width() // 2, 650 // 2 - background_start.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)


#Game mapping 
def Game_Over():  #displays game over text when you get caught
  screen.blit(font_style2.render("GAME OVER", True,(255,64,64)),(500,400))

def show_you_won():
    text = font_style2.render("You won!", True, (0, 255, 0))
    text_rect = text.get_rect()
    text_rect.center = (1170 // 2, 650 // 2)
    screen.fill((255,255,255))
    screen.blit(text, text_rect)
    pygame.display.update()

def score_display(val):#displays score
    screen.fill((0, 0, 0) , pygame.Rect(0, 0, 1170, 50))
    screen.blit(font_style.render("Score : " + str(Score), True, (255, 48, 48)), (500, 0))
    screen.blit(font_style.render("Level " +str(val), True, (255, 255, 255)), (900, 0))

def high_score(): #reads the highscore file to display it
   with open("highest score.txt","r") as file:
      return(file.read())

def render_map(grid, user_pos, chaser1_pos, chaser2_pos, objective_pos, map_coords): #renders the entire map
    x_offset = 50
    y_offset = 50
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            current_coordinates = (str(i), str(j))
            image_position = (x_offset + 50 * j, y_offset)
            if current_coordinates == map_coords[user_pos]:
                screen.blit(user_image, image_position)#shows current position
            elif current_coordinates == map_coords[chaser1_pos]:
                screen.blit(chaser1_image, image_position)#shows djisktra chaser
            elif current_coordinates == map_coords[chaser2_pos]:
                screen.blit(chaser2_image, image_position)#shows random chaser
            elif current_coordinates == map_coords[objective_pos]:
                screen.blit(objective_image, image_position)#shows objective
            elif grid[i][j] == "1":
                barrier_x_offset = x_offset + 10 * (i % 2)#establishes barrier
                image_position = (barrier_x_offset + 50 * j, y_offset)
                screen.blit(barrier_image, image_position)
            else:
                screen.blit(Start_image, image_position)
            if current_coordinates == map_coords["93"]:
                screen.blit(teleporter_image, image_position)#shows teleporter
        y_offset += 60
        x_offset = 50

# Coordinates
def location(map): #established current coords
  user_pos = str(random.randint(1,len(map))) # user position
  chaser1_pos = str(bot_pos(user_pos, map)) # djisktra chaser
  chaser_pos = str(bot_pos(user_pos, map)) # random chaser
  objective_pos = str(bot_pos(user_pos, map)) # objective chaser
  return(user_pos, chaser1_pos, objective_pos, chaser_pos)

def bot_pos(user_pos, map): # chaser1 caught coords
  ans = random.randint(1,len(map))
  while ans == user_pos :
      ans = random.randint(1,36)
  return(ans)

def new_bot_pos(cpu_loc, map): # chaser2 caught coords
    lst = []
    available_loc = map[cpu_loc]
    for i in available_loc:
      lst.append(i[0])
    ans = random.choice(lst)
    return(ans)


#Game Running
game_run = True #game run flag
Score = 0 #score intialized
user_pos, chaser1_pos, objective_pos, chaser2_pos = location(map) #starting location of game

display_image_and_text()
screen.blit(background, (0,0,1200,650))

render_map(adj_matrix, user_pos, chaser1_pos, chaser2_pos, objective_pos, map_coords) #renders the map

score_display(val=1)
pygame.display.update()
clock = pygame.time.Clock()
highscore = int(high_score())

while game_run==True: #game 
    clock.tick(FPS)
    key_event = pygame.key.get_pressed()
    user_move = False 
    if Score > highscore: #condition for updating highscore
        highscore = Score
        with open("highest score.txt", "w") as f:
            f.write(str(highscore))
    while user_move == False:  #barrier movement block
        avail_loc = map[user_pos]
        options = []
        for i in avail_loc:
            options.append(i[1])
        key_event = pygame.key.get_pressed()
        for i in pygame.event.get(): #keybinds for movements
           if i.type == pygame.QUIT:
            user_move = True 
            game_run = False
           if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT or i.key == pygame.K_a:
              move.play()
              if ("Left" in options) == True:
                    for j in avail_loc:
                        if j[1] == "Left":
                          user_pos = j[0]
                          user_move = True
            if i.key == pygame.K_RIGHT or i.key ==pygame.K_d:
              move.play()
              if ("Right" in options) == True:
                    for j in avail_loc:
                        if j[1] == "Right":
                          user_pos = j[0]
                          user_move = True
            if i.key == pygame.K_UP or i.key ==pygame.K_w:
              move.play()
              if ("Up" in options) == True:
                    for j in avail_loc:
                        if j[1] == "Up":
                          user_pos = j[0]
                          user_move = True
            if i.key == pygame.K_DOWN or i.key == pygame.K_s:
              move.play()
              if ("Down" in options) == True:
                    for j in avail_loc:
                        if j[1] == "Down":
                          user_pos = j[0]
                          user_move = True 
    if user_pos == objective_pos:
        objective.play()
        Score = Score + 100
        objective_pos = str(bot_pos(user_pos, map))
        screen.blit(background, (0,0))
        val = 1
        if Score >= 300:
            end.play()
            val = 2
            background = pygame.image.load("Assests/background1.jpg")
            Start_image = pygame.image.load("Assests/pixel1.png")
            chaser1_image =  pygame.image.load("Assests/dchaser1.png")
            chaser2_image = pygame.image.load("Assests/rchaser1.png")
            barrier_image = pygame.image.load("Assests/barrier1.png")
            objective_image = pygame.image.load("Assests/objective1.png")
            user_image = pygame.image.load("Assests/user1.png")
            teleporter_image = pygame.image.load("Assests/teleporter1.png")
            teleporter_image = pygame.transform.scale(teleporter_image, (50, 50))
            user_image = pygame.transform.scale(user_image, (75,75))
            chaser1_image = pygame.transform.scale(chaser1_image, (75,75))
            objective_image = pygame.transform.scale(objective_image, (75,75))
            barrier_image= pygame.transform.scale(barrier_image, (75, 75))
            Start_image = pygame.transform.scale(Start_image, (75, 75))
            chaser2_image = pygame.transform.scale(chaser2_image, (75,75))
            screen.blit(background, (0,0,1200,650))
        if Score >= 600:
            end.play()
            val = 3
            background = pygame.image.load("Assests/background2.jpg")
            Start_image = pygame.image.load("Assests/pixel2.png")
            chaser1_image =  pygame.image.load("Assests/dchaser2.png")
            chaser2_image = pygame.image.load("Assests/rchaser2.png")
            barrier_image = pygame.image.load("Assests/barrier2.png")
            objective_image = pygame.image.load("Assests/objective2.png")
            user_image = pygame.image.load("Assests/user2.png")
            teleporter_image = pygame.image.load("Assests/teleporter2.png")
            teleporter_image = pygame.transform.scale(teleporter_image, (50, 50))
            user_image = pygame.transform.scale(user_image, (75,75))
            chaser1_image = pygame.transform.scale(chaser1_image, (75,75))
            objective_image = pygame.transform.scale(objective_image, (75,75))
            barrier_image= pygame.transform.scale(barrier_image, (75, 75))
            Start_image = pygame.transform.scale(Start_image, (75, 75))
            chaser2_image = pygame.transform.scale(chaser2_image, (75,75))
            screen.blit(background, (0,0,1200,650))
        score_display(val)
        if Score > 1000:
            show_you_won()
            pygame.display.update()
            pygame.time.delay(500)
            break
    if user_pos == "93": #teleporter condition
        user_pos = str(bot_pos(user_pos, map))




    chaser1_pos = new_bot_pos(chaser1_pos, map)
    chaser2_pos = shortest_path(map, chaser2_pos, user_pos)
    render_map(adj_matrix, user_pos, chaser1_pos, chaser2_pos, objective_pos, map_coords)

    #High Score display
    high_score_display = font_style3.render("High Score: " + str(highscore), True, (240, 248, 255)) 
    screen.blit(high_score_display, (10, 0))
    pygame.display.update()


    #Game end 
    if (user_pos == chaser1_pos) or (user_pos == chaser2_pos):
        Game_Over()
        pygame.display.update()
        pygame.time.delay(500)
        break

pygame.quit()
sys.exit()