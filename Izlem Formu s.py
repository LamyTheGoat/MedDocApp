#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 0th: import modules
import pandas as pd
import os
import numpy as np
from tkinter import *
from tkinter import ttk,dialog
from tkinter import font as tkfont
import json
import ast
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")


# In[2]:


## 1st: Check if database exists; if so load, if not create


# In[3]:


data_columns = ['op id','Tarih','Ad','Soyad','Yaş','Cinsiyet','Cep Telefonu','TC Kimlik No','Adres','Yakınma','Fizik Muayene','Plan']
file_data=pd.DataFrame(columns=data_columns)
if (os.path.isfile('./data.csv')):
    file_data = pd.read_csv('./data.csv', index_col=[0], dtype= str)
file_data.to_csv('./data.csv')
file_data



# In[4]:


for row in data_columns:
    file_data[row] = file_data[row].astype(str)
    
file_data["op id"] = [int(float(i)) for i in file_data["op id"]]


age_dum = file_data['Yaş']
for i in range(len(age_dum)):
    try:
        if('.' in str(age_dum[i])):
            age_dum[i] = str(age_dum[i])[0:str(age_dum[i]).find('.')]
    except:
        pass
file_data['Yaş'] = age_dum;
age_dum = None

tel_dum = file_data['Cep Telefonu']
for i in range(len(tel_dum)):
    try:
        if('.' in str(tel_dum[i])):
            tel_dum[i] = str(tel_dum[i])[0:str(tel_dum[i]).find('.')]
    except:
        pass
file_data['Cep Telefonu'] = tel_dum;
tel_dum = None

id_dum = file_data['TC Kimlik No']
for i in range(len(id_dum)):
    try:
        if('.' in str(id_dum[i])):
            id_dum[i] = str(id_dum[i])[0:str(id_dum[i]).find('.')]
    except:
        pass
file_data['TC Kimlik No'] = id_dum;
id_dum = None

for i in data_columns:
    if(i != 'op id'):
        for j in file_data.index:
            #print(str(i)+":"+str(j))
            if(file_data[i][j] == 'nan'):
                file_data[i][j] = ''
        


city_file = open("cities.txt", "r", encoding='utf-8')
contents = city_file.read()
my_city_dict = ast.literal_eval(contents)
my_city_tuple= tuple(my_city_dict.keys())
city_file.close()

file_data
foreground='black'


# In[5]:


# 2nd: Define the functions that will manipulate the database
display_data = pd.DataFrame()
def refreshDisplay():
    global display_data
    display_data = file_data

refreshDisplay()
def addElement(element):
    data_added = pd.DataFrame(element, columns=data_columns)
    data_added.index.name='id'
    global file_data
    file_data = file_data.append(data_added,ignore_index=True)
    saveData(file_data)
    refreshDisplay()
    return file_data


    
def createElement(opid, date, name, last_name, age, sex, ph_number, id_no, location, complain, inspection, plan):
    element= ([[opid, str(date), str(name), str(last_name), str(age), str(sex), str(ph_number), str(id_no), str(location), (complain), (inspection), (plan)]])
    return element

def createTableElement(date, name, last_name, age, sex, ph_number, id_no, location, complain, inspection, plan):
    opid =0
    if(len(file_data['op id'])>0):
        opid = int(max(file_data['op id'])) +1
    element= ([[opid, str(date), str(name), str(last_name), str(age), str(sex), str(ph_number), str(id_no), str(location), (complain), (inspection), (plan)]])
    return element

def removeElement(op_id):
    global file_data
    file_data = file_data[(file_data["op id"]) != op_id]
    saveData(file_data)
    refreshDisplay()
    return file_data
    
def editElement(op_id, element):
    global file_data
    file_data.loc[file_data['op id'] == op_id] = element;
    saveData(file_data)
    refreshDisplay()
    return file_data

def saveData(data):
    data.to_csv('./data.csv')  
    
def contains(element, array):
    l = []
    for i in array:
        l.append(element in str(i))
    return l
    
def searchElement(element, tree):
    if(element == "" or element == None):
        refreshDisplay()
        updateTree(tree)
    else:
        opid = element
        try:
            opid = int(element)
        except ValueError:
            pass
        element= str(element)
        element=element.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c')
        #print(element)
        #print(list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Soyad'])))
        condition = (opid == file_data['op id']) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Tarih']))) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Ad']))) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Soyad']))) | contains(element, file_data['Cep Telefonu']) | contains(element, file_data['TC Kimlik No']) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Adres']))) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Yakınma']))) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Fizik Muayene']))) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Plan']))) |  contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Soyad']))) | contains(element, file_data['Yaş']) | contains(element, list(map(lambda x:x.lower().replace('ş','s').replace('ğ','g').replace('ı','i').replace('ü','u').replace('ö','o').replace('ç','c'),file_data['Cinsiyet'])))
        global display_data
        display_data = file_data[condition]
        updateTree(tree)


# In[6]:


# 3rd: Create gui and define basic operations

#update tree function
def updateTree(datatree):
    #clear tree
    for i in datatree.get_children():
        datatree.delete(i)
    #put dataframe data in tree
    data_rows = display_data.to_numpy().tolist()
    for row in data_rows:
        
        row[9] = row[9].split("\n")[0]
        row[10] = row[10].split("\n")[0]
        row[11] = row[11].split("\n")[0]
        ##print(row)
        datatree.insert("","end",values=row)
        
    return


#delete selection function   
def deleteSelection(datatree, selected):
    op_id = datatree.item(selected)['values'][0]
    removeElement(op_id)
    #print(condition)
    datatree.delete(selected)
        



# In[7]:


# 3.1: Create data addition form window
def patient_add_form_window(tree, numVar):
    ap = Tk()
    ap.resizable(height = True, width = True)
    ap.geometry("520x570")
    ap.title("Hasta Ekleme Formu")
    ap.iconbitmap('icon.ico')
    
    add_patient = Frame(ap)
    
    myfont = ("Arial", 8, "bold") 
    mypady=5
    


    heading= Label(add_patient,text='Hasta Ekleme Formu', bg='grey', fg="white", width="500", height="3")
    heading.pack()
    
    
    
    
    #Defining variables for values
    date       = StringVar()
    firstname  = StringVar()
    lastname   = StringVar()
    age        = StringVar()
    sex        = StringVar()
    tel        = StringVar()
    tc         = StringVar()
    adress_c   = StringVar()
    adress_t   = StringVar()
    adress_l   = StringVar()
    complain   = StringVar()
    inspection = StringVar()
    plan       = StringVar()
    ################################
    
    
    
    
    CP_form_frame = Frame(add_patient)
    #Defining Frames for each row##########################
    rowframe1 = Frame(CP_form_frame)
    date_text       = Label(rowframe1, text='Tarih                ', font= myfont)
    date_text.pack(pady=mypady, padx=5, side="left")
    date_entry      = Entry(rowframe1, textvariable= date, font= myfont)
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y") 
    date_entry.insert(0, date_time)
    date_entry.pack(pady=mypady, padx=5, side="left")
    rowframe1.pack(anchor="w")


    rowframe2 = Frame(CP_form_frame)
    firstname_text  = Label(rowframe2, text='İsim                 ', font= myfont)
    lastname_text   = Label(rowframe2, text='Soyisim ', font= myfont)
    firstname_entry  = Entry(rowframe2, textvariable= firstname, font= myfont)
    lastname_entry   = Entry(rowframe2, textvariable= lastname, font= myfont)
    
    firstname_text.pack(padx=5, pady=mypady, side="left")
    firstname_entry.pack(padx=6, pady=mypady,  side="left")
    
    lastname_text.pack(padx=5, pady=mypady,  side="left")
    lastname_entry.pack(padx=5, pady=mypady,  side="left")
    
    rowframe2.pack(anchor="w")
    
    
    rowframe3 = Frame(CP_form_frame)
    age_text        = Label(rowframe3, text='Yaş                   ', font= myfont)
    sex_text        = Label(rowframe3, text='Cinsiyeti', font= myfont)
    age_entry        = Entry(rowframe3, textvariable= age, font= myfont)
    sex_entry        = ttk.Combobox(rowframe3, textvariable= sex, state='readonly', font=myfont)
    sex_entry['values'] = ('Erkek',
                           'Kadın',
                           'Diğer',
                           'Belirtilmemiş')
    
    
    
    
    
    age_text.pack(padx=5, pady=mypady, side="left")
    age_entry.pack(padx=4, pady=mypady, side="left")
    
    sex_text.pack(padx=5, pady=mypady, side="left") 
    sex_entry.pack(padx=5, pady=mypady, side="left")
    
    rowframe3.pack(anchor="w")
    
    rowframe4 = Frame(CP_form_frame)
    tel_text        = Label(rowframe4, text='Cep Telefonu ', font= myfont)
    tc_text         = Label(rowframe4, text='TC No     ', font= myfont)
    tel_entry        = Entry(rowframe4, textvariable= tel, font= myfont)
    tc_entry         = Entry(rowframe4, textvariable= tc, font= myfont)
    
    tel_text.pack(padx=5, pady=mypady, side="left")
    tel_entry.pack(padx=5, pady=mypady, side="left")
    
    tc_text.pack(padx=5, pady=mypady, side="left")
    tc_entry.pack(padx=5, pady=mypady, side="left")
    
    rowframe4.pack(pady=5,anchor="w")
    
    
    rowframe5 = Frame(CP_form_frame)
    subframe5 = Frame(rowframe5)
    adress_text     = Label(subframe5, text='Adres               ', font= myfont)
    adress_text.pack()
    subframe5.pack(side="left", padx=5, pady=mypady)
    adress_entry_c   = ttk.Combobox(rowframe5, textvariable= adress_c, font= myfont)
    adress_entry_c['values']= my_city_tuple
    adress_entry_l   = ttk.Entry(rowframe5, textvariable= adress_l, font= myfont)
    adress_entry_c.pack(padx=2, pady=10, side="left")
    adress_entry_l.pack(padx=2, pady=10, side="left")
    
    rowframe5.pack(pady=5,anchor="w")
    
    
    rowframe6= Frame(CP_form_frame)
    subframe6 = Frame(rowframe6)
    complain_text   = Label(subframe6, text='Yakınma           ', font= myfont)
    complain_text.pack(pady=2, padx =5, side="top")
    subframe6.pack(side="left", padx=5, pady=mypady)
    
    
    complain_entry   = Text(rowframe6, height=4, font= myfont, wrap="word")
    complain_entry.pack(pady=10, side="left")
    
    rowframe6.pack(anchor="w")
    
    
    rowframe7 = Frame(CP_form_frame)
    
    subframe7 = Frame(rowframe7)
    inspection_text = Label(subframe7, text='Fizik Muayene', font= myfont)
    inspection_text_2 = Label(subframe7, text='(US)', font= myfont)
    inspection_text.pack(pady=2, padx =5, side="top")
    inspection_text_2.pack(pady=2, padx =5, side="top")
    subframe7.pack(side="left", padx=5, pady=mypady)
    
    
    inspection_entry   = Text(rowframe7, height=6, font= myfont, wrap="word")
    inspection_entry.pack(pady=mypady, side="left")
    
    rowframe7.pack(anchor="w")
    
    
    rowframe8= Frame(CP_form_frame)
    subframe8 = Frame(rowframe8)
    plan_text       = Label(subframe8, text='Plan                  ', font= myfont)
    plan_text.pack(pady=2, padx =6, side="top")
    subframe8.pack(side="left", padx=5, pady=mypady)
    
    plan_entry       = Text(rowframe8, height=3, font= myfont, wrap="word")
    plan_entry.pack(pady=mypady, side="left")
    
    rowframe8.pack(anchor="w")
    ########################################################
    
    CP_form_frame.pack()
    
    
    
    

    
    
   

    
    
    
    
    
    


    

    #tel_text.place(x=10, y=180)
    #tc_text.place(x=250, y=180)
    #adress_text.place(x=10, y=220)
    #complain_text.place(x=10, y=320)
    #inspection_text.place(x=10, y=500)
    #inspection_text_2.place(x=10, y=520)
    #plan_text.place(x=10, y=600)









    

    

    


    
    

    ##REGISTER FUNCTION
    def register_patient():
        age=''
        tel=''
        tc=''
        
        date = date_entry.get()
        firstname = firstname_entry.get()
        lastname = lastname_entry.get()

        try:
            age_a = int(age_entry.get()) if (age_entry.get() != None and age_entry.get() != '' and age_entry.get() != 'nan') else 'nan'
            age = str(age_entry.get())
        except ValueError:
            error_text.config(text='Hata: Lütfen Yaş, TC Kimlik Numarası ve Telefon Numarası alanlarının\n numerik bir girdi olduğuna emin olunuz.\n Bir değer girmeyecekseniz lütfen boş bırakınız')
            return
        try:
            tel_a = int(tel_entry.get()) if (tel_entry.get() != None and tel_entry.get() != '' and tel_entry.get() != 'nan') else 'nan'
            tel = str(tel_entry.get())
        except ValueError:
            error_text.config(text='Hata: Lütfen Yaş, TC Kimlik Numarası ve Telefon Numarası alanlarının\n numerik bir girdi olduğuna emin olunuz.\n Bir değer girmeyecekseniz lütfen boş bırakınız')
            return
        try:
            tc_a = int(tc_entry.get()) if (tc_entry.get() != None and tc_entry.get() != '' and tc_entry.get() != 'nan') else 'nan'
            tc = str(tc_entry.get())
        except ValueError:
            error_text.config(text='Hata: Lütfen Yaş, TC Kimlik Numarası ve Telefon Numarası alanlarının\n numerik bir girdi olduğuna emin olunuz.\n Bir değer girmeyecekseniz lütfen boş bırakınız')
            return

        sex = sex_entry.get()
        adress = adress_entry_l.get()+", "+adress_entry_c.get()
        complain = complain_entry.get(1.0,END)
        inspection = inspection_entry.get(1.0,END)
        plan = plan_entry.get(1.0,END)
            
        
        
        row=createTableElement(
        date,
        firstname,
        lastname,
        age,
        sex,
        tel,
        tc,
        adress,
        complain,
        inspection,
        plan
        )
        addElement(row)
        value = row[0]
        try:
            value[6] = str(value[6])
        except:
            pass
        try:
            value[7] = str(value[7])
        except:
            pass
        try:
            value[4] = str(value[4])
        except:
            pass
        value[10] = value[10].split("\n")[0]
        value[11] = value[11].split("\n")[0]
        value[9] = value[9].split("\n")[0]
        tree.insert("","end",values=value);
        numVar.set("Kayıtlı Hasta Sayısı: " +str(len(file_data["op id"])))
        

        ap.destroy()

    reg_button= Button(add_patient, text="Hastayı Kaydet", command = register_patient, bg='orange',fg=foreground, width="20", font=myfont)
    reg_button.pack(padx=10, pady= mypady+5)
    
    error_text = Label(add_patient, text='')
    error_text.pack()
    
    add_patient.pack(padx=10, pady=mypady)
    
    ap.mainloop()


# In[8]:


# 3.2: Create data editing form window
def patient_edit_form_window(tree, selected):
    ep = Tk()
    ep.resizable(height = True, width = True)
    ep.geometry("520x570")
    ep.title("Hasta Düzenleme Formu")
    ep.iconbitmap('icon.ico')
    
    edit_patient = Frame(ep)
    
    myfont = ("Arial", 8, "bold") 
    mypady = 5;


    heading= Label(edit_patient,text='Hasta Düzenleme Formu', bg='grey', fg="white", width="500", height="3")
    heading.pack()

    values= tree.item(selected)['values']
    op_id=values[0]
    values = file_data[file_data["op id"] == op_id]
    values = (values.iloc[0])




       
    
    
    
    #Defining variables for values
    date       = StringVar()
    firstname  = StringVar()
    lastname   = StringVar()
    age        = StringVar()
    sex        = StringVar()
    tel        = StringVar()
    tc         = StringVar()
    adress_c   = StringVar()
    adress_t   = StringVar()
    adress_l   = StringVar()
    complain   = StringVar()
    inspection = StringVar()
    plan       = StringVar()
    ################################
    
    
    
    
    EP_form_frame = Frame(edit_patient)
     #Defining Frames for each row##########################
    rowframe1 = Frame(EP_form_frame)
    date_text       = Label(rowframe1, text='Tarih                ', font= myfont)
    date_text.pack(pady=mypady, padx=5, side="left")
    date_entry      = Entry(rowframe1, textvariable= date, font= myfont)
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y") 
    date_entry.insert(0, date_time)
    date_entry.pack(pady=mypady, padx=5, side="left")
    rowframe1.pack(anchor="w")


    rowframe2 = Frame(EP_form_frame)
    firstname_text  = Label(rowframe2, text='İsim                 ', font= myfont)
    lastname_text   = Label(rowframe2, text='Soyisim ', font= myfont)
    firstname_entry  = Entry(rowframe2, textvariable= firstname, font= myfont)
    lastname_entry   = Entry(rowframe2, textvariable= lastname, font= myfont)
    
    firstname_text.pack(padx=5, pady=mypady, side="left")
    firstname_entry.pack(padx=6, pady=mypady,  side="left")
    
    lastname_text.pack(padx=5, pady=mypady,  side="left")
    lastname_entry.pack(padx=5, pady=mypady,  side="left")
    
    rowframe2.pack(anchor="w")
    
    
    rowframe3 = Frame(EP_form_frame)
    age_text        = Label(rowframe3, text='Yaş                   ', font= myfont)
    sex_text        = Label(rowframe3, text='Cinsiyeti', font= myfont)
    age_entry        = Entry(rowframe3, textvariable= age, font= myfont)
    sex_entry        = ttk.Combobox(rowframe3, textvariable= sex, state='readonly', font=myfont)
    sex_entry['values'] = ('Erkek',
                           'Kadın',
                           'Diğer',
                           'Belirtilmemiş')
    
    
    
    
    
    age_text.pack(padx=5, pady=mypady, side="left")
    age_entry.pack(padx=4, pady=mypady, side="left")
    
    sex_text.pack(padx=5, pady=mypady, side="left") 
    sex_entry.pack(padx=5, pady=mypady, side="left")
    
    rowframe3.pack(anchor="w")
    
    rowframe4 = Frame(EP_form_frame)
    tel_text        = Label(rowframe4, text='Cep Telefonu ', font= myfont)
    tc_text         = Label(rowframe4, text='TC No     ', font= myfont)
    tel_entry        = Entry(rowframe4, textvariable= tel, font= myfont)
    tc_entry         = Entry(rowframe4, textvariable= tc, font= myfont)
    
    tel_text.pack(padx=5, pady=mypady, side="left")
    tel_entry.pack(padx=5, pady=mypady, side="left")
    
    tc_text.pack(padx=5, pady=mypady, side="left")
    tc_entry.pack(padx=5, pady=mypady, side="left")
    
    rowframe4.pack(pady=5,anchor="w")
    
    
    rowframe5 = Frame(EP_form_frame)
    subframe5 = Frame(rowframe5)
    adress_text     = Label(subframe5, text='Adres               ', font= myfont)
    adress_text.pack()
    subframe5.pack(side="left", padx=5, pady=mypady)
    adress_entry_c   = ttk.Combobox(rowframe5, textvariable= adress_c, font= myfont)
    adress_entry_c['values']= my_city_tuple
    adress_entry_l   = ttk.Entry(rowframe5, textvariable= adress_l, font= myfont)
    adress_entry_c.pack(padx=2, pady=10, side="left")
    adress_entry_l.pack(padx=2, pady=10, side="left")
    
    rowframe5.pack(pady=5,anchor="w")
    
    
    rowframe6= Frame(EP_form_frame)
    subframe6 = Frame(rowframe6)
    complain_text   = Label(subframe6, text='Yakınma           ', font= myfont)
    complain_text.pack(pady=2, padx =5, side="top")
    subframe6.pack(side="left", padx=5, pady=mypady)
    
    
    complain_entry   = Text(rowframe6, height=4, font= myfont, wrap="word")
    complain_entry.pack(pady=10, side="left")
    
    rowframe6.pack(anchor="w")
    
    
    rowframe7 = Frame(EP_form_frame)
    
    subframe7 = Frame(rowframe7)
    inspection_text = Label(subframe7, text='Fizik Muayene', font= myfont)
    inspection_text_2 = Label(subframe7, text='(US)', font= myfont)
    inspection_text.pack(pady=2, padx =5, side="top")
    inspection_text_2.pack(pady=2, padx =5, side="top")
    subframe7.pack(side="left", padx=5, pady=mypady)
    
    
    inspection_entry   = Text(rowframe7, height=6, font= myfont, wrap="word")
    inspection_entry.pack(pady=mypady, side="left")
    
    rowframe7.pack(anchor="w")
    
    
    rowframe8= Frame(EP_form_frame)
    subframe8 = Frame(rowframe8)
    plan_text       = Label(subframe8, text='Plan                  ', font= myfont)
    plan_text.pack(pady=2, padx =6, side="top")
    subframe8.pack(side="left", padx=5, pady=mypady)
    
    plan_entry       = Text(rowframe8, height=3, font= myfont, wrap="word")
    plan_entry.pack(pady=mypady, side="left")
    
    rowframe8.pack(anchor="w")
    ########################################################
    
    EP_form_frame.pack()
    
    
    
    

    t_adress = StringVar
    t_adress = values[8]
    t_adress_0 = t_adress[:(t_adress.index(','))]
    t_adress_1 = t_adress[(t_adress.index(',')+2):]
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y")
    
    ##Uncommend this if you want to update time when you edit
    #date_entry.insert(0, date_time)
    #########################################################
    
    
    ##Delete this if you update time when you edit###########
    date_entry.insert(0, values[1])
    #########################################################
    
    firstname_entry.insert(0, values[2])
    lastname_entry.insert(0, values[3])
    try:
        age_entry.insert(0, values[4])
    except:
        pass
    try:
        sex_entry.current(('Erkek',
                           'Kadın',
                           'Diğer',
                           'Belirtilmemiş').index(values[5]))
    except:
        pass
    try:
        tel_entry.insert(0, values[6])
    except:
        pass
    try:
        tc_entry.insert(0, values[7])
    except:
        pass
    try:
        adress_entry_l.insert(0, t_adress[:t_adress.index(',')])
        if(t_adress_1 in my_city_tuple):
            adress_entry_c.current(my_city_tuple.index(t_adress_1))
        else:
            adress_entry_c.set(t_adress_1)
        
        
        complain_entry.insert(1.0, values[9])
        inspection_entry.insert(1.0, values[10])
        plan_entry.insert(1.0, values[11])
    except:
        pass
    
    

    
    
    
    
    
    
    


    def edit_patient_info():
        age=''
        tel=''
        tc=''
        
        date = date_entry.get()
        firstname = firstname_entry.get()
        lastname = lastname_entry.get()
        sex = sex_entry.get()
        
        try:
            age_a = int(age_entry.get()) if (age_entry.get() != None and age_entry.get() != '' and age_entry.get() != 'nan') else 'nan'
            age = str(age_entry.get())
        except ValueError:
            error_text.config(text='Hata: Lütfen Yaş, TC Kimlik Numarası ve Telefon Numarası alanlarının\n numerik bir girdi olduğuna emin olunuz.\n Bir değer girmeyecekseniz lütfen boş bırakınız')
            return
        try:
            tel_a = int(tel_entry.get()) if (tel_entry.get() != None and tel_entry.get() != '' and tel_entry.get() != 'nan') else 'nan'
            tel = str(tel_entry.get())
        except ValueError:
            error_text.config(text='Hata: Lütfen Yaş, TC Kimlik Numarası ve Telefon Numarası alanlarının\n numerik bir girdi olduğuna emin olunuz.\n Bir değer girmeyecekseniz lütfen boş bırakınız')
            return
        try:
            tc_a = int(tc_entry.get()) if (tc_entry.get() != None and tc_entry.get() != '' and tc_entry.get() != 'nan') else 'nan'
            tc = str(tc_entry.get())
        except ValueError:
            error_text.config(text='Hata: Lütfen Yaş, TC Kimlik Numarası ve Telefon Numarası alanlarının\n numerik bir girdi olduğuna emin olunuz.\n Bir değer girmeyecekseniz lütfen boş bırakınız')
            return

            
        adress = adress_entry_l.get()+", "+adress_entry_c.get()
        complain = complain_entry.get(1.0,END)
        inspection = inspection_entry.get(1.0,END)
        plan = plan_entry.get(1.0,END)
        
        op_id=values[0]
        
        row=createElement(
        op_id,
        date,
        firstname,
        lastname,
        age,
        sex,
        tel,
        tc,
        adress,
        complain,
        inspection,
        plan
        )
        editElement(op_id,row)
        
        value = row[0]
        try:
            value[6] = str(value[6])
        except:
            pass
        try:
            value[7] = str(value[7])
        except:
            pass
        try:
            value[4] = str(value[4])
        except:
            pass
        value[10] = value[10].split("\n")[0]
        value[11] = value[11].split("\n")[0]
        value[9] = value[9].split("\n")[0]
        
        tree.item(selected, values=value)
        ep.destroy()


    reg_button= Button(edit_patient, text="Hastayı Kaydet", command = edit_patient_info, bg='orange', fg=foreground, width="20", font=myfont)
    reg_button.pack(padx=10, pady= mypady+5)
    
    error_text = Label(edit_patient, text='')
    error_text.pack()
    
    
    edit_patient.pack(padx=10, pady=mypady)
    
    ep.mainloop()


# In[9]:


# 3.3 Create backup screen
def backup_window():
    now = datetime.now()
    save_backup = Tk()
    save_backup.resizable(height = False, width = False)
    save_backup.geometry("520x80")
    save_backup.title("Yedek Oluştur")
    save_backup.iconbitmap('icon.ico')
    
    backup_name = StringVar()
    backup_name_entry = Entry(save_backup, textvariable= backup_name,width="80")
    backup_name_entry.pack(pady=10,padx=5)
    
    date = now.strftime("%m-%d-%Y-%H-%M-%S")
    filename= ("patient-data-backup-"+date)
    backup_name_entry.insert(0, filename)
    
    def saveBackup():
        global file_data
        file_data.to_csv('./backups/'+backup_name_entry.get()+'.csv') 
        save_backup.destroy()
    
    button_save = Button(save_backup,text="Kaydet", command =lambda:saveBackup(), bg='orange', fg=foreground, width="5")
    button_save.pack()
    save_backup.mainloop()


# In[10]:


# 4th: Create PDF Files:
def createPDF(data):
    
    #content
    filename = 'patient_pdf.pdf'
    documentTitle = 'patient information'
    title = 'Doktor İzlem Formu'
    
    dateLabel = 'Tarih:'
    nameLabel = 'Hasta Adı Soyadı:'
    ageLabel = 'Yaşı:'
    sexLabel = 'Cinsiyeti:'
    telLabel = 'Cep Tel:'
    idLabel = 'TC:'
    locationLabel = 'Adres:'
    complainLabel = 'YAKINMA:'
    inspLabel  = 'FİZİK MUAYENE:'
    planLabel = 'PLAN:'
    
    op_id = data[0]
    data = file_data[file_data["op id"] == op_id]
    data = (data.iloc[0])

    
    
    date = str(data[1])
    name = str(data[2]) + ' ' + str(data[3])
    age = str(data[4])
    sex = str(data[5])
    tel = str(data[6])
    idno = str(data[7])
    location = str(data[8])
    
    from textwrap import wrap
    import re
    complain = str(data[9])
    complain = ('\n'.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', complain)))
    complain = complain.split("\n")
    
    insp= str(data[10])
    insp = ('\n'.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', insp)))
    insp = insp.split("\n")
    
    plan = str(data[11])
    plan = ('\n'.join(line.strip() for line in re.findall(r'.{1,70}(?:\s+|$)', plan)))
    plan = plan.split("\n")
        
    
    
    # 0) Create Document :
    from reportlab.pdfgen import canvas

    
    pdf = canvas.Canvas(filename)
    pdf.setTitle(documentTitle)
    
    # 1) Title :: Set fonts
    
        
    
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    
    pdfmetrics.registerFont(TTFont("tr-font",'fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont("tr-font-b",'fonts/arialbd.ttf'))
    pdf.setFont("tr-font",24)
    
    pdf.drawCentredString(290, 770, title)
    
    



    
    
    # 2) Labels
    pdf.setFont('tr-font-b', 12)
    pdf.drawString(50, 730, dateLabel)
    pdf.drawString(50, 700, nameLabel)
    pdf.drawString(50, 670, ageLabel)
    pdf.drawString(210, 670, sexLabel)
    pdf.drawString(50, 640, telLabel)
    pdf.drawString(210, 640, idLabel)
    pdf.drawString(50, 610, locationLabel)
    
    
    
    
    
    # 3) Contents
    pdf.setFont("tr-font",12)
    pdf.drawString(90, 730, date)
    pdf.drawString(153, 700, name)
    pdf.drawString(82, 670, age)
    pdf.drawString(264, 670, sex)
    pdf.drawString(101, 640, tel)
    pdf.drawString(233, 640, idno)
    pdf.drawString(90, 610, location)
    
    
    pdf.setFont('tr-font-b', 12)
    pdf.drawString(50, 550, complainLabel)
    pdf.setFont('tr-font', 12)
    pdf.drawString(150, 550, complain[0])
    comp=0;
    for i in range(1,len(complain)):
        if(len(complain[i])>0):
            comp = i
            pdf.drawString(150, 550-(i*15), complain[i])
            
    #print("comp = " + str(comp))
    
    
    pdf.setFont('tr-font-b', 12)
    pdf.drawString(50, 500 - (comp*15), inspLabel)
    pdf.setFont('tr-font', 12)
    pdf.drawString(150, 500 - (comp*15), insp[0])
    inspec=0
    for i in range(1,len(insp)):
        if(len(insp[i])>0):
            inspec=i
            pdf.drawString(150, 500-(i*15) - (comp*15), insp[i])
    #print("inspec = " + str(inspec))
    
    
    pdf.setFont('tr-font-b', 12)
    pdf.drawString(50, 450 - (inspec*15) - (comp*15), planLabel)
    pdf.setFont('tr-font', 12)
    pdf.drawString(150, 450 - (inspec*15) - (comp*15), plan[0])
    pl=0
    for i in range(1,len(plan)):
        if(len(plan[i])>0):
            pl=i
            pdf.drawString(150, 450-(i*15) - (inspec*15) - (comp*15), plan[i])
    

        

    
    # F) Save The File
    import webbrowser
    pdf.save()
    webbrowser.open_new(filename)


# In[11]:


# 5th Create table window
def table_window():
    root=Tk();
    root.title("Main")
    root.geometry("1250x500")
    root.iconbitmap('icon.ico')

    #Define tree frame
    tree_frame = Frame(root);
    tree_frame.pack(padx=20,pady=20);
    
    #Define Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill= Y)
    
    #Define tree object
    datatree= ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
    hastasayisi = StringVar();
    hastasayisi.set("Kayıtlı Hasta Sayısı: " +str(len(file_data["op id"])))
    

    #Configure the scrollbar
    tree_scroll.config(command = datatree.yview)
    
    #Define columns from pandas dataframe
    datatree['columns'] = data_columns
    datatree['show'] = 'headings'
    
    #loop trough data tree and add headers
    #for column in datatree["column"]:
    #    datatree.heading(column, text=column)
    
    
    
    
    #Sorting Function#################################################
    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
    
    
        #print(col)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
        
    

    datatree.heading("op id", text="op id", command=lambda:treeview_sort_column(datatree, "op id", False))
    datatree.heading("Tarih", text="Tarih", command=lambda:treeview_sort_column(datatree, "Tarih", False))
    datatree.heading("Ad", text="Ad", command=lambda:treeview_sort_column(datatree, "Ad", False))
    datatree.heading("Soyad", text="Soyad", command=lambda:treeview_sort_column(datatree, "Soyad", False))
    datatree.heading("Yaş", text="Yaş", command=lambda:treeview_sort_column(datatree, "Yaş", False))
    datatree.heading("Cinsiyet", text="Cinsiyet", command=lambda:treeview_sort_column(datatree, "Cinsiyet", False))
    datatree.heading("Cep Telefonu", text="Cep Telefonu", command=lambda:treeview_sort_column(datatree, "Cep Telefonu", False))
    datatree.heading("TC Kimlik No", text="TC Kimlik No", command=lambda:treeview_sort_column(datatree, "TC Kimlik No", False))
    datatree.heading("Adres", text="Adres", command=lambda:treeview_sort_column(datatree, "Adres", False))
    datatree.heading("Yakınma", text="Yakınma", command=lambda:treeview_sort_column(datatree, "Yakınma", False))
    datatree.heading("Fizik Muayene", text="Fizik Muayene", command=lambda:treeview_sort_column(datatree, "Fizik Muayene", False))
    datatree.heading("Plan", text="Plan", command=lambda:treeview_sort_column(datatree, "Plan", False))

    

    
    #################################################################
    
    refreshDisplay()
    updateTree(datatree)

    
    #Formate columns
    datatree.column("#0",width=25,minwidth=5)
    datatree.column("op id",width=0,minwidth=0)
    datatree.column("Tarih",width=100,minwidth=5)
    datatree.column("Ad",width=60,minwidth=5)
    datatree.column("Soyad",width=60,minwidth=5)
    datatree.column("Yaş",width=40,minwidth=5)
    datatree.column("Cinsiyet",width=60,minwidth=5)
    datatree.column("Cep Telefonu",width=120,minwidth=5)
    datatree.column("TC Kimlik No",width=120,minwidth=5)
    datatree.column("Adres",width=150,minwidth=5)
    datatree.column("Yakınma",width=180,minwidth=5)
    datatree.column("Fizik Muayene",width=150,minwidth=5)
    datatree.column("Plan",width=120,minwidth=5)
          
    def OnDoubleClick(event):
        try:
            patient_edit_form_window(datatree, datatree.selection()[0])
        except:
            pass
        
    def ClearSelection(event):
        for item in datatree.selection():
            datatree.selection_remove(item)
        
    datatree.bind("<Double-1>", OnDoubleClick)
    datatree.bind("<Button-1>", ClearSelection)
    
    
    

    
    
    datatree.pack()


        
    def createFunc():
        patient_add_form_window(datatree, hastasayisi)
        
        
        
    def removeFunc():
        deleteSelection(datatree, datatree.selection()[0])
        hastasayisi.set("Kayıtlı Hasta Sayısı: " +str(len(file_data["op id"])))

    
    
            
    buttonFrame = Frame(root)
    
    button_add = Button(buttonFrame,text="Yeni Oluştur", command =lambda:createFunc(), bg='orange', fg=foreground, width="15")
    button_add.pack(pady=20,padx=(0,30), side="left")
    button_delete = Button(buttonFrame,text="Seçileni Sil", command =lambda:removeFunc(), bg='orange', fg=foreground, width="15")
    button_delete.pack(pady=20,padx=(0,30), side="left")
    button_edit = Button(buttonFrame,text="Seçileni Düzenle", command =lambda:patient_edit_form_window(datatree, datatree.selection()[0]), bg='orange', fg=foreground, width="15")
    button_edit.pack(pady=20,padx=(0,30), side="left")
    buttonFrame.pack()


    
    
    
    searchFrame = Frame(root)    
    search = StringVar()
    search_entry = Entry(searchFrame, textvariable= search)
    search_entry.pack(pady=20, side="left")
    button_search = Button(searchFrame,text="Ara", command =lambda:searchElement(search_entry.get(), datatree), bg='orange', fg=foreground, width="5")
    button_search.pack(pady=20,padx=(5,0), side="left")
    searchFrame.pack()
    
    saveFrame = Frame(root)
    button_save = Button(saveFrame, text="Yedek Kaydet", command =backup_window, bg='orange', fg=foreground)
    button_save.pack()
    saveFrame.pack()
    
    viewFrame = Frame(root)
    button_view = Button(viewFrame, text="PDF Oluştur", command =lambda: createPDF(datatree.item(datatree.selection()[0])['values']), bg='orange', fg=foreground)
    button_view.pack()
    viewFrame.pack()
    

    
    countFrame = Frame(root)
    label_count = Label(countFrame, textvariable=hastasayisi)
    label_count.pack()
    countFrame.pack()

    root.mainloop()
table_window()


# In[12]:


#file_data

