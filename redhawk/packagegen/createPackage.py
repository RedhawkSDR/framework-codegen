from packageTemplates import xmlTemplate as XML_TEMPLATE_STRING
import subprocess
import os

def create(configFile, outputDir, mFiles, force=False):
    """
    Use configFile to create the package XML files (SPD, PRF, SCD) and call
    the code generator to create component code.

    """


    component = _processConfigFile(configFile)

    # Do simple find/replace operations
    newLines = _findAndReplaceTags(XML_TEMPLATE_STRING, component)

    # Create XML entries for specified ports/properties
    newLines = _addPorts(newLines, component)
    newLines = _addPortTypes(newLines, component)
    newLines = _addProperties(newLines, component)
    newLines = _addDependencies(newLines, component)

    # Single XML file -> XML Files (SPD, PRF, SCD, .wavedev)
    myXmlGenerator = _XmlSplitter(component.name, newLines, outputDir)
    myXmlGenerator.generate()

    # XML files -> code
    _callCodegen(outputDir + "/" + component.name + "/" + component.name + ".spd.xml",
                 mFiles,
                 force)

def _callCodegen(spdLocation, mFiles = [], force = False):
    """
    Format command line arguments and call redhawk-codegen.

    For example:

        force = True
        mFiles = ["foo1.m", "foo2.m"]
        spdLocation = /home/user/bar.spd.xml

    Yields:

        $ redhawk-codegen -m foo1.m -m foo2.m -f /home/user/bar.spd.xml

    """

    codegenArgs = ["redhawk-codegen"]
    for mFile in mFiles:
        codegenArgs.append("-m")
        codegenArgs.append(mFile)

    if force:
        codegenArgs.append("-f")

    codegenArgs.append(spdLocation)
    subprocess.call(codegenArgs)

class _Port:
    """
    Simple data structure for storing port information

    """

    def __init__(self, name, dataType, direction):
        self.name = name
        self.direction = direction
        self.dataType = dataType.lower()
        if self.dataType.lower() == "double":
            self.bulkIOType = "IDL:BULKIO/dataDouble:1.0"
        elif self.dataType.lower() == "domainmanager":
            self.bulkIOType = "IDL:CF/DomainManager:1.0"
        else:
            self.bulkIOType = None
    def __str__(self):
        ret = ""
        ret += "name = " + self.name + "\n"
        ret += "direction = " + self.direction + "\n"
        ret += "bulkIO type = " + self.bulkIOType + "\n"
        return ret

class _Property:
    """
    Simple data structure for storing property information

    """

    def __init__(self, name, dataType, default, kindType):
        self.name = name
        self.kindType = kindType
        self.dataType = dataType
        self.default = default

        # If the default value is a list, the propType is simpleSequence.
        # Otherwise, the type is simple.
        if type(default) == type([]):
            self.propType = "simpleSequence"
        else:
            self.propType = "simple"

class Component:
    def __init__(self, name, generator, ports, props, deps):
        self.props = props
        self.ports = ports
        self.name = name
        self.generator = generator
        self.dependencies = deps
        self._setUniqueTypes()

    def _setUniqueTypes(self):
        """
        For every unique port type, corresponding XML must be added. For
        example, if a component has 3 double ports and 1 short, port,
        there should be 1 double declaration in XML and 1 short declaration
        in XML.  Note that there will still be 4 entries when defining
        the ports themselves.

        This method will garauntee that the component only has one entry
        in self.uniqueTypes per type.

        """

        self.uniqueTypes = []
        for port in self.ports:
            if not _inList(self.uniqueTypes, port.bulkIOType):
                self.uniqueTypes.append(port.bulkIOType)

def _inList(list, itemInQuestion):
    """
    Return True if itemInQeustion is already in the list.

    """

    for item in list:
        if item == itemInQuestion:
            return True
    return False

def _getComponentName(lines):
    """
    Loop through config file lines and look for a name entry.

    """

    for line in lines:
        if line.find("name") == 0:
            return line.split()[1]
    raise Exception

def _getGenerator(lines):
    """
    Loop through config file lines and look for a generator entry.

    """

    for line in lines:
        if line.find("generator") == 0:
        # if there is a generator entry, return the specified generator
            return line.split()[1]
    # If no generator entry was found, default to true
    return "pull"

def _getDeps(lines):
    """
    Loop through config file lines and look for dependency entries.

    """

    deps = []
    for line in lines:
        if line.lower().find("dependency") == 0:
            splits = line.split()
            deps.append(splits[1])

    return deps



def _getPorts(lines):
    """
    Loop through config file lines and look for port entries.

    """

    ports = []
    for line in lines:
        if line.lower().find("port") == 0:
            splits = line.split()
            ports.append(_Port(splits[1], splits[2], splits[3]))
    return ports

def _getProps(lines):
    """
    Loop through config file lines and look for property entries.

    """

    props = []
    for line in lines:
        if line.lower().find("prop") == 0:
            # look for sequences
            openBracket = line.find("[")
            closeBracket = line.find("]")
            if openBracket != -1 and closeBracket != -1:
                # SimpleSequence, need to parse out the default argument
                defaultStr = line[openBracket+1:closeBracket]
                if closeBracket == len(line)-1:
                    # close bracket is the last character
                    line = line[:openBracket]
                else:
                    # close bracket is not the last character
                    line = line[:openBracket] + line[closeBracket+1:]
                default = []
                for val in defaultStr.split(","):
                    default.append(val)

            else:
                # Simple

                # pull out the default value from the line and reconstruct
                # the line without the default value
                splits = line.split()
                default = splits[3]

                line = ""
                for substr in splits:
                    if substr != default:
                        line += substr + " "

            splits = line.split()
            if len(splits) == 3:
                props.append(_Property(splits[1], splits[2], default, "configure"))
            else:
                # a kindtype was specified
                props.append(_Property(splits[1], splits[2], default, splits[3]))

    return props

def _processConfigFile(configFileName):
    """
    Populate a component object based on the contents of a config file.

    """

    lines = _myReadlines(configFileName)
    lines = _removeComments(lines, "#")
    name = _getComponentName(lines)
    generator = _getGenerator(lines)
    ports = _getPorts(lines)
    props = _getProps(lines)
    deps = _getDeps(lines)
    component = Component(name, generator, ports, props, deps)
    return component

def _myReadlines(filename):
    """
    Wrapper around the python readlines method that assures the file gets 
    closed.

    """

    fp = open(filename)
    lines = fp.readlines()
    fp.close()
    return lines

def _addPorts(newLines, component):
    """
    Add lines of XML for each port of the component.

    """

    newLinesWithPorts = []
    for line in newLines:
        if line.find("__PORTS") != -1:
            for port in component.ports:
                if port.direction == "input":
                    portLine = ' '*6 + '<provides repid="{0}" providesname="{1}"/>\n'
                    portLine = portLine.format(port.bulkIOType, port.name)
                    newLinesWithPorts.append(portLine)

                if port.direction == "output":
                    portLine = ' '*6 + '<uses repid="{0}" usesname="{1}"/>\n'
                    portLine = portLine.format(port.bulkIOType, port.name)
                    newLinesWithPorts.append(portLine)

        else:
            newLinesWithPorts.append(line)

    return newLinesWithPorts

def _addPortTypes(newLines, component):
    """
    Add liens of XML to define each unique port type of the component.

    """

    # TODO: support interface descriptions
    # note that this is only for standards compliance and adds no real function value
    #<!-- __PORT_TYPES-->\n\
    #  <inheritsinterface repid="IDL:BULKIO/ProvidesPortStatisticsProvider:1.0"/>\n\
    #  <inheritsinterface repid="IDL:BULKIO/updateSRI:1.0"/>\n\
    #</interface>\n\
    newLinesWithTypes = []
    for line in newLines:
        if line.find("__PORT_TYPES") != -1:
            for type in component.uniqueTypes:
                typeLine = ' '*4 + '<interface name="{0}" repid="IDL:BULKIO/{0}:1.0">\n'
                typeLine = typeLine.format(type)
                newLinesWithTypes.append(typeLine)
        else:
            newLinesWithTypes.append(line)
    return newLinesWithTypes

def _addProperties(newLines, component):
    newLinesWithProps = []
    for line in newLines:
        if line.find("__PROPERTIES") != -1:
            # found the tag
            for prop in component.props:
                if prop.propType == "simple":
                    propLines  = ' ' *4 + '<simple id="{0}" mode="readwrite" type="{1}">\n'
                    propLines += ' ' *6 + '<description></description>\n'
                    propLines += ' ' *6 + '<value>{2}</value>\n'
                    propLines += ' ' *6 + '<kind kindtype="configure"/>\n'
                    propLines += ' ' *6 + '<kind kindtype="{3}"/>\n'
                    propLines += ' ' *6 + '<action type="external"/>\n'
                    propLines += ' ' *4 + '</simple>\n'
                    propLines = propLines.format(prop.name, prop.dataType, prop.default, prop.kindType)
                    newLinesWithProps.append(propLines)
                else:
                    propLines  = ' ' *4 + '<simplesequence id="{0}" mode="readwrite" type="{1}">\n'.format(prop.name, prop.dataType)
                    if prop.default:
                        propLines  += ' ' *6 + '<values>\n'
                        for val in prop.default:
                            propLines  += ' ' *8 + '<value>{0}</value>\n'.format(val)
                        propLines  += ' ' *6 + '</values>\n'
                    propLines += ' ' *6 + '<kind kindtype="configure"/>\n'
                    propLines += ' ' *6 + '<kind kindtype="{0}"/>\n'.format(prop.kindType)
                    propLines += ' ' *6 + '<action type="external"/>\n'
                    propLines += ' ' *4 + '</simplesequence>\n'
                    newLinesWithProps.append(propLines)
        else:
            # regular line (no tag)
            newLinesWithProps.append(line)
    return newLinesWithProps

def _addDependencies(newLines, component):
    newLinesWithDependency = []
    for line in newLines:
        if line.find("__DEPENDENCY") != -1:
            for dependency in component.dependencies:
                propLines = ' '*4 + '<dependency type="runtime_requirements">\n'
                propLines += ' '*6 + '<softpkgref>\n'
                propLines += ' '*8 + '<localfile name="{0}"/>\n'.format(dependency)
                propLines += ' '*8 + '<implref refid="default_impl"/>\n'
                propLines += ' '*6 + '</softpkgref>\n'
                propLines += ' '*4 + '</dependency>\n'
                newLinesWithDependency.append(propLines)
        else:
            # regular line (no tag)
            newLinesWithDependency.append(line)

    return newLinesWithDependency



def _findAndReplaceTags(inputLines, component):
    """
    Perform simple find and replace operations for know tags.

    """
    outputLines = []
    inputLinesAsList = inputLines.split("\n")
    for line in inputLinesAsList:
        line += "\n"
        if line.find("__COMPONENT_NAME") != -1:
            outputLines.append(line.replace("__COMPONENT_NAME", component.name))
        elif line.find("__GENERATOR") != -1:
            outputLines.append(line.replace("__GENERATOR", component.generator))
        else:
            outputLines.append(line)
    return outputLines

def _removeComments(inputLines, commentFlag):
    """
    Loop through inputLines. If a commentFlag is the character in a line, 
    remove the whole line.

    """

    outputLines = []
    for line in inputLines:
        if line.find(commentFlag) != 0:
            outputLines.append(line)
    return outputLines

class _XmlSplitter:
    """
    Class for breaking down a single XML file that contains SPD, PRF, and SCD
    content into the 3 separate XML files.

    """

    def __init__(self, componentName, lines, outputDir):
        self.componentName = componentName
        self.lines = lines
        self.outputDir = outputDir

        if not os.path.exists(self.outputDir+"/"+self.componentName):
            os.makedirs(self.outputDir+"/"+self.componentName)

    def _getContent(self, lines, begin, end):
        """
        Get the lines after the begin tag and before the end tag.

        """

        recording = False
        content = []
        for line in lines:
            if line.find(end) != -1:
                recording = False
            if recording:
                content.append(line)
            if line.find(begin) != -1:
                recording = True
        return content

    def _createXmlFile(self, beginTag, endTag, extention, hidden = False):
        """
        Take the content between beginTag and endTag and write it to
        self.componentName + extention.

        """

        prependVal = ""
        if hidden:
            prependVal = "."
        content = self._getContent(self.lines, beginTag, endTag)
        outputFile=self.outputDir+"/"+self.componentName+"/"+prependVal+\
                   self.componentName+extention
        outputFilePointer = open(outputFile, 'w')

        outputFilePointer.writelines(content)

    def generate(self):
        self._createXmlFile("BEGIN_SPD", "END_SPD", ".spd.xml")
        self._createXmlFile("BEGIN_SCD", "END_SCD", ".scd.xml")
        self._createXmlFile("BEGIN_PRF", "END_PRF", ".prf.xml")
        self._createXmlFile("BEGIN_WAVEDEV", "END_WAVEDEV", ".wavedev", hidden=True)

