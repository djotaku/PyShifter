__progname__ = "Pyshifter"
__author__ = "Eric Mesa"
__version__ = "v0.2"
__license__ = "GNU GPL v3"
__copyright__ = "(c)2008 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"
__picture__ = "Nam" #picture must be 480x480

#v0.1 - basically the LXF code with some improvements 
#v0.2 - add score

from pygame import *
import random

class Tile:
    def __init__(self,actualpos,correctpos):
        self.actualpos = actualpos
        self.correctpos = correctpos
    def render(self):
        #helps us determine the column and row of the tile we want to move
        ya = self.actualpos/3
        xa = self.actualpos % 3

        yc = self.correctpos/3
        xc = self.correctpos % 3

        #tile 8 is never drawn
        if self.correctpos != 8:
            screen.blit(mainpic,[xa*160,ya*160,160,160],[xc*160,yc*160,160,160])

def swap_tile(num):
    #-1 means we can't move in that direction
    if num == 0: try_swap(0,1,3,-1,-1)
    if num == 1: try_swap(1,0,2,4,-1)
    if num == 2: try_swap(2,1,5,-1,-1)
    if num == 3: try_swap(3,0,4,6,-1)
    if num == 4: try_swap(4,1,3,5,7)
    if num == 5: try_swap(5,2,4,8,-1)
    if num == 6: try_swap(6,3,7,-1,-1)
    if num == 7: try_swap(7,6,4,8,-1)
    if num == 8: try_swap(8,5,7,-1,-1)

def find_pos(pos):
    for x in range(9):
        if tile_list[x].actualpos == pos:
            return x

    return -1

def swap_pos(one,two):
    tmp = tile_list[one].actualpos
    tile_list[one].actualpos = tile_list[two].actualpos
    tile_list[two].actualpos = tmp 

def try_swap(clicked,pos1,pos2,pos3,pos4):
    num = find_pos(clicked)
    a = find_pos(pos1)
    b = find_pos(pos2)
    c = find_pos(pos3)
    d = find_pos(pos4)

    #make sure you want to move tile to a valid position and that it is swapping with blank tile
    if a != -1 and tile_list[a].correctpos == 8:
        swap_pos(a,num)
        return 
    if b != -1 and tile_list[b].correctpos == 8:
        swap_pos(b,num)
        return
    if c != -1 and tile_list[c].correctpos == 8:
        swap_pos(c,num)
        return
    if d != -1 and tile_list[d].correctpos == 8:
        swap_pos(d,num)
        return 

init()
screen = display.set_mode((480,480))
display.set_caption(("%s - %s - %s") % (__progname__,__version__, __picture__))

scorefont = font.Font(None,60)
#for windows use
# scorefont = font.Font('freesansbold.ttf',30)

moves = 0

mainpic = image.load('picture.jpg')
highlight = image.load('highlight.png')

tile_list = []

#initialize the list
for x in range(9):
    tmp_tile = Tile(x,x)
    tile_list.append(tmp_tile)

for x in range(1000):
    swap_tile(random.randrange(0,8))

player_tile = 0

quit = 0

while quit == 0:
    screen.fill((0,0,0))

    for x in range(9):
        tile_list[x].render()

    xh = player_tile/3
    yh = player_tile%3
    screen.blit(highlight,(yh*160,xh*160))

    display.update()

    e = event.wait()

    if e.type == KEYDOWN:
        if e.key == K_UP:
            if player_tile > 2:
                player_tile -= 3

        if e.key == K_DOWN:
            if player_tile < 6:
                player_tile += 3

        if e.key == K_LEFT:
            if player_tile != 0 and player_tile != 3 and player_tile != 6:
                player_tile -= 1

        if e.key == K_RIGHT:
            if player_tile != 2 and player_tile != 5 and player_tile != 8:
                player_tile += 1

        if e.key == K_SPACE:
            swap_tile(player_tile)
            moves += 1

        if e.key == K_ESCAPE:
            quit = 1

        success = 1
    
        for x in range(9):
            if tile_list[x].actualpos != tile_list[x].correctpos:
                success = 0

end = 0
while end == 0:
    if success == 1:
        scoretext = scorefont.render('Moves:' + str(moves),True,(255,255,255),(0,0,0))
        scoretext2 = scorefont.render('Congrats, you did it!',True,(255,255,255),(0,0,0))
        scoretext3 = scorefont.render('Press Escape to Quit',True,(255,255,255),(0,0,0))
        screen.blit(scoretext,(5,5))
        screen.blit(scoretext2,(5,80)) 
        screen.blit(scoretext3,(5,120))
        #print "Congratulations, you did it!"
        #print moves
    else:
        scoretext = scorefont.render('Moves:' + str(moves),True,(255,255,255),(0,0,0))
        scoretext2 = scorefont.render('Better Luck Next time!',True,(255,255,255),(0,0,0))
        scoretext3 = scorefont.render('Press Escape to Quit',True,(255,255,255),(0,0,0))
        screen.blit(scoretext,(5,5))
        screen.blit(scoretext2,(5,80)) 
        screen.blit(scoretext3,(5,120))
        #print "Better luck next time."
        #print moves
    display.update()

    e = event.wait()

    if e.type == KEYDOWN:

        if e.key == K_ESCAPE:
            end = 1
