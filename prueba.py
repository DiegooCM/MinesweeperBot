import numpy as np

abc = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
num = np.array(['1', '2', '3', '4', '5', '6', '7', '8'])

matrix = np.array([
    [0, 1, "x", "x", "x"], 
    [0, 1, "x", "x", "x"], 
    [0, 1, "x", "x", "x"],
    [0, 1, "x", "x" ,"x"], 
    [1, 1, "x", "x", "x"]])



# Devuelve las posiciones alrededor de la posición que se le dé. En formato lista.
def alrededor(pos):
    positions = []
    
    for b in range(-1, 2):
        for c in range(-1, 2):
            positions.append([pos[0] + b, pos[1] + c])
    
    return positions


# Busca el item de la posición y la matriz que se le dé
def buscar_item(row, column, matrix):
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            item = matrix[y][x]
            if row == x and column == y:
                return item


position = [1, 1]

# Crea una matriz 3x3, pero no se le da la matriz, está cogiendo la primera. Va iterando por las posiciones de alrededor y viendo si coinciden y añadiendolas a 'b'(la matriz).
def matrix_3x3():
    b = []
    n = 0 #Para la letra
    temp_list = []
    around = alrededor(position)# Posiciones de alrededor

    for a in around:
        item = buscar_item(a[0], a[1], matrix)

        if item == 'x':
            item = abc[n]

        temp_list.append(item)

        if len(temp_list) == 3:
            b.append(temp_list)
            temp_list = []

        n += 1

    b = np.array(b)
    b = np.rot90(b)
    return b


def buscar_x(busq, matrix):
    list_x = []
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            item = matrix[y, x]
            list_tf  = np.isin(busq, str(item))
            if np.any(list_tf) == True:
                list_x.append([x, y])
    
    return list_x

# Busca las posiciones de alrededor de la posición y matriz que se le dé. Está hecho de forma muy manual. Ver si se puede cambiar por alrededor1
def alrededor2(pos, matrix):
    list_around = []
    #Bucle para las posiciones
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if (pos == [x,y]):
                pass
            elif ((pos[0] + 1 == x) and (pos[1] == y)):# +1, 0
                list_around.append(matrix[y, x])
            elif ((pos[1] + 1 == y) and (pos[0] == x)):# 0, +1
                list_around.append(matrix[y, x])
            elif ((pos[0] + 1 == x) and (pos[1] + 1 == y)):# +1, +1
                list_around.append(matrix[y, x])
            elif ((pos[0] - 1 == x) and (pos[1] + 1 == y)):# -1, +1
                list_around.append(matrix[y, x])
            elif ((pos[0] - 1 == x) and (pos[1] == y)):# -1, 0
                list_around.append(matrix[y, x])
            elif ((pos[1] - 1 == y) and (pos[0] == x)):# 0, -1
                list_around.append(matrix[y, x])
            elif((pos[0] - 1 == x) and (pos[1] - 1 == y)):# -1, -1
                list_around.append(matrix[y, x])
            elif ((pos[0] + 1 == x) and (pos[1] - 1 == y)):# +1, -1
                list_around.append(matrix[y, x])

    list_around = np.array(list_around)        
    return list_around


    
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
    

def sol_matrix(matrix):
    letters = np.isin(matrix, num) 
    list_x = buscar_x(num, matrix33)
    
    list_letters = []
    equation2 = []
    for x in list_x:
        letter = int(buscar_item(x[0], x[1], matrix))#Busca la letra que estamos buscando

        equation2.append([letter])

        list_around = alrededor2(x, matrix)# Itera sobre los que están alrededor del que buscamos
        
        filter_list = find_num(list_around, letter)
        
        list_letters.append(filter_list)
        
    equation1 = first_equation(list_letters)
    equation2 = np.array(equation2)
    
    sol_equation = np.linalg.solve(equation1, equation2)
    print(f'x is {sol_equation[0]}, y-is {sol_equation[1]} and z-is {sol_equation[2]}')

matrix33 = matrix_3x3()
#sol_matrix(matrix33)
sol_matrix(matrix33)

