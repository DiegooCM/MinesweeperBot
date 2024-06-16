#Tendrá todas las funciones para resolver la matriz
from collections import OrderedDict
import itertools
from time import sleep
import numpy as np
import pyautogui
import keyboard

from iterater import Iter

abc = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
num = np.array(['1', '2', '3', '4', '5', '6', '7', '8'])
iter = Iter()


class Solve():
    
    def __init__(self):        
        self.board_left = iter.board[0] + 15
        self.board_top = iter.board[1] + 15
        self.square_side = 30

    def matrix(self):
        sleep(1)
        matrix_xl = iter.get_matrix() 

        return matrix_xl
        #print(self.matrix)
        
    def click_bomb(self, pos):
        pyautogui.moveTo(self.board_left + (pos[0] * self.square_side), self.board_top + (pos[1] * self.square_side))
        pyautogui.click(button='right')
        
    def click_free(self, pos):
        pyautogui.moveTo(self.board_left + (pos[0] * self.square_side), self.board_top + (pos[1] * self.square_side))
        pyautogui.click(button='left')

    def buscar_item(self, row, column, matrix):  
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if row == x and column == y:
                    item = matrix[y][x]
                    return item
                      
    # Finds whatever in a given matrix and search
    def find_x(self, busq, matrix):
        pos_x  = []
        items_x = []
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                item = matrix[y][x]
                list_tf  = np.isin(busq, str(item))
                if np.any(list_tf) == True:
                    pos_x.append([x, y]) #Posicion de donde se encuentra la incognita en la 3x3
                    items_x.append(item)
                    
        return pos_x, items_x
    
    def alrededor(self, pos, matrix):
        items_list = []
        list_positions_matrix = []
        n = 0

        for y in range(-1, 2):
            temp_list = []
            temp_list2 = []

            for x in range(-1, 2):
                position = [pos[0] + x, pos[1] + y]
                
                item = Solve.buscar_item(self, position[0], position[1], matrix)
                if item == 'x':
                    item = abc[n]
                        
                temp_list.append(item)
                temp_list2.append(position)    
                n += 1
                
            items_list.append(temp_list)
            list_positions_matrix.append(temp_list2)
        
        return items_list, list_positions_matrix
    
    def check_x_around(self, items_list, positions_list, number):
        count_x = 0
        temp_pos = []
        positions = []

        #print(items_list, positions_list, number)
        #Mira las posibles bombas o las bombas existentes alrededor, y coge la posicion
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
    
    def equation1(self, array1, array2):
        equation = []
        if len(array1) >= len(array2):
            equation.append(np.isin(array1, array2))
            equation.append(np.isin(array1, array1))
        
        else:
            equation.append(np.isin(array2, array1))
            equation.append(np.isin(array2, array2))

        return equation


    def equation_solving(self, item_list, position_list, pos_number):
        positions_near = []
        number_near = []

        positions_x = []
        bomb_positions = []

        #Busca las x alrededor del número a buscar
        xb, e1 = Solve.find_x(self, abc, item_list)

        #Busca los numeros alrededor de la posición y devuelve sus posiciones e items
        for x in range(len(item_list)):
            for y in range(len(item_list[x])):
                item = item_list[x][y]
                pos = [x, y]
                check_item = np.isin(num, item)
                if (np.any(check_item) == True) and (pos_number != position_list[x][y]):
                    positions_near.append(position_list[x][y])
                    number_near.append(item)

        # Coge las x alrededor del otro numero para poder hacer la ecuacion
        for pos in positions_near:
            item_num, pos_num = Solve.alrededor(self, pos, self.matrix)

            pos_n, n = Solve.find_x(self, abc, item_num)
            
            #Crea las equaciones para que sean resolvidas más adelante
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
            else:
                # Queda por tener en cuenta cuando es una bomba aqui: 
                bombs = Solve.equation_solving(self, items_list, list_positions_matrix, pos_letters[n])
                for b in bombs:
                    list_pos_bomb.append(b)
                
                
            
            frees = Solve.check_free(self, items_list, list_positions_matrix, numbers[n])
            if len(frees) != 0:
                for a in frees:
                    list_pos_free.append(a)

        return list_pos_bomb, list_pos_free
    
    # Clika en las posiciones dadas
    def click(self, pos_bombs, pos_frees):
        pos_bombs = list(pos_bombs for pos_bombs,_ in itertools.groupby(pos_bombs) )
        pos_frees = list(pos_frees for pos_frees,_ in itertools.groupby(pos_frees) )
        
        print(f'bombs: {pos_bombs}, frees: {pos_frees}')
        if len(pos_frees) > 0:
            
            for b in pos_frees:
                print(f'Libre en {b}')
                Solve.click_free(self, b)

        if len(pos_bombs) > 0:
            for a in pos_bombs:
                print(f'Bomba en {a}')
                Solve.click_bomb(self, a)
            


    def main(self):
        #Coge la matriz
        self.matrix = Solve.matrix(self)
        print(self.matrix)
        pos_letters, numbers_mx = Solve.find_x(self, num, self.matrix)

        list_pos_bomb, list_pos_free = Solve.sol_matrix(self, pos_letters, numbers_mx)

        Solve.click(self, list_pos_bomb, list_pos_free)

        #Mueve el raton hacia un sitio para que así no cree confusiones a la hora de hacer la matriz
        pyautogui.moveTo(100, 100)




solve = Solve()                 

while not keyboard.is_pressed('q'):
    solve.main()