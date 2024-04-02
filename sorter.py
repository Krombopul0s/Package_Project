import hashTable
from packData import distanceData
from packData import locationIndex

global packageReference
packageReference = hashTable.HashTable(41)
#---greedy-ish sort for packages. Includes a few filters to handle special instructions and calls truckSorter which actually sorts
# the packages that are on the trucks and then is used to add the remaining packages to trucks based on which truck would be closer---
def sortPackages(packageList, sorter_key=1): #1 = normal sort,  2 = resort

        #create 3 loads of packages (40 packages total divided by 16 package limit in truck)
        load1 = []
        load2 = []
        load3 = []

        #---dealing with special notes---

        #must be on truck 2
        for i in range(1, 41):
            #print(packageList.getItem(i).notes)
            if 'truck 2' in packageList.getItem(i).notes:
                load2.append(packageList.getItem(i))
                packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                packageList.delete(i)
            elif 'Wrong' in packageList.getItem(i).notes:
                load3.append(packageList.getItem(i))
                packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                packageList.delete(i)
        

        #must be delivered with something else
        for i in range(1, 41):
            if packageList.getItem(i) != None:
                #if this package has to be mated to another package
                if 'Must be delivered with' in packageList.getItem(i).notes:
                    mate1 = ''
                    mate2 = ''
                    s = packageList.getItem(i).notes.split(", ")
                    mate1 = int(s[-1])
                    mate2 = int(s[0].split()[-1])
                    checkList = []
                    #create a checklist of package ID's for boxes already loaded into truck 2
                    for item in load2:
                        checkList.append(item.packageID)
                    if packageList.getItem(i).packageID in checkList:
                        load2.append(packageList.getItem(i))
                        packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                        packageList.delete(i)
                    else:
                        load1.append(packageList.getItem(i))
                        if packageList.getItem(mate1) != None:
                            load1.append(packageList.getItem(mate1))
                            packageReference.add(packageList.getItem(mate1).packageID, packageList.getItem(mate1))
                        if packageList.getItem(mate2) != None:
                            load1.append(packageList.getItem(mate2))
                            packageReference.add(packageList.getItem(mate2).packageID, packageList.getItem(mate2))
                    packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                    packageList.delete(i)
                    packageList.delete(mate1)
                    packageList.delete(mate2)

        #sort out EOD and deadlines, split accross trucks
        for i in range(1, 41):
            if packageList.getItem(i) != None:
                #if package is delayed, add to load2
                if 'Delayed' in packageList.getItem(i).notes:
                    if ':' in packageList.getItem(i).deadline:
                        load2.append(packageList.getItem(i))
                        packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                        packageList.delete(i)
                    else:
                        load3.append(packageList.getItem(i))
                        packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                        packageList.delete(i)

                elif len(load1) < 9:
	                #if package has a deadline add it to load1 since it is leaving at 0800
                    if ':' in packageList.getItem(i).deadline:
                        load1.append(packageList.getItem(i))
                        packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                        packageList.delete(i)
                #add the rest of priority to load2 since it is leaving at 0905 when the late packages get in
                elif ':' in packageList.getItem(i).deadline:
                        load2.append(packageList.getItem(i))
                        packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                        packageList.delete(i)
        
        #sort what is in the trucks as of now to add the closest packages next
        global sortedLoad1
        sortedLoad1 = truckSorter(load1)
        global sortedLoad2
        sortedLoad2 = truckSorter(load2)
        
        for i in range(1, 41):
            #alternate searching trucks to see which one would be closer to current package
            if packageList.getItem(i) != None:
                loc1 = locationIndex.index(packageList.getItem(i).address)
                loc2 = locationIndex.index(sortedLoad1[-1].address)
                loc3 = locationIndex.index(sortedLoad2[-1].address)

                if getDistance(loc2, loc1) < getDistance(loc3, loc1):
                    packageList.getItem(i).distanceToBox = getDistance(loc2, loc1)
                    if len(sortedLoad1) < 16:
                        sortedLoad1.append(packageList.getItem(i))
                    elif len(sortedLoad2) < 16:
                        sortedLoad2.append(packageList.getItem(i))
                    else:
                        load3.append(packageList.getItem(i))
                    packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                    packageList.delete(i)
                elif getDistance(loc3, loc1) < getDistance(loc2, loc1):
                    packageList.getItem(i).distanceToBox = getDistance(loc3, loc1)
                    if len(sortedLoad1) < 16:
                        sortedLoad2.append(packageList.getItem(i))
                    elif len(sortedLoad2) < 16:
                        sortedLoad1.append(packageList.getItem(i))
                    else:
                        load3.append(packageList.getItem(i))
                    packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                    packageList.delete(i)

        #once they're full, load onto truck 3
        for i in range(1, 41):
            if packageList.getItem(i) != None:
                    load3.append(packageList.getItem(i))
                    packageReference.add(packageList.getItem(i).packageID, packageList.getItem(i))
                    
        #sorts load 3 after everything leftover has been added to it.
        global sortedLoad3
        sortedLoad3 = truckSorter(load3)
        sortedLoad1 = truckSorter(sortedLoad1)
        sortedLoad2 = truckSorter(sortedLoad2)
        
        '''----- Testing for package list on each truck and mileage -----
        totalDist = 0
        for box in sortedLoad1:
            print(box.packageID, box.deadline, box.notes, box.distanceToBox)
            totalDist += float(box.distanceToBox)
        print()
        print(totalDist)
        totalDist = 0
        for box in sortedLoad2:
            print(box.packageID, box.deadline, box.notes, box.distanceToBox)
            totalDist += float(box.distanceToBox)
        print()
        print(totalDist)
        totalDist = 0
        
        for box in sortedLoad3:
            print(box.packageID, box.deadline, box.notes, box.distanceToBox)
            totalDist += float(box.distanceToBox)
        print()
        print(totalDist)
        '''

        '''----- Testing for mated packages and requirements -----
        for box in load1:
            print(box.packageID)
            print(box.notes)
        print()
        for box in load2:
            print(box.packageID)
            print(box.notes)
        print()
        for box in load3:
            print(box.packageID)
            print(box.notes)
        #print(load2)
        #print(load1)
        '''

#set hub as start location, as boxes are iterated through, prioritize deadlines, then distance
def truckSorter(load):
    startLocation = 0 #index of the hubs location in the data
    sortedLoad = []
    priority = []
    standard = []
    min = 1000
    #split load into standard and priority delivery
    for box in load:
        if ':' in box.deadline:
            priority.append(box)
        else:
            standard.append(box)
    #sort priority by distance using a greedy algorithm
    while len(priority) !=0:
        min = 1000
        nextBox = None
        #for each box still in load
        for box in priority:
            #next stop is this box and call getDistance from previous box to this one
            nextStop = locationIndex.index(box.address)
            distance = float(getDistance(startLocation, nextStop))
            if distance <= min:
                min = distance
                nextBox = box
        #once all boxes have been gone through, add the next closest box, set variables for next round, and remove this one from the list
        startLocation = locationIndex.index(nextBox.address)
        packageReference.getItem(nextBox.packageID).distanceToBox = min
        sortedLoad.append(nextBox)
        priority.remove(nextBox)
    #sort the rest into the sorter
    while len(standard) !=0:
        min = 1000
        nextBox = None
        #for each box still in load
        for box in standard:
            if len(standard) == 1:
                nextBox = box
            #next stop is this box and call getDistance from previous box to this one
            nextStop = locationIndex.index(box.address)
            distance = float(getDistance(startLocation, nextStop))
            if distance <= min:
                min = distance
                nextBox = box
        #once all boxes have been gone through, add the next closest box, set variables for next round, and remove this one from the list
        startLocation = locationIndex.index(nextBox.address)
        packageReference.getItem(nextBox.packageID).distanceToBox = min
        sortedLoad.append(nextBox)
        standard.remove(nextBox)
    return sortedLoad


#takes the index values from distanceData given to it
def getDistance(loc1, loc2):
        distance = distanceData.getItem(loc1)[loc2]
        if distance == '':
            distance = distanceData.getItem(loc2)[loc1]
        return distance

