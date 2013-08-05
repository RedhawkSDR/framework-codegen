#{% macro simple(prop) %}
#{%   filter codealign %}
${prop.pyname} = simple_property(id_="${prop.identifier}",
#%    if prop.name
                                 name="${prop.name}",
#%    endif
                                 type_="${prop.type}",
#%    if prop.pyvalue is defined
                                 defvalue=${prop.pyvalue},
#%    endif
#%    if prop.isComplex
                                 complex=True,
#%    endif
                                 mode="${prop.mode}",
                                 action="${prop.action}",
                                 kinds=${prop.kinds|quote|tuple}
#%-    if prop.hasDescription
,
                                 description="""${prop.description}"""
#%    endif
                                 )
#{%   endfilter %}
#{% endmacro %}

#{% macro simplesequence(prop) %}
#{%   filter codealign %}
${prop.pyname} = simpleseq_property(id_="${prop.identifier}",
#%    if prop.name
                                    name="${prop.name}",
#%    endif
                                    type_="${prop.type}",
#%    if prop.pyvalue
                                    defvalue=[
#{%   for val in prop.pyvalue %}
                                              ${val},
#{%   endfor %}
                                             ],
#%    else
                                    defvalue=None,
#%    endif
#%    if prop.units
                                    units="${prop.units}",
#%    endif
#%    if prop.isComplex
                                    complex=True,
#%    endif
                                    mode="${prop.mode}",
                                    action="${prop.action}",
                                    kinds=${prop.kinds|quote|tuple}
#%-    if prop.hasDescription
,
                                    description="""${prop.description}"""
#%    endif
                                    )
#{%   endfilter %}
#{% endmacro %}

#{% macro struct(prop) %}
#{%   filter codealign %}
${prop.pyname} = struct_property(id_="${prop.identifier}",
#%    if prop.name
                                 name="${prop.name}",
#%    endif
                                 structdef=${prop.pyclass},
                                 configurationkind=${prop.kinds|quote|tuple},
                                 mode="${prop.mode}"
#%-    if prop.hasDescription
,
                                 description="""${prop.description}"""
#%    endif
                                 )
#{%   endfilter %}
#{% endmacro %}

#{% macro structsequence(prop) %}
#{%   filter codealign %}
${prop.pyname} = structseq_property(id_="${prop.identifier}",
#%    if prop.name
                                    name="${prop.name}",
#%    endif
                                    structdef=${prop.structdef.pyclass},
                                    defvalue=[${prop.pyvalues|join(',')}],
                                    configurationkind=${prop.kinds|quote|tuple},
                                    mode="${prop.mode}"
#%-    if prop.hasDescription
,
                                 description="""${prop.description}"""
#%    endif
                                    )
#{%   endfilter %}
#{% endmacro %}

#{% macro initializer(fields) %}
#{%   filter trim|lines|join(', ') %}
#{%   for field in fields %}
${field.pyname}=${field.pyvalue|default(python.defaultValue(field.type))}
#{%   endfor %}
#{%   endfilter %}
#{% endmacro %}

#{% macro members(fields) %}
#{%   filter trim|lines|join(',') %}
#{%   for field in fields %}
("${field.pyname}",self.${field.pyname})
#{%   endfor %}
#{%   endfilter %}
#{% endmacro %}

#{% macro structdef(struct, initialize=true) %}
class ${struct.pyclass}(object):
#{%   for field in struct.fields %}
#{%   filter codealign %}
    ${field.pyname} = simple_property(id_="${field.identifier}",
#{%     if field.name %}
                                      name="${field.name}",
#{%     endif %}
                                      type_="${field.type}",
#{%     if field.pyvalue %}
                                      defvalue=${field.pyvalue},
#{%     endif %}
#{%     if field.isComplex %}
                                      complex=True,
#{%     endif %}
                                      )
#{%   endfilter %}
#{%   endfor %}

#{%   if initialize: %}
    def __init__(self, **kw):
        """Construct an initialized instance of this struct definition"""
        for attrname, classattr in type(self).__dict__.items():
            if type(classattr) == simple_property:
                classattr.initialize(self)
        for k,v in kw.items():
            setattr(self,k,v)
#{%   else %}
    def __init__(self, ${initializer(struct.fields)}):
#{%     for field in struct.fields %}
        self.${field.pyname} = ${field.pyname}
#{%     endfor %}
#{%   endif %}

    def __str__(self):
        """Return a string representation of this structure"""
        d = {}
#{%   for field in struct.fields %}
        d["${field.pyname}"] = self.${field.pyname}
#{%   endfor %}
        return str(d)

    def getId(self):
        return "${struct.identifier}"

    def isStruct(self):
        return True

    def getMembers(self):
        return [${members(struct.fields)}]
#{% endmacro %}
