import json
import os
import pickle

from node import Node

if __name__ == "__main__":
    results_file = open("results.json")
    results = json.load(results_file)
    nodes_timeline = {}
    ''' nodes_timeline = {
            timestep_1: {
                node_id_1: node_1, 
                node_id_2: node_2, 
                ...
            },
            timestep_3: {
                node_id_1: node_1, 
                node_id_2: node_2, 
                ...
            },
            ...
        }
    '''

    if len(results.keys()) > 0:
        node_vectors = results[list(results.keys())[0]]["vectors"]

        for vector in node_vectors:
            name = vector["module"]
            timesteps = vector["time"]
            node_field = vector["name"]
            values = vector["value"]

            for i in range(len(timesteps)):
                nodes_at_timestep = {}
                node = Node()
                time = timesteps[i]

                if time in nodes_timeline.keys():
                    nodes_at_timestep = nodes_timeline[time]

                if name in nodes_at_timestep.keys():
                    node = nodes_at_timestep[name]

                if node_field == "posx":
                    node.posX = values[i]
                elif node_field == "posy":
                    node.posY = values[i]
                elif node_field == "speed":
                    node.speed = values[i]
                elif node_field == "acceleration":
                    node.acceleration = values[i]

                nodes_at_timestep[name] = node
                nodes_timeline[time] = nodes_at_timestep

        nodes_timeline_file = open("nodes_timeline.pkl","wb")
        pickle.dump(nodes_timeline, nodes_timeline_file)
        nodes_timeline_file.close()
