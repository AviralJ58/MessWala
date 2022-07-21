import csv
import json

hostel=0
mess=0
hostel_dict={1:"MH", 2:"LH"}
mess_dict={1:"Special", 2:"Veg", 3:"NonVeg"}

hostel=int(input("Select the hostel type:\n1. MH\n2. LH\n"))
mess=int(input("Select the mess type:\n1. Special\n2. Veg\n3. Non-veg\n"))
menu=input("Enter the menu file path:\n")

if (hostel>2 or mess>3 or hostel<1 or mess<1):
    print("Invalid input")
    exit()

json_menu={"hostel":hostel,"mess":mess,"menu":[]}

with open(menu) as file_obj:
    reader_obj=csv.reader(file_obj)
    for row in reader_obj:
        menu_json={}
        menu_json["date"]=row[0]
        menu_json["menu"]=[]
        for i in range(1,len(row)):
            menu_json["menu"].append({"type":i,"menu":row[i].replace('\n',', ')})
        json_menu["menu"].append(menu_json)

# save as json file
with open('menu-'+hostel_dict[hostel]+'-'+mess_dict[mess]+'.json','w') as file_obj:
    json.dump(json_menu,file_obj)