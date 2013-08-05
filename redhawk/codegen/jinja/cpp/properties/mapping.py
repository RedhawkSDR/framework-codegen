from redhawk.codegen.lang import cpp
from redhawk.codegen.lang.idl import IDLInterface

from redhawk.codegen.jinja.mapping import PropertyMapper

class CppPropertyMapper(PropertyMapper):
    def mapProperty(self, prop):
        cppprop = {}
        if prop.hasName():
            name = prop.name()
        else:
            name = prop.identifier()
        cppprop['cppname'] = cpp.identifier(name)
        return cppprop

    def mapSimpleProperty(self, prop):
        cppprop = self.mapProperty(prop)
        cppprop['cpptype'] = cpp.cppType(prop.type(), prop.isComplex())
        if prop.hasValue():
            cppprop['cppvalue'] = cpp.literal(prop.value(), 
                                              prop.type(),
                                              prop.isComplex())
        return cppprop

    def mapSimpleSequenceProperty(self, prop):
        cppprop = self.mapProperty(prop)
        cppprop['cpptype'] = cpp.sequenceType(prop.type(), prop.isComplex())
        if prop.hasValue():
            cppprop['cppvalues'] = [cpp.literal(v, 
                                                prop.type(), 
                                                prop.isComplex()) 
                                    for v in prop.value()]
        return cppprop

    def mapStructProperty(self, prop, fields):
        cppprop = self.mapProperty(prop)
        typename = prop.name()+'_struct'
        cppprop['cpptype'] = typename
        cppprop['cppvalue'] = typename + '()'
        return cppprop

    def mapStructSequenceProperty(self, prop, structdef):
        cppprop = self.mapProperty(prop)
        cppprop['cpptype'] = 'std::vector<%s>' % structdef['cpptype']
        cppprop['cppvalues'] = [self.mapStructValue(structdef, value) for value in prop.value()]
        return cppprop

    def mapStructValue(self, structdef, value):
        newval = {}
        for field in structdef['fields']:
            identifier = field['identifier']
            if identifier in value:
                newval[identifier] = cpp.literal(value[identifier], field['type'])
        return newval
