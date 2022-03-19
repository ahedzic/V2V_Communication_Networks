#! /bin/sh
# This script has to be run from omnetpp's mingwenv console
opp_scavetool x results/*-\#0.vec -F JSON -o - > results.json
python node_parser.py
