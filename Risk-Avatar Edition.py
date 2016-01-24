import sys,pygame
import random
from pygame.locals import *
import os


# citation:
# 
# boardMap:
# http://i.imgur.com/pjLM1.jpg
# 
# soundtrack:
# https://www.youtube.com/watch?v=gsiFrzQ6Qv4
############################################
############### Start Menu #################
############################################
class StartMenu(pygame.sprite.Sprite):
    def __init__(self,width,height):
        black = 0,0,0
        ltblue = 80,125,225
        dkblue = 0,51,102
        self.phase = True
        self.width,self.height = width,height
        # initializing title
        msg = "Risk: A Game of Global Domination"
        largeFont = pygame.font.Font('freesansbold.ttf',50)
        self.title = TextObjs(self.width/2,self.height/3,msg,largeFont,black)

        # initializing avatar
        self.Avatar = AvatarAang(self.width/4,self.height/2)
        
        # initializing buttons
        buttonTexts = ["Single Player Mode","Multi Player Mode",
        "Tutorial","Option"]
        smallFont = pygame.font.Font('freesansbold.ttf',25)
        buttonLength = int(self.width/4)
        buttonHeight = int(self.height/12)
        margin = buttonHeight/3
        self.buttons = []
        x = int(5*self.width/8)

        for i in xrange(len(buttonTexts)):
            buttText = buttonTexts[i]
            y = int(self.height/2 + i * buttonHeight + i * margin)
            button = Button(x=x,y=y,msg=buttText,
                font=smallFont,textcolor=black,
                length=buttonLength,height=buttonHeight,
                buttonColor=ltblue,hoverColor = dkblue)
            self.buttons.append(button)

    def display(self,screen):
        self.title.draw(screen)
        self.Avatar.float(self.height/2,self.height/2 + 20)
        self.Avatar.draw(screen)

        for button in self.buttons:
            button.update()
            button.draw(screen)

class TextObjs(pygame.sprite.Sprite):
    def __init__(self,x,y,msg,font,textColor):
        self.msg = msg
        self.textColor = textColor
        self.font = font
        self.surface = self.font.render(self.msg,True,self.textColor)
        self.rect = self.surface.get_rect()
        self.rect.center = (x,y)

    def update(self):
        self.surface = self.font.render(self.msg,True,self.textColor)

    def draw(self,screen):
        screen.blit(self.surface,self.rect)

class AvatarAang(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.image = pygame.image.load('Aang14.png')
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.speed = 1

    def float(self,upperBound,lowerBound):
        self.rect.y += self.speed
        if self.rect.y < upperBound:
            self.speed = 1
        if self.rect.y > lowerBound:
            self.speed = -2
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Button(TextObjs):
    def __init__(self,x,y,msg,font,textcolor,length,height,
        buttonColor,hoverColor):
        super(Button,self).__init__(x,y,msg,font,textcolor)
        self.length = length
        self.height = height
        self.color = buttonColor
        self.buttonColor = buttonColor
        self.hoverColor = hoverColor

    def mouseOver(self):
        pos = pygame.mouse.get_pos()
        left = self.rect.center[0] - self.length/2
        top = self.rect.center[1] - self.height/2
        if (left <= pos[0] <= left + self.length) and \
        (top <= pos[1] <= top + self.height):
            return True
        else:
            return False

    def leftClick(self):
        return self.mouseOver() and pygame.mouse.get_pressed()[0] == 1

    def update(self):
        if self.mouseOver():
            self.color = self.hoverColor
        else:
            self.color = self.buttonColor


    def draw(self,screen):
        left = self.rect.center[0] - self.length/2
        top = self.rect.center[1] - self.height/2
        self.update()
        pygame.draw.rect(screen,self.color,
                        (left,top,self.length,self.height))
        super(Button,self).draw(screen)

###########################################
############### Board #####################
###########################################
######################### Dark Blue ##############################
Northern_Water_Tribe = {'name': 'N. Water Tribe','x':500,'y':105,
'neighbors':['Abbey','Spirit Oasis']}

Spirit_Oasis = {'name':'Spirit Oasis','x':550,'y':80,
'neighbors':['N. Water Tribe','Outskirts','N. Tundra']}

Outskirs = {'name':'Outskirts','x': 615,'y': 80,
'neighbors':['Provinces','Spirit Oasis','N. Tundra']}

Northern_Tundra = {'name':'N. Tundra','x': 535,'y':40,
'neighbors':['Outskirts','Spirit Oasis','The Shipwreck']}

dkblueStates = [Northern_Water_Tribe,Spirit_Oasis, 
                Outskirs,Northern_Tundra]

dkblueNames = ['N. Water Tribe','Spirit Oasis','Outskirts','N. Tundra']
        
######################### Yellow ##############################
Western_Air_Temple = {'name': 'W. Air Temple','x':320,'y':220,
'neighbors':['Abbey','Sun Warrior Ruins']}

Whaletail_Island = {'name': 'Whaletail Island','x':580,'y':470,
'neighbors':['Kyoshi Island','Patola Mountains','The Swamp']}

Eastern_Air_Temple = {'name': 'E. Air Temple','x':970,'y': 460,
'neighbors':['Oblisk Islands','Siwong Desert','Ba Sing Se']}

Southern_Air_Temple = {'name': 'S. Air Temple','x':430,'y':555,
'neighbors':['Black Cliffs','Patola Mountains']}

Patola_Mountains = {'name': 'Patola Mountains','x': 570,'y': 540,
'neighbors':['S. Tundra','Kyoshi Island','Oblisk Islands','S. Air Temple',
'Whaletail Island']}

Northern_Air_Temple = {'name': 'N. Air Temple','x':728,'y':160,
'neighbors':['Provinces','Taku Ruins','Ba Sing Se','Crystal Catacombs']}

Republic_City = {'name': 'Republic City','x': 535,'y':206,
'neighbors':['Provinces','Wulong Forrest', 'Crescent Islands','Abbey',
'Mt. Makapu']}

yellowStates = [Western_Air_Temple,Whaletail_Island,Eastern_Air_Temple,
Southern_Air_Temple,Patola_Mountains,Northern_Air_Temple,Republic_City]

yellowNames = ['W. Air Temple','Whaletail Island','E. Air Temple',
    'S. Air Temple','Patola Mountains','N. Air Temple','Republic City']

######################### Red ##############################
Sun_Warrior_Ruins = {'name':'Sun Warrior Ruins','x': 255,'y':280,
'neighbors':['W. Air Temple','Boiling Rock','Great Gates of Azulon']}

Boiling_Rock = {'name':'Boiling Rock','x': 350,'y': 300,
'neighbors':['Sun Warrior Ruins','Great Gates of Azulon','Ember Island']}

Great_Gates_of_Azulon = {'name':'Great Gates of Azulon','x': 300,'y':330,
'neighbors':['Sun Warrior Ruins','Ember Island','Fire Nation Capitol',
'Black Cliffs','Boiling Rock']}

Fire_Nation_Capitol = {'name':'Fire Nation Capitol','x':252,'y': 370,
'neighbors':['Great Gates of Azulon','Black Cliffs']}

Black_Cliffs = {'name': 'Black Cliffs','x':350,'y':400,
'neighbors':['Great Gates of Azulon','Fire Nation Capitol','Ember Island',
'Fire Fountain City','S. Air Temple']}

Ember_Island = {'name': 'Ember Island','x': 400,'y': 330,
'neighbors':['Great Gates of Azulon','Black Cliffs']}

Fire_Fountain_City = {'name': 'Fire Fountain City','x': 440,'y': 370,
'neighbors':['Black Cliffs','Roku Island']}

Roku_Island = {'name': 'Roku Island','x': 485,'y': 352,
'neighbors':['Fire Fountain City','Crescent Islands']}

Crescent_Islands = {'name': 'Crescent Islands','x': 520,'y': 320,
'neighbors':['Roku Island','Republic City','Heibai Forrest','Mt. Makapu']}

redStates = [Sun_Warrior_Ruins,Boiling_Rock, Great_Gates_of_Azulon,
Fire_Nation_Capitol, Black_Cliffs, Ember_Island, Fire_Fountain_City,
Roku_Island, Crescent_Islands]

redNames = ['Sun Warrior Ruins','Boiling Rock','Great Gates of Azulon',
    'Fire Nation Capitol','Black Cliffs','Ember Island','Fire Fountain City',
    'Roku Island','Crescent Islands']

######################### Light Blue ##############################
Settlements = {'name': 'Settlements' ,'x': 502,'y':662,
'neighbors':['S. Tundra','The Shipwreck']}

Southern_Tundra = {'name': 'S. Tundra','x': 580,'y': 630,
'neighbors':['Patola Mountains','Ice Floes','The Shipwreck','Settlements']}

The_Shipwreck = {'name': 'The Shipwreck' ,'x':580 ,'y': 695,
'neighbors':['S. Tundra','Ice Floes','Settlements','N. Tundra']}

Ice_Floes = {'name': 'Ice Floes','x': 670,'y': 640,
'neighbors':['S. Tundra','The Shipwreck']}

ltblueStates = [Settlements,Southern_Tundra,The_Shipwreck,Ice_Floes]

ltblueNames = ['Settlements','S. Tundra','The Shipwreck','Ice Floes']

######################### Dark Olive ##############################
The_Great_Divide = {'name':'The Great Divide','x': 655,'y': 300,
'neighbors':['Mt. Makapu','Serpents Pass','Heibai Forrest',
'Kolau Mountains']}

Heibais_Forrest = {'name': 'Heibai Forrest','x': 605,'y': 330,
'neighbors':['Crescent Islands','The Great Divide','Kolau Mountains']}

Kolau_Mountains = {'name': 'Kolau Mountains','x': 710,'y': 330,
'neighbors':['Heibai Forrest','The Great Divide','Omashu',
'Serpents Pass','Siwong Desert']}

Omashu = {'name': 'Omashu','x': 678,'y': 379,
'neighbors':['Kolau Mountains','Siwong Desert','The Swamp']}

The_Swamp = {'name': 'The Swamp','x': 700,'y': 438,
'neighbors':['Kyoshi Island','Whaletail Island','Omashu',
'Siwong Desert']}

Si_Wong_Desert = {'name': 'Siwong Desert','x': 795,'y': 425,
'neighbors':['The Swamp','Omashu','The Library','E. Air Temple']}

Kyoshi_Island = {'name': 'Kyoshi Island','x': 670,'y': 500,
'neighbors':['The Swamp','Whaletail Island','Oblisk Islands']}

The_Oblisk_Islands = {'name':'Oblisk Islands','x': 785,'y': 520,
'neighbors':['Kyoshi Island','E. Air Temple']}

The_Library = {'name': 'The Library','x': 833,'y': 365,
'neighbors':['Siwong Desert','E. Air Temple']}

dkoliveStates = [The_Great_Divide, Heibais_Forrest, Kolau_Mountains, Omashu,
The_Swamp, Si_Wong_Desert, Kyoshi_Island, The_Oblisk_Islands,
The_Library]

dkoliveNames = ['The Great Divide','Heibai Forrest','Kolau Mountains',
'Omashu','The Swamp','Siwong Desert','Kyoshi Island','Oblisk Islands',
'The Library']
######################### Dark Green ##############################
Abbey = {'name': 'Abbey','x': 470,'y': 183,
'neighbors':['Wulong Forrest','W. Air Temple','Republic City',
'N. Water Tribe']}

Wulong_Forrest = {'name': 'Wulong Forrest','x': 451,'y': 262,
'neighbors':['Abbey','Republic City']}

Provinces = {'name': 'Provinces','x': 638,'y': 184,
'neighbors':['Outskirts','N. Air Temple','Taku Ruins','Mt. Makapu',
'Republic City']}

Mt_Makapu = {'name': 'Mt. Makapu','x': 590,'y': 260,
'neighbors':['Republic City','Taku Ruins','Provinces','Crescent Islands',
'The Great Divide']}

Taku_Ruins = {'name': 'Taku Ruins','x': 665,'y': 235,
'neighbors':['Provinces','N. Air Temple','Ba Sing Se','Mt. Makapu']}

Serpents_Pass = {'name': 'Serpents Pass','x': 735,'y': 281,
'neighbors':['The Great Divide','Kolau Mountains','Ba Sing Se',
'Lake Laogai']}

Ba_Sing_Se = {'name': 'Ba Sing Se','x': 835,'y': 235,
'neighbors':['Serpents Pass','Lake Laogai','Crystal Catacombs',
'Eastern Air Temple','Taku Ruins']}

Crystal_Catacombs = {'name': 'Crystal Catacombs', 'x': 816,'y': 175,
'neighbors':['N. Air Temple','Ba Sing Se']}

Lake_Laogai = {'name': 'Lake Laogai','x': 850,'y': 290,
'neighbors':['Ba Sing Se','Serpents Pass']}

dkgreenStates = [Abbey,Wulong_Forrest,Provinces, Mt_Makapu, Taku_Ruins,
Serpents_Pass, Ba_Sing_Se, Crystal_Catacombs, Lake_Laogai]

dkgreenNames = ['Abbey','Wulong Forrest','Provinces','Mt. Makapu','Taku Ruins',
'Serpents Pass','Ba Sing Se','Crystal Catacombs','Lake Laogai']

class Board(pygame.sprite.Sprite):

    def statesInit(self,listStates,textColor,buttonColor,hoverColor):
        font = pygame.font.Font("freesansbold.ttf",10)
        for buttonState in listStates:
            newState = State(x=buttonState['x'],y=buttonState['y'],
                    msg=buttonState['name'],font=font,textColor=textColor,
                    buttonColor=buttonColor,hoverColor=hoverColor,
                    r=20,neighbors=buttonState['neighbors'])
            self.states.append(newState)

    def dkblueStatesInit(self):
        global dkblueStates

        buttonColor = 52,126,201 #ltblue
        hoverColor = 0,51,102 # dkblue
        textColor = 245,245,220 # beige

        self.statesInit(listStates=dkblueStates,textColor=textColor,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def yellowStatesInit(self):
        global yellowStates

        buttonColor = 245,245,220 # beige
        hoverColor = 255,208,0 # yellow
        textColor = 0,0,0 # black

        self.statesInit(listStates=yellowStates,textColor=textColor,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def redStatesInit(self):
        global redStates

        buttonColor = 232,140,49 # lt orange
        hoverColor = 255,55,0 # dk orange
        textColor = 0,0,0 # black

        self.statesInit(listStates=redStates,textColor=textColor,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def ltblueStatesInit(self):
        global ltblueStates

        buttonColor = 0,51,102 # dkblue
        hoverColor = 54,141,255 # lt blue
        textColor = 0,0,0 # black

        self.statesInit(listStates=ltblueStates,textColor=textColor,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def dkoliveStatesInit(self):
        global dkoliveStates

        buttonColor = 34,139,34 # dk green
        hoverColor = 112,112,66 # dk olive
        textColor = 245,245,220 # beige

        self.statesInit(listStates=dkoliveStates,textColor = textColor,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def dkgreenStatesInit(self):
        global dkgreenStates

        buttonColor = 112,112,66 # dk olive
        hoverColor = 34,139,34 # dk green
        textColor = 245,245,220 # beige

        self.statesInit(listStates=dkgreenStates,textColor = textColor,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def diceInit(self):
        attackingDice = ['0','0','0']
        defendingDice = ['0','0']

        font = pygame.font.Font('freesansbold.ttf',25)
        textColor = (0,0,0) # black
        buttonColor = (245,245,220) # beige
        hoverColor = (255,255,255) # white
        buttonSize = 60
        for i in xrange(len(attackingDice)):
            die = attackingDice[i]
            j = 1200 - buttonSize/2 - buttonSize*i
            newDie = Die(x=j,y=buttonSize/2,msg=die,
                font=font,textcolor=textColor,
                length=buttonSize,height=buttonSize,
                buttonColor=buttonColor,hoverColor=hoverColor)
            self.attDice.append(newDie)

        for i in xrange(len(defendingDice)):
            die = attackingDice[i]
            j = 1200 - buttonSize/2 - buttonSize*i
            newDie = Die(x=j,y=3*buttonSize/2,msg=die,
                font=font,textcolor=textColor,
                length=buttonSize,height=buttonSize,
                buttonColor=buttonColor,hoverColor=hoverColor)
            self.defDice.append(newDie)

    def __init__(self):
        img = pygame.image.load("Avatar Map.jpg")
        self.width,self.height = 1200,720
        self.img = img
        self.rect = self.img.get_rect()
        self.states = []
        self.attDice = []
        self.defDice = []
        self.dkblueStatesInit()
        self.yellowStatesInit()
        self.redStatesInit()
        self.ltblueStatesInit()
        self.dkoliveStatesInit()
        self.dkgreenStatesInit()
        self.diceInit()

    def resetDice(self):
        for die in self.attDice:
            die.msg = '0'

        for die in self.defDice:
            die.msg = '0'

    def rollAttDice(self,numDice):
        for i in xrange(numDice):
            self.attDice[i].roll()
            self.attDice[i].update()

    def rollDefDice(self,numDice):
        for i in xrange(numDice):
            self.defDice[i].roll()
            self.defDice[i].update()

    def compareDice(self):
        attDiceVal = [eval(die.msg) for die in self.attDice]
        defDiceVal = [eval(die.msg) for die in self.defDice]

        attList = sorted(attDiceVal)[::-1]
        defList = sorted(defDiceVal)[::-1]

        attFirst,attSecond = attList[0],attList[1]
        defFirst,defSecond = defList[0],defList[1]
        if defSecond == 0:
            if attFirst<=defFirst:
                return "Lose"
            else:
                return "Win"
        else:
            if attFirst > defFirst and attSecond > defSecond:
                return "Win"
            elif attFirst <= defFirst and attSecond <= defSecond:
                return "Lose"
            else:
                return "Tie"

    def findOwner(self,state,players):
        for player in players:
            if state in player.territory:
                return player

    def findState(self,stateName):
        for state in self.states:
            if state.msg == stateName:
                return state

    def draw(self,screen):
       
        # draw background board
        screen.blit(self.img,self.rect)
        # draw states
        for state in self.states:
            state.draw(screen)
        # draw attacking dice
        for die in self.attDice:
            die.draw(screen)
        # draw defending dice
        for die in self.defDice:
            die.draw(screen)

class State(Button):
    def __init__(self,x,y,msg,font,textColor,buttonColor,hoverColor,r,
        neighbors,troop=0):
        self.buttonColor = buttonColor
        self.hoverColor = hoverColor
        self.r = r
        self.center = (x,y)
        # locates statename
        self.msg = msg
        self.textColor = textColor
        self.font = font
        self.name_surface = self.font.render(self.msg,True,self.textColor)
        self.name_rect = self.name_surface.get_rect()
        self.name_rect.center = (x,y - r/3)
        
        self.neighbors = neighbors

        # locates troop
        self.troop = troop
        self.troop_surface=self.font.render(str(self.troop),True,self.textColor)
        self.troop_rect = self.troop_surface.get_rect()
        self.troop_rect.center = (x,y + r/3)

        # state is not claimed
        self.claimed = False
        self.selected = False

    def mouseOver(self):
        pos = pygame.mouse.get_pos()
        mouseX,mouseY = pos[0],pos[1]
        x,y = self.center[0],self.center[1]
        return ((mouseX-x)**2 + (mouseY-y)**2) ** (0.5) <= self.r

    def leftClick(self):
        return self.mouseOver() and pygame.mouse.get_pressed()[0] == 1

    def rightClick(self):
        return self.mouseOver() and pygame.mouse.get_pressed()[2] == 1

    def addTroop(self):
        self.troop += 1

    def removeTroop(self):
        if self.troop > 1:
            self.troop -= 1

    def isNeighbor(self,other):
        return (other.msg in self.neighbors)

    def update(self):
        super(State,self).update()
        self.troop_surface=self.font.render(str(self.troop),True,self.textColor)
        
    def draw(self,screen):
        # draws circle button
        self.update()
        pygame.draw.circle(screen,self.color,self.center,self.r)

        highlight = (0,0,0)
        # draws the highlight ring
        if self.selected:
            pygame.draw.circle(screen,highlight,self.center,self.r,5)
        # draws statename
        screen.blit(self.name_surface,self.name_rect)
        # displays num troop
        screen.blit(self.troop_surface,self.troop_rect)

class Die(Button):
    def __init__(self,x,y,msg,font,textcolor,length,height,
        buttonColor,hoverColor):
        super(Die,self).__init__(x,y,msg,font,textcolor,length,height,\
        buttonColor,hoverColor)

    def roll(self):
        self.msg = str(random.randint(1,6))

    def update(self):
        super(Die,self).update()
        # update die value
        self.surface = self.font.render(self.msg,True,self.textColor)

    def draw(self,screen):
        self.update()
        super(Die,self).draw(screen)
###########################################
################# Players #################
###########################################
class Player(pygame.sprite.Sprite):
    def __init__(self,img,color,mobileTroop=25):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (65,65)
        self.territory = []
        self.color = color

        black = 0,0,0
        self.mobileTroop = mobileTroop
        self.font = pygame.font.Font('freesansbold.ttf',25)
        self.troopSurface = self.font.render(str(self.mobileTroop),True,black)
        self.troopRect = self.troopSurface.get_rect()
        self.troopRect.center = (65,160)

        self.gotTroop = False
        self.selectedState = None

        white = 255,255,255
        self.end = Button(65,220,"End Turn",self.font,black,
                        140,60,self.color,white)

        self.stat = TextObjs(x=65,y=300,msg='Territory: ',
            font=self.font,textColor=black) # to do

        self.result = TextObjs(x=1080,y=150,msg='-',
            font=self.font,textColor=black)

    def claim(self,other):
        if other.troop == 0 and self.mobileTroop!=0:
            other.buttonColor = self.color
            other.troop += 1
            other.claimed = True
            self.mobileTroop -= 1
            self.territory.append(other)

    def contain(self,listState):
        stateNames = []
        for state in self.territory:
            stateNames.append(state.msg)

        for state in listState:
            if state not in stateNames:
                return False
        return True

    def getTroop(self):
        
        if len(self.territory) <= 9:
            self.mobileTroop = 3
        else: 
            self.mobileTroop = len(self.territory) / 3

            global dkblueNames,yellowNames,redNames,\
            ltblueNames,dkoliveNames,dkgreenNames

            if self.contain(dkblueNames):
                self.mobileTroop += 3

            if self.contain(yellowNames):
                self.mobileTroop += 7

            if self.contain(redNames):
                self.mobileTroop += 5

            if self.contain(ltblueNames):
                self.mobileTroop += 2

            if self.contain(dkoliveNames):
                self.mobileTroop += 7

            if self.contain(dkgreenNames):
                self.mobileTroop += 7

    def addTroop(self,state):
        if self.mobileTroop > 0:
            state.addTroop()
            self.mobileTroop -= 1

    def removeTroop(self,state):
        if state.troop > 1:
            state.removeTroop()
            self.mobileTroop += 1

    def attack(self,other,board):
        board.resetDice()

        if self.selectedState.troop>=2:
            if self.selectedState.troop==2:
                board.rollAttDice(1)
            elif self.selectedState.troop==3:
                board.rollAttDice(2)
            else:
                board.rollAttDice(3)

            if other.troop == 1:
                board.rollDefDice(1)
            elif other.troop >= 2:
                board.rollDefDice(2)

            outcome = board.compareDice()

            if outcome == "Win":
                if other.troop <= 2:
                    other.troop = 0
                else:
                    other.troop -= 2
            elif outcome == "Tie":
                self.selectedState.troop -= 1
                other.troop -= 1
            else:
                if other.troop == 1:
                    self.selectedState.troop -= 1
                else:
                    self.selectedState.troop -= 2

            self.result.msg = outcome

    def conquer(self,other):
        if self.selectedState.troop > 1:
            self.selectedState.troop -= 1
            other.troop += 1
            other.buttonColor = self.color
            self.territory.append(other)

    def lose(self,state):
        self.territory.remove(state)

    def update(self):
        black = 0,0,0
        self.troopSurface = self.font.render(str(self.mobileTroop),
                                                True,black)
        self.result.update()
        
        self.stat.msg = "Territory: " + str(len(self.territory))
        self.stat.update()

    def checkWon(self,board):
        return len(self.territory) == len(board.states)

    def draw(self,screen):
        self.update()
        white = 255,255,255
        # draws the img
        pygame.draw.rect(screen,white,self.rect)
        screen.blit(self.img,self.rect)
        pygame.draw.rect(screen,self.color,self.rect,5)
        # draws mobiletroop
        screen.blit(self.troopSurface,self.troopRect)
        # draws end button
        self.end.draw(screen)
        # draws match result
        self.result.draw(screen)
        # draws state
        self.stat.draw(screen)

class Icon(pygame.sprite.Sprite):
    def __init__(self,img,x,y,edgeColor):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.length = self.img.get_width()
        self.height = self.img.get_height()
        self.edgeColor = edgeColor

    def mouseOver(self):
        pos = pygame.mouse.get_pos()
        left = self.rect.center[0] - self.length/2
        top = self.rect.center[1] - self.height/2
        if (left <= pos[0] <= left + self.length) and \
        (top <= pos[1] <= top + self.height):
            return True
        else:
            return False

    def leftClick(self):
        return self.mouseOver() and pygame.mouse.get_pressed()[0] == 1

    def draw(self,screen):
        # draws frame if mouseOver:
        if self.mouseOver():
            left = self.rect.center[0] - self.length/2
            top = self.rect.center[1] - self.height/2
            pygame.draw.rect(screen,self.edgeColor,
                            (left,top,self.length,self.height),5)
        # draws img
        screen.blit(self.img,self.rect)
###########################################
############### Transition ################
###########################################
class Transition(pygame.sprite.Sprite):
    def iconInit(self):
        waterImg = pygame.image.load("Images/Waterbending.png")
        blue = 13,37,114
        water = {'img':waterImg,'edgeColor':blue}

        earthImg = pygame.image.load("Images/Earthbending.png")
        green = 30,104,52
        earth = {'img':earthImg,'edgeColor':green}
        
        fireImg = pygame.image.load("Images/Firebending.png")
        red = 255,0,0
        fire = {'img':fireImg,'edgeColor':red}
        
        airImg = pygame.image.load("Images/Airbending.png")
        ltblue = 113,204,211
        air = {'img':airImg,'edgeColor':ltblue}
        
        wlImg = pygame.image.load("Images/White Lotus.png")
        grey = 35,31,32
        wl = {'img':wlImg,'edgeColor':grey}

        emblems = [water,earth,fire,air,wl]
        margin = 100
        imgWidth = 120
        y = 5*self.height/8
        
        for i in xrange(len(emblems)):
            emblem = emblems[i]
            x = (i+1) * (margin + imgWidth/2) + (i*imgWidth/2)
            newIcon = Icon(img=emblem['img'],x=x,y=y,
                    edgeColor=emblem['edgeColor'])
            self.icons.append(newIcon)

    def __init__(self,width,height,title):
        self.width = width
        self.height = height
        lgfont = pygame.font.Font('freesansbold.ttf',50)
        textColor = 0,0,0 # black

        self.playerCount = 1

        if title == "Choose Player ":
            newTitle = title + str(self.playerCount)
            self.title = TextObjs(x=self.width/2,y=3*self.height/8,msg=newTitle,
                font=lgfont,textColor=textColor)
        else:
            self.title = TextObjs(x=self.width/2,y=3*self.height/8,msg=title,
                font=lgfont,textColor=textColor)

        
        self.icons = []
        self.iconInit()
        
        smfont = pygame.font.Font('freesansbold.ttf',25)
        buttonColor = 80,125,225# ltblue
        hoverColor = 0,51,102# dkblue
        self.go = Button(x=2*self.width/3,y=10*self.height/12,
            msg='Go!',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

        self.back = Button(x=1*self.width/3,y=10*self.height/12,
            msg='Back',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

        self.backReminder = TextObjs(x=self.width/3-self.width/8,
            y=1*self.height/8,msg="",font=smfont,textColor=buttonColor)
        self.goReminder = TextObjs(x=2*self.width/3-self.width/8,
            y=1*self.height/8,msg="",font=smfont,textColor=hoverColor)
    
    def update(self):
        if self.title.msg.startswith("Choose Player"):
            if self.playerCount == 6:
                self.title.msg = "Click Go!"
            else:
                self.title.msg = "Choose Player " + str(self.playerCount)
        else:
            if self.playerCount == 1:
                self.title.msg = "Choose Your Emblem"
            elif self.playerCount == 6:
                self.title.msg = "Click Go!"
            else:
                self.title.msg = "Choose A.I. " + str(self.playerCount-1)
        self.title.update()
        self.backReminder.update()
        self.goReminder.update()

    def display(self,screen):
        # draw title
        self.update()
        self.title.draw(screen)

        # draw icons
        for icon in self.icons:
            icon.draw(screen)

        # draw button
        self.go.draw(screen)
        self.back.draw(screen)

        # draw reminder
        if self.backReminder.msg!="":
            self.backReminder.draw(screen)

        if self.goReminder.msg!="":
            self.goReminder.draw(screen)

class EndMenu(Transition):
    def __init__(self,width,height,title):
        
        self.width = width
        self.height = height
        lgfont = pygame.font.Font('freesansbold.ttf',50)
        textColor = 0,0,0 # black

        self.title = TextObjs(x=self.width/2,y=3*self.height/8,msg=title,
            font=lgfont,textColor=textColor)

        self.img = None

        smfont = pygame.font.Font('freesansbold.ttf',25)
        buttonColor = 80,125,225# ltblue
        hoverColor = 0,51,102# dkblue
        
        self.exit = Button(x=2*self.width/3,y=11*self.height/12,
            msg='exit',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

        self.restart = Button(x=1*self.width/3,y=11*self.height/12,
            msg='restart',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def display(self,screen):
        # draw title
        self.title.draw(screen)
        # draw winner img
        screen.blit(self.img,(self.width/2,self.height/2))

        # draw button
        self.exit.draw(screen)
        self.restart.draw(screen)

class OptionMenu(pygame.sprite.Sprite):
    def __init__(self,width,height,title):
        self.width = width
        self.height = height
        lgfont = pygame.font.Font('freesansbold.ttf',50)
        textColor = 0,0,0 # black

        self.title = TextObjs(x=self.width/2,y=3*self.height/8,msg=title,
            font=lgfont,textColor=textColor)

        lgfont = pygame.font.Font('freesansbold.ttf',50)
        textColor = 0,0,0 # black
        self.title = TextObjs(x=self.width/2,y=3*self.height/8,msg=title,
            font=lgfont,textColor=textColor)

        smfont = pygame.font.Font('freesansbold.ttf',25)
        buttonColor = 80,125,225# ltblue
        hoverColor = 0,51,102# dkblue
        
        self.back = Button(x=2*self.width/3,y=10*self.height/12,
            msg='back',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

        self.music = Button(x=1*self.width/3,y=10*self.height/12,
            msg='music',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def display(self,screen):
        self.title.draw(screen)

        self.back.draw(screen)
        self.music.draw(screen)

class Tutorial(pygame.sprite.Sprite):
    def textInit(self):
        smfont = pygame.font.Font('freesansbold.ttf',25)
        textColor = 0,0,0

        t0 = ['Player are given 30 reinforcements at the beginning of the game.',
        'Player will then claim territory by clicking on the empty state.',
        'After all states on board are taken, the game enter stage 2']

        for i in xrange(len(t0)):
            text = t0[i]
            newText = TextObjs(x=self.width/2, y=(3+i)*self.height/8,msg=text,
            font=smfont,textColor=textColor)
            self.text0.append(newText)

        t1 = ['In stage 2, player will receive reinforcement based on their territory.',
        'If player has less than 3 states, he/she will receive 3 by default.', 
        'If player has more than 3 states, he/she will receive however',
        'many states he/she owns divided by 3,', 
        'and additional reinforcements if he/she owns an continent.']

        for i in xrange(len(t1)):
            text = t1[i]
            newText = TextObjs(x=self.width/2, y=(1+i)*self.height/8,msg=text,
            font=smfont,textColor=textColor)
            self.text1.append(newText)

        t2 = ['In each turn, player must first locate his/her reforcement before attacking.', 
        'Left click to place troop down, right click to withdraw troop from selected state.',
        'To attack, a player must first select a state he/she wants to use,',
        'then click on the state he/she wants to conquer.']

        for i in xrange(len(t2)):
            text = t2[i]
            newText = TextObjs(x=self.width/2, y=(2+i)*self.height/8,msg=text,
            font=smfont,textColor=textColor)
            self.text2.append(newText)
        
    def __init__(self,width,height,title):
        self.width = width
        self.height = height
        lgfont = pygame.font.Font('freesansbold.ttf',50)
        textColor = 0,0,0 # black
        self.title = TextObjs(x=self.width/2,y=2*self.height/8,msg=title,
            font=lgfont,textColor=textColor)

        smfont = pygame.font.Font('freesansbold.ttf',25)
        buttonColor = 80,125,225 # ltblue
        hoverColor = 0,51,102 # dkblue

        self.phase = 0

        self.text0 = []
        self.text1 = []
        self.text2 = []

        self.textInit()

        self.back = Button(x=1*self.width/3,y=10*self.height/12,
            msg='back',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

        self.next = Button(x=2*self.width/3,y=10*self.height/12,
            msg='next',font=smfont,textcolor=textColor,
            length=self.width/4,height=self.height/12,
            buttonColor=buttonColor,hoverColor=hoverColor)

    def display(self,screen):
        if self.phase == 0:
            self.title.draw(screen)
            for exp in self.text0:
                exp.draw(screen)

        elif self.phase == 1:
            for exp in self.text1:
                exp.draw(screen)

        elif self.phase == 2:
            for exp in self.text2:
                exp.draw(screen)

        self.back.draw(screen)
        if self.phase != 2:
            self.next.draw(screen)
#################################################
################### main ########################
#################################################
def main():
    pygame.init()

    size = (width,height) = 1200,720
    white = 255,255,255
    black = 0,0,0

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    players = []
    board = Board()
    Risk = True
    Music = True
    pygame.mixer.music.load("Legend of Korra Soundtrack.mp3")

    startMenu = StartMenu(width,height)
    inStartMenu = True

    transition = Transition(width,height,"Choose Player ")
    inTransition = False

    option = OptionMenu(width,height,"Option")
    inOption = False

    tutorial = Tutorial(width,height,"Tutorial")
    inTutorial = False
    
    board = Board()
    gamePlay = False
    stage1 = True
    stage2 = False
    winner = None
    
    endMenu = EndMenu(width,height,"The Winner is:")
    endScreen = False

    while Risk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if Music:
            pygame.mixer.music.play(-1)

        while inStartMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(white)
            startMenu.display(screen)

            for button in startMenu.buttons:
                if button.leftClick():

                    if button.msg == 'Multi Player Mode' or \
                        button.msg == 'Single Player Mode':
                        inTransition = True

                    if button.msg == "Option":
                        inOption = True

                    if button.msg == "Tutorial":
                        inTutorial = True

                    inStartMenu = False
                    pygame.time.wait(200)

            pygame.display.update()
            clock.tick(30)

        while inOption:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(white)
            option.display(screen)

            if option.back.leftClick():
                inOption = False
                inStartMenu = True
                pygame.time.wait(200)

            if option.music.leftClick():
                pygame.time.wait(200)

                if Music == True:
                    pygame.mixer.music.stop()
                    Music = False
                elif Music == False:
                    pygame.mixer.music.play()
                    Music = True
                
            pygame.display.update()
            clock.tick(30)

        while inTutorial:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.fill(white)
            tutorial.display(screen)

            if tutorial.back.leftClick():
                if tutorial.phase == 0:
                    inStartMenu = True
                    inTutorial = False
                else:
                    tutorial.phase -= 1
                pygame.time.wait(200)

            if tutorial.next.leftClick():
                if 0<=tutorial.phase <=1:
                    tutorial.phase += 1
                pygame.time.wait(200)

            pygame.display.update()
            clock.tick(30)

        while inTransition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(white)

            transition.go.update()
            transition.display(screen)

            for icon in transition.icons:
                if icon.leftClick():
                    newPlayer = Player(img=icon.img,color=icon.edgeColor)
                    players.append(newPlayer)
                    transition.icons.remove(icon)
                    transition.playerCount += 1

            transition.backReminder.msg = ""
            transition.goReminder.msg = ""

            if transition.go.mouseOver():
                msg = "This will start the game"
                transition.goReminder.msg = msg

            if len(players) >= 2 and transition.go.leftClick():
                inTransition = False
                gamePlay = True
            
            if transition.back.mouseOver():
                msg = "This will clear all selected player"
                transition.backReminder.msg = msg
                # print transition.backReminder.msg

            if transition.back.leftClick():
                inTransition = False
                transition = Transition(width,height,"Choose Player ")
                inStartMenu = True
                players = []

            pygame.display.update()
            clock.tick(30)

        while gamePlay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            while stage1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                
                screen.fill(white)
                board.draw(screen)
                i = 0
                
                while i < len(players):
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()

                    screen.fill(white)
                    board.draw(screen)
                    player = players[i]
                    player.draw(screen)

                    for state in board.states:
                        if state.leftClick():
                            pygame.time.wait(100)
                            if state.claimed == False:
                                player.claim(state)
                                i += 1
                            else:
                                if state in player.territory:
                                    player.addTroop(state)
                                    i += 1

                    pygame.display.update()
                    clock.tick(30)

                lastPlayer = players[len(players)-1]
                if lastPlayer.mobileTroop == 0:
                    stage1 = False
                    stage2 = True

                pygame.display.update()
                clock.tick(30)

            while stage2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                
                screen.fill(white)
                board.draw(screen)
                i = 0

                while i < len(players):
                    player = players[i]

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

                    if len(player.territory) == 0:
                        player.gotTroop = True
                        i += 1
                        players.remove(player)

                    if player.gotTroop == False:
                        player.getTroop()
                        player.gotTroop = True

                    for state in board.states:
                        if state.leftClick():
                            pygame.time.wait(100)
                            if player.mobileTroop != 0:
                                if state in player.territory:
                                    player.addTroop(state)
                            else:
                                if state in player.territory:
                                    if player.selectedState == None:
                                        state.selected = True
                                        player.selectedState = state
                                        pygame.time.wait(100)
                                    else:
                                        if player.selectedState.msg == state.msg:
                                            state.selected = False
                                            player.selectedState = None
                                        else:
                                            player.selectedState.selected = False
                                            state.selected = True
                                            player.selectedState = state
                                
                                else:
                                    if player.selectedState == None:
                                        pass

                                    else:
                                        if state.claimed == True:
                                            if player.selectedState.isNeighbor(state):
                                                stateowner = board.findOwner(state,players)
                                                player.attack(state,board)
                                                if state.troop == 0:
                                                    player.conquer(state)
                                                    stateowner.lose(state)
                                                    player.selectedState.selected = False
                                                    player.selectedState = None
                                            else:
                                                print "you can't do that!"

                        if state.rightClick():
                            pygame.time.wait(100)
                            if state in player.territory:
                                player.removeTroop(state)

                    if player.mobileTroop == 0 and player.end.leftClick():
                        i += 1
                        player.gotTroop = False
                        board.resetDice()
                        if player.selectedState != None:
                            player.selectedState.selected = False
                            player.selectedState = None

                    if player.checkWon(board) == True:
                        stage2 = False
                        gamePlay = False
                        endScreen = True
                        winner = player
                        break

                    screen.fill(white)
                    board.draw(screen)
                    player.draw(screen)

                    pygame.display.update()
                    clock.tick(30)

        while endScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(white)
            endMenu.img = winner.img
            endMenu.display(screen)
            
            if endMenu.exit.leftClick():
                pygame.quit()
                quit()

            if endMenu.restart.leftClick():
                inStartMenu = True
                stage1 = True
                endScreen = False
                board = Board()
                players = []
                transition = Transition(width,height,"Choose Player ")

            pygame.display.update()
            clock.tick(30)