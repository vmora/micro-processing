# -*- coding: UTF-8 -*-

import os
import subprocess
from PyQt4.QtGui import *

from processing.core.parameters import ParameterVector,\
                                       ParameterTable,\
                                       ParameterString,\
                                       ParameterNumber,\
                                       ParameterFile
from processing.core.outputs import OutputVector,\
                                    OutputTable

from processing.core.GeoAlgorithm import GeoAlgorithm

from processing.core.ProcessingConfig import ProcessingConfig, Setting

from processing.core.AlgorithmProvider import AlgorithmProvider

from processing.core.Processing import Processing

class MicroAlgorithm(GeoAlgorithm):

    def __init__(self):
        GeoAlgorithm.__init__(self)

    def getIcon(self):
        return QIcon(os.path.dirname(__file__) + '/algo.svg')

    def helpFile(self):
       return None # well, would be nice to have, wouldn't it ?

    def commandLineName(self):
        return 'micro:algo' #to run algo from the python console

    def defineCharacteristics(self):
        self.name = 'run the command you configured'
        self.group = 'algorithms (this is a group)'

        self.addParameter(ParameterString('MyString', 'A string'))

        # Other exemples of what you may need:
        #
        #    self.addParameter(ParameterVector('MyVectorLayer', 'A vector layer',
        #                      [ParameterVector.VECTOR_TYPE_POINT, 
        #                       ParameterVector.VECTOR_TYPE_LINE]))
        #    self.addParameter(ParameterTable('MyTable', 'A table'))
        #    self.addParameter(ParameterNumber('MyNumber', 'A number'))
        #    self.addParameter(ParameterFile('MyFile', 'A file'))

        self.addOutput(OutputTable('MyOutputTable', 'Output table'))

        # There are many examples of creating vector output in
        # the porcessing algorithms comming with QGIS
        # so we won't do that here
        #
        #     self.addOutput(OutputVector('MyOutputLayer', 'Output layer'))
    
    def checkBeforeOpeningParametersDialog(self):
        if not ProcessingConfig.getSetting('MicroCommand'):
            return 'MicroCommand is not configured.\n\
                Please configure it before running micro algorithms.'
        # you can also set parameters if you are able to make an
        # educated guess for their value, e.g.:
        #     self.setParameterValue('MyVectorLayer', yourGuessedLayer )

    def processAlgorithm(self, progress):
        # the actual work is done here 
        
        mystring = self.getParameterValue('MyString')
        progress.setText('your string: '+mystring)
        
        command = ProcessingConfig.getSetting('MicroCommand')

        progress.setText('running: '+command)
        proc = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=False,
            ).stdout
        for line in iter(proc.readline, ''):
            progress.setText(line)
            if line.find('error') != -1:
                raise GeoAlgorithmExecutionException(
                        "errot found in command output: "+line)
       
        # create your output
        link_table_writer = self.getOutputFromName(
                "MyOutputTable").getTableWriter( ['First Column Name', 'Second Column Name'])
        link_table_writer.addRecords([['row1 col1', 'row1, col2'],
                                      ['row2 col1', 'row2, col2']])
        

class MicroAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)
        self.activate = True

    def getDescription(self):
        return 'a micro plugin for the processing framework'

    def getName(self):
        return 'micro'

    def getIcon(self):
        return QIcon(os.path.dirname(__file__) + '/micro.svg')

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)
        ProcessingConfig.addSetting(
                Setting(self.getDescription(),
                'MicroCommand', # name of setting
                'Custom command for micro',
                ''))

    def unload(self):
        AlgorithmProvider.unload(self)
        ProcessingConfig.removeSetting('MicroCommand')

    def _loadAlgorithms(self):
        try:
            self.algs.append(MicroAlgorithm())
        except Exception, e:
            ProcessingLog.addToLog(ProcessingLog.LOG_ERROR, 
                    'Could not create MicroAlgorithm:'+str(e))
            raise e


class MicroProcessing(object):
    
    def __init__(self, iface):
        self.algorithmProvider = MicroAlgorithmProvider()

    def initGui(self):
        Processing.addProvider(self.algorithmProvider, True)
    
    def unload(self):
        Processing.removeProvider(self.algorithmProvider)

def classFactory(iface):
    return MicroProcessing(iface)

