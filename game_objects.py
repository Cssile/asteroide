from if3_game.engine import init, Sprite
from pyglet.window.key import symbol_string 
from math import cos, sin, radians
from random import randint

RESOLUTION = (800, 600)

class SpaceObject(Sprite):

    def __init__ (self, image, position = (0,0), speed = (0,0), anchor = (0,0) ) :
        super().__init__(image,position, anchor = anchor, )
        self.speed = speed
        self.rotation_speed = 0
    def update(self, dt): # dt = delta time = temps depuis la dernière update
        super().update(dt)
        
        
        movement = (self.speed [0] * dt, self.speed [1] * dt  )
        self.position = (self.position [0] + movement [0], self.position [1] + movement [1])
        self.rotation += self.rotation_speed * dt

        # position et rotation existent déjà dans les Sprites
        
        # self.position [0] + movement [0] ( équivaut à self.position [0] + (self.speed[0] * dt))
        # if self.position > (800, 600) :
        #     self.position = (self.position [0] + movement [0], self.position [1] + movement [1])
    
        if self.position[0] > RESOLUTION[0]:
            self.position = (0,self.position [1])

        elif self.position[0] < 0:
            self.position = (RESOLUTION[0], self.position[1])
   
        if self.position[1] > RESOLUTION[1]:
            self.position = (self.position [0], 0)

        elif self.position[1] < 0:
            self.position = (self.position[0], RESOLUTION[1])

class Spaceship (SpaceObject) :
    def __init__ (self,position) :
        super().__init__("assets/spaceship.png", position, anchor = (32,32) )
        self.velocity = 0
        self.engine_on = False
        self.acceleration = 1
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
    

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "RIGHT" :
            self.rotation_speed += 180
        if symbol_string(key) == "LEFT":
            self.rotation_speed -= 180
        if symbol_string(key) == "UP":
            self.engine_on = True

        if symbol_string (key) == "SPACE" :
            self.shoot ()
    
    def on_key_release(self, key, modifiers):
        if symbol_string(key) == "RIGHT" :
            self.rotation_speed -= 180
        if symbol_string(key) == "LEFT":
            self.rotation_speed += 180
        if symbol_string(key) == "UP":
            self.velocity = 0
            self.engine_on = False


    def update (self, dt) :
        if self.engine_on :
            self.velocity += self.acceleration * dt
            angle = -radians(self.rotation) #randians = convention de degrés
            direction = (cos (angle) , sin (angle) )
            new_speed = (self.velocity * direction [0], self.velocity* direction [1])
            self.speed = ( self.speed [0] + new_speed [0], self.speed [1] + new_speed [1] )
        
        self.invincible_timer -= dt
        if self.invincible_timer <= 0:
            self.invincible = False
            self.opacity = 255
        super().update(dt)
    
    def shoot (self) :
        pos = self.position
        # tirer a partir du spaceship
        angle = - radians (self.rotation)
        direction = (cos (angle), sin (angle))
    
        #calculer vitesse du missile
        missile_speed = (200* direction [0], 200* direction [1])

        #créer le missile
        missile = Missile (pos, missile_speed)
        
        # ajouter le missile au layer
        self.layer.add (missile)

    def destroy (self)  :
        if not self.invincible :
            if self.lives <= 0 :
                super().destroy ()
            
            else :
                self.lives -= 1
                self.invincible = True
                self.opacity = 100
                self.invincible_timer = 3
                print (self.lives)
        


class Asteroid (SpaceObject) :
    
    def __init__ (self, position = (200,200), speed = (30,30), size = 3 ) :
        if size == 3 :
            super().__init__("assets/asteroid128.png", position = position , speed = speed , anchor = (64,64))
        elif size == 2 :
            super().__init__("assets/asteroid64.png", position = position , speed = speed , anchor = (32,32))
        else :
            super().__init__("assets/asteroid32.png", position = position , speed = speed , anchor = (16,16))
        
        self.size = size

        self.rotation_speed = 45
    
    def on_collision(self, other):
        if isinstance (other, Spaceship) :
            other.destroy ()
        if isinstance (other, Missile ) :
            other.destroy ()
            self.destroy ()
            

            
    
    def destroy(self) :
        super().destroy()
        if self.size > 1 :
            for _ in range (2):
                new_speed = (randint (-200,200), randint (-200,200))
                new_asteroid = Asteroid (self.position, new_speed, self.size -1 )
                self.layer.add (new_asteroid)
        
        


class Missile (SpaceObject) :

    def __init__ (self, position = (0,0), speed = (0,0)) :
        super().__init__ ("assets/bullet.png", position = position, speed= speed, anchor = (8,8))
        self.timer = 3
        
        # dt = temps depuis la dernière update dt =  delta time
        
        #def update(self, dt):
        #for item in self.__items:
        #    item.update(dt)
        
    def update (self, dt):
        super ().update(dt)
        self.timer -= dt
        if self.timer <= 0 :
            self.destroy ()
    
    
        

            

        # a chaque update le temps diminue un petit peu depuis le temps de la dernière update

        # a chaque update on retire le temps qui est passé de la durée de vie et ensuite on supprime le missile missile.destroy

# Donner des vies au joueur


        

        
        
    