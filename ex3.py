# -*- coding: utf-8 -*-
from dateutil.parser import parse

"""
Created on Thu May  6 18:28:31 2021

@author: o
"""
def is_date(string):
    """
    Return whether the string can be interpreted as a date.
    """
    try: 
        parse(string)
        return True
    except ValueError:
        return False
    
    
def messages (file):  
    fhand = open(file,'r',encoding='UTF-8')
    phones_book = []
    id = 0 
    text=" " 
    data = []
    datetime_arr = []

    for line in fhand :
        line= line.strip()
        if 'נוצרה'in line or '<המדיה לא נכללה> 'in line or 'הוסיף/ה' in line or'מוצפנות' in line :
            continue 
        line= line.strip() 
        splitted_line = line.split(",")
        
        if not is_date(splitted_line[0]): #continue with the previos messsage
           data[id-1]["text"] = text+" "+line
        else:                               #new message
           datetime_and_data = line.split(" - ")  
           datetime_arr = datetime_and_data[0].split(",")
           phone = datetime_and_data[1].split(":")[0]
           text = datetime_and_data[1].split(":")[1]

           if phone in phones_book:
               given_id=phones_book.index(phone)
               data.append({"datetime":datetime_arr[1]+ " "+datetime_arr[0], "id" :given_id,"text": text})
           else:
               phones_book.append(phone)
               data.append({"datetime":datetime_arr[1]+ " "+datetime_arr[0], "id" :id,"text": text})
               id=id+1
           
    fhand.close()
    return data

def people_num(file):
    data = messages(file)
    max_id = 0
    for x in data:
        id = x["id"]
        if (id > max_id):
            max_id = id
    return max_id + 1

def create_group(file):
    data = messages(file)
    return data[0]["datetime"]
   
def creator(file):
    fhand = open(file,'r',encoding='UTF-8')
    for line in fhand :
        line= line.strip()
        if  'הוסיף/ה' in line:
            datetime_and_data = line.split(" - ")  
            return datetime_and_data[1].split(" ")[0]
            

def metadata(file):
    file_name = file
    people = "<"+str(people_num(file))+">"
    create = create_group(file)
    leader = creator(file)
    dict = {"name_chat": file_name, "date_creation": create, "num_of_participants": people, "creator": leader}
    return dict

def all_in_one(file):
    dict = {"messages": messages(file), "metadata": metadata(file)}
    return dict

def print_to_txt(file):
    all_data = all_in_one(file)
    f = open(file, "w", encoding='UTF-8')
    f.write(str(all_data))
    
file=input("Enter the filename : ")
print_to_txt(file)