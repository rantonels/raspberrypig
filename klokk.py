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
        "#080808",# nero
        "#FCF9F9",# bianco
        "#981717",# rosso
        "#0D3F78",# blu
        ]

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#').lower()
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

palette = map(hex_to_rgb,palette_hex)

black, white, red, blue = tuple(palette)

size = 480,320
szarr = np.array(size)

pg.init()
screen = pg.display.set_mode(size)


fontfn = "res/coolvetica.ttf"

pg.font.init()
font_large = pg.font.Font(fontfn,200)
font_big = pg.font.Font(fontfn,50)
font_normal = pg.font.Font(fontfn,35)


fps_clock = pg.time.Clock()


flag_quit = False
frame = 0

reset = False

def timestring():
    now = datetime.datetime.now()
    nowstring = "%02d:%02d"%(now.hour,now.minute)
    return nowstring

def clock(screen):
    screen.fill(palette[0])
    
    nowstring = timestring()

    label = font_large.render(nowstring,True,palette[1])

    lab_rect = label.get_rect()
    w,h = lab_rect.width, lab_rect.height



    screen.blit(label,(
            (size[0]-w)//2  ,
            (size[1]-h)//2 - 30
            )
        )

    today = datetime.date.today()
    nowstring = "%s %d" % ( weekday_names[today.weekday()] , today.day )
    label = font_big.render(nowstring,True,palette[1])
    lab_rect = label.get_rect()
    w,h = lab_rect.width, lab_rect.height

    screen.blit(label,(
            (size[0]-w)//2  ,
            size[1]//2 + 60
            )
        )


s_a = [(0,0),(0,0), (0,0)]
s_scales = np.ones(3)
s_shifts = np.zeros((3,2) )
s_x = [0,0]
s_rotation = np.zeros((3,2,2))

def sierpinski(screen):
    global reset,s_a,s_x
    if reset:
        s_a[0] = (random.randint(0,size[0]-1), random.randint(0,size[1]//2))
        s_a[1] = (random.randint(0,size[0]//2), random.randint(size[1]//2, size[1]-1))
        s_a[2] = (random.randint(size[0]//2,size[0]-1), random.randint(size[1]//2, size[1]-1))

        for i in range(3):
            s_scales[i] = np.random.uniform(low=0.3,high=0.7)
            s_shifts[i] = np.random.uniform(low=-size[1]/2, high=size[1]/2, size=2)
            angle = np.random.uniform(low=0, high=2*np.pi)
            s,c = np.sin(angle), np.cos(angle)
            s_rotation[i,:,:] = np.array([[c,s],[-s,c]])

        screen.fill(palette[1])
        s_x = np.random.uniform( size = (50,2) ) 
        s_x[:,0] *= size[0]
        s_x[:,1] *= size[1]
        reset = False


        ind = np.random.randint(0,3,size=(s_x.shape[0]))
#        s_x[0] = (s_x[0] + s_a[ind][0])/2.0
#        s_x[1] = (s_x[1] + s_a[ind][1])/2.0
#
        s_x = (s_x - szarr/2.0)
#        s_x = (s_scales[ind] * np.tensordot( s_rotation[ind,:,:] , s_x , axes=([1],[1])))
        print s_x.shape, s_rotation[ind,:,:].shape
        s_x = np.einsum("ik,i,ijk->ij",s_x,s_scales[ind],   s_rotation[ind,:,:])
        s_x += szarr/2.0 
        s_x += s_shifts[ind]

#        for j in range(2):
#            s_x
#            s_x[j] = (s_x[j] - size[j]/2.0) * s_scales[ind] + size[j]/2.0 + s_shifts[ind][j]
        for i in range(s_x.shape[0]):
            
            screen.set_at((int(s_x[i][0]),int(s_x[i][1])) , palette[2])


l_a = np.zeros(( size[0]//2,size[1]//2))

def life(screen):
    global reset,l_a,frame
    if reset:
        l_a = np.random.randint(2,size = l_a.shape).astype(int)
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

        kron = np.kron(l_a, np.ones((2,2)).astype(int) )
        pixels =  np.einsum(" ij,k",kron,np.array(blue) ) \
                + np.einsum(" ij,k",np.logical_not(kron),np.array(black) )



        pg.surfarray.blit_array(screen,pixels)


def smallclock(screen):
    nowstring = timestring()
    label = font_big.render(nowstring,True,palette[1])

    lab_rect = label.get_rect()
    w,h = lab_rect.width, lab_rect.height

    pg.draw.rect(screen, black, (0,0,w+20,h))

    screen.blit(label,(10,0))


def wall(screen):
    now = datetime.datetime.now()

    center = tuple( (szarr/2.0).astype(int))

    radius = int(size[1]//2 * 0.7)

    screen.fill(white)
    pg.draw.circle(screen,black, center, radius, 4)

    angle = now.hour / 12. * 2* np.pi
    endp = (szarr/2.0) + radius * 0.6 * np.array( [ np.sin(angle), -np.cos(angle) ] )

    pg.draw.line( screen, black, center, tuple(endp.astype(int)) , 5)

    angle = now.minute / 60. * 2* np.pi
    endp = (szarr/2.0) + radius * 0.8 * np.array( [ np.sin(angle), -np.cos(angle) ])

    pg.draw.line( screen, black, center, tuple(endp.astype(int))  , 3)

    angle = now.second / 60. * 2* np.pi
    endp = (szarr/2.0) + radius * 0.8 * np.array( [ np.sin(angle), -np.cos(angle) ])

    pg.draw.line( screen, black, center, tuple(endp.astype(int))  , 1)


deg_sign= u'\N{DEGREE SIGN}'
def thermometer(screen):
    global reset,temperature
    if reset:
        f = open("/sys/class/thermal/thermal_zone0/temp",'r')
        temperature = int(f.read()) / 1000.0
        reset = False

    screen.fill(white)

    label = font_normal.render("CPU temp: %.1f %sC"%(temperature,deg_sign) , True, red)
    screen.blit(label,(size[0]//2-50, size[1]//2-80))



reset = True
panel = 3
panels = [clock,wall,life,thermometer]

period = 150

while not flag_quit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag_quit = True

    if frame % period == period-1:
        reset = True
        panel = (panel+1)%len(panels)

    panels[panel](screen)

    if panel != 0:
        smallclock(screen)

    pg.display.flip()
    fps_clock.tick(30)

    frame += 1
