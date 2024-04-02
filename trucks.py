import hashTable
import datetime
from packData import distanceData
from sorter import packageReference

#creates truck object that contains a hashTable for it's manifest
class Truck:

    def __init__(self, truckNum, time=900):
        self.truckNum = truckNum
        self.manifest = []
        self.mileage = 0.0
        
    #"delivers" package, increments time and mileage to simulate duration and distance of route --- use commented prints to see truck package lists
    def deliverPackages(self, load, hour, minute):
        time = datetime.datetime(2023, 11, 27, hour=hour, minute=minute)
        #print('Truck Number: ' + str(self.truckNum))
        #for each package in manifest
        for box in load:
            distance = box.distanceToBox
            self.mileage += float(distance)
            travelTime = float(distance)/(18/60)
            deliveryTime = datetime.timedelta(minutes = travelTime)
            time += deliveryTime
            referenceBox = packageReference.getItem(box.packageID)
            referenceBox.status = 'Delivered'
            referenceBox.deliveryTime = time.time()
            referenceBox.truckNum = self.truckNum
            self.manifest.append(referenceBox)
            #print(referenceBox.packageID)

        return
    
    
        
    