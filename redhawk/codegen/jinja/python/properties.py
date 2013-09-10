from redhawk.codegen.lang import python

from redhawk.codegen.jinja.mapping import PropertyMapper

class PythonPropertyMapper(PropertyMapper):
    def mapProperty(self, prop):
        pyprop = {}
        if prop.hasName():
            name = prop.name()
        else:
            name = prop.identifier()
        pyprop['pyname'] = python.identifier(prop.name())
        return pyprop

    def mapSimpleProperty(self, simple):
        pyprop = self.mapProperty(simple)
        pyprop['isComplex'] = simple.isComplex()
        if simple.hasValue():
            pyprop['pyvalue'] = python.literal(simple.value(), 
                                               simple.type(), 
                                               simple.isComplex())
        return pyprop

    def mapSimpleSequenceProperty(self, simplesequence):
        pyprop = self.mapProperty(simplesequence)
        pyprop['isComplex'] = simplesequence.isComplex()
        if simplesequence.hasValue():
            pyprop['pyvalue'] = python.sequenceValue(simplesequence.value(), 
                                                     simplesequence.type(), 
                                                     simplesequence.isComplex())
        return pyprop

    def mapStructProperty(self, struct, fields):
        pyprop = self.mapProperty(struct)
        pyprop['pyclass'] = self._structName(struct.name())
        return pyprop

    def mapStructSequenceProperty(self, structsequence, structdef):
        pyprop = self.mapProperty(structsequence)
        if structsequence.hasValue():
            pyprop['pyvalues'] = [self._mapStructValue(v, structdef) for v in structsequence.value()]
        return pyprop

    def _mapStructValue(self, value, structdef):
        args= []
        for f in structdef['fields']:
            if f['type'] == 'string' or f['type'] == 'char':
                args.append('\''+value[f['identifier']]+'\'')
            elif f['type'] == 'boolean':
                args.append(value[f['identifier']].capitalize())
            else:
                args.append(value[f['identifier']])
        return '%s(%s)' % (structdef['pyclass'], ','.join(args))

    def _structName(self, name):
        # For compatiblity with legacy generators, remove trailing "Struct" from name.
        if name.endswith('Struct'):
            name = name[:-6]
        name = name[0].upper() + name[1:]
        return python.identifier(name)
