THERMAL_MATERIAL_JSON_FILE_NAME = 'thermal_constants_21c.json'


class Coolant:
    """Coolant class with properties"""
    
    def __init__(self, name, coolantProperties = {'coolantT':25, 'flowRate':1000, 'concPercent':20}):
        self.name = name
        if len(coolantProperties) > 3:
            self.rho = coolantProperties['rho']     # density (g/cm3)
            self.k = coolantProperties['k']         # thermal conductivity (W/cm-K)
            self.cp = coolantProperties['cp']       # specific heat capacity (J/g-C)
            self.mu = coolantProperties['mu']       # viscosity (N-s/cm2)
            self.fzT = coolantProperties['fzT']     # freezing temperature (C)
            self.coolantT = coolantProperties['coolantT']   # coolant temperature (C)
            self.flowRate = coolantProperties['flowRate']   # coolant flow rate
            self.flowUnit = coolantProperties['flowUnit']   # cooolant flow rate unit
        else:
            self.coolantT = coolantProperties['coolantT']
            self.flowRate = coolantProperties['flowRate']
            if name.lower() == 'air':
                self.rho = get_air_rho(self.coolantT)
                self.k = get_air_k(self.coolantT)
                self.cp = get_air_cp(self.coolantT)
                self.mu = get_air_mu(self.coolantT)
                self.fzT = -273
                self.flowUnit = 'cfm'
            elif name.lower() == 'water':
                self.rho = get_water_rho(self.coolantT)
                self.k = get_water_k(self.coolantT)
                self.cp = get_water_cp(self.coolantT)
                self.mu = get_water_mu(self.coolantT)
                self.fzT = 0
                self.flowUnit = 'ccm'
            elif name.lower() == 'egw':
                self.concPercent = coolantProperties['concPercent']      # concentration %
                self.rho = get_egw_rho(self.coolantT, self.concPercent)
                self.k = get_egw_k(self.coolantT, self.concPercent)
                self.cp = get_egw_cp(self.coolantT, self.concPercent)
                self.mu = get_egw_mu(self.coolantT, self.concPercent)
                self.fzT = get_egw_fzt(self.concPercent)
                self.flowUnit = 'ccm'
            else:
                self.rho = None
                self.k = None
                self.cp = None
                self.mu = None
                self.fzT = None
                self.flowUnit = None

    def calc_flow_rth(self):
        #calculate the flow thermal resistance in (C/W)
        r = max(self.flowRate, 1e-6)
        if self.flowUnit.lower() == 'cfm':
            r = r*(12*2.54)**3
        flowRth = 1/((r/60)*self.rho*self.cp)
        return flowRth





def interp1d(x, y, xi):
    if xi <= x[0]:
        yi = y[0]
    elif xi >= x[len(x) - 1]:
        yi = y[len(x) - 1]
    else:
        xn = (xj for xj in x if xj > xi).next()
        n = x.index(xn)
        yi = y[n] - ((y[n] - y[n-1])/(x[n] - x[n-1]))*(x[n] - xi)
    return yi


def get_air_rho(coolantT):
# The following data are from Introduction to Heat Transfer Table A.4, pg. 757
    x = [250, 300, 350, 400]
    y = [1.3947, 1.1614, 0.9950, 0.8711]
    xi = coolantT + 273
    yi = interp1d(x, y, xi)*1e-3
    return yi

def get_air_k(coolantT):
    # The following data are from Introduction to Heat Transfer Table A.4, pg. 757
    x = [250, 300, 350, 400]
    y = [22.3, 26.3, 30.0, 33.8]
    xi = coolantT + 273
    yi = interp1d(x, y, xi)*1e-5
    return yi


def get_air_cp(coolantT):
    # The following data are from Introduction to Heat Transfer Table A.4, pg. 757
    x = [250, 300, 350, 400]
    y = [1.006, 1.007, 1.009, 1.014]
    xi = coolantT + 273
    yi = interp1d(x, y, xi)
    return yi


def get_air_mu(coolantT):
    # The following data are from Introduction to Heat Transfer Table A.4, pg. 757
    x = [250, 300, 350, 400]
    y = [159.6, 184.6, 208.2, 230.1]
    xi = coolantT + 273
    yi = interp1d(x, y, xi)*1e-11
    return yi

def get_water_rho(coolantT):
    # The following data are from Introduction to Heat Transfer Table A.6, pg. 764
    x = [273.15, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320]
    y = [1.000, 1.000, 1.000, 1.000, 1.001, 1.002, 1.003, 1.005, 1.007, 1.009, 1.011]
    yinv = []
    for yn in y:
        yinv.append(1.0/yn)
    xi = coolantT + 273
    yi = interp1d(x, yinv, xi)
    return yi

def get_water_k(coolantT):
    # The following data are from Introduction to Heat Transfer Table A.6, pg. 764
    x = [273.15, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320]
    y = [569, 574, 582, 590, 598, 606, 613, 620, 628, 634, 640]
    xi = coolantT + 273
    yi = interp1d(x, y, xi)*1e-5
    return yi


def get_water_cp(coolantT):
    # The following data are from Introduction to Heat Transfer Table A.6, pg. 764
    x = [273.15, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320]
    y = [4.217, 4.211, 4.198, 4.189, 4.184, 4.181, 4.179, 4.178, 4.178, 4.179, 4.180]
    xi = coolantT + 273
    yi = interp1d(x, y, xi)
    return yi


def get_water_mu(coolantT):
    # The following data are from Introduction to Heat Transfer Table A.6, pg. 764
    x = [273.15, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320]
    y = [1750, 1652, 1422, 1225, 1080, 959, 855, 769, 695, 631, 577]
    xi = coolantT + 273
    yi = interp1d(x, y, xi)*1e-10
    return yi


def get_egw_rho(coolantT, concPercent):
    # The following data are from the Handbook of Tables for Applied Engineering Science
    # (pg. 96, Table 1-51. Antifreeze Solutions)
    x = [10, 20, 30, 40, 50]
    y = [1.012, 1.025, 1.040, 1.055, 1.065]
    yi = interp1d(x, y, concPercent)
    return yi

def get_egw_k(coolantT, concPercent):
    # The following data are from the Handbook of Tables for Applied Engineering Science
    # (pg. 96, Table 1-51. Antifreeze Solutions)
    x = [10, 20, 30, 40, 50]
    y0 = [0.32, 0.30, 0.28, 0.26, 0.24]     # k vs concentration at 0 degree C
    y20 = [0.33, 0.31, 0.28, 0.26, 0.24]     # k vs concentration at 20 degree C
    yi0 = interp1d(x, y0, concPercent)*1.7296/100
    yi20 = interp1d(x, y20, concPercent)*1.7296/100
    x = [0, 20]
    y = [yi0, yi20]
    yi = interp1d(x, y, coolantT)
    return yi


def get_egw_cp(coolantT, concPercent):
    # The following data are from the Handbook of Tables for Applied Engineering Science
    # (pg. 96, Table 1-51. Antifreeze Solutions)
    x = [10, 20, 30, 40, 50]
    y0 = [0.96, 0.93, 0.87, 0.81, 0.76]     # cp vs concentration at 0 degree C
    y20 = [0.97, 0.94, 0.89, 0.84, 0.79]     # cp vs concentration at 20 degree C
    yi0 = interp1d(x, y0, concPercent)*4.184
    yi20 = interp1d(x, y20, concPercent)*4.184
    x = [0, 20]
    y = [yi0, yi20]
    yi = interp1d(x, y, coolantT)
    return yi


def get_egw_mu(coolantT, concPercent):
    # The following data are from the Handbook of Tables for Applied Engineering Science
    # (pg. 96, Table 1-51. Antifreeze Solutions)
    x = [10, 20, 30, 40, 50]
    y0 = [2.5, 3.0, 4.0, 5.3, 8.0]     # mu vs concentration at 0 degree C
    y20 = [1.4, 1.9, 2.4, 3.1, 4.1]     # mu vs concentration at 20 degree C
    yi0 = interp1d(x, y0, concPercent)*1e-7
    yi20 = interp1d(x, y20, concPercent)*1e-7
    x = [0, 20]
    y = [yi0, yi20]
    yi = interp1d(x, y, coolantT)
    return yi


def get_egw_fzt(concPercent):
    # The following data are from the Handbook of Tables for Applied Engineering Science
    # (pg. 96, Table 1-51. Antifreeze Solutions)
    x = [10, 20, 30, 40, 50]
    yF = [24, 15, 4, -12, -32]
    y = []
    for tF in yF:
        y.append((tF - 32)*(5/9))
    yi = interp1d(x, y, concPercent)
    return yi



class ThermalMaterial:
    """Thermal material class with thermal properties"""
    
    def __init__(self, name, thermalProperties = None):
        if thermalProperties == None:
            import json
        
            try:
                with open(THERMAL_MATERIAL_JSON_FILE_NAME, 'r') as f:
                    dict = json.load(f)
                x = (item for item in dict if item['Name'].lower() == name.lower()).next()
                self.name = x['Name']
                self.rho = x['Density (g/cm3)']
                self.k = x['Thermal Conductivity (W/cm-K)']
                self.cp = x['Specific Heat (J/g-K)']
                self.alpha = x['Linear Expansion (um/cm/C)']
            except:
                self.name = None
                self.rho = None
                self.k = None
                self.cp = None
                self.alpha = None
        else:
            self.name = name
            self.rho = thermalProperties['rho']
            self.k = thermalProperties['k']
            self.cp = thermalProperties['cp']
            self.alpha = thermalProperties['alpha']


def get_material_list():
    import json
            
    try:
        with open(THERMAL_MATERIAL_JSON_FILE_NAME, 'r') as f:
            dict = json.load(f)
        materialList = []
        for item in dict:
            materialList.append(item['Name'])
        materialList.sort()
        return materialList
    except:
        return None










