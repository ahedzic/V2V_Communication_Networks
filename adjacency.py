'''
Generates an adjacency matrix from a netstate_dump.xml, which was the output from a simulation run.
The logic is that vehicles on the same road in same direction can be adjacent to each other within a 
distance threshold.
'''

import xml.etree.ElementTree as ET
import numpy as np

tree = ET.parse('netstate_dump.xml')
root = tree.getroot()

NUM_VEHICLES = 99
NUM_TIMESTEPS = 681
THRES = 10. # threshold in meters to determine adjacency

adj = np.zeros(shape=(NUM_TIMESTEPS, NUM_VEHICLES, NUM_VEHICLES), dtype=np.int8) # first dim is channel

for timestep in root:
    t = int(float(timestep.attrib['time']))
    for edge in timestep: # road
        vehicles = [] # list of xml vehicle nodes
        for lane in edge: # ignore lanes and collate vehicles
            for vehicle in lane:
                vehicles.append(vehicle)
        if len(vehicles) > 1: # do n^2 check of position
            for i in range(len(vehicles)):
                for j in range(len(vehicles)):
                    if j == i: # skip itself
                        continue
                    diff = abs(float(vehicles[i].attrib['pos'])-float(vehicles[j].attrib['pos']))
                    if diff < THRES: # i and j are adjacent
                        adj[t, int(vehicles[i].attrib['id']), int(vehicles[j].attrib['id'])] = 1

np.savez_compressed("my_data", adj=adj)
