import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from math import *
from operator import add
           


def levinestein(a,b):
    table = [[0]*(len(b)+1) for i in range(len(a)+1)]
    for i in range(len(a)+1):
        table[i][0] = i
    for j in range(len(b)+1):
        table[0][j] = j
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            if(a[i-1] == b[j-1]):
                table[i][j] = min(table[i-1][j]+1,table[i][j-1]+1,table[i-1][j-1])
            else:
                table[i][j] = min(table[i-1][j]+1,table[i][j-1]+1,table[i-1][j-1]+1)
    return table[len(a)][len(b)]
    





def generate_coded_string(image_path,n_of_points):
    image = Image.open(image_path)


    gray_img = image.convert("L")


    X_s = []
    Y_s = []


    for x in range(gray_img.width):
        for y in range(gray_img.height):
            if gray_img.getpixel((x,y)) < 128:
                X_s.append(x)
                Y_s.append(gray_img.height - y)


    h = gray_img.height
    w = gray_img.width
    X = np.asarray(X_s)
    Y = np.asarray(Y_s)

    X = np.asarray(X)
    Y = np.asarray(Y)
    width = 100
    height = (np.max(Y)*width)/np.max(X)
    X -=  np.min(X)
    Y -=  np.min(Y)
    X = X * (width/np.max(X))
    Y = Y * (height/np.max(Y))

    plt.scatter(X,Y)
    plt.show()
   

    


    grid = n_of_points
    while True:


        ind_x = []
        ind_y = []
        for i in range(int((h*grid)/w)):
            for j in range(grid):
                ind_x.append(j*(gray_img.width/grid))
                ind_y.append(i*(gray_img.height/(int((h*grid)/w))))

        nop = int((h*grid)/w)* grid



        ind_x = np.asarray(ind_x)
        ind_y = np.asarray(ind_y)




        categ_x = [[] for i in range(nop)]
        categ_y = [[] for i in range(nop)]

        for i in range(len(X)):
            x1 = X[i]
            y1 = Y[i]
            temp_x = ind_x - x1
            temp_y = ind_y - y1
            dist = np.square(temp_x) + np.square(temp_y)
            min_ind = np.argmin(dist)
            categ_x[min_ind].append(x1)
            categ_y[min_ind].append(y1)
        

        fin_x = []
        fin_y = []


        for i in range(nop):
            if(categ_x[i]):
                fin_x.append(sum(categ_x[i])/len(categ_x[i]))
                fin_y.append(sum(categ_y[i])/len(categ_y[i]))
        
        if(len(fin_x) >= n_of_points):
            break
        else:
            nop+= 1
    k = 0
    while len(fin_x) != n_of_points:
        if k >= len(fin_x):
            k = 0
        x1 = fin_x[k]
        y1 = fin_y[k]
        temp_x = [(x - x1)**2 for x in fin_x]
        temp_y = [(y - y1)**2 for y in fin_y]
        temp = list(map(add, temp_x,temp_y))
        temp.pop(k)
        temp = np.asarray(temp)
        ind = np.argmin(temp)
        #fin_x[ind] = (fin_x[ind] + fin_x[k])/2
        #fin_y[ind] = (fin_y[ind] + fin_y[k])/2
        fin_x[ind] = max(fin_x[ind] , fin_x[k])
        fin_y[ind] = max(fin_y[ind] , fin_y[k])
        fin_x.pop(k)
        fin_y.pop(k)
        k+=1

    # fin_x = np.asarray(fin_x)
    # fin_y = np.asarray(fin_y)
    # width = 300
    # height = (np.max(fin_y)*width)/np.max(fin_x)
    # fin_x -=  np.min(fin_x)
    # fin_y -=  np.min(fin_y)
    # fin_x = fin_x * (width/np.max(fin_x))
    # fin_y = fin_y * (height/np.max(fin_y))




    plt.scatter(fin_x,fin_y)
    plt.show()
    #dist_part = 7
    ratio = 12
    li = []
    x_mean = sum(fin_x)/len(fin_x)
    y_mean = sum(fin_y)/len(fin_y)
    
    dists = np.square(np.asarray(fin_x) - x_mean) + np.square(np.asarray(fin_y) - y_mean)
    for i in range(len(fin_x)):
        tan = abs((fin_y[i]- y_mean)/(fin_x[i]-x_mean))
        deg = degrees(atan(tan))
        if fin_x[i] - x_mean !=0:
            if (fin_y[i] >= y_mean):
                    if(fin_x[i] > x_mean):
                        deg = deg
                    else:
                        deg = 180 - deg
            else:
                if(fin_x[i] > x_mean):
                    deg = 360 - deg
                else:
                    deg = 180 + deg         
        else: 
            if(fin_y[i] > y_mean):
                deg =  90
            else:
                deg = 270
        deg %= 360
        li.append((deg, i))

    li.sort()
    vector_list = []
    for i in range(len(fin_x)):
        deg, point = li[i]
        for seg in range(ratio):
            if deg >= seg*(360/ratio) and deg < (seg+1)*(360/ratio):
                part1  = (seg + 1)
                break
        # for seg in range(dist_part):
        #     if dists[point] >= seg*(max(dists)/dist_part) and dists[point] <= (seg+1)*(max(dists)/dist_part):
        #         part2 = (seg+1)
        #         break
        vector_list.append(str(part1))
        #vector_list.append(str(part2))


    


    # for i in range(len(fin_x)-1):
    #      if fin_x[i+1] != fin_x[i]:
    #          tan = abs((fin_y[i+1]- fin_y[i])/(fin_x[i+1]-fin_x[i]))
    #          deg = degrees(atan(tan))
    #          if (fin_y[i+1] >= fin_y[i]):
    #              if(fin_x[i+1] > fin_x[i]):
    #                  deg = deg
    #              else:
    #                  deg = 180 - deg
    #          else:
    #              if(fin_x[i+1] > fin_x[i]):
    #                  deg = 360 - deg
    #              else:
    #                  deg = 180 + deg         
    #      else: 
    #          if(fin_y[i+1] > fin_y[i]):
    #              deg =  90
    #          else:
    #              deg = 270
    #      deg %= 360
    #      for seg in range(vector_seg):
    #          if deg >= seg*(360/vector_seg) and deg < (seg+1)*(360/vector_seg):
    #              vector_list.append(seg + 1)
    #              break
    return vector_list

# vl1  = generate_coded_string("0.png",25,7)
# vl2 = generate_coded_string("5.png",25,8)

#vl3 = generate_coded_string("78.png",40,7)
#vl4 = generate_coded_string("75.png",40,7)
#vl2 = generate_coded_string("5.png", 35,7)
# print(levinestein(vl1,vl2))



    

