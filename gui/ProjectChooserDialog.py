#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ProjectChooseDialog.py
#  
#  Copyright 2015 Fernando Bachega <fernando@bahamuth>
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
import pango
from pprint import pprint

class ProjectChooserDialog:
    """ Class doc """
    
    def __init__ (self, MASTERSSession = None): 
        
        """ Class initialiser """
        self.MASTERSSession   =  MASTERSSession
        if self.MASTERSSession == None:
            self.gui = os.getcwd()
            
        else:
            self.gui = MASTERSSession.gui
            
        
        
        
        #---------------- building the ProjectChooserDialog ------------------#
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(self.gui, 'ProjectChooserDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog  = self.builder.get_object('dialog1')
        #---------------------------------------------------------------------#

    #---------------GUI CONFIG METHOD----------------#
    def AddProjectHistoryToTreeview (self, liststore=None , cell = None):
        
        model = liststore
        model = self.builder.get_object('liststore3')
        model.clear()
        #n = 0

        numbers  = list(self.MASTERSSession.projects) # this is necessary to sorte the self.project dic
        numbers2 = []
        
        for i in numbers:
            numbers2.append(int(i))
        numbers2.sort()
        
        for i in numbers2:
            if self.MASTERSSession.projects[str(i)] == None:
                pass
            else:
                cell = self.builder.get_object('cellrenderertext1')
                cell.props.weight_set = True
                cell.props.weight = pango.WEIGHT_NORMAL
                i = str(i)
                data = [str(i)                                           , 
                        self.MASTERSSession.projects[i]['ProjectName']   , 
                        self.MASTERSSession.projects[i]['Modified']      , 
                        str(len(self.MASTERSSession.projects[i]['Jobs'])), 
                        self.MASTERSSession.projects[i]['User'] 
                       ]
                #print i
                model.append(data)
                #n = n + 1
 
    
    #----------------TREEVIEW METHOD-----------------#
    def on_treeview3_button_release_event(self, tree, event):
        """ Function doc """
        if event.button == 3:
            print 'button3'
            #print "Mostrar menu de contexto botao3"
            #selection     = tree.get_selection()
            #model         = tree.get_model()
            #(model, iter) = selection.get_selected()
            #
            #if iter != None:
            #    self.selectedID  = str(model.get_value(iter, 1))
            #    self.selectedObj = str(model.get_value(iter, 2))
            #
            #    self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedID+' -' )
            #    widget = self.builder.get_object('treeview_menu')
            #    widget.popup(None, None, None, event.button, event.time)
            
        if event.button == 1:
            #print "Mostrar menu de contexto botao1"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            if iter != None:
                #print model, iter
                #JobID         = model.get_value(iter, 0)
                pymol_object  = model.get_value(iter, 2)  # @+
                projectID     = model.get_value(iter, 0)  # @+
                
                #self.MASTERSSession.ActivedProject = projectID
                
                
                
                
                #print _object
                #pprint (self.MASTERSSession.projects[self.MASTERSSession.ActivedProject]['Jobs'][JobID])
                pprint (self.MASTERSSession.projects[projectID])
                #filename = self.projects[self.ActivedProject]['Jobs'][JobID]['Output']
                ##print filename
                #self.load_file(filename)


    #-----------------TOOLBAR METHOD-----------------#
    def on_toolbutton_NewProject_clicked (self, button):
        """ Function doc """
        self.MASTERSSession.ProjectChooserDialog.dialog.hide()
        self.MASTERSSession.NewProjectDialog.dialog.run()
        self.MASTERSSession.NewProjectDialog.dialog.hide()
        self.MASTERSSession.ProjectChooserDialog.dialog.run()

    def on_toolbutton_DeleteSelectedProject_clicked (self, button):
        """ Function doc """
        tree = self.builder.get_object('treeview1')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        
        if iter != None:
            jobID       = str(model.get_value(iter, 0))
            
            
            self.MASTERSSession.MessageDialogQuestion.format_secondary_text("Delete the selected project - "+jobID+"?")
            a = self.MASTERSSession.MessageDialogQuestion.run()  # possible "a" valors                                                           
            self.MASTERSSession.MessageDialogQuestion.hide()                                                                  
            # -8  -  yes   
            # -9  -  no    
            # -4  -  close 
            # -5  -  OK                                                                                                       
            # -6  -  Cancel                                                                                                   
            if a == -8:
                self.MASTERSSession.DeleteProject(jobID)
                buff = self.MASTERSSession.text_view.get_buffer()
                buff.set_text("")
                self.AddProjectHistoryToTreeview()
    
    #--------------------BUTTONS---------------------#

    def on_button_select_project_clicked(self, button):
        """ Function doc """
        tree          = self.builder.get_object('treeview1')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        
        if iter != None:
            pymol_object  = model.get_value(iter, 2)  # @+
            projectID     = model.get_value(iter, 0)  # @+
            self.MASTERSSession.ActivedProject = projectID
            
            project  =  self.MASTERSSession.projects[projectID]
            
            self.MASTERSSession.AddJobHistoryToTreeview()
            
            self.MASTERSSession.spinbutton_minX.set_value(int(project['Cell']['minX']))
            self.MASTERSSession.spinbutton_minY.set_value(int(project['Cell']['minY']))
            self.MASTERSSession.spinbutton_minZ.set_value(int(project['Cell']['minZ']))
            self.MASTERSSession.spinbutton_maxX.set_value(int(project['Cell']['maxX']))
            self.MASTERSSession.spinbutton_maxY.set_value(int(project['Cell']['maxY']))
            self.MASTERSSession.spinbutton_maxZ.set_value(int(project['Cell']['maxZ'])) 
        
        
        
        
        

def main():
    dialog = ProjectChooserDialog()
    dialog.dialog.run()
    return 0

if __name__ == '__main__':
	main()

