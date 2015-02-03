#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MastersMain.py
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



# System
import datetime
import time
import pygtk
pygtk.require('2.0')

import gtk
import gobject
import sys

import os
import json
from  pprint import pprint

import pango

#------------------------GUI------------------------#
from gui.FileChooserWindow       import FileChooserWindow 
from gui.NewProjectDialog        import NewProjectDialog
from gui.WorkspaceDialog         import WorkspaceDialog
from gui.ProjectChooserDialog    import ProjectChooserDialog
from gui.MonteCarloDialog        import MonteCarloDialog
from modules.MatplotGTK          import PlotGTKWindow, ParseOutputLogFile
from subprocess                  import Popen


#--------------PyMOL--------------#
import pymol
from pymol import *
from pymol.cgo import *


#from MASTERSviewer.MASTERSviewer import MASTERS_main
# Roda o gateway
#p = Popen(['sh', '/home/labio/Documents/NetlogoMasters/MASTERS/run_masters_gateway.sh'])
p = Popen(['sh', 'run_masters_gateway.sh'])
# faz tudo que precisa (todo o resto)


#from WindowControl          import WindowControl
#from MCwindow               import MonteCarloSimulationWindow
#from MastersWorkSpaceDialog import WorkSpaceDialog
#from BoxSetupDialog         import BoxSetupDialog


class MastersMain():


    def __init__(self):
        print '           Intializing MasterGUI object          '
        
        # ------------- MASTERS GUI CONFIG FILE -------------- #
        self.HOME          = os.environ.get('HOME')
        self.configMASTERS = os.path.join(self.HOME, '.config/MASTERS/')
        #------------------------------------------------------#
        path = os.getcwd()
        self.gui  = os.path.join(path, 'gui')
        
        #---------------------------------- MasterGUI --------------------------------#
        self.builder = gtk.Builder()                                                  #
        self.builder.add_from_file(os.path.join(self.gui, "MastersMainWindow.glade")) #
        self.builder.add_from_file(os.path.join(self.gui, "MessageDialogs.glade")) #
        self.builder.add_from_file(os.path.join(self.gui, "MastersAboutDialog.glade")) 
        self.win     = self.builder.get_object("window1")                             #
        self.win.show()                                                               #
        self.builder.connect_signals(self)                                            #
                                                                                      #
        self.text_view = self.builder.get_object("textview1")                         #
        self.text_view.modify_font(pango.FontDescription("monospace 10"))             #
        #-----------------------------------------------------------------------------#

        
        self.projects = {}
        self.selectedID  = None
        #self.selectedObj = None    
    
        #---------------------------------------------------------#
        #                PROJECT HISTORY DATA                     #
        #---------------------------------------------------------#      
        try:
            self.projects = json.load(open(self.configMASTERS + 'ProjectHistory.dat'))
            pprint(self.projects)
        except:
            self.projects = {}
        

        self.ActivedProject = None    
        
        
        #---------------------------------------------------------#
        #                  MASTERS GUI CONFIG                     #
        #---------------------------------------------------------#
        self.GUIConfig = {                              
                       'HideWorkSpaceDialog': False,  
                       'WorkSpace'          : self.HOME,  
                       'History'            : {}   } 
        self.Load_GUI_ConfigFile()
        #---------------------------------------------------------#

        
        #---------------------------------------Dialogs and Windows------------------#
        #self.WindowControl    = WindowControl   (self.builder, self.projects )      #
        self.NewProjectDialog     = NewProjectDialog(self)                           #
        self.WorkSpaceDialog      = WorkspaceDialog (self)                           #
        self.ProjectChooserDialog = ProjectChooserDialog(self)                       #
        self.MessageDialogQuestion= self.builder.get_object('messagedialog_question')#
        self.MessageDialogError   = self.builder.get_object('messagedialog_error')   #
        self.MonteCarloDialog     = MonteCarloDialog(self)
        self.AboutDialog          = self.builder.get_object('aboutdialog')
        #----------------------------------------------------------------------------#


        
        
        adjustment1 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_minX  = self.builder.get_object("spinbutton_minX")
        self.spinbutton_minX.set_adjustment(adjustment1)
        self.spinbutton_minX.update()
        #self.spinbutton_minX.set_value(int(project['Cell']['minX']))

        adjustment2 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_minY  = self.builder.get_object("spinbutton_minY")
        self.spinbutton_minY.set_adjustment(adjustment2)
        self.spinbutton_minY.update()
        #self.spinbutton_minY.set_value(int(project['Cell']['minY']))

        adjustment3 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_minZ  = self.builder.get_object("spinbutton_minZ")
        self.spinbutton_minZ.set_adjustment(adjustment3)
        self.spinbutton_minZ.update()
        #self.spinbutton_minZ.set_value(int(project['Cell']['minZ']))
        
        adjustment4 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_maxX  = self.builder.get_object("spinbutton_maxX")
        self.spinbutton_maxX.set_adjustment(adjustment4)
        self.spinbutton_maxX.update()
        #self.spinbutton_maxX.set_value(int(project['Cell']['maxX']))

        adjustment5 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_maxY  = self.builder.get_object("spinbutton_maxY")
        self.spinbutton_maxY.set_adjustment(adjustment5)
        self.spinbutton_maxY.update()
        #self.spinbutton_maxY.set_value(int(project['Cell']['maxY']))

        adjustment6 = gtk.Adjustment(0.0, -1000.0, 1000.0, 1.0, 0.0, 0.0)
        self.spinbutton_maxZ  = self.builder.get_object("spinbutton_maxZ")
        self.spinbutton_maxZ.set_adjustment(adjustment6)
        self.spinbutton_maxZ.update()
        #self.spinbutton_maxZ.set_value(int(project['Cell']['maxZ'])) 

        
        
        # testing the workspace dialog True/False 
        if self.GUIConfig['HideWorkSpaceDialog'] == False:
            self.WorkSpaceDialog.dialog.run()
            self.WorkSpaceDialog.dialog.hide()

        # if project existis -  open project list
        if self.projects != {}:
            pprint(self.projects)
            self.LoadProjectChooserDialog()
   
        if self.projects == {}:
            self.LoadNewProjectDialog()


        #------------PYMOL----------------#
        self.nonpolarColor = 'green'
        self.polarColor    = 'purple' 
    
    ''' 
        --------------------------------------------------
    
                        GUI CONFIG METHODS
    
        --------------------------------------------------
    ''' 
        
    def Load_GUI_ConfigFile (self, filename = None):
        """ Function doc """
        #.config
        path = os.path.join(self.HOME ,'.config', 'MASTERS', 'GUI.config')
        
        try:
            self.GUIConfig = json.load(open(path)) 
        except:
            print 'error: GUIConfig file not found'
            print 'open WorkSpace Dialog'

    def Save_GUI_ConfigFile(self):
        """ Function doc """
        path = os.path.join(self.HOME,'.config')
        if not os.path.exists (path): 
            os.mkdir (path)

        path = os.path.join(path, 'MASTERS')
        if not os.path.exists (path): 
            os.mkdir (path)
        
        filename = os.path.join(path,'GUI.config')
        json.dump(self.GUIConfig, open(filename, 'w'), indent=2)


    ''' 
        --------------------------------------------------
    
                        GUI METHODS
    
        --------------------------------------------------
    ''' 
    def LoadProjectChooserDialog (self):
        """ Function doc """
        self.ProjectChooserDialog.AddProjectHistoryToTreeview()
        self.ProjectChooserDialog.dialog.run()
        self.ProjectChooserDialog.dialog.hide()

    def LoadNewProjectDialog (self):
        """ Function doc """
        self.NewProjectDialog.dialog.run()
        self.NewProjectDialog.dialog.hide()

    def AddJobHistoryToTreeview (self, liststore = None, Jobs = None ):
        #self.ActivedProject = projectID
        try:
            Jobs   = self.projects[self.ActivedProject]['Jobs']
            Folder = self.projects[self.ActivedProject]['Folder']

            liststore = self.builder.get_object("liststore1")
            
            try:
                #self.WindowControl.AddJobHistoryToTreeview(liststore, Jobs)
                model = self.builder.get_object('liststore1')
                model = liststore

                numbers = list(Jobs)      # this is necessary to sorte the Jobs dic
                numbers2 = []
                
                for i in numbers:
                    numbers2.append(int(i))
                numbers2.sort()
                model.clear()
                #print model
                
                for i in numbers2:
                    i = str(i)
                    
                    if Jobs[str(i)]==None:
                        pass
                    else:
                        data = [str(i), Jobs[i]['Type'],Jobs[i]['Start'],Jobs[i]['Status'],Jobs[i]['Energy'],Jobs[i]['LowestEnergyModel'] ]
                        #print i, data
                        model.append(data)
            except:
                pass
            text = 'Project: ' + self.projects[self.ActivedProject]['ProjectName'] + '    Directory:' + Folder
            self.STATUSBAR_SET_TEXT(text)
        
        except:
            model = self.builder.get_object('liststore1')
            model.clear()

    def LoadFileToTextView(self, filename):
        ## add Loading message to status bar and ensure GUI is current
        try:
            fin = open(filename, "r")
            text = fin.read()
            fin.close()
            
            # disable the text view while loading the buffer with the text
            self.text_view.set_sensitive(False)
            buff = self.text_view.get_buffer()
            buff.set_text(text)
            buff.set_modified(False)
            self.text_view.set_sensitive(True)
        except:
            self.text_view.set_sensitive(False)
            buff = self.text_view.get_buffer()
            buff.set_text("Output file not found")
            buff.set_modified(False)
            self.text_view.set_sensitive(True)
            
            
    def DeleteProject (self, projectID):
        """ Function doc """
        self.projects[projectID] = None
        json.dump(self.projects, open(os.path.join(self.configMASTERS ,'ProjectHistory.dat'), 'w'), indent=2)
        self.AddJobHistoryToTreeview()
    
    def DeleteJob (self, jobID):
        """ Function doc """
        if jobID == "0":
            print 'The Initial coordenates can not be removed. Please remove the whole project'
        else:
            self.projects[self.ActivedProject]['Jobs'][str(jobID)] = None
            json.dump(self.projects, open(os.path.join(self.configMASTERS ,'ProjectHistory.dat'), 'w'), indent=2)
            self.AddJobHistoryToTreeview()
            
    def STATUSBAR_SET_TEXT(self, text):
        """ Function doc """
        self.builder.get_object('statusbar1').push(0, text)


    #------------------------------------------------#
    #                   MAIN MENU                    #
    #------------------------------------------------#
    
    def on_imagemenuitem_about_activate(self, menuitem):
        """ Function doc """
        self.AboutDialog.run()
        self.AboutDialog.hide()
    
    #------------------------------------------------#
    #               TOOLBAR  METHODS                 #
    #------------------------------------------------#

    def on_toolbutton_LoadProjectChooserDialog_clicked(self, button):
        """ Function doc """
        self.LoadProjectChooserDialog ()

    def on_toolbutton_NewProject_clicked(self, button):
        self.LoadNewProjectDialog()

    def on_button_DeleteCurrentProject_clicked (self, button):
        """ Function doc """
        if self.ActivedProject == None:
            print 'No project in memory'
            pass
        
        else:
            self.MessageDialogQuestion.format_secondary_text("Delete the selected project - "+self.ActivedProject+"?")
            a = self.MessageDialogQuestion.run()  # possible "a" valors                                                           
            self.MessageDialogQuestion.hide()                                                                  
            # -8  -  yes   
            # -9  -  no    
            # -4  -  close 
            # -5  -  OK                                                                                                       
            # -6  -  Cancel                                                                                                   
            if a == -8:
                self.DeleteProject (self.ActivedProject)
                buff = self.text_view.get_buffer()
                buff.set_text("")
            else:
                pass
    
    def on_toolbutton_DeleteSelectedJob_clicked (self, button):
        """ Function doc """
        tree          = self.builder.get_object('treeview3')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        if iter != None:
            jobID       = str(model.get_value(iter, 0))
            #print jobID
            
            self.MessageDialogQuestion.format_secondary_text("Delete the selected job - "+ jobID + "?")
            a = self.MessageDialogQuestion.run()                                                            
            self.MessageDialogQuestion.hide()                                                               
            # -8  -  yes   
            # -9  -  no    
            # -4  -  close 
            # -5  -  OK                                                              
            # -6  -  Cancel                                                                                           

            if a == -8:
                print jobID
                self.DeleteJob (jobID)
                buff = self.text_view.get_buffer()
                buff.set_text("")
            else:
                pass
        pass

    def on_toolbutton_MonteCarlo_clicked (self, button):
        """ Function doc """
        self.MonteCarloDialog.ImportCellValorsFromProject()
        self.MonteCarloDialog.dialog.run()
        self.MonteCarloDialog.dialog.hide()
    
    def on_toolbutton_loadMASTERSViewer_clicked (self, button):
        """ Function doc """
        MASTERS_main()
        
        
    #------------------------------------------------#
    #               TREEVIEW  METHODS                #
    #------------------------------------------------#         
    def on_treeview3_button_release_event(self, tree, event):
        """ Function doc """
        if event.button == 3:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))
                self.selectedObj = str(model.get_value(iter, 2))

                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedID+' -' )
                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, event.button, event.time)
            
        if event.button == 1:
            #print "Mostrar menu de contexto botao1"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            if iter != None:
                #print model, iter
                JobID         = model.get_value(iter, 0)
                pymol_object  = model.get_value(iter, 2)  # @+
                #print _object
                #pprint (self.projects[self.ActivedProject]['Jobs'][JobID])
                filename = self.projects[self.ActivedProject]['Jobs'][JobID]['Output']
                #print filename
                self.LoadFileToTextView(filename)
            
    
    #------------------------------------------------#
    #                 TREEVIEW MENU                  #
    #------------------------------------------------#
    
    def on_menuitem_plot_graph_activate (self, menuitem):
        """ Function doc """
        tree          = self.builder.get_object('treeview3')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()

        if iter != None:
            #print model, iter
            JobID         = model.get_value(iter, 0)
        
            parameters = ParseOutputLogFile (self.projects[self.ActivedProject]['Jobs'][JobID]['LogFile'])
            _PlotGTKWindow = PlotGTKWindow(parameters)
            
    def run(self):
        gtk.main()


    def on_menuitem_show_model_activate (self, menuitem):
        """ Function doc """
        tree          = self.builder.get_object('treeview3')
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()

        if iter != None:
            #print model, iter
            JobID         = model.get_value(iter, 0)
            self.LoadFileInPyMOL(self.projects[self.ActivedProject]['Jobs'][JobID]['Output'])
        
    def LoadFileInPyMOL (self, filein):
        """ Function doc """
        cmd.load(filein)
        cmd.show("spheres")                               
        cmd.hide('lines')
        cmd.show('ribbon')                                
        cmd.color(self.polarColor)
        
        cmd.select('sele', "resn leu")
        cmd.color(self.nonpolarColor, 'sele')
        
        cmd.select('sele', "resn ala")
        cmd.color(self.nonpolarColor, 'sele')
        
        cmd.select('sele', "resn ile")
        cmd.color(self.nonpolarColor, 'sele')
        
        cmd.select('sele', "resn pro")
        cmd.color(self.nonpolarColor, 'sele')
        
        cmd.select('sele', "resn val")
        cmd.color(self.nonpolarColor, 'sele')
        
        cmd.select('sele', "resn gly")
        cmd.color(self.nonpolarColor, 'sele')
        
        cmd.select('sele', "resn cys")
        cmd.color(self.nonpolarColor, 'sele')
        
        
        
        #cmd.do('select resn leu')
        #cmd.do('color ' + self.nonpolarColor + ', sele')
        #cmd.do('select resn ala')
        #cmd.do('color ' + self.nonpolarColor + ', sele')
        #cmd.do('select resn ile')
        #cmd.do('color ' + self.nonpolarColor + ', sele')
        #cmd.do('select resn pro')
        #cmd.do('color ' + self.nonpolarColor + ', sele')
        #cmd.do('select resn val')
        #cmd.do('color ' + self.nonpolarColor + ', sele')
        #cmd.do('select resn met')
        #cmd.do('color ' + self.nonpolarColor + ', sele')
        #cmd.do('select resn gly')
        #cmd.do('color ' + self.nonpolarColor + ', sele')
        #cmd.do('select resn cys')
        #cmd.do('color ' + self.nonpolarColor + ', sele') 
   
   
    
    
    def on_toolbutton_ShowBox_clicked(self, button):
        """ Function doc """
        if button.get_active():
            self.DrawCell()
        else:
            try:
                cmd.delete("box")
            except:
                pass
    
    def on_spinbutton_change_value2(self, widget, event= None):
        
        if widget == self.builder.get_object("spinbutton_minX"):
            minX  = self.builder.get_object("spinbutton_minX").get_value_as_int()
            self.projects[self.ActivedProject]['Cell']['minX'] = minX
        
        if widget == self.builder.get_object("spinbutton_minY"):
            minY  = self.builder.get_object("spinbutton_minY").get_value_as_int()
            self.projects[self.ActivedProject]['Cell']['minY'] = minY
        
        if widget == self.builder.get_object("spinbutton_minZ"):
            minZ  = self.builder.get_object("spinbutton_minZ").get_value_as_int()
            self.projects[self.ActivedProject]['Cell']['minZ'] = minZ 

        if widget == self.builder.get_object("spinbutton_maxX"):
            maxX  = self.builder.get_object("spinbutton_maxX").get_value_as_int()
            self.projects[self.ActivedProject]['Cell']['maxX'] = maxX 
        
        if widget == self.builder.get_object("spinbutton_maxY"):
            maxY  = self.builder.get_object("spinbutton_maxY").get_value_as_int()
            self.projects[self.ActivedProject]['Cell']['maxY'] = maxY 

        if widget == self.builder.get_object("spinbutton_maxZ"):
            maxZ  = self.builder.get_object("spinbutton_maxZ").get_value_as_int()
            self.projects[self.ActivedProject]['Cell']['maxZ'] = maxZ 
        
        if self.builder.get_object("toolbutton_ShowBox").get_active():
            self.DrawCell()
        
        
        
        
    
    def ChangeCell (self, PyMOL = False):
        """ Function doc """
        minX  = self.builder.get_object("spinbutton_minX").get_value_as_int()
        minY  = self.builder.get_object("spinbutton_minY").get_value_as_int()
        minZ  = self.builder.get_object("spinbutton_minZ").get_value_as_int()
        maxX  = self.builder.get_object("spinbutton_maxX").get_value_as_int()
        maxY  = self.builder.get_object("spinbutton_maxY").get_value_as_int()
        maxZ  = self.builder.get_object("spinbutton_maxZ").get_value_as_int()
        
        self.projects[self.ActivedProject]['Cell']['minX'] = minX 
        self.projects[self.ActivedProject]['Cell']['minY'] = minY 
        self.projects[self.ActivedProject]['Cell']['minZ'] = minZ 
        self.projects[self.ActivedProject]['Cell']['maxX'] = maxX 
        self.projects[self.ActivedProject]['Cell']['maxY'] = maxY 
        self.projects[self.ActivedProject]['Cell']['maxZ'] = maxZ 
        self.DrawCell()
    
    
    def DrawCell (self):
        """ Function doc """
        minX = self.projects[self.ActivedProject]['Cell']['minX']
        minY = self.projects[self.ActivedProject]['Cell']['minY']
        minZ = self.projects[self.ActivedProject]['Cell']['minZ']
        maxX = self.projects[self.ActivedProject]['Cell']['maxX']
        maxY = self.projects[self.ActivedProject]['Cell']['maxY']
        maxZ = self.projects[self.ActivedProject]['Cell']['maxZ']
        
        selection="(all)"
        padding=0.0
        linewidth=2.0
        r=0.0
        g=0.0
        b=0.0
        
        boundingBox = [
                LINEWIDTH, float(linewidth),

                BEGIN, LINES,
                COLOR, float(r), float(g), float(b),

                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, minY, maxZ,       #2

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, minY, maxZ,       #6

                VERTEX, maxX, maxY, minZ,       #7
                VERTEX, maxX, maxY, maxZ,       #8


                VERTEX, minX, minY, minZ,       #1
                VERTEX, maxX, minY, minZ,       #5

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, maxY, maxZ,       #4
                VERTEX, maxX, maxY, maxZ,       #8

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, maxX, minY, maxZ,       #6


                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, maxY, minZ,       #3

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, maxZ,       #6
                VERTEX, maxX, maxY, maxZ,       #8

                END
        ]

        try:
            cmd.delete("box")
        except:
            pass
        
        boxName = "box"
        cmd.set('auto_zoom', 0)
        cmd.load_cgo(boundingBox,boxName)
        #cmd.set_frame(-1)
        
            
    def run(self):
        gtk.main()



def PyMOL_GUIConfig():
    """ Function doc """
    #-------------------- config PyMOL ---------------------#
    pymol.cmd.set("internal_gui", 1)                        #
    pymol.cmd.set("internal_gui_mode", 0)                   #
    pymol.cmd.set("internal_feedback", 1)                   #
    pymol.cmd.set("internal_gui_width", 220)                #
    pymol.cmd.set("cartoon_fancy_helices", 'on')            #  
    pymol.cmd.set('ribbon_sampling', 3)
    sphere_scale = 0.1                                      #
    stick_radius = 0.15                                     #
    label_distance_digits = 4                               #
    mesh_width = 0.3                                        #
    cmd.set('sphere_scale', sphere_scale)                   #
    cmd.set('stick_radius', stick_radius)                   #
    cmd.set('label_distance_digits', label_distance_digits) #
    cmd.set('mesh_width', mesh_width)                       #
    cmd.set("retain_order")         # keep atom ordering    #
    cmd.bg_color("white")            # background color     #
    #cmd.do("set field_of_view, 70")                         #
    cmd.do("set ray_shadows,off")                           #
    #-------------------------------------------------------#

def main():
    pymol.finish_launching()    
    gtk.gdk.threads_init()
    PyMOL_GUIConfig()
    
    masters = MastersMain()
    masters.run()
    #fecha o gateway quando for sair do programa
    p.terminate()
    return 0

if __name__ == '__main__':
	main()
