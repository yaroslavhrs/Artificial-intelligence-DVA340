import time

def read_file(n):
    
    with open('Assignment 2 sudoku.txt') as file:
        lines = file.readlines()
    
    sudoku_1 = lines[5:14]
    sudoku_2 = lines[16:25]
    sudoku_3 = lines[27:36]
    sudoku_4 = lines[38:47]
    sudoku_5 = lines[49:58]
    sudoku_6 = lines[60:69]
    sudoku_7 = lines[71:80]
    sudoku_8 = lines[82:91]
    sudoku_9 = lines[93:102]
    sudoku_10 = lines[104:113]
    
    if n == 1:
        sudoku_n = sudoku_1
    elif n == 2:
        sudoku_n = sudoku_2
    elif n == 3:
        sudoku_n = sudoku_3
    elif n == 4:
        sudoku_n = sudoku_4
    elif n == 5:
        sudoku_n = sudoku_5
    elif n == 6:
        sudoku_n = sudoku_6
    elif n == 7:
        sudoku_n = sudoku_7
    elif n == 8:
        sudoku_n = sudoku_8
    elif n == 9:
        sudoku_n = sudoku_9
    elif n == 10:
        sudoku_n = sudoku_10        
    else:
        print("Wrong number of sudoku!")

    for i in range(0, len(sudoku_n)):
        sudoku_n[i] = sudoku_n[i].replace('\n','')
        line = sudoku_n[i]
        sudoku_n[i] = [int(line[0])]
        for j in range(1, len(line)):
            sudoku_n[i].append(int(line[j]))
    return sudoku_n
        

def print_sudoku(sudoku_n):
    m = 0
    for i in range(0, 9):
        m += 1
        k = 0
        for j in range(0, 9):
            k += 1
            print(sudoku_n[i][j], end="")
            if k == 3 or k == 6:
                print(end=" ")
        print()
        if m == 3 or m == 6:
                print() 
    

def find_possibilities(sudoku_n, i, j):
    possibilities = [1,2,3,4,5,6,7,8,9]
        
    for k in range(0, 9):
        # cheking the line
        if not sudoku_n[i][k] == 0:
            if sudoku_n[i][k] in possibilities:
                possibilities.remove(sudoku_n[i][k])
        # checking the column
        if not sudoku_n[k][j] == 0:
            if sudoku_n[k][j] in possibilities:
                possibilities.remove(sudoku_n[k][j])            
    r = 0
    c = 0
    
    if i in [0,1,2]:
        r = 0
    elif i in [3,4,5]:
        r = 3
    else:
        r = 6
        
    if j in [0,1,2]:
        c = 0
    elif j in [3,4,5]:
        c = 3
    else:
        c = 6
    
    for x in range(r, r+3):
        for y in range(c, c+3):
            if not sudoku_n[x][y] == 0:
                if sudoku_n[x][y] in possibilities:
                    possibilities.remove(sudoku_n[x][y])                
    return possibilities

      
def find_empty(sudoku_n, i, j):
    for k in range(i, 9):
        for m in range(j, 9):
            if sudoku_n[k][m] == 0:
                i = k
                j = m
                return (i, j)
            if m == 8:
                j = 0
    return False
                
def Backtrack(sudoku_n, i, j):

    possibilities = []

    res = find_empty(sudoku_n, i, j)
    if res == False:
        return sudoku_n
    else:
        i,j = res
        
    possibilities = find_possibilities(sudoku_n, i, j)
    
    
    for k in possibilities:
        sudoku_n[i][j] = k
        Backtrack(sudoku_n, i, j)
        if find_empty(sudoku_n, i, j) == False:
            return sudoku_n
    sudoku_n[i][j] = 0
    
    return


# Main
sudokus = []
solutions = []


for i in range(1, 11):
    sudokus.append(read_file(i))

start_time = time.time()
for sudoku in sudokus:
    solutions.append(Backtrack(sudoku, 0, 0))
end_time = time.time()

i = 1
for solution in solutions:
    print("Sudoku ", i)
    print()
    print_sudoku(solution)
    print("-------------------------------------")
    i += 1
    
executed_time = end_time - start_time
print("Time of execution:", round(executed_time, 3), "s")