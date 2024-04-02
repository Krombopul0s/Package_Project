import packData
import hashTable
import sorter
import trucks
import datetime
from datetime import datetime
from packData import packages
from sorter import packageReference

#create trucks
global truck1, truck2, truck3
truck1 = trucks.Truck(1)
truck2 = trucks.Truck(2)
truck3 = trucks.Truck(3)
    
#sort packages
sorter.sortPackages(packages)

from sorter import sortedLoad1, sortedLoad2, sortedLoad3

#add sorted packages to trucks
truck1Load = sortedLoad1
truck2Load = sortedLoad2
truck3Load = sortedLoad3

#deliver packages
truck1.deliverPackages(truck1Load, 8, 0)
truck2.deliverPackages(truck2Load, 9, 5)
truck3.deliverPackages(truck3Load, 12, 0)

#sets up menu options table and defines options
menuOptions = hashTable.HashTable(7)

menuOptions.add(1, 'Print Full Report ------------- 1')
menuOptions.add(2, 'Get Info for package(s) ------- 2')
menuOptions.add(3, 'Update package data ----------- 3')
menuOptions.add(4, 'Exit -------------------------- 4')

global trucksSorted
trucksSorted = False
#displays menu until exited.
def displayMenu():
    print()
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for i in range(1, 5):
        print(menuOptions.getItem(i))
    print()
    print('Note: If you are having difficulies with system, please run program again and select option 4 before trying again.')
    print('Thank you.')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    
def reportTrucks():

    #prints out report of all packages and mileage for each truck
    for i in range(1,41):
        package = packageReference.getItem(i)
        print('Package #: ' + str(package.packageID) + ' ' + package.address + ' ' + package.status + ' at ' + str(package.deliveryTime) + ' by Truck ' + str(package.truckNum) + '. Deadline was: ' + package.deadline)

    print()
    print('Total miles for each truck: ')
    print('Truck 1: ' + ' ' + str(int(truck1.mileage)))
    print('Truck 2: ' + ' ' + str(int(truck2.mileage)))
    print('Truck 3: ' + ' ' + str(int(truck3.mileage)))
    print('Total: ' + str(int(truck1.mileage) + int(truck2.mileage) + int(truck3.mileage)))

def packageStatus():
    print('You may search for a single package and get delivery status as of desired time or all package statuses within a time frame.')
    prompt = int(input('Are you looking for one, or multiple packages? (Please enter 1 for 1 package or 2 for multiple): '))
    #searching for one package at a certain time, returns delivery status
    if prompt == 1:
        id = int(input('Please input the package ID you are looking for: '))
        startTime = datetime.strptime(str(input('Please enter the time (24 hour clock HH:MM): ')), '%H:%M')
        print()
        box = packageReference.getItem(id)
        time = box.deliveryTime
        t1Start = datetime.strptime(str('08:00'), '%H:%M')
        t2Start = datetime.strptime(str('09:05'), '%H:%M')
        t3Start = datetime.strptime(str('12:00'), '%H:%M')
        tenTwenty = datetime.strptime(str('10:20'), '%H:%M')
        if startTime.time() < time:
            if box.truckNum == 1 and startTime.time() < t1Start.time():
                print('Package ID: ' + str(box.packageID) + ' ' + box.address + ' ' + box.city + ' ' + box.zipcode + ' ' + box.weight + 'kg Delivery Dealine: ' + box.deadline)
                print('\n Package at Hub. Awaiting departure.')
            elif box.packageID == 9:
                if startTime.time() < tenTwenty.time():
                    print('Package ID: ' + str(box.packageID) + ' 300 State St, ' + box.city + ' ' + box.zipcode + ' '  + box.weight + 'kg Delivery Dealine: ' + box.deadline)
                    print('\n Package at Hub. Awaiting departure.')
                elif startTime.time() > tenTwenty.time() and startTime.time() < t3Start.time():
                    print('Package ID: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.zipcode + ' ' + box.weight + 'kg Delivery Dealine: ' + box.deadline)
                    print('\n Package at Hub. Awaiting departure.')
                else:
                    print('Package ID: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ', ' + box.zipcode +  ' ' +box.weight + 'kg Delivery Dealine: ' + box.deadline)
                    print('\nPackage is out for delivery! \n')
            elif box.truckNum == 2 and startTime.time() < t2Start.time():
                print('Package ID: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ', ' + box.zipcode + ' ' + box.weight + 'kg Delivery Dealine: ' + box.deadline)
                print('\n Package at Hub. Awaiting departure.')
            elif box.truckNum == 3 and startTime.time() < t3Start.time():
                print('Package ID: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ', ' + box.zipcode +  ' ' +box.weight + 'kg Delivery Dealine: ' + box.deadline)
                print('\n Package at Hub. Awaiting departure.')
            else:
                print('Package ID: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ', ' + box.zipcode +  ' ' +box.weight + 'kg Delivery Dealine: ' + box.deadline)
                print('\n Package is out for delivery! \n')
        else:
            print('Package ID: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ', ' + box.zipcode +  ' ' +box.weight + 'kg Delivery Dealine: ' + box.deadline)
            print('\nPackage was delivered at: \n' + time.strftime('%H:%M:%S'))

    #searching for a window of time and returning all packages by truck
    if prompt == 2:
        trucks = [truck1, truck2, truck3]
        t1Start = datetime.strptime(str('08:00'), '%H:%M')
        t2Start = datetime.strptime(str('09:05'), '%H:%M')
        t3Start = datetime.strptime(str('11:00'), '%H:%M')
        startTimeFrame = datetime.strptime(str(input('Please enter the start time (24 hour clock HH:MM): ')), '%H:%M')
        endTimeFrame = datetime.strptime(str(input('Please enter the end time (24 hour clock HH:MM): ')), '%H:%M')
        tenTwenty = datetime.strptime(str('10:20'), '%H:%M')
        for truck in trucks:
            if truck.truckNum == 1:
                truckStart = t1Start
            elif truck.truckNum ==2:
                truckStart = t2Start
            else:
                truckStart = t3Start
            print()
            print('Truck ' + str(truck.truckNum) + ':')
            for box in truck.manifest:
                time = box.deliveryTime
                #if the delivery time is prior to start time print delivered
                if box.packageID == 9:
                    if endTimeFrame.time() < tenTwenty.time():
                        box.address = '300 State St'
                    if time < startTimeFrame.time():
                        print('Package #: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + box.status + ' at ' + str(box.deliveryTime) + ' by Truck ' + str(box.truckNum) + '. Deadline was: ' + box.deadline)
                    elif time < endTimeFrame.time() and time > startTimeFrame.time():
                        print('Package #: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + 'expected to be delivered within given timeframe by Truck '  + str(box.truckNum) + '. Deadline is: ' + box.deadline)
                    elif time > endTimeFrame.time() and startTimeFrame.time() < truckStart.time():
                        print('Package # :' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + 'at Hub. Awaiting departure. Expected to be delivered by Truck '  + str(box.truckNum) + '. Deadline is: ' + box.deadline)
                    else: 
                        print('Package #: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + ' is out for delivery on Truck ' + str(box.truckNum) + '. Expected later than given time frame.')
                    box.address = '410 S State St'
                #if the delivery time is prior to start time print delivered
                elif time < startTimeFrame.time():
                    print('Package #: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + box.status + ' at ' + str(box.deliveryTime) + ' by Truck ' + str(box.truckNum) + '. Deadline was: ' + box.deadline)
                elif time < endTimeFrame.time() and time > startTimeFrame.time():
                    print('Package #: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + 'expected to be delivered within given timeframe by Truck '  + str(box.truckNum) + '. Deadline is: ' + box.deadline)
                elif time > endTimeFrame.time() and startTimeFrame.time() < truckStart.time():
                    print('Package # :' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + 'at Hub. Awaiting departure. Expected to be delivered by Truck '  + str(box.truckNum) + '. Deadline is: ' + box.deadline)
                else: 
                    print('Package #: ' + str(box.packageID) + ' ' + box.address + ', ' + box.city + ' ' + box.weight + ' kg ' + ' is out for delivery on Truck ' + str(box.truckNum) + '. Expected later than given time frame.')
        

def updatePackage():
    #updates address if possible and resorts truck. 
    print('Warning, you can only update a delivery address prior to it being delivered.')
    id = int(input('Please provide package ID from tracking information: '))
    updateAddress = str(input('Please provide the updated address: (i.e. 410 S State St) '))
    currTime = datetime.strptime(str(input('Please enter current time (HH:MM): ')), '%H:%M')
    box = packageReference.getItem(id)
    if box.deliveryTime < currTime.time():
        print('Unfortunately, the package was delivered to the address on file. Please file ticket with WGUPS.')
        exit()
    else:
        #update address for package ID in truck manifest, resort truck, and deliver what hasn't been delivered yet.
        truckList = [truck1, truck2, truck3]
        modBoxList = []
        resortTruck = trucks.Truck(4)
        for truck in truckList:
            for box in truck.manifest:
                if box.packageID == id:
                    print('found')
                    box.address = updateAddress
                    resortTruck.truckNum = int(truck.truckNum)
                    resortTruck.manifest = truck.manifest
                    print('Updating packge information and resorting truck for delivery.')
                    print()
        startTime = datetime.strptime(str('00:00'), '%H:%M')
        for box in resortTruck.manifest:
            if 'delivered' in box.status:
                modBoxList.append(box)
                startTime = datetime.strptime(box.deliveryTime, '%H:%M:%S')
            else:
                if resortTruck.truckNum == 1:
                    startTime = datetime.strptime(str('08:00'), '%H:%M')
                elif resortTruck.truckNum == 2:
                    startTime = datetime.strptime(str('09:05'), '%H:%M')
                else:
                    startTime = datetime.strptime(str('12:00'), '%H:%M')
        newLoad = sorter.truckSorter(resortTruck.manifest)
        resortTruck.deliverPackages(newLoad, startTime.hour, startTime.minute)

        for i in range(1,41):
            package = packageReference.getItem(i)
            print('Package #: ' + str(package.packageID) + ' ' + package.address + ' ' + package.status + ' at ' + str(package.deliveryTime) + ' by Truck ' + str(package.truckNum) + '. Deadline was: ' + package.deadline)

        print()
        print('Miles after resorted truck: ')
        totalMiles = 0
        for truck in truckList:
            if resortTruck.truckNum == truck.truckNum:
                print('Truck ' + str(truck.truckNum)  + ' resorted. Mileage is now: ' + str(int(resortTruck.mileage)))
                totalMiles += resortTruck.mileage
            else:
                print('Truck ' + str(truck.truckNum)  + ': ' + str(int(truck.mileage)))
                totalMiles += truck.mileage
        print()
        print('Total: ' + str(int(totalMiles)))
        

#displays menu until you exit.
if __name__=='__main__':
    reportTrucks()
    while(True):
        displayMenu()
        option = ''
        try:
            option = int(input('Enter option number: '))
        except:
            print('Hmmm, I\'m having trouble finding that option, please try another or check your input ...')
        match option:
            case 1:
                try:
                    print('\n' + 'Loading both trucks . . . . .')
                    trucksSorted = True
                    reportTrucks()
                except:
                    print('There seems to have been an error. Please try running the program again and exiting using option 4.')
                    exit()
            case 2:
                try:
                    packageStatus()
                except:
                   exit()
            case 3:
                try:
                    updatePackage()
                except:
                    exit()
            case 4:
                print('Thank you for choosing WGUPS for your delivery needs!')
                print()
                exit()
            case default:
                print('Please choose from the options below: ')

