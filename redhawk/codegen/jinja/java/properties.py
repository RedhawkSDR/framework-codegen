from redhawk.codegen.lang import java
from redhawk.codegen.lang.idl import CorbaTypes

from redhawk.codegen.jinja.mapping import PropertyMapper

from ossie import properties

# CORBA type to native Java
_propertyType = {
    CorbaTypes.OCTET:     java.Types.BYTE,
    CorbaTypes.BOOLEAN:   java.Types.BOOLEAN,
    CorbaTypes.CHAR:      java.Types.CHAR,
    CorbaTypes.SHORT:     java.Types.SHORT,
    CorbaTypes.USHORT:    java.Types.SHORT,
    CorbaTypes.LONG:      java.Types.INT,
    CorbaTypes.ULONG:     java.Types.INT,
    CorbaTypes.LONGLONG:  java.Types.LONG,
    CorbaTypes.ULONGLONG: java.Types.LONG,
    CorbaTypes.FLOAT:     java.Types.FLOAT,
    CorbaTypes.DOUBLE:    java.Types.DOUBLE,
    CorbaTypes.STRING:    'String',
    CorbaTypes.OBJREF:    'String'
}

# CORBA type to Java property container prefix
_propertyClass = {
    CorbaTypes.OCTET:     'Octet',
    CorbaTypes.BOOLEAN:   'Boolean',
    CorbaTypes.CHAR:      'Char',
    CorbaTypes.SHORT:     'Short',
    CorbaTypes.USHORT:    'UShort',
    CorbaTypes.LONG:      'Long',
    CorbaTypes.ULONG:     'ULong',
    CorbaTypes.LONGLONG:  'LongLong',
    CorbaTypes.ULONGLONG: 'ULongLong',
    CorbaTypes.FLOAT:     'Float',
    CorbaTypes.DOUBLE:    'Double',
    CorbaTypes.STRING:    'String',
    CorbaTypes.OBJREF:    'Objref'
}

class JavaPropertyMapper(PropertyMapper):
    def mapProperty(self, prop):
        javaprop = {}
        if prop.hasName():
            name = prop.name()
        else:
            name = prop.identifier()
        javaprop['javaname'] = java.identifier(name)
        javaprop['javakinds'] = ['Kind.'+k.upper() for k in prop.kinds()]
        return javaprop

    def javaType(self, typename):
        return _propertyType[typename]

    def javaClass(self, typename):
        return _propertyClass[typename]

    def _createComplexJavaProp(self, prop):
        '''
        Create a javaprop that may or may not be complex.
        '''
        javaprop = self.mapProperty(prop)
        javaprop['isComplex'] = prop.isComplex()
        if prop.isComplex():
            javaprop['javatype'] = properties.mapComplexType(prop.type())
            javaprop['CFType']   = javaprop['javatype']
            javaprop['javaclass'] = 'Complex'+self.javaClass(prop.type())
            javatype             = javaprop['javatype']
        else:
            javatype = self.javaType(prop.type())
            javaprop['javaclass'] = self.javaClass(prop.type())
            javaprop['javatype'] = java.boxedType(javatype)
        return javaprop, javatype
 
    def mapSimpleProperty(self, prop):
        javaprop, javatype = self._createComplexJavaProp(prop)

        if prop.hasValue():
            value = java.literal(prop.value(), 
                                 javatype, 
                                 complex = prop.isComplex())
        else:
            value = java.NULL
        javaprop['javavalue'] = value

        return javaprop

    def mapSimpleSequenceProperty(self, prop):
        javaprop, javatype = self._createComplexJavaProp(prop)
        if prop.hasValue():
            values = []
            for value in prop.value(): 
                values.append(java.literal(value,
                                           javatype,
                                           complex = prop.isComplex()))
            javaprop['javavalues'] = values

        return javaprop

    def mapStructProperty(self, prop, fields):
        javaprop = self.mapProperty(prop)
        javaprop['javatype'] = javaprop['javaname'] + '_struct'
        return javaprop

    def mapStructSequenceProperty(self, prop, structdef):
        javaprop = self.mapProperty(prop)
        javaprop['javatype'] = 'ArrayList<%s>' % structdef['javatype']
        javaprop['javavalues'] = [self.mapStructValue(structdef, value) for value in prop.value()]
        return javaprop

    def mapStructValue(self, structdef, value):
        newval = []
        for field in structdef['fields']:
            identifier = field['identifier']
            if identifier in value:
                itemvalue = value[identifier]
            else:
                itemvalue = field.get('value', None)
            if itemvalue is not None:
                newval.append(java.literal(itemvalue, field['javatype']))
            else:
                newval.append(java.NULL)
        return newval
