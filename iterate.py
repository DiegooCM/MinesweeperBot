from time import sleep
import pyautogui
from PIL import ImageGrab

class Iter():

    

    def __init__(self, mode="M") -> None:

        if mode == "E":
            
            self.MINES = 10
        elif mode == "M":
            self.squares_x = 18 
            self.squares_y = 14
            self.MINES = 40
            #18x14
        elif mode == "H":
            
            self.MINES = 99

    def find_board(self):
        board = pyautogui.locateOnScreen("Python\Proyectos\Bots\BotMinesweeper\Imagenes\medium.png", confidence=0.97)
        self.board = board
        self.board_left = board[0]
        self.board_top = board[1]
        self.board_width = board[2] 
        self.board_height = board[3]
        print(board)
    
    # Dependiendo del color que sea imprimirá un color u otro
    def rgb_find(self, rgb):
        if rgb == (170, 215, 81): 
            print('Verde Claro')
        elif rgb == (162, 209, 73):
            print('Verde Oscuro')
        elif rgb == (229, 194, 159):
            print('Blanco Claro')
        elif rgb == (215, 184, 153):
            print('Blanco Oscuro')
        elif rgb[2] >= 185:
            print('1')
        elif rgb == (56, 142, 60):
            print('2')
        elif rgb == (211, 48, 48):
            print('3')
        elif rgb == (138, 57, 161):
            print('4')
        elif rgb[2] == 0: 
            print('5')#No es seguro 
        elif rgb[0] == 0:
            print('6')#No es seguro 
        elif rgb == (66, 66, 66):
            print('7')#No es seguro 
        else:
            print(rgb)
    
    def get_box(self):
        self.board_bbox = self.board_left, self.board_top, self.board_left + 32 * (self.squares_x - 1), self.board_top + 32 * (self.squares_y - 1) # Son unos calculos para adivinar donde se encuentra la region de la caja
        print(self.board_bbox)
        sleep(3)
        self.square = ImageGrab.grab(bbox=(self.board_bbox))
        #self.square.show()
        for x in range(0, self.squares_x):
            for y in range(0, self.squares_y):
                coordinates = (x * 30) + 16, (y * 30) + 16
                centerpixel = self.square.getpixel(coordinates)
                Iter.rgb_find(self, centerpixel)

                
                
                
