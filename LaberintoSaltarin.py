import pygame
import numpy as np
from collections import deque

def LSDFS(mat, matrev, v, nr, m, n):
    if(mat[v[-1]]==0):
        return 0
    temp = 0
    vec = v
    matrev1 = matrev
    temp = mat[v[-1]]
    if(v[-1][0]+3<m and mat[int(v[-1][0]+temp)][v[-1][1]]):
        vec.append((int(v[-1][0]+temp),v[-1][1]))
        matrev1[vec[-1][0], vec[-1][1]] = 1
        temp1 = LSDFS(mat,matrev1,vec,nr,m,n) + 1 
        if(temp1 < temp):
            temp = temp1
        vec = v
        matrev1 = matrev
    if(v[-1][0]-3>=0 and mat[int(v[-1][0]-temp)][v[-1][1]]):
        vec.append((int(v[-1][0]-temp),v[-1][1]))
        matrev1[vec[-1][0], vec[-1][1]] = 1
        temp = LSDFS(mat,matrev1,vec,nr,m,n) + 1 
        if(temp1 < temp):
            temp = temp1
        vec = v
        matrev1 = matrev
    if(v[-1][1]+3<n and mat[v[-1][0]][int(v[-1][1]+temp)]):
        vec.append((v[-1][0],int(v[-1][1]+temp)))
        matrev1[vec[-1][0], vec[-1][1]] = 1
        temp = LSDFS(mat,matrev1,vec,nr,m,n) + 1 
        if(temp1 < temp):
            temp = temp1
        vec = v
        matrev1 = matrev
    if(v[-1][1]-3>=0 and mat[v[-1][0]][int(v[-1][1]-temp)]):
        vec.append((v[-1][0],int(v[-1][1]-temp)))
        matrev1[vec[-1][0], vec[-1][1]] = 1
        temp = LSDFS(mat,matrev1,vec,nr,m,n) + 1 
        if(temp1 < temp):
            temp = temp1
        vec = v
        matrev1 = matrev
    return temp

def LSBCU():
    return 0

def testing(mat,v,temp):
    temp1 = v[-1][0]+temp
    return mat[int(v[-1][0]+temp)][v[-1][1]]

def main():
    v=[(0,0)]
    with open('example.txt','r') as file:
        m = int(file.read(2))
        n = int(file.read(2))
        xs = int(file.read(2))
        ys = int(file.read(2))
        xe = int(file.read(2))
        ye = int(file.read(2))
        mat = np.zeros((m,n))
        matrev = np.zeros((m,n))
        for i in range(m):
            for j in range(n):
                mat[i][j] = int(file.read(2))
        file.close()
    print(n)
    print(m)
    print(xs)    
    print(ys)
    print(xe)
    print(ye)
    for i in range(m):
        for j in range(n):
            print(mat[i][j], end=" ")
        print()
    matrev[0][0] = 1
    print(LSDFS(mat,matrev,v,1,m,n))
    #print(testing(mat,v,mat[0][0]))
    return 0

if __name__ == "__main__":
    main()

#sol de example.txt son 13, no hay solucion, 20