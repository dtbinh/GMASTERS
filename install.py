import gobject
import sys
import glob, math, os




#System
import datetime
import time


#install
# apt-get install openjdk7-jdk
# pip install py4j
# sudo apt-get install openjdk-7-jdk





if not sys.platform.startswith('win'):
	HOME         = os.environ.get('HOME')
else:            
	HOME         = os.environ.get('PYMOL_PATH')
system = True			
answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	



folder         = os.getcwd()
gtkdyn_folder  = folder			


'''
# Debian/Ubuntu/Mint
sudo apt-get install pymol
 
# Fedora
yum install pymol
 
# Gentoo
emerge -av pymol
 
# openSUSE (12.1 and later)
sudo zypper install pymol
 
# CentOS with EPEL
rpm -i http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-5.noarch.rpm
yum --enablerepo=epel install pymol
'''


print "\nChecking GTK and pyGTK"
try:
	import pygtk
	print "pygtk.......................OK"
except:
	print "pygtk.......................Fail"
	print "Please install  pygtk"
	system = False


try:
	import gtk
	print "gtk.........................OK"
except:
	print "gtk.........................Fail"
	print "Please install  gtk"
	system = False


print "\nChecking JSON"

try:
	import json
	print "json........................OK"
except:
	print "json........................Fail"
	print "Please install  json"
	system = False


       #-----------------------------------#
       #                                   #
       #               PYMOL               #
       #                                   #
       #-----------------------------------#

#Checking PyMOL
#----------------------------------------------------------------------------------------#
print "\nChecking PyMOL"                                                                 #
try:                                                                                     #
	import pymol                                                                         #
	print "PyMOL.......................OK"                                               #
except:                                                                                  #
	print "PyMOL.......................Fail"                                             #
	print "Please install PyMOL"                                                         #
	                                                                                     #
	s = raw_input('\nWould like install PyMOL - Ubuntu/Debian/Mint users only - (Y/n):') #
	if s in answer:                                                                      #
		try:                                                                             #
			os.system("sudo apt-get install pymol")                                      #
		except:                                                                          #
			pass 	                                                                     #
	else:                                                                                #
		system = False                                                                   #
#----------------------------------------------------------------------------------------#









       #-----------------------------------#
       #                                   #
       #             python-pip,           #
       #                 py4j              #
       #                and                #
       #            openjdk-7-jdk          #
       #                                   #
       #-----------------------------------#

print "\nInstalling python-pip and py4j"                                 
try:
    from py4j.java_gateway import JavaGateway
    print "py4j........................OK"                                              

except:
    print "py4j........................Fail"                                            
	
    s = raw_input('\nWould like install py4j - Ubuntu/Debian/Mint users only - (Y/n):') 
	
    if s in answer:                                                                     
        try:      
            os.system("sudo apt-get install python-pip")
            os.system("sudo pip install py4j")
        except:
            pass
    else:                                                                               
		system = False 
        
try:
    print "\nInstalling openjdk-7-jdk"                                 
    os.system("sudo apt-get install openjdk-7-jdk")
except:
    pass






       #-----------------------------------#
       #                                   #
       #             matplotlib            #
       #                                   #
       #-----------------------------------#

#Checking matplotlib
#----------------------------------------------------------------------------------------------#
print "\nChecking matplotlib"                                                                  #
try:                                                                                           #
	from matplotlib import *                                                                   #
	print "matplotlib..................OK"                                                     #
except:                                                                                        #
	print "matplotlib..................Fail"                                                   #
	print "Please install matplotlib"                                                          #
	                                                                                           #
	s = raw_input('\nWould like install matplotlib - Ubuntu/Debian/Mint users only - (Y/n):')  #
	if s in answer:                                                                            #
		try:                                                                                   #
			os.system("sudo apt-get install python-matplotlib")                                #
		except:                                                                                #
			pass 	                                                                           #
	else:                                                                                      #
		system = False                                                                         #
#----------------------------------------------------------------------------------------------#




       #--------------------------------#
       #                                #
       #             MASTERS            #
       #                                #
       #--------------------------------#
"""
if system == True:
	os.chdir(gtkdyn_folder)
	folder = gtkdyn_folder
	sh_MASTERS_root           = "MASTERS_ROOT="
	sh_extport_MASTERS_root   = " ; export MASTERS_ROOT"
	csh_MASTERS_root          = "setenv MASTERS_ROOT " 

	# creating the environment file
	try:
		# SH
		arq  = open(os.path.join("environment_bash.com"), "w")
		text = ""
		text = text + '''#!/bin/bash \n\n# . Bash environment variables and paths to be added to a user's ".bash_profile" file.\n# . Some modifications may be necessary to work properly (e.g. MASTERS_ROOT and PYTHONPATH).\n\n'''
		text = text + sh_MASTERS_root + folder + sh_extport_MASTERS_root
		arq.writelines(text)
		arq.close()
		print "\n\n"
		print "creating the file: environment_bash.com"
		
		#CSH
		arq  = open(os.path.join("environment_cshell.com"), "w")
		text = ""
		text = text + '''#!/bin/bash\n\n# . Cshell environment variables and paths to be added to a user's ".cshrc" file.\n# . Some modifications may be necessary to work properly (e.g. MASTERS_ROOT and PYTHONPATH).\n\n'''
		text = text + csh_MASTERS_root + folder 
		arq.writelines(text)
		arq.close()
		print "creating the file: environment_cshell.com"

	except:
		print "Fail, trying to build the environment file: permission denied"


	# Editing bashrc file and chsrc
	if not sys.platform.startswith('win'):
		HOME         = os.environ.get('HOME')
	else:            
		HOME         = os.environ.get('PYMOL_PATH')

	try:
		#bashrc
		answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	
		s = raw_input('\nWould like to auto add information to the .bashrc file? -MASTERS- (Y/n):')
		
			
		text = "\n#MASTERS \n"
		text = text + "source " + folder + "/environment_bash.com\n"
		text = text + "alias MASTERS='" + folder +"/GTKPyMOL.py'\n"
		text = text + "export LC_ALL=en_US.UTF-8\n"		
		text = text + "export LANG=en_US.UTF-8\n"	
		text = text + "export LANGUAGE=en_US.UTF-8\n"	
		
		
		
		
		if s in answer:
			arq  = open(os.path.join(HOME +"/.bashrc"), "a")
			arq.writelines(text)
			arq.close()
			print "The .bashrc file has been modified"
			print "obs:if you are using CSH please do it manually"

		else:
			print "\n\nPlease add to the .bashrc the following lines:"
			print text
			print "\n\nobs:if you are using CSH please do it manually"
	except:
		print "Fail, trying to build the environment file: permission denied"

	try:
		os.system("chmod +x GTKPyMOL.py")
	except:
		pass


	
	print "\n - - - Installation successful - - - \n"
	print '          "Happy simulating :)"          \n\n'

else:
	print "\n - - - Installation failed - - - \n"
"""	
	
    
try:
    print "Building masters gateway"
    os.system("./build_masters_gateway.sh")
except:
	pass		


print "\n\n         - - - Instalation complete - - - "
print "\nplease  type 'python MastersMain.py' to run MASTERS-GUI"

	
	
	
	
	
	
	
	
	
