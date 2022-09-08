# -*- coding: utf-8 -*-
"""
Created on Thu May 19 10:34:55 2022

@author: jsrih
"""

from pprint import pprint
import random
import nltk
from stat_parser import Parser
import pickle
import os
import webbrowser

#The knowledge base as a set
knowledge = {("Patient", "firstname", "?"), \
             ("Patient", "lastname", "?"),
             ("Patient", "Gender", "?"),
             ("Patient", "Age", "?"),
             ("Patient", "Condition", "?")
             }

#A file containging thousands of medical conditions
with open(r'C:\Users\jsrih\OneDrive\Documents\Designing intelligent agents\Coursework submission\wordlist.txt') as f:
    lines = f.read().splitlines() 

#removing genders from this list of conditions
lines.remove('male')
lines.remove('female')
lines.remove('Smith')

#A function to check if the condition entered by the user is also present
#in the 'database'
def check(word, lst):    
    if word in lst:
        global condition
        #assign the disease to the variable condition
        condition = word
        #the NHS website refers to a cold as the 'common-cold'
        if condition == "cold":
            condition = "common-cold"
        
#naming the condition file
condition_file = 'mypickle.pk'        
condition_list = []
symptom_list = [] 

#Need this to intialise the file

# with open("condition_file","wb") as fi:
#     pickle.dump(condition_list, fi)

#reopen and unpickle the pickled content
if os.path.exists("condition_file"): 
    with open("condition_file",'rb') as fi: 
        #assigning condition_list to the unpickled data (appending all condition
        #to the condition list)
        condition_list = pickle.load(fi)
print("hello I am a medical chatbot, I shall ask you some questions now!")
active = True
while active:
    unknowns = { (person,fact,value) for (person,fact,value) 
                 in knowledge if value=="?" }
    if unknowns: #is non-empty
    #randomly select a value
        person, fact, value = random.choice(list(unknowns))
        question = "What is your "+fact+"? "
        reply = input(question)
        if reply=="bye":
            active = False
            continue
        #remove that fact when it is chosen
        knowledge.remove( (person,fact,value) ) 
        #parsing the user input into trees for NLP
        parser = Parser() 
        t = parser.parse(reply) 
        #must set values equal to none
        st = None
        vpTree = None
        npTree = None
        #for st in the tree
        for st in t.subtrees():
            #if the label is the part of the tree we need
            if st.label()=="VP":
                #assing the lable to st
                vpTree = st 
        #joining the leaves of the tree to give the answer
        answer = (" ".join(st.leaves()))
        #print('answer is', answer)
        #adding the answer to the knowledge set
        knowledge.add( (person, fact, answer) )
    #after we have asked our intial questions we then go onto the quesitons surrounding conditions
    else:
        #converting the knowledge store to a list
        kb_list = list(knowledge)
        #iterating through the list 
        for i in kb_list:
            for j in kb_list:
                #checking if the condition is in our database of conditions
                check (j[2], lines)
        #iterating through the condition list, if the user inputted condition is found in
        #the condition list then we append the symptoms of the condition to the symptom list to use later 
        #if not, we input the condition to the condition list at the end
        for string in condition_list:
            for a in string:
                if a == condition:
                    #need to append the symptoms and not the condition
                    symptom_list.append(string[1])
        question = f"How does {condition} affect you?"
        helpRequest = input(question)
        if helpRequest =="bye":
            active = False
            continue
        #if the symptom list is not empty (the agent has had another user input the same condition)
        if symptom_list:
            question = f"would you like to know some other {condition} patients symptoms? Please reply 'yes' or 'no' "
            ask = input(question)
            if ask == "no":
                question = "thank you for talking to me, would you like to know some more about your syptoms and condition? Please reply 'yes' or 'no'."
                ask = input(question)
                if ask == "yes":
                    webbrowser.open(f"https://www.nhs.uk/conditions/{condition}/")
                    print("Thank you for speaking with me!")
                    active = False
                else:
                    print("Thank you for speaking with me!")
                    active = False
            else:
                #if the user wants to know more about the condition, we randomly choose a symptom from the symptom list 
                print(random.choice(symptom_list))
                question = f"would you like to know all recorded {condition} symptoms?"
                ask = input(question)
                #if the user wants to know all of the recorded symptoms, then we print all elements of the symptom list 
                if ask == "yes":
                    for i in symptom_list:
                        print(i)
                    question = "thank you for talking to me, would you like to know some more about your syptoms and condition? Please reply 'yes' or 'no' "
                    ask = input(question)
            #if the user wants to know more about their condition, then the agent opens up the page for that condition
                    if ask == "yes":
                        webbrowser.open(f"https://www.nhs.uk/conditions/{condition}/")
                        print("Thank you for speaking with me!")
                        active = False
                    else:
                        print("Thank you for speaking with me!")
                        active = False
                else:
                    question = "thank you for talking to me, would you like to know some more about your syptoms and condition? Please reply 'yes' or 'no' "
                    ask = input(question)
                    if ask == "yes":
                        webbrowser.open(f"https://www.nhs.uk/conditions/{condition}/")
                        print("Thank you for speaking with me!")
                        active = False 
                    else:
                        print("Thank you for speaking with me!")
                        active = False
        else:
            #if the symptom list is empty i.e. it is a new condition inputted to the system then the else loop starts
            #where the agent can open up the NHS page for that condition
            question = "thank you for talking to me, would you like to know some more about your syptoms and condition? Please reply 'yes' or 'no'."
            ask = input(question)
            if ask == "yes":
                webbrowser.open(f"https://www.nhs.uk/conditions/{condition}/")
                print("Thank you for speaking with me!")
                active = False 
            else:
                print("Thank you for speaking with me!")
                active = False
        #here we append the condition and the symptoms to the condition ready to be used for the next patient
        test = condition, helpRequest
        condition_list.append(test)

with open("condition_file","wb") as fi:
    pickle.dump(condition_list, fi)

#reopen and unpickle the pickled content and read to obj
with open("condition_file","rb") as fi:
    condition_list = pickle.load(fi)

print("Final knowledge base of the patient: ")
print(knowledge)
print(f"all stored symptoms of {condition}: ")
print(symptom_list)
    
    
