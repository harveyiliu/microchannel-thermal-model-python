#!/usr/bin/python
import microchannel as mc


if __name__ == "__main__":
    """ Microchannel thermal modeling demo
            Input arguments:
                modelName = predefined model name, current set of models are:
                    1. LSLaserBackplane
                    2. LSTEColdPlate
                    3. LSTEHotPlate
                    4. LSEpiTip
        Run command example:
            ./microchannel_demo.py LSLaserBackplane &      
    """
    
    import sys
    modelName = sys.argv[1]     # MCML model name
    model = mc.Microchannel(modelName)
    channelPerf = model.calc_channel_perf()
    print '\nRTotal (degree C/W): {0:.4f}'.format(channelPerf['RTotal'])
    print 'RConv (degree C/W): {0:.4f}'.format(channelPerf['RConv'])
    print 'RHeat (degree C/W): {0:.4f}'.format(channelPerf['RHeat'])
    print 'RCond (degree C/W): {0:.4f}'.format(channelPerf['RCond'])
    print 'surface area multiplier alpha: {0:.3f}'.format(channelPerf['alpha'])
    print 'finEta (%): {0:.2f}'.format(channelPerf['finEta'])
    print 'flow speed (cm/s): {0:.2f}'.format(channelPerf['v'])
    print 'pressure drop p (psi): {0:.2f}'.format(channelPerf['P'])
    print 'flow rate f (ccm): {0:.2f}'.format(channelPerf['f'])
    print 'Re: {0:.2f}'.format(channelPerf['Re'])
    print 'NuAvg: {0:.2f}'.format(channelPerf['NuAvg'])
    print 'xCrit (mm): {0:.2f}'.format(channelPerf['xCrit'])
