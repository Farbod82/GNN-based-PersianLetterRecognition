

from test2 import generate_coded_string, group_images

from knn import levinestein

file_name = "all_data.txt"



def classify(li):
    f = open(file_name,"r")
    least = 1000
    nearest_num = -1
    for i in range(10):
        f.readline()
        for j in range(2):
            line = f.readline()[:-1]
            line = line.split(" ")
            dif = levinestein(line,li)
            if dif < least:
                least = dif
                nearest_num = i
    f.close()
    return nearest_num

            











def identify_image(image_name):
    groups,h = group_images(image_name)
    keys = groups.keys()
    numbers_list = []
    if len(keys) == 0:
        print("no number")
        return
    for key in keys:
        X = [pair[1] for pair in groups[key]]
        Y = [(h - pair[0]) for pair in groups[key]]
        if len(X) > 20:
            li = generate_coded_string(X,Y,35)
            nearest_num = classify(li)
            numbers_list.append(nearest_num)
    return numbers_list






numbers_list = identify_image('8.png')
print(*numbers_list)
        


