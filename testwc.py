#!/bin/python

# Approximates the ratio between camp trips and warehouse trips for woodcutters in royal woodlands.
# Adjust the numbers for other biomes and citadel progress.
import random;

class woodcutter:
    epsilon=1e-9
    prod={"wood":1, "fiber":1, "egg": 1, "resin": 1}
    chance={"wood":[1,1], "fiber":[0.1], "egg":[0.05], "resin":[0.15]}
    storage={"wood":0, "fiber":0, "egg": 0, "resin":0, "total":0}
    storageCap=10
    carryCap=5
    warehouseTrips=0
    campTrips=0

    def store(self, resources):
       for key,value in resources.items():
           self.storage[key] = self.storage[key] + value;

    def cut(self):
        self.campTrips = self.campTrips + 1;
        for key,value in self.chance.items():
            for p in value:
                if(p > 1 - self.epsilon or random.random() < p):
                    self.storage[key] = self.storage[key] + self.prod[key]
                    self.storage["total"] = self.storage["total"] + self.prod[key]

    def emptyCamp(self):
        for key,value in self.storage.items():
            if(value > 0):
                self.emptyCampResource(key);

    def emptyCampResource(self, key):
        while(self.storage[key]>0):
            self.storage["total"] = self.storage["total"] - min(self.storage[key], self.carryCap)
            self.storage[key] = self.storage[key] - min(self.storage[key], self.carryCap)
            self.warehouseTrips = self.warehouseTrips + 1

    def isFull(self):
        return self.storage["total"] >= self.storageCap

    def run(self):
        random.seed(5225)
        while(self.warehouseTrips < 1000000):
            self.cut()
            if(self.isFull()):
                self.emptyCamp()
                self.cut()
                self.emptyCamp()
                self.cut()
                self.emptyCamp()

    def run2(self):
        random.seed(5225)
        while(self.warehouseTrips < 1000000):
            self.cut()
            if(self.isFull()):
                self.emptyCamp()

wc = woodcutter()
wc.run()
print("Low estimate:")
print("Warehouse Trips: {}".format(wc.warehouseTrips) )
print("Camp trips: {}".format(wc.campTrips))
wc2 = woodcutter()
wc2.run2()
print("High estimate:")
print("Warehouse Trips: {}".format(wc2.warehouseTrips) )
print("Camp trips: {}".format(wc2.campTrips))
