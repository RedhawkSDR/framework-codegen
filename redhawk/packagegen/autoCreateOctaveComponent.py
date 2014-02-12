from redhawk.codegen.model import softpkg
from redhawk.packagegen import createPackage
import subprocess

# TODO: default values should probably be a class
__DEFAULT_STRING_PROPS__ = ['diaryOnOrOff', 'logDir']
__DEFAULT_DOUBLE_PROPS__ = ['sampleRate', 'bufferingEnabled']

DEFAULTS = {"double" : "0",
            "string" : "."}

def inList(list, itemInQuestion):
    """
    Public.

    Return True if itemInQeustion is already in the list.

    """

    for item in list:
        if item == itemInQuestion:
            return True
    return False

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

def addPropertyIfMissing(
        lines,
        name,
        type,
        default,
        kindtype=''):
    '''
    Check for an existing property of the same name.  If it already exists,
    use the existing one, as it might have a particular default value; otherwise,
    create a new property.

    '''

    addProp = True
    declaration = 'prop ' + name + ' ' + type
    for line in lines:
        if line.find(declaration) != -1:
            addProp = False
    if addProp:
        lines.append(declaration + ' ' + str(default) + ' ' + kindtype)
    return lines

def create(
    mFiles,
    function,
    portTag,
    propTag,
    complexPropTag,
    stringTag,
    buildRpm         = False,
    install          = False,
    propertyDefaults = {},
    outputDir        = ".",
    force            = False,
    sharedLibraries  = None,
    diaryEnabled     = False,
    bufferingEnabled = True):
    '''
    Create an octave component using tags in the function arguments.

    All Octave components will have the follwing properties:

        logDir
        sampleRate
        bufferingEnabled
        diaryOnOrOff

    '''

    if bufferingEnabled:
        bufferingEnabledStr = '1'
    else:
        bufferingEnabledStr = '0'

    if diaryEnabled == True:
        diaryOnOrOffStr = 'on'
    else:
        diaryOnOrOffStr = 'off'

    # Need defaults for the implied properties
    # sampleRate and logDir values don't really matter since
    # the are effectively read only
    propertyDefaults['sampleRate'       ] = '-1'
    propertyDefaults['logDir'           ] = DEFAULTS['string']
    propertyDefaults['diaryOnOrOff'     ] = diaryOnOrOffStr
    propertyDefaults['bufferingEnabled' ] = bufferingEnabledStr

    mFunctionParameters = None

    # find the master m file and parse its m function
    for mFile in mFiles:
        if mFile.find(function + '.m') != -1:
            mFunctionParameters = softpkg.parseMFile(mFile)
            break
    if mFunctionParameters is None:
        raise SystemExit('ERROR: No matching m file for specified function')

    properties        = []
    complexProperties = []
    stringProperties  = []
    inputPorts        = []
    outputPorts       = []

    # Categorize function inputs as ports, prop, or string props
    for input in mFunctionParameters.inputs:
        if input.find(portTag) == 0:
            inputPorts.append(input)
        elif input.find(propTag) == 0:
            if not inList(properties, input):
                properties.append(input)
        elif input.find(complexPropTag) == 0:
            if not inList(complexProperties, input):
                complexProperties.append(input)
        elif input.find(stringTag) == 0:
            if not inList(stringProperties, input):
                stringProperties.append(input)
        elif inList(__DEFAULT_DOUBLE_PROPS__, input):
            if not inList(properties, input):
                properties.append(input)
        elif inList(__DEFAULT_STRING_PROPS__, input):
            if not inList(stringProperties, input):
                stringProperties.append(input)
        else:
            ambiguousArgumentException(
                input,
                validTags=[portTag, propTag, stringTag])

    # Categorize function outputs as ports, prop, or string props
    for output in mFunctionParameters.outputs:
        if output.find(portTag) == 0:
            outputPorts.append(output)
        elif output.find(propTag) == 0:
            if not inList(properties, output):
                properties.append(output)
        elif output.find(complexPropTag) == 0:
            if not inList(complexProperties, output):
                complexProperties.append(output)
        elif output.find(stringTag) == 0:
            if not inList(stringProperties, output):
                stringProperties.append(output)
        elif inList(__DEFAULT_DOUBLE_PROPS__, output):
            if not inList(properties, output):
                properties.append(output)
        elif inList(__DEFAULT_STRING_PROPS__, output):
            if not inList(stringProperties, output):
                stringProperties.append(output)
        else:
            ambiguousArgumentException(
                output,
                validTags=[portTag, propTag, stringTag])

    lines = []

    # Create port entries
    for output in outputPorts:
        lines.append('port ' + output + ' double output')
    for input in inputPorts:
        lines.append('port ' + input + ' double input')

    # Create double property entries
    for property in properties:
        if propertyDefaults.has_key(property):
            default = propertyDefaults[property]
        else:
            print "Setting default value for " + property + " to " + DEFAULTS['double']
            default= DEFAULTS['double']
        lines.append('prop ' + property + ' double ' + default)

    # Create double property entries
    for property in complexProperties:
        if propertyDefaults.has_key(property):
            default = propertyDefaults[property]
        else:
            print "Setting default value for " + property + " to [" + DEFAULTS['double'] + "]"
            default = DEFAULTS['double']

        lines.append('prop ' + property + ' complexdouble ' + default)

    # Create string property values
    for property in stringProperties:
        if propertyDefaults.has_key(property):
            default = propertyDefaults[property]
        else:
            print "Setting default value for " + property + " to " +  DEFAULTS['string']
            default = DEFAULTS['string']

        lines.append('prop ' + property + ' string ' + default)


    # Create standard properties
    class Default:
        def __init__(self, name, type, kindtype=''):
            self.name = name
            self.type = type
            self.kindtype = kindtype

    defaults = [Default('logDir',           'string'),
                Default('sampleRate',       'double'),
                Default('diaryOnOrOff',     'string'),
                Default('bufferingEnabled', 'double')]
    for default in defaults:
        lines = addPropertyIfMissing(
            lines,
            name     = default.name,
            type     = default.type,
            default  = propertyDefaults[default.name],
            kindtype = default.kindtype)

    # Write out lines related to the function name
    lines.append('name ' + function)
    lines.append('prop __mFunction string ' + function)

    lines.append('generator octave')

    # Create entries for soft package dependencies
    for dep in sharedLibraries:
        lines.append('dependency ' + dep)

    createPackage.create(
        config     = lines,
        outputDir  = outputDir,
        mFiles     = mFiles,
        force      = force,
        buildRpm   = buildRpm,
        install    = install)
