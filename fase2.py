# -*- coding: utf-8 -*-

from binarysearchtree import BinarySearchTree
from dlist import DList
import csv      #read files csv, tsv
import os.path  #to work with files and directory https://docs.python.org/3/library/os.path.html
import queue    #package implementes a queueu, https://docs.python.org/3/library/queue.html
import re       #working with regular expressions

def checkFormatHour(time):
    """checks if the time follows the format hh:dd"""
    pattern = re.compile(r'\d{1,2}:\d{2}')  # busca la palabra foo
    
    if pattern.match(time):
        data=time.split(':')
        hour=int(data[0])
        minute=int(data[1])
        if hour in range(8,20) and minute in range(0,60,5):
            return True
    
    return False



#number of all possible appointments for one day
NUM_APPOINTMENTS=144

class Patient:
    """Class to represent a Patient"""
    def __init__(self,name,year,covid,vaccine,appointment=None):

        self.name=name
        self.year=year
        self.covid=covid
        self.vaccine=vaccine
        self.appointment=appointment     #string with format hour:minute

    def setAppointment(self,time):
        """gets a string with format hour:minute"""
        self.appointment=time
        
    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)+'\t appointment:'+str(self.appointment)

    def __eq__(self,other):
        return  other!=None and self.name == other.name 



class HealthCenter2(BinarySearchTree):
    """Class to represent a Health Center. This class is a subclass of a binary search tree to 
    achive a better temporal complexity of its algorithms for 
    searching, inserting o removing a patient (or an appointment)"""


    def __init__(self,filetsv=None,orderByName=True):
        """
        This constructor allows to create an object instance of HealthCenter2. 
        It takes two parameters:
        - filetsv: a file csv with the information about the patients whe belong to this health center
        - orderByName: if it is True, it means that the patients should be sorted by their name in the binary search tree,
        however, if is is False, it means that the patients should be sorted according their appointments
        """

        #Call to the constructor of the super class, BinarySearchTree.
        #This constructor only define the root to None
        super(HealthCenter2, self).__init__()
        
        if filetsv is None or not os.path.isfile(filetsv):
            #If the file does not exist, we create an empty tree (health center without patients)
            self.name=''
            print('Warning!!!! File does not exist ',filetsv)
        else: 
           # order='by appointment'
           #if orderByName:
           #    order='by name'
           #print('\n\nloading patients from {}. The order is {}\n\n'.format(filetsv,order))
            
            self.name=filetsv[filetsv.rindex('/')+1:].replace('.tsv','')
            #print('The name of the health center is {}\n\n'.format(self.name))

            fichero = open(filetsv)
            lines = csv.reader(fichero, delimiter="\t")
    
            for row in lines:
                #print(row)
                name=row[0] #nombre
                year=int(row[1]) #año nacimiento
                covid=False
                if int(row[2])==1:          #covid:0 o 1
                    covid=True
                vaccine=int(row[3])         #número de dosis
                try:
                    appointment=row[4]
                    if checkFormatHour(appointment)==False:
                        #print(appointment, ' is not a right time (h:minute)')
                        appointment=None
                        
                except:
                    appointment=None    

                objPatient=Patient(name,year,covid,vaccine,appointment)
                #name is the key, and objPatient the element
                if orderByName:
                    self.insert(name,objPatient)
                elif orderByName==False and appointment:
                    #we only save if the appointment has a right format
                    self.insert(appointment,objPatient)
                
    
            fichero.close()




    def searchPatients(self,year=2021,covid=None,vaccine=None):
        """return a new object of type HealthCenter 2 with the patients who
        satisfy the criteria of the search (parameters). 
        The function has to visit all patients, so the search must follow a level traverse of the tree.
        If you use a inorder traverse, the resulting tree should be a list!!!"""
        
        
        result=HealthCenter2()
    
        if self._root==None:
            print('tree is empty')
        else:
            
            q=queue.Queue()
            q.put(self._root) #enqueue: we save the root
            
            while q.empty()==False:
                current=q.get() #dequeue
                if (current.elem.year <= year) and (covid == None or current.elem.covid == covid) and (current.elem.vaccine == vaccine or vaccine == None):
                    result.insert(current.key,current.elem) #if the requirements are fulfilled, we insert the patient at the health center
                if current.left!=None: #we iterate recursively until the leaf nodes
                    q.put(current.left)
                if current.right!=None:
                    q.put(current.right)
                
        return result
       
   
        #usar preorder/level order

    def vaccine(self,name,vaccinated):
        """This functions simulates the vaccination of a patient whose
        name is name. It returns True is the patient is vaccinated and False eoc"""
        
       #use find, not search (find print the node)
       #node = find(name)
       #if node = none: return false
       #if not, check number of dosis (node.elem.vaccine)
       #to insert in the vaccinated .insert(node.key,node.elem)
       #to remove 
        node = self.find(name)
        
        if node == None: #non-existing patient
           print('The patient does not exist')
           return False
       
        if node.elem.vaccine == 2: #already full of vaccines
            print('Patient has already received the 2 dosis')
            vaccinated.insert(node.key,node.elem)
            self.remove(node.key) #remove the patient from the health center
            return False 
        
        #we insert a second vaccine and we insert it in vaccinated
        if node.elem.vaccine == 1:
            node.elem.vaccine +=1 #add up the new dosis
            vaccinated.insert(node.key,node.elem) #insert in the vaccinated health center
            self.remove(node.key) #remove from the other one
            return True
        
        if node.elem.vaccine == 0:
            node.elem.vaccine +=1 #add up the dosis
            return True
        
        return False #for some other case (good practice)
    
    def getList(self):
        #this method returns a DList from the node "node" (in the recursive way)
        returnList = DList()
        self._getList(self._root, returnList) #execute the method from the root iteratively
        return returnList
    
    def _getList(self, node, returnList):
        if node != None:
            self._getList(node.left, returnList)
            returnList.addLast(node.key)
            self._getList(node.right, returnList)
        
    
    def MinConversion(self,string): #this takes a time hh:mm format and converts to minutes
        time = string.split(":") #split by the :
        hour = int(time[0])
        minutes = int(time[1])
        
        conversion = hour*60 + minutes #conversion computation
        return conversion
    
    def backToFormat(self, total): #this method converts the minutes back to the original format hh:mm
        hour = total//60
        minutes = total - (60*hour)
        
        #we fix the format for numbers between 8 and 10
        if minutes == 5:
            minutes = "05"
        if minutes == 0:
            minutes = "00"
        
        if hour == 8:
            hour = "08"
        
        if hour == 9:
            hour = "09"
        
        return str(hour) + ":" + str(minutes) #setting the hour up again
    

    def makeAppointment(self,name,time,schedule):
        """This functions makes an appointment 
        for the patient whose name is name. It functions returns True is the appointment 
        is created and False eoc """
        
        if checkFormatHour(time) == False:
            print("Wrong hour format")
            return False
        
        #if we don't find the patient, we return False
        node = self.find(name)
        if node is None:
            print("Patient", name, "was not found")
            return False
        patient = node.elem 
        
        #If they have already received both doses, we do nothing and return False
        if patient.vaccine == 2:
            print("Patient", name, "is already vaccinated")
            return False

        found = schedule.search(time)         
        #if there is a free hour, we add the patient to that time slot
        if found == False:
           patient.appointment = time
           schedule.insert(time, patient) #insert(key, elem)
           print("There was a free hour at", time)
           return True 
        #whenever there are no free hours (all covered), return False
        if schedule.size() == NUM_APPOINTMENTS:
            print("\n\tThere are no free appointment slots")
            return False
        
        #if none of the above are fulfilled, it means we have free time to assign to the patient but not at the time it is provided
        list = schedule.getList()
        index = list.index(time) #we see the index in which the time provided is
        before_idx = index - 1
        after_idx = index + 1
        #now let's create a marker to see the time attached to the position index
        initial = list.getAt(index)
        time_before = initial
        time_after = initial
        find = False #by default, we haven't found the hour before or after hour
        
        while not find: #until it finds the position and time we look for
            if before_idx >=0: #in case we are not in the first position of the list
                timeAfter_before = time_before #we assign the time after the before to the variable we already created 
                time_before = list.getAt(before_idx)
                
                #convert to minutes in order to compare them
                before_minutes = self.MinConversion(time_before)
                afterBefore_minutes = self.MinConversion(timeAfter_before)
                
                #let's compare this current position in the list of taken hours (list) with the previous one;
                #if there is a difference from more than 5 minutes, there is a free position right before the current position
                if (afterBefore_minutes - before_minutes) > 5 and checkFormatHour(time_before):
                    #in this case, we are not considering the right format from default, we check it and convert it back
                    patient.appointment = self.backToFormat(afterBefore_minutes - 5)
                    schedule.insert(patient.appointment, patient) #we insert the node and the time at schedule
                    return True
                
                before_idx -= 1 #if there is no gap between both positions, we step back the index we use for before
            
            
            #if we can't assign an hour before, we iterate looking for a gap in the hours after the proposed one
            if after_idx <= (len(list) - 1): #iterate if current is not the last node
                timeBefore_after = time_after
                time_after = list.getAt(after_idx)
                
                after_minutes = self.MinConversion(time_after)
                beforeAfter_minutes = self.MinConversion(timeBefore_after)
                
                #we look for gaps of more than 5 minutes, in such case ther will be a free hour;
                #ex: 19:50-- .gap. --20:00, difference: 10 minutes > 5
                if (after_minutes - beforeAfter_minutes) > 5 and checkFormatHour(time_after):
                    patient.appointment = self.backToFormat(beforeAfter_minutes + 5)
                    schedule.insert(patient.appointment, patient)
                    return True
                
                after_idx += 1
            print(patient.appointment)

        #return False
        
        
        
if __name__ == '__main__':
    
    ###Testing the constructor. Creating a health center where patients are sorted by name
    o=HealthCenter2('data/LosFrailes2.tsv')
    o.draw()
    print()


    print('Patients who were born in or before than 1990, had covid and did not get any vaccine')
    result=o.searchPatients(1990, True,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990, did not have covid and did not get any vaccine')
    result=o.searchPatients(1990, False,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and got one dosage')
    result=o.searchPatients(1990, None,1)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and had covid')
    result=o.searchPatients(1990, True)
    result.draw()
    print()


    ###Testing the constructor. Creating a health center where patients are sorted by name
    schedule=HealthCenter2('data/LosFrailesCitas.tsv',False)
    schedule.draw(False)
    print()
    
    

    o.makeAppointment("Perez","08:00",schedule)
    o.makeAppointment("Losada","19:55",schedule)
    o.makeAppointment("Jaen","16:00",schedule)
    o.makeAppointment("Perez","16:00",schedule)
    o.makeAppointment("Jaen","16:00",schedule)

    o.makeAppointment("Losada","15:45",schedule)
    o.makeAppointment("Jaen","08:00",schedule)

    o.makeAppointment("Abad","8:00",schedule)
    o.makeAppointment("Omar","15:45",schedule)
    
    
    schedule.draw(False)

    vaccinated=HealthCenter2('data/vaccinated.tsv')
    vaccinated.draw(False)

    name='Ainoza'  #doest no exist
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Abad'   #0 dosages
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
   

    name='Font' #with one dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
    name='Omar' #with two dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
