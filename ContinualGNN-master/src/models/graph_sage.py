import sys
import logging
import numpy as np 

import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score

import dgl
import dgl.function as fn

sys.path.append('..')
from layers.sage_conv import SAGEConv
from layers.sampler import Sampler
from layers.aggregator import Aggregator


class DotPredictor(nn.Module):
    def forward(self, g, h):
        with g.local_scope():
            g.ndata['h'] = h
            # Compute a new edge feature named 'score' by a dot-product between the
            # source node feature 'h' and destination node feature 'h'.
            g.apply_edges(fn.u_dot_v('h', 'h', 'score'))
            # u_dot_v returns a 1-element vector for each edge so you need to squeeze it.
            return g.edata['score'][:, 0]


class GraphSAGE(nn.Module):

    def __init__(self, layers, in_features, adj_lists, args):
        super(GraphSAGE, self).__init__()

        self.layers = layers
        self.num_layers = len(layers) - 2
        self.in_features = torch.Tensor(in_features).to(args.device)
        self.adj_lists = adj_lists
        self.num_neg_samples = args.num_neg_samples
        self.device = args.device

        self.convs = nn.ModuleList()
        for i in range(self.num_layers):
            self.convs.append(SAGEConv(layers[i], layers[i + 1]))
        self.sampler = Sampler(adj_lists)
        self.aggregator = Aggregator()

        self.weight = nn.Parameter(torch.Tensor(layers[-2], layers[-1]))
        self.xent = nn.CrossEntropyLoss()
        self.dot_predictor = DotPredictor()

        self.init_parameters()

    def init_parameters(self):
        for param in self.parameters():
            nn.init.xavier_uniform_(param)

    def forward(self, nodes, pos_u, pos_v, neg_u, neg_v):
        train_pos_g = dgl.graph((torch.tensor(pos_u), torch.tensor(pos_v)), num_nodes=len(nodes))
        train_neg_g = dgl.graph((torch.tensor(neg_u), torch.tensor(neg_v)), num_nodes=len(nodes))
        layer_nodes, layer_mask = self._generate_layer_nodes(nodes)
        features = self.in_features[layer_nodes[0]]
        for i in range(self.num_layers):
            cur_nodes, mask = layer_nodes[i + 1], layer_mask[i]            
            aggregate_features = self.aggregator.aggregate(mask, features)
            features = self.convs[i].forward(x = features[cur_nodes], aggregate_x = aggregate_features)
        pos_score = 0
        pos_score = self.dot_predictor(train_pos_g, features)
        neg_score = self.dot_predictor(train_neg_g, features)
        return pos_score, neg_score

    def loss(self, nodes, pos_u, pos_v, neg_u, neg_v):
        pos_score, neg_score = self.forward(nodes, pos_u, pos_v, neg_u, neg_v)
        scores = torch.cat([pos_score, neg_score])
        labels = torch.cat([torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])])
        #print("AUC SCORE", roc_auc_score(labels, scores))
        return F.binary_cross_entropy_with_logits(scores, labels)

    def _generate_layer_nodes(self, nodes):
        layer_nodes = list([nodes])
        layer_mask = list()
        for i in range(self.num_layers):
            nodes_idxs, unique_neighs, mask = self.sampler.sample_neighbors(layer_nodes[0])
            layer_nodes[0] = nodes_idxs
            layer_nodes.insert(0, unique_neighs)
            layer_mask.insert(0, mask.to(self.device))
        return layer_nodes, layer_mask


    def get_embeds(self, nodes):
        layer_nodes, layer_mask = self._generate_layer_nodes(nodes)
        features = self.in_features[layer_nodes[0]]
        for i in range(self.num_layers):
            cur_nodes, mask = layer_nodes[i + 1], layer_mask[i]            
            aggregate_features = self.aggregator.aggregate(mask, features)
            features = self.convs[i].forward(x = features[cur_nodes], aggregate_x = aggregate_features)
        return features.data.numpy()