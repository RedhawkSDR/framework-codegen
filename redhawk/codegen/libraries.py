from redhawk.codegen.lang import python

import versions

redhawkLibs = {
    'BULKIO': {
        'libname':    'bulkio',
        'interfaces': 'bulkioInterfaces',
        'rpmname':    'bulkioInterfaces',
        'version':    versions.bulkio,
        'pymodule':   'bulkio',
        'jarfiles':   ('bulkio.jar', 'BULKIOInterfaces.jar')
    },
    'BURSTIO': {
        'libname':    'burstio',
        'interfaces': 'burstioInterfaces',
        'rpmname':    'burstioInterfaces',
        'version':    versions.burstio,
        'pymodule':   'redhawk.burstio',
        'jarfiles':   ('burstio.jar', 'BURSTIOInterfaces.jar')
    },
    'FRONTEND': {
        'libname':    'frontend',
        'interfaces': 'frontendInterfaces',
        'rpmname':    'frontendInterfaces',
        'version':    versions.frontend,
        'pymodule':   'frontend',
        'jarfiles':   ('FRONTENDInterfaces.jar',)
    }
}

def getInterfaceLibrary(namespace):
    if namespace in redhawkLibs:
        return redhawkLibs[namespace]
    else:
        name = namespace.lower() + 'Interfaces'
        library = {
            'libname': name,
            'interfaces': name,
            'rpmname': name,
            'version': None,
            'pymodule': python.idlModule(namespace),
            'jarfiles': (namespace + 'Interfaces.jar',)
        }
        return library

def getPackageRequires(namespace):
    library = getInterfaceLibrary(namespace)
    if library['version']:
        return '%s >= %s' % (library['libname'], library['version'])
    else:
        return library['libname']

def getRPMDependency(name):
    library = getInterfaceLibrary(name)
    if library['version']:
        return '%s >= %s' % (library['rpmname'], library['version'])
    else:
        return library['interfaces']
