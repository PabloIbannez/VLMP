import sys,os

VLMP_comp_path = "../VLMP/components/"

comptName = sys.argv[1]

#Check if component exists, it is a directory
if not os.path.isdir(VLMP_comp_path+comptName):
    print("Component "+comptName+" does not exist")
    sys.exit()
else:
    #List all files in the component directory
    files = os.listdir(VLMP_comp_path+comptName)
    #Print all files
    for file in files:
        if "__" not in file and ".py" in file:
            name = file.split(".")[0]
            #Print every file as a subsection in rst format
            print(name)
            print("-"*len(name))
            print("\n")
            print("This is the component of type "+comptName+" and name "+name)
            print("\n")
            print("\n")






