# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 23:51:24 2022

@author: Sachin G
"""
import numpy as np
import matplotlib.pyplot as plt


span = int(input(f"Enter the length of the simply supported beam in m: "))


loadSet = []  # list of lists containing the load case type, magnitude of the load and location of the load

loadCases = int(input("Enter the total number of external load cases acting on the beam: "))
print("\n")

print("Enter 'CF' for point loads, 'UDL' for uniformly distributed loads, 'UVL' for uniformly varying loads.")

for i in range(loadCases):
    loadCaseType = str(input("Enter the type for load case " + str(i+1) +": "))
    if loadCaseType == 'CF':
        magnitude = float(input("Enter the magnitude of the concentrated force in N (+ve force upwards, -ve downwards): "))
        pointOfAction = float(input("Enter the horizontal distance in m of the force from the left end of the beam: "))
        loadSet.append([loadCaseType, magnitude, pointOfAction])
    elif loadCaseType == 'UDL':
        magnitude = float(input("Enter the magnitude of the uniformly distributed load in N/m (+ve distribution upwards, -ve downwards): "))
        udlStart = float(input("Enter the horizontal distance in m to the start of UDL from the left end of the beam: "))
        udlEnd = float(input("Enter the horizontal distance in m to the end of UDL from the left end of the beam: "))
        loadSet.append([loadCaseType, magnitude, udlStart, udlEnd])
    elif loadCaseType == 'UVL':
        magnitude = float(input("Enter the magnitude of the uniformly varying load in N/m (+ve distribution upwards, -ve downwards): "))
        uvlStart = float(input("Enter the horizontal distance in m to the start of UVL from the left end of the beam: "))
        uvlEnd = float(input("Enter the horizontal distance in m to the end of UVL from the left end of the beam: "))
        loadSet.append([loadCaseType, magnitude, uvlStart, uvlEnd])
   
    else:
        print("Enter the correct symbols for the desired load cases as mentioned above")
        
# Statics - calculate reactions forces at supports using input data
# Considers equilibrium of moments with respect to left support
sumOfForces = 0
sumOfMoments = 0
for e in loadSet:
    if e[0] == 'UDL':
        sumOfForces += (e[1] * (e[3] - e[2]))
        sumOfMoments += (e[1] * (e[3] - e[2]) * (e[2] + e[3])/2)
        
    elif e[0] == 'CF':
        sumOfForces += (e[1])
        sumOfMoments += (e[1] * e[2])
    
    elif e[0] == 'UVL':
        uvLoad = 0.5 * (e[1] * (e[3] - e[2]))
        sumOfForces += uvLoad
        sumOfMoments += uvLoad * (e[2] + ((2/3) * (e[3] - e[2])))

rightReaction = -1 * (sumOfMoments/span) # summation of Moments = 0
leftReaction = -1 * (sumOfForces + rightReaction) # summation of vertical forces = 0
loadSet.insert(0, ['R', round(leftReaction,2), 0])
loadSet.append(['R', round(rightReaction,2), span])

print(loadSet)

# Shear forces calculation
sumOfForces = np.zeros(1000)
shearForcesList = []
spanValuesList = []

# Shear Force calculation
for i in range(len(loadSet)-1):
    if loadSet[i][0] == 'R':
        x = np.linspace(loadSet[i][2], loadSet[i+1][2], 1000, endpoint=True)
        sumOfForces += loadSet[i][1]
        shearForcesList.extend(sumOfForces)
        spanValuesList.extend(x)
        
    elif loadSet[i][0] == 'CF':
        x = np.linspace(loadSet[i][2], loadSet[i+1][2], 1000, endpoint=True)
        sumOfForces += loadSet[i][1]
        shearForcesList.extend(sumOfForces)
        spanValuesList.extend(x)
        
    elif loadSet[i][0] == 'UDL':
        # this section computes shear force distribution in the span of the UDL
        x = np.linspace(loadSet[i][2], loadSet[i][3], 1000, endpoint=True)
        base = x - loadSet[i][2]
        udLoad = loadSet[i][1] * base
        sumOfForces += udLoad
        shearForcesList.extend(sumOfForces)
        spanValuesList.extend(x)
        
        # this section computes shear force distribution from end of UDL to start of next load case
        x1 = np.linspace(loadSet[i][3], loadSet[i+1][2], 1000, endpoint=True)
        sumOfForces = sumOfForces[-1]*np.ones(1000)
        shearForcesList.extend(sumOfForces)
        spanValuesList.extend(x1)
    
    elif loadSet[i][0] == 'UVL':
        # this section computes shear force distribution in the span of the UVL
        x = np.linspace(loadSet[i][2], loadSet[i][3], 1000, endpoint=True)       
        base = x - loadSet[i][2]
        uvlSpan = loadSet[i][3] - loadSet[i][2]
        height = (base / uvlSpan) * loadSet[i][1]
        uvLoad = 0.5 * base * height
        sumOfForces += uvLoad
        shearForcesList.extend(sumOfForces)
        spanValuesList.extend(x)
        
        # this section computes shear force distribution from end of UVL to start of next load case
        x1 = np.linspace(loadSet[i][3], loadSet[i+1][2], 1000, endpoint=True)
        sumOfForces = sumOfForces[-1] * np.ones(1000)
        shearForcesList.extend(sumOfForces)
        spanValuesList.extend(x1)
        
# Plotting shear force vs beam span
plt.figure(figsize=(10,6))
plt.plot(spanValuesList, shearForcesList, 'r', lw=3,  linestyle='-')
plt.fill_between(spanValuesList, y1=0, y2=shearForcesList, color='r', alpha=0.25)
plt.xlabel("Span (m)", fontsize=15, fontweight="bold")
plt.ylabel("Shear force (N)", fontsize=20, fontweight="bold")
plt.title("Shear force diagram", fontsize=20, fontweight="bold")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.axis([loadSet[0][-1], loadSet[-1][-1], min(shearForcesList)-5e3, max(shearForcesList)+5e3])
plt.show()

# Bending moments calculation
bendingMomentsList = []
xValues = [] # plays the same role as spanValuesList before, just using a different name.

for i in range(len(loadSet)-1):
    if loadSet[i][0] == 'R':
        x = np.linspace(loadSet[i][2], loadSet[i+1][2], 1000, endpoint=True)
        xValues.extend(x)
        sumOfMoments = np.zeros(1000)
        for j in range(i+1):              
            sumOfMoments += loadSet[j][1]*(x-loadSet[j][2])
            
        bendingMomentsList.extend(sumOfMoments)
             
    elif loadSet[i][0] == 'CF':
        x = np.linspace(loadSet[i][2], loadSet[i+1][2], 1000, endpoint=True)
        xValues.extend(x)
        sumOfMoments = np.zeros(1000)
        for j in range(i+1):
            if(loadSet[j][0] == 'UDL'):
                load = loadSet[j][1]*(loadSet[j][3] - loadSet[j][2])
                pointOfAction = (loadSet[j][2] + loadSet[j][3])/2
                sumOfMoments = sumOfMoments + (load * (x - pointOfAction))
            else:
                sumOfMoments = sumOfMoments + (loadSet[j][1]*(x-loadSet[j][2]))
                        
        bendingMomentsList.extend(sumOfMoments)
           
    elif loadSet[i][0] == 'UDL':
        x = np.linspace(loadSet[i][2], loadSet[i][3], 1000, endpoint=True)
        xValues.extend(x)
        sumOfMoments = np.zeros(1000)
        for j in range(i):
            if(loadSet[j][0] == 'UDL'):
                load = loadSet[j][1]*(loadSet[j][3] - loadSet[j][2])
                pointOfAction = (loadSet[j][2] + loadSet[j][3])/2
                sumOfMoments = sumOfMoments + (load * (x - pointOfAction))
            else:
                sumOfMoments += loadSet[j][1]*(x-loadSet[j][2])
        
        udLoad = loadSet[i][1]*(x-loadSet[i][2])
        sumOfMoments = sumOfMoments + (udLoad*(x-((x + loadSet[i][2])/2)))
        
        bendingMomentsList.extend(sumOfMoments)
        
        x1 = np.linspace(loadSet[i][3], loadSet[i+1][2], 1000, endpoint=True)
        xValues.extend(x1)
        sumOfMoments = np.zeros(1000)
        for j in range(i+1): 
            if(loadSet[j][0] == 'UDL'):
                load = loadSet[j][1] * (loadSet[j][3] - loadSet[j][2])
                pointOfAction = (loadSet[j][2] + loadSet[j][3])/2
                sumOfMoments = sumOfMoments + (load * (x1 - pointOfAction))
            else:
                sumOfMoments = sumOfMoments + (loadSet[j][1]*(x1-loadSet[j][2]))
    
        bendingMomentsList.extend(sumOfMoments)
    
    elif loadSet[i][0] == 'UVL':
        x = np.linspace(loadSet[i][2], loadSet[i][3], 1000, endpoint=True)
        xValues.extend(x)
        sumOfMoments = np.zeros(1000)
        for j in range(i):
            if(loadSet[j][0] == 'UVL'):
                load = 0.5 * loadSet[j][1] * (loadSet[j][3] - loadSet[j][2])
                momentArm = (2/3) * (loadSet[j][3] - loadSet[j][2])
                pointOfAction = x - (loadSet[j][2] + momentArm)
                sumOfMoments = sumOfMoments + (load * pointOfAction)
            else:
                sumOfMoments += loadSet[j][1]*(x-loadSet[j][2])
                
        baseOfLoad = x - loadSet[i][2]
        heightOfLoad = ( (x - loadSet[i][2]) / (loadSet[i][3] - loadSet[i][2]) ) * loadSet[i][1]
        uvLoad = 0.5 * baseOfLoad * heightOfLoad
        momentArm = x - (loadSet[i][2] + ((2/3) * (loadSet[i][3] - loadSet[i][2])))
        sumOfMoments = sumOfMoments + (uvLoad * momentArm)
        
        bendingMomentsList.extend(sumOfMoments)
        
        x1 = np.linspace(loadSet[i][3], loadSet[i+1][2], 1000, endpoint=True)
        xValues.extend(x1)
        sumOfMoments = np.zeros(1000)
        for j in range(i+1):
            if(loadSet[j][0] == 'UVL'):
                load = 0.5 * loadSet[j][1] * (loadSet[j][3] - loadSet[j][2])
                momentArm = (2/3) * (loadSet[j][3] - loadSet[j][2])
                pointOfAction = x1 - (loadSet[j][2] + momentArm)
                sumOfMoments = sumOfMoments + (load * pointOfAction)
            else:
                sumOfMoments += loadSet[j][1]*(x1-loadSet[j][2])
            
        bendingMomentsList.extend(sumOfMoments)
         

formattedBendingMomentsList = [round(elem, 4) for elem in bendingMomentsList] # list comprehension

# Plotting bending moment vs beam span
plt.figure(figsize=(10,6))
plt.plot(xValues, formattedBendingMomentsList, 'g', lw=3, linestyle='-')
plt.fill_between(xValues, y1=0, y2=formattedBendingMomentsList, color='g', alpha=0.25)
plt.xlabel("Span (m)", fontsize=15, fontweight="bold")
plt.ylabel("Bending moment (N-m)", fontsize=20, fontweight="bold")
plt.title("Bending moment diagram", fontsize=20, fontweight="bold")
plt.axis([loadSet[0][-1],loadSet[-1][-1],0,max(formattedBendingMomentsList)+5e3])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()

absShearForcesList = [abs(ele) for ele in shearForcesList]
print("Reaction at left support = " + str(leftReaction) + " N")
print("Reaction at right support = " + str(rightReaction) + " N")
print("Max shear force = " + str(max(absShearForcesList)) + ' N' + '\n' +
"Max bending moment = " + str(max(formattedBendingMomentsList)) + ' N-m')


    