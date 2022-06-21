import arcade
import random
import threading
import time


SCREEN_WIDTH=700
SCREEN_HEIGHT=500

class Ship(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png")
        self.center_x=SCREEN_WIDTH//2
        self.center_y=50
        self.height=70
        self.width=70
        self.speed=5
        self.heart=3
        self.score=0
        self.game_over=False
    def move(self):
         self.center_x += self.change_x*self.speed



class Enm(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png")
        self.width=50
        self.height=50
        self.center_y=500
        self.center_x=random.randint(0,SCREEN_WIDTH)
        self.speed=5

    def move(self):
        self.center_y -=self.speed


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,"Space Craft")
        self.background_color=arcade.color.BLACK
        self.image=arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.image1=arcade.load_texture("heart2.png")
        self.shooter=Ship()
        self.enemies=[]
        self.shots=[]
        self.myThread=threading.Thread(target=self.enemy_generator)
        self.myThread.start()
        self.game_over=False
    
    def on_key_press(self,symbol,modifier):
            if symbol==arcade.key.LEFT:
                if self.shooter.center_x>49 :
                    self.shooter.change_x = -1
            elif symbol==arcade.key.RIGHT:
                if self.shooter.center_x<751 :
                  self.shooter.change_x = 1
    
    def on_key_release(self,symbol,modifier):
        if symbol == arcade.key.LEFT:
           
            self.shooter.change_x = 0

        elif symbol == arcade.key.RIGHT:

            self.shooter.change_x = 0    

    def enemy_generator(self):
        while True:
            self.enemies.append(Enm())
            time.sleep(4)
        
    def on_update(self, delta_time):
        if self.game_over==False:
            self.shooter.move()
            if(self.shooter.center_x>750):
                self.shooter.change_x=0
            if(self.shooter.center_x<50):
                self.shooter.change_x=0
            
            
            
            for shot in self.shots:                  
                for enemy in self.enemies:                  
                    if (arcade.check_for_collision(shot,enemy)):
                        self.shots.remove(shot)
                        self.enemies.remove(enemy)
                        self.shooter.score += 1
                        break
            
            for enemy in self.enemies:
                if (arcade.check_for_collision(self.shooter,enemy)):
                    self.enemies.remove(enemy)
                    self.shooter.heart -= 1
                    break
        
        for shot in self.shots:
            shot.move()
        
        for enemy in self.enemies:
            enemy.move()

        for shot in self.shots:
            if (shot.center_y>600):
                self.shots.remove(shot)

        for enemy in self.enemies:
            if (enemy.center_y<0):
                self.enemies.remove(enemy)
        
        
        if self.shooter.heart==0:
            self.game_over=True
          
        

    def on_draw(self):
        arcade.start_render()
        if self.game_over==False:
            arcade.draw_lrwh_rectangle_textured(0,0,self.width,self.height,self.image)
            
            for shot in self.shots:
                    shot.draw()
                
            for enemy in self.enemies:
                enemy.draw()
        
            self.shooter.draw()    
            for i in range (1,self.shooter.heart+1):
                arcade.draw_texture_rectangle(i*35,35,35,35,self.image1)
            score_text = f"Score: {self.shooter.score}"
        
        
            arcade.draw_text(score_text,self.width-120,10,arcade.color.GREEN_YELLOW,20)
        else:

            arcade.draw_text("You lost again",self.width/2-170,self.height/2,arcade.color.RED_ORANGE,50)
        


mygame=Game()
arcade.run()