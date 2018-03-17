# -*- coding: utf-8 -*-
"""A text based snake game"""
import curses
import locale
import time
import random

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()  

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Snake(object):
    def __init__(self, p, direction):
        """init a snake, start from (x,y) with direction
        """
        self.direction = direction
        self._body = list()
        self._body.append(p)
    
    def __len__(self):
        return len(self._body)

    def _next_point(self):
        head = self._body[0]
        new_x = head.x
        new_y = head.y
        if self.direction == UP:
            new_y -= 1
        elif self.direction == DOWN:
            new_y += 1
        elif self.direction == RIGHT:
            new_x += 1
        elif self.direction == LEFT:
            new_x -= 1
        else:
            pass
        return Point(new_x, new_y)

    def is_food(self, p):
        return self._next_point() == p
        
    def has_point(self, other):
        """Check if the point on Snake"""
        ans = False
        for p in self._body:
            if p  == other:
                ans = True
                break
        return ans

    def eat(self, p):
        """eat a new point, append to the last
        """
        self._body.insert(0, p)

    def move(self):
        """return True or False
        return new head and trail
        """
        new_pos = self._next_point()
        if self.has_point(new_pos):
            return (None, None)
        else:
            self._body.insert(0, new_pos)
            old_tail = self._body[-1]
            self._body = self._body[:-1]

            return (new_pos, old_tail)



class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class Stage(object):
    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)              
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)        
        curses.curs_set(0)

        self.screen.keypad(True)
        self.screen.border()

        self.MIN_X = 30
        self.MIN_Y = 0
        self.SPEED = 1000
        self.MAX_Y, self.MAX_X = self.screen.getmaxyx()

        self.screen.timeout(self.SPEED)
        self.screen.vline(0, self.MIN_X, curses.ACS_VLINE, self.MAX_Y)
        self.screen.addch(0, self.MIN_X, curses.ACS_TTEE)
        self.screen.addch(self.MAX_Y-1,30,curses.ACS_BTEE)

        self.screen.addstr(1,1,'Information',curses.color_pair(1))
        self.screen.addstr(10,1,'Press q to exit',curses.color_pair(4))
        self.screen.addstr(11,1,'Use arrow to control',curses.color_pair(4))

    
    def _generate_food_p(self):
        rand_x = random.randint(self.MIN_X + 1, self.MAX_X -2)
        rand_y = random.randint(self.MIN_Y + 1, self.MAX_Y -2)
        food = Point(rand_x, rand_y)
        while self.snake.has_point(food):
            rand_x = random.randint(self.MIN_X + 1, self.MAX_X -2)
            rand_y = random.randint(self.MIN_Y + 1, self.MAX_Y -2)
            food = Point(rand_x, rand_y)
        return food

    def _on_wall(self, p):
        if p.x in (self.MIN_X , self.MAX_X-1) or p.y in (self.MIN_Y, self.MAX_Y-1):
            return True
        else:
            return False

    def _update_info(self, y, info):
        self.screen.addstr(y,1,info,curses.color_pair(1))
    
    def refresh_snake(self):
        for p in self.snake._body:
            self.screen.addstr(p.y, p.x,'#')
    

    def run(self):
        step_counter = 0
        p1 = Point(35,2)
        self.snake = Snake(p1, RIGHT)
        for _ in range(10):
            next_p = self.snake._next_point()
            if not self._on_wall(next_p):
                self.snake.eat(next_p)
        # self.snake.direction = DOWN
        # next_p = self.snake._next_point()
        # self.snake.eat(next_p)
        # self.snake.direction = LEFT
        # for _ in range(168):
        #     next_p = self.snake._next_point()
        #     if not self._on_wall(next_p):
        #         self.snake.eat(next_p)
        # self.snake.direction = DOWN
        # next_p = self.snake._next_point()
        # self.snake.eat(next_p)
        # self.snake.direction = RIGHT
        # for _ in range(168):
        #     next_p = self.snake._next_point()
        #     if not self._on_wall(next_p):
        #         self.snake.eat(next_p)
        # self.snake.direction = DOWN
            
        


        self._update_info(2, "Length {}".format(len(self.snake)))
        self._update_info(3, "Head ({},{})          ".format(self.snake._body[0].y, self.snake._body[0].x))
        food = self._generate_food_p()
        self._update_info(4, "Food ({},{})          ".format(food.y, food.x))

        self.refresh_snake()

        while True:
            step_counter += 1
            self._update_info(5, "Moves {}".format(step_counter))
            self._update_info(6, "Speed {}    ".format(self.SPEED))
            key = self.screen.getch()

            if key == -1:
                pass
            elif key == ord('k') or key == curses.KEY_UP:
                self.snake.direction = UP
            elif key == ord('l') or key == curses.KEY_RIGHT:
                self.snake.direction = RIGHT
            elif key == ord('j') or key == curses.KEY_DOWN:
                self.snake.direction = DOWN
            elif key == ord('h') or key == curses.KEY_LEFT:
                self.snake.direction = LEFT
            elif key == ord('q'):
                curses.endwin()
                break
            else:
                pass

            self.screen.addstr(food.y,food.x,'@',curses.color_pair(2))

            if self.snake.is_food(food):
                self.snake.eat(food)
                self._update_info(2, "Length {}".format(len(self.snake)))
                self.SPEED = 1000 - len(self.snake)
                self.screen.timeout(self.SPEED)

                self.screen.addstr(food.y, food.x,'#',curses.color_pair(3))
                food = self._generate_food_p()
                self._update_info(4, "Food ({},{})            ".format(food.y, food.x))
            else:
                head, tail = self.snake.move()
                if head is None or self._on_wall(head):
                    curses.flash()
                    time.sleep(3)
                    curses.endwin()
                    break
                else:
                    self.refresh_snake()
                    self._update_info(3, "Head ({},{})         ".format(head.y, head.x))
                    self.screen.addstr(tail.y, tail.x, ' ')


def main():
    stage = Stage()
    # stage.run()
    stage.run()



if __name__ == '__main__':
    main()

