import random
import pygame
import tutorial as t
import menu as men
import time
import save as s
pygame.init()
gamebg=pygame.image.load('data/bg.jpg')
lasersound=pygame.mixer.Sound('data/laser.wav')
hitsound=pygame.mixer.Sound('data/hit.wav')

seccount=0
totaltestseconds=0

screenbreite=700
screenhoehe=550
shootloop=0
alienkills=0
level=1
spaceshipkills=0
colorcounter=0
timee=''
ru=True
pausebutton=False
show1=True
spawnaliens=True
clock=pygame.time.Clock()
addalien=False

powerups=[['double shooting ability',False,False,'allows you to have twice as much lasers as normal on screen'],
          ['half alien velocity',False,False,'slows down the aliens or the spaceship'],
          ['double laser damage',False,False,'your lasers do twice as much damage as normal'],
          ['double cannons',False,False,'allows you to have two cannons on your spaceship'],
          ['Health Boost',False,False,'replenishes your health by 1/5']]

holdingpowerup=False
usepowerup=False
poweruploop=0

aliennumber=2
alienhealth=10
alienlaserdamage=1
alienvelocity=1.3


yellow=(255,255,0)
black=(0,0,0)
white=(255,255,255)
grey=(150,150,150)
red=(255,0,0)
green=(0,222,0)

color=green

class spaceship:
    def __init__(self,x,y,breite,hoehe):
        self.x=x
        self.y=y
        self.vel=5
        self.breite=110
        self.hoehe=hoehe
        self.health=200
        self.hitbox=(self.x,self.y,self.breite,self.hoehe)
        self.visible=True

    def draw(self,win):
        global powerups
        global usepowerup

        if powerups[4][2]:
            self.health+=40
            if self.health>200:
                self.health=200
            powerups[4][2]=False
            usepowerup=False
        
        pygame.draw.rect(win,grey,(self.x+20,self.y,70,50))
        pygame.draw.rect(win,yellow,(self.x+90,self.y+15,20,35))
        pygame.draw.rect(win,yellow,(self.x,self.y+15,20,35))

        if powerups[3][2]:
            pygame.draw.rect(win,white,(self.x+round(self.breite/2)+5,self.y-20,10,20))
            pygame.draw.rect(win,white,(self.x+round(self.breite/2)-15,self.y-20,10,20))

        else:
            pygame.draw.rect(win,white,(self.x+round(self.breite/2)-5,self.y-20,10,20))

        self.hitbox=(self.x,self.y,self.breite,self.hoehe)

    def fire(self):
        global powerups
        if powerups[0][2]:
            le=10
        else:
            le=5
        if len(lasers)<le: 
            if men.soundchoose.get_tof():
                lasersound.set_volume(men.soundbar.get_Volume())
                lasersound.play()

            if powerups[3][2]:
                lasers.append(laser(self.x+round(self.breite/2)+9,470,yellow))
                lasers.append(laser(self.x+round(self.breite/2)-11,470,yellow))
            else:
                lasers.append(laser(self.x+round(self.breite/2)-1,470,yellow))


    def drawHealthBar(self,win):
        font1=pygame.font.SysFont('comicsans',30)
        text=font1.render('Health:',1,white)
        win.blit(text,(5,5))
        if self.health>0:
            pygame.draw.rect(win,red,(15+text.get_width(),round(text.get_height()/2),round(self.health/2),10))

    def hit(self):
        global alienlaserdamage
        self.health-=alienlaserdamage
        hitsound.play()

class enemyAlien:
    walkRight=[pygame.image.load('data/R1E.png'),pygame.image.load('data/R2E.png'),pygame.image.load('data/R3E.png'),pygame.image.load('data/R4E.png'),pygame.image.load('data/R5E.png'),
               pygame.image.load('data/R6E.png'),pygame.image.load('data/R7E.png'),pygame.image.load('data/R8E.png'),pygame.image.load('data/R9E.png'),pygame.image.load('data/R10E.png'),
               pygame.image.load('data/R11E.png')]

    walkLeft=[pygame.image.load('data/L1E.png'),pygame.image.load('data/L2E.png'),pygame.image.load('data/L3E.png'),pygame.image.load('data/L4E.png'),pygame.image.load('data/L5E.png'),
              pygame.image.load('data/L6E.png'),pygame.image.load('data/L7E.png'),pygame.image.load('data/L8E.png'),pygame.image.load('data/L9E.png'),
              pygame.image.load('data/L10E.png'),pygame.image.load('data/L11E.png')]

    
    def __init__(self,x,y,health,vel):
        self.x=x
        self.y=y
        self.health=health
        self.path=[64,634]
        self.walkCount=0
        self.hitbox=(self.x+17,self.y+2,31,57)
        self.breite=self.hitbox[2]
        self.vel=vel
        self.visible=True
        self.lasercount=0

    def move(self):
        global powerups
            
        if self.vel>0:
            if powerups[1][2]:
                e=self.vel/2
            else:
                e=self.vel
            if self.x+self.vel<self.path[1]-self.hitbox[2]:
                self.x+=e
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if powerups[1][2]:
                e=self.vel/2
            else:
                e=self.vel
            if self.x-self.vel>self.path[0]:
                self.x+=e
            else:
                self.vel=self.vel*-1
                self.walkCount=0

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount+1>=33:
                self.walkCount=0

            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//6],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//6],(self.x,self.y))
                self.walkCount+=1

            if self.vel>0:
                self.hitbox=(self.x+14,self.y+2,31,57)
            else:
                self.hitbox=(self.x+23,self.y+2,31,57)
            self.drawHealthBar(win)

            self.fire()

    def drawHealthBar(self,win):
        y=self.hitbox[1]-10
        healthfont=pygame.font.SysFont('arial',20)
        text=healthfont.render(str(self.health),1,red)
        win.blit(text,(self.hitbox[0]+(self.hitbox[2]/2),y))
            
        

    def fire(self):
        if self.lasercount==0:
            if men.soundchoose.get_tof():
                lasersound.set_volume(men.soundbar.get_Volume())
                lasersound.play()
            enemylasers.append(laser(self.x+round(self.breite/2)+15,self.y+8,green))
            self.lasercount=1

        else:
            self.lasercount+=1
            if self.lasercount>66:
                self.lasercount=0


    def hit(self):
        hitsound.play()

        global powerups
        if powerups[2][2]:
            self.health-=2
        else:
            self.health-=1
        
class laser:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.width=3
        self.height=30
        self.color=color
        self.vel=4
        self.visible=True

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))

class enemyspaceship:
    def __init__(self):
        self.x=150
        self.y=70
        self.breite=110
        self.vel=3
        self.hoehe=50
        self.health=50
        self.path=[64,634]
        self.hitbox=(self.x,self.y,self.breite,self.hoehe)
        self.lasercount=0
        self.showrage=True

    def draw(self,win):
        global colorcounter
        global color
        
        if self.health<26:
            colorcounter+=1
            if colorcounter>30:
                colorcounter=0
                if color==green:
                    color=red
                else:
                    color=green

        else:
            color=green

        pygame.draw.rect(win,grey,(self.x+20,self.y,70,50))
        if color==red:
            ef=pygame.font.SysFont('comicsansms',35)
            text=ef.render('2x',1,red)
            win.blit(text,(self.x+33,self.y-2))
        pygame.draw.rect(win,color,(self.x+90,self.y,20,35))
        pygame.draw.rect(win,color,(self.x,self.y,20,35))
        pygame.draw.rect(win,white,(self.x+round(self.breite/2)-5,self.y+50,10,20))

        self.hitbox=(self.x,self.y,self.breite,self.hoehe)

        self.drawHealthBar(win)
        self.move()
        self.fire()

    def move(self):
        if self.vel>0:
            if powerups[1][2]:
                self.vel=1.5
            else:
                self.vel=3
            if self.x+self.vel<self.path[1]-self.hitbox[2]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
        else:
            if powerups[1][2]:
                self.vel=-1.5
            else:
                self.vel=-3
            if self.x-self.vel>self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1

    def fire(self):
        if self.health>25:
            seq=66
        else:
            seq=33   
        if self.lasercount==0:
            if men.soundchoose.get_tof():
                lasersound.set_volume(men.soundbar.get_Volume())
                lasersound.play()

            if self.vel>0:
                laserx=self.x+round(self.breite/2)+13
            else:
                laserx=self.x+round(self.breite/2)-13
            enemylasers.append(laser(laserx,self.y+8,green))
            self.lasercount=1

        else:
            self.lasercount+=1
            if self.lasercount>seq:
                self.lasercount=0

    def hit(self):
        hitsound.play()
        self.health-=1

    def drawHealthBar(self,win):
        y=self.hitbox[1]-10
        healthfont=pygame.font.SysFont('arial',20)
        text=healthfont.render(str(self.health),1,red)
        win.blit(text,(round((self.hitbox[0]+(self.hitbox[2]/2))-round(text.get_width()/2)),y-10))

###########################################################################################
###########################################################################################

def showLevel(win,level,msg):
    lvlfont=pygame.font.SysFont('comicsans',50)
    text=lvlfont.render('Level: '+str(level),1,white)
    win.blit(text,(350-round(text.get_width()/2),275))

    msgfont=pygame.font.SysFont('comicsans',30)
    text=msgfont.render(msg,1,white)
    win.blit(text,(350-round(text.get_width()/2),315))

    pygame.display.update()
    time.sleep(3)

def generateLevel(win,number):
    global powerups
    global addalien
    global level
    global aliennumber
    global alienhealth
    global alienlaserdamage
    global alienvelocity
    global spawnaliens
    global seccount
    global totaltestseconds

    global levelcounter

    if number==1:
        global level
        level=0
        alienkills=0
        spaceshipkills=0
        levelcounter=1
        global battleship
        global show1
        show1=True
        battleship=spaceship(150,490,70,50)
        global addalien
        addalien=False
        aliennumber=2
        alienhealth=10
        alienlaserdamage=2
        alienvelocity=1.3


    if levelcounter==2:
        alienhealth+=5
        showLevel(win,level+1,'Alien health +5')
    elif levelcounter==3:
        alienlaserdamage+=2
        showLevel(win,level+1,'Alien laser damage +2')
    elif levelcounter==4:
        alienvelocity+=0.1
        showLevel(win,level+1,'Alien velocity +0.1')
    elif levelcounter==5:
        showLevel(win,level+1,'Enemy spaceship attacks')
        levelcounter=0
        spawnaliens=False
    elif levelcounter==1 and number!=1:
        for p in powerups:
            if p[1]:
                p[1]=False
        a=random.randint(0,len(powerups)-1)
        powerups[a][1]=True

        newpfont=pygame.font.SysFont('comicsans',50)
        newtext=newpfont.render('New Powerup: '+powerups[a][0],1,white)
        win.blit(newtext,(350-round(newtext.get_width()/2),225))

        exfont=pygame.font.SysFont('comicsans',30)
        textex=exfont.render(powerups[a][3],1,white)
        win.blit(textex,(350-round(textex.get_width()/2),295))

        pygame.display.update()
        time.sleep(3)
        redrawGameWindow(win)
        
        if addalien:
            aliennumber+=1
            showLevel(win,level+1,'Alien number +1')
            addalien=False
        else:
            alienlaserdamage+=2
            showLevel(win,level+1,'Alien laser damage +2')
            addalien=True

    if spawnaliens:
        alieny=70
        alienx=64
        for e in range(aliennumber):
            aliens.append(enemyAlien(alienx,alieny,alienhealth,alienvelocity))
            alieny+=72
            if alienx==64:
                alienx=634
            elif alienx==634:
                alienx=349
            else:
                alienx=64
                
    else:
        enemyspaceships.append(enemyspaceship())
        spawnaliens=True
    levelcounter+=1
    level+=1

###########################################################################################
###########################################################################################

def gameover(win):
    global alienkills
    global spaceshipkills
    global totaltestseconds
    global level
    global aliens
    global lasers
    global enemylasers
    global timee
    pygame.mixer.music.stop()
    helplevel=level
    
    ptime=calculateTime()
    if int(ptime[1])<10:
        timee=ptime[0]+':0'+ptime[1]
    else:
        timee=ptime[0]+':'+ptime[1]
        
    generateLevel(win,1)
    print(str(helplevel))
    print(str(s.readlevel()))
    if helplevel>s.readlevel():
        s.save(helplevel,alienkills,spaceshipkills,timee,totaltestseconds)
        highscoreloop=True
        hslo=0
        ybutton=370
    elif helplevel==s.readlevel() and totaltestseconds>s.readseconds():
        s.save(helplevel,alienkills,spaceshipkills,timee,totaltestseconds)
        highscoreloop=True
        hslo=0
        ybutton=370
    else:
        highscoreloop=False
        ybutton=350
    
    f=True
    g=True
    h=True
    while f:
        try:
            aliens.pop()
        except:
            f=False
    while g:
        try:
            lasers.pop()
        except:
            g=False
    while h:
        try:
            enemylasers.pop()
        except:
            h=False
            
    gaov=True
    while gaov:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                ptime=calculateTime()
                if int(ptime[1])<10:
                    timee=ptime[0]+':0'+ptime[1]
                else:
                    timee=ptime[0]+':'+ptime[1]
                return 0
        pygame.draw.rect(win,yellow,(50,75,600,400))
        pygame.draw.rect(win,black,(60,85,580,380))
        
        gameoverfont=pygame.font.SysFont('comicsansms',50)
        text=gameoverfont.render('Game Over!',1,yellow)
        win.blit(text,(350-round(text.get_width()/2),80))

        statfont=pygame.font.SysFont('comicsans',30)

        text=statfont.render('Level: '+str(helplevel),1,white)
        win.blit(text,(350-round(text.get_width()/2),160))
        
        text=statfont.render('Aliens killed: '+str(alienkills),1,white)
        win.blit(text,(350-round(text.get_width()/2),190))

        text=statfont.render('Enemy spaceships destroyed: '+str(spaceshipkills),1,white)
        win.blit(text,(350-round(text.get_width()/2),220))

        if highscoreloop:
            hslo+=1
            if hslo<15:
                highfont=pygame.font.SysFont('comicsansms',40)
                text=highfont.render('New Highscore!',1,yellow)
                win.blit(text,(350-round(text.get_width()/2),290))
            elif hslo==30:
                hslo=0
                
        text=statfont.render('Survived time: '+timee,1,white)
        win.blit(text,(350-round(text.get_width()/2),250))

        exbutton=t.button(win,'Main Menu',250,ybutton,200,50,yellow,black,yellow)
        if exbutton:
            return 1
        
        pygame.display.update()

def calculateTime():
    global totaltestseconds
    minutes=totaltestseconds//60
    seconds=totaltestseconds%60

    return [str(minutes),str(seconds)]

def pause(win):
    global timee
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            ptime=calculateTime()
            if int(ptime[1])<10:
                timee=ptime[0]+':0'+ptime[1]
            else:
                timee=ptime[0]+':'+ptime[1]
            return 0
    
    pygame.draw.rect(win,yellow,(150,115,400,320))
    pygame.draw.rect(win,black,(160,125,380,300))

    paufont=pygame.font.SysFont('comicsansms',50)
    text=paufont.render('Paused',1,yellow)
    win.blit(text,(350-round(text.get_width()/2),120))

    notefont=pygame.font.SysFont('comicsansms',15)
    text=notefont.render('NOTE: if you quit, you can go back to the current',1,yellow)
    win.blit(text,(170,320))
    text=notefont.render('save by just starting the game via the main menu.',1,yellow)
    win.blit(text,(170,340))
    text=notefont.render('If you close the whole game with an unfinished save,',1,yellow)
    win.blit(text,(170,360))
    text=notefont.render('it will be saved regularly but you wont be able to',1,yellow)
    win.blit(text,(170,380))
    text=notefont.render('finish it.',1,yellow)
    win.blit(text,(170,400))

    resumebutton=t.button(win,'Resume',250,200,200,50,yellow,black,yellow)
    if resumebutton:
        return 1

    quitbutton=t.button(win,'Quit',250,260,200,50,yellow,black,yellow)
    if quitbutton:
        ptime=calculateTime()
        if int(ptime[1])<10:
            timee=ptime[0]+':0'+ptime[1]
        else:
            timee=ptime[0]+':'+ptime[1]
        return 0

    pygame.display.update()

###########################################################################################
###########################################################################################
        
def redrawGameWindow(win):
    global powerups
    global battleship
    global alienkills
    global spaceshipkills
    global pausebutton
    global holdingpowerup
    global usepowerup
    global poweruploop
    
    win.blit(gamebg,(0,0))

    lvlfont=pygame.font.SysFont('comicsans',30)
    text=lvlfont.render('Level: '+str(level),1,white)
    win.blit(text,(350-round(text.get_width()/2),5))

    text=lvlfont.render('Powerups: ',1,white)
    win.blit(text,(5,25))

    for powerup in powerups:
        if powerup[1]==True:
            textp=lvlfont.render(powerup[0],1,white)
            win.blit(textp,(text.get_width()+5,25))
            holdingpowerup=True

    if holdingpowerup:
        usebutton=t.button(win,'Use',5+text.get_width()+textp.get_width()+20,25,45,20,yellow,black,yellow)
        if usebutton:
            holdingpowerup=False
            usepowerup=True

    if usepowerup:
        for powerup in powerups:
            if powerup[1]==True:
                powerup[1]=False
                powerup[2]=True

    for powerup in powerups:
        if powerup[2]:
            textp=lvlfont.render(powerup[0],1,white)
            win.blit(textp,(text.get_width()+5,25))
            poweruploop+=1
            if poweruploop==720:
                poweruploop=0
                powerup[2]=False
                usepowerup=False

    if not holdingpowerup and not usepowerup:
        textp=lvlfont.render('None',1,white)
        win.blit(textp,(text.get_width()+5,25))
        
    
    pausebutton=t.button(win,'Pause',625,10,65,30,yellow,black,yellow)
    
    keys=pygame.key.get_pressed()
    if pausebutton or keys[pygame.K_ESCAPE]:
        pause(win)

    for laser in lasers:
        laser.draw(win)

    for laser in enemylasers:
        laser.draw(win)

    for alien in aliens:
        if alien.health>0:
            alien.draw(win)
        else:
            aliens.pop(aliens.index(alien))
            alienkills+=1

    for v in enemyspaceships:
        if v.health>0:
            v.draw(win)
        else:
            enemyspaceships.pop()
            spaceshipkills+=1
            

    if battleship.visible:    
        battleship.draw(win)
    battleship.drawHealthBar(win)

    pygame.display.update()
    
battleship=spaceship(150,490,70,50)
clock=pygame.time.Clock()
lasers=[]
enemylasers=[]
aliens=[]
enemyspaceships=[]

def run(win):
    global alienkills
    global spaceshipkills
    global battleship
    global ru
    global seccount
    global pausebutton
    global totaltestseconds
    global timee
    clock.tick(60)

    seccount+=1
    if seccount==60:
        totaltestseconds+=1
        seccount=0

    redrawGameWindow(win)
    
    global show1
    if show1:
        alienkills=0
        spaceshipkills=0
        generateLevel(win,1)
        showLevel(win,level,'')
        totaltestseconds=0
        seccount=1
        show1=False
        
    global shootloop
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            ptime=calculateTime()
            if int(ptime[1])<10:
                timee=ptime[0]+':0'+ptime[1]
            else:
                timee=ptime[0]+':'+ptime[1]
            return 0

    if battleship.visible:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if battleship.x>battleship.vel:
                battleship.x-=battleship.vel

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if battleship.x<screenbreite-battleship.breite-battleship.vel:
                battleship.x+=battleship.vel

        if keys[pygame.K_SPACE]:
            if shootloop==0:
                battleship.fire()
                shootloop=1

    if shootloop>0:
        shootloop+=1
    if shootloop>14:
        shootloop=0

    for laser in lasers:
        if laser.y>40:
            laser.y-=laser.vel
           
        else:
            lasers.pop(lasers.index(laser))
            
    for alien in aliens:
        if alien.visible:
            for laser in lasers:
                if laser.y<alien.hitbox[1]+alien.hitbox[3] and laser.y>alien.hitbox[1]:
                    if laser.x>alien.hitbox[0] and laser.x<alien.hitbox[0]+alien.hitbox[2]:
                        alien.hit()
                        lasers.pop(lasers.index(laser))
                elif laser.y+laser.height<alien.hitbox[1]+alien.hitbox[3] and laser.y+laser.height>alien.hitbox[1]:
                    if laser.x>alien.hitbox[0] and laser.x<alien.hitbox[0]+alien.hitbox[2]:
                        alien.hit()
                        lasers.pop(lasers.index(laser))
    

    for v in enemyspaceships:
        for laser in lasers:
            if laser.y<v.hitbox[1]+v.hitbox[3] and laser.y>v.hitbox[1]:
               if laser.x>v.hitbox[0] and laser.x<v.hitbox[0]+v.hitbox[2]:
                        v.hit()
                        lasers.pop(lasers.index(laser))
            elif laser.y+laser.height<v.hitbox[1]+v.hitbox[3] and laser.y+laser.height>v.hitbox[1]:
                    if laser.x>v.hitbox[0] and laser.x<v.hitbox[0]+v.hitbox[2]:
                        v.hit()
                        lasers.pop(lasers.index(laser))

    for laser in enemylasers:
        if laser.y+laser.height<battleship.hitbox[1]+battleship.hitbox[3] and laser.y+laser.height>battleship.hitbox[1]:
            if laser.x>battleship.hitbox[0] and laser.x<battleship.hitbox[0]+battleship.hitbox[2]:
                battleship.hit()
                enemylasers.pop(enemylasers.index(laser))

    for laser in enemylasers:
        if laser.y<470:
            laser.y+=laser.vel
        else:
            enemylasers.pop(enemylasers.index(laser))

    if battleship.health<=0:
        if not ru:
            go=gameover(win)
            if go==0 or go==1:
                ru=True
                return go
        ru=False

    if len(aliens)==0 and len(enemyspaceships)==0:
        l=True
        while l:
            try:
                lasers.pop()
            except:
                l=False
        e=True
        while e:
            try:
                enemylasers.pop()
            except:
                e=False
        battleship.x=150
        redrawGameWindow(win)
        generateLevel(win,0)

    keys=pygame.key.get_pressed()
    if pausebutton or keys[pygame.K_ESCAPE]:
        pausebutton=False
        pau=True
        while pau:
            g=pause(win)
            if g==1:
                pau=False
            elif g==0:
                pau=False
                return 1
