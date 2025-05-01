import pygame
import numpy as np
from collections import deque
import queue

pygame.init()
pygame.font.init()
fuente_boton = pygame.font.Font(None, 20)
fuente = pygame.font.Font(None, 20)
ancho_celda = 20
alto_celda = 20
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (200, 200, 200)
VERDE = (0, 255, 0)
AZUL_CLARO = (173, 216, 230)


def LSDFS(mat, matrev_original, vars, pantalla):
    matrev = matrev_original.copy()
    m = vars[0]
    n = vars[1]
    xs = vars[2]
    ys = vars[3]
    stack = deque()
    stack.append([(xs,ys),0])
    while(len(stack) != 0):
        s = stack[-1][0]
        pantalla.fill(BLANCO)
        dib_mat(mat, pantalla, vars, s)
        pygame.display.flip()
        pygame.time.delay(200)
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
    return "no hay solución"

def LSUCS(mat, matrev_original, vars, pantalla):    
    matrev = matrev_original.copy()
    m = vars[0]
    n = vars[1]
    xs = vars[2]
    ys = vars[3]
    q = queue.PriorityQueue()
    q.put((0,(xs,ys)))
    while not q.empty():
        next = q.get()
        s = next[1]
        pantalla.fill(BLANCO)
        dib_mat(mat, pantalla, vars, s)
        pygame.display.flip()
        pygame.time.delay(100)
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
    return "no hay solución"

def dib_mat(mat, pantalla, vars, act):
    for fila in range(vars[0]):
        for columna in range(vars[1]):
            valor = mat[fila][columna]
            if(int(valor) == 0):
                if(fila == act[0] and columna == act[1]):
                    texto = fuente.render("G", True, ROJO)
                else:
                    texto = fuente.render("G", True, AZUL)
            elif(fila == act[0] and columna == act[1]):
                texto = fuente.render(str(int(valor)), True, ROJO)
            elif(fila == vars[2] and columna == vars[3]):
                texto = fuente.render(str(int(valor)), True, AZUL)
            else:
                texto = fuente.render(str(int(valor)), True, NEGRO)
            texto_rect = texto.get_rect(center=((columna * ancho_celda + ancho_celda // 2)+ancho_celda // 2,(fila * alto_celda + alto_celda // 2)+alto_celda // 2))

            pantalla.blit(texto, texto_rect)

            pygame.draw.rect(pantalla, NEGRO, ((columna * ancho_celda)+ancho_celda // 2, (fila * alto_celda)+alto_celda // 2, ancho_celda, alto_celda), 1)

def dib_txt(text, x, y, pantalla):
    texto_render = fuente.render(str(text), True, NEGRO)
    pantalla.blit(texto_render, (x,y))

class Boton:
    def __init__(self, texto, x, y, ancho, alto, color_normal, color_hover, color_click, funcion):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_click = color_click
        self.color_actual = self.color_normal
        self.funcion = funcion
        self.texto_render = fuente_boton.render(self.texto, True, NEGRO)
        self.texto_rect = self.texto_render.get_rect(center=self.rect.center)
        self.presionado = False

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color_actual, self.rect)
        superficie.blit(self.texto_render, self.texto_rect)

    def change_size(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto_rect = self.texto_render.get_rect(center=self.rect.center)

    def manejar_evento(self, evento, superficie, mat, matrev, vars):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                self.presionado = True
                self.color_actual = self.color_click
                return self.funcion(mat, matrev, vars, superficie)
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and self.rect.collidepoint(evento.pos) and self.presionado:
                self.color_actual = self.color_hover
            else:
                self.color_actual = self.color_normal
            self.presionado = False
        elif evento.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(evento.pos):
                self.color_actual = self.color_hover
            else:
                self.color_actual = self.color_normal
        return -1

class CuadroTexto:
    def __init__(self, x, y, ancho, alto, texto=''):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = BLANCO
        self.color_borde_activo = AZUL_CLARO
        self.color_borde_inactivo = NEGRO
        self.color_borde_actual = self.color_borde_inactivo
        self.texto = texto
        self.fuente_render = fuente.render(self.texto, True, NEGRO)
        self.activo = False

    def change_size(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.activo = not self.activo
            else:
                self.activo = False
            self.color_borde_actual = self.color_borde_activo if self.activo else self.color_borde_inactivo
            self.color = AZUL_CLARO if self.activo else BLANCO
        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_RETURN:
                    ret = self.texto
                    self.texto = '' 
                    self.fuente_render = fuente.render(self.texto, True, NEGRO)
                    return ret
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    self.texto += evento.unicode
                self.fuente_render = fuente.render(self.texto, True, NEGRO)
        return "-1"

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect, 2)
        pygame.draw.rect(superficie, self.color_borde_actual, self.rect, 2) 
        superficie.blit(self.fuente_render, self.rect)

def data_extract(s):
    with open('example'+s+'.txt','r') as file:
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
    matrev[vars[2]][vars[3]] = 1

    ancho_pantalla = vars[1] * ancho_celda*2
    alto_pantalla = vars[0] * alto_celda*2
    if(vars[0] < 5):
        alto_pantalla = 5 * ancho_celda*2

    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    pygame.display.set_caption("Matriz en Pygame")
    return ancho_pantalla, alto_pantalla, pantalla, vars, mat, matrev


def main():
    ancho_pantalla, alto_pantalla, pantalla, vars, mat, matrev = data_extract("1")

    boton_DFS = Boton("DFS", ((3*ancho_pantalla)//4)-ancho_celda, ((alto_pantalla)//6)-alto_celda, 3*ancho_celda, 2*alto_celda, GRIS, VERDE, (0, 150, 0), LSDFS)
    boton_UCS = Boton("UCS", ((3*ancho_pantalla)//4)-ancho_celda, (5*(alto_pantalla)//12)-alto_celda, 3*ancho_celda, 2*alto_celda, GRIS, VERDE, (0, 150, 0), LSUCS)
    cuadro_texto = CuadroTexto(((3*ancho_pantalla)//4)-ancho_celda, (7*(alto_pantalla)//12), 3*ancho_celda, alto_celda)
    last_result_DFS = -1
    last_result_UCS = -1
    error_file = 0
    file_to_read = '-1'

    ejecutando = True
    while ejecutando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            result_DFS = boton_DFS.manejar_evento(evento,pantalla,mat,matrev,vars)
            result_UCS = boton_UCS.manejar_evento(evento,pantalla,mat,matrev,vars)
            file_to_read=cuadro_texto.manejar_evento(evento)
            if(result_DFS != -1):
                last_result_DFS = result_DFS
                last_result_UCS = -1
                error_file = 0
            if(result_UCS != -1):
                last_result_UCS = result_UCS
                last_result_DFS = -1
                error_file = 0
            if(file_to_read != "-1"):
                try:
                    ancho_pantalla, alto_pantalla, pantalla, vars, mat, matrev = data_extract(file_to_read)
                    boton_DFS.change_size(((3*ancho_pantalla)//4)-ancho_celda, ((alto_pantalla)//6)-alto_celda, 3*ancho_celda, 2*alto_celda)
                    boton_UCS.change_size(((3*ancho_pantalla)//4)-ancho_celda, (5*(alto_pantalla)//12)-alto_celda, 3*ancho_celda, 2*alto_celda)
                    cuadro_texto.change_size(((3*ancho_pantalla)//4)-ancho_celda, (7*(alto_pantalla)//12), 3*ancho_celda, alto_celda)
                except:
                    error_file = 1
                    last_result_DFS = -1
                    last_result_UCS = -1
                file_to_read = "-1"

        pantalla.fill(BLANCO)
        boton_DFS.dibujar(pantalla)
        boton_UCS.dibujar(pantalla)
        cuadro_texto.dibujar(pantalla)
        if(last_result_DFS != -1):
            dib_txt(last_result_DFS, ((3*ancho_pantalla)//4)-3*ancho_celda, ((11*alto_pantalla)//12)-alto_celda, pantalla)
        if(last_result_UCS != -1):
            dib_txt(last_result_UCS, ((3*ancho_pantalla)//4)-3*ancho_celda, ((11*alto_pantalla)//12)-alto_celda, pantalla)
        if(error_file == 1):
            dib_txt("File Error", ((3*ancho_pantalla)//4)-3*ancho_celda, ((11*alto_pantalla)//12)-alto_celda, pantalla)
        dib_mat(mat, pantalla, vars, (-1,-1))
        pygame.display.flip()
    pygame.quit()
    return 0

if __name__ == "__main__":
    main()
