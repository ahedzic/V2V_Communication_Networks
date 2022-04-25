# V2V_Communication_Networks

Following the installation guide at https://www.youtube.com/watch?v=PfAWhrmoYgM, install OMNeT++ IDE, then install inet from the options. 
Start OMNeT++ IDE from mingwenv console, found in your omnetpp root directory, and type 

	omnetpp
	
Make sure to download Veins, then import Veins into the OMNeT++ IDE by right-clicking in Project Explorer->Import->Existing projects into workspace->Veins folder.
Download and do the same with this V2VSimulation project, then right-click and select Build Project. Then download and install SUMO. 

To run, first start SUMO by typing command in the mingwenv console

	python [path_to_veins]/sumo-launchd.py -vv -c '[path_to_sumo]/Eclipse/Sumo/bin/sumo.exe'
	
Then run the simulator from the IDE by right-clicking on V2VSimulation->Run As->OMNeT++ Simulation. Accept default configuration. Click Run. 
To run it on the custom map, go to V2VSimulation/simulations/veins_inet/omnetpp.ini, right-click on the .ini file->Run As->OMNeT++ Simulation.

My versions:  OMNeT++ 5.6.2, Veins 5.2, SUMO 1.8.0, INET (installed by OMNet++ IDE).