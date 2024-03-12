from dlist import DList
from dlist import DNode

import csv
import os.path

class Patient:
    """Class to represent a Patient"""
    def __init__(self,name,year,covid,vaccine):
        self.name=name
        self.year=year
        self.covid=covid
        self.vaccine=vaccine
        
    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)


class HealthCenter(DList):
    """Class to represent a Health Center"""
    def __init__(self,filetsv=None):
        super(HealthCenter, self).__init__()

        if filetsv is None or not os.path.isfile(filetsv):
            self.name=''

        else: 
            print('loadimg the data for the health center from the file ',filetsv)
    
            self.name=filetsv.replace('.tsv','')
            #self.name = self.name.split('/')[1]
            tsv_file = open(filetsv)
            read_tsv = csv.reader(tsv_file, delimiter="\t")
    
    
            for row in read_tsv:
                name=row[0]
                year=int(row[1])
                covid=False
                
                if int(row[2])==1:
                    covid=True

                vaccine=int(row[3])
                self.addLast(Patient(name,year,covid,vaccine))
                
    
    def addPatient(self,patient):
        "add a new patient in alphabetic order"
        
           
        i = 0
        current = self._head
        while current != None:
            if (patient.name < self._head.elem.name):
                self.addFirst(patient)
            if (patient.name > self._tail.elem.name):
                self.addLast(patient)
            if current.elem.name == patient.name:
                print('Patient is already in the list')
                return
            
            if current.elem.name > patient.name:
                self.insertAt(i,patient)
                return
            else:
                i+=1
                current = current.next
        return
                            
    def searchPatients(self,year,covid=None,vaccine=None):
        
       expectedCenter = HealthCenter()
       current = self._head
       
       while current:
           """For those patients which fulfill the age condition AND the others related to the vaccine and covid requirements to search and add it to the second center"""
           if (current.elem.year <= year) and (covid == None or current.elem.covid == covid) and (current.elem.vaccine == vaccine or vaccine == None):
               expectedCenter.addLast(current.elem)
           current = current.next
       return expectedCenter
                  

    
    def statistics(self):
        current = self.__head
        
        """We create many indexes"""
        
        total = 0
        infected = 0
        first_dose = 0
        second_dose = 0
        no_dose = 0
        total_no = 0
        older_70 = 0
        older_70_and_infected = 0
        older_70_and_no_dose = 0
                
        """We compute its frequency through the health center patients"""
        if current.elem.covid:
            infected += 1
        
        if current.elem.vaccine == 0:
            no_dose += 1
        
        if current.elem.vaccine == 1:
            first_dose += 1
        
        if current.elem.vaccine == 2:
            second_dose += 1        
        
        if current.elem.year <= 1950:
            older_70 += 1
        
        if current.elem.year <= 1950 and current.elem.covid:
            older_70_and_infected += 1
            
        if current.elem.year <= 1950 and (current.elem.covid == 0):
            older_70_and_no_dose += 1   
        
        current = current.next 
        total += 1

        """"Then, we create the statistics percentages themselves """
                
        covid_percentage = round((infected/total), 2)
        older_70_covid_percentage = round((older_70_and_infected/older_70), 2)
        no_dose_percentage = round((no_dose/total), 2)
        older_70_nodose_percentage = round((older_70_and_no_dose/older_70), 2)
        first_dose_percentage = round((first_dose/total), 2)
        second_dose_percentage = round((second_dose/total), 2)
        
        return covid_percentage, older_70_covid_percentage, older_70_nodose_percentage, no_dose_percentage, first_dose_percentage, second_dose_percentage
        
    def merge(self,other):
           
        merged = HealthCenter()
        
        """We set the current of the original center and the current of the other one, and we create an empty "merged" one"""
        
        current = self._head 
        currentO = other._head 
        
        while current and currentO:
            
            if currentO.elem.name < current.elem.name:
                merged.addLast(currentO.elem)
                currentO = currentO.next
                
            elif currentO.elem.name > current.elem.name:
                merged.addLast(current.elem)
                current = current.next
                
            else:
                merged.addLast(current.elem)
                current = current.next
                currentO = currentO.next
                                
        while current:
            merged.addLast(current.elem)
            current = current.next
            
        while currentO:
            merged.addLast(currentO.elem)
            currentO = currentO.next
            
        return merged
            
     
    def minus(self,other):
       current = self._head
       currentO = other._head
       
       """We proceed as before and then we create an index to find patients"""
       found = False
       hc = HealthCenter()
       
       while current:
           
           while currentO and not found:
               if current.elem.name == currentO.elem.name:
                   found = True
               else:
                   currentO = currentO.next
           if found == False:
               hc.addLast(current.elem)
               
                 
           current = current.next
           found = False
               
       currenthc = hc._head
       currentO = other._head
       found = False
       while currentO:
           
           while currenthc and not found:
               if currentO.elem.name == currenthc.elem.name:
                   found = True
               else:
                   currenthc = currenthc.next
           if found == False:
               hc.addLast(currentO.elem)
               
                 
           currentO = currentO.next
           found = False
       return hc   
        
    
    def inter(self,other):
        hc = HealthCenter()
        current = self._head
        currentO = other._head
         
        while current:
            
            while currentO:
                if current.elem.name == currentO.elem.name:
                    hc.addLast(current.elem)
                    
                else:
                    currentO = currentO.next
                    
            current = current.next
            
        return hc
                
'''

if __name__ == '__main__':
    gst=HealthCenter('LosFrailes.tsv')
    print(gst)
    
    #Puedes añadir más llamadas a funciones para probarlas

'''
