#!/usr/bin/env python
"""
show how to add a matplotlib FigureCanvasGTK or FigureCanvasGTKAgg widget and
a toolbar to a gtk.Window
"""
import gtk

from matplotlib.figure import Figure
from numpy import arange, sin, pi
from pylab import *
# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
#from matplotlib.widgets import Cursor









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



class PlotGTKWindow:
    
    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        key_press_handler(event, self.canvas, self.toolbar)
    
    def on_pick(self, event):
        thisline = event.artist
        xdata, ydata = thisline.get_data()
        ind = event.ind
        print('on pick line:', zip(xdata[ind], ydata[ind]))
        self.ax.plot(xdata[ind], ydata[ind], 'bo', picker=5)

    def __init__ (self, parameters = None):
        """ Function doc """
        self.win = gtk.Window()
        self.win.connect("destroy", lambda x: gtk.main_quit())
        self.win.set_default_size(900,600)
        self.win.set_title("MASTERS plot graph window")

        vbox = gtk.VBox()
        self.win.add(vbox)

        # fig, (ax0, ax1) = plt.subplots(nrows=2)
        # 
        # ax0.plot(x, y)
        # ax0.set_title('normal spines')
        # ax1.plot(x, y)
        # ax1.set_title('bottom-left spines')
        # 
        # # Hide the right and top spines
        # ax1.spines['right'].set_visible(False)
        # ax1.spines['top'].set_visible(False)
        # # Only show ticks on the left and bottom spines
        # ax1.yaxis.set_ticks_position('left')
        # ax1.xaxis.set_ticks_position('bottom')
        
        if parameters == None:
            x = arange(0.0,3.0,0.01)
            y = sin(2*pi*x)
            parameters = {
                         'title' : 'test',
                         'X'     : x     ,
                         'y'     : y     ,
                         'xlabel': 'x\n '   ,
                         'ylabel': '\nsin'
                         }
            
            
        else:
            x  = parameters['model'               ]
            y1 = parameters['acc_director_agents' ]
            y2 = parameters['acc_searching_agents']
            y3 = parameters['energy'              ]
                

        
        f = Figure(figsize=(5, 4), dpi=100)
        
       
        font = {#'family' : 'DejaVu Sans Mono',
                'color'  : 'black',
                'weight' : 'normal',
                'size'   : 12,
                }     
            
        self.ax = f.add_subplot(3, 1, 1)
        #self.ax.set_title('line styles')

        self.ax.plot(x, y1, 'y.-')
        #self.ax.set_xlabel('model')
        self.ax.set_ylabel('Acceptance ratio\ndirector agents (a.u.)', fontdict=font)   
        self.ax.set_xlabel('models' , fontdict=font)

     
        self.ax = f.add_subplot(3, 1, 2)
        self.ax.plot(x, y2, 'r.-', )
        #self.ax.plot(x, y2, linewidth=1, color='black',label='zorder=10',zorder = 10)
        self.ax.set_xlabel('models')
        self.ax.set_ylabel('Acceptance ratio\nsearching agents (a.u.)', fontdict=font)   
        
        
        self.ax = f.add_subplot(3, 1, 3)
        #self.ax.set_title('line styles')

        self.ax.plot(x, y3, 'g.-')
        self.ax.set_xlabel('models' , fontdict=font)
        self.ax.set_ylabel('Energy (a.u.)', fontdict=font)    
                
        f.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.34)        
        
       
        self.canvas = FigureCanvas(f)  # a gtk.DrawingArea
        vbox.pack_start(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self.win)
        vbox.pack_start(self.toolbar, False, False)

        self.win.show_all()
        gtk.main()
    

   
if __name__ == "__main__":
    parameters = ParseOutputLogFile ('/home/labio/Dropbox/mastersGUI/1_MonteCarlo.log')
    PlotGTKWindow = PlotGTKWindow(parameters)
    
