#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MonteCarloWindow.py
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

# System
import time
import pygtk
pygtk.require('2.0')
import gtk
#import gtk.gtkgl
#import gobject
import sys
import os


import json 
from pprint import pprint

#gui
#from gui.FileChooserWindow  import FileChooserWindow 
#from modules.GetFileType    import GetFileType

try:
    from py4j.java_gateway import JavaGateway
except:
    print 'Impossible to import py4j.java_gateway / JavaGateway'
    print 'Please try: sudo pip instal py4j'

from modules.LogFileParse import LogFileParse

from modules.LogFileParse import fromParametersToFile

class MonteCarloDialog:
    """ Class doc """
    def __init__ (self,  Session = None, ClickedJobID = None, ReRunJOB = None ):
        """ Class initialiser """
        self.Session = Session
        try:
            self.gui = self.Session.gui
        except:
            self.gui = os.getcwd()
            
        self.ClickedJobID = ClickedJobID
        self.project      =  None
        #---------------- building the ProjectChooserDialog ------------------#
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(self.gui, 'MonteCarloDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog  = self.builder.get_object('dialog1')
        #---------------------------------------------------------------------#
        
    
        #---------------------------------------------#
        #              INPUT  PARAMETERS              #
        #---------------------------------------------#
        self.InputFiles       = None               
        self.InputParamaters  = None
        self.OutputParameters = None
        self.folder           = ''
        
        #---------------------------------------------#
        #                 INPUT FILES                 #
        #---------------------------------------------#

        if ReRunJOB == None:
            self.InputFiles = None#{
                             #'input_coords': self.Session.projects[self.Session.ActivedProject]['Jobs']['0']['Output']
                             #}
        else:                #
            self.InputFiles = None #{
                             #'input_coords': self.Session.projects[self.Session.ActivedProject]['Jobs']['0']['Output']
                             #}
                              
    #--------------Dialog methods----------------#
    def ImportCellValorsFromProject (self):
        """ Function doc """
        project = self.Session.projects[self.Session.ActivedProject]
        try:
            self.builder.get_object('cell_maxX_entry').set_text(str(project['Cell']["maxX"]))
            self.builder.get_object('cell_maxY_entry').set_text(str(project['Cell']["maxY"]))
            self.builder.get_object('cell_maxZ_entry').set_text(str(project['Cell']["maxZ"]))
            self.builder.get_object('cell_minX_entry').set_text(str(project['Cell']["minX"]))
            self.builder.get_object('cell_minY_entry').set_text(str(project['Cell']["minY"]))
            self.builder.get_object('cell_minZ_entry').set_text(str(project['Cell']["minZ"]))
        except:
            print 'Cell parameters not available'
    #--------------------------------------------#
    
    def CreateNewFolder (self):
        """ Function doc """
        # - - - Ceating a new folder - - - #
        Job       = str(len(self.project['Jobs'])) # the new job ID
        newfolder = os.path.join(self.project['Folder'],Job +'_MonteCarlo')  # eg. /home/LABIO/Workspace/myself.project/1_MonteCarlo
        if not os.path.exists (newfolder): 
            os.mkdir (newfolder) 
        self.folder = newfolder

    def GenerateMastersMCInputFiles (self, InputFileName = None, OutputFileName = None):
        """ Function doc """
        parameters   = self.InputParamaters['MCparameters']
        input_coords = self.InputFiles['input_coords']
        
        Job          = str(len(self.project['Jobs'])) # the new job ID
        
        if OutputFileName == None:
            self.InputParamaters['outputname'] = Job +'_MonteCarlo'
        else:
            self.InputParamaters['outputname'] = OutputFileName

        
        
        '''                                    
        --- ---------------------------------- ---
        ---            Input File              ---
        --- ---------------------------------- ---
        '''
         
        arq          = open(InputFileName, 'w')
        #----------------------------------INPUT-PARAMETERS---------------------------------------#
        text = '#  - - MASTERS input file simulation - - \n'                                      #
        text = str(text)                                                                          #
        text =  text + '\n'                                                                       #
        text =  text + '#JobTitle    = ' + self.InputParamaters['title']             + '\n'       #
        text =  text + '#ProjectName = ' + self.project['ProjectName']               + '\n'       #
        text =  text + '#User        = ' + self.project['User']                      + '\n'       #
        text =  text + '#Generated   = ' + time.asctime(time.localtime(time.time())) + '\n'       #
                                                                                                  #
        text =  text + '\n\n'                                                                     #
                                                                                                  #
        text =  text + '# - - JOB-PATH - - \n'                                                    #
        text =  text + 'job_path     = ' + '"' + self.folder                        + '/"' + '\n' #
        text =  text + 'input_coords = ' + '"' + input_coords                       + '/"\n'      #
        text =  text + 'title        = ' + '"' + self.InputParamaters['outputname'] + '"'  + '\n' #
        text =  text + '\n\n'                                                                     #
        #-----------------------------------------------------------------------------------------#

        
        
        #-----------------------------CELL-PARAMETERS------------------------------------#
        text =  text + '# - - CELL-PARAMETERS - - \n'                                    #
        text =  text + 'max_pxcor = ' + str(self.InputParamaters['Cell']["maxX"]) + '\n' #
        text =  text + 'max_pycor = ' + str(self.InputParamaters['Cell']["maxY"]) + '\n' #
        text =  text + 'max_pzcor = ' + str(self.InputParamaters['Cell']["maxZ"]) + '\n' #
        text =  text + 'min_pxcor = ' + str(self.InputParamaters['Cell']["minX"]) + '\n' #
        text =  text + 'min_pycor = ' + str(self.InputParamaters['Cell']["minY"]) + '\n' #
        text =  text + 'min_pzcor = ' + str(self.InputParamaters['Cell']["minZ"]) + '\n' #
        text =  text + '\n\n'                                                            #
        #--------------------------------------------------------------------------------#
        
        
        
        #-------------------------------MCPARAMETERS------------------------------#
        text =  text + '# - - PARAMETERS - - \n'                                  #
        for i in parameters:                                                      #
            text =  text + i + ' = ' + parameters[i] + '\n'                       #
        #-------------------------------------------------------------------------#
        
        arq.writelines(text)
        arq.close()
        return InputFileName

    def RunMastersMCSimulation (self):
        """ Function doc """
        #-------------------------INPUT FILE-------------------------------#
        self.project = self.Session.projects[self.Session.ActivedProject]  #
        Job     = str(len(self.project['Jobs']))                           #
        title   = Job +'_MonteCarlo'                                       #
                                                                           #
                                                                           #
        self.CreateNewFolder()                                             #
        InputFileName = os.path.join(self.folder, Job +'_MonteCarlo.in')   #
        self.GenerateMastersMCInputFiles(InputFileName)                    #
        #------------------------------------------------------------------#
        
        
        HOME   = os.environ.get('HOME')
        FOLDER = HOME +'/.config/MASTERS/'
        
        
        
        # - - - - - RUN MC SIMULATION - - - - -#
        gateway = JavaGateway()
        masters = gateway.entry_point.getMasters()
        masters.loadParameters(InputFileName)
        
        print 'Starting simulation'
        step = 0
        
        
        start      = time.asctime(time.localtime(time.time()))
        self.Session.projects[self.Session.ActivedProject]['Jobs'][Job] = {
                                     'Title'             : self.InputParamaters['title']         ,
                                     'Folder'            : self.folder                           ,                
                                     'Input'             : InputFileName                         ,
                                     'Output'            : os.path.join(self.folder,title+'.pdb'),
                                     'LogFile'           : os.path.join(self.folder,title+'.log'),
                                     'Type'              : 'MonteCarlo'                          , 
                                     'Status'            : 'running'                             ,
                                     'Energy'            : '  -  '                               ,                   
                                     'LowestEnergyModel' : '  -  '                               ,
                                     'Start'             : start                                 ,                 
                                     'End'               : 'running'                             ,
                                     'Energy'            : '  -  '                               ,
                                     'parameters'        : self.InputParamaters['MCparameters']
                                     }              
        
        
        
    #projects[index]['Jobs']['0'] = {
    #                            'Title'  : 'Extended coordinates from AB sequence',
    #                            'Folder' : folder, #
    #                            #'File'   : os.path.join(Filename),
    #                            'Input'  : '-',
    #                            'Output' : os.path.join(Filename),
    #                            'LogFile': os.path.join(Filename),
    #                            'Type'   : 'Initial Coordinates', #
    #                            'Energy' : '-', # exemplo de como deve ser o dic jobs
    #                            'Start'  : start, #
    #                            'End'    : 'finished' } #
    #    
        

        json.dump(self.Session.projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)
        self.Session.AddJobHistoryToTreeview()
        
        projectID  = self.Session.ActivedProject
        Jobs       = self.Session.projects[projectID]['Jobs']
        liststore  = self.Session.builder.get_object("liststore1")
        pprint(self.Session.projects[self.Session.ActivedProject]['Jobs'][Job])
        

        self.Session.MonteCarloDialog.dialog.hide()
        #self.Session.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
        
        
        try:
            while masters.is_running():
                masters.step()

                # Update UI
                while gtk.events_pending():
                    gtk.main_iteration(False)

                # ---------- adicionar aqui  tudo que  sera gerado de arquivos --------- #
                try:
                    
                    _parameters = LogFileParse (os.path.join(self.folder,title+'-current.pdb'))
                    fromParametersToFile(_parameters, self.folder, Job +'_MonteCarlo.log') 
                    
                    self.Session.projects[self.Session.ActivedProject]['Jobs'][Job]['Energy'] = _parameters['lowerEnergy']
                    self.Session.projects[self.Session.ActivedProject]['Jobs'][Job]['LowestEnergyModel']= _parameters['LowestEnergyModel']
                    #print self.Session.projects[self.Session.ActivedProject]['Jobs'][Job]['Energy']
                    #self.Session.projects[self.Session.ActivedProject]['Jobs'][Job]['Energy'] = _parameters['lowerEnergyModel']
                    
                    self.Session.AddJobHistoryToTreeview()
                    
                    os.rename(
                             os.path.join(self.folder,title+'-current.pdb'),
                             os.path.join(self.folder,title+'_step_' + str(step))
                             )
                    step += 1
                    
                except:
                    pass
        
            self.Session.projects[self.Session.ActivedProject]['Jobs'][Job]['Status'] = 'finished'
        except Exception as error:
            self.Session.projects[self.Session.ActivedProject]['Jobs'][Job]['Status'] = 'aborted'
            #print 'olha o erro ai moreno' 
            print error
            
        json.dump(self.Session.projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)
        self.Session.AddJobHistoryToTreeview()
    
    
    #----------------------------BUTTONS---------------------------#
    def on_button_RunMCSimulation_clicked (self, button):
        """ Function doc """
        
        # Environment Variables
        title                            = self.builder.get_object('job_title_entry')                       .get_text()
        InitialTemperature               = self.builder.get_object('Initial_Temperature_entry')             .get_text()
        Temperature_THR                  = self.builder.get_object('Temperature_THR_entry')                 .get_text()
        AttemptsThresholdWithDirector    = self.builder.get_object('AttemptsThresholdWithDirector_entry')   .get_text()
        AttemptsThresholdWithoutDirector = self.builder.get_object('AttemptsThresholdWithoutDirector_entry').get_text()
        MaxMumberOfNoImprovenment        = self.builder.get_object('MaxMumberOfNoImprovenment_entry')       .get_text()
        MinTemperatureAllowed            = self.builder.get_object('MinTemperatureAllowed_entry')           .get_text()
        TemperatureDecreaseRatio         = self.builder.get_object('TemperatureDecreaseRatio_entry')        .get_text()
        EnergyVariationThreshold         = self.builder.get_object('EnergyVariationThreshold_entry')        .get_text()

        # Directors
        TotalDirectorsMovies             = self.builder.get_object('TotalDirectorsMovies_entry')     .get_text()
        TemperatureFactorDirector        = self.builder.get_object('TemperatureFactorDirector_entry').get_text()
        MinCrank                         = self.builder.get_object('MinCrank_entry')                 .get_text()
        AddWeightPivotCrank              = self.builder.get_object('AddWeightPivotCrank_entry')      .get_text()
        MinPivotDistance                 = self.builder.get_object('MinPivotDistance_entry')         .get_text()
        MaxAngle                         = self.builder.get_object('MaxAngle_entry')                 .get_text()

        # Searching Agents
        TemperatureFactorSearch          = self.builder.get_object('TemperatureFactorSearch_entry').get_text()

        
        self.InputFiles = {
                           'input_coords': self.Session.projects[self.Session.ActivedProject]['Jobs']['0']['Output']
                           }        
        
        InputFiles       =  {
                             'input_coords'      : self.InputFiles['input_coords'],
                             'spatial_restraints': None,
                             'SS_restraints'     : None
                            } 
                         
        self.InputParamaters = {
                                 'title'        : title,
                                 'outputname'   : None ,
                                 
                                 'Cell'         : {
                                                   "maxX": self.builder.get_object('cell_maxX_entry').get_text(),
                                                   "maxY": self.builder.get_object('cell_maxY_entry').get_text(),
                                                   "maxZ": self.builder.get_object('cell_maxZ_entry').get_text(),
                                                   "minX": self.builder.get_object('cell_minX_entry').get_text(),
                                                   "minY": self.builder.get_object('cell_minY_entry').get_text(),
                                                   "minZ": self.builder.get_object('cell_minZ_entry').get_text()
                                                   },
                                            
                                 'MCparameters' :{
                                                   'temperature'                            : InitialTemperature               ,
                                                   'temp_thr'                               : Temperature_THR                  ,
                                                   'attempted_threshold_with_dir'           : AttemptsThresholdWithDirector    ,
                                                   'attempted_threshold_without_dir'        : AttemptsThresholdWithoutDirector ,
                                                   'max_number_of_no_improvement_in_energy' : MaxMumberOfNoImprovenment        ,
                                                   'min_temperature_allowed'                : MinTemperatureAllowed            ,
                                                   'temp_decrease_ratio'                    : TemperatureDecreaseRatio         ,
                                                   'energy_variation_threshold'             : EnergyVariationThreshold         ,
                                                   'total_dir_moves'                        : TotalDirectorsMovies             ,
                                                   'temp_factor_dir'                        : TemperatureFactorDirector        ,
                                                   'min_crank'                              : MinCrank                         ,
                                                   'max_crank'                              : AddWeightPivotCrank              ,
                                                   'min_pivot_dist'                         : MinPivotDistance                 ,
                                                   'max_angle'                              : MaxAngle                         ,
                                                   'temp_factor_search'                     : TemperatureFactorSearch         
                                                   },
                                 }

        self.OutputParameters = {
                                'PyMOL_update'       : None,
                                'PDB_real'           : None,
                                'Graph_log'          : True,
                                'Splitted_PDB_files' : False
                                }

        pprint(self.InputFiles)
        pprint(self.InputParamaters)
        pprint(self.OutputParameters)
        
        self.RunMastersMCSimulation()
  
    def on_button_addFiles_clicked(self, button):
        """ Function doc """
        print 'Add new files'
        
    def on_button_removeFile_clicked(self, button):
        """ Function doc """
        print 'Remove files'


def main():
    dialog = MonteCarloDialog()
    a = dialog.dialog.run()
    b = dialog.dialog.hide()
    print a
if __name__ == '__main__':
	main()

