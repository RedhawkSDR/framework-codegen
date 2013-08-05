/*{% macro header(prop) %}*/
/**
 * The property ${prop.identifier}
 * ${prop.description|default("If the meaning of this property isn't clear, a description should be added.", true)}
 *
 * @generated
 */
/*{%- endmacro %}*/

/*{% macro structdef(prop) %}*/
/**
 * The structure for property ${prop.identifier}
 * 
 * @generated
 */
public static class ${prop.javatype} extends StructDef {
/*{% for field in prop.fields %}*/
    ${simple(field)|indent(4)}
/*{% endfor %}*/

    /**
     * @generated
     */
    public ${prop.javatype}(
/*{%- filter trim|lines|join(', ') %}*/
/*{%   for field in prop.fields %}*/
${field.javatype} ${field.javaname}
/*{%   endfor %}*/
/*{% endfilter -%}*/
) {
        this();
/*{% for field in prop.fields %}*/
        this.${field.javaname}.setValue(${field.javaname});
/*{% endfor %}*/
    }

    /**
     * @generated
     */
    public ${prop.javatype}() {
/*{% for field in prop.fields %}*/
        addElement(this.${field.javaname});
/*{% endfor %}*/
    }
};
/*{%- endmacro %}*/

/*{% macro simple(prop) %}*/
${header(prop)}
public final ${prop.javaclass}Property ${prop.javaname} =
    new ${prop.javaclass}Property(
        "${prop.identifier}", //id
        ${java.stringLiteral(prop.name) if prop.name else java.NULL}, //name
        ${prop.javavalue}, //default value
        Mode.${prop.mode|upper}, //mode
        Action.${prop.action|upper}, //action
        new Kind[] {${prop.javakinds|join(',')}} //kind
        );
/*{% endmacro %}*/

/*{% macro simplesequence(prop) %}*/
${header(prop)}
public final ${prop.javaclass}SequenceProperty ${prop.javaname} =
    new ${prop.javaclass}SequenceProperty(
        "${prop.identifier}", //id
        ${java.stringLiteral(prop.name) if prop.name else java.NULL}, //name
        ${prop.javaclass}SequenceProperty.asList(${prop.javavalues|join(',')}), //default value
        Mode.${prop.mode|upper}, //mode
        Action.${prop.action|upper}, //action
        new Kind[] {${prop.javakinds|join(',')}} //kind
        );
/*{% endmacro %}*/

/*{% macro struct(prop) %}*/
${structdef(prop)}

${header(prop)}
public final StructProperty<${prop.javatype}> ${prop.javaname} =
    new StructProperty<${prop.javatype}>(
        "${prop.identifier}", //id
        ${java.stringLiteral(prop.name) if prop.name else java.NULL}, //name
        ${prop.javatype}.class, //type
        new ${prop.javatype}(), //default value
        Mode.${prop.mode|upper}, //mode
        new Kind[] {${prop.javakinds|join(',')}} //kind
        );
/*{% endmacro %}*/

/*{% macro structsequence(prop) %}*/
${structdef(prop.structdef)}

${header(prop)}
public final StructSequenceProperty<${prop.structdef.javatype}> ${prop.javaname} =
    new StructSequenceProperty<${prop.structdef.javatype}> (
        "${prop.identifier}", //id
        ${java.stringLiteral(prop.name) if prop.name else java.NULL}, //name
        ${prop.structdef.javatype}.class, //type
/*{% if prop.javavalues %}*/
        StructSequenceProperty.asList(
/*{%   filter trim|lines|join(',\n')|indent(12, true) %}*/
/*{%     for values in prop.javavalues %}*/
            new ${prop.structdef.javatype}(${values|join(', ')})
/*{%     endfor %}*/
/*{%   endfilter %}*/

            ), //defaultValue
/*{% else %}*/
        StructSequenceProperty.<${prop.structdef.javatype}>asList(), //defaultValue
/*{% endif %}*/
        Mode.${prop.mode|upper}, //mode
        new Kind[] { ${prop.javakinds|join(',')} } //kind
    );
/*{% endmacro %}*/

/*{% macro structsequence_init(prop) %}*/
/*{% endmacro %}*/
