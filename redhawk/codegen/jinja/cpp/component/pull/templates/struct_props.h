/*#
 * This file is protected by Copyright. Please refer to the COPYRIGHT file 
 * distributed with this source distribution.
 * 
 * This file is part of REDHAWK core.
 * 
 * REDHAWK core is free software: you can redistribute it and/or modify it 
 * under the terms of the GNU Lesser General Public License as published by the 
 * Free Software Foundation, either version 3 of the License, or (at your 
 * option) any later version.
 * 
 * REDHAWK core is distributed in the hope that it will be useful, but WITHOUT 
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License 
 * for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License 
 * along with this program.  If not, see http://www.gnu.org/licenses/.
 #*/
/*{% block license %}*/
/*# Allow child templates to include license #*/
/*{% endblock %}*/
/*{% block header %}*/
#ifndef STRUCTPROPS_H
#define STRUCTPROPS_H

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

*******************************************************************************************/
/*{% endblock %}*/

/*{% block includes %}*/
#include <ossie/CorbaUtils.h>
#include <ossie/PropertyInterface.h>
/*{% endblock %}*/

/*{% block struct %}*/
/*{% from "properties/properties.cpp" import structdef with context %}*/
/*{% for struct in component.structdefs %}*/
${structdef(struct)}

/*{% endfor %}*/
/*{% endblock %}*/

/*{% block structSequence %}*/
/*{% for prop in component.properties if prop is structsequence %}*/
inline bool operator== (const ${prop.cpptype}& s1, const ${prop.cpptype}& s2) {
    if (s1.size() != s2.size()) {
        return false;
    }
    for (unsigned int i=0; i<s1.size(); i++) {
        if (s1[i] != s2[i]) {
            return false;
        }
    }
    return true;
};

inline bool operator!= (const ${prop.cpptype}& s1, const ${prop.cpptype}& s2) {
    return !(s1==s2);
};

template<> inline short StructSequenceProperty<${prop.structdef.cpptype}>::compare (const CORBA::Any& a) {
    if (super::isNil_) {
        if (a.type()->kind() == (CORBA::tk_null)) {
            return 0;
        }
        return 1;
    }

    ${prop.cpptype} tmp;
    if (fromAny(a, tmp)) {
        if (tmp != this->value_) {
            return 1;
        }

        return 0;
    } else {
        return 1;
    }
}
/*{% endfor %}*/
/*{% endblock %}*/

#endif
