//% set interface = component.interface
//% set operations = component.operations
//% set attributes = component.attributes
//% set mainclass = component.mainclass
//% set namespace = component.namespace
//% set imports = component.imports
//% set userclass = component.userclass.name

package ${component.package};

import java.lang.reflect.InvocationTargetException;
import java.util.Map;
import java.util.Properties;
import org.apache.log4j.Logger;

import org.ossie.component.Service;
import CF.InvalidObjectReference;

import org.omg.PortableServer.POA;
import org.omg.PortableServer.Servant;

import ${imports}${namespace}.${interface}Operations;
import ${imports}${namespace}.${interface}POATie;

/**
 * @generated
 */

public class ${userclass} extends Service implements ${interface}Operations
{
    public final static Logger logger = Logger.getLogger(${userclass}.class.getName());

    public ${userclass}(Map<String, String> execparams)
    {
    }

    public void terminateService()
    {
    }

/*{% for function in operations %}*/
    public ${function.returns} ${function.name} (${function.arglist}) ${"throws " + function.throws if function.throws}
    {
        // TODO
/*{% if function.returns != 'void' %}*/
        return ${java.defaultValue(function.returns)};
/*{% endif %}*/
    }

/*{% endfor %}*/
/*{% for attr in attributes %}*/
    // ${attr.name} getter
    public ${attr.type} ${attr.name} ()
    {
        // TODO
        return ${java.defaultValue(attr.type)};
    }
/*{% if attr.readonly != 1 %}*/

    // ${attr.name} setter
    public void ${attr.name} (${attr.type} new_${attr.name})
    {
        // TODO
    }
/*{% endif %}*/

/*{% endfor %}*/
    protected Servant newServant(final POA poa)
    {
        return new ${interface}POATie(this, poa);
    }

    public static void main (String[] args)
    {
        final Properties orbProps = new Properties();
        try {
            Service.start_service(${userclass}.class, args, orbProps);
        } catch (InvalidObjectReference e) {
            e.printStackTrace();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();  
        } catch (NoSuchMethodException e) {
            logger.error("Service must immplement constructor: ${userclass}(Map<String,String> execparams)");
        }
    }
}

