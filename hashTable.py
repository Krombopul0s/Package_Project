import csv

#Creates Hashtable structure
class HashTable:
    def __init__(self, initial_capacity):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
      
    #Inserts/adds item in hashTable.
    def add(self, key, item):
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        #If it exists, this updates item
        for pair in index_list:
          #print (key_value)
          if pair[0] == key:
            pair[1] = item
            return True
        
        #If not, this adds to the end of the list.
        key_value = [key, item]
        index_list.append(key_value)
        return True
 
    #Gets/Searches for item object based on key, returns none if not found
    def getItem(self, key):
        # get the list item where this key would be.
        index = hash(key) % len(self.table)
        index_list = self.table[index]
        #print(index_list) 
 
        # search for the key in the list
        for pair in index_list:
          #print the kv pair
          if pair[0] == key:
            return pair[1]
        #return None
 
    #Deletes item if it is in the Hash Table.
    def delete(self, key):
        # get the list item where this item is
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        # remove the item from from the list
        for pair in index_list:
          #print kv pair
          if pair[0] == key:
              index_list.remove([pair[0],pair[1]])

    #Prints entire list of items currently loaded into Hastable
    def getList(self):
        index_list = self.table
        return index_list
        #print(index_list)

    def getInfo(self, key):
        return


''' -----Teasting Hastable----- 
packages = HashTable()
packages.add(3, 'package')
packages.add(5, 'package')
packages.add(7, 'package')
packages.add(5, 'package2')
print(packages.getList())
packages.delete(3)
print(packages.getList())
'''