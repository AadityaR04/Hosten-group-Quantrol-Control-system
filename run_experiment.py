from artiq.experiment import *

from numpy import linspace

class run_experiment(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('urukul0_cpld')
        self.setattr_device('urukul0_ch0')
        self.setattr_device('urukul0_ch1')
        self.setattr_device('urukul0_ch2')
        self.setattr_device('urukul0_ch3')
        self.setattr_device('urukul1_cpld')
        self.setattr_device('urukul1_ch0')
        self.setattr_device('urukul1_ch1')
        self.setattr_device('urukul1_ch2')
        self.setattr_device('urukul1_ch3')
        self.setattr_device('urukul2_cpld')
        self.setattr_device('urukul2_ch0')
        self.setattr_device('urukul2_ch1')
        self.setattr_device('urukul2_ch2')
        self.setattr_device('urukul2_ch3')
        self.setattr_device('ttl0')
        self.setattr_device('ttl1')
        self.setattr_device('ttl2')
        self.setattr_device('ttl3')
        self.setattr_device('ttl4')
        self.setattr_device('ttl5')
        self.setattr_device('ttl6')
        self.setattr_device('ttl7')
        self.setattr_device('ttl8')
        self.setattr_device('ttl9')
        self.setattr_device('ttl10')
        self.setattr_device('ttl11')
        self.setattr_device('ttl12')
        self.setattr_device('ttl13')
        self.setattr_device('ttl14')
        self.setattr_device('ttl15')
        self.setattr_device('zotino0')
        self.a = linspace(11.000000, 25.000000, 10)

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        self.zotino0.init()
        self.urukul0_cpld.init()
        self.urukul0_ch0.init()
        self.urukul0_ch1.init()
        self.urukul0_ch2.init()
        self.urukul0_ch3.init()
        self.urukul1_cpld.init()
        self.urukul1_ch0.init()
        self.urukul1_ch1.init()
        self.urukul1_ch2.init()
        self.urukul1_ch3.init()
        self.urukul2_cpld.init()
        self.urukul2_ch0.init()
        self.urukul2_ch1.init()
        self.urukul2_ch2.init()
        self.urukul2_ch3.init()
        delay(5*s)
        for a in self.a:
            #Edge number 0 name of edge: Default
            self.ttl0.off()
            self.ttl1.off()
            self.ttl2.off()
            self.ttl3.off()
            self.ttl4.off()
            self.ttl5.off()
            self.ttl6.off()
            self.ttl7.off()
            delay(5*ms)
            self.ttl8.on()
            self.ttl9.off()
            self.ttl10.off()
            self.ttl11.off()
            self.ttl12.off()
            self.ttl13.off()
            self.ttl14.off()
            self.ttl15.off()
            self.zotino0.write_dac(0, 0)
            self.zotino0.write_dac(1, 0)
            self.zotino0.write_dac(2, 0)
            self.zotino0.write_dac(3, 0)
            self.zotino0.write_dac(4, 0)
            self.zotino0.write_dac(5, 0)
            self.zotino0.write_dac(6, 0)
            self.zotino0.write_dac(7, 0)
            self.zotino0.write_dac(8, 0)
            self.zotino0.write_dac(9, 0)
            self.zotino0.write_dac(10, 0)
            self.zotino0.write_dac(11, 0)
            self.zotino0.write_dac(12, 0)
            self.zotino0.write_dac(13, 0)
            self.zotino0.write_dac(14, 0)
            self.zotino0.write_dac(15, 0)
            self.zotino0.write_dac(16, 0)
            self.zotino0.write_dac(17, 0)
            self.zotino0.write_dac(18, 0)
            self.zotino0.write_dac(19, 0)
            self.zotino0.write_dac(20, 0)
            self.zotino0.write_dac(21, 0)
            self.zotino0.write_dac(22, 0)
            self.zotino0.write_dac(23, 0)
            self.zotino0.write_dac(24, 0)
            self.zotino0.write_dac(25, 0)
            self.zotino0.write_dac(26, 0)
            self.zotino0.write_dac(27, 0)
            self.zotino0.write_dac(28, 0)
            self.zotino0.write_dac(29, 0)
            self.zotino0.write_dac(30, 0)
            self.zotino0.write_dac(31, 0)
            self.zotino0.load()
            self.urukul0_ch0.set_att(0.0*dB) 
            self.urukul0_ch0.set(frequency = 226.73083*MHz, amplitude = 0.9, phase = 0.0)
            self.urukul0_ch0.sw.on() 
            self.urukul0_ch1.set_att(0.5*dB) 
            self.urukul0_ch1.set(frequency = 386.605*MHz, amplitude = 0.3, phase = 0.0)
            self.urukul0_ch1.sw.on() 
            self.urukul0_ch2.set_att(0.5*dB) 
            self.urukul0_ch2.set(frequency = 182.65869*MHz, amplitude = 0.3, phase = 0.0)
            self.urukul0_ch2.sw.on() 
            self.urukul0_ch3.set_att(0.0*dB) 
            self.urukul0_ch3.set(frequency = 80.0*MHz, amplitude = 0.2, phase = 0.0)
            self.urukul0_ch3.sw.on() 
            self.urukul1_ch0.set_att(0.0*dB) 
            self.urukul1_ch0.set(frequency = 80.0*MHz, amplitude = 0.4, phase = 0.0)
            self.urukul1_ch0.sw.on() 
            self.urukul1_ch1.set_att(0.0*dB) 
            self.urukul1_ch1.set(frequency = 80.0*MHz, amplitude = 0.2, phase = 0.0)
            self.urukul1_ch1.sw.on() 
            self.urukul1_ch2.set_att(0.0*dB) 
            self.urukul1_ch2.set(frequency = 80.0*MHz, amplitude = 0.2, phase = 0.0)
            self.urukul1_ch2.sw.on() 
            self.urukul1_ch3.set_att(0.0*dB) 
            self.urukul1_ch3.set(frequency = 80.0*MHz, amplitude = 0.25, phase = 0.0)
            self.urukul1_ch3.sw.on() 
            self.urukul2_ch0.set_att(0.0*dB) 
            self.urukul2_ch0.set(frequency = 80.0*MHz, amplitude = 0.2, phase = 0.0)
            self.urukul2_ch0.sw.on() 
            self.urukul2_ch1.set_att(0.0*dB) 
            self.urukul2_ch1.set(frequency = 0.0*MHz, amplitude = 0.0, phase = 0.0)
            self.urukul2_ch1.sw.off() 
            self.urukul2_ch2.set_att(0.0*dB) 
            self.urukul2_ch2.set(frequency = 0.0*MHz, amplitude = 0.0, phase = 0.0)
            self.urukul2_ch2.sw.off() 
            self.urukul2_ch3.set_att(0.0*dB) 
            self.urukul2_ch3.set(frequency = 0.0*MHz, amplitude = 0.0, phase = 0.0)
            self.urukul2_ch3.sw.off() 
            #Edge number 1 name of edge: b
            delay((2)*ms)
            self.ttl1.on()
            self.zotino0.write_dac(1, 4)
            self.zotino0.load()
            #Edge number 2 name of edge: c
            delay((1)*ms)
            self.ttl2.on()
            self.zotino0.write_dac(2, 6)
            self.zotino0.load()
            #Edge number 3 name of edge: d
            delay((1)*ms)
            self.ttl3.on()
            self.zotino0.write_dac(3, 8)
            self.zotino0.load()
            #Edge number 4 name of edge: a
            delay(((a)-(4))*ms)
            self.ttl0.on()
            self.zotino0.write_dac(0, 2)
            self.zotino0.load()
