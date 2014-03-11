from redhawk.codegen.model import softpkg
from redhawk.packagegen.resourcePackage import ResourcePackage

#TODO: handle sampleRate correctly
__RESERVED_KEYWORDS__    = ['sampleRate', '__sampleRate', 'diaryOnOrOff', 'bufferingEnabled']

def ambiguousArgumentException(argument, validTags):
    '''
    Print an error and raise an exception indicating that an ambiguous
    argument has been encountered.

    '''

    errString = 'ERROR: Ambiguous argument: ' + argument
    errString += '\nMust prepend one of:'
    for tag in validTags:
        errString += '\n    ' + str(tag)
    raise SystemExit(errString)

def getMFunctionParameters(function, mFiles):
    mFunctionParameters = None

    # find the master m file and parse its m function
    for mFile in mFiles:
        if mFile.find(function + '.m') != -1:
            mFunctionParameters = softpkg.parseMFile(mFile)
            break
    if mFunctionParameters is None:
        raise SystemExit('ERROR: No matching m file for specified function')

    return mFunctionParameters

def _cleanQuotes(value):
    if len(value) == 0:
        return
    if value[0] == "'":
        return value.replace("'","")
    if value[0] == '"':
        return value.replace('"',"")

class OctavePackage(ResourcePackage):

    def __init__(
            self,
            mFiles,
            function,
            outputDir        = ".",
            sharedLibraries  = None,
            diaryEnabled     = False,
            bufferingEnabled = False):
        '''
        Create an octave component using tags in the function arguments.

        All Octave components will have the following properties:

            bufferingEnabled
            diaryOnOrOff

        '''

        mFunctionParameters = getMFunctionParameters(function, mFiles)

        self.diaryEnabled = str(diaryEnabled).lower()
        self.bufferingEnabled= str(bufferingEnabled).lower()

        ResourcePackage.__init__(
            self,
            name = function,
            outputDir = outputDir,
            generator = "octave",
            mFiles = mFiles)

        self._addDefaultProps()

        nonPropOrKeywordArgs = []
        nonPropOrKeywordArgs.extend(__RESERVED_KEYWORDS__)

        def isStringProp(value):
            if type(value) == type([]):
                # simple sequence
                if len(value) > 0:
                    return value[0].find('"') != -1 or value[0].find("'") != -1
                else:
                    # if empty, assume not a string
                    return False
            else:
                # simple
                return value.find('"') != -1 or value.find("'") != -1

        for propName in mFunctionParameters.defaults.keys():
            value = mFunctionParameters.defaults[propName]
            if type(value) == type([]):
                # simple sequence
                if isStringProp(value):
                    # string
                    for index in range(len(values)):
                        values[index]=_cleanQuotes(values[index])
                    self.addSimpleSequencProperty(
                        id=propName,
                        values=value,
                        type="string",
                        complex=False)
                else:
                    # double
                    self.addSimpleSequencProperty(
                        id=propName,
                        values=value)
            else:
                # simple
                if isStringProp(value):
                    # string
                    value=_cleanQuotes(value)
                    self.addSimpleProperty(
                        id=propName,
                        value=value,
                        type="string",
                        complex=False)
                else:
                    # double
                    self.addSimpleProperty(
                        id=propName,
                        value=value)
            nonPropOrKeywordArgs.append(propName)

        for input in mFunctionParameters.inputs:
            if nonPropOrKeywordArgs.count(input) == 0:
                self.addProvidesPort(input, "IDL:BULKIO/dataDouble:1.0")

        for output in mFunctionParameters.outputs:
            if nonPropOrKeywordArgs.count(output) == 0:
                self.addUsesPort(output, "IDL:BULKIO/dataDouble:1.0")

        for sharedLibrary in sharedLibraries:
            self.addSoftPackageDependency(sharedLibrary)

    def _addDefaultProps(self):
        self.addSimpleProperty(
            complex=False,
            type="boolean",
            id="diaryEnabled",
            value=self.diaryEnabled)

        self.addSimpleProperty(
            complex=False,
            type="boolean",
            id="bufferingEnabled",
            value=self.bufferingEnabled)

        # TODO: fix this
        self.addSimpleProperty(
            complex=False,
            type="double",
            id="sampleRate",
            mode="readonly",
            value="0")

        self.addSimpleProperty(
            complex=False,
            type="string",
            id="__mFunction",
            mode="readonly",
            value=self.name,
            kindtypes=["configure","execparam"])
