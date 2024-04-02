import csv
import hashTable

'''
cleaned package data and distance table to remove unneccessary spaces, commas, etc. "na" added to packages with no applicable notes
Please use the included csv files as there was no built-in cleaning features added.
'''

#create data structure (hash table?) for everything in and define package and truck objects
class Package:
    def __init__(self, packageID, address, city, zipcode, deadline, notes, deliveryStatus, deliveryTime, distanceToBox, truckNum,weight):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.notes = notes
        self.status = deliveryStatus
        self.deliveryTime = deliveryTime
        self.distanceToBox = distanceToBox
        self.truckNum = truckNum
        self.weight = weight

#reads in data for packages 
with open("Cleaned_Package_Data.csv", "r") as csvfile:
    global packages
    packages = hashTable.HashTable(50)
    reader = csv.reader(csvfile)
    count = 0
    #getting rid of first row since I cannot use dictreader to separate package values
    for row in reader:
        if count == 0:
            count += 1
        else:
            #use data to create package object
            newPack = Package(int(row[0]), row[1], row[2] + ' ' + row[3], row[4], row[5], row[6], 'awaiting sort', 'not yet delivered', 0.0, 0, row[7])
            #add object to hashtable
            packages.add(newPack.packageID, newPack)

'''-----Tests package upload, insertion into hashtable, and individual package modification-----
print(packages.getList())
print(packages.getItem(37))
currPackage = packages.getItem(37)
currPackage.status = 'Out for Delivery'
print(currPackage.status)
'''

#reads in distance data and adds to array only the relevant dstance values from table
with open("Cleaned_Distance_Data.csv", "r") as csvfile:
    global distanceData
    locationIndex = []
    distanceData = hashTable.HashTable(25)
    reader = csv.reader(csvfile)
    count = 0
    for row in reader:
        if count == 0:
            for item in row:
                address = item.split(", ")
                locationIndex.append(address[1])
                count += 1
        else:
            address = row[0].split(", ")[1]
            index = locationIndex.index(address)
            distanceData.add(index, row[1:])

''' -----Tests loading distance data and accessing mileage associated with that location -----
print(locationIndex)
print(distanceData.getList())
indexLocation = int(locationIndex.index('3060 Lester St'))
print(indexLocation)
print(distanceData.getItem(indexLocation))
'''
