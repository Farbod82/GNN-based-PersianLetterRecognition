import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import *
from operator import add

def generate_coded_string(X_s,Y_s,n_of_points):



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
        for i in range(int((height*grid)/width)):
            for j in range(grid):
                ind_x.append(j*(width/grid))
                ind_y.append(i*(height/(int((height*grid)/width))))

        nop = int((height*grid)/width)* grid



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
    for i in range(n_of_points):
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
    for i in range(n_of_points):
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

    return vector_list





def group_images(file_name):
    img = cv2.imread(file_name,0)
    img = cv2.bitwise_not(img)
    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8)

    ret,img = cv2.threshold(img,127,255,0)



    img = cv2.bitwise_not(img)
    cv2.imshow("er", img)

    im = np.asarray(img)
    im = im.astype('int')




    h,w = np.shape(im)

    for i in range(h):
        for j in range(w):
            if im[i,j] == 255:
                im[i,j] = 0
            else:
                im[i,j] = -1


    groups = dict()
    count = 0



    for i in range(h-3):
        for j in range(w-3):
            part = im[i:i+3,j:j+3]
            if np.count_nonzero(part) == 0:
                continue
            colors = []
            temp_set = set()
            uncol = []
            for p in range(3):
                for q in range(3):
                    if part[p,q] != 0 and part[p,q] != -1:
                        colors.append((part[p,q], i+p,j+q))
                        temp_set.add(part[p,q])
                    if part[p,q] == -1:
                        uncol.append((i+p,j+q))
            if len(temp_set) > 1:
                color  = colors[0][0]
                for c in range(1,len(colors)):# uniting colors in filter adding new points to their group
                    col, p,q = colors[c]
                    groups[col].add((p,q))
                for c in temp_set:#updating colors in the whole image and uniting sets
                    if c != color:   
                        set2 = groups[c]
                        for pair in set2:
                            p, q = pair
                            im[p,q] = color
                        groups[color].update(set2)
                        del groups[c]
            elif len(temp_set) == 1:
                color = colors[0][0]
                for pair in uncol:
                    p, q = pair
                    im[p,q] = color
                    groups[color].add((p,q))
            else:
                if len(uncol) > 0:
                    count += 1
                    groups[count] = set()
                    for pair in uncol:
                        p,q = pair
                        im[p,q] = count
                        groups[count].add((p,q))
    return groups,h
        



#for key in groups.keys():
#     print(key)
#     X = [pair[1] for pair in groups[key]]
#     Y = [(h - pair[0]) for pair in groups[key]]
#     li = generate_coded_string(X,Y,35)
    


        
                
            
            


        
                    
            
        
            
        
