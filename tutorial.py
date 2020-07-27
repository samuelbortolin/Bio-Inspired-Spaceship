import pygame
pygame.init()
clock=pygame.time.Clock()

yellow=(255,255,0)
black=(0,0,0)
white=(255,255,255)
grey=(150,150,150)
green=(0,255,0)

alienimage=pygame.image.load('data/R11E.png')

first=True
second=False
third=False
fourth=False
fifth=False

def button(win,msg,x,y,w,h,itext,atext,col):
    mouse = pygame.mouse.get_pos()
    if msg=='Back to Title Screen':
        size=20
        w+=50
    elif msg=='Pause':
        size=20
    elif msg=='Use':
        size=15
    else:
        size=35
    if x<mouse[0]<x+w and y<mouse[1]<y+h:
        pygame.draw.rect(win,col,(x,y,w,h))
        font1=pygame.font.SysFont('comicsansms',size)
        text=font1.render(msg,1,atext)
        win.blit(text, (round(x + (w/2 - text.get_width()/2)),round( y + (h/2 - text.get_height()/2))))
        click=pygame.mouse.get_pressed()
        global clickable
        if click[0]==1:
            loop=True
            while loop:
                e=False
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONUP:
                        e=True
                if e:
                    return True
            
        else:
            return False
    else:
        pygame.draw.rect(win,col,(x,y,w,h),1)
        font1=pygame.font.SysFont('comicsansms',size)
        text=font1.render(msg,1,itext)
        win.blit(text, (round(x + (w/2 - text.get_width()/2)),round( y + (h/2 - text.get_height()/2))))

font1=pygame.font.SysFont('comicsansms',20)

def writeText(win,y,msg):
    global font1
    text=font1.render(msg,1,white)
    win.blit(text,(220,y))

def printKey(win,key,x,y):
    pygame.draw.rect(win,white,(x,y,40,40),1)
    text=font1.render(key,1,white)
    win.blit(text,(x+7,y+7))

def drawtutorialship(win,x,y):
    pygame.draw.rect(win,grey,(x+20,y,70,50))
    pygame.draw.rect(win,yellow,(x+90,y+15,20,35))
    pygame.draw.rect(win,yellow,(x,y+15,20,35))
    pygame.draw.rect(win,white,(x+round(110/2)-5,y-20,10,20))
    
def drawLaser(win,x,y,color):
    pygame.draw.rect(win,color,(x,y,3,30))

def drawfirst(win):
    writeText(win,130,'Welcome to this tutorial! In this game you are')
    writeText(win,155,'in control of a yellow spaceship which is getting')
    writeText(win,180,'attacked by aliens and you have to defend it.')
    writeText(win,205,'You can use A and D or the arrowkeys to move')
    writeText(win,230,'your spaceship around the bottom of the screen.')

    drawtutorialship(win,390,350)

    printKey(win,'A',330,360)
    printKey(win,'<-',280,360)
    printKey(win,'D',520,360)
    printKey(win,'->',570,360)

    global nextbutton
    nextbutton=button(win,'Next',470,470,150,50,yellow,black,yellow)
    
    pygame.display.update()

def drawsecond(win):
    writeText(win,130,'Use Space or the Upper Arrowkey to shoot')
    writeText(win,155,'at the aliens with your laser. But be')
    writeText(win,180,'careful! The aliens will be firing back!')

    drawtutorialship(win,390,400)
    win.blit(alienimage,(390,220))

    drawLaser(win,444,340,yellow)
    drawLaser(win,425,290,green)

    global nextbutton
    global backbutton
    nextbutton=button(win,'Next',470,470,150,50,yellow,black,yellow)
    backbutton=button(win,'Back',300,470,150,50,yellow,black,yellow)

    pygame.display.update()

def drawthird(win):
    writeText(win,130,'The game itself is divided into levels,')
    writeText(win,155,'everyone a bit harder than the one before.')
    writeText(win,180,'Every five levels you will face a green')
    writeText(win,205,'spaceship of the aliens, which will give')
    writeText(win,230,'you a random time-lmited powerup you can')
    writeText(win,255,'use if you manage to destroy it.')
    writeText(win,280,'But be aware! When the spaceship has lost half')
    writeText(win,305,'of its health, it will double its shooting!')
    writeText(win,355,'NOTE: only one powerup can be held at a time.')
    writeText(win,380,'If you get another powerup while you already')
    writeText(win,405,'hold one, the old one will disappear.')
    global nextbutton
    global backbutton
    nextbutton=button(win,'Next',470,470,150,50,yellow,black,yellow)
    backbutton=button(win,'Back',300,470,150,50,yellow,black,yellow)
    pygame.display.update()

def drawfourth(win):
    writeText(win,130,'You can see your healthbar at the top left')
    writeText(win,155,'of the screen. You have 200 health at the')
    writeText(win,180,'beginning, every hit of an opponents laser')
    writeText(win,205,'will cost you one health. This number will')
    writeText(win,230,'increase dependent by your current level.')
    writeText(win,280,'You will see the health of the opponents')
    writeText(win,305,'right over their top. Their health will also')
    writeText(win,330,'go up the further you get. When an enemy has')
    writeText(win,355,'zero health, he will disappear and wont shoot')
    writeText(win,380,'at you anymore. When all enemies are dead, you')
    writeText(win,405,'passed the level.')
    global nextbutton
    global backbutton
    nextbutton=button(win,'Next',470,470,150,50,yellow,black,yellow)
    backbutton=button(win,'Back',300,470,150,50,yellow,black,yellow)
    pygame.display.update()

def drawfifth(win):
    writeText(win,130,'This is the end of the Tutorial.')
    writeText(win,155,'You are now ready to begin the game!')

    global beginbutton
    global backbutton
    global backtotitle
    beginbutton=button(win,'Begin',250,280,150,50,yellow,black,yellow)
    backbutton=button(win,'Back',450,280,150,50,yellow,black,yellow)
    backtotitle=button(win,'Back to Title Screen',450,420,150,50,yellow,black,yellow)
    pygame.display.update()
    
def doTutorial(win):
    global first
    global second
    global third
    global fourth
    global fifth
    if first:
        drawfirst(win)
        if nextbutton:
            first=False
            second=True
    if second:
        drawsecond(win)
        if nextbutton:
            second=False
            third=True
        if backbutton:
            second=False
            first=True
    if third:
        drawthird(win)
        if nextbutton:
            third=False
            fourth=True
        if backbutton:
            third=False
            second=True
    if fourth:
        drawfourth(win)
        if nextbutton:
            fourth=False
            fifth=True
        if backbutton:
            fourth=False
            third=True
    if fifth:
        drawfifth(win)
        if beginbutton:
            fifth=False
        if backbutton:
            fifth=False
            fourth=True
        if backtotitle:
            fifth=False
            return 2
    if first==False and second==False and third==False and fourth==False and fifth==False:
        return 1
    return 0
