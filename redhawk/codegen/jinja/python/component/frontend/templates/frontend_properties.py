#{#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK core.
#
# REDHAWK core is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#}
#{% import "base/properties.py" as properties with context %}

#{% macro inheritedinitializer(fields) %}
#{%   filter trim|lines|join(', ') %}
#{%   for field in fields if field.inherited %}
${field.pyname}=${field.pyname}
#{%   endfor %}
#{%   endfilter %}
#{% endmacro %}

#{% macro notinheritedmembers(fields) %}
#{%   filter trim|lines|join(',') %}
#{%   for field in fields if not field.inherited %}
("${field.pyname}",self.${field.pyname})
#{%   endfor %}
#{%   endfilter %}
#{% endmacro %}

#{% macro frontendstructdef(struct) %}
        class ${struct.pyclass}(${struct.baseclass}):
#{%   for field in struct.fields if not field.inherited %}
#{%   filter codealign %}
            ${field.pyname} = simple_property(id_="${field.identifier}",
#%      if field.name
                                          name="${field.name}",
#%      endif
                                          type_="${field.type}"
#%-     if field.pyvalue is defined
        ,
                                          defvalue=${field.pyvalue}
#%-     endif
#%-     if field.isComplex
        ,
                                          complex=True
#%-     endif
        )
#{%   endfilter %}

#{%   endfor %}
            def __init__(self, ${properties.initializer(struct.fields)}):
                ${struct.baseclass}.__init__(self, ${inheritedinitializer(struct.fields)})
#{%     for field in struct.fields if not field.inherited %}
                self.${field.pyname} = ${field.pyname}
#{%     endfor %}

            def __str__(self):
                """Return a string representation of this structure"""
                d = ${struct.baseclass}.__str__(self) 
#{%   for field in struct.fields if not field.inherited %}
                d["${field.pyname}"] = self.${field.pyname}
#{%   endfor %}
                return str(d)

            def getId(self):
                return "${struct.identifier}"

            def isStruct(self):
                return True

            def getMembers(self):
                return ${struct.baseclass}.getMembers(self) + [${notinheritedmembers(struct.fields)}]
#{% endmacro %}
