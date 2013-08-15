/*{% macro initsequence(prop) %}*/
//%   if prop is structsequence
${prop.cppname}.resize(${prop.cppvalues|length});
//%     for value in prop.cppvalues
//%       set index = loop.index0
//%       for field in prop.structdef.fields
${prop.cppname}[${index}].${field.cppname} = ${value[field.identifier]};
//%       endfor
//%     endfor
//%   else
// Set the sequence with its initial values
//%     for value in prop.cppvalues
${prop.cppname}.push_back(${value});
//%     endfor
//%   endif
/*{%- endmacro %}*/

/*{% macro addproperty(prop) %}*/
addProperty(${prop.cppname},
//% if prop.cppvalues
            ${prop.cppname},
//% elif prop.cppvalue
            ${prop.cppvalue},
//% endif
            "${prop.identifier}",
            "${prop.name}",
            "${prop.mode}",
            "${prop.units}",
            "${prop.action}",
            "${prop.kinds|join(',')}");
/*{%- endmacro %}*/

/*{% macro structdef(struct) %}*/
struct ${struct.cpptype} {
    ${struct.cpptype} ()
    {
/*{% for field in struct.fields if field.cppvalue %}*/
        ${field.cppname} = ${field.cppvalue};
/*{% endfor %}*/
    };

    static std::string getId() {
        return std::string("${struct.identifier}");
    };

/*{% for field in struct.fields %}*/
    ${field.cpptype} ${field.cppname};
/*{% endfor %}*/
};

inline bool operator>>= (const CORBA::Any& a, ${struct.cpptype}& s) {
    CF::Properties* temp;
    if (!(a >>= temp)) return false;
    CF::Properties& props = *temp;
    for (unsigned int idx = 0; idx < props.length(); idx++) {
/*{% for field in struct.fields %}*/
        if (!strcmp("${field.identifier}", props[idx].id)) {
/*{% if field.type == 'char' %}*/
/*{%   set extractName = 'temp_char' %}*/
            CORBA::Char temp_char;
/*{% else %}*/
/*{%   set extractName = 's.'+field.cppname %}*/
/*{% endif %}*/
            if (!(props[idx].value >>= ${cpp.extract(extractName, field.type)})) return false;
/*{% if field.type == 'char' %}*/
            s.${field.cppname} = temp_char;
/*{% endif %}*/
        }
/*{% endfor %}*/
    }
    return true;
};

inline void operator<<= (CORBA::Any& a, const ${struct.cpptype}& s) {
    CF::Properties props;
    props.length(${struct.fields|length});
/*{% for field in struct.fields %}*/
    props[${loop.index0}].id = CORBA::string_dup("${field.identifier}");
    props[${loop.index0}].value <<= ${cpp.insert('s.'+field.cppname, field.type)};
/*{% endfor %}*/
    a <<= props;
};

inline bool operator== (const ${struct.cpptype}& s1, const ${struct.cpptype}& s2) {
/*{% for field in struct.fields %}*/
    if (s1.${field.cppname}!=s2.${field.cppname})
        return false;
/*{% endfor %}*/
    return true;
};

inline bool operator!= (const ${struct.cpptype}& s1, const ${struct.cpptype}& s2) {
    return !(s1==s2);
};

template<> inline short StructProperty<${struct.cpptype}>::compare (const CORBA::Any& a) {
    if (super::isNil_) {
        if (a.type()->kind() == (CORBA::tk_null)) {
            return 0;
        }
        return 1;
    }

    ${struct.cpptype} tmp;
    if (fromAny(a, tmp)) {
        if (tmp != this->value_) {
            return 1;
        }

        return 0;
    } else {
        return 1;
    }
}
/*{%- endmacro %}*/
