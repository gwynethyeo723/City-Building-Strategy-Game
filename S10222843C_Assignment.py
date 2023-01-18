#Yeo Sze Yun, Gwyneth S10222843C - DS01/P08
#date: 9/8/21

'''
This program is a game that can let users build buildings and score points. It can also save and load previous game plays (if any).
'''
import random
import os
####functions:####
##main menu - prints out options for the main menu for user to choose
def main_menu():
    print('1. Start new game')
    print('2. Load saved game')
    print('3. Show high scores')
    print()
    print('0. Exit')

##main menu choice - prompts user to choose option from main menu
def mainmenu_choice():
    global mainmenuchoice
    try:
        mainmenuchoice=int(input('Your choice? '))
        #see if the user's option is valid 
        while mainmenuchoice!=1 and mainmenuchoice!=2 and mainmenuchoice!=3 and mainmenuchoice!=0:
            mainmenuchoice=int(input('Please enter either 1,2,3 or 0. Your choice? '))
    except:
        mainmenu_choice()
    
    return mainmenuchoice

##board - prints out the board and the contents that may be inside it
def board():
    global num_of_col
    global num_of_row
    num_of_col=len(map[0])
    num_of_row=len(map)
    #print out the contents of the board
    print('{:>6}{:>6}{:>6}{:>6}'.format('A','B','C','D'))
    print('  ',end='')
    for col in range(num_of_col):
        print('+-----',end='')
    print('+')
    for row in range(num_of_row):
        print('{:>2}'.format(row+1),end='')
     
        for col in range(num_of_col):
            print('|{:^5}'.format(map[row][col]),end='') #print out the buildings if any
        print('|')
        print('  ',end='')
        for col in range(num_of_col):
            print('+-----',end='')
        print('+')
        
##selection - prints out the options for user to choose what, where they want
#to build, see remaining buildings, current scores, save game and exit back
#to main menu
def selection():
        global first
        first=random.choice(building_list)
        global second
        second=random.choice(building_list)
        print('1. Build a {}'.format(first))
        print('2. Build a {}'.format(second))
        print('3. See remaining buildings')
        print('4. See current score')
        print()
        print('5. Save game')
        print('0. Exit to main menu')

##selection choice - prompts user for choice from selection menu
def selection_choice():
    global selectionchoice
    try:
        selectionchoice=int(input('Your choice? '))
        #see if the user's option is valid 
        while selectionchoice!=1 and selectionchoice!=2 and selectionchoice!=3 and\
              selectionchoice!=4 and selectionchoice!=5 and selectionchoice!=0:
            selectionchoice=int(input('Please enter either 1,2,3,4,5 or 0. Your choice? '))
    except:
        selection_choice()
    return selectionchoice

##build where choice - prompt user for choice on where to build the building
def build():
        global build_where
        build_where=input('Build where?')
        return build_where

##checking - check whether the building is built next to an existing building
def checking(build_where):
    global check
    
    #A1 corner
    if build_where==[0,0]:
        if map[build_where[0]+1][build_where[1]]!=' ' or map[build_where[0]][build_where[1]+1]!=' ': #A2 or B1
            check=True
        else:
            check=False
    #D1 corner
    elif build_where==[0,num_of_col-1]:
        if map[build_where[0]][build_where[1]-1]!=' ' or map[build_where[0]+1][build_where[1]]!=' ': #C1 or D2
            check=True
        else:
            check=False
    #D4 corner
    elif build_where==[num_of_row-1,num_of_col-1]:
        if map[build_where[0]-1][build_where[1]]!=' ' or map[build_where[0]][build_where[1]-1]!=' ': #D3 or C4
            check=True
        else:
            check=False
    #A4 corner
    elif build_where==[num_of_row-1,0]:
        if map[build_where[0]-1][build_where[1]]!=' ' or map[build_where[0]][build_where[1]+1]!=' ': #A3 or B4
            check=True
        else:
            check=False
            
    elif build_where[1]==0 or build_where[1]==num_of_col-1:
        for j in range(1,num_of_row-1):
            #first column 
            if build_where==[j,0]: #A1/A2 or A3/A4 or B2/B3
                if map[build_where[0]-1][build_where[1]]!=' ' or map[build_where[0]+1][build_where[1]]!=' ' or map[build_where[0]][build_where[1]+1]!=' ':
                    check=True
                else:
                    check=False
            #last column 
            elif build_where==[j,num_of_col-1]: #D1/D2 or D3/D4 or C2/C3
                if map[build_where[0]-1][build_where[1]]!=' ' or map[build_where[0]+1][build_where[1]]!=' ' or map[build_where[0]][build_where[1]-1]!=' ':
                    check=True
                else:
                    check=False
                
    elif build_where[0]==0 or build_where[0]==num_of_row-1:
        for j in range(1,num_of_col-1):
            #first row
            if build_where==[0,j]: #A1/B1 or B2/C2 or C1/D1
                if map[build_where[0]][build_where[1]-1]!=' ' or map[build_where[0]+1][build_where[1]]!=' ' or map[build_where[0]][build_where[1]+1]!=' ':
                    check=True
                else:
                    check=False
            #last row
            elif build_where==[num_of_row-1,j]: #A4/B4 or C4/D4 or B3/C3
                if map[build_where[0]][build_where[1]-1]!=' ' or map[build_where[0]][build_where[1]+1]!=' ' or map[build_where[0]-1][build_where[1]]!=' ':
                    check=True
                else:
                    check=False
    else:
        #B2/B3/C2/C3
        if map[build_where[0]-1][build_where[1]]!=' ' or map[build_where[0]+1][build_where[1]]!=' ' or map[build_where[0]][build_where[1]-1]!=' ' or map[build_where[0]][build_where[1]+1]!=' ' :
            check=True
        else:
            check=False

##position - check whether the place where the user wants to build the building
#has no building and also whether the input is valid
def position(choice):
    global build_where
    global check
    global i 
    try:
        build_where=build_where.upper()
        build_where=build_where.replace(build_where[1],';'+build_where[1]) #cannot just insert in as build_where is a str 
        build_where=build_where.split(';')
        build_where=[building_dict[build_where[1]],building_dict[build_where[0]]]
   
    
        while map[build_where[0]][build_where[1]] != ' ': #so that it does not replace the buildings
            build_where=input('You have already placed a building there. Please choose where to build your buildings again: ')
            build_where=build_where.upper()
            build_where=build_where.replace(build_where[1],';'+build_where[1])
            build_where=build_where.split(';')
            build_where=[building_dict[build_where[1]],building_dict[build_where[0]]]
        if i!=1: #for turn 2 onwards 
            checking(build_where)
            if check==False:
                while check==False:
                    build_where=input('You are not allowed to build there. Please choose where to build your buildings again: ')
                    build_where=build_where.upper()
                    build_where=build_where.replace(build_where[1],';'+build_where[1])
                    build_where=build_where.split(';')
                    build_where=[building_dict[build_where[1]],building_dict[build_where[0]]]
                    checking(build_where)
        map[build_where[0]].pop(build_where[1])
        map[build_where[0]].insert(build_where[1],choice)
        building_list.remove(first)
        building_list.remove(second)
    except: #if the input is not inside the board e.g e4
        print('Invalid input. Please choose where to build your buildings again: ')
        build()
        position(option)
        

##remaining buildings - lets user see the remaining buildings
def remaining_buildings():
    print('{:<20}{}'.format('Building','Remaining'))
    print('{:<20}{}'.format('-'*len('Building'),'-'*len('Remaining')))
    for j in range(len(count_list)): 
        print('{:<20}{}'.format(str(count_list[j][0]),str(count_list[j][1])))
    

##scoring - calculate the user's score
def scoring():
    global total_score
    #score for BCH
    
    BCH=[0] #put 0 cos if not if there is nothing in the list right then wont be 0 
    for k in range(num_of_row):
        for m in range(num_of_col):
            if map[k][m]=='BCH':
                #check for BCH in column A and D
                if m==0 or m==num_of_col-1:
                    BCH==BCH.append(3)
                #check for BCH in other columns (B and C)
                else:
                    BCH==BCH.append(1)
                    
    #score for FAC
    
    FAC=[0]
    temp=0
    for k in range(num_of_row):
        temp+=map[k].count('FAC') #count in total got how many FAC
        
    if temp<5:
        for r in range(1,temp+1): #if there is less than 5
            FAC==FAC.append(temp)
    else:
        for r in range(1,5): #if there is more than 5 
            FAC==FAC.append(4)
        for r in range(5,temp+1):
            FAC==FAC.append(1)
            
    #score for HSE
    
    HSE=[0]
   
    for x in range(num_of_row):
        for y in range(num_of_row):
            if map[x][y]=='HSE':
                temp=0
                if x==0 and y==0: #A1
                    if map[0][y+1]=='FAC' or map[x+1][0]=='FAC': #B1 or A2
                        temp+=1
                    elif map[0][y+1]!='FAC' and map[x+1][0]!='FAC': #use and so that to make sure there is no FAC at all 
                        if map[0][y+1]=='SHP' or map[0][y+1]=='HSE': #check whether at B1 there is SHP or HSe
                            temp+=1
                        elif map[0][y+1]=='BCH': #check whether at B1 there is BCH
                            temp+=2
                        else:
                            temp+=0
                        if map[x+1][0]=='SHP' or map[x+1][0]=='HSE': #check whether at A2 there is SHP or HSE
                            temp+=1
                        elif map[x+1][0]=='BCH': #check whether at A2 there is BCH
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                    
                            
                elif x==num_of_row-1 and y==0: #A4
                    if map[x-1][0]=='FAC' or map[x][y+1]=='FAC': #A3 or B4
                        temp+=1
                    elif map[x-1][0]!='FAC' and map[x][y+1]!='FAC': 
                        if map[x-1][0]=='SHP' or map[x-1][0]=='HSE':
                            temp+=1
                        elif map[x-1][0]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x][y+1]=='SHP' or map[x][y+1]=='HSE':
                            temp+=1
                        elif map[x][y+1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp++0
                            
                elif x==0 and y==num_of_col-1: #D1
                    if map[0][y-1]=='FAC' or map[x+1][y]=='FAC': #C1 or D2
                        temp+=1
                    elif map[0][y-1]!='FAC' and map[x+1][y]!='FAC':
                        if map[0][y-1]=='SHP' or map[0][y-1]=='HSE':
                            temp+=1
                        elif map[0][y-1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x+1][y]=='SHP' or map[x+1][y]=='HSE':
                            temp+=1
                        elif map[x+1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                        
                elif x==num_of_row-1 and y==num_of_col-1: #D4
                    if map[x][y-1]=='FAC' or map[x-1][y]=='FAC': #C4 or D3
                        temp+=1
                    elif map[x][y-1]!='FAC' and map[x-1][y]!='FAC':
                        if map[x][y-1]=='SHP' or map[x][y-1]=='HSE':
                            temp+=1
                        elif map[x][y-1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x-1][y]=='SHP' or map[x-1][y]=='HSE':
                            temp+=1
                        elif map[x-1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                elif x==0 and (y!=0 and y!=num_of_col-1): #first row
                    if map[x][y-1]=='FAC' or map[x][y+1]=='FAC' or map[x+1][y]=='FAC': #A1/B1 or C1/D1 or B2/C2
                        temp+=1
                    elif map[x][y-1]!='FAC' and map[x][y+1]!='FAC' and map[x+1][y]!='FAC':
                        if map[x][y-1]=='SHP' or map[x][y-1]=='HSE':
                            temp+=1
                        elif map[x][y-1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x][y+1]=='SHP' or map[x][y+1]=='HSE':
                            temp+=1
                        elif map[x][y+1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x+1][y]=='SHP' or map[x+1][y]=='HSE':
                            temp+=1
                        elif map[x+1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                elif x==num_of_row-1 and (y!=0 and y!=num_of_col-1): #last row 
                    if map[x][y-1]=='FAC' or map[x][y+1]=='FAC' or map[x-1][y]=='FAC': #A4/B4 or C4/D4 or B3/C3 
                        temp+=1
                    elif map[x][y-1]!='FAC' and map[x][y+1]!='FAC' and map[x-1][y]!='FAC':
                        if map[x][y-1]=='SHP' or map[x][y-1]=='HSE':
                            temp+=1
                        elif map[x][y-1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x][y+1]=='SHP' or map[x][y+1]=='HSE':
                            temp+=1
                        elif map[x][y+1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x-1][y]=='SHP' or map[x-1][y]=='HSE':
                            temp+=1
                        elif map[x-1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                elif (x!=0 and x!=num_of_row-1) and y==0: #first column
                    if map[x-1][y]=='FAC' or map[x+1][y]=='FAC' or map[x][y+1]=='FAC': #A1/A2 or A3/A4 or B2/B3
                        temp+=1
                    elif map[x-1][y]!='FAC' and map[x+1][y]!='FAC' and map[x][y+1]!='FAC':
                        if map[x-1][y]=='SHP' or map[x-1][y]=='HSE':
                            temp+=1
                        elif map[x-1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x+1][y]=='SHP' or map[x+1][y]=='HSE':
                            temp+=1
                        elif map[x+1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x][y+1]=='SHP' or map[x][y+1]=='HSE':
                            temp+=1
                        elif map[x][y+1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                elif (x!=0 and x!=num_of_row-1) and y==num_of_col-1: #last column 
                    if map[x-1][y]=='FAC' or map[x+1][y]=='FAC' or map[x][y-1]=='FAC': #D1/D2 or D3/D4 or C2/C3
                        temp+=1
                    elif map[x-1][y]!='FAC' and map[x+1][y]!='FAC' and map[x][y-1]!='FAC':
                        if map[x-1][y]=='SHP' or map[x-1][y]=='HSE':
                            temp+=1
                        elif map[x-1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x+1][y]=='SHP' or map[x+1][y]=='HSE':
                            temp+=1
                        elif map[x+1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x][y-1]=='SHP' or map[x][y-1]=='HSE':
                            temp+=1
                        elif map[x][y-1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                else:
                    if map[x-1][y]=='FAC' or map[x+1][y]=='FAC' or map[x][y-1]=='FAC' or map[x][y+1]=='FAC': #B2/B3/C2/C3
                        temp+=1
                    elif map[x-1][y]!='FAC' and map[x+1][y]!='FAC' and map[x][y-1]!='FAC' and map[x][y+1]!='FAC':
                        if map[x-1][y]=='SHP' or map[x-1][y]=='HSE':
                            temp+=1
                        elif map[x-1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x+1][y]=='SHP' or map[x+1][y]=='HSE':
                            temp+=1
                        elif map[x+1][y]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x][y-1]=='SHP'or map[x][y-1]=='HSE':
                            temp+=1
                        elif map[x][y-1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                        if map[x][y+1]=='SHP' or map[x][y+1]=='HSE':
                            temp+=1
                        elif map[x][y+1]=='BCH':
                            temp+=2
                        else:
                            temp+=0
                    else:
                        temp+=0
                       
                HSE==HSE.append(temp)       

    #score for SHP
    
    SHP=[0]

    for x in range(num_of_row):
        for y in range(num_of_col):
            if map[x][y]=='SHP':
                temp2=['SHP']
                temp=0
                if x==0 and y==0: #A1
                    temp2==temp2.append(map[x][y+1]) #B1
                    temp2==temp2.append(map[x+1][y]) #A2
                    
                elif x==num_of_row-1 and y==0: #A4
                    temp2==temp2.append(map[x-1][y]) #A3
                    temp2==temp2.append(map[x][y+1]) #B4

                elif x==0 and y==num_of_col-1: #D1
                    temp2==temp2.append(map[x][y-1]) #C1
                    temp2==temp2.append(map[x+1][y]) #D2

                elif x==num_of_row-1 and y==num_of_col-1: #D4
                    temp2==temp2.append(map[x-1][y]) #D3
                    temp2==temp2.append(map[x][y-1]) #C4

                elif x==0 and (y!=0 and y!=num_of_col-1): #first row
                    temp2==temp2.append(map[x][y-1]) #A1/B1
                    temp2==temp2.append(map[x][y+1]) #C1/D1
                    temp2==temp2.append(map[x+1][y]) #B2/C2

                elif x==num_of_row-1 and (y!=0 and y!=num_of_col-1): #last row
                    temp2==temp2.append(map[x][y-1]) #A4/B4
                    temp2==temp2.append(map[x][y+1]) #C4/D4
                    temp2==temp2.append(map[x-1][y]) #B3/C3

                elif (x!=0 and x!=num_of_row-1) and y==0: #first column
                    temp2==temp2.append(map[x-1][y]) #A1/A2
                    temp2==temp2.append(map[x+1][y]) #A3/A4
                    temp2==temp2.append(map[x][y+1]) #B2/B3

                elif (x!=0 and x!=num_of_row-1) and y==num_of_col-1: #last column
                    temp2==temp2.append(map[x-1][y]) #D1/D2
                    temp2==temp2.append(map[x+1][y]) #D3/D4
                    temp2==temp2.append(map[x][y-1]) #C2/C3

                else:
                    temp2==temp2.append(map[x-1][y])
                    temp2==temp2.append(map[x+1][y])
                    temp2==temp2.append(map[x][y-1])
                    temp2==temp2.append(map[x][y+1])

                if temp2.count('SHP')>1:
                    temp+=1
                if temp2.count('BCH')>0:
                    temp+=1
                if temp2.count('FAC')>0:
                    temp+=1
                if temp2.count('HWY')>0:
                    temp+=1
                if temp2.count('HSE')>0:
                    temp+=1
                SHP==SHP.append(temp)
                
    #score for HWY
    
    HWY=[0]
    for x in range(num_of_row): #check each row
        count=map[x].count('HWY') #count how many HWY in each row
        if count==1:
            HWY==HWY.append(1) #only one HWY in the row so +1
        elif count>1: #2 or more HWY in one row
            firstindex=map[x].index('HWY') #find out the index of the first time HWY appears in the row
            
            for k in range(num_of_col):#find out the index of the last time HWY appears in the row
                if map[x][k]=='HWY': #have to do this because if .index('HWY',count), then it will only find the element at that index or
                                      #if there is another 'HWY' after that index if not it will be deemed as 'HWY' not in list
                    lastindex=k
            
            if lastindex-firstindex==1: #meaning there is 2 HWY side by side
                for y in range(2):
                    HWY==HWY.append(2)
            elif lastindex-firstindex==2: #meaning there is 3 HWY side by side or 2 HWY in a row but not side by side
                if map[x][lastindex-1]=='HWY': #check the in between value isit HWY, if yes means 3 HWY is side by side
                    for y in range(3):
                        HWY==HWY.append(3)
                else: #the in between value is either ' ' or 'BCH' or 'HSE' or 'FAC' or 'SHP'
                    for y in range(2):
                        HWY==HWY.append(1)
            elif lastindex-firstindex==3: #meaning there is 4 HWY side by side or 2 HWY not side by side, at extreme ends or 3 HWY not in a row
                if map[x][lastindex-1]!='HWY' and map[x][firstindex+1]!='HWY': #find out beside got HWY anot, if both dont have meens that 2 HWY at extreme ends
                    for y in range(2):
                        HWY==HWY.append(1)
                    
                elif map[x][lastindex-1]=='HWY' and map[x][firstindex+1]=='HWY': #find out if beside got HWY anot if both got means 4 HWY is side by side
                    for y in range(4):
                        HWY==HWY.append(4)
                else: #left the 2 HWY side by side and 1 HWY not
                    if map[x][firstindex+1]!='HWY' and map[x][lastindex-1]=='HWY': #means index 1 is not HWY
                        HWY==HWY.append(1)
                        for y in range(2):
                            HWY==HWY.append(2)
                        
                    elif map[x][lastindex-1]!='HWY' and map[x][firstindex+1]=='HWY': #means index 2 is not HWY
                        for y in range(2):
                            HWY==HWY.append(2)
                        HWY==HWY.append(1)
                        
        else:
            HWY==HWY

    #print out the scores for each building respectively
    
    HSE_score=HSE[0]          
    print('HSE: ', end='')
    if len(HSE)>1:
        print(HSE[1],end=' ')
        HSE_score+=HSE[1]
        for z in range(2,len(HSE)):
            print(' + ',HSE[z],end=' ')
            HSE_score+=HSE[z]
    else:
        print(HSE[0],end=' ')
    print(' = ',HSE_score)
    

    FAC_score=FAC[0]
    print('FAC: ',end='')
    if len(FAC)>1:
        print(FAC[1],end=' ')
        FAC_score+=FAC[1]
        for z in range(2,len(FAC)):
            print(' + ',FAC[z],end=' ')
            FAC_score+=FAC[z]
    else:
        print(FAC[0],end=' ')
    print(' = ',FAC_score)
    

    SHP_score=SHP[0]
    print('SHP: ',end='')
    if len(SHP)>1:
        print(SHP[1],end=' ')
        SHP_score+=SHP[1]
        for z in range(2,len(SHP)):
            print(' + ',SHP[z],end=' ')
            SHP_score+=SHP[z]
    else:
        print(SHP[0],end=' ')
    print(' = ',SHP_score)
    

    HWY_score=HWY[0]
    print('HWY: ',end='')
    if len(HWY)>1:
        print(HWY[1],end=' ')
        HWY_score+=HWY[1]
        for z in range(2,len(HWY)):
            print(' + ',HWY[z],end=' ')
            HWY_score+=HWY[z]
    else:
        print(HWY[0],end=' ')
    print(' = ',HWY_score)
    

    BCH_score=BCH[0]
    print('BCH: ',end='')
    if len(BCH)>1:
        print(BCH[1],end=' ')
        BCH_score+=BCH[1]
        for z in range(2,len(BCH)):
            print(' + ',BCH[z],end=' ')
            BCH_score+=BCH[z]
    else:
        print(BCH[0],end=' ')
    print(' = ',BCH_score)
    

    total_score=HSE_score+FAC_score+SHP_score+HWY_score+BCH_score

    
    print('Total score: {}'.format(total_score))

##save game - lets users save their game
def save_game():
    #open file 
    path="C:\\Users\\Lenovo T14\\Desktop\\programming 1\\assignment\\"
    file=open(path+'save_game.csv','w')
    #row
    for x in range(num_of_row):
        #column
        for y in range(len(map[x])):
            #copy the column 
            if y+1<len(map[0]):
                file.write(map[x][y]+',') #put a comma so that the next element will be saved in the next box 
            else:
                file.write(map[x][y]) #last value dont need comma 
        file.write('\n')
    #count list 
    count_list=[['BCH',building_list.count('BCH')],['FAC',building_list.count('FAC')],['HSE',building_list.count('HSE')],\
                ['SHP',building_list.count('SHP')],['HWY',building_list.count('HWY')]]

    for x in range(len(count_list)):
        if x+1<len(count_list):
            file.write(str(count_list[x][1])+',')
        else:
            file.write(str(count_list[x][1]))
    file.write('\n')
    file.write(str(i))
    file.close()

            
    

##load game - allows users to load their saved game
def load_game():
    #open file 
    path="C:\\Users\\Lenovo T14\\Desktop\\programming 1\\assignment\\"
    file=open(path+'save_game.csv','r')
    read=file.readlines()
    num_of_row=len(map)

        
    for row in range(num_of_row):
        read_row=read[row]
        read_row=read_row.replace('\n','')
        row_split=read_row.split(',')
            
        for column in range(num_of_row-1):
            map[row][column]=row_split[column].replace(',','')
        
           
    remaining_buildings=read[num_of_row]
    remaining_buildings.replace('\n','')
    remaining_buildings_split=remaining_buildings.split(',')
    
    num=[]
    minus_list=[]
    #put this list again in case the user play game already then
    #go to main menu to load game
    global building_list
    building_list=['BCH','BCH','BCH','BCH','BCH','BCH','BCH','BCH',\
                   'FAC','FAC','FAC','FAC','FAC','FAC','FAC','FAC',\
                   'HSE','HSE','HSE','HSE','HSE','HSE','HSE','HSE',\
                   'SHP','SHP','SHP','SHP','SHP','SHP','SHP','SHP',\
                   'HWY','HWY','HWY','HWY','HWY','HWY','HWY','HWY']
    count_list=[['BCH',building_list.count('BCH')],['FAC',building_list.count('FAC')],['HSE',building_list.count('HSE')],\
                ['SHP',building_list.count('SHP')],['HWY',building_list.count('HWY')]]
    for x in range(len(count_list)):
        num==num.append(remaining_buildings_split[x])
        minus=8-int(num[x])
        minus_list==minus_list.append(minus)
    
    #so that can take away those buildings that are already removed
    for k in range(minus_list[0]):
        building_list.remove('BCH')
    for k in range(minus_list[1]):
        building_list.remove('FAC')
    for k in range(minus_list[2]):
        building_list.remove('HSE')
    for k in range(minus_list[3]):
        building_list.remove('SHP')
    for k in range(minus_list[4]):
        building_list.remove('HWY')
        
      
    count_list=[['BCH',building_list.count('BCH')],['FAC',building_list.count('FAC')],['HSE',building_list.count('HSE')],\
            ['SHP',building_list.count('SHP')],['HWY',building_list.count('HWY')]]
    
    global i
    i=int(read[5])
    file.close()
    return building_list, map

##save high scores - save the previous high scores
def save_highscore():
    try:    
        path="C:\\Users\\Lenovo T14\\Desktop\\programming 1\\assignment\\"
        file=open(path+'high_scores.csv','w')
        for x in range(len(score_list)):
            if x+1<len(score_list):
                file.write(str(score_list[x])+',')
            else:
                file.write(str(score_list[x]))
        file.write('\n')

        for x in range(len(name_list)):
            if x+1<len(name_list):
                file.write(name_list[x]+',')
            else:
                file.write(name_list[x])
    
        file.close()
    except:
        print('Error occurred. Please start a new game')
        mainmenuchoice=4
        

##load high scores - load the previous high scores
def load_highscore():
    
    path="C:\\Users\\Lenovo T14\\Desktop\\programming 1\\assignment\\"
    if os.path.isfile('high_scores.csv')==True:
        file=open(path+'high_scores.csv','r')
        read=file.readlines()
        read_name_list=read[1]
        read_name_list=read_name_list.replace('\n','')
        name_list_split=read_name_list.split(',')
        read_score_list=read[0]
        read_score_list=read_score_list.replace('\n','')
        score_list_split=read_score_list.split(',')
        
        
        for s in range(len(name_list_split)):
            
            name_list==name_list.append(name_list_split[s])
            score_list==score_list.append(int(score_list_split[s]))
        
        
        file.close()
        
    else:
        print('Play a full game first.')

##check high scores - check whether the user's score is eligible to be in the high score list
def check_highscore():
    global name_list
    global score_list
    name_list=[]
    score_list=[]
    pos_list=['1.','2.','3.','4.','5.','6.','7.','8.','9.','10.']
    path="C:\\Users\\Lenovo T14\\Desktop\\programming 1\\assignment\\"
    if os.path.isfile('high_scores.csv')==False: #create file 
        save_highscore()
        
    
    if os.stat(path+"high_scores.csv").st_size == 0: ##empty file
        name_list=[]
        score_list=[]
        print('Congratulations! You made the high score board at position 1!')
        name=input('Please enter your name (max 20 chars): ')
        name_list.append(name)
        score_list.append(total_score)
        
    else: ##file got things inside
       
        load_highscore()
        counts=0
        index=0
        index2=0
        for h in range(len(score_list)):
            if total_score<=score_list[h]: #see if total score is less than the score, if it is, take the index of the score 
                index=score_list.index(score_list[h]) 
                
               
            if index>0:    
                counts=score_list.count(score_list[index-1]) #see if got more than one of the same score for next value 
            else:
                counts=score_list.count(score_list[index]) #see if got more than one of the same score for the lower value 
        
        if index>0:
            index2=index-counts #to find the correct index where the score should be placed
            
        if counts>1:
            for k in range(len(score_list)):
                if score_list[k]==score_list[index]: #find the last index of that value 
                    index=k
        
        if index==(len(pos_list)-1) and len(name_list)==10: #cannot qualify to be in the high score list
            score_list==score_list.append(total_score) #append to the end to be popped later
            score_list=score_list.pop(len(score_list)-1)
        else: #can qualify to be in the high score list
            
            print('Congratulations! You made the high score board at position {}!'.format(pos_list[index+1]))
        
            name=input('Please enter your name (max 20 chars): ')
        
            if score_list[index]==total_score:
                name_list==name_list.insert(index+1,name)
                score_list==score_list.insert(index+1,total_score)
                
            elif index2==1 and total_score>score_list[0]: #top of the list 
                name_list==name_list.insert(0,name)
                score_list==score_list.insert(0,total_score)
                
            else:    
                name_list==name_list.insert(index+1,name)
                score_list==score_list.insert(index+1,total_score)
            if len(name_list)>10:
                score_list==score_list.pop(len(score_list)-1)
                name_list==name_list.pop(len(name_list)-1)
            
            

    save_highscore()
    return name_list,score_list
            

##high scores - shows users the high score
def highscore():
    print()
    print('{} {} {}'.format('-'*9,'HIGH SCORES','-'*9))
    print('{} {}{}{}'.format('Pos','Player',' '*16,'Score'))
    print('{} {}{}{}'.format('-'*len('pos'),'-'*len('player'),' '*16,'-'*len('score')))
    pos_list=['1.','2.','3.','4.','5.','6.','7.','8.','9.','10.']
    for x in range(len(name_list)):
        print('{} {}{}{:>8}'.format(pos_list[x],name_list[x],' '*(17-len(name_list[x])),score_list[x]))
        
####game####
##print title
title='Welcome, mayor of Simp City!'
print(title)
print('-'*len(title))

#main menu
main_menu()
mainmenu_choice()

#building dictionary
building_dict={'A':0,'B':1,'C':2,'D':3,\
               '1':0,'2':1,'3':2,'4':3}
#building list
building_list=['BCH','BCH','BCH','BCH','BCH','BCH','BCH','BCH',\
               'FAC','FAC','FAC','FAC','FAC','FAC','FAC','FAC',\
               'HSE','HSE','HSE','HSE','HSE','HSE','HSE','HSE',\
               'SHP','SHP','SHP','SHP','SHP','SHP','SHP','SHP',\
               'HWY','HWY','HWY','HWY','HWY','HWY','HWY','HWY']
#map 
map=[[' ',' ',' ',' '],\
     [' ',' ',' ',' '],\
     [' ',' ',' ',' '],\
     [' ',' ',' ',' ']]
i=1
if mainmenuchoice==2: #load game
    path="C:\\Users\\Lenovo T14\\Desktop\\programming 1\\assignment\\"
    if os.stat(path+'save_game.csv').st_size!=0 or os.path.isfile('save_game.csv')==False: #check if file is empty and exists anot 
        load_game()
        mainmenuchoice=1
    else:
        print('There is no previously saved file. Please choose another option.')
        mainmenuchoice=4
while i>0:
    if mainmenuchoice==4:
        print()
        main_menu()
        mainmenu_choice()
        if mainmenuchoice==1:
            i=1
        
    if mainmenuchoice==1:
        if i==1: #if you load game then exit then want to start new game 
            #building list
            building_list=['BCH','BCH','BCH','BCH','BCH','BCH','BCH','BCH',\
               'FAC','FAC','FAC','FAC','FAC','FAC','FAC','FAC',\
               'HSE','HSE','HSE','HSE','HSE','HSE','HSE','HSE',\
               'SHP','SHP','SHP','SHP','SHP','SHP','SHP','SHP',\
               'HWY','HWY','HWY','HWY','HWY','HWY','HWY','HWY']
            #map 
            map=[[' ',' ',' ',' '],\
                 [' ',' ',' ',' '],\
                 [' ',' ',' ',' '],\
                 [' ',' ',' ',' ']]
            
        #since there are only 16 turns so use while loop to continue looping the same thing
        while i<17:
            print()
            print('Turn {}'.format(i))
            #print out board
            board()
            #print out selection choices
            selection()
            #prompt user for selection choice
            selection_choice()
            #first building
            if selectionchoice==1:
                option=first
                #prompt user on where to build the building 
                build()
                #find whether isit valid to build there
                position(option)
                #next turn
                i+=1
            #second building
            elif selectionchoice==2:
                option=second
                #prompt user on where to build the building
                build()
                #find whether isit valid to build there
                position(option)
                #next turn
                i+=1
            #see remaining buildings 
            elif selectionchoice==3:
                #countlist
                count_list=[['BCH',building_list.count('BCH')],['FAC',building_list.count('FAC')],['HSE',building_list.count('HSE')],\
                            ['SHP',building_list.count('SHP')],['HWY',building_list.count('HWY')]]

                remaining_buildings()
            #see score
            elif selectionchoice==4:
                print()
                scoring()
            #save game
            elif selectionchoice==5:
                save_game()
                print('Game saved!')
            #exit to main menu
            elif selectionchoice==0:
                print()
                #so that the main menu can be printed out 
                mainmenuchoice=4
                break
        #print out the final layout of simp city 
        if i==17:
            print()
            print('Final layout of Simp City')
            board()
            scoring()
            check_highscore()
            highscore()
            mainmenuchoice=4
        else:
            continue
        
    #load game
    elif mainmenuchoice==2:
        path="C:\\Users\\Lenovo T14\\Desktop\\programming 1\\assignment\\"
        if os.stat(path+'save_game.csv').st_size!=0 or os.path.isfile('save_game.csv')==False: #check if file is empty or exists 
            load_game()
            mainmenuchoice=1
        else:
            print('There is no previously saved file. Please choose another option.')
            mainmenuchoice=4
        
    #show high scores
    elif mainmenuchoice==3:
        name_list=[]
        score_list=[]
        load_highscore()
        highscore()
        mainmenuchoice=4
        
    #exit game 
    elif mainmenuchoice==0:
        break

print('Thank you for playing this game!')
         
###end of game###











        
