"""
Given a library, create a soft-package dependency.

The soft-package dependency consists of:
    - an spd.xml file
    - a directory containing the library (this program will create a symbolic
      link to the library)
    - autoconf files

Example usage:
    >>> import createPackageDependency
    >>> createPackageDependency.create("/home/user/theLibrary/",\
                                       "/home/user/mySoftPkgDeps/")

"""

import os
import shutil

from packageDependencyTemplates import Makefile as MAKEFILE_TEMPLATE
from packageDependencyTemplates import spd as SPD_TEMPLATE
from packageDependencyTemplates import reconf as RECONF_STRING
from packageDependencyTemplates import configureAc as CONFIGUREAC_STRING


def create(libraryLocation, outputDir):
    """
    This is the main entry point to the module.

    Arguments:
        libraryLocation - location of the library that should be wrapped as a
                          soft package dependency.

        outputDir       - where to write the associated soft package dependency
                          files.  Default is current working directory.

    Creates output dir and sym links to the input package.
    Copies over standard files, such as reconf.
    Calls _processTemplate on all applicable templates strings, which will write 
    files to the outputDir.

    """

    libraryName = _generatePackageName(libraryLocation)

    fullOutputDir = outputDir+"/" + libraryName+"Pkg/"
    if not os.path.exists(fullOutputDir):
        os.makedirs(fullOutputDir)
    if not os.path.exists(fullOutputDir+libraryName):
        if not os.path.isabs(libraryLocation):
            libraryLocation = os.path.join(os.getcwd(), libraryLocation)
        os.symlink(libraryLocation, fullOutputDir+libraryName)

    fp = open(fullOutputDir+"configure.ac", 'w')
    fp.write(CONFIGUREAC_STRING)
    fp.close()

    fp = open(fullOutputDir+"reconf", 'w')
    fp.write(RECONF_STRING)
    fp.close()
    os.chmod(fullOutputDir+"reconf", 0775)

    _processTemplateString(MAKEFILE_TEMPLATE,
                     outputDir + "/" + libraryName + "Pkg/"+ "Makefile.am",
                     libraryName)
    _processTemplateString(SPD_TEMPLATE,
                     outputDir + "/" + libraryName + "Pkg/"+ libraryName+"Pkg.spd.xml",
                     libraryName)


def _processTemplateString(templateString, outputFileName, libraryName):
    """
    Replace the package name tag in templateString with libraryName 
    and write to outputFileName.

    """

    templateString = templateString.replace("__LIBRARY_NAME__", libraryName)

    # Write to file.
    fp = open(outputFileName, 'w')
    fp.write(templateString)
    fp.close()

def _generatePackageName(libraryLocation):
    """
    Given a directory a/b/c, return c.

    """

    subdirs = libraryLocation.split("/")

    # remove blank entries
    subdirs = [x for x in subdirs if x != ""]

    # last item in the list
    libraryName = subdirs[-1]

    return libraryName

