#Imports
import pygame, random, time, pickle, sys
from maps import map
from maps import buttons
from tk import one_country_select, two_country_select, entry_dialogue, start_game, alert, move_country_entry, two_country_attack
############################################################################################################
#start pygame
pygame.init()
clock=pygame.time.Clock()
############################################################################################################
#Variables
global turn_done
turn_done=False
is_legal=True
current_player=None
global  has_been_called
has_been_called=False
game_over=False
while True:
    try:
        player_amount=start_game()
        player_amount=int(player_amount)
        if player_amount<=6:
            break
    except:
        alert("Please enter an amount that is less than or equal to 6")

current_player=None
players=[]
for player in range(player_amount):
	players.append(player+1)
############################################################################################################
#create window
screen=pygame.display.set_mode([0,0],pygame.RESIZABLE |pygame.HWSURFACE)
pygame.display.set_caption("RISK")
background_image= pygame.image.load("map.png").convert()
background_pos=[0,0]
notification_pos=[1570,410]
##transparent_screen=pygame.Surface((374,371))
##transparent_screen.set_alpha(255)
##transparent_screen.fill((255,255,255))
############################################################################################################
#Initalises UI
WHITE=[255,255,255,255]
BLUE=[0,104,178,255]
BLACK=[0,0,0,255]
CLEAR=[0,0,0,128]
RED=[255,0,0]
font=pygame.font.SysFont("Calibri",15,True,False)
#############################################################################################################
#Classes
#Buttons class
class Button(object):
    """Class for menu buttons"""
    def draw_button(self,name):
        x_pos=buttons[name][0]
        y_pos=buttons[name][1]
        b=pygame.draw.rect(screen,CLEAR,[x_pos,y_pos,179,36],0)
        mouse_pos=pygame.mouse.get_pos()
        if b.collidepoint(mouse_pos[0],mouse_pos[1])==True:
            return True
            print("BUTTON")
        else:
            return False
#Button Creator
roll_dice_button=Button()
attack_button=Button()
reinforce_button=Button()
move_button=Button()
next_turn_button=Button()
save_game_button=Button()
load_game_button=Button()
exit_button=Button()

#Create Notification class
class Notification(object):
    """The system of notifying players"""
    def notify(self,message):
        notification=font.render(message,True,BLACK)
        screen.blit(notification,notification_pos)
        time.sleep(2)
    def error(self):
        message=font.render("That cannot be done",True,BLACK)
        screen.blit(message,notification_pos)
error_message=Notification()
notification=Notification()

############################################################################################################
#Functions
#Attack
#Roll dice, higher die wins, remove winners amount of army from loser
def attack(player):
    current_country,new_country=two_country_attack(player)
    #Get Dice loop
    while True:
        screen.blit(background_image,background_pos)
        notification.notify("Attacking player please roll the die")
        e=pygame.event.wait()
        if e.type==pygame.MOUSEBUTTONUP:
            if roll_dice_button.draw_button("Roll Dice")==True:   
                attacking_die=diceroll()
                draw_country_data(player)
                pygame.display.update()
                break
        draw_country_data(player)
        pygame.display.update()
    while True:
        screen.blit(background_image,background_pos)
        notification.notify("Defending player please roll the die")
        e=pygame.event.wait()
        if e.type==pygame.MOUSEBUTTONUP:
            if roll_dice_button.draw_button("Roll Dice")==True:   
                defending_die=diceroll()
                draw_country_data(player)
                pygame.display.update()
                break
        draw_country_data(player)
        pygame.display.update()
    print(attacking_die,defending_die)    
    attacking_army=map[current_country][1]
    attacking_player=map[current_country][0]
    defending_army=map[new_country][1]
    defending_player=map[new_country][0]
    turn_done=True
    if attacking_die>defending_die: #Attacker wins the attack
        if attacking_army>=defending_army: #Complete win for the attacker
            map[new_country][1]=0 #Remove army from defending country
            map[new_country][0]=0 #Remove ownership from defending country
        elif attacking_army<defending_army: #Partial win for attacker
            result=defending_army-attacking_army
            map[new_country][1]=result
    elif attacking_die<defending_die: #Attacker loses attack
        if attacking_army<=defending_army: #Complete loss for attacker
            map[current_country][1]=0 #Remove army from attacking country
            map[current_country][0]=0 #Remove ownership from attacking country
        elif attacking_army>defending_army: #Partial loss for attacker
            result=attacking_army-defending_army
            map[current_country][1]=result
    return turn_done,map
    
#Legal Move
#If new country number is in possible moves of current country and country is owned by player or empty allow move 
def legal_move(current_country,new_country):
    moves=map[current_country][3]
    new=map[new_country][2]
    current_player=map[current_country][0]
    new_player=map[new_country][0]
    if new in moves:
        print(current_player,new_player)
        if current_player==new_player or new_player==0:
            is_legal=True
    else:
        is_legal=False
    return is_legal

#Move Army
#Checks to see if move is legal, if so; checks for moving more army than available, moves army and changes country ownership
def move_army(player):
    current_country,new_country,amount=move_country_entry(player)
    is_legal=legal_move(current_country,new_country)
    current_player=player
    amount=int(amount)
    if is_legal==True:
        new_amount=map[current_country][1]-amount
        print(new_amount)
        #check for having negative army left in country
        if new_amount<0:
            error_message.error()
            time.sleep(5)
            turn_done=False
        elif new_amount==0: #check for having no army left in country
            map[new_country][1]=amount
            map[current_country][1]=new_amount
            map[current_country][0]=0 #Remove ownership in old country
            map[new_country][0]=current_player#set ownership in new country
            turn_done=True
        elif new_amount>0: #check for having army still left in the country
            map[new_country][1]=amount
            map[current_country][1]=new_amount
            map[new_country][0]=current_player #set ownership in new country
            turn_done=True
    else:
        error_message.error()
        time.sleep(5)
        turn_done=False
    return turn_done, map

#Next Turn
#Cycle through each player by adding one until end player when it subtracts to go back to 1st player
def next_turn(turn_done,player):
    if turn_done==True:
        player_pos=player+1
        if player_pos>len(players):
            player_pos-=len(players)
        player=players[player_pos-1]
        turn_done=False
    return turn_done, player
	
#Add Army
#Checks if country is not owned by another player, if same owner adds amount rolled by die to army total of country
def add_army(player):
    while True:
        try:
            country=one_country_select(player)
            break
        except KeyError:
            alert("Please select a country")
    #Get Dice loop
    while True:
        screen.blit(background_image,background_pos)
        notification.notify("Please roll the dice")
        e=pygame.event.wait()
        if e.type==pygame.MOUSEBUTTONUP:
            if roll_dice_button.draw_button("Roll Dice")==True:   
                value=diceroll()
                break
        draw_country_data(player)
        pygame.display.update()
    if map[country][0]==player:
        current_amount=map[country][1]
        final_amount=current_amount+value
        map[country][1]=final_amount
        map[country][0]=player
        message=font.render("The amount has been added, total is now"+str(final_amount),True,BLACK)
        screen.blit(message,notification_pos)
        turn_done=True
    else:
        error_message.error()
        time.sleep(5)
        turn_done=False
    return turn_done, map

#Dice Roll
#Generates a number from 1-6 and returns that number
def diceroll():
	value=random.randint(1,6)
	notification.notify("Player has rolled a:"+str(value))
	return value

#Has won game
#Checks to see if total owners exceeds 1, if so contiues play. If not declares winner
def has_won():
    countries_owned=[]
    winner=None
    for entry in map:
        owner=map[entry][0]
        if owner not in countries_owned:
            if owner!=0:
                countries_owned.append(owner)
    if len(countries_owned)>1:
        is_winner=False
    elif len(countries_owned)==1:
        is_winner=True
        winner=str(countries_owned[0])
    else:
        error_message.error()
    return is_winner, winner
	
#Save Game
#Saves the current board ready to be loaded back at a future time
def save_game(player):
    file_name=entry_dialogue()
    f=open(file_name,"wb")
    pickle.dump(map,f)
    picklle.dump(player,f)
    notification.notify("Game Saved")
    f.close()

#Load Game
#Loads a previous game save
def load_game():
    file_name=entry_dialogue()
    try:
        f=open(file_name,"rb")
    except IOError as e:
        error_message.error()
        sys.exit()
    map=pickle.load(f)
    player=pickle.load(f)
    f.close()
    return map, player
    
def draw_country_data(player):
    #Populate Country with Data
    for entry in map:
        text_pos_x=map[entry][4][0]
        text_pos_y=map[entry][4][1]
        if map[entry][0]==player:
            colour=RED
        else:
            colour=WHITE
        text=font.render(str(entry),True,colour)
        player_num=font.render("Player "+str(map[entry][0]),True,BLACK)
        army_amount=font.render("Army:"+str(map[entry][1]),True,BLACK)
        screen.blit(text,[text_pos_x,text_pos_y])
        screen.blit(player_num,[text_pos_x,text_pos_y+25])
        screen.blit(army_amount,[text_pos_x,text_pos_y+50])

def player_defeated(players):
    current_players=[]
    for player in players:
        for entry in map:
            if player==map[entry][0]:
                if player not in current_players:
                    current_players.append(player)
    current_players.sort()
    return current_players
        
############################################################################################################
for player in players:
	first_country_id=random.randint(1,42)
	for entry in map:
		if first_country_id==map[entry][2]:
			map[entry][0]=player
			map[entry][1]=3
current_player=players[0]
#Main Loop
while not game_over:
    #Event Handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
        elif event.type==pygame.MOUSEBUTTONUP:
            if roll_dice_button.draw_button("Roll Dice")==True:
                diceroll()
                print("Roll Dice")
            elif attack_button.draw_button("Attack")==True:
                while True:
                    try:
                        turn_done,map=attack(current_player)
                        break
                    except KeyError:
                        alert("Please enter both countries")
                print("Attack")
            elif reinforce_button.draw_button("Reinforce")==True:
                while True:
                    try:
                        turn_done,map=add_army(current_player)
                        break
                    except KeyError:
                        alert("Please enter a country")
                print("Reinforce")
            elif move_button.draw_button("Move")==True:
                while True:
                    try:
                        turn_done,map=move_army(current_player)
                        break
                    except KeyError:
                        alert("Please enter a country")
                print("Move")
            elif next_turn_button.draw_button("Next Turn")==True:
                turn_done,current_player=next_turn(turn_done,current_player)
                print("Next Turn")
            elif save_game_button.draw_button("Save Game")==True:
                save_game(current_player)
                print("Save Game")
            elif load_game_button.draw_button("Load Game")==True:
                map,current_player=load_game()
                print("Load Game")
            elif exit_button.draw_button("Exit")==True:
                game_over=True
                print("Exit") 
        else:
            game_over=False
    players=player_defeated(players)
    is_winner,winner=has_won()
    if is_winner==True:
        game_over=True
    screen.blit(background_image,background_pos)
    draw_country_data(current_player)
    notification.notify("It is currently players "+str(current_player)+" turn")
    pygame.display.update()
    clock.tick(60)
if is_winner==True:    
    alert("Player "+winner+" has won the game")
pygame.quit()
