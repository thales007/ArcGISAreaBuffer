#######################################
# Title: AreaBuffer.pyt
# Description: Buffer points based upon an area
# Tools:
# Author: Timothy Hales
# Created: 3/13/2013
# Last Updated: 3/18/2014
# Version: 0.3 beta
# Python Version: 2.7
# Version 0.1 Notes: Fixed some error messages, and exposed the negative buffer distance for the building height tool.
# Version 0.2 Notes: Allowed any type of feature type for input.  Created option to select area units.
# Version 0.3 Notes: Added in Acres and Hectares as input units.
########################################
import arcpy, math


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [AreaBufferTool]


class AreaBufferTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Area Buffer"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        pInputFC = arcpy.Parameter(
            displayName="Input feature class",
            name="inputPoints",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        #pInputPoints.filter.list = ["Point"]

        pOutputBuffer = arcpy.Parameter(
            displayName="Output buffer feature class",
            name="outputBuffer",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")
        
        pInputArea = arcpy.Parameter(
            displayName="Area of output buffer",
            name="inputArea",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        pInputUnits = arcpy.Parameter(
            displayName="Area units",
            name="inputUnits",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        pInputUnits.filter.type = "ValueList"
        pInputUnits.filter.list = ["Centimeters", "Decimal degrees", "Decimeters", "Feet", "Inches", "Kilometers",
                                   "Meters", "Acres", "Hectares", "Miles", "Millimeters", "Nautical Miles", "Points", "Unknown", "Yards"]

        parameters = [pInputFC, pOutputBuffer, pInputArea, pInputUnits]
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
        area = parameters[2].value
        #acres = float(parameters[2].value)
        units = parameters[3].value


       #Check to see what unit is selected.  If a two word unit is used, convert to a single word
        if units == "Decimal degrees":
            units = "Decimaldegrees"
        elif units == "Nautical Miles":
            units = "NauticalMiles"
            
        #Conversion for Acrea and Hetares
        if units == "Hectares":
            area = area * 107600
            units = "Feet"
        elif units == "Acres":
            area = area * 43560
            units = "Feet"

        buffDist = str(math.sqrt(area/math.pi)) + " {}".format(units)
        #arcpy.AddMessage(str(buffDist))


        arcpy.Buffer_analysis(inputFC, outputFC, buffDist)
