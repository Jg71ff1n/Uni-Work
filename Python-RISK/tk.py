from tkinter import *
from tkinter import ttk
from maps import map
import sys

class App(Frame):
    def __init__(self,master):
        super(App,self).__init__(master)
        self.grid()
        
    def label(self,message):
        self.label=ttk.Label(self,text=message)
        self.label.grid(column=1,row=0,sticky=N)
        
    #Methods for the input buttons  
    def first_button(self):
        self.button=Button(self,text="Select",command=self.get_country)
        self.button.grid(column=2,row=2,sticky=SE)

    def second_button(self):
        self.button=Button(self,text="Select",command=self.get_second_country)
        self.button.grid(column=2,row=2,sticky=SE)
    
    def entry_button(self):
        self.button=Button(self,text="Enter",command=self.get_entry)
        self.button.grid(column=2,row=2,sticky=SE)
    
    def amount_button(self):
        self.button=Button(self,text="Enter",command=self.get_amount)
        self.button.grid(column=2,row=2,sticky=SE)
    
    def alert_button(self):
        self.button=Button(self,text="Close",command=self.alert_function)
        self.button.grid(column=2,row=2,sticky=SE)
        
    #Methods for creating and populating various comboboxs
    def first_combobox(self,player):
        first_country_choice=StringVar()
        self.first_country=ttk.Combobox(self,textvariable=first_country_choice)
        self.first_country["values"]=first_country_select(player)
        self.first_country.grid(column=1,row=2,sticky=N)
       
    def second_combobox(self,chosen_country):
        second_country_choice=StringVar()
        self.second_country=ttk.Combobox(self,textvariable=second_country_choice)
        self.second_country["values"]=second_country_select(chosen_country)
        self.second_country.grid(column=1,row=2,sticky=N)

    def second_combobox_attack(self,chosen_country,player):
        second_country_choice=StringVar()
        self.second_country=ttk.Combobox(self,textvariable=second_country_choice)
        self.second_country["values"]=second_country_attack(chosen_country,player)
        self.second_country.grid(column=1,row=2,sticky=N)    
    
    def amount_combobox(self,chosen_country):
        amount_choice=StringVar()
        self.amount=ttk.Combobox(self,textvariable=amount_choice)
        self.amount["values"]=get_army(chosen_country)
        self.amount.grid(column=1,row=2,sticky=N)
        
    #Method for creating entry box
    def entry_box(self):
        save_game_name=StringVar()
        self.save_game=ttk.Entry(self, textvariable=save_game_name)
        self.save_game.grid(column=1,row=2,sticky=N)
       
	#Functions for the individual buttons	
    def get_country(self):
        global selected_country
        selected_country=self.first_country.get()
        self.master.destroy()
        return selected_country,

    def get_second_country(self):
        global second_selected_country
        second_selected_country=self.second_country.get()
        self.master.destroy()
        return second_selected_country
    
    def get_entry(self):
        global entry_value
        entry_value=self.save_game.get()
        self.master.destroy()
        return entry_value
        
    def get_amount(self):
        global value
        value=self.amount.get()
        self.master.destroy()
        return value
    
    def alert_function(self):
        self.master.destroy()
		
#Functions for creating the lists of the countries
def first_country_select(player):
    possible_start=[]
    for entry in map:
        #Adds countries owned by player to a list
        if player==map[entry][0]:
            possible_start.append(entry)
    return possible_start

def second_country_select(chosen_country):
    possible_moves_id=map[chosen_country][3]
    possible_moves=[]
    #Goes through the dictionary and checks to see if the country ID is in the tuple. If so adds to a list	
    for entry in map:        
        if map[entry][2] in possible_moves_id:
            if map[entry][0]==0:
                possible_moves.append(entry)    
    return possible_moves

def second_country_attack(chosen_country,player):
    possible_moves_id=map[chosen_country][3]
    possible_moves=[]
    #Goes through the dictionary and checks to see if the country ID is in the tuple and the country has a player that isn't the current players. If so adds to a list	
    for entry in map:        
        if map[entry][2] in possible_moves_id:
            if map[entry][0]!=player and map[entry][0]!=0:
                possible_moves.append(entry)    
    return possible_moves

def get_army(original_country):
    army_total=map[original_country][1]
    print(army_total)
    army=[]
    for i in range(army_total):
        army.append(i+1)
    return army
#Function that creates the tkinter window
def one_country_select(player):
    root=Tk()
    root.title("Country Selection")
    app=App(root)
    app.label("Please select a country:")
    app.first_combobox(player)
    app.first_button()
    root.mainloop()
    return selected_country

def two_country_select(player):
    one_country_select(player)
    root=Tk()
    root.title("Country Selection")
    second=App(root)
    second.label("Please select a second country:")
    second.second_combobox(selected_country)
    second.second_button()
    root.mainloop()
    return selected_country, second_selected_country

def two_country_attack(player):
    one_country_select(player)
    root=Tk()
    root.title("Country Selection")
    second=App(root)
    second.label("Please select a second country:")
    second.second_combobox_attack(selected_country,player)
    second.second_button()
    root.mainloop()
    return selected_country, second_selected_country
 
def move_country_entry(player):
    a,b=two_country_select(player)
    root=Tk()
    root.title("Move Country")
    move_window=App(root)
    move_window.label("Please choose the amount you wish to move:")
    move_window.amount_combobox(a)
    move_window.amount_button()
    root.mainloop()
    return selected_country, second_selected_country, value
 
def entry_dialogue():
    root=Tk()
    root.title("Entry")
    entry_window=App(root)
    entry_window.label("Please enter a save game name:")
    entry_window.entry_box()
    entry_window.entry_button()
    root.mainloop()
    return entry_value

def start_game():
    root=Tk()
    root.title("Start Game")
    entry_window=App(root)
    entry_window.label("Please enter the amount of players:(6 Maximum)")
    entry_window.entry_box()
    entry_window.entry_button()
    root.mainloop()
    return entry_value

def alert(message):
    root=Tk()
    root.title("Alert")
    alert=App(root)
    alert.label(message)
    alert.alert_button()
    root.mainloop()
