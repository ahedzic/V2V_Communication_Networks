# V2V_Communication_Networks

Following the installation guide at https://www.youtube.com/watch?v=PfAWhrmoYgM, install OMNet++ IDE, then install inet from the options. 
Make sure to download Veins, then import it in the OMNet++ IDE by right-clicking in Project Explorer->Import->Existing projects into workspace->Veins folder.
Download and do the same with this V2VSimulation project. Then download and install SUMO. 

To run, first start SUMO by typing command

	python path_to_veins/sumo-launched.py -vv -c 'path_to_sumo/Eclipse/Sumo/bin/sumo.exe'
	
Then run the simulator by right-clicking on V2VSimulation->Run As->OMNet++ Simulation. Accept default configuration. Click Run. 

My versions:  OMNet++ 5.6.2, Veins 5.2, SUMO 1.8.0, INET (installed by OMNet++ IDE).