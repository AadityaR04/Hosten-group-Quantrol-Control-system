import os
   
def create_experiment(self):
    #CREATING A FILE
    file_name = "run_experiment.py"
    if not os.path.exists(file_name):
        with open(file_name, 'w'): pass

    #IMPORT AND BUILD FUNCTIONS
    file = open(file_name,'w')
    indentation = ""
    file.write(indentation + "from artiq.experiment import *\n\n")
    file.write(indentation + "from numpy import linspace\n\n")
    file.write(indentation + "class " + file_name[:-3] + "(EnvExperiment):\n")
    indentation += "    "
    file.write(indentation + "def build(self):\n")
    indentation += "    "
    file.write(indentation + "self.setattr_device('core')\n")
    for _ in range(3):
        file.write(indentation + "self.setattr_device('urukul%d_cpld')\n" %_) 
        for i in range(4):
            file.write(indentation + "self.setattr_device('urukul%d_ch%d')\n" %(_,i)) 
    for _ in range(16):
        file.write(indentation + "self.setattr_device('ttl%d')\n" %_)
    file.write(indentation + "self.setattr_device('zotino0')\n")

    if self.experiment.do_scan:
        #iterating over valid (not "None") scanned variables and creating an array to be used as a collection of names
        var_names = ""
        for_zipping = ""
        for variable in self.experiment.scanned_variables:
            if variable.name != "None":
                file.write(indentation + "self.%s = linspace(%f, %f, %d)\n"%(variable.name, variable.min_val, variable.max_val, self.experiment.step_val))
                var_names += variable.name + ", "
                for_zipping += "self." + variable.name + ", "

    file.write("\n")
    indentation = indentation[:-4]
    file.write(indentation + "@kernel\n")
    file.write(indentation + "def run(self):\n")
    indentation += "    "
    file.write(indentation + "self.core.reset()\n")
    file.write(indentation + "self.core.break_realtime()\n")
    file.write(indentation + "self.zotino0.init()\n")
    file.write(indentation + "self.urukul0_cpld.init()\n")
    file.write(indentation + "self.urukul0_ch0.init()\n")
    file.write(indentation + "self.urukul0_ch1.init()\n")
    file.write(indentation + "self.urukul0_ch2.init()\n")
    file.write(indentation + "self.urukul0_ch3.init()\n")
    file.write(indentation + "self.urukul1_cpld.init()\n")
    file.write(indentation + "self.urukul1_ch0.init()\n")
    file.write(indentation + "self.urukul1_ch1.init()\n")
    file.write(indentation + "self.urukul1_ch2.init()\n")
    file.write(indentation + "self.urukul1_ch3.init()\n")
    file.write(indentation + "self.urukul2_cpld.init()\n")
    file.write(indentation + "self.urukul2_ch0.init()\n")
    file.write(indentation + "self.urukul2_ch1.init()\n")
    file.write(indentation + "self.urukul2_ch2.init()\n")
    file.write(indentation + "self.urukul2_ch3.init()\n")

    if self.experiment.do_scan == True:
        # this delay needs to be optimized. It may depend on scanning parameters as well
        file.write(indentation + "delay(5*s)\n") 
        #making a scanning loop 
        #introduce a flag for multi and single variable scan
        if self.experiment.scanned_variables_count > 1:
            file.write(indentation + "for %s in zip(%s):\n" %(var_names[:-2], for_zipping[:-2]))
        else:
            file.write(indentation + "for %s in %s:\n" %(var_names[:-2], for_zipping[:-2]))        
        indentation += "    "

 
    self.delta_t = 0

    #flag_init is used to indicate that there is no need for a delay calculation for the first row
    flag_init = 0
    for edge in range(self.sequence_num_rows):
        file.write(indentation + "#Edge number " + str(edge) + " name of edge: " + self.experiment.sequence[edge].name + "\n")
        if flag_init == 0:
            flag_init = 1
        else:
            self.delta_t = "(" + str(self.experiment.sequence[edge].for_python) + ")" + "-" + "(" + str(self.experiment.sequence[edge-1].for_python) + ")"
            try: #this try is used to try evaluating the expression. It will only be able to do so in case it is scanned
                print(self.delta_t)
                exec("self.delta_t = " + self.delta_t)
                print("Done")
                print(self.delta_t)
            except:
                pass
        #ADDING A DELAY
        if self.delta_t != 0:
            file.write(indentation + "delay((" + str(self.delta_t) + ")*ms)\n")

        #DIGITAL CHANNEL CHANGES
        for index, channel in enumerate(self.experiment.sequence[edge].digital):
            if edge == 0 and index == 8: #adding a 5 ms delay to make changes into TTL channels
                file.write(indentation + "delay(5*ms)\n")

            if channel.changed == True:
                if channel.value == 1:
                    file.write(indentation + "self.ttl" + str(index) + ".on()\n") 
                else:
                    file.write(indentation + "self.ttl" + str(index) + ".off()\n") 

        #ANALOG CHANNEL CHANGES
        flag_zotino_change_needed = False      
        for index, channel in enumerate(self.experiment.sequence[edge].analog):
            if channel.changed == True:
                flag_zotino_change_needed = True
                file.write(indentation + "self.zotino0.write_dac(%d, " %index)
                file.write(channel.for_python + ")\n")
        if flag_zotino_change_needed:
            file.write(indentation + "self.zotino0.load()\n")

        #DDS CHANNEL CHANGES
        for index, channel in enumerate(self.experiment.sequence[edge].dds):
            if channel.changed == True:
                urukul_num = int(index // 4)
                channel_num = int(index % 4)
                file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set_att(" + str(channel.attenuation.for_python) + "*dB) \n")    
                file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set(frequency = " + str(channel.frequency.for_python) + "*MHz, amplitude = " + str(channel.amplitude.for_python) + ", phase = " + str(channel.phase.for_python) + ")\n")    
                if channel.state.value == 1:
                    file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.on() \n")
                else:
                    file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.off() \n")
                
    file.close()


def create_go_to_edge(self):
    edge = self.sequence_table.selectedIndexes()[0].row()
    self.experiment.go_to_edge = edge
    file_name = "go_to_edge.py"
    if not os.path.exists(file_name):
        with open(file_name, 'w'): pass
    file = open(file_name,'w')
    indentation = ""
    file.write(indentation + "from artiq.experiment import *\n\n")
    file.write(indentation + "class " + file_name[:-3] + "(EnvExperiment):\n")
    indentation += "    "
    file.write(indentation + "def build(self):\n")
    indentation += "    "
    file.write(indentation + "self.setattr_device('core')\n")
    for _ in range(3):
        file.write(indentation + "self.setattr_device('urukul%d_cpld')\n" %_) 
        for i in range(4):
            file.write(indentation + "self.setattr_device('urukul%d_ch%d')\n" %(_,i)) 
    for _ in range(16):
        file.write(indentation + "self.setattr_device('ttl%d')\n" %_)
    file.write(indentation + "self.setattr_device('zotino0')\n")
    file.write("\n")
    indentation = indentation[:-4]
    file.write(indentation + "@kernel\n")
    file.write(indentation + "def run(self):\n")
    indentation += "    "
    file.write(indentation + "self.core.reset()\n")
    file.write(indentation + "self.core.break_realtime()\n")
    file.write(indentation + "self.zotino0.init()\n")
    file.write(indentation + "self.urukul0_cpld.init()\n")
    file.write(indentation + "self.urukul0_ch0.init()\n")
    file.write(indentation + "self.urukul0_ch1.init()\n")
    file.write(indentation + "self.urukul0_ch2.init()\n")
    file.write(indentation + "self.urukul0_ch3.init()\n")
    file.write(indentation + "self.urukul1_cpld.init()\n")
    file.write(indentation + "self.urukul1_ch0.init()\n")
    file.write(indentation + "self.urukul1_ch1.init()\n")
    file.write(indentation + "self.urukul1_ch2.init()\n")
    file.write(indentation + "self.urukul1_ch3.init()\n")
    file.write(indentation + "self.urukul2_cpld.init()\n")
    file.write(indentation + "self.urukul2_ch0.init()\n")
    file.write(indentation + "self.urukul2_ch1.init()\n")
    file.write(indentation + "self.urukul2_ch2.init()\n")
    file.write(indentation + "self.urukul2_ch3.init()\n")
    file.write(indentation + "delay(5*ms)\n")  

    for index, channel in enumerate(self.experiment.sequence[edge].digital):
        if edge == 0 and index == 8: #adding a 5 ms delay to make changes into TTL channels
            file.write(indentation + "delay(5*ms)\n")
        if channel.value == 0:
            file.write(indentation + "self.ttl" + str(index) + ".off()\n")
        elif channel.value == 1:
            file.write(indentation + "self.ttl" + str(index) + ".on()\n")        
    for index, channel in enumerate(self.experiment.sequence[edge].analog):
        file.write(indentation + "self.zotino0.write_dac(%d, %.4f)\n" %(index, channel.value))
    file.write(indentation + "self.zotino0.load()\n")
    for index, channel in enumerate(self.experiment.sequence[edge].dds):
        urukul_num = int(index // 4)
        channel_num = int(index % 4)
        file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set_att(" + str(channel.attenuation.value) + "*dB) \n")    
        file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set(frequency = " + str(channel.frequency.value) + "*MHz, amplitude = " + str(channel.amplitude.value) + ", phase = " + str(channel.phase.value) + ")\n")    
        if channel.state.value == 1:
            file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.on() \n")
        elif channel.state.value == 0:
            file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.off() \n")                

    file.close()