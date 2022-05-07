import os
import sys
import numpy as np 
import logging
import random
from collections import defaultdict

from .data_handler import DataHandler

class StreamDataHandler(DataHandler):

    def __init__(self):
        super(StreamDataHandler, self).__init__()

    def load(self, data_name, t):
        self.data_name = data_name
        self.t = t
        self.feature_size = 3
        self.train_size = 128

        # Load attributes
        attributes_file_name = os.path.join('../data', data_name, 'stream_attributes', str(self.t))
        self.features = np.loadtxt(attributes_file_name)

        # Load labels
        self.positive_u_labels = []
        stream_labels_positive_u_file_name = os.path.join('../data', data_name, 'stream_labels_positive_u', str(self.t))
        with open(stream_labels_positive_u_file_name) as file:
            for line in file: 
                line = line.strip() #or some other preprocessing
                self.positive_u_labels.append(int(line))

        self.positive_v_labels = []
        stream_labels_positive_v_file_name = os.path.join('../data', data_name, 'stream_labels_positive_v', str(self.t))
        with open(stream_labels_positive_v_file_name) as file:
            for line in file: 
                line = line.strip() #or some other preprocessing
                self.positive_v_labels.append(int(line))

        self.negative_u_labels = []
        stream_labels_negative_u_file_name = os.path.join('../data', data_name, 'stream_labels_negative_u', str(self.t))
        with open(stream_labels_negative_u_file_name) as file:
            for line in file: 
                line = line.strip() #or some other preprocessing
                self.negative_u_labels.append(int(line))

        self.negative_v_labels = []
        stream_labels_negative_v_file_name = os.path.join('../data', data_name, 'stream_labels_negative_v', str(self.t))
        with open(stream_labels_negative_v_file_name) as file:
            for line in file: 
                line = line.strip() #or some other preprocessing
                self.negative_v_labels.append(int(line))

        # Load nodes
        nodes_file_name = os.path.join('../data', data_name, 'nodes')
        self.all_nodes_list = np.loadtxt(nodes_file_name, dtype = np.int64)

        # Load graph
        stream_edges_dir_name = os.path.join('../data', data_name, 'stream_edges_training')
        self.nodes = set()
        self.cha_nodes_list, self.old_nodes_list = set(), set()
        self.adj_lists = defaultdict(set)
        
        begin_time = 0
        end_time = t
        edges_file_name = os.path.join(stream_edges_dir_name, str(t))
        with open(edges_file_name) as fp:
            for i, line in enumerate(fp):
                info = line.strip().split()
                node1, node2 = int(info[0]), int(info[1])

                self.nodes.add(node1)
                self.nodes.add(node2)

                self._assign_node(node1, int(t))
                self._assign_node(node2, int(t))

                self.adj_lists[node1].add(node2)
                self.adj_lists[node2].add(node1)
        
        # Generate node and label list
        #self.labels = np.ones(len(self.nodes), dtype=np.int64)
        #self.labels[labels[:, 0]] = labels[:, 1]

        # Input & Output size
        #self.feature_size = self.features.shape[1]
        #self.label_size = np.unique(self.labels).shape[0]

        # Train & Valid data
        self.train_nodes = self.all_nodes_list
        
        self.train_nodes = list(self.train_nodes)
        self.cha_nodes_list, self.old_nodes_list = list(self.cha_nodes_list), list(self.old_nodes_list)
        
        self.train_size = len(self.train_nodes)
        self.data_size = self.train_size



    def _assign_node(self, node, tt):
        if node in self.all_nodes_list and tt == self.t:
            self.cha_nodes_list.add(node)
        elif node in self.all_nodes_list and tt < self.t:
            self.old_nodes_list.add(node)
    