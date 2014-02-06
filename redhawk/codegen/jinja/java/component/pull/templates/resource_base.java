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
//% set userclass = component.userclass.name
//% set classname = component.baseclass.name
//% set superClass = component.superclass.name
//% set artifactType = component.artifacttype
package ${component.package};

/*{% if component is device %}*/
import java.util.HashMap;
/*{% endif %}*/
import java.util.Properties;

import org.apache.log4j.Logger;

/*{% if component.events %}*/
import org.omg.CORBA.ORB;
/*{% endif %}*/
/*{% if component is not device %}*/
import org.omg.CosNaming.NamingContextPackage.CannotProceed;
import org.omg.CosNaming.NamingContextPackage.InvalidName;
import org.omg.CosNaming.NamingContextPackage.NotFound;
/*{% endif %}*/
/*{% if component.events %}*/
import org.omg.PortableServer.POA;
/*{% endif %}*/
import org.omg.PortableServer.POAPackage.ServantNotActive;
import org.omg.PortableServer.POAPackage.WrongPolicy;

/*{% if component is device %}*/
import CF.DevicePackage.AdminType;
import CF.DevicePackage.OperationalType;
import CF.DevicePackage.UsageType;
/*{% endif %}*/
import CF.InvalidObjectReference;
/*{% filter lines|unique|join('\n') %}*/
/*{%    for prop in component.properties %}*/
/*{%        if prop.CFType %}*/
import CF.${prop.CFType};
/*{%        endif %}*/
/*{%    endfor %}*/
/*{% endfilter %}*/

import org.ossie.component.*;
/*{% if component.properties %}*/
import org.ossie.properties.*;
/*{% endif %}*/
/*{% filter lines|unique|join('\n') %}*/
/*{%   for portgen in component.portgenerators %}*/
/*{%     if loop.first %}*/

/*{%     endif %}*/
/*{%     if portgen.package %}*/
import ${portgen.package}.${portgen.className()};
/*{%     endif %}*/

/*{%   endfor %}*/
/*{% endfilter %}*/

/**
 * This is the ${artifactType} code. This file contains all the access points
 * you need to use to be able to access all input and output ports,
 * respond to incoming data, and perform general ${artifactType} housekeeping
 *
 * Source: ${component.profile.spd}
 *
 * @generated
 */
public abstract class ${classname} extends ${superClass} implements Runnable {
    /**
     * @generated
     */
    public final static Logger logger = Logger.getLogger(${classname}.class.getName());

    /**
     * Return values for service function.
     */
    public final static int FINISH = -1;
    public final static int NOOP   = 0;
    public final static int NORMAL = 1;

/*{% import "base/properties.java" as properties with context %}*/
/*{% for prop in component.properties %}*/
/*{%   if prop is simple %}*/
    ${properties.simple(prop)|indent(4)}
/*{%   elif prop is simplesequence %}*/
    ${properties.simplesequence(prop)|indent(4)}
/*{%   elif prop is struct %}*/
    ${properties.struct(prop)|indent(4)}
/*{%   elif prop is structsequence %}*/
    ${properties.structsequence(prop)|indent(4)}
/*{%   endif %}*/

/*{% endfor %}*/
    // Provides/inputs
/*{% for port in component.ports if port is provides %}*/
    /**
     * @generated
     */
    public ${port.javatype} ${port.javaname};

/*{% endfor %}*/
    // Uses/outputs
/*{% for port in component.ports if port is uses %}*/
    /**
     * @generated
     */
    public ${port.javatype} ${port.javaname};

/*{% endfor %}*/
    /**
     * @generated
     */
    public ${classname}()
    {
        super();
/*{% if component is device %}*/
        this.usageState = UsageType.IDLE;
        this.operationState = OperationalType.ENABLED;
        this.adminState = AdminType.UNLOCKED;
        this.callbacks = new HashMap<String, AllocCapacity>();
/*{% endif %}*/
/*{% for prop in component.properties if prop is structsequence %}*/
        ${properties.structsequence_init(prop)|indent(8)}
/*{% endfor %}*/
/*{% for prop in component.properties %}*/
        addProperty(${prop.javaname});
/*{% endfor %}*/

        // Provides/input
/*{% for port in component.ports if port is provides %}*/
        this.${port.javaname} = new ${port.constructor};
        this.addPort("${port.name}", this.${port.javaname});
/*{% endfor %}*/

        // Uses/output
/*{% for port in component.ports if port is uses %}*/
        this.${port.javaname} = new ${port.constructor};
        this.addPort("${port.name}", this.${port.javaname});
/*{% endfor %}*/
    }

/*{% if component.events %}*/
    /**
     * @generated
     */
    public CF.Resource setup(final String compId, final String compName, final ORB orb, final POA poa) throws ServantNotActive, WrongPolicy
    {
    	CF.Resource retval = super.setup(compId, compName, orb, poa);
    	
/*{% for prop in component.events %}*/
        this.port_propEvent.registerProperty(this.compId, this.compName, this.${prop.javaname});
/*{% endfor %}*/
        
        this.registerPropertyChangePort(this.port_propEvent);
        
    	return retval;
    }

/*{% endif %}*/
    public void start() throws CF.ResourcePackage.StartError
    {
/*{% for port in component.ports if port.start %}*/
        this.${port.javaname}.${port.start};
/*{% endfor %}*/
        super.start();
    }

    public void stop() throws CF.ResourcePackage.StopError
    {
/*{% for port in component.ports if port.stop %}*/
        this.${port.javaname}.${port.stop};
/*{% endfor %}*/
        super.stop();
    }

    public void run() 
    {
        while(this.started())
        {
            int state = this.serviceFunction();
            if (state == NOOP) {
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    break;
                }
            } else if (state == FINISH) {
                return;
            }
        }
    }

    protected abstract int serviceFunction();

    /**
     * The main function of your ${artifactType}.  If no args are provided, then the
     * CORBA object is not bound to an SCA Domain or NamingService and can
     * be run as a standard Java application.
     * 
     * @param args
     * @generated
     */
    public static void main(String[] args) 
    {
        final Properties orbProps = new Properties();
        ${userclass}.configureOrb(orbProps);

        try {
            ${superClass}.start_${artifactType}(${userclass}.class, args, orbProps);
        } catch (InvalidObjectReference e) {
            e.printStackTrace();
/*{% if component is not device %}*/
        } catch (NotFound e) {
            e.printStackTrace();
        } catch (CannotProceed e) {
            e.printStackTrace();
        } catch (InvalidName e) {
            e.printStackTrace();
/*{% endif %}*/
        } catch (ServantNotActive e) {
            e.printStackTrace();
        } catch (WrongPolicy e) {
            e.printStackTrace();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
    }
}
