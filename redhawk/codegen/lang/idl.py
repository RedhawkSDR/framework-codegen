import os
from ossie.utils.sca import importIDL

from redhawk.codegen.utils import strenum

CorbaTypes = strenum('octet','boolean','char','short','ushort','long','ulong',
                     'longlong','ulonglong','float','double','string','objref')

# Cached mapping of IDL repository IDs to interfaces
idlRepo = {}

class IDLInterface(object):
    def __init__(self, repid):
        self.__repid = repid
        self.__namespace, self.__interface = self.__repid.split(':')[1].rsplit('/', 1)
        self.__idl = None

    def repid(self):
        return self.__repid

    def namespace(self):
        return self.__namespace

    def interface(self):
        return self.__interface

    def idl(self):
        if not self.__idl:
            # NB: This may be a costly operation, as it will parse most of the IDL
            #     files known to REDHAWK on the first invocation; it's not strictly
            #     necessary unless looking at the operations or attributes.
            self.__idl = findInterface(self.repid())
        return self.__idl

    def operations(self):
        return self.idl().operations

    def attributes(self):
        return self.idl().attributes

def findInterface(repid):
    # Return immediately if the repository ID is already in the cache
    global idlRepo
    if repid in idlRepo:
        return idlRepo[repid]

    namespace = IDLInterface(repid).namespace()
    if namespace.startswith('omg.org'):
        includePaths = []
        includePaths.append('/usr/local/share/idl/omniORB')
        includePaths.append('/usr/share/idl/omniORB')
        includePaths.append('/usr/local/share/idl/omniORB/COS')
        includePaths.append('/usr/share/idl/omniORB/COS')
        idlRepo.update((interface.repoId, interface) for interface in findInterfacesByPath(namespace, '/usr/share/idl/omniORB/COS', includePaths))
    elif 'IDL:CF/Resource:1.0' not in idlRepo:
        idlRepo.update((interface.repoId, interface) for interface in importIDL.importStandardIdl())

    # Try to find the interface again; if it is not in the cache by now, we
    # don't know anything about it.
    if repid in idlRepo:
        return idlRepo[repid]
    else:
        raise KeyError, 'Unsupported IDL interface', repid

def findInterfacesByPath(namespace, path, includes):
    namespace = namespace.split('/')[1] + '.idl'
    ints = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name == namespace:
                ints.extend(importIDL.getInterfacesFromFile(os.path.join(root, name), includes))
    return ints
