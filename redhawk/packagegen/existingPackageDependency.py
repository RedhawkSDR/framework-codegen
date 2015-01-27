import subprocess
import os
from ossie.parsers import spd
from redhawk.packagegen.softPackage import SoftPackage

OSSIEHOME=os.environ["OSSIEHOME"]

class ExistingPackageDependency(SoftPackage):

    def __init__(
            self,
            type,
            name,
            implementation,
            outputDir=".",
            pkgConfig="",
            spdTemplateFile = OSSIEHOME+"/lib/python/redhawk/packagegen/templates/resourceTemplate.spd.xml",
            variant = ""):
        self.type = type     
        self.implementation = implementation       
        
        if pkgConfig:
            with open(pkgConfig) as f:
                pkgC = f.readlines()

            matching = [s for s in pkgC if "Libs" in s]
            string= matching[0].split()
            
            linking = [l for l in string if "-l" in l]
            
            name = linking[0].replace("-l","")

        SoftPackage.__init__(self, name, implementation, outputDir)
        #else:
        #    SoftPackage.__init__(self,name,"cpp_"+implementation,outputDir)
      
        self.spd = spd.parse(spdTemplateFile)

        self._setNameInSpd()
        self._setImplementation()

        self._createWavedevContent(generator="project.softPackageDependency.existing")
  
        fullOutputDir = outputDir+"/" + name + "/"
        if not os.path.exists(fullOutputDir):
            os.makedirs(fullOutputDir)
        #def _createWavedevContent(self, generator):
        # TODO: replace this with an XML template
    def _setImplementation(self):
        #if self.useArch:
        #    for arch in self.arch:
        #        localfile = spd.localFile(name = "./" + "cpp_" + arch + "/lib")
        #        code = spd.code(type_= "SharedLibrary", localfile = localfile)
        #        compiler = spd.compiler(version="4.1.2", name="/usr/bin/gcc")
        #        localimpl = "cpp_" + arch
        #        print self.implementation
        #        implementation = spd.implementation(
        #            id_=localimpl,
        #            description="",
        #            code = code,
        #            compiler = compiler,
        #            programminglanguage = spd.programmingLanguage(name="c++"),
        #            humanlanguage = spd.humanLanguage(name="EN"))
        #        os = spd.os(name="Linux")
        #        implementation.add_os(value=os)
        #        if arch == 'i686':
        #            implementation.add_processor(spd.processor(name="x86"))
        #        else:
        #            implementation.add_processor(spd.processor(name=arch))                                        
        #        self.spd.add_implementation(value=implementation)          
        #else:        
        localfile = spd.localFile(name = "./" + self.implementation + "/lib")
        code = spd.code(type_= "SharedLibrary", localfile = localfile)
        compiler = spd.compiler(version="4.1.2", name="/usr/bin/gcc")
        #localimpl = "cpp"            
        #if self.proc:
        #    localimpl = localimpl+"_"+self.proc

        implementation = spd.implementation(
            id_=self.implementation,
            description="",
            code = code,
            compiler = compiler,
            programminglanguage = spd.programmingLanguage(name="c++"),
            humanlanguage = spd.humanLanguage(name="EN"))
        os = spd.os(name="Linux")
        implementation.add_os(value=os)
               
        implementation.add_processor(spd.processor(name="x86"))
        implementation.add_processor(spd.processor(name="x86_64"))

        self.spd.add_implementation(value=implementation)

#    def writeXML(self,variant=""):
#        '''
#        Call methods to Write resource.spd.xml, resource.prf.xml,
#        resource.scd.xml, and .resource.wavedev.#

#        '''
#
#       if self.spd:
#            self.writeSPD(variant)
#        if self.scd:
#            self.writeSCD()
#        if self.prf:
#            self.writePRF()
#        if self.wavedevContent:
#            self.writeWavedev()
#
#    def _writeXMLwithHeader(self, xmlObject, fileType, dtdName, name_=None, variant=""):
#        '''
#        The xml files contain two header lines that are outside of the primary
#        file element.  Write the two header lines followed by the primary file
#        element to output file.
#
#        '''
#
#        outFile = open(self.outputDir+"/"+self.name+"/"+self.name+"_"+variant+"."+fileType+".xml", 'w')
#        outFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
#        outFile.write('<!DOCTYPE _DTDNAME_ PUBLIC "-//JTRS//DTD SCA V2.2.2 SPD//EN" "_DTDNAME_.dtd">\n'.replace("_DTDNAME_", dtdName))
#        if name_ == None:
#            name_ = dtdName
#        xmlObject.export(
#            outfile = outFile,
#            level = 0,
#            pretty_print = True,
#            name_ = name_)
#        outFile.close()

#    def writeSPD(self,variant=""):
#        self.createOutputDirIfNeeded()
#        self._writeXMLwithHeader(self.spd, "spd", "softpkg", name_="softpkg", variant=variant)#



            
#def callCodegen(self, force = False, variant = "", sFiles=[], hFiles=[], objs="", ):
#        """
#        Format command line arguments and call redhawk-codegen.#
#
#        For example:

#            $ redhawk-codegen -s foo1.c -s foo2.c -h foo1.h -h foo2.h -f /home/user/bar.spd.xml

#        """

#        codegenArgs = ["redhawk-codegen"]
#        
#        for sFile in sFiles:
#            codegenArgs.append("-s")
#            codegenArgs.append(sFile)
#        
#        for hFile in hFiles:
#            codegenArgs.append("-h")
#            codegenArgs.append(hFile)
#        
#        for obj in objs:
#            codegenArgs.append("-obj")
#            codegenArgs.append(obj)#
#
#        if force:
#            codegenArgs.append("-f")#

#        if variant != "":
#            codegenArgs.append("--variant=" + variant)#
#
        #codegenArgs.append(self.outputDir+"/"+self.name+"/"+self.name+"_"+variant+".spd.xml")
#        codegenArgs.append(self.outputDir+"/"+self.name+"/"+self.name+".spd.xml")
        
#        subprocess.call(codegenArgs)
