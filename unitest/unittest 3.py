#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from fase3 import Map
from fase3 import HealthCenter


class Test(unittest.TestCase):
    
    def setUp(self):
        #print('\nLos datos se inicializan para cada test..\n')
        
        
        
        #https://www.bogotobogo.com/python/images/Dijkstra/graph_diagram.png
        
        self.m=Map()
        
        for c in ['A','B','C','D','E','F']:
            self.m.addHealthCenter(HealthCenter(c))
            
        A=self.m.centers[0]
        B=self.m.centers[1]
        C=self.m.centers[2]
        D=self.m.centers[3]
        E=self.m.centers[4]
        F=self.m.centers[5]
        
        self.m.addConnection(A,B,7)#A,B,7
        self.m.addConnection(A,C,9)#A,C,9
        self.m.addConnection(A,F,14)#A,F,14
        
        self.m.addConnection(B,C,10)#B,C,10
        self.m.addConnection(B,D,15)#B,D,15
        self.m.addConnection(C,D,11)#C,D,11
        self.m.addConnection(C,F,2)#C,F,2
        self.m.addConnection(E,D,6)#E,D,6

        self.m.addConnection(E,F,9)#E,F,9
        
        #print(self.m)
        
        
        
    def test1_areConnected(self):
        #print(str(self.m))
        #comprobamos por ejemplo las conexiones de p0
        print('\n****** test1_areConnected ******************')
        A=self.m.centers[0]
        B=self.m.centers[1]
        C=self.m.centers[2]
        D=self.m.centers[3]
        E=self.m.centers[4]
        F=self.m.centers[5]


        self.assertEqual(self.m.areConnected(A,B),7)
        self.assertEqual(self.m.areConnected(B,A),7)

        self.assertEqual(self.m.areConnected(A,C),9)
        self.assertEqual(self.m.areConnected(A,F),14)
        self.assertEqual(self.m.areConnected(B,C),10)
        self.assertEqual(self.m.areConnected(B,D),15)
        
        #y una de sus recíprocas
        #comprobamos algunas que no están conectadas
        self.assertEqual(self.m.areConnected(A,D),0)
        self.assertEqual(self.m.areConnected(A,E),0)
        self.assertEqual(self.m.areConnected(B,F),0)

        print('****** OK test1_areConnected ******************')
    
        
    def test2_removeConnection(self):
        #print(str(self.m))
        #comprobamos por ejemplo las conexiones de p0
        print('\n****** test2_removeConnection ******************')
        A=self.m.centers[0]
        D=self.m.centers[3]

        self.assertEqual(self.m.areConnected(A,D),0)
        self.m.addConnection(A,D,33)                    #A,D,33
        self.assertEqual(self.m.areConnected(A,D),33)
        self.m.removeConnection(A,D)                    #A,D,33
        self.assertEqual(self.m.areConnected(A,D),0)


        print('****** OK test2_removeConnection ******************')
    
           

    def test3_createPath(self):
        print('\n****** test3_createPath ******************')
        result=self.m.createPath()
        A=self.m.centers[0]
        B=self.m.centers[1]
        C=self.m.centers[2]
        D=self.m.centers[3]
        E=self.m.centers[4]
        F=self.m.centers[5]
        dfs=[A,B,C,D,E,F]
        

        self.assertEqual(len(result),len(dfs))
        self.assertEqual(result,dfs)

        
        
        print('****** OK test3_createPath ******************')
    
    def test4_minimumPath(self):
        print('\n******  test4_minimumPath ALGORITMO dijkstra (A,E)******************')

        A=self.m.centers[0]
        E=self.m.centers[4]
        
        result,d=self.m.minimumPath(A,E)
        expepcted=['A', 'C', 'F', 'E']
        d_expected=20
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPath(E,A)
        expepcted=['E', 'F', 'C', 'A']
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)

       
        print('****** OK test4_minimumPath ******************')

    def test5_minimumPathBF(self):
        print("\n----------------- test5_minimumPathBF ALGORITMO Bellman Ford (A,B) -----------")
        A=self.m.centers[0]
        B=self.m.centers[1]
        result,d=self.m.minimumPathBF(A,B)
        expepcted=['A','B']
        d_expected=7
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathBF(B,A)
        expepcted=['B','A']
        d_expected=7
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test5_minimumPathBF ******************')

   
    
    def test6_minimumPathBF(self):
        print("\n----------------- test6_minimumPathBF: ALGORITMO Bellman Ford  (A,E) -----------")
        A=self.m.centers[0]
        E=self.m.centers[4]
        
        result,d=self.m.minimumPathBF(A,E)
        expepcted=['A', 'C', 'F', 'E']
        d_expected=20
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathBF(E,A)
        expepcted=['E', 'F', 'C', 'A']
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test6_minimumPathBF ******************')

                
    def test7_minimumPathBF(self):
        print("\n----------------- test7_minimumPathBF: ALGORITMO Bellman Ford  (A,F) -----------")
        A=self.m.centers[0]
        F=self.m.centers[5]
        
        result,d=self.m.minimumPathBF(A,F)
        
        expepcted=['A', 'C', 'F']
        d_expected=11
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathBF(F,A)
        expepcted=['F', 'C', 'A']
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test7_minimumPathBF ******************')

        
    def test8_minimumPathBF(self):
        print("\n----------------- test8_minimumPathBF: ALGORITMO Bellman Ford  (B,E) -----------")
        B=self.m.centers[1]
        E=self.m.centers[4]
        
        result,d=self.m.minimumPathBF(B,E)
        
        expepcted1=['B', 'D', 'E']
        expepcted2=['B', 'C', 'F', 'E']

        d_expected=21
        
        self.assertEqual(d,d_expected)
        try:
            self.assertEqual(result,expepcted1)
        except:
            self.assertEqual(result,expepcted2)

        
        result,d=self.m.minimumPathBF(E,B)

        expepcted1=['E', 'D', 'B']
        expepcted2=['E', 'F', 'C', 'B']

        self.assertEqual(d,d_expected)
        try:
            self.assertEqual(result,expepcted1)
        except:
            self.assertEqual(result,expepcted2)
        print('****** OK test8_minimumPathBF ******************')

    
    
    def test9_minimumPathBF(self):
        print("\n----------------- test9_minimumPathBF: ALGORITMO Bellman Ford  (D,F) -----------")
        D=self.m.centers[3]
        F=self.m.centers[5]
        
        result,d=self.m.minimumPathBF(D,F)
        
        expepcted=['D', 'C', 'F']
        d_expected=13
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathBF(F,D)

        expepcted=['F', 'C', 'D']
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test9_minimumPathBF ******************')

    def test10_minimumPathFW(self):
        print("\n----------------- test10_minimumPathFW ALGORITMO Floyd Warshall (A,B) -----------")
        A=self.m.centers[0]
        B=self.m.centers[1]
        result,d=self.m.minimumPathFW(A,B)
        expepcted=['A','B']
        d_expected=7
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathFW(B,A)
        expepcted=['B','A']
        d_expected=7
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test10_minimumPathFW ******************')

   
    
    def test11_minimumPathFW(self):
        print("\n----------------- test11_minimumPathFW: ALGORITMO Floyd Warshall  (A,E) -----------")
        A=self.m.centers[0]
        E=self.m.centers[4]
        
        result,d=self.m.minimumPathFW(A,E)
        expepcted=['A', 'C', 'F', 'E']
        d_expected=20
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathFW(E,A)
        expepcted=['E', 'F', 'C', 'A']
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test11_minimumPathFW ******************')

                
    def test12_minimumPathFW(self):
        print("\n----------------- test12_minimumPathFW: ALGORITMO Floyd Warshall  (A,F) -----------")
        A=self.m.centers[0]
        F=self.m.centers[5]
        
        result,d=self.m.minimumPathFW(A,F)
        
        expepcted=['A', 'C', 'F']
        d_expected=11
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathFW(F,A)
        expepcted=['F', 'C', 'A']
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test12_minimumPathFW ******************')

        
    def test13_minimumPathBF(self):
        print("\n----------------- test13_minimumPathFW: ALGORITMO Floyd Warshall  (B,E) -----------")
        B=self.m.centers[1]
        E=self.m.centers[4]
        
        result,d=self.m.minimumPathFW(B,E)
        
        expepcted1=['B', 'D', 'E']
        expepcted2=['B', 'C', 'F', 'E']

        d_expected=21
        
        self.assertEqual(d,d_expected)
        try:
            self.assertEqual(result,expepcted1)
        except:
            self.assertEqual(result,expepcted2)

        
        result,d=self.m.minimumPathFW(E,B)

        expepcted1=['E', 'D', 'B']
        expepcted2=['E', 'F', 'C', 'B']

        self.assertEqual(d,d_expected)
        try:
            self.assertEqual(result,expepcted1)
        except:
            self.assertEqual(result,expepcted2)
        print('****** OK test13_minimumPathFW ******************')

    
    
    def test14_minimumPathFW(self):
        print("\n----------------- test14_minimumPathFW: ALGORITMO Floyd Warshall  (D,F) -----------")
        D=self.m.centers[3]
        F=self.m.centers[5]
        
        result,d=self.m.minimumPathFW(D,F)
        
        expepcted=['D', 'C', 'F']
        d_expected=13
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        
        result,d=self.m.minimumPathFW(F,D)

        expepcted=['F', 'C', 'D']
        
        self.assertEqual(d,d_expected)
        self.assertEqual(result,expepcted)
        print('****** OK test14_minimumPathFW ******************')

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()




