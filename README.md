# Installation and running

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

# Custom road network and routes

To build a network from a custom map exported from OpenStreetMaps, manually select an area on OpenStreetMaps and export to an .osm file and save it in data/ folder. 
Then in a console, cd to Sumo root folder where it was installed, and execute the command

	bin/netconvert.exe --osm-files data/asutempe.osm -o data/asutempe.net.xml --type-files "data/typemap/osmNetconvert.typ.xml, data/typemap/osmNetconvertPedestrians.typ.xml, data/typemap/osmNetconvertBicycle.typ.xml" --geometry.remove --tls.join --junctions.join --ramps.guess
	
This imports sidewalks for pedestrians and bicycle lanes on top of default motorway settings. The .net.xml file contains the road network. 
Next, make sure you have typemap.xml in the data/ folder, execute the command 

	bin/polyconvert.exe --net-file data/asutempe.net.xml --osm-files data/asutempe.osm --type-file data/typemap.xml -o data/asutempe.poly.xml
	
This imports polygons from the .osm file such as buildings, rivers, and railways and generates the .poly.xml file. 
Finally, you will edit the .sumocfg file by adding the generated .net.xml file and .poly.xml file. The body of the .sumocfg file looks like this

	<configuration>
		<input>
			<net-file value="asutempe.net.xml"/>
			<route-files value="asuvehicle.rou.xml"/>
			<additional-files value="asutempe.poly.xml"/>
		</input>
	
		<time>
			<begin value="0"/>
			<end value="2000"/>
		</time>
	</configuration>
	
<!-- The route file, asupedestrian.rou.xml, generates a list of pedestrian trips. This is generated using the command

	python tools/randomTrips.py --net-file data/asutempe.net.xml --output-trip-file data/asupedestrian.trips.xml --route-file data/asupedestrian.rou.xml --pedestrians --length --end 20
	 -->
Generate the vehicle route file using the command 

	python tools/randomTrips.py --net-file data/asutempe.net.xml --output-trip-file data/asuvehicle.trips.xml --route-file data/asuvehicle.rou.xml --length --end 100 
	
You will import the .net.xml, .rou.xml, .poly.xml, and .trips.xml files into your OMNeT++ simulation project folder, and update map.sumo.cfg and square.launchd.xml. 
Then you can run simulations on the custom map as in the previous section.

# Output 

To get a dump of the state of the network at every time step, i.e. which vehicle is on which edge (street) with pos and speed, cd into the bin/ folder where sumo.exe is, and execute 

	sumo.exe -c ../data/asutempe.sumocfg --netstate-dump ../data/netstate_dump.xml
	
To create adjacency matrix between vehicle nodes from a simulation run, cd into the same directory as netstate_dump.xml, and run 

	python adjacency.py
	
which generates my_data.npz. Load the numpy array via 

	my_data = np.load("my_data.npz")
	adj = my_data["adj"]
	
The numpy array adj has 3 dimensions, the first dimension indexes the timestep, and there are 681 timesteps in seconds. 
Each timestep contains an adjacency array of size 99 x 99, for 99 vehicles. 
The adjacency array simply captures adjacency between V2V, and not any other node type. 