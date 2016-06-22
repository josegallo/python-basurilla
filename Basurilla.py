# BASURILLA GAME
# to be played at http://www.codeskulptor.org/
import simplegui
import random
import math

# Canvas size
width = 1000
height = 700

# Players initial features
k = {0: "left", 1:"right", 2:"up", 3:"down", 4:"a", 5:"s", 6:"w", 7:"s"}
player_pos = [(width / 2)*0.5, height / 2]
player_pos_2 = [(width / 2)*1.5, height / 2]
color_player = "White"
#Name_1 = ""
#Name_2 = ""
text = ""
radius = 20
color = "White"

# Particule traits

colors =["Aqua","Blue","Fuchsia","Gray","Green","Lime", "Maroon", "Navy", "Olive", "Orange", \
         "Purple","Red","Silver", "Teal","White", "Yellow"]
particules = []
remove = []       
        
# math helper functions

def dot(v, w):
    return v[0] * w[0] + v[1] * w[1]

def distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# classes

class RectangularDomain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.border = 2

    # return if bounding circle is inside the domain    
    def inside(self, center, radius):
        in_width = ((radius + self.border) < center[0] < 
                    (self.width - self.border - radius))
        in_height = ((radius + self.border) < center[1] < 
                     (self.height - self.border - radius))
        return in_width and in_height

    # return a unit normal to the domain boundary point nearest center
    def normal(self, center):
        left_dist = center[0]
        right_dist = self.width - center[0]
        top_dist = center[1]
        bottom_dist = self.height - center[1]
        if left_dist < min(right_dist, top_dist, bottom_dist):
            return (1, 0)
        elif right_dist < min(left_dist, top_dist, bottom_dist):
            return (-1, 0)
        elif top_dist < min(bottom_dist, left_dist, right_dist):
            return (0, 1)
        else:
            return (0, -1)

#   if the ball go further the domain is recolocated inside the domain     
    def recolocate(self, center, radius):
        if center[1] < radius + 2 :
            center[1] = radius + 2
            center[0] = center[0]
        if center[1] > self.height - radius - 2: 
            center[1] = self.height - radius - 2
            center[0] = center[0]
        if center[0] < radius + 2:
            center[0] = radius + 2
            center[1] = center[1] 
        if center[0] > self.width - radius - 2: 
            center[0] = self.width - radius - 2
        return [center[0], center[1]]
        
    # return random location
    def random_pos(self, radius):
        x = random.randrange(radius, self.width - radius - self.border)
        y = random.randrange(radius, self.height - radius - self.border)
        return [x, y]

    # Draw boundary of domain
    def draw(self, canvas):
        canvas.draw_polygon([[0, 0], [self.width, 0], 
                             [self.width, self.height], [0, self.height]],
                             self.border*2, "Red")
        
class CircularDomain:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.border = 2
        
    # return if bounding circle is inside the domain    
    def inside(self, center, radius):
        dx = center[0] - self.center[0]
        dy = center[1] - self.center[1]
        dr = math.sqrt(dx ** 2 + dy ** 2)
        return dr < (self.radius - radius - self.border)

    # return a unit normal to the domain boundary point nearest center
    def normal(self, center):
        dx = center[0] - self.center[0]
        dy = center[1] - self.center[1]
        dr = math.sqrt(dx ** 2 + dy ** 2)
        return [dx / dr, dy / dr]      

#   if the ball go further the domain is recolocated inside the domain         
    def recolocate(self, center, radius):
        d_rec = distance(center, self.center) - self.radius + radius + 2
        n = self.normal (center)
        if ((distance(center, self.center) + radius + 2)) > self.radius:
            center[0] =  center[0] - d_rec * n[0]
            center[1] =  center[1] - d_rec * n[1]
        return [center[0],center[1]]
        
        
    # return random location
    def random_pos(self, radius):
        r = random.random() * (self.radius - radius - self.border)
        theta = random.random() * 2 * math.pi
        x = r * math.cos(theta) + self.center[0]
        y = r * math.sin(theta) + self.center[1]
        return [x, y]
        
    # Draw boundary of domain
    def draw(self, canvas):
        canvas.draw_circle(self.center, self.radius, self.border*2, "Red")

class Player:
    def __init__(self, radius, color, domain, init_pos):
        self.radius = radius
        self.color = color
        self.domain = domain        
        if init_pos == "left":
            self.pos = player_pos
        if init_pos == "right":
            self.pos = player_pos_2
        self.vel = [0,0]
        self.score = 0
        self.name = ""
        self.score = 0
        self.w = ""
    
    # bounce
    def reflect(self):
        norm = self.domain.normal(self.pos)
        norm_length = dot(self.vel, norm)
        self.vel[0] = self.vel[0] - 2 * norm_length * norm[0]
        self.vel[1] = self.vel[1] - 2 * norm_length * norm[1]    

    def recolo(self):
        rec = self.domain.recolocate(self.pos, self.radius)
        self.pos[0] = rec[0]
        self.pos[1] = rec[1]        
        
    # update ball position
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if not self.domain.inside(self.pos, self.radius):
            self.reflect()
            self.recolo()            
    
    # move ball with keywords
    
    def keydown1(self, key):
            v_h = 2
            v_v = 2
            if key == simplegui.KEY_MAP["left"]:
                self.vel[0] = - v_h
                self.vel[1] =  0
            elif key == simplegui.KEY_MAP["right"]:
                self.vel = [v_h,0]             
            elif key == simplegui.KEY_MAP["down"]:
                self.vel[0] = 0
                self.vel[1] =  v_v
            elif key == simplegui.KEY_MAP["up"]:
                self.vel[0] = 0
                self.vel[1] = - v_v
    def keydown2(self, key):
            v_h = 2
            v_v = 2
            if key == simplegui.KEY_MAP["a"]:
                self.vel[0] = - v_h
                self.vel[1] =  0
            elif key == simplegui.KEY_MAP["s"]:
                self.vel = [v_h,0]             
            elif key == simplegui.KEY_MAP["x"]:
                self.vel[0] = 0
                self.vel[1] =  v_v
            elif key == simplegui.KEY_MAP["w"]:
                self.vel[0] = 0
                self.vel[1] = - v_v

#    def keyup(self, key):
#        self.vel = [0,0]
#    #		stop ball if key up

    # absorb balls
    def absorb(self, radius, position, color):
        d = distance(position,self.pos)
        if  d <= (self.radius + radius):
                self.radius = math.sqrt(self.radius**2 + radius**2)
                self.color = color
    
#    once there are not balls the bigger player eats the other
    def absorb_w(self, radius, position, color):
        global w
        d = distance(position,self.pos)
        if particules ==[]:
            if  d  <= (self.radius + radius):
                if self.radius > radius:
                    self.radius = math.sqrt(self.radius**2 + radius**2)
                    self.color = color
                    self.w = "Winner!"
                    self.vel = [0,0]
                    
#    the player go out the domain                
    def go_out(self, radius, position):
        d = distance(position,self.pos)
        if particules ==[]:
            if  d  <= (self.radius + radius):
                if self.radius < radius:
                    self.radius = 0.01
                    self.vel = [0,0]
                    self.pos = [21000,21000]

    def draw(self, canvas, init_pos):
        
        canvas.draw_circle(self.pos, self.radius, 2, "red", self.color)
        canvas.draw_text(self.name, (self.pos[0] - 10, self.pos[1] + 5 ), 20, "Black")
        canvas.draw_text(self.w, (self.pos[0] - 10, self.pos[1] + 25 ), 20, "Black")
        if init_pos == "left":
            canvas.draw_text(("Score  " + str (self.name) + "  " + str(self.score) + \
                              "  " + "Radius = " + str(round(self.radius,1))),\
                             (width *0.125, 100), 20, "white")
        if init_pos == "right":
            canvas.draw_text(("Score  " + str (self.name) + "  " + str(self.score) + \
                              "  " + "Radius = " + str(round(self.radius,1))),\
                             (width *0.625, 100), 20, "white")

class Ball:
    def __init__(self, number, radius, color, domain):
        self.radius = radius
        self.color = color
        self.domain = domain
        self.number = number
        
        self.pos = self.domain.random_pos(self.radius)
        self.vel = [random.random() + .1, random.random() + .1]     
        
    def information(self): 
        return self.number
    
    def position(self):
        return self.pos
        
    # bounce
    def reflect(self):
        norm = self.domain.normal(self.pos)
        norm_length = dot(self.vel, norm)
        self.vel[0] = self.vel[0] - 2 * norm_length * norm[0]
        self.vel[1] = self.vel[1] - 2 * norm_length * norm[1]
    
    # absorb
    def absorb(self, radius, position):     
        d = distance(position, self.pos)
        if  d + 1 <= (self.radius + radius):
                self.radius = 0.1
                self.vel = [0,0]
                self.pos = [-100,-100]
                if position == player1.pos:
                    player1.score += 1
                if position == player2.pos:
                    player2.score += 1

    # update ball position
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if not self.domain.inside(self.pos, self.radius):
            self.reflect()
    
#    def position(self):
#        return self.pos

    # draw
    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1, 
                           self.color, self.color)        

# handlers and domains

def draw(canvas):

    field.draw(canvas)
    
    for p in particules:
        p.draw(canvas)
        p.update()
        p.absorb(player1.radius, player1.pos)
        p.absorb(player2.radius, player2.pos)
        if p.position() == [-100,-100]:
            particules.remove(p)

    player1.draw(canvas, "left")
    player1.update()    
    player2.draw(canvas, "right")
    player2.update()
    
    for i in range (len(particules)):
        player1.absorb(particules[i].radius,particules[i].pos, particules[i].color)
        player2.absorb(particules[i].radius,particules[i].pos, particules[i].color)

    if player1.radius > player2.radius: 
        player1.absorb_w(player2.radius, player2.pos, player2.color)
        player2.go_out(player1.radius, player1.pos)
    if player2.radius > player1.radius:     
        player2.absorb_w(player1.radius, player1.pos, player1.color)
        player1.go_out(player2.radius, player2.pos)
    
def input_handler1(text):
#    global Name_1
    player1.name = text
    inp1.set_text("")
    label1.set_text("Player Name 1 = " + text)

def input_handler2(text):
#    global Name_2
    player2.name = text
    inp2.set_text("")
    label2.set_text("Player Name 2 = " + text) 

def input_handler3(text):
    global n_balls, particules, d
    n_balls = int (text)
    inp3.set_text("")
    label3.set_text("Number of balls = " + text)
    for i in range (n_balls):
        p = Ball(i,random.choice(range (5,20)),random.choice(colors),field)
        particules.append(p)
    print "particules =", particules
    print "len =", len(particules)

field = RectangularDomain(width, height)

def keydown(key):
    player1.keydown1(key)
    player2.keydown2(key)
    
#def keyup(key):    
#    player1.keyup(key)
#    player2.keyup(key)
    
def button_handler3():
    frame.start()   
    
def button_handler4():
    player1.pos =  [(width / 2)*0.5, height / 2]
    player2.pos =  [(width / 2)*1.5, height / 2]
    player1.radius = player2.radius = radius    
    player1.vel = [0,0]
    player2.vel = [0,0]
    player1.color = player2.color = "white"
    player1.score = player2.score = 0
    player1.w = ""
    player2.w = ""
    
def button_handler5():
    global field
    player1.domain = RectangularDomain(width, height)
    player2.domain = RectangularDomain(width, height)
    Ball.domain = RectangularDomain(width, height)
    field = RectangularDomain(width, height)

def button_handler6(): 
    global field
    player1.domain = CircularDomain([width/2, height/2],height/2)
    player2.domain = CircularDomain([width/2, height/2],height/2)
    Ball.domain = CircularDomain([width/2, height/2],height/2)
    field = CircularDomain([width/2, height/2],height/2)
    
player1 = Player(radius, color_player, field, "left")
player2 = Player(radius, color_player, field, "right")    
    
frame = simplegui.create_frame("Basurilla", width, height)

# register even handlers

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
#frame.set_keyup_handler(keyup)
button3 = frame.add_button('Start/Faster', button_handler3)
inp1 = frame.add_input("Player Name 1 = ", input_handler1, 50)
label1 = frame.add_label('')
inp2 = frame.add_input("Player Name 2 = ", input_handler2, 50)
label2 = frame.add_label('')
inp3 = frame.add_input("Number of balls = ", input_handler3, 50)
label3 = frame.add_label('')
button4 = frame.add_button('ReStart', button_handler4)
##label5 = frame.add_label("Rectangular Domain")
#button5 = frame.add_button('Rectangular Domain', button_handler5)
#button6 = frame.add_button('Circular Domain', button_handler6)






