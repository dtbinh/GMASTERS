#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  LogFileParse.py
#  
#  Copyright 2015 Labio <labio@labio-XPS-8300>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os
from pprint import pprint


def ParseOutputLogFile (filein):
    """ Function doc """
    arq = open(filein, 'r')
    model                = []
    acc_director_agents  = []
    acc_searching_agents = []
    energy               = []
    
    
    for line in arq:
        line2 = line.split()
        if len(line2) ==4:
            if line[0] != '#':
                #print line 
                model               .append(float(line2[0]))
                acc_director_agents .append(float(line2[1]))
                acc_searching_agents.append(float(line2[2]))
                energy              .append(float(line2[3]))
                #print model, acc_director_agents, acc_searching_agents, energy
    
    parameters = {
                 'type'                 : 'masterslog'        ,
                 'model'                : model               , 
                 'acc_director_agents'  : acc_director_agents , 
                 'acc_searching_agents' : acc_searching_agents, 
                 'energy'               : energy              
                 }
    return parameters #model, acc_director_agents, acc_searching_agents, energy
    
    
    
def fromParametersToFile (par, path = None, title = None  ):
    """ Function doc """
    if path == None:
        path =  os.getcwd()
    if title == None:
        title =  'output.log'
    
    text = '\n' 
    arq  = open(os.path.join(path, title), 'a')
    
    text = text + par['model'] 
    text = text + "   "+ par['acc_ratio_director_agents'] 
    text = text + "   "+ par['acc_ratio_searching_agents']
    text = text + "   "+ par['current_energy']
    
    arq.writelines(text)
    arq.close()
    

#ef fromParametersToString (parameters, path = None, title = None  ):
#   """ Function doc """
#   return parameters['acc_ratio_director_agents' ], 
#          parameters['acc_ratio_searching_agents'],
#          parameters['current_energy'            ],
#          parameters['lowerEnergy'               ],
#          parameters['lowerEnergyModel'          ],
#          parameters['model'                     ],
#          parameters['title'                     ]
#

def LogFileParse (filein):
    """ Function doc """
    parameters = {}
    
    arq = open(filein, 'r')
    for line in arq:
        #print line
        line2 = line.split()
        if line2[0] == 'MODEL':
            parameters['model'] = line2[1]
        
        if line2[0] == 'REMARK':
            if line2[1] == 'TITLE:':
                parameters['title'] = line2[2]
            
            if line2[1] == 'LOWER':
                if line2[2] == 'ENERGY:':
                    parameters['lowerEnergy'] = line2[3]

            if line2[1] == 'LOWER':
                if line2[2] == 'ENERGY':
                    if line2[3] == 'MODEL:':
                        parameters['LowestEnergyModel'] = line2[4]
            
            if line2[1] == 'current_energy:':
                parameters['current_energy'] = line2[2]
            
            if line2[1] == 'acc_ratio_searching_agents:':
                parameters['acc_ratio_searching_agents'] = line2[2]
            
            if line2[1] == 'acc_ratio_director_agents:':
                parameters['acc_ratio_director_agents']  = line2[2]
    pprint(parameters)
    return parameters
    
def main():
    LogFileParse ('/home/labio/MastersWorkspace/TesteComMasters_Jan_27_2015/2_MonteCarlo/2_MonteCarlo_step_137')
    #ParseOutputLogFile ('/home/labio/Dropbox/mastersGUI/1_MonteCarlo.log')
    return 0

if __name__ == '__main__':
	main()

