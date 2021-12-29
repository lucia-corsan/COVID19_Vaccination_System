#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys


class HealthCenter():
    def __init__(self,name=None):
        self.name=name
        
        
    def __eq__(self,other):
        return  other!=None and self.name==other.name
    
    def __str__(self):
        return self.name


class AdjacentVertex:
  def __init__(self,vertex,weight):
    self.vertex=vertex
    self.weight=weight
  
  def __str__(self):
    return '('+str(self.vertex)+','+str(self.weight)+')'
 
class Map():
    def __init__(self):
        self.centers={}
        self.vertices={}
    
    def addHealthCenter(self,center):
        i=len(self.centers)
        self.centers[i]=center
        self.vertices[i]=[]
        
    def _getIndice(self,center):
        for index in self.centers.keys():
            if self.centers[index]==center:
                return index
        return -1
        
    def __str__(self):
        result=''
        for i in self.vertices.keys():
            result+=str(self.centers[i])+':\n'
            for adj in self.vertices[i]:
                result+='\t'+str(self.centers[adj.vertex])+', distance:'+str(adj.weight)+'\n'
        return result
    
       
    def addConnection(self,center1,center2,distance):
        #print('new conexion:',pto1,pto2)
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)
        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        self.vertices[index1].append(AdjacentVertex(index2,distance))
        #print('adding:',index2,index1,distancia)
        self.vertices[index2].append(AdjacentVertex(index1,distance))

        
    def areConnected(self,center1,center2):
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)
        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        
        for adj in self.vertices[index1]:
            if adj.vertex==index2:
                return adj.weight
        #print(pto1,pto2," no están conectados")
        return 0
            
    def removeConnection(self,center1,center2):
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)
        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        
        for adj in self.vertices[index1]:
            if adj.vertex==index2:
                self.vertices[index1].remove(adj)
                break
                
        for adj in self.vertices[index2]:
            if adj.vertex==index1:
                self.vertices[index2].remove(adj)
                break

    
        

    def createPath(self): 
        """This function prints the vertices by dfs algorithm"""
        #print('dfs traversal:')
        # Mark all the vertices as not visited 
        visited = [False] * len(self.vertices)

        paths=[]
        for v in  self.vertices:
            if visited[v]==False:
                self._dfs(v, visited,paths)
        
        print()
        return paths
        
    def _dfs(self, v, visited,paths): 
        # Mark the current node as visited and print it 
        visited[v] = True
        #print(self.centers[v], end = ' ') 
        paths.append(self.centers[v])
        # Recur for all the vertices  adjacent to this vertex 
        for adj in self.vertices[v]: 
          i=adj.vertex
          if visited[i] == False: 
            self._dfs(i, visited,paths) 
            
            
    
    def printSolution(self,distances,previous,v): 
        """imprime los caminos mínimos desde v"""
        for i in range(len(self.vertices)):
          if distances[i]==sys.maxsize:
            print("There is not path from ",v,' to ',i)
          else: 
            minimum_path=[]
            prev=previous[i]
            while prev!=-1:
              minimum_path.insert(0,self.centers[prev])
              prev=previous[prev]
            
            minimum_path.append(self.centers[i])  
    
            print('Ruta mínima de:',self.centers[v],'->',self.centers[i],", distance", distances[i], ', ruta: ',  end= ' ')
            for x in minimum_path:
                print(x,end= ' ')
            print()
    
    def minDistance(self, distances, visited): 
        """This functions returns the vertex (index) with the mininum distance. To do this, 
        we see in the list distances. We 
        only consider the set of vertices that have not been visited"""
        # Initilaize minimum distance for next node 
        min = sys.maxsize 
    
        #returns the vertex with minimum distance from the non-visited vertices
        for i in range(len(self.vertices)): 
          if distances[i] <= min and visited[i] == False: 
            min = distances[i] 
            min_index = i 
      
        return min_index 
    
    def dijkstra(self, v=0): 
        """"This function takes the index of a delivery point pto and calculates its mininum path 
        to the rest of vertices by using the Dijkstra algoritm. Devuelve una lista con las distancias
        y una lista con los vértices anteriores a uno dado en el camino mínimo"""  
        
        
        #we use a Python list of boolean to save those nodes that have already been visited  
        visited = [False] * len(self.vertices) 
    
        #this list will save the previous vertex 
        previous=[-1]*len(self.vertices) 
    
        #This array will save the accumulate distance from v to each node
        distances = [sys.maxsize]*len(self.vertices) 
        #The distance from v to itself is 0
        distances[v] = 0
    
        for i in range(len(self.vertices)): 
          # Pick the vertex with the minimum distance vertex.
          # u is always equal to v in first iteration 
          u = self.minDistance(distances, visited) 
          # Put the minimum distance vertex in the shotest path tree
          visited[u] = True
          
          # Update distance value of the u's adjacent vertices only if the current  
          # distance is greater than new distance and the vertex in not in the shotest path tree 
          for adj in self.vertices[u]:
            i=adj.vertex
            w=adj.weight
            if visited[i]==False and distances[i]>distances[u]+w:
              distances[i]=distances[u]+w   
              previous[i]=u       
              
        #finally, we print the minimum path from v to the other vertices
        #self.printSolution(distances,previous,v)
        return previous,distances
 
    def minimumPath(self, start, end):
        """calcula la ruta mínima entre dos puntos de entrega"""
        indexStart=self._getIndice(start)
        if indexStart==-1:
            print(str(start) + " does not exist")
            return None
        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end)  + " does not exist")
            return None
        
        previous,distances=self.dijkstra(indexStart)
        
        #construimos el camino mínimo
        minimum_path=[]
        prev=previous[indexEnd]
        while prev!=-1:
            minimum_path.insert(0,str(self.centers[prev]))
            prev=previous[prev]
            
        minimum_path.append(str(self.centers[indexEnd]))
        return minimum_path, distances[indexEnd]
    
    
    def minimumPathBF(self,start,end):
        """"calcula y devuelve la ruta mínima entre start y end, aplicando el algoritmo de 
         Bellman-Ford. """
        minimum_path=[]
        minimumDistance=0
        
        #first, we obtains the indixes in the dictionary of the two centers
        indexStart=self._getIndice(start)
        if indexStart==-1:
            print(str(start) + " does not exist")
            return None
        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end)  + " does not exist")
            return None

        #APPLY THE BELLMAN-FORD ALGORITHM
        
        distance = [sys.maxsize]*len(self.vertices)#create the list of distances and initialice it to infinite
        previous=[-1]*len(self.vertices) #create the list of previous vertex and initialice it to -1
        
        distance[indexStart] = 0 #update the prev vertex of the start
        
        #algortithm
        for i in range(len(self.centers)-1): #iterations over the different centers
            for u in range(len(self.centers)):
                for v in self.vertices[u]:
                    if distance[v.vertex] > distance[u]+ v.weight: 
                        distance[v.vertex] = distance[u] + v.weight #update the distance if it is smaller on the list
                        previous[v.vertex] =  u #update the previous vertex on the list
        
        #there is no negative weights, so we do not need this part of the algorithm
        
        #for u in range(len(self.vertices)):
        #    for v in self.vertices[u]:        
         #       if distance[v.vertex] > distance[u] + v.weight:
          #          return False
        
        
        #update list that we are going to return
        prev=previous[indexEnd]  
        while prev!=-1: #util we reach the start center
            minimum_path.insert(0,str(self.centers[prev])) #insert previous center in minimum_path
            prev=previous[prev]#update pev
            
        minimum_path.append(str(self.centers[indexEnd]))#insert the last center
        minimumDistance = distance[indexEnd] #obtain minimun distance from distance list at the position of the indexEnd

        return minimum_path, minimumDistance
    


    def minimumPathFW(self,start,end):
        """"calcula y devuelve la ruta mínima entre start y end, aplicando el algoritmo de 
         Floyd-Warshall. """
        minimum_path=[]
        minimumDistance=0

        #first, we obtains the indixes in the dictionary of the two centers
        indexStart=self._getIndice(start)
        if indexStart==-1:
            print(str(start) + " does not exist")
            return None
        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end)  + " does not exist")
            return None
        
        
        
        #APPLY THE FLOYD WARSHALL ALGORITHM
        
        
        #first, initialice the matrices
        
        #d matrix with the distances, initialice to infinit
        d = [ [ float ('inf') for i in range(len(self.centers)) ] for j in range(len(self.centers)) ]
        #p matrix with the previous vertex, initialice with None
        p = [ [ None for i in range(len(self.centers)) ] for j in range(len(self.centers)) ]
        
        #update matrices with current distances
        for i in range(len(self.centers)):
            for j in range(len(self.centers)):
                if i == j:
                    d[i][j] = 0  #distance from a center to itself is 0
                    
        for i in range(len(self.vertices)): #uodating distances looking in the vertex and its weights
            for j in self.vertices[i]:
                d[i][j.vertex] = j.weight
                p[i][j.vertex] = i

        #apply the algorithm
        for k in range(len(self.centers)):
            for i in range(len(self.centers)):
                for j in range(len(self.centers)):
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]  #update the distances according the method of the algorithm
                        p[i][j] = p[k][j]  #also updating the previous vertex
        
        
        #update list that we are going to return
        n = indexEnd
        while n != indexStart and n!= None:
            minimum_path.insert(0, str(self.centers[n])) #insert the vertices we visit on the path
            n = p[indexStart][n]
            
        minimum_path.insert(0, str(self.centers[indexStart])) #insert the indexStart 
        minimumDistance = d[indexStart][indexEnd] #obtaining the distance from the matrix [origin center][final center]

        return minimum_path, minimumDistance

def test():
    #https://www.bogotobogo.com/python/images/Dijkstra/graph_diagram.png
   
    m=Map()
    for c in ['A','B','C','D','E','F']:
        m.addHealthCenter(HealthCenter(c))
    
    print(m)
    m.addConnection(m.centers[0],m.centers[1],7)#A,B,7
    m.addConnection(m.centers[0],m.centers[2],9)#A,C,9
    m.addConnection(m.centers[0],m.centers[5],14)#A,F,14
    
    m.addConnection(m.centers[1],m.centers[2],10)#B,C,10
    m.addConnection(m.centers[1],m.centers[3],15)#B,D,15
    
    m.addConnection(m.centers[2],m.centers[3],11)#C,D,11
    m.addConnection(m.centers[2],m.centers[5],2)#C,F,2
    
    m.addConnection(m.centers[3],m.centers[4],6)#D,E,6
    
    m.addConnection(m.centers[4],m.centers[5],9)#E,F,9
    print(m)
   
    c1=m.centers[0]
    c2=m.centers[3]
    print(c1,c2,' are connected?:',m.areConnected(c1,c2))
    
    c2=m.centers[1]
    print(c1,c2,' are connected?:',m.areConnected(c1,c2))
    
    #m.removeConnection(c1,c2)
    print(m)

    print('createPath:',end=' ')
    ruta=m.createPath()
    #print('Ruta:',ruta)
    for r in ruta:
        print(r, end=' ')
    print()

    minimum_path,d=m.minimumPathFW(c1,c2)
    for p in minimum_path:
        print(p,end=' ')
    print('total distance:',d)
    
    print("----------------- ALGORITMO dijkstra A-F-----------")
   
    minimum_path,d=m.minimumPath(m.centers[0],m.centers[5])
  
    print(minimum_path,d)
  
     
  
      
  
    print("----------------- ALGORITMO bellmanFord A-F-----------")
  
    minimum_path,d=m.minimumPathBF(m.centers[0],m.centers[5])
  
    print(minimum_path,d)

   

    

   

    print("----------------- ALGORITMO floyd warshall A-F-----------")
  
    minimum_path,d=m.minimumPathFW(m.centers[0],m.centers[5])
  
    print(minimum_path,d)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    test()
