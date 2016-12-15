import pygame as pg
import datetime
import random
import numpy as np

weekday_names = [
        "Lun",
        "Mar",
        "Mer",
        "Gio",
        "Ven",
        "Sab",
        "Dom"
        ]

palette_hex = [
        "#414141", # nero
        "#CCDFCB", # bianco
        "#FF6A5C", # rosso
        "#056571"  # blu
        ]

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

palette = map(hex_to_rgb,palette_hex)



size = 480,320

pg.init()
screen = pg.display.set_mode(size)


pg.font.init()
font_large = pg.font.SysFont("monospace",120)
font_big = pg.font.SysFont("monospace",40)


fps_clock = pg.time.Clock()


flag_quit = False
frame = 0

reset = False

def clock(screen):
    screen.fill(palette[0])

    now = datetime.datetime.now()
    nowstring = "%02d:%02d"%(now.hour,now.minute)

    label = font_large.render(nowstring,True,palette[1])

    lab_rect = label.get_rect()
    w,h = lab_rect.width, lab_rect.height



    screen.blit(label,(
            (size[0]-w)//2  ,
            (size[1]-h)//2
            )
        )

    today = datetime.date.today()
    nowstring = "%s %d" % ( weekday_names[today.weekday()] , today.day )
    label = font_big.render(nowstring,True,palette[1])
    lab_rect = label.get_rect()
    w,h = lab_rect.width, lab_rect.height

    screen.blit(label,(
            (size[0]-w)//2  ,
            size[1]//2 + 80
            )
        )


s_a = [(0,0),(0,0), (0,0)]
s_x = [0,0]

def sierpinski(screen):
    global reset,s_a,s_x
    if reset:
        for i in range(3):
            s_a[i] = (random.randint(0,size[0]-1), random.randint(0,size[1]-1))

        screen.fill(palette[1])
        s_x = list(s_a[random.randint(0,2)])
        reset = False

    for i in range(30):

        ind = random.randint(0,2)
        s_x[0] = (s_x[0] + s_a[ind][0])/2.0
        s_x[1] = (s_x[1] + s_a[ind][1])/2.0

        screen.set_at((int(s_x[0]),int(s_x[1])) , palette[2])


l_a = np.array(size)
def life(screen):
    global reset,l_a,frame
    if reset:
        l_a = np.random.randint(2,size = size)
        reset = False

    if frame % 3 == 0:

        neigh = sum(np.roll(np.roll(l_a,i,0),j,1)
                    for i in (-1,0,1) for j in (-1,0,1)
                    if (i!= 0 or j != 0) )
        
        l_a = np.logical_or ( 
                np.logical_and ( l_a , np.logical_and( (neigh > 1) , (neigh < 4) ) )  ,
                neigh == 3
                )


        #    pixels = np.outer( l_a, np.array(palette[3]))

        pixels = np.einsum(" ij,k",l_a,np.array(palette[3]))


        pg.surfarray.blit_array(screen,pixels)


reset = True
panel = 2

period = 500

while not flag_quit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag_quit = True

    if frame % period == period-1:
        reset = True
        panel = (panel+1)%3

    if panel == 0:
        clock(screen)
    elif panel == 1:
        sierpinski(screen)
    elif panel == 2:
        life(screen)

    pg.display.flip()
    fps_clock.tick(60)

    frame += 1
