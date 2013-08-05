#ifndef STRUCTPROPS_H
#define STRUCTPROPS_H

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

*******************************************************************************************/

#include <ossie/CorbaUtils.h>
#include <ossie/PropertyInterface.h>

/*{% from "properties/properties.cpp" import structdef with context %}*/
/*{% for struct in component.structdefs %}*/
${structdef(struct)}

/*{% endfor %}*/
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

#endif
