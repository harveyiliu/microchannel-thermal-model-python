from thermal_properties import ThermalMaterial
from thermal_properties import Coolant
import math

class Microchannel:
    """Microchannel class with properties"""
    
    def __init__(self, name, microchannelProperties = None):
        self.name = name
        if microchannelProperties == None:
            if name.lower() == ('LSLaserBackplane').lower():
                self.channelWidth = 0.305       # channel width [mm]
                self.channelHeight = 2.032      # channel height [mm]
                self.channelLength = 4.1        # channel length [cm]
                self.baseThickness = 0.5        # base thickness [mm]
                self.wallThickness = 0.305      # wall thickness [mm]
                self.numSplits = 2              # number of splits
                self.numChannelsPerSplit = 24   # number of channels per split
                self.sourceWidth = 3.0          # heat source width [cm]
                self.sourceArea = 15.0          # heat source area[cm2]
                self.flowMode = 'constFlow'     # flow mode control, constant flow rate or pressure
                self.flowRate = 1000            # flow rate for constant flow mode [ccm]
                self.pressure = 0.8             # pressure drop for constant pressure mode [psi]
                self.headloss = 10              # headloss number
                self.nuInf = 6                  # fully developed Nusselt number
                self.thermalMaterial = ThermalMaterial('Cu')
                self.coolant = Coolant('EGW', {'coolantT':20, 'flowRate':1000, 'concPercent':20})
            elif name.lower() == ('LSTEColdPlate').lower():
                self.channelWidth = 0.432
                self.channelHeight = 0.508
                self.channelLength = 3.025
                self.baseThickness = 0.5
                self.wallThickness = 0.432
                self.numSplits = 4
                self.numChannelsPerSplit = 25
                self.sourceWidth = 2.5
                self.sourceArea = 25.0
                self.flowMode = 'constFlow'
                self.flowRate = 150
                self.pressure = 0.3
                self.headloss = 6
                self.nuInf = 6
                self.thermalMaterial = ThermalMaterial('Cu')
                self.coolant = Coolant('EGW', {'coolantT':5, 'flowRate':150, 'concPercent':20})
            elif name.lower() == ('LSTEHotPlate').lower():
                self.channelWidth = 0.305
                self.channelHeight = 1.778
                self.channelLength = 2.469
                self.baseThickness = 0.5
                self.wallThickness = 0.305
                self.numSplits = 2
                self.numChannelsPerSplit = 25
                self.sourceWidth = 2.5
                self.sourceArea = 12.5
                self.flowMode = 'constFlow'
                self.flowRate = 1000
                self.pressure = 0.6
                self.headloss = 5
                self.nuInf = 6
                self.thermalMaterial = ThermalMaterial('Cu')
                self.coolant = Coolant('EGW', {'coolantT':20, 'flowRate':1000, 'concPercent':20})
            elif name.lower() == ('LSEpiTip').lower():
                self.channelWidth = 0.254
                self.channelHeight = 1.778
                self.channelLength = 4.801
                self.baseThickness = 0.254
                self.wallThickness = 0.254
                self.numSplits = 1
                self.numChannelsPerSplit = 8
                self.sourceWidth = 0.4
                self.sourceArea = 1.92
                self.flowMode = 'constFlow'
                self.flowRate = 150
                self.pressure = 2.0
                self.headloss = 10
                self.nuInf = 6
                self.thermalMaterial = ThermalMaterial('Cu')
                self.coolant = Coolant('EGW', {'coolantT':5, 'flowRate':150, 'concPercent':20})
            else:
                self.channelWidth = None
                self.channelHeight = None
                self.channelLength = None
                self.baseThickness = None
                self.wallThickness = None
                self.numSplits = None
                self.numChannelsPerSplit = None
                self.sourceWidth = None
                self.sourceArea = None
                self.flowMode = None
                self.flowRate = None
                self.pressure = None
                self.headloss = None
                self.nuInf = None
                self.thermalMaterial = None
                self.coolant = None
        else:
            self.channelWidth = microchannelProperties['channelWidth']
            self.channelHeight = microchannelProperties['channelHeight']
            self.channelLength = microchannelProperties['channelLength']
            self.baseThickness = microchannelProperties['baseThickness']
            self.wallThickness = microchannelProperties['wallThickness']
            self.numSplits = microchannelProperties['numSplits']
            self.numChannelsPerSplit = microchannelProperties['numChannelsPerSplit']
            self.sourceWidth = microchannelProperties['sourceWidth']
            self.sourceArea = microchannelProperties['sourceArea']
            self.flowMode = microchannelProperties['flowMode']
            self.flowRate = microchannelProperties['flowRate']
            self.pressure = microchannelProperties['pressure']
            self.headloss = microchannelProperties['headloss']
            self.nuInf = microchannelProperties['nuInf']
            self.thermalMaterial = ThermalMaterial(microchannelProperties['thermalMaterialName'])
            self.coolant = Coolant(microchannelProperties['coolantName'], {'coolantT':microchannelProperties['coolantT'], 'flowRate':microchannelProperties['flowRate'], 'concPercent':microchannelProperties['concPercent']})

    def calc_channel_perf(self):
        # CalcCalcObj sets up the microchannel system and calculate the performance
        # The calculations are based on a set of equations given in D. Tukerman's IEEE paper
        # on VLSI microchannel designs.
        
        # set up the coolant parameters
        self.coolant.flowRate = self.flowRate
        
        # obtain channel parameters
        wc = self.channelWidth		# channel width [mm]
        zc = self.channelHeight     # channel height [mm]
        Lc = self.channelLength  	# channel length [mm]
        nsp = self.numSplits		# number of splits
        nc = self.numChannelsPerSplit   # number of channels per split
        ws = self.sourceWidth*10		# total source width [mm]
        As = self.sourceArea		    # total source area [cm2]
        zb = self.baseThickness		    # base thickness [mm]
        ww = self.wallThickness         # wall thickness [mm]
        kw = self.thermalMaterial.k		# wall conductivity [W/C-cm]
        
        # obtain fluid parameters
        f = self.flowRate			# flow rate [ccm]
        P = self.pressure			# flow pressure [psi]
        Ph = self.headloss			# pressure head loss
        kf = self.coolant.k         # fluid thermal conductivity [W/C-cm]
        mu = self.coolant.mu		# viscosity [N-s/cm2]
        rho = self.coolant.rho	    # density [g/cm^3]
        cp = self.coolant.cp		# heat capacity [J/g-C]
        NuInf = self.nuInf		    # fully developed Nusselt number
        fMode = self.flowMode       # flow mode, constant 'constFlow' or 'constPressure'
        
        #Calculate flow parameters
        Pr = (mu*1e4)*(cp*1e3)/(kf*1e2)		# Prandtl number
        D = 4*wc*zc/(2*(zc + wc))			# channel characteristic width [mm]
        
        B = (math.pi*(D**2)/4)/(wc*zc)		# cross section shape factor for calculating pressure drop
        C = 16*math.exp(0.294*(B**2) + 0.068*B - 0.318)      # fRe, C factor in calculating pressure drop
        c1 = Ph*(rho*1e3)/2		# coefficient due to pressure head loss
        c2 = (2*C*(mu*1e4)*(Lc*1e-3))/((D*1e-3)**2)		# coefficient due to laminar flow pressure
        if fMode.lower() == ('constPressure'):      # constant pressure case
            if c1 == 0:
                v = 1e2*((P/1.4504e-4)/c2)
            else:
                # mean flow velocity for a constant pressure [cm/s]
                v = 1e2*((-c2 + (c2**2 + 4*c1*(P/1.4504e-4))**0.5)/(2*c1))
                
                f = 60*v*(nsp*nc*wc*zc*1e-2)		# flow rate [ccm]
        else:       # constant flow rate case
            v = (f/60)/(nsp*nc*wc*zc*1e-2)		# mean flow velocity for constant flow rate [cm/s]
            P = 1.4504e-4*(c1*(v*1e-2)**2 + c2*(v*1e-2))

        
        Re = (v*1e-2)*(D*1e-3)*(rho*1e3)/(mu*1e4)		# Reynolds number
        alpha = nsp*nc*(2*zc + wc)*Lc/(As*1e2)			# surface area multiplication factor
        
        DRePr = D*Re*Pr		# D*Re*Pr product [mm]
        NuAvg = NuInf + ((0.0668*DRePr/Lc)/(1 + 0.04*(DRePr/Lc)**(2/3)))		# average Nusselt number
        xCrit = 0.02*DRePr		# critical length for fully developed flow [mm]
        
        h = NuAvg*kf/(D*1e-1)		# convective heat transfer coefficient [W/C-cm^2]
        finN = (zc*1e-1)*(2*h/(kw*(ww*1e-1)))**0.5		# factor for calculating fin efficiency
        finEta = 100*math.tanh(finN)/finN		# fin efficiency [%]

        RConv = 1/(h*alpha*As)			# thermal resistance due to convection [C/W]
        RHeat = 1/(2*rho*cp*(f/60))		# thermal resistance due to fluid heating [C/W]
        RCond = (zb*1e-1)/(kw*As)		# thermal resistance due to source base conduction [C/W]
        RTotal = RConv + RHeat + RCond		# total thermal resistance [C/W]
        
        zcOpt = 10*(1/(2*h/(kw*(ww*1e-1)))**0.5)	# optimum channel height [mm]
        #guessed optimum channel width [mm]
        wcOpt0 = 1e3*2.29*((mu*1e4)*(kf*1e2)*((Lc*1e-3)**2)*NuAvg/((rho*1e3)*(cp*1e3)*(P/1.4504e-4)))**(1/4)

        
        # Load the calculation results
        channelPerf = {}
        channelPerf['RConv'] = RConv
        channelPerf['RHeat'] = RHeat
        channelPerf['RCond'] = RCond
        channelPerf['RTotal'] = RTotal
        channelPerf['alpha'] = alpha
        channelPerf['finEta'] = finEta
        channelPerf['v'] = v
        channelPerf['P'] = P
        channelPerf['f'] = f
        channelPerf['Re'] = Re
        channelPerf['NuAvg'] = NuAvg
        channelPerf['xCrit'] = xCrit

        return channelPerf


