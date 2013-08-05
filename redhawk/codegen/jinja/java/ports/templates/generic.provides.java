//% set classname = portgenerator.className()
package ${package};

import ${component.package}.${component.baseclass.name};

/**
 * @generated
 */
public class ${classname} extends ${portgenerator.poaClass()} {

    /**
     * @generated
     */
    protected ${component.baseclass.name} parent;

    /**
     * @generated
     */
    protected String name;

    /**
     * @generated
     */
    public ${classname}(${component.baseclass.name} parent, String portName)
    {
        this.parent = parent;
        this.name = portName;

        //begin-user-code
        //end-user-code
    }
/*{% for operation in portgenerator.operations() %}*/

    /**
     * @generated
     */
    public ${operation.returns} ${operation.name}(${operation.arglist})${" throws " + operation.throws if operation.throws}
    {
        //begin-user-code
        // TODO you must provide an implementation for this port.
/*{% if operation.returns != 'void' %}*/
    /*{%   if operation.returns == 'org.omg.CORBA.Object' %}*/
        return null;
/*{%   else %}*/
        return ${java.defaultValue(operation.returns)};
/*{%   endif %}*/
/*{% endif %}*/
        //end-user-code
    }
/*{% endfor %}*/
}
