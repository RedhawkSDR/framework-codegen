import subprocess
import os
import ossie.parsers
from ossie.parsers import spd, scd, prf
from ossie.parsers.scd import softwarecomponent

def runCompileRpm(outputDir, componentName):
    process = subprocess.Popen(
        './build.sh rpm',
        shell=True,
        cwd=outputDir+'/'+componentName)
    process.wait()

def runInstall(outputDir, componentName):
    process = subprocess.Popen(
        './reconf',
        shell=True,
        cwd=outputDir+'/'+componentName+'/cpp')
    process.wait()
    process = subprocess.Popen(
        './configure',
        shell=True,
        cwd=outputDir+'/'+componentName+'/cpp')
    process.wait()
    process = subprocess.Popen(
        'make install',
        shell=True,
        cwd=outputDir+'/'+componentName+'/cpp')
    process.wait()

def _createDependency(dep):
    softpkgref = spd.softPkgRef(localfile=spd.localFile(name=dep),
                                implref=spd.implRef(refid="default_impl"))
    dependency = spd.dependency(type_="runtime_requirements",
                                softpkgref=softpkgref)
    return dependency

def _createImplementation(component):
    '''
    Create implementation element to be inserted into a softpkg element within
    the SPD file.
    '''

    localfile = spd.localFile(name="cpp")

    code = spd.code("Executable",
             localfile = localfile,
             entrypoint = "cpp/" + component.name)
    implementation = spd.implementation(id_="cpp")
    implementation.description = "The implementation contains descriptive information about the template for a software component."
    implementation.code = code
    implementation.compiler = spd.compiler()
    implementation.compiler.name = "/usr/bin/gcc"
    implementation.compiler.version = "4.1.2"

    implementation.programminglanguage = spd.programmingLanguage(name = "C++")
    implementation.humanlanguage = spd.humanLanguage(name = "EN")
    implementation.add_os(spd.os(name = "Linux"))
    for dep in component.dependencies:
        implementation.add_dependency(_createDependency(dep))
    implementation.add_processor(spd.processor(name="x86"))
    implementation.add_processor(spd.processor(name="x86_64"))
    return implementation

def _createDescriptor(component):
    descriptor = spd.descriptor()
    descriptor.localfile=spd.localFile(component.name+".scd.xml")
    return descriptor

def _createPropertyFile(component):
    propertyfile = spd.propertyFile()
    propertyfile.localfile=spd.localFile(name=component.name+".prf.xml")
    return propertyfile

def writeSPD(component, outputDir):
    implementation = _createImplementation(component)
    descriptor = _createDescriptor(component)
    propertyfile = _createPropertyFile(component)

    softpkg = spd.softPkg(type_="sca_compliant",
                          id_=component.name,
                          name=component.name,
                          propertyfile=propertyfile,
                          title="",
                          descriptor=descriptor)
    author = spd.author()
    author.add_name(value="null")
    softpkg.add_author(author)
    softpkg.add_implementation(implementation)

    outfile = open(outputDir+'/'+component.name+"/"+component.name+".spd.xml", 'w')
    boilerplateLines = []
    boilerplateLines.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    boilerplateLines.append('<!DOCTYPE softpkg PUBLIC "-//JTRS//DTD SCA V2.2.2 SPD//EN" "softpkg.dtd">\n')
    outfile.writelines(boilerplateLines)
    softpkg.export(outfile = outfile, level = 0, pretty_print=True, name_="softpkg")
    outfile.close()

def _createComponentFeature(component):
    componentfeatures=scd.componentFeatures()
    componentfeatures.add_supportsinterface(
        scd.supportsInterface(
            supportsname="Resource",
            repid="IDL:CF/Resource:1.0"))
    componentfeatures.add_supportsinterface(
        scd.supportsInterface(
            supportsname="LifeCycle", 
            repid="IDL:CF/LifeCycle:1.0"))
    componentfeatures.add_supportsinterface(
        scd.supportsInterface(
            supportsname="PortSupplier",
            repid="IDL:CF/PortSupplier:1.0"))
    componentfeatures.add_supportsinterface(
        scd.supportsInterface(
            supportsname="PropertySet",
            repid="IDL:CF/PropertySet:1.0"))
    componentfeatures.add_supportsinterface(
        scd.supportsInterface(
            supportsname="IDL:CF/TestableObject:1.0",
            repid="TestableObject"))

    ports = scd.ports()
    for port in component.ports:
        if port.direction == "output":
            ports.add_uses(scd.uses(usesname=port.name,
                                    repid=port.bulkIOType))
        if port.direction == "input":
            ports.add_provides(scd.provides(providesname=port.name,
                                            repid=port.bulkIOType))
    componentfeatures.ports=ports

    return componentfeatures

def _createInterfaces(component):
    interfaces = scd.interfaces()

    resourceInterface = scd.interface(name="Resource", 
                                      repid="IDL:CF/Resource:1.0")
    resourceInterface.add_inheritsinterface(
        scd.inheritsInterface(repid="IDL:CF/LifeCycle:1.0"))
    resourceInterface.add_inheritsinterface(
        scd.inheritsInterface(repid="IDL:CF/PortSupplier:1.0"))
    resourceInterface.add_inheritsinterface(
        scd.inheritsInterface(repid="IDL:CF/PropertySet:1.0"))
    resourceInterface.add_inheritsinterface(
        scd.inheritsInterface(repid="IDL:CF/TestableObject:1.0"))
    interfaces.add_interface(resourceInterface)

    interfaces.add_interface(
        scd.interface(
            name="LifeCycle",
            repid="IDL:CF/LifeCycle:1.0"))
    interfaces.add_interface(
        scd.interface(
            name="PortSupplier",
            repid="IDL:CF/PortSupplier:1.0"))
    interfaces.add_interface(
        scd.interface(
            name="PropertySet",
            repid="IDL:CF/PropertySet:1.0"))
    interfaces.add_interface(
        scd.interface(
            name="TestableObject",
            repid="IDL:CF/TestableObject:1.0"))
    interfaces.add_interface(
        scd.interface(
            name="ProvidesPortStatisticsProvider",
            repid="IDL:BULKIO/ProvidesPortStatisticsProvider:1.0"))
    interfaces.add_interface(
        scd.interface(
            name="updateSRI",
            repid="IDL:BULKIO/updateSRI:1.0"))

    return interfaces

def writeSCD(component, outputDir):
    componentrepid=scd.componentRepId(repid="IDL:CF/Resource:1.0")
    softwarecomponent = scd.softwarecomponent(corbaversion="2.2",
                                              componentrepid=componentrepid,
                                              componenttype="resource")

    softwarecomponent.componentfeatures=_createComponentFeature(component)
    softwarecomponent.interfaces=_createInterfaces(component)

    outfile = open(outputDir+"/"+component.name+"/"+component.name+".scd.xml", 'w')
    boilerplateLines = []
    boilerplateLines.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    boilerplateLines.append('<!DOCTYPE softwarecomponent PUBLIC "-//JTRS//DTD SCA V2.2.2 SCD//EN" "softwarecomponent.dtd">\n')
    outfile.writelines(boilerplateLines)
    softwarecomponent.export(outfile = outfile, level = 0, pretty_print=True)
    outfile.close()

def _createProperties(component):
    properties = prf.properties()

    for prop in component.props:
        if prop.propType == "simple":
            simple = prf.simple(
                complex=prop.complexFlag,
                type_=prop.dataType,
                id_=prop.name,
                mode="readwrite",
                value=prop.default,
                action=prf.action(type_="external"))

            simple.add_kind(value=prf.kind(kindtype="configure"))
            if prop.kindType != "configure":
                simple.add_kind(value=prf.kind(kindtype=prop.kindType))
            properties.add_simple(simple)

        elif prop.propType == "simpleSequence":
            simplesequence = prf.simpleSequence(
                complex=prop.complexFlag,
                type_=prop.dataType,
                id_=prop.name,
                mode="readwrite",
                action=prf.action(type_="external"))

            values = prf.values()
            for value in prop.default:
                values.add_value(value=value)
            simplesequence.values=values

            simplesequence.add_kind(value=prf.kind(kindtype="configure"))
            if prop.kindType != "configure":
                simplesequence.add_kind(value=prf.kind(kindtype=prop.kindType))
            properties.add_simplesequence(simplesequence)

    return properties

def writePRF(component, outputDir):
    properties = _createProperties(component)

    outfile = open(outputDir+"/"+component.name+"/"+component.name+".prf.xml", 'w')
    boilerplateLines = []
    boilerplateLines.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    boilerplateLines.append('<!DOCTYPE properties PUBLIC "-//JTRS//DTD SCA V2.2.2 PRF//EN" "properties.dtd">\n')
    outfile.writelines(boilerplateLines)
    properties.export(outfile = outfile, level = 0, pretty_print=True)
    outfile.close()

    return

def writeWavedev(component, outputDir):
    content='<?xml version="1.0" encoding="ASCII"?>\n'
    content+='<codegen:WaveDevSettings xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:codegen="http://www.redhawk.gov/model/codegen">\n'
    content+='<implSettings key="cpp">\n'
    content+='<value outputDir="cpp" template="redhawk.codegen.jinja.cpp.component.__GENERATOR" generatorId="redhawk.codegen.jinja.cpp.component.__GENERATOR" primary="true"/>\n'
    content+='</implSettings>\n'
    content+='</codegen:WaveDevSettings>\n'

    content = content.replace("__GENERATOR", component.generator)
    outfile=open(outputDir+"/"+component.name+"/."+component.name+".wavedev", 'w')
    outfile.write(content)
    outfile.close()

def writeXMLUsingXMLGen(component, outputDir):
    writeSPD(component, outputDir)
    writeSCD(component, outputDir)
    writePRF(component, outputDir)
    writeWavedev(component, outputDir)

def create(config,
           outputDir,
           mFiles,
           force       = False,
           buildRpm    = False,
           install     = False):
    """
    Use config to create the package XML files (SPD, PRF, SCD) and call
    the code generator to create component code.

    """

    if type(config) == type(''): 
        component = _processConfigFile(config)
    elif type(config) == type([]):
        component = _processConfigLines(config) 
    else:
        raise SystemExit("Invalid data type sent to create method")

    if not os.path.exists(outputDir + "/" + component.name):
        os.makedirs(outputDir + "/" + component.name)

    writeXMLUsingXMLGen(component, outputDir)

    # XML files -> code
    _callCodegen(outputDir + "/" + component.name + "/" + component.name + ".spd.xml",
                 mFiles,
                 force)

    if buildRpm:
        runCompileRpm(outputDir, component.name)

    if install:
        runInstall(outputDir, component.name)

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
        ret = "\n"
        ret += "name = " + self.name + "\n"
        ret += "direction = " + self.direction + "\n"
        ret += "bulkIO type = " + self.bulkIOType + "\n"
        return ret

class _Property:
    """
    Simple data structure for storing property information

    """

    def __init__(self, name, dataType, default, kindType, complexFlag = "false"):
        self.name        = name
        self.kindType    = kindType
        self.dataType    = dataType
        self.default     = default
        if self.dataType == 'double':
            if self.default == ['']:
                self.default = ['0']
        self.complexFlag = complexFlag

        # If the default value is a list, the propType is simpleSequence.
        # Otherwise, the type is simple.
        if type(default) == type([]):
            self.propType = "simpleSequence"
        else:
            self.propType = "simple"

    def __str__(self):
        ret = "\n"
        ret += 'name ' + self.name + '\n' 
        ret += 'kindType ' + self.kindType+ '\n' 
        ret += 'dataType ' + self.dataType+ '\n' 
        ret += 'default ' + self.default+ '\n' 
        ret += 'complexFlag ' + self.complexFlag+ '\n' 
        ret += 'propType ' + self.propType+ '\n' 
        return ret

class Component:
    def __init__(self, name, generator, ports, props, deps):
        self.props = props
        self.ports = ports
        self.name = name
        self.generator = generator
        self.dependencies = deps

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

def standardizeComplexFormat(input):
    """
    Takes complex numbers of the form:

        A+Bj

    And converts to:

        A+jB

    """

    input.replace("i", "j")

    try:
        complexVal = complex(input)
        if complexVal.imag >= 0:
            sign = "+"
        else:
            sign = "-"
        return str(complexVal.real) + sign + "j" + str(complexVal.imag) 
    except:
        # Assume input is already in A+jB form
        return input

def _getProps(lines):
    """
    Loop through config file lines and look for property entries.

    """

    props = []
    for line in lines:
        if line.lower().find("prop") == 0:
            splits   = line.split()
            name     = splits[1]
            dataType = splits[2]
            default  = splits[3]

            complexFlag = "false"
            if dataType.lower().find("complex") == 0:
                complexFlag = "true"
                dataType = dataType[len("complex"):].lower()

            # look for sequences
            openBracket = default.find("[")
            if default.find("[") != -1: # sequence
                # Take out the brackets
                default = default[1:len(default)-1]

                # split by commans and break into a list
                default = default.split(",")

                if complexFlag == "true":
                    for val in default:
                        val = standardizeComplexFormat(val)

            else:  # Simple
                if complexFlag == "true":
                    default = standardizeComplexFormat(default)

            if len(splits) == 4:
                props.append(_Property(name     = name,
                                       dataType = dataType,
                                       default  = default,
                                       kindType = "configure",
                                       complexFlag = complexFlag))
            elif len(splits) == 5:
                # a kindtype was specified
                props.append(_Property(name        = name,
                                       dataType    = dataType,
                                       default     = default,
                                       kindType    = splits[4],
                                       complexFlag = complexFlag))

    return props

def _processConfigFile(configFileName):
    """
    Populate a component object based on the contents of a config file.

    """

    lines = _myReadlines(configFileName)
    lines = _removeComments(lines, "#")
    return _processConfigLines(lines)

def _processConfigLines(configLines):
    name      = _getComponentName(configLines)
    generator = _getGenerator(configLines)
    ports     = _getPorts(configLines)
    props     = _getProps(configLines)
    deps      = _getDeps(configLines)
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

