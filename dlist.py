# -*- coding: utf-8 -*-
"""DList.ipynb

# Doubly Linked List

First, we must implement the class Node to store the nodes. In addition to the element and the reference to the next node, the class includes a reference, **prev**, to the previous node.
"""

class DNode:
  def __init__(self,elem,next=None,prev=None ):
    self.elem = elem
    self.next = next
    self.prev = prev

class DList:
    def __init__(self):
        """creates an empty list"""
        self._head=None
        self._tail=None
        self._size=0
    
    def __len__(self):
        return self._size

    def isEmpty(self):
        """Checks if the list is empty"""
        #return self.head == None   
        return len(self)==0

    
    def __str__(self):
        """Returns a string with the elements of the list"""
        nodeIt=self._head
        result=''
        while nodeIt:
            result += str(nodeIt.elem)+',\n'
            nodeIt=nodeIt.next

        if len(result)>0:
            result=result[:-2]
        
        return result
    
    def addFirst(self,e):
        """Add a new element, e, at the beginning of the list"""
        #create the new node
        newNode=DNode(e)                                   
        #the new node must point to the current head
        
        if self.isEmpty():                                
            self._tail=newNode                               
        else:
            newNode.next=self._head                          
            self._head.prev=newNode                          
        
        #update the reference of head to point the new node
        self._head=newNode                                 
        #increase the size of the list  
        self._size+=1                             
        
    
    
    def addLast(self,e):
        """Add a new element, e, at the end of the list"""
        #create the new node
        newNode=DNode(e)
        
        if self.isEmpty():
            self._head=newNode
        else:
            newNode.prev=self._tail
            self._tail.next=newNode
        
        #update the reference of head to point the new node
        self._tail=newNode
        #increase the size of the list  
        self._size+=1
   
    def removeFirst(self):
        """Returns and remove the first element of the list"""
        result=None
        if self.isEmpty():
            print("Error: list is empty")
        else:
            result=self._head.elem 
            self._head= self._head.next 
            if self._head==None:
                self._tail=None
            else:
                self._head.prev = None

            self._size-=1

        return result
    
    def removeLast(self):
        """Returns and remove the last element of the list"""
        result=None

        if self.isEmpty():
            print("Error: list is empty")
        else:
            result=self._tail.elem                       #1
            self._tail= self._tail.prev                 
            if self._tail==None:
                self._head=None
            else:
                self._tail.next = None

            self._size-=1

        return result
  
 
    def getAt(self,index):
        """return the element at the position index.
        If the index is an invalid position, the function
        will return -1"""
        result=None
        if index not in range(0,len(self)): 
            print(index,'Error getAt: index out of range')
        else:
            nodeIt=self._head
            i=0
            while nodeIt and i<index:
                nodeIt=nodeIt.next
                i+=1

            #nodeIt is at the position index
            result=nodeIt.elem

        return result

    def index(self,e):
        """returns the first position of e into the list.
        If e does not exist in the list, 
        then the function will return -1"""
        nodeIt=self._head
        index=0
        while nodeIt:
            if nodeIt.elem==e:
                return index
            nodeIt=nodeIt.next
            index+=1
            
        #print(e,' does not exist!!!')
        return -1 

    def insertAt(self,index,e):
        """It inserts the element e at the index position of the list"""
        if index not in range(len(self)+1):
            print('Error: index out of range')
        elif index==0:
            self.addFirst(e)
        elif index==len(self): 
            self.addLast(e)
        else:
            #we must to reach the node at the index position
            nodeIt=self._head
            for i in range(1,index+1):
                nodeIt=nodeIt.next

            #nodeIt is the node at the index

            newNode=DNode(e)
            #we have to insert the new node before nodeIt
            newNode.next=nodeIt
            newNode.prev=nodeIt.prev

            nodeIt.prev.next=newNode
            nodeIt.prev=newNode
            self._size+=1
      
      
    

    
    def removeAt(self,index):
        """This methods removes the node at the index position in the list"""
        
        #We must check that index is a right position in the list
        #Remember that the indexes in a list can range from 0 to size-1
        """This methods removes the node at the index position in the list"""
        result=None
        #We must check that index is a right position in the list
        #Remember that the indexes in a list can range from 0 to size-
        #print(str(self)," len=", len(self), "index=",index)
        if index not in range(len(self)): 
            print(index,'Error removeAt: index out of range')
        elif index==0:
            result= self.removeFirst()
        elif index==len(self)-1:
            result= self.removeLast()
        else:
            #we must to reac
            #we must to reach the node at the index position
            nodeIt=self._head
            for i in range(1,index+1):
                nodeIt=nodeIt.next

            #nodeIt is the node to be removed

            result=nodeIt.elem
            prevNode=nodeIt.prev
            nextNode=nodeIt.next
            
            prevNode.next=nextNode
            nextNode.prev=prevNode
            self._size-=1
        
        return result


if __name__ == '__main__':
    import random

    l=DList()    
    print("list:",str(l))
    print("len:",len(l))
    
    #we generate 5 random integers
    for i in range(5):
        #creates a positive integer between 0 <=x<= 100
        x=random.randint(0,100)
        #l.addFirst(x)
        l.addLast(x)
    
    print(l)
    
    for i in range(len(l)):
        print('getAt({})={}'.format(i,l.getAt(i)))
    
    print(str(l))
    print()
    print("index of {}={}".format(20,l.index(20)))
    print("index of {}={}".format(0,l.index(0)))
    print("index of {}={}".format(5,l.index(5)))
    print("index of {}={}".format(10,l.index(10)))
    
    
    while l.isEmpty()==False:
        print("after removeLast():{}, {}".format(l.removeLast(),l))
    
    l.insertAt(-1,1)
    l.insertAt(0,0)
    print(str(l))
    print('after l.insertAt(0,0)', str(l))
    
    l.insertAt(len(l)//2,3)
    print('after l.insertAt(2,3)', str(l))
    print("index of {}={}".format(3,l.index(3)))
    print('len of l',len(l))
    l.insertAt(len(l),3)
    print('after l.insertAt(12,3)', str(l))
    print("index of {}={}".format(3,l.index(3)))
    l.insertAt(len(l),100)
    print('after l.insertAt(13,100)', str(l))
    
    print()
    print('testing removeAt', str(l))
    x=0
    print('after l.removeAt({})={}, {}'.format(x,l.removeAt(x), str(l)))
    
    x=len(l)//2
    print('after l.removeAt({})={}, {}'.format(x,l.removeAt(x), str(l)))
    
    x=len(l)-1
    print('after l.removeAt({})={}, {}'.format(x,l.removeAt(x), str(l)))