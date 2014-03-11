import subprocess
import os
import ossie.parsers
from ossie.parsers import spd, scd, prf

OSSIEHOME=os.environ["OSSIEHOME"]

def standardizeComplexFormat(input):
    """
    Takes complex numbers of the form:

        A+Bj

    And converts to:

        A+jB

    """

    input = input.replace("i", "j")

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

class ResourcePackage(object):

    def __init__(
            self,
            name,
            outputDir=".",
            generator="pull",
            spdTemplateFile = OSSIEHOME+"/lib/python/redhawk/packagegen/templates/resourceTemplate.spd.xml",
            scdTemplateFile = OSSIEHOME+"/lib/python/redhawk/packagegen/templates/resourceTemplate.scd.xml",
            prfTemplateFile = OSSIEHOME+"/lib/python/redhawk/packagegen/templates/resourceTemplate.prf.xml",
            mFiles = []):

        self.name = name
        self.outputDir = outputDir

        self.spd = spd.parse(spdTemplateFile)
        self.scd = scd.parse(scdTemplateFile)
        self.prf = prf.parse(prfTemplateFile)

        self._setNameInSpd()

        self.mFiles = mFiles

        self._createWavedevContent(generator=generator)

    def _setNameInSpd(self):
        self.spd.id_ = self.name
        self.spd.name = self.name
        self.spd.propertyfile.localfile.name = self.name + ".prf.xml"
        self.spd.descriptor.localfile.name = self.name + ".scd.xml"
        for index in range(len(self.spd.implementation)):
            self.spd.implementation[index].code.entrypoint = self.spd.implementation[index].code.entrypoint.replace("template", self.name)

    def addUsesPort(self, name, type):
        ports = self.scd.componentfeatures.get_ports()
        if ports is None:
            # this is the first port to be added
            ports = scd.ports()
        ports.add_uses(scd.uses(usesname=name,
                                repid=type))
        self.scd.componentfeatures.set_ports(ports)

    def addProvidesPort(self, name, type):
        ports = self.scd.componentfeatures.get_ports()
        if ports is None:
            # this is the first port to be added
            ports = scd.ports()
        ports.add_provides(scd.provides(providesname=name,
                                        repid=type))
        self.scd.componentfeatures.set_ports(ports)

    def addSimpleProperty(
            self,
            id,
            value,
            complex=True,
            type="double",
            mode="readwrite",
            kindtypes=["configure"]):

        if complex:
            # convert from Octave complex to BulkIO complex
            value = standardizeComplexFormat(value)

        simple = prf.simple(
            complex=complex,
            type_=type,
            id_=id,
            mode=mode,
            value=value,
            action=prf.action(type_="external"))
        for kindtype in kindtypes:
            simple.add_kind(value=prf.kind(kindtype=kindtype))
        self.prf.add_simple(simple)

    def addSimpleSequencProperty(
            self,
            id,
            values,
            complex=True,
            type="double",
            mode="readwrite",
            kindtypes=["configure"]):

        if complex:
            # convert from Octave complex to BulkIO complex
            for index in range(len(values)):
                values[index] = standardizeComplexFormat(values[index])

        simplesequence = prf.simpleSequence(
            complex=complex,
            type_=type,
            id_=id,
            mode=mode,
            action=prf.action(type_="external"))

        if len(values) > 0:
            if values[0] != "":
                # only create value entries if there is actual content in the list
                valuesXml = prf.values()
                for value in values:
                    valuesXml.add_value(value=value)
                simplesequence.values=valuesXml

        for kindtype in kindtypes:
            simplesequence.add_kind(value=prf.kind(kindtype=kindtype))
        self.prf.add_simplesequence(simplesequence)

    def runCompileRpm(self):
        process = subprocess.Popen(
            './build.sh rpm',
            shell=True,
            cwd=self.outputDir+'/'+self.name)
        process.wait()

    def callCodegen(self, force = False):
        """
        Format command line arguments and call redhawk-codegen.

        For example:

            $ redhawk-codegen -m foo1.m -m foo2.m -f /home/user/bar.spd.xml

        """

        codegenArgs = ["redhawk-codegen"]
        for mFile in self.mFiles:
            codegenArgs.append("-m")
            codegenArgs.append(mFile)

        if force:
            codegenArgs.append("-f")

        codegenArgs.append(self.outputDir+"/"+self.name+"/"+self.name+".spd.xml")
        subprocess.call(codegenArgs)

    def runInstall(self):
        process = subprocess.Popen(
            './reconf',
            shell=True,
            cwd=self.outputDir+'/'+self.name+'/cpp')
        process.wait()
        process = subprocess.Popen(
            './configure',
            shell=True,
            cwd=self.outputDir+'/'+self.name+'/cpp')
        process.wait()
        process = subprocess.Popen(
            'make install',
            shell=True,
            cwd=self.outputDir+'/'+self.name+'/cpp')
        process.wait()

    def addSoftPackageDependency(self, dep, arch="noarch"):
        softpkgref = spd.softPkgRef(localfile=spd.localFile(name=dep),
                                    implref=spd.implRef(refid="default_impl_" + arch))
        dependency = spd.dependency(type_="runtime_requirements",
                                    softpkgref=softpkgref)
        for index in range(len(self.spd.implementation)):
            self.spd.implementation[index].add_dependency(dependency)

    def _createWavedevContent(self, generator):
        self.wavedevContent='<?xml version="1.0" encoding="ASCII"?>\n'
        self.wavedevContent+='<codegen:WaveDevSettings xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:codegen="http://www.redhawk.gov/model/codegen">\n'
        self.wavedevContent+='<implSettings key="cpp">\n'
        self.wavedevContent+='<value outputDir="cpp" template="redhawk.codegen.jinja.cpp.component.__GENERATOR" generatorId="redhawk.codegen.jinja.cpp.component.__GENERATOR" primary="true"/>\n'
        self.wavedevContent+='</implSettings>\n'
        self.wavedevContent+='</codegen:WaveDevSettings>\n'
        self.wavedevContent = self.wavedevContent.replace("__GENERATOR", generator)

    def writeWavedev(self, outputDir="."):
        self.createOutputDirIfNeeded()
        outfile=open(self.outputDir+"/"+self.name+"/."+ self.name+".wavedev", 'w')
        outfile.write(self.wavedevContent)
        outfile.close()

    def createOutputDirIfNeeded(self):
        if not os.path.exists(self.outputDir + "/" + self.name):
            os.makedirs(self.outputDir + "/" + self.name)

    def writeXML(self):
        self.writeSPD()
        self.writeSCD()
        self.writePRF()
        self.writeWavedev()

    def _writeXMLwithHeader(self, xmlObject, fileType, dtdName):
        outFile = open(self.outputDir+"/"+self.name+"/"+self.name+"."+fileType+".xml", 'w')
        outFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outFile.write('<!DOCTYPE _DTDNAME_ PUBLIC "-//JTRS//DTD SCA V2.2.2 SPD//EN" "_DTDNAME_.dtd">\n'.replace("_DTDNAME_", dtdName))
        xmlObject.export(
            outfile      = outFile,
            level        = 0,
            pretty_print = True)
        outFile.close()

    def writeSPD(self):
        self.createOutputDirIfNeeded()
        self._writeXMLwithHeader(self.spd, "spd", "softpkg")

    def writeSCD(self):
        self.createOutputDirIfNeeded()
        self._writeXMLwithHeader(self.scd, "scd", "softwarecomponent")

    def writePRF(self):
        self.createOutputDirIfNeeded()
        self._writeXMLwithHeader(self.prf, "prf", "properties")

