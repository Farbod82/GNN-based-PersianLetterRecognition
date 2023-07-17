import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('1.png',0)
img = cv2.bitwise_not(img)
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
 
ret,img = cv2.threshold(img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False

 
while( not done):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy()
 
    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        done = True
 
skel = cv2.bitwise_not(skel)


cv2.imshow("er", skel)

im = skel.astype('int')




h,w = np.shape(im)

for i in range(h):
    for j in range(w):
        if im[i,j] == 255:
            im[i,j] = 0
        else:
            im[i,j] = -1

keys = set()


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



for key in groups.keys():
    print(key)
    X = [pair[1] for pair in groups[key]]
    Y = [(h - pair[0]) for pair in groups[key]]
    plt.scatter(X,Y)
    plt.show()


        
                
            
            


        
                    
            
        
            







# tx = []
# ty = []
# X = []
# y_ind = []
# Y_s = []
# for i in range(np.shape(img)[0]):
#     temp = []
#     for j in range(np.shape(img)[1]):
#         if img[i,j] == 0:
#             temp.append(j+1)
#     X = []
#     if(len(temp) > 1):
#         for j in range(len(temp)-1):
#             if temp[j+1] - temp[j] > 5: 
#                 X.append((temp[j] + temp[j+1])/2)
#                 tx.append((temp[j] + temp[j+1])/2)
#                 ty.append( np.shape(img)[0] - i -1)

#     if X:
#         Y_s.append(X)
#         y_ind.append(np.shape(img)[0] - i +1)






# for i in range(len(Y_s)):
#     Y_s[i].sort()



# plt.scatter(tx,ty)
# plt.show()

# groups =[]




# while True:
#     last_x = -1
#     last_y = -1
#     temp = []
#     for i in range(len(Y_s)):
    
#         if len(Y_s[i]) > 0:
#             if (last_x == -1 or (abs(last_x - Y_s[i][0] ) < 10 and abs(last_y - y_ind[i]) < 3)):
#                 last_y = y_ind[i]
#                 last_x = Y_s[i].pop(0)
#                 temp.append((last_x,last_y))
#     if not temp:
#         break
#     else:
#         if len(temp) > 20:
#             groups.append(temp)



# h = np.shape(img)[0]
# w = np.shape(img)[1]
# for g in groups:
#     X = [i[0] for i in g]
#     Y = [i[1] for i in g]
#     #plt.scatter(X,Y)
#     #plt.show()

#     fail = 0
#     if len(X) > 20 :
#         X = np.asarray(X)
#         Y = np.asarray(Y)
#         arg = np.argmin(X)
#         x_min = X[arg]
#         y_min = Y[arg]
#         arg = np.argmax(X)
#         x_max = X[arg]
#         y_max = Y[arg]

#         part = img[:h - int(y_max),int(x_max)]
#         for i in range(len(part)):
#             if part[i] == 0:
#                 fail = 1
#                 break
#         if y_min < h:
#             part = img[h - int(y_min) -1 :h,int(x_min)]
#             for i in range(len(part)):
#                 if part[i] == 0:
#                     fail = 1
#                     break
#         if fail == 0:
#             plt.scatter(X,Y)
#             plt.show()



        


        



# h = int(max(Y))
# w = int(max(X))

# table = np.zeros((h,w))
# for i in range(len(X)):
#     table[int(Y[i])-1][int(X[i])-1] =  1

# count = 1

# groups = []




# while True:
#     temp = []
#     for i in range(h):
#         last_i = -1
#         last_j = -1
#         for j in range(w):
#             if table[i][j] == 1:
#                 if(last_i == -1 or (abs(last_j - j) < 5 and abs(last_i - i) < 3)):
#                     last_i = i
#                     last_j = j
#                     temp.append((j,h-i))
#                     table[i][j] = 0
#                 break

#     if len(temp) == 0:
#         break
#     else:
#         groups.append(temp)

# for i in range(len(groups)):
#     x = [j[0] for j in groups[i]]
#     y = [j[1] for j in groups[i]]
#     plt.scatter(x,y)
#     plt.show()
    
            




        

