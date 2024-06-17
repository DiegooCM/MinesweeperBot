from collections import OrderedDict
import itertools
from time import sleep
import numpy as np
import pyautogui
import keyboard

from iterater import Iter

#Arrays for searching in the arrays
abc = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
num = np.array(['1', '2', '3', '4', '5', '6', '7', '8'])

iter = Iter()


class Solve():
    
    def __init__(self):     
        # Variables to click in the right position   
        self.board_left = iter.board[0] + 15
        self.board_top = iter.board[1] + 15
        self.square_side = 30

    def matrix(self):
        sleep(1) # Without the 'sleep' it makes error when getting the matrix
        matrix_xl = iter.get_matrix() 

        return matrix_xl


    # Click the bombs    
    def click_bomb(self, pos):
        pyautogui.moveTo(self.board_left + (pos[0] * self.square_side), self.board_top + (pos[1] * self.square_side))
        pyautogui.click(button='right')
        
    # Click the squares with no bombs inside
    def click_free(self, pos):
        pyautogui.moveTo(self.board_left + (pos[0] * self.square_side), self.board_top + (pos[1] * self.square_side))
        pyautogui.click(button='left')

    # Find an given item in a given matrix
    def find_item(self, row, column, matrix):  
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if row == x and column == y:
                    item = matrix[y][x]
                    return item
                      
    # Finds whatever (normally the 'abc' and 'num' arrays) in a given matrix and return the position in the matrix and their items
    def find_x(self, busq, matrix):
        pos_x  = []
        items_x = []
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                item = matrix[y][x]
                list_tf  = np.isin(busq, str(item))
                if np.any(list_tf) == True:
                    pos_x.append([x, y])
                    items_x.append(item)
                    
        return pos_x, items_x
    
    # 'Alrededor' means around. It creates a 3x3 matrix from a given position and matrix
    def alrededor(self, pos, matrix):
        items_list = []
        list_positions_matrix = []
        n = 0

        for y in range(-1, 2):
            temp_list = []
            temp_list2 = []

            for x in range(-1, 2):
                position = [pos[0] + x, pos[1] + y]
                
                item = Solve.find_item(self, position[0], position[1], matrix)
                if item == 'x':
                    item = abc[n]
                        
                temp_list.append(item)
                temp_list2.append(position)    
                n += 1
                
            items_list.append(temp_list)
            list_positions_matrix.append(temp_list2)
        
        return items_list, list_positions_matrix
    
    # Look at the possible bombs or the existing bombs around, and take the position
    def check_x_around(self, items_list, positions_list, number):
        count_x = 0
        temp_pos = []
        positions = []

        for y in range(len(items_list)):
            for x in range(len(items_list[y])):
                item = items_list[y][x]
                check_item = np.isin(abc, item)
                if np.any(check_item) == True:
                    temp_pos.append([x, y])
                    count_x += 1
                elif item == '-1':
                    count_x += 1

        if count_x == int(number):
            for a in range(len(temp_pos)):
                posx = temp_pos[a][0]
                posy = temp_pos[a][1]
                positions.append(positions_list[posy][posx])

        return positions
    
    # Check the posible free squares by looking at the numbers with all their bombs finded
    def check_free(self, items_list, list_positions_matrix, number):
        count_bombs = 0
        list_pos_free = []
        for y in range(len(items_list)):
            for x in range(len(items_list[y])):
                item = items_list[y][x]
                if item == '-1':
                    count_bombs += 1

        if count_bombs == int(number):
            for y in range(len(items_list)):
                for x in range(len(items_list[y])):
                    item = items_list[y][x]
                    check_item = np.isin(abc, item)

                    if np.any(check_item) == True: 
                        list_pos_free.append(list_positions_matrix[y][x])

        return list_pos_free
    
    # Creates the first equation
    def equation1(self, array1, array2):
        equation = []
        if len(array1) >= len(array2):
            equation.append(np.isin(array1, array2))
            equation.append(np.isin(array1, array1))
        
        else:
            equation.append(np.isin(array2, array1))
            equation.append(np.isin(array2, array2))

        return equation

    # Creates the equations and solves them, many times this function gives problems or doesn't find correctly the bombs
    def equation_solving(self, item_list, position_list, pos_number):
        positions_near = []
        number_near = []

        positions_x = []
        bomb_positions = []

        #Look for the x's around the number to look for
        xb, e1 = Solve.find_x(self, abc, item_list)

        #Look for the numbers next to the position and return their positions and items
        colindants_pos = [[1,0], [0,1], [2,1], [1,2]]
        for x in colindants_pos:
            item = item_list[x[0]][x[1]]
            pos = [x[0], x[1]]
            check_item = np.isin(num, item)
            if np.any(check_item) == True:
                positions_near.append(position_list[x[0]][x[1]])
                number_near.append(item)

        # Take the x's around the other number to make the equation
        for pos in positions_near:
            item_num, pos_num = Solve.alrededor(self, pos, self.matrix)

            pos_n, n = Solve.find_x(self, abc, item_num)
            
            # Create the equations to be solved later
            equation1 = Solve.equation1(self, e1, n)
            equation2 = np.array([self.matrix[pos_number[1]][pos_number[0]], self.matrix[pos[1]][pos[0]]])
            equation2 = equation2.astype(int)
            
            x, residuals, rank, s = np.linalg.lstsq(equation1, equation2, rcond=None)
            if len(x) > 3:
                break

            for p in range(len(pos_n)):
                positions_x.append(pos_num[pos_n[p][1]][pos_n[p][0]])
            positions_x = list(reversed(positions_x))

            for s in range(3):
                try:
                    sol = round(x[s])
                    if sol == 1:
                        bomb_positions.append(positions_x[s])
                except IndexError:
                    pass
        
        return bomb_positions
            
    # First and most reliable method to find bombs. Looks for those boxes in which the number matches the possible mines around and returns the positions
    def sol_matrix(self, pos_letters, numbers):
        list_pos_bomb = []
        list_pos_free = []
        for n in range(len(pos_letters)):
            #pilla los items q hay alrededor(matrix 3x3)
            items_list, list_positions_matrix = Solve.alrededor(self, pos_letters[n], self.matrix)
            
            x_around = Solve.check_x_around(self, items_list, list_positions_matrix, numbers[n])

            if len(x_around) != 0:
                for a in x_around:
                    pos_bomb = [a[0], a[1]]
                    list_pos_bomb.append(pos_bomb)
                
            frees = Solve.check_free(self, items_list, list_positions_matrix, numbers[n])
            if len(frees) != 0:
                for a in frees:
                    list_pos_free.append(a)

        return list_pos_bomb, list_pos_free
    
    # Second method, as I said before, this have some problems. It creates an equation of the mines around
    def sol_equation(self, pos_letters, numbers):
        list_pos_free = []
        for n in range(len(pos_letters)):
            items_list, list_positions_matrix = Solve.alrededor(self, pos_letters[n], self.matrix)

            list_pos_bomb = Solve.equation_solving(self, items_list, list_positions_matrix, pos_letters[n])

            frees = Solve.check_free(self, items_list, list_positions_matrix, numbers[n])
            if len(frees) != 0:
                for a in frees:
                    list_pos_free.append(a)

        return list_pos_bomb, list_pos_free

    # Eliminate duplicates in the given lists
    def clean_list(list1):
        new1 = []
        if len(list1) > 0:
            for item in list1:
                if item not in new1:
                    new1.append(item)

        return new1
    
    # Clik in the positions given
    def click(self, bombs, frees):
        pos_bombs = Solve.clean_list(bombs)
        pos_frees = Solve.clean_list(frees)
        
        print(f'bombs: {pos_bombs}, frees: {pos_frees}')
        if len(pos_frees) > 0:
            for b in pos_frees:
                #print(f'Libre en {b}')
                Solve.click_free(self, b)

        if len(pos_bombs) > 0:
            for a in pos_bombs:
                #print(f'Bomba en {a}')
                Solve.click_bomb(self, a)
    
    # Main loop
    def main(self):
        while not keyboard.is_pressed('q'):
            self.matrix = Solve.matrix(self)# Take the matrix
            if np.any(self.matrix == 'x') :
                pos_letters, numbers_mx = Solve.find_x(self, num, self.matrix)

                list_pos_bomb, list_pos_free = Solve.sol_matrix(self, pos_letters, numbers_mx)
                
                if (len(list_pos_bomb) + len(list_pos_free)) == 0:
                    elist_pos_bomb, elist_pos_free = Solve.sol_equation(self, pos_letters, numbers_mx)
                    if (len(elist_pos_bomb) + len(elist_pos_free)) == 0:
                        break
                    else:
                        Solve.click(self, elist_pos_bomb, elist_pos_free) 
                    
                else:
                    Solve.click(self, list_pos_bomb, list_pos_free)
                
                pyautogui.moveTo(100, 100) # This is bcz if the mouse is in the board, it changes some colors and make errors when taking the matrix
            else:
                break
            

solve = Solve()                 

solve.main()