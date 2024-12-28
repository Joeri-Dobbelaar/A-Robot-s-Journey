# This is my (Joeri Dobbelaar) submission the final exercise for the Python Programming MOOC 2024 of the University of Helsinki as described in part 14.
# This is a relatively simple game made with pygame
# The exercise was to make a simple game in pygame using only 4 sprites 
#
# In the game the player plays a robot
# In the game the player can:
#       - collect coins
#       - go through doors
#       - talk to other robots (npcs) and fulfill quests for them to make friends
#       - avoid enemies or touch an enemy and lose a life
# The player's goal is to collect as many coins as possible and/or make as many friends as possible
# 
#
#
# If you are reviewing this game for the MOOC, please play it first
# also, it's probably too big. I'm sorry.
# You can expand & collapse classes and functions by clicking the arrow symbol in between the line number and the word 'class' or 'def'

import pygame
from random import randint



# To model objects in the game I have made a bunch of custom classes. NB these classes are not the game itself. (normally I would have stored these in a different file, but I wasn't sure if that was possible for this exercise)
# First there is 'GameObject'. GameObject is an abstract class, meaning there are no actual GameObjects in the game,
# but there are a bunch of classes in the game that inherit from GameObject: Coin, NPC, Bug, Door & Player all inherit from GameObject

# all GameObjects record the name of the level they are present in and their x and y coordinates in that level.
# furthermore they also record their own width and heigth (so I dont have to type image.get_height() a million times.)
# images are not stored in the GameObjects themself
class GameObject:
    def __init__(self, level: str, x: int, y: int, width: int, height: int):
        self.__level = level
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
    # GETTERS
    @property
    def level(self):
        return self.__level
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, x):
        self.__x = x
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, y):
        self.__y = y
    @property
    def width(self):
        return self.__width
    @property
    def height(self):
        return self.__height


# COIN      (doesnt do anything fancy)
# represented by 'coin.png' ingame
class Coin(GameObject):
    def __init__(self, level, x, y, width=40, height=40):
        super().__init__(level, x, y, width, height)


# NPC   (NPC = NON PLAYER CHARACTER)
# represented by 'robot.png' ingame
#
# the player can talk to npcs to do quests
# NPCs start with their quest_stage set to 0
# when players talk to them and interact with the world the npc quest_stage will increase. a quest_stage of 30 is considered the final stage
# depending on their quest_stage, NPCs will display certain messages, which are stored in quest_message, which is a list (and quest_msg_2 for more convuluted quests)
class NPC(GameObject):
    def __init__(self, level: str, x: int, y: int, name: str, quest_id: str, quest_message: list, quest_msg_2: list=[], width: int=50, height: int=86, quest_stage: int=0):
        super().__init__(level, x, y, width, height)
        self.__name = name
        self.__quest_id = quest_id
        self.__quest_message = quest_message
        self.__quest_message_2 = quest_msg_2
        self.__quest_stage = quest_stage
    @property
    def name(self):
        return self.__name
    @property
    def quest_stage(self):
        return self.__quest_stage
    @quest_stage.setter
    def quest_stage(self, q_stage: int):
        self.__quest_stage = q_stage
    @property
    def friend(self):
        return self.__quest_stage == 30
    @property
    def quest_id(self):
        return self.__quest_id
    @property
    def quest_message(self):
        return self.__quest_message
    @property
    def quest_message_2(self):
        return self.__quest_message_2


# Bug
#
# Bugs are enemies in the game touching them will make the player lose a life
# represented by 'monster.png' ingame
# in game Bugs alway move vertically, so they have a variable to know whether they are going up or down
class Bug(GameObject):
    def __init__(self, level, x, y, width: int=50, height: int=70):
        super().__init__(level, x, y, width, height)
        self.__down = True
    @property
    def down(self):
        return self.__down
    @down.setter
    def down(self, down):
        self.__down = down



# DOOR
#
# Doors are used to switch between levels.
# every door has an 'id', which is their own address
# and a 'link', which is the address of the door they are linked to
# represented by 'door.png' ingame
class Door(GameObject):
    def __init__(self, level: str, x: int, y: int, id: str, link: str, width: int=50, height: int=70,):
        super().__init__(level, x, y, width, height)
        self.__id = id
        self.__link = link
    # GETTERS
    @property
    def id(self):
        return self.__id
    @property
    def link(self):
        return self.__link



# PLAYER
#
# represented by 'robot.png' ingame (so player and npc look the same)
#
# has a variables in 4 directions that are used in movement and associated getters/setters
# has variables for lives (starts with 3) and coins and has methods to lose and gain lives/coins
class Player(GameObject): 
    def __init__(self, x, y, width=50, height=86, level="ANYWHERE"):
        super().__init__(level, x, y, width, height)
        # movement
        self.__left = False
        self.__right = False
        self.__up = False
        self.__down = False
        # stats
        self.__lives = 3
        self.__coins = 0
    
    # movement getters & setters
    @property
    def left(self):
        return self.__left
    @left.setter
    def left(self, truefalse: bool):
        self.__left = truefalse
    @property
    def right(self):
        return self.__right
    @right.setter
    def right(self, truefalse: bool):
        self.__right = truefalse
    @property
    def up(self):
        return self.__up
    @up.setter
    def up(self, truefalse: bool):
        self.__up = truefalse
    @property
    def down(self):
        return self.__down
    @down.setter
    def down(self, truefalse: bool):
        self.__down = truefalse
    
    # stats GETTERS and methods
    @property
    def lives(self):
        return self.__lives
    def gain_live(self, amount: int=1):
        self.__lives += amount
    def lose_live(self, amount: int=1):
        self.__lives -= amount
    @property
    def coins(self):
        return self.__coins
    @coins.setter
    def coins(self, coins):
        self.__coins = coins
    def gain_coin(self, amount: int=1):
        self.__coins += amount
    def lose_coin(self, amount: int=1):
        if self.__coins >= amount:
            self.__coins -= amount
            return True
        else:
            return False



# LEVEL
#
# Another custom class, however does NOT inherit from GameObject
# 
# Levels are used to store information that pygame uses to know how to draw the window and which things to display in the window
#
# Levels have a name
# the width & height variables are used to define the width and height of windows in pygame
# color variable is used to define the background color, using a tuple that has 3 values ranging from 0 to 255
# GameObjects are stored in lists.
# the Levels themself will be stored in a dictionary
# 
# When the game is running there will always be one current Level
class Level:
    def __init__(self, name: str, width: int, height: int, color: tuple):
        self.__name = name
        self.__width = width
        self.__height = height
        self.__color = color
        self.__doors = []
        self.__coins = []
        self.__npcs = []
        self.__bugs = []
    # GETTERS
    @property
    def name(self):
        return self.__name
    @property
    def width(self):
        return self.__width
    @property
    def height(self):
        return self.__height
    @property
    def color(self):
        return self.__color
    @property
    def doors(self):
        return self.__doors
    @property
    def coins(self):
        return self.__coins
    @property
    def npcs(self):
        return self.__npcs
    @property
    def bugs(self):
        return self.__bugs
    
    






# The code of the actual game
class RobotJourney:
    # Initialize
    def __init__(self):
        # INIT PYGAME
        pygame.init()
        self.__clock = pygame.time.Clock()
        
        # LOAD STUFF
        self.__load_everything()

        # START MAIN GAME LOOP
        self.__main_loop()





    # LOAD ALL
    def __load_everything(self):
        # quest variables
        self.__load_quest_variables()
        # images
        self.__load_images()
        # Player Character Object
        self.__load_player()
        # stats display
        self.__render_displays()
        # Doors - list
        self.__load_doors()
        # Coins
        self.__load_coins()
        # NPC's
        self.__load_NPCs()
        # Bugs
        self.__load_bugs()
        # Levels - dict
        self.__load_levels()
        # Load the first level
        self.__next_level("INTRO")

    # QUEST / LEVEL VARIABLES
    def __load_quest_variables(self):
        # ROOF : COIN_RAIN quest
        self.__rain = False
        self.__rained_coins = 0
        self.__sky_coins = 0
        # FALL
        self.__fall_coins = 0
        # ELEVATOR
        self.__elevator_go_up = False
        # RESCUE    (SEWERS_2 Level)
        self.__follower_lives = 2
        # SCORE
        self.__friends = 0

    # IMAGES
    def __load_images(self):
        
        # PLAYER
        self.__player_character = pygame.image.load("robot.png")
        
        # GAME OBJECT IMAGES
        # doors
        self.__door_image = pygame.image.load("door.png")
        # coins
        self.__coin_image = pygame.image.load("coin.png")
        # npc's
        self.__npc_image = pygame.image.load("robot.png")
        # bugs
        self.__bug_image = pygame.image.load("monster.png")

    # PLAYER
    def __load_player(self):
        self.__player = Player(520, 470)    # starting coordinates
        
    # TEXT DISPLAYS
    def __render_displays(self):    
        
        # coins & lives stats
        self.__font = pygame.font.SysFont("Cascadia Mono", 28)
        self.__coins_text = self.__font.render(f"Coins: {self.__player.coins}", True, (255, 255, 0))
        self.__lives_text = self.__font.render(f"Lives: {self.__player.lives}", True, (255, 0, 0))
        
        # quest related stats
        self.__sky_coins_text = self.__font.render(f"Sky Coins: {self.__sky_coins}", True, (255, 128, 0))
        self.__follower_lives_text = self.__font.render(f"Follower Lives: {self.__follower_lives}", True, (255, 0, 255))
        
        # NPC MESSAGES
        self.__npc_font = pygame.font.SysFont("Cascadia Mono", 24)
        self.__npc_greeting_message = self.__npc_font.render('" HELLO  WORLD "', True, (255, 255, 255))
        self.__npc_friend_message = self.__npc_font.render('" friend  =  True "', True, (255, 255, 255))
        
        # INTRO TEXT
        self.__title_font = pygame.font.SysFont("Cascadia Mono", 100)
        self.__title_text = self.__title_font.render("  A  ROBOT'S  JOURNEY  ", True, (255, 255, 255))
        self.__big_font = pygame.font.SysFont("Cascadia Mono", 30)
        self.__intro_lines = ["Use the ARROW keys to move.", "Use SPACE to enter doors or talk to other robots.", "Robots speak a weird dialect of Python.", "Collect COINS and make FRIENDS.", "Avoid the BUGs.", "Press ESCAPE to exit without scoring.", "Or enter the door on the left to SCORE & EXIT.",  "This is you: "]
        self.__score_and_exit_text = self.__font.render("SCORE & EXIT", True, (255, 255, 255))

        # SCORING TEXT
        self.__game_over_text = self.__title_font.render("GAME OVER", True, (255, 255, 255))
        self.__final_score_text = self.__big_font.render("FINAL SCORE: ", True, (255, 255, 255))
        self.__final_coins_text = self.__big_font.render(f"COINS: {self.__player.coins}", True, (255, 255, 0))
        self.__final_friends_text = self.__big_font.render(f"FRIENDS: {self.__friends}", True, (255, 0, 255))
        self.__escape_to_exit_text = self.__big_font.render("Press ESCAPE to exit.", True, (255, 255, 255))
        self.__n_for_new_game_text = self.__big_font.render("Press N to start a new game.", True, (255, 255, 255))

    # All the GameObjects are stored in lists (except COINS, which are in a dict). First all these lists are loaded.
    # Then a dict of all the Levels will be loaded
    # Then all the GameObjects will be loaded in their corresponding levels
     
    # DOORS
    def __load_doors(self):
        # list of all doors
        self.__all_doors = [
        #   Door("LEVEL_NAME", x, y, "Door.id", "Door.link"),
            Door("INTRO", 600, 720 - self.__door_image.get_height(), "INTRO_SOUTH", "BEGIN_SOUTH"),
            Door("INTRO", 40, 720 - self.__door_image.get_height(), "EXIT", "SCORING"),

            Door("BEGIN", 320, 480 - self.__door_image.get_height(), "BEGIN_SOUTH", "INTRO_SOUTH"),    
            Door("BEGIN", 0, 200, "BEGIN_WEST", "TRUST_EAST"),
            Door("BEGIN", 640 - self.__door_image.get_width(), 200,"BEGIN_EAST", "HALLWAY_WEST"),
            Door("BEGIN", 320, 10, "BEGIN_NORTH", "ROOF_SOUTH"),

            Door("HALLWAY", 0, 240, "HALLWAY_WEST", "BEGIN_EAST"),
            Door("HALLWAY", 320 - self.__door_image.get_width(), 240 - self.__door_image.get_height(), "HALLWAY_EAST", "ELEVATOR_DOOR"),

            Door("ROOF", 480, 480 - self.__door_image.get_height(), "ROOF_SOUTH", "BEGIN_NORTH"),
            
            Door("TRUST", 640 - self.__door_image.get_width(), 240, "TRUST_EAST", "BEGIN_WEST"),
            Door("TRUST", 160, 480 - self.__door_image.get_height(), "TRUST_SOUTH", "FALL_DOWN"),

            Door("FALL_2", 320 - self.__door_image.get_width(), 720 - self.__door_image.get_height(), "FALL_2_DOOR", "SEWERS_WEST"),

            Door("SEWERS", 0, 240, "SEWERS_WEST", "FALL_2_DOOR"),
            Door("SEWERS", 1200 - self.__door_image.get_width(), 240, "SEWERS_EAST", "SEWERS_2_WEST"),
            Door("SEWERS", 620, 480 - self.__door_image.get_height(), "SEWERS_SOUTH", "MARKET_NORTH"),

            Door("SEWERS_2", 0, 240, "SEWERS_2_WEST", "SEWERS_EAST"),
            Door("SEWERS_2", 1200 - self.__door_image.get_width(), 240, "SEWERS_2_EAST", "ELEVATOR_DOOR"),

            Door("ELEVATOR", 0, 80, "ELEVATOR_DOOR", "ELEVATOR_SPECIAL"),

            Door("MARKET", 220, 0, "MARKET_NORTH", "SEWERS_SOUTH"),
            Door("MARKET", 480 - self.__door_image.get_width(), 240, "MARKET_EAST", "CAGE_DOOR"),
            
            Door("CAGE", 0, 100, "CAGE_DOOR", "MARKET_EAST")

        ]

    # COINS
    def __load_coins(self):
        # dict with lists of coins per corresponding level
        # here they are tuples, will be converted into coins later
        self.__all_coins = {
           
            'INTRO': [(350,188), (350,228), (350,268), (350,308), (350,348), (350,388), (350,428), (350,468)],
            'BEGIN' : [(50,60), (50,110), (50,350), (50,400), (100,350), (100,400)],
            'HALLWAY' : [(150,100), (150,220), (150,340)],
            'TRUST' : [(120,100), (200,100), (280,100), (360,100), (440,100)],
            'SEWERS' : [(150,80), (150,200), (150,360), (350,160), (350,300), (350,420), (550,80), (550,300), (550,420), (750,80), (750,280), (750,420), (950, 80), (950,300), (950, 420)],
            'SEWERS_2' :[(200,80), (200,200), (200,340), (400,160), (400,300), (400,420), (600,80), (600,300), (600,420), (800,80), (800,260), (800,420)]

        }

    # NPC's
    def __load_NPCs(self):
        self.__all_npcs = [

            NPC("INTRO", 1000, 720 - self.__npc_image.get_height(), "Friendly Fred", "FRIEND_OF_FRIEND", ['', '" if friend.friend  ==  True: ', '        friend  =  True "']),
            NPC("ROOF", 50, 480 - self.__npc_image.get_height(), "Rooftop Roy", "COIN_RAIN", ['" sky.rain_coins() ', 'if collect_my_coins():', '  self.give_half_to( player ) "'], [' ','" too few ', ' friend  =  False "']),
            NPC("TRUST", 50, 480 - self.__npc_image.get_height(), "Trapdoor Terry", "FALL_DOWN", ['" player.fall() ', '   player.fall() ', ' FALL FALL FALL"']),
            NPC("SEWERS_2", 45, 480 - self.__npc_image.get_height(), "Lost Louis", "RESCUE", [' ', '" self.islost() ', ' player.escort_to( right_side )"'], ['','', '" follow  =  True "']),
            NPC("ELEVATOR", 182 - self.__npc_image.get_width(), 240 - self.__npc_image.get_height(), "Elevator Elly", "USE_ELEVATOR", ['', '" if player.pay( 1 ): ', '   use_elevator() "']),
            NPC("ELEVATOR_2", 182 - self.__npc_image.get_width(), 240 - self.__npc_image.get_height(), "Elevator Elly", "ELEVATOR_JOKE", ['', '" elevator  =  stuck', '    BYE WORLD "'], ['" HA HA HA', 'if  joke  ==  True:', '     friend  =  True "'], quest_stage=5),
            NPC("MARKET", 320, 240, "Spareparts Spike", "BUY_LIFE", [' ', '" if player.pay( 10 ): ', '   player.buy( 1 life ) "']),
            NPC("CAGE", 180, 120, "Vicky the Victem", "NAIVE", [' ', ' ', ' '])
        
        ]

    # BUGS
    def __load_bugs(self):
        self.__all_bugs = [
            # SEWERS
            Bug("SEWERS", 150, 0),
            Bug("SEWERS", 350, 480 - self.__bug_image.get_height()),
            Bug("SEWERS", 550, 0),
            Bug("SEWERS", 750, 480 - self.__bug_image.get_height()),
            Bug("SEWERS", 950, 0),

            # SEWERS_2
            Bug("SEWERS_2", 150, 480 - self.__bug_image.get_height()),
            Bug("SEWERS_2", 300, 0),
            Bug("SEWERS_2", 450, 480 - self.__bug_image.get_height()),
            Bug("SEWERS_2", 600, 0),
            Bug("SEWERS_2", 750, 480 - self.__bug_image.get_height()),
            Bug("SEWERS_2", 900, 0)

        ]

    # LEVELS 
    # load levels and load lists of game objects into the LEVELS
    def __load_levels(self):
        self.__all_levels = {
        #   'KEY' : Level("LVL_NAME", width, height, (color))
            'INTRO' : Level("INTRO", 1200, 720, (0,0,0)),
            'BEGIN' : Level("BEGIN", 640, 480, (0,0,0)),
            'HALLWAY': Level("HALLWAY", 320, 480, (0,0,0)),
            'ROOF': Level("ROOF", 960, 480, (0,0,102)),
            'TRUST' : Level("TRUST", 640, 480, (0,0,0)),
            'FALL' : Level("FALL", 320, 720, (50,50,50)),
            'FALL_2' : Level("FALL_2", 320, 720, (50,50,50)),
            'SEWERS' : Level("SEWERS", 1200, 480, (50,100,0)),
            'SEWERS_2' : Level("SEWERS_2", 1200, 480, (50,100,0)),
            'ELEVATOR' : Level("ELEVATOR", 240, 240, (153,0,153)),
            'ELEVATOR_2' : Level("ELEVATOR_2", 240, 240, (153,0,153)),
            'MARKET' : Level("MARKET", 480, 480, (100,50,0)),
            'CAGE' : Level("CAGE", 360, 360, (100,50,0)),
            #'RANDOM' : Level("RANDOM", 360, 360, (0,0,0)),     # ended up not using this
            'SCORE' : Level("SCORE", 720, 540, (0,0,0))
        }

        # load coins into corresponding levels
        for lvl in self.__all_coins:
            for coin in self.__all_coins[lvl]:          
                self.__all_levels[lvl].coins.append(Coin(lvl, coin[0], coin[1]))    # note how the tuple is converted into a Coin object

        # coins works a bit different, but below could all be refactored into single method
        # load doors into corresponding levels
        for lvl in self.__all_levels:
            for door in self.__all_doors:
                if door.level == lvl:
                    self.__all_levels[lvl].doors.append(door)
        
        # load npcs into levels
        for lvl in self.__all_levels:
            for npc in self.__all_npcs:
                if npc.level == lvl:
                    self.__all_levels[lvl].npcs.append(npc)
        
        # load bugs into levels
        for lvl in self.__all_levels:
            for bug in self.__all_bugs:
                if bug.level == lvl:
                    self.__all_levels[lvl].bugs.append(bug)
        
    





    # MAIN GAME LOOP, basically the same as in the examples of part 13 & 14, with a little bit extra
    def __main_loop(self):
        while True:
            # check for events (player inputs)
            self.__check_events()
            # draw level
            self.__draw_level()
            # consume coins
            self.__eat_coins()
            # move bugs and handle touching one
            self.__move_bugs_vertically()
            self.__touch_bug()
            # specific level / quest events
            self.__level_events()




    # CHECK EVENTS = PLAYER CONTROLS
    # This code is very simular to examples in part 13 & 14
    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # CONTROLS
            if event.type == pygame.KEYDOWN:
                # arrows
                if event.key == pygame.K_LEFT:
                    self.__player.left = True
                if event.key == pygame.K_RIGHT:
                    self.__player.right = True
                if event.key == pygame.K_UP:
                    self.__player.up = True
                if event.key == pygame.K_DOWN:
                    self.__player.down = True
                
                # SPACE_BAR is used to interact with NPCs and DOORS
                # Try to open a DOOR. If this fails, try to talk an NPC (this way SPACE_BAR can be used for both)
                if event.key == pygame.K_SPACE:
                    if not self.__open_door():
                        self.__talk_to_npc()
                
                # Esc = Exit
                if event.key == pygame.K_ESCAPE:
                    exit()
                # After scoring press N to start new game
                if event.key == pygame.K_n and self.__level.name == "SCORE":
                    self.__load_everything()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.__player.left = False
                if event.key == pygame.K_RIGHT:
                    self.__player.right = False
                if event.key == pygame.K_UP:
                    self.__player.up = False
                if event.key == pygame.K_DOWN:
                    self.__player.down = False

        # EXECUTE MOVEMENT 
        # execute horizontal movement        
        # (if player is doing the follower quest in the level SEWERS_2, the NPC will also follow)   
        if self.__player.left and self.__player.x > 0:
            self.__player.x -=2
            # FOLLOWER
            if self.__level.name == "SEWERS_2" and self.__level.npcs[0].quest_stage == 20:
                self.__level.npcs[0].x -= 2
        if self.__player.right and self.__player.x + self.__player.width < self.__window_width:
            self.__player.x += 2
            # FOLLOWER
            if self.__level.name == "SEWERS_2" and self.__level.npcs[0].quest_stage == 20:
                self.__level.npcs[0].x += 2
        
        # if allowed execute vertical movement 
        # (ROOF, FALL and FALL_2 don't allow vertical movement, but that code is in: __next_level())
        if self.__vertical_movement:
            if self.__player.up and self.__player.y > 0:
                self.__player.y -= 2
                # FOLLOWER
                if self.__level.name == "SEWERS_2" and self.__level.npcs[0].quest_stage == 20:
                    self.__level.npcs[0].y -= 2
            if self.__player.down and self.__player.y + self.__player.height < self.__window_height:
                self.__player.y += 2
                # FOLLOWER
                if self.__level.name == "SEWERS_2" and self.__level.npcs[0].quest_stage == 20:
                    self.__level.npcs[0].y += 2

    # MOVE BUGS
    def __move_bugs_vertically(self):
        for bug in self.__level.bugs:
            # move bugs
            if bug.down:
                bug.y += 2
            else:
                bug.y -= 2
            # if bug hit wall, change direction
            if bug.down and bug.y + bug.height >= self.__window_height:
                bug.down = False
            elif not bug.down and bug.y <= 0:
                bug.down = True          

    # LEVEL SPECIFIC EVENTS
    def __level_events(self):

        # ROOF
        # RAIN COINS
        if self.__level.name == "ROOF" and self.__rain == True:
            self.__rain_coins("ROOF")
        
        # FALL
        # RAIN COINS UPWARDS
        elif self.__level.name == "FALL":
            self.__player_keeps_falling()
            self.__rain_coins("FALL")
            self.__rain_bugs()
        # KEEP RESETTING FALL LEVEL TO CREATE ILLUSION OF CONTINUOUS FALLING
        if self.__level.name == "FALL" and self.__player.y > self.__window_height:
            self.__level.coins.clear()
            self.__level.bugs.clear()
            self.__player.y = 0

            # If all 50 fall coins have been generated, continue to FALL_2
            if self.__fall_coins >= 50:
                self.__next_level("FALL_2")

        # FALL_2
        # IN FALL_2 PLAYER KEEPS FALLING TILL BOTTOM
        if self.__level.name == "FALL_2" and self.__player.y + self.__player.height < self.__window_height:
            self.__player_keeps_falling()

        # SEWERS_2
        # This level has a quest with an npc following the player. The player has to escort the npc to the right side of the room to succeed.
        if self.__level.name == "SEWERS_2" and self.__level.npcs[0].x > 1050:
            self.__level.npcs[0].quest_stage = 30




    # DRAW LEVEL / WINDOW
    def __draw_level(self):
        # fill background with level color
        self.__window.fill(self.__level.color)

        # draw Game Objects
        # draw DOORS
        for door in self.__level.doors:
            self.__window.blit(self.__door_image, (door.x, door.y))        
        # draw BUGS
        for bug in self.__level.bugs:
            self.__window.blit(self.__bug_image, (bug.x, bug.y))
        # draw COINS
        for coin in self.__level.coins:
            self.__window.blit(self.__coin_image, (coin.x, coin.y))

        # draw NPCs + NPC text
        self.__draw_npcs()  # a lot of coding to display text dending on the current quest_stage, so has its own method

        # draw player
        self.__window.blit(self.__player_character, (self.__player.x, self.__player.y))


        # DRAW STATS
        # COINS & LIVES 
        self.__window.blit(self.__coins_text, (self.__window_width - 105, 15))
        self.__window.blit(self.__lives_text, (10, 15))

        # quest specific stats
        if self.__level.name == "ROOF" and self.__level.npcs[0].quest_stage == 10:
            self.__window.blit(self.__sky_coins_text, (self.__window_width - 145, 50))
        if self.__level.name == "SEWERS_2" and self.__level.npcs[0].quest_stage >= 20 and self.__level.npcs[0].quest_stage < 30:
            self.__window.blit(self.__follower_lives_text, (10, 50))
        
        # DRAW OTHER TEXT
        # INTRO LVL TEXT
        if self.__level.name == "INTRO":
            self.__draw_intro_text()    # lot of text, so has its own method
        # FINAL SCORING TEXT
        if self.__level.name == "SCORE":
            self.__draw_score_text()    # lot of text, so has its own method


        # UPDATE & TICK
        pygame.display.flip()
        self.__clock.tick(60)


    # DRAW NPCS and NPC TEXT
    def __draw_npcs(self):
        # check each npc in level
        for npc in self.__level.npcs:
            # NPC IMAGE
            self.__window.blit(self.__npc_image, (npc.x, npc.y))
            
            # NPC TEXT
            # draw npc message, depending on quest stage (quest_stage 0 & 30 are basic messages, same for all npcs, quest_stage 10 renders a unique message)
            if npc.quest_stage == 0:
                self.__window.blit(self.__npc_greeting_message, (npc.x - 48, npc.y - 20))
            
            elif npc.quest_stage >= 30:
                self.__window.blit(self.__npc_friend_message, (npc.x - 40, npc.y - 20))
            
            # pygame render text doesnt allow multiple lines (so can't use '\n'), so print multiple lines from a list to get the same effect
            elif npc.quest_stage == 10:
                for line in npc.quest_message:
                    self.__window.blit(self.__npc_font.render(f'{line}', True, (255, 255, 255)), (npc.x - 40, npc.y - 64 + npc.quest_message.index(line) * 22))
            
            # Some npcs use quest_stage 20
            elif npc.quest_stage == 20:
                for line in npc.quest_message_2:
                    self.__window.blit(self.__npc_font.render(f'{line}', True, (255, 255, 255)), (npc.x - 40, npc.y - 64 + npc.quest_message_2.index(line) * 22))

    # DRAW TEXT FOR INTRO SCREEN
    def __draw_intro_text(self):
        # TITLE
        self.__window.blit(self.__title_text, (200, 80))
        # Game Explanation text
        for line in self.__intro_lines:
            self.__window.blit(self.__big_font.render(f'{line}', True, (255,255,255)), (400, 200 + self.__intro_lines.index(line) * 40))
        # 'Score & Exit' Door
        self.__window.blit(self.__score_and_exit_text, (0, 640))
    # DRAW TEXT FOR SCORE SCREEN
    def __draw_score_text(self):
        # game over
        self.__window.blit(self.__game_over_text, (160, 80))
        # scores
        self.__window.blit(self.__final_score_text, (200, 170))
        self.__window.blit(self.__final_coins_text, (240, 250))
        self.__window.blit(self.__final_friends_text, (430, 250))
        # mention keys for exit or new game
        self.__window.blit(self.__escape_to_exit_text, (200, 400))
        self.__window.blit(self.__n_for_new_game_text, (200, 440))





    # GO TO NEXT LEVEL AND CHANGE RELEVANT SETTINGS
    def __next_level(self, lvl: str):

        # change active level
        self.__level = self.__all_levels[lvl]

        # change window size
        self.__window_width = self.__level.width
        self.__window_height = self.__level.height
        self.__window = pygame.display.set_mode((self.__window_width, self.__window_height)) 

        # change window caption
        pygame.display.set_caption(f"A Robot's Journey: {self.__level.name}")

        # change movement rules (for certain levels)
        if self.__level.name in "ROOF_FALL_2":
            self.__vertical_movement = False
        else:
            self.__vertical_movement = True
        










    # INTERACTIONS

    # GENERIC CHECK COLLISION CODE
    # checks if two different GameObjects are occupying the same position
    def __check_for_collision(self, agent: GameObject, other: GameObject):
        # the '- 8' is to adjust for the fact that the size of the actual .png is bigger than what the player sees, somewhat imprecise, but it works
        # check x
        if agent.x + agent.width - 8 >= other.x and not agent.x > other.x + other.width - 8:
            # check y
            if agent.y + agent.height - 8 >= other.y and not agent.y > other.y + other.height - 8:
                return True


    # these methods all use the __check_for_collision() method
    # CONSUME COINS
    def __eat_coins(self):
        # check each coin in current level
        for coin in self.__level.coins:
            # check collission with player
            if self.__check_for_collision(self.__player, coin):
                
                # remove coin from list
                self.__level.coins.remove(coin)
                # give the player a coin
                self.__player.gain_coin()

                # check if player is collecting sky coins (related to the quest in the ROOF level)
                if self.__level.name == "ROOF" and self.__rain == True:
                    self.__sky_coins += 1 
                
                # update the display (so the player sees they collected a coin)
                self.__render_displays()

    # TOUCH ENEMY
    def __touch_bug(self):
        for bug in self.__level.bugs:
            # check collision for player
            if self.__check_for_collision(self.__player, bug):
                self.__level.bugs.remove(bug)   # the bug dies, remove from list
                self.__player.lose_live()       # player loses a life
                self.__render_displays()        # update the display, so player can see they now have one less life
                
                # if player has no more lives left, game over and go to scoring
                if self.__player.lives <= 0:
                    self.__final_scoring()
                    
            # check collision for npcs (relevant in SEWERS_2 Level, which has a quest with NPC following Player)
            for npc in self.__level.npcs:
                if self.__check_for_collision(npc, bug):
                    self.__level.bugs.remove(bug)   # the bug dies, remove from list
                    self.__follower_lives -= 1      # follower has one less life  
                    self.__render_displays()        # update the display so player can see follower has one less life
                    
                    # if follower has no more lives, it dissapears
                    if self.__follower_lives <= 0:
                        # removing caused issues, just placing it out of sight also works
                        #self.__level.npcs.remove(npc)
                        npc.x = -100
                        npc.y = -100
                        npc.quest_stage = -10

    # OPEN DOOR
    def __open_door(self):
        
        # check doors in level
        for door in self.__level.doors:
            # check collision
            if self.__check_for_collision(self.__player, door):
                # save the address of the linked door
                new_door = door.link

                # SPECIAL CASES
                # special case for FALL, FALL level has no doors, when player enters the Door linked to FALL_DOWN, they will enter top of FALL level (and start falling)
                if new_door == "FALL_DOWN":
                    self.__next_level("FALL")
                    self.__player.y = 0
                    self.__elevator_go_up = True        # having to keep track of the location/direction of an elevator is very painful
                # special case for ELEVATOR
                if new_door == "ELEVATOR_SPECIAL":      # the door inthe ELEVATOR Level doesn't link to specific door, instead depending of the state of the elevator it will link to either of two doors
                    if self.__elevator_go_up == False:
                        new_door = "HALLWAY_EAST"
                    elif self.__elevator_go_up == True:
                        new_door = "SEWERS_2_EAST"
                # if player uses the "SCORE & EXIT" Door in the INTRO LEvel, go to scoring (SCORE Level has no doors, once entering scoring should not be able to go back)
                if new_door == "SCORING":
                    self.__final_scoring()      # same code as when player dies and has no more lives left


                # check ALL doors for the linked address
                for door in self.__all_doors:
                    if door.id == new_door:
                        # set new level
                        self.__next_level(door.level)
                        # set player coordinates in new level (adjust a bit, because player image is taller than door image)
                        self.__player.x = door.x + door.width - self.__player.width
                        self.__player.y = door.y + door.height - self.__player.height
                        return True     # SPACE_BAR is used for both interaction with NPCs and DOORS, so if we return True the game knows it should not try to interact with an NPC
    



    # TALK TO NPC
    def __talk_to_npc(self):
        # functionality to talk to npc when standing next to / around to
        for npc in self.__level.npcs:
            # check for collision OR adjacency (so doesnt use generic code)
            # check y
            if self.__player.y + self.__player.height >= npc.y and not self.__player.y > npc.y + npc.height:
                # check x  (more broader than other checks, standing next to npc is good enough)
                if self.__player.x + self.__player.width > npc.x and self.__player.x - self.__player.width < npc.x:
                    # check quest stage --- I'm sorry, everything relating to quests is a mess, complete spaghetti code, but it works right now and refactoring will break everything
                    if npc.quest_stage == 5:
                        npc.quest_stage += 5
                    elif npc.quest_stage == 0:
                        self.__advance_quest(npc)
                        npc.quest_stage += 10                       
                    elif npc.quest_stage >= 10:
                        self.__advance_quest(npc)





    # QUEST METHODS
    # GENERIC  
    # Sadly, the method __advance_quest() has become SPAGHETTI CODE ---MY BAD--- but if I refactor this, quests will break and I'm kinda out of time.
    # So I dont expect you to read and understand it all, but these are the basics:

    # quest_id
    # NPC objects have a variable 'quest_id' (a string) which is used to know which code to run.

    # quest_stage
    # NPC objects have a variable 'quest_stage', (integer) which starts at 0. It is used to track the progress of the quest. It can only go up, not down
    # talking to an npc and fullfilling quest objectives will increment their quest_stage (often by 10, but it depends on the quest)
    # a quest_stage of 30 indicates a quest has been completed and the npc is now considered a friend.
    
    def __advance_quest(self, npc: NPC):

        # ROOF Level Quest
        # After initiating it will immediatly start to rain coins
        # Withing this level coin collection will also be tracked as 'Sky Coins'
        # NPC claims the sky coins are his, but the player has to collect them.
        # The player gets to keep half, if he collected at least 20 sky coins and the player shares, the NPC will be a friend
        # However, if the player collects the coins and then never talks to the NPC he gets to keep all the coins (but doesnt make a friend)                                    
        if npc.quest_id == "COIN_RAIN":
            # start rain
            if self.__rained_coins == 0:
                self.__rain = True                
            # finish quest                      # make sure player doesn't finish quest with still a bunch of coins in the air
            elif self.__rained_coins >= 50 and len(self.__level.coins) == 0 and npc.quest_stage < 20:
                # turn off rain
                self.__rain = False
                # if player collected at least 20 sky coins, Roy is happy and friend
                # the method __eat_coins() will (if this quest is ongoing) keep track of how many coins have been collected in the ROOF level, that's the stat sky coins.
                if self.__sky_coins >= 20:
                    self.__level.npcs[0].quest_stage = 30
                else:
                    self.__level.npcs[0].quest_stage = 20
                # give half the Sky Coins to Rooftop Roy
                self.__player.lose_coin(self.__sky_coins // 2)
                self.__render_displays()
                self.__sky_coins = 0
            
        # ELEVATOR
        elif npc.quest_id == "USE_ELEVATOR" and npc.quest_stage >= 10:
            if self.__player.lose_coin():   # using the elevator costs 1 coin, so player coins must be at least 1
                self.__render_displays()    # update display, so player can see they lost 1 coin
                self.__next_level("ELEVATOR_2") # go to next level which is ELEVATOR_2, the elevator in transit (so no doors)
                # switch elevator destination
                if self.__elevator_go_up:
                    self.__elevator_go_up = False
                elif not self.__elevator_go_up:
                    self.__elevator_go_up = True

        # ELEVATOR_2        
        elif npc.quest_id == "ELEVATOR_JOKE":
            npc.quest_stage += 10
            if npc.quest_stage >= 30:
                self.__next_level("ELEVATOR")
                # set the quest stage of the guy in new level
                self.__level.npcs[0].quest_stage = 30
        

        # follower quest, once quest_stage is 20, npc will follow the player within the level
        elif npc.quest_id == "RESCUE":
            if npc.quest_stage == 10:
                npc.quest_stage += 10
        

        # player can buy 1 life in MARKET Level for 10 coins, but this will kill the NPC in CAGE Level, a life for a life
        elif npc.quest_id == "BUY_LIFE":
            if npc.quest_stage == 10:
                if self.__player.lose_coin(10):
                    self.__player.gain_live()
                    self.__render_displays()
                    npc.quest_stage += 10
                    # remove the npc in the CAGE level
                    # remove from level
                    self.__all_levels['CAGE'].npcs.clear()
                    # remove from all npcs list
                    for npc in self.__all_npcs:
                        if npc.quest_id == "NAIVE":
                            self.__all_npcs.remove(npc)
        

        # NPC in CAGE always wants to be your friend
        elif npc.quest_id == "NAIVE":
            npc.quest_stage = 30


        # NPC in INTRO Level wants to be your friend if you have at least 1 other friend
        elif npc.quest_id == "FRIEND_OF_FRIEND":
            if npc.quest_stage > 0 and npc.quest_stage < 30:
                num_of_friends = 0
                
                # count all friends
                for lvl in self.__all_levels:
                    for other_npc in self.__all_levels[lvl].npcs:
                        if other_npc.quest_stage >= 30:
                            num_of_friends += 1

                # if player has at least 1 friend
                if num_of_friends > 0:
                    npc.quest_stage = 30







    # PLAYERS FALLS DOWN (This is used in the Levels FALL & FALL_2)
    def __player_keeps_falling(self):
        self.__player.y += 2

    # QUEST / LEVEL SPECIFIC METHODS
    def __rain_coins(self, lvl_name: str):
        # Used in Level ROOF & FALL 
        # in ROOF the coins actually fall down
        if lvl_name == "ROOF":
            y_value = 1
            y_position = 0
            condition = self.__rained_coins
        # in FALL the coins shoot upwards to generate the feeling that the player is falling
        elif lvl_name == "FALL":
            y_value = -3
            y_position = self.__window_height - 1
            condition = self.__fall_coins

        # Add coin to  respective coins list.
        if condition <= 50:
            # random chance of creating a coin in the sky
            if randint(1, 60) == 1:
                self.__level.coins.append(Coin(self.__level.name, randint(0, self.__window_width - self.__coin_image.get_width()), y_position))   
                # increment the condition
                if lvl_name == "ROOF":
                    self.__rained_coins += 1
                elif lvl_name == "FALL":
                    self.__fall_coins += 1

        # move all coins
        for coin in self.__level.coins:
            coin.y += y_value
        # clean up coins
        for coin in self.__level.coins:
            if coin.y > self.__window_height or coin.y < 0:
                self.__level.coins.remove(coin)

    # RAIN BUGS
    # probably could/should be refactored since it's mostly the same code as __rain_coins()
    def __rain_bugs(self):
        if self.__fall_coins <= 50:
            if randint(1, 180) == 1 and self.__player.y < self.__window_height - 240:
                self.__level.bugs.append(Bug(self.__level.name, randint(0, self.__window_width - self.__bug_image.get_width()), self.__window_height - 1))
        # move bugs
        for bug in self.__level.bugs:
            bug.y += -1
        # clean up bugs
        for bug in self.__level.bugs:
            if bug.y > self.__window_height or bug.y < 0:
                self.__level.bugs.remove(bug) 





    # FINAL SCORING
    # used when player dies and is out of lives or when they used the 'SCORE & EXIT' Door in INTRO Level
    def __final_scoring(self):
        # go to scoring screen
        self.__next_level("SCORE")
        # set player coordinates
        self.__player.x = 360
        self.__player.y = 300 - self.__player.height
        
        # count number of FRIENDS made
        friends_list = []
        for lvl in self.__all_levels:
            for npc in self.__all_levels[lvl].npcs:
                if npc.quest_stage >= 30:
                    # Technically speaking there are two instances of Elevator Elly, I want to count only one of them
                    if npc.name not in friends_list:
                        friends_list.append(npc.name)
        self.__friends += len(friends_list)
        # show player their scores
        self.__render_displays()




# RUN the PROGRAM
RobotJourney()

