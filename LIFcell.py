from neuron import h
h.load_file('stdrun.hoc') # load standard run library to give high-level simulation control functions

class LIFcell:
    def __init__(self,gid):
        self._gid = gid; # global id of this cell
        self.soma = h.Section(name='soma',cell=self)  # create soma section
        self._setup_morphology()
        self._setup_biophysics()
        self._setup_recordings()

    def _setup_morphology(self):        
        self.soma.L = 20 # um
        self.soma.diam = 20 # um
    
    def _setup_biophysics(self):        
        self.soma.cm = 1 # uF/cm2
        self.soma.insert('pas') # insert passive conductance
        self.soma.g_pas = 1/33e3 # S/cm^2
        self.soma.e_pas = -65 # mV reversal (and rest) potential
        self.soma.nseg = 1
        self.spkout = h.SpikeOut(self.soma(0.5))
        h.thresh_SpikeOut = -40	# (mV)
        h.refrac_SpikeOut = 4 # (ms)
        h.vrefrac_SpikeOut = self.soma.e_pas # (mV) reset potential
        h.grefrac_SpikeOut = 100 # (uS) clamped at reset
    
    def _setup_recordings(self):
        self._spike_detector = h.NetCon(self.spkout,None)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)
        self.soma_v = h.Vector().record(self.soma(0.5)._ref_v) # Vm vector
        self.t = h.Vector().record(h._ref_t) # time vector

    def __repr__(self):
        return 'LIF[{}]'.format(self._gid)
