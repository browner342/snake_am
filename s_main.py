from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty,ListProperty, ReferenceListProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from random import randrange
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

import time
Builder.load_file('statusbar.kv')
Builder.load_file('board.kv')
class Score(Widget):
    points = NumericProperty(0)

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        
class Menu(Screen):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

class TableScoore(Screen):
    score_list = ListProperty()
    table = StringProperty()
    
    def read(self):
        '''
        Reading scores from txt file
        
        input file.txt
        output string(self.table)
        '''
        #renew data
        self.score_list.clear()
        self.table = ""

        #new data read from file
        score_file = open('score.txt','r')
        self.score_list = score_file.readlines()
        self.score_list.sort()
        
        
        for item in self.score_list[::-1]:
            self.table += item
        
        score_file.close()

class AddScore(Screen):
    '''
    box nick input
    adding score to file
    '''
    textinput = ObjectProperty(None)
    score = ObjectProperty(None)
    def poi(self):
        global lll
        self.score.points = lll

    def new_score(self):
        global lll
        score_file = open('score.txt','a')
        if lll < 10:
            score_file.write('0')
        score_file.write(str(lll))
        score_file.write(' - ')
        score_file.write(self.textinput.text)
        score_file.write('\n')
        score_file.close()
        
        self.manager.current = 'menu'
    
###########################################################################################
class Fruit(Widget):
    def throw_fruit(self):
        self.x = randrange(0,Window.width, 1/20 * Window.width)
        self.y = randrange(0,Window.height, 1/20 * Window.height)

class Snake(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Snake, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.config_keyboard()

    def on_touch_down(self, touch):
        self.isTextInput = False

        def filter(widget):
            for child in widget.children:
                filter(child)
            if isinstance(widget, TextInput) and widget.collide_point(*touch.pos):
                self.isTextInput = True
                widget.on_touch_down(touch)

        filter(self)

        if not self.isTextInput and self._keyboard is None:
            self.config_keyboard()

    def config_keyboard(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers): 
        if keycode[1] == 'left' or keycode[1] == 'a':
            self.velocity_x = -1
            self.velocity_y = 0
        if keycode[1] == 'right' or keycode[1] == 'd':
            self.velocity_x = 1
            self.velocity_y = 0
        if keycode[1] == 'up' or keycode[1] == 'w':
            self.velocity_x = 0
            self.velocity_y = 1
        if keycode[1] == 'down' or keycode[1] == 's':
            self.velocity_x = 0
            self.velocity_y = -1
            
    
    def move(self):
        self.x += self.width * self.velocity_x
        self.y += self.width * self.velocity_y

class Board(Widget):
    pass

class ClassicGame(Screen):
    fruit = ObjectProperty(None)
    snake = ObjectProperty(None)
    event = ObjectProperty(None)
    points = NumericProperty(0)
    time_start = NumericProperty(0)
    time_end = NumericProperty(0)
    delta_time = NumericProperty(0)
    score = ObjectProperty(None)
    
    def end_game(self):
        pass
    def on_board(self, dt): 
        #snake out of board
        if self.snake.x >= Window.width:
            self.snake.x = 0
        elif self.snake.x < 0:
            self.snake.x = Window.width - self.snake.width
        elif self.snake.y >= Window.height:
            self.snake.y = 0
        elif self.snake.y < 0:
            self.snake.y = Window.height - self.snake.height

        #if snake eat fruit, fruit change position
        if self.fruit.pos == self.snake.pos:
            self.fruit.throw_fruit()
            global lll
            lll += 1
            self.score.points += 1
        
        self.snake.move()
        self.time_end = time.time()
        self.delta_time = self.time_end - self.time_start

        if self.delta_time >= 60:
            self.event.cancel()
            time.sleep(1)
            self.manager.current = 'addscore'

    def game(self):
        global lll
        lll = 0
        self.score.points = 0
        self.snake.config_keyboard()
        self.fruit.throw_fruit()
        self.event = Clock.schedule_interval(self.on_board, 1.0/50.0)
        self.time_start = time.time()
       

class SnakeAmApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    Window.size = (500, 500)
    SnakeAmApp().run()