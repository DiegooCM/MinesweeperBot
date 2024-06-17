from time import sleep
import numpy as np
import pyautogui
from PIL import ImageGrab

# This class creates the matrix
class Iter():    

    def __init__(self, mode="M") -> None:
        # For now, it can only be played in medium mode.
        if mode == "E":
            self.MINES = 10
        elif mode == "M":
            self.squares_x = 18 
            self.squares_y = 14
            self.MINES = 40
            #18x14
        elif mode == "H":
            self.MINES = 99

        
        board = pyautogui.locateOnScreen("medium.png", confidence=0.97)# Locates the empty board and saves the positions
        self.board = board
        self.board_left = board[0]
        self.board_top = board[1]
        self.board_width = board[2] 
        self.board_height = board[3]
        Iter.click_first(self)

    #Makes the first click in the upper left corner
    def click_first(self):
        pyautogui.moveTo(self.board_left + 15, self.board_top + 15)
        pyautogui.click(button='left')#Clicks first position

    # Depending on the color it will return one color or another
    def rgb_find(self, rgb):
        if rgb == (170, 215, 81): 
            return('x') # Verde Claro
        elif rgb == (162, 209, 73):
            return('x') # Verde Oscuro
        elif rgb[0] == 229:
            return('0') # Blanco Claro
        elif rgb == (215, 184, 153):
            return('0') # Blanco Oscuro
        elif rgb == (25, 118, 210):
            return('1')
        elif rgb == (56, 142, 60):
            return('2')
        elif rgb[0] ==  211:
            return('3')
        elif rgb == (138, 57, 161) or rgb == (141, 59, 162)or rgb == (123, 31, 162):
            return('4')
        elif rgb == (232, 189, 143) or rgb == (255, 143, 0): 
            return('5')
        elif rgb[0] == 0:
            return('6')# I'm not sure
        elif rgb == (66, 66, 66):
            return('7')# I'm not sure
        elif rgb == (242, 54, 7):
            return('-1') 

    
    def get_matrix(self):
        self.board_bbox = self.board_left, self.board_top, self.board_left + 32 * (self.squares_x - 1), self.board_top + 32 * (self.squares_y - 1) # Son unos calculos para adivinar donde se encuentra la region de la caja
        self.square = ImageGrab.grab(bbox=(self.board_bbox))
        principal_matrix = []
        
        for x in range(self.squares_x):
            temp_list = []
            for y in range(self.squares_y):
                coordinates = (x * 30) + 16, (y * 30) + 8 # The y is a bit higher so it can reads also the bombs
                centerpixel = self.square.getpixel(coordinates) # Takes the pixel
                item = Iter.rgb_find(self, centerpixel) # Reads the pixel and return the number

                temp_list.append(item)
            
            
            principal_matrix.append(temp_list)

        # Creates and transpose the matrix
        principal_matrix = np.array(principal_matrix)
        principal_matrix = principal_matrix.transpose()
                
        return principal_matrix
                   
