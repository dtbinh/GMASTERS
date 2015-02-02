#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DialogNewProject.py
#  
#  Copyright 2014 Labio <labio@labio-XPS-8300>
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
import gtk
import time
from pprint import pprint
import json 
from modules.pdbmodules import *

import pango




               
def CreateNewProject (projects, parameters):

    """ Function doc """
    user          = parameters['User']
    projectID     = parameters['ProjectName']
    add_info      = parameters['Info']
    folder        = parameters['Folder']
    sequence      = parameters['Sequence']
    
    ABsequence    = parameters['ABsequence']
    AminoAcidDic  = parameters['ABmodel'] 
    
    
    ABsequence = from20letterToAB (sequence, AminoAcidDic)
    
    index      = str(len(projects) + 1)
    
    start      = time.asctime(time.localtime(time.time()))
    
    #----------------------------CELL PARAMETERS-------------------------------#
    size = float(len(sequence))                                                #
    size = size + 14                                                           #
    minX = -1*(size/2)                                                         #
    minY = -20.0                                                               #
    minZ = -20.0                                                               #
    maxX =  (size/2)                                                           #
    maxY =  20.0                                                               #
    maxZ =  20.0                                                               #
    #--------------------------------------------------------------------------#
    
    projects[index] = {
                       'User'        : user     ,
                       'ProjectName' : projectID,
                       'Info'        : add_info ,
                       'Folder'      : folder   ,
                       'Sequence'    : sequence,
                       'ABsequence'  : ABsequence,                
                       'ABmodel'     : AminoAcidDic,        
                       'Generated'   : start,                
                       'Modified'    : start,                
                       'Cell'        : {'minX' : minX,
                                        'minY' : minY,
                                        'minZ' : minZ,
                                        'maxX' : maxX,
                                        'maxY' : maxY,
                                        'maxZ' : maxZ},
                       'Jobs'        : {}
                        }
    
    HOME   = os.environ.get('HOME')
    FOLDER = HOME +'/.config/MASTERS/'
    
    
    _filename = str(index)+'_initialCoordinates.pdb'
    Filename = GeneratePDBtoProject(projects[index], parameters = None, filename = _filename)
    
    projects[index]['Jobs']['0'] = {
                                'Title'             : 'Extended coordinates from AB sequence',
                                'Folder'            : folder                                 , 
                                'Input'             : '-'                                    ,
                                'Output'            : os.path.join(Filename)                 ,
                                'LogFile'           : os.path.join(Filename)                 ,
                                'Type'              : 'Initial Coordinates'                  , 
                                'Status'            : 'finished'                             ,
                                'Energy'            : '  -  '                                , 
                                'LowestEnergyModel' : '  -  '                                ,
                                'Start'             : start                                  , 
                                'End'               : 'finished' } #
    
    json.dump(projects, open(FOLDER + 'ProjectHistory.dat', 'w'), indent=2)


class NewProjectDialog():
    
    """ Class doc """
    def on_new_project_entry_changed (self, entry):
        """ Function doc """
        text      = self.builder.get_object("new_project_entry").get_text()
        WorkSpace = self.MASTERSSession.GUIConfig['WorkSpace']
        path      = os.path.join(WorkSpace, text)
        print  text
        self.builder.get_object("project_directory_entry").set_text(path)
    
    def CreateNewProject_button (self, button):
        """ Function doc """
        user          =  self.builder.get_object('user_entry').get_text()
        projectID     =  self.builder.get_object('new_project_entry').get_text()
        folder        =  self.builder.get_object('project_directory_entry').get_text()
        _buffer       =  self.builder.get_object('textview1').get_buffer()
        _buffer_infor =  self.builder.get_object('textview2').get_buffer()



        folder2 = folder.split('/')
        path = '/'
        for i in folder2:
            path = os.path.join(path, i)
            if not os.path.exists (path): 
                os.mkdir (path)
        
        
        sequence  = _buffer.get_text(*_buffer.get_bounds(), include_hidden_chars=False)
        add_info  = _buffer_infor.get_text(*_buffer_infor.get_bounds(), include_hidden_chars=False)
        sequence = sequence.replace('\n', '')
        sequence = sequence.replace(' ', '')
        sequence = sequence.replace('-', '')
        sequence = sequence.replace('.', '')
        sequence = sequence.replace(',', '')
        sequence = sequence.upper()
    
        if folder == None:
            self.builder.get_object('dialog1').hide()
            self.builder.get_object('messagedialog1').format_secondary_text("A folder is required")
            
            MessageDialog = self.builder.get_object('messagedialog1')
            #dialog.dialog.run()
            #dialog.dialog.hide()
            a = MessageDialog.run()  # possible "a" valors                                                           
            # 4 step                 # -8  -  yes                                                                    
            MessageDialog.hide()     # -9  -  no                                                                     
                                     # -4  -  close                                                                  
                                     # -5  -  OK                                                                     
                                     # -6  -  Cancel   
            self.builder.get_object('dialog1').run()

        elif sequence == '':
            self.builder.get_object('dialog1').hide()
            
            self.builder.get_object('messagedialog1').format_secondary_text("A sequence is required")
            
            MessageDialog = self.builder.get_object('messagedialog1')
            #dialog.dialog.run()
            #dialog.dialog.hide()
            a = MessageDialog.run()  # possible "a" valors                                                           
            # 4 step                 # -8  -  yes                                                                    
            MessageDialog.hide()     # -9  -  no                                                                     
                                     # -4  -  close                                                                  
                                     # -5  -  OK                                                                     
                                     # -6  -  Cancel   
            self.builder.get_object('dialog1').run()
        
        else:
            parameters =   {'User'        : user     ,
                            'ProjectName' : projectID,
                            'Info'        : add_info ,
                            'Folder'      : folder   ,
                            'Sequence'    : sequence,
                            'ABsequence'  : None,                
                            'ABmodel'     : AminoAcidDic,        
                            'Generated'   : None,                
                            'Modified'    : None,                
                            'Jobs'        : {}
                            }
            
            """ Starting a new project 
                'Title'  : 'Testing MonteCarlos Sim',
                'Folder' : folder,                
                'Input'  : filename_in,
                'Output' : filename_out,
                'LogFile': ''          , 
                'Type'   : 'MonteCarlo', 
                'Energy' : str(rdm.random()*1.2345),                   
                'Start'  : '  -  ',                 
                'End'    : '  -  ' } 
            """


            
            CreateNewProject (self.projects, parameters, )
            
            print self.projects
            self.MASTERSSession.ProjectChooserDialog.AddProjectHistoryToTreeview()

    def __init__(self, MASTERSSession = None): #main_builder=None, projects = None, WindowControl = None, GUIConfig = None):
        
        """ Class initialiser """
        
        self.MASTERSSession   =  MASTERSSession
        self.projects         =  MASTERSSession.projects
        login                 =  os.getlogin()
        self.gui              = MASTERSSession.gui

        
        if self.projects == None:
            self.projects = {}
        
        self.builder = gtk.Builder()
        self.main_builder = MASTERSSession.builder

        
        self.builder.add_from_file(os.path.join(self.gui,'MastersNewProject.glade'))
        self.builder.connect_signals(self)
        
        self.dialog    = self.builder.get_object('dialog1')
        self.GUIConfig = MASTERSSession.GUIConfig
        
        
        
        localtime = time.asctime(time.localtime(time.time()))
        print "Local current time :", localtime
        localtime = localtime.split()

        #  0     1    2       3         4
        #[Sun] [Sep] [28] [02:32:04] [2014]
        text = login + '_project_' + localtime[1] + \
            '_' + localtime[2] + '_' + localtime[4]
        self.builder.get_object("new_project_entry").set_text(text)
        self.builder.get_object("user_entry").set_text(login)
        
        
        
        if self.GUIConfig  != None:
            self.builder.get_object('project_directory_entry').set_text(self.GUIConfig['WorkSpace'])
        
        



def main():
    dialog = NewProjectDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()



def main():
	
	return 0

if __name__ == '__main__':
	main()

