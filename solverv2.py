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
        sleep(0.1)
        pyautogui.click(button='right')
        
    def click_free(self, pos):
        pyautogui.moveTo(self.board_left + (pos[0] * self.square_side), self.board_top + (pos[1] * self.square_side))
        sleep(0.1)
        pyautogui.click(button='left')

    def buscar_item(self, row, column, matrix):  
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if row == x and column == y:
                    item = matrix[y][x]
                    return item
                
    # Creates            
    def matrix_3x3(self, pos, matrix):
        matrix_3x3 = []
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
                    
            matrix_3x3.append(temp_list)
            list_positions_matrix.append(temp_list2)

        return matrix_3x3, list_positions_matrix
    
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
    
    def find_num(list_around, x):

        #Filtra la lista con los colindantes
        tf_list = np.isin(list_around, abc)
        filter_list = list_around[tf_list]
        #filter_list = list(filter_list)
        return filter_list

        
    def first_equation(listas):
        max_list = []
        for lista in listas:
            if len(max_list) <= len(lista):
                max_list = lista
        
        equation1 = []

        for lista in listas:
            new_list = np.isin(max_list, lista)
            equation1.append(new_list)
        
        return equation1

    def equation(self, matrix, list_pos_matrix):
        list_letters = []
        equation2 = []

        list_positions = []

        #letters = np.isin(matrix, num) 
        list_abc = Solve.find_x(self, abc, matrix) #Busca las letras que hay en la matriz y devuelve las posiciones
        for x in list_abc:
            item = list_pos_matrix[x[1]][x[0]]
            
            list_positions.append(item)

        list_num = Solve.find_x(self, num, matrix)

        for x in list_num:
            letter = int(Solve.buscar_item(self, x[0], x[1], matrix))#Busca la letra que estamos buscando

            equation2.append([letter])
            
            list_around = Solve.alrededor(self, x, matrix)# Itera sobre los que están alrededor del que buscamos
            
            filter_list = Solve.find_num(list_around, letter)
            
            list_letters.append(filter_list)    
        
        equation1 = Solve.first_equation(list_letters)
        
        equation2 = np.array(equation2)

        #Other solutions 
       
        try:
            sol_equation = np.linalg.solve(equation1, equation2)

            print(f'{list_positions[0]} is {sol_equation[0]}, {list_positions[1]} is {sol_equation[1]} and {list_positions[2]}is {sol_equation[2]}')
            for a in range(3):
                if sol_equation[a] == 0:
                    Solve.click_free(self, list_positions[a])
                elif sol_equation[a] >= 1:
                    Solve.click_bomb(self, list_positions[a])

        except np.linalg.LinAlgError:
            pass

    

    def sol_matrix(self, pos_letters, numbers):
        list_pos_bomb = []
        list_pos_free = []
        for n in range(len(pos_letters)):
            #pilla los items q hay alrededor(matrix 3x3)
            items_list, list_positions_matrix = Solve.alrededor(self, pos_letters[n], self.matrix)
            
            x_around = Solve.check_x_around(self, items_list, list_positions_matrix, numbers[n])

            if x_around == None:
                matrix_3x3, list_positions_matrix = Solve.matrix_3x3(self, pos_letters[n], self.matrix)
                Solve.equation(self, matrix_3x3, list_positions_matrix)

            else:
                for a in x_around:
                    pos_bomb = [a[0], a[1]]
                    list_pos_bomb.append(pos_bomb)
            
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