# MASTERS
## HOW TO OPEN IT ON NETLOGO?

1. First of all you need NETLOGO. Make sure you have the Netlogo matrix, array and shell extensions installed. You have 2 options:
    1. Download Netlogo from it website: http://ccl.northwestern.edu/netlogo/  and then download the extensions and install them. You will need to download Masters_vBETA.nlogo3d too.
    2. Download our netlogo folder, with MASTERS inside (along with all other netlogo models) and with the extensions already installed. You will find it here in github, at the folder Netlogo-MASTERS. 
2. Execute the netlogo-3d.sh script. (Linux)  or  Open the NetLogo 3D 5.0.4 executable (Mac).
2. Click FILE -> OPEN  then find /MASTERS/Masters_vBETA.nlogo3d
3. For fast simulations it is advisable to unmark the "view uptdates" option at the 3D View window.
4. It's done! Enjoy MASTERS!

## WHAT IS IT?

MASTERS is a general sequence-based MultiAgent System for protein TERtiary Structure prediction.

## HOW IT WORKS

MASTERS is based on an ab initio approach. It's a cooperative hierarchical multiagent system guided by a combined Simulated Annealing/Monte Carlo scheme to address the PSP problem. The main idea behind MASTERS is to provide the user with freedom to choose the abstraction level, as well as the energy function/force field to lead the simulation. 

## THINGS TO NOTICE

When running the program the user can look at the Acceptance Ratio plot and see the progress of the simulation. 
It is recommendable a not so high acceptance ratio, for example.

It is important to stress that (1) type of movements, (2) model abstraction level and (3) energy function are three sides of the same triangle. Changing one of them will affect the behavior of the entire. 

## THINGS TO TRY

Create or apply the abstraction level of your choice!
Create or apply the energy function of your choice! 
Create or apply the scheme of movements of your choice!


## EXTENDING THE MODEL

The code is open, you can dig in and modify the optimization (Simulated Annealing/Monte Carlo) procedure as your wish.


## NETLOGO FEATURES

One of the remarkable advantages of Netlogo is its embedded tools,being BehaviorSpace is one of them. BehaviorSpace offers the possibility of automatically performing a big set of experiments based on changing parameters' values. In MASTERS, due to the BehaviorSpace capability, it is possible to explore more efficiently the conformational space of PSP predictions and tune MASTERS's parameters to achieve better results. 

### Try it yourself! 
Go to Tools -> BehaviorSpace.
There we have 2 samples:

1. How to take 2 sets of parameters: Each one run 40 times recording, at the end of each simulation, a lot of attributes including the final x,y and z coordinates  and the energy of every tick(timestep).

2. How to tune all your parameters: In the sample there are 7 different parameters. Each one with at least 2 options/values. Running this experiment will result in a combinatorial number of runs, regarding the combination of all the parameters/values.  


# HOW TO USE IT
## SETUP COMMANDS

###title
Normally it is the ID of the protein. It will be at the top of the .pdb file, if the user exports the 3-D visualization using the create_pdb_from simulation procedure. 

Example:

    create_pdb_from simulation "file.pdb"

###nr-of-directors
Input--> Number of Director Agents. Default value: 1.

 
###limit_prob_dir and limit_prob_search
Input--> Thresholds related to the acceptance ratio of the Director and Searching agents.

###parameters
Input--> Used by the procedure **load_parameters** to prepare the simulation. Follows the pattern a-b-c-d-e-f-g, where:

a = orchestra-sleep-time;

b = temp_factor_dir;

c = temp_factor_search;

d = nr-of-directors;

e = limit_prob_dir;

f = limit_prob_search

g = attempted_threshold_with_dir

###Resize
Button used to change the searching agent's size. It will not affect the simulation, just the 3-D visualization.

###Clear All
Clears all the input textboxes.

## MOVEMENTS
### SEARCHING AGENTS MOVEMENT
#### SCHEME 1
The _scheme 1_ movements are based on angles. The distance from two consecutive residues remain the same. This is a requirement of the default energy function (AB Model). There are two types:
  * 1 DOF move(Degrees of Freedom): Most of the residues move in 1DOF, keeping fixed the distance from the residues from the front and back.  
  * 3 DOF's: Just the first and last residues move that way. They also keep fixed their distances but they are binded at just one residue, so they have more freedom to move.

#### SCHEME 2
The _scheme 2_ movements are based on distance. The agent is placed on the center of a 1A cube and have the same probability to move to each other place on this cube. All the phase space is accessible this way. It is simple to achieve erodicity.

### DIRECTOR AGENTS MOVEMENT
##### CRANKSHAFT MOVE
First choose 2 residues A and B chain (at a distance of 3 residues). Rotate the residues that separate A and B by choosing a random angle, using the line from A to B as axis.

#### PIVOT MOVE
Choose a point (pivot residue) and a part of the chain rotates around this point using a random angle.


## CONTROL MONITORS
### Nr of Searching Agents.
Shows the current number of Searching agents

### Nr of Director Agents
Shows the current number of Director agents.

### Nr of Environment Agents
Shows the current number of Environment agents.

### Step
Shows the timestep or temperature step (related to the simulated annealing scheme).

### Current Energy
Shows system current energy based on the **compute_global_energy** procedure.

### Lower Energy and Lower Energy tick
Shows the best(lower) obtained energy.


## WORKFLOW
To be filled.

## PLOTS
To be filled.
## ATTEMPTED MOVES CONTROL
To be filled.
## SEARCHING AGENTS
To be filled.
## DIRECTOR AGENTS
To be filled.
## ENVIRONMENT AGENTS
To be filled.
## MONTE CARLO FACTORS
To be filled.
## DEBUGING
To be filled.

# CREDITS AND REFERENCES

## PUBLICATION
MASTERS: A general sequence-based MultiAgent System for protein TERtiary Structure prediction 

CS2BIO 2014
