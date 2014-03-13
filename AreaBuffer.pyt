#######################################
# Title: 3DHeightTools.pyt
# Description: Buffer points based upon an area
# Tools:
# Author: Timothy Hales
# Created: 3/13/2013
# Last Updated: 3/13/2014
# Version: 0.1 beta
# Python Version: 2.7
# Version 0.1 Notes: Fixed some error messages, and exposed the negative bufgfer distance for the building height tool.
########################################
import arcpy, math


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        pInputPoints = arcpy.Parameter(
            displayName="Input point feature class",
            name="inputPoints",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input")
        pInputPoints.filter.list = ["Point"]

        pOutputBuffer = arcpy.Parameter(
            displayName="Output buffer feature class",
            name="outputBuffer",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Output")
        
        pInputArea = arcpy.Parameter(
            displayName="Acres of output buffer",
            name="inputArea",
            datatype="GPString",
            parameterType="Required",
            direction="Input")


        parameters = [pInputPoints, pOutputBuffer, pInputArea]
        return parameters
    
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputFC = parameters[0].value
        outputFC = parameters[1].value
        acres = float(parameters[2].value)

        #need to read the linear unit of input FC
        
        areaFt = acres * 43560
        buffDist = math.sqrt(areaFt/math.pi)
        arcpy.AddMessage(str(buffDist))


        arcpy.Buffer_analysis(inputFC, outputFC, buffDist)
