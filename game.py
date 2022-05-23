import random
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    def __init__(self, width=4, height=4):
        self.__width = width
        self.__height = height
        self.zero_pos = (0, 0)
        self.table = self.generate_table()
        self.message = ''
        self.counter = 0

    def form_new_turn(self, direction):
        directions = {
            'right': (0, -1),
            'left': (0, 1),
            'down': (-1, 0),
            'up': (1, 0)
        }
        self.message = ''
        new_pos = (self.zero_pos[0] + directions[direction][0], self.zero_pos[1] + directions[direction][1])
        if new_pos[0] not in range(self.__height) or new_pos[1] not in range(self.__width):
            self.message = 'Impossible turn'
            return
        self.table[self.zero_pos[0]][self.zero_pos[1]] = self.table[new_pos[0]][new_pos[1]]
        self.table[new_pos[0]][new_pos[1]] = 0
        self.zero_pos = new_pos
        self.counter += 1
        if self.zero_pos == (self.__height - 1, self.__width - 1):
            self.message = self.__check_complete(self.table)


    def generate_table(self):
        r = list(range(self.__width * self.__height))
        random.shuffle(r)
        z = r.index(0)
        self.zero_pos = (z // self.__width, z % self.__width)
        return [[r[i*self.__width+j] for j in range(self.__width)] for i in range(self.__height)]

    @staticmethod
    def __check_complete(table):
        count = 0
        for i in range(len(table)):
            for j in range(len(table[0])):
                if i == len(table) - 1 and j == len(table[0]) - 1:
                    continue
                count += 1
                if table[i][j] != count:
                    return ''
        return 'Puzzle completed! Congratulation!'
