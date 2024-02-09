

from knn import generate_coded_string

save_file = "all_data.txt"



for i in range(10):
    f = open(save_file, "a")
    f.write(str(i) + ":")
    f.write("\n")
    for j in range(1,3):
        img_name= str(i)+ "_v" + str(j) + (".png")
        
        li = generate_coded_string(img_name,35)
        
        f.write(" ".join(li))
        f.write("\n")
    f.close()
        
