import pygame
import numpy as np
from collections import deque
import queue

def LSDFS(mat, matrev, m, n,xs,ys):
    stack = deque()
    stack.append([(xs,ys),0])
    while(len(stack) != 0):
        s = stack[-1][0]
        c = stack[-1][1]
        t = mat[s]
        if(int(t) == 0):
            return c
        stack.pop()
        if(s[0]+t<m and matrev[int(s[0]+t)][s[1]] == 0):
            stack.append([(int(s[0]+t),s[1]),c+1])
            matrev[int(s[0]+t)][s[1]] = c+1
        if(s[0]-t>=0 and matrev[int(s[0]-t)][s[1]] == 0):
            stack.append([(int(s[0]-t),s[1]),c+1])
            matrev[int(s[0]-t)][s[1]] = c+1
        if(s[1]+t<n and matrev[s[0]][int(s[1]+t)] == 0):
            stack.append([(s[0],int(s[1]+t)),c+1])
            matrev[s[0]][int(s[1]+t)] = c+1
        if(s[1]-t>=0 and matrev[s[0]][int(s[1]-t)] == 0):
            stack.append([(s[0],int(s[1]-t)),c+1])
            matrev[s[0]][int(s[1]-t)] = c+1
    return "not found"

def LSUCS(mat, matrev, m, n,xs,ys):    
    q = queue.PriorityQueue()
    q.put((0,(xs,ys)))
    while not q.empty():
        next = q.get()
        s = next[1]
        c = next[0]
        t = mat[s]
        if(int(t) == 0):
            return c
        if(s[0]+t<m and matrev[int(s[0]+t)][s[1]] == 0):
            q.put((c+1,(int(s[0]+t),s[1])))
            matrev[int(s[0]+t)][s[1]] = c+1
        if(s[0]-t>=0 and matrev[int(s[0]-t)][s[1]] == 0):
            q.put((c+1,(int(s[0]-t),s[1])))
            matrev[int(s[0]-t)][s[1]] = c+1
        if(s[1]+t<n and matrev[s[0]][int(s[1]+t)] == 0):
            q.put((c+1,(s[0],int(s[1]+t))))
            matrev[s[0]][int(s[1]+t)] = c+1
        if(s[1]-t>=0 and matrev[s[0]][int(s[1]-t)] == 0):
            q.put((c+1,(s[0],int(s[1]-t))))
            matrev[s[0]][int(s[1]-t)] = c+1
    return "not found"

def testing(mat,v,temp):
    s = (0,0)
    return mat[s]


def main():
    pygame.init()
    pygame.font.init()
    with open('example1.txt','r') as file:
        line = file.readline()
        pos =  0
        vars = []
        for i in range(len(line)):
            if line[i] == ' ':
                vars.append(int(line[pos:i]))
                pos = i+1
        vars.append(int(line[pos:]))
        mat = np.zeros((vars[0],vars[1]))
        matrev = np.zeros((vars[0],vars[1]))
        for i in range(vars[0]):
            line = file.readline()
            pos =  0
            j = 0
            for k in range(len(line)):
                if(line[k] == ' '):
                    mat[i][j] = int(line[pos:k])
                    pos = k+1
                    j = j+1
            mat[i][j] = int(line[pos:])
        file.close()
    for i in range(len(vars)):
        print(vars[i])
    for i in range(vars[0]):
        for j in range(vars[1]):
            print(mat[i][j], end=" ")
        print()
    matrev[vars[2]][vars[3]] = 1

    #Pygame Part Start
    fuente = pygame.font.Font(None, 30)
    ancho_celda = 50
    alto_celda = 50
    ancho_pantalla = vars[0] * ancho_celda
    alto_pantalla = vars[1] * alto_celda

    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    pygame.display.set_caption("Matriz en Pygame")

    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    AZUL = (0, 0, 255)



    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            # Aquí puedes agregar lógica para interactuar con la matriz,
            # por ejemplo, al hacer clic en una celda.

        pantalla.fill(BLANCO)  # Limpiar la pantalla
        for fila in range(vars[0]):
            for columna in range(vars[1]):
                valor = mat[fila][columna]
                if(int(valor) == 0):
                    texto = fuente.render("G", True, AZUL)
                elif(fila == vars[2] and columna == vars[3]):
                    texto = fuente.render(str(int(valor)), True, AZUL)
                else:
                    texto = fuente.render(str(int(valor)), True, NEGRO)
                texto_rect = texto.get_rect(center=(columna * ancho_celda + ancho_celda // 2,
                                                fila * alto_celda + alto_celda // 2))

                # Dibujar el fondo de la celda (opcional)
                pygame.draw.rect(pantalla, BLANCO, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda))

                # Dibujar el texto centrado
                pantalla.blit(texto, texto_rect)

                # Opcional: Dibujar un borde para que se vean las celdas
                pygame.draw.rect(pantalla, NEGRO, (columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda), 1)
        pygame.display.flip()  # Actualizar la pantalla
    pygame.quit()

    #Pygame Part End

    #print(LSDFS(mat,matrev,vars[0],vars[1],vars[2],vars[3]))
    print(LSUCS(mat,matrev,vars[0],vars[1],vars[2],vars[3]))
    #print(testing(mat,v,mat[0][0]))
    return 0

if __name__ == "__main__":
    main()

#sol de example.txt son 13, no hay solucion, 20