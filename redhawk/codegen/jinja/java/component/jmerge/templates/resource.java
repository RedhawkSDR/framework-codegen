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
//% set classname = component.userclass.name
//% set superClass = component.superclass.name
//% set artifactType = component.artifacttype
package ${component.package};

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;
import org.omg.CORBA.ORB;
import org.omg.PortableServer.POA;
import org.omg.PortableServer.POAPackage.ServantNotActive;
import org.omg.PortableServer.POAPackage.WrongPolicy;
import org.omg.CosNaming.NamingContextPackage.CannotProceed;
import org.omg.CosNaming.NamingContextPackage.InvalidName;
import org.omg.CosNaming.NamingContextPackage.NotFound;
import CF.PropertiesHolder;
import CF.ResourceHelper;
import CF.UnknownProperties;
/*{% if component is device %}*/
import CF.DevicePackage.AdminType;
import CF.DevicePackage.OperationalType;
import CF.DevicePackage.UsageType;
/*{% endif %}*/
import CF.LifeCyclePackage.InitializeError;
import CF.LifeCyclePackage.ReleaseError;
import CF.InvalidObjectReference;
import CF.PropertySetPackage.InvalidConfiguration;
import CF.PropertySetPackage.PartialConfiguration;
import CF.ResourcePackage.StartError;
import CF.ResourcePackage.StopError;
import CF.DataType;
import org.omg.CORBA.UserException;
import org.omg.CosNaming.NameComponent;
import org.apache.log4j.Logger;
import org.ossie.component.*;
/*{% if component.properties %}*/
import org.ossie.properties.*;
/*{% endif %}*/
/*{% if component.hasbulkio %}*/
import bulkio.*;
/*{% endif %}*/
/*{% filter lines|unique|join('\n') %}*/
/*{%   for portgen in component.portgenerators %}*/
/*{%     if portgen.package %}*/
import ${portgen.package}.${portgen.className()};
/*{%     endif %}*/
/*{%   endfor %}*/
/*{% endfilter %}*/

/*{% filter lines|unique|join('\n') %}*/
/*{%    for prop in component.properties %}*/
/*{%        if prop.CFType %}*/
import CF.${prop.CFType};
/*{%        endif %}*/
/*{%    endfor %}*/
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
public class ${classname} extends ${superClass} implements Runnable {
    /**
     * @generated
     */
    public final static Logger logger = Logger.getLogger(${classname}.class.getName());

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

        //begin-user-code
        //end-user-code
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
        
        //begin-user-code
        //end-user-code
        
    	return retval;
    }

/*{% endif %}*/
    /**
     *
     * Main processing thread
     *
     * <!-- begin-user-doc -->
     * 
     * General functionality:
     * 
     *    This function is running as a separate thread from the ${artifactType}'s main thread. 
     *    
     *    The IDE uses JMerge during the generation (and re-generation) process.  To keep
     *    customizations to this file from being over-written during subsequent generations,
     *    put your customization in between the following tags:
     *      - //begin-user-code
     *      - //end-user-code
     *    or, alternatively, set the @generated flag located before the code you wish to 
     *    modify, in the following way:
     *      - "@generated NOT"
     * 
     * StreamSRI:
     *    To create a StreamSRI object, use the following code:
     *            String stream_id = "testStream";
     * 		  BULKIO.StreamSRI sri = new BULKIO.StreamSRI();
     * 		  sri.mode = 0;
     * 		  sri.xdelta = 0.0;
     * 		  sri.ydelta = 1.0;
     * 		  sri.subsize = 0;
     * 		  sri.xunits = 1; // TIME_S
     * 		  sri.streamID = (stream_id != null) ? stream_id : "";
     * 
     * PrecisionUTCTime:
     *    To create a PrecisionUTCTime object, use the following code:
     * 		  BULKIO.PrecisionUTCTime tstamp = bulkio.time.utils.now();
     * 
     * Ports:
     * 
     *    Each port instance is accessed through members of the following form: this.port_<PORT NAME>
     * 
     *    Data is obtained in the run function through the getPacket call (BULKIO only) on a
     *    provides port member instance. The getPacket function call is non-blocking; it takes
     *    one argument which is the time to wait on new data. If you pass 0, it will return
     *    immediately if no data available (won't wait).
     *    
     *    To send data, call the appropriate function in the port directly. In the case of BULKIO,
     *    convenience functions have been added in the port classes that aid in output.
     *    
     *    Interactions with non-BULKIO ports are left up to the ${artifactType} developer's discretion.
     *    
     * Properties:
     * 
     *    Properties are accessed through members of the same name with helper functions. If the 
     *    property name is baudRate, then reading the value is achieved by: this.baudRate.getValue();
     *    and writing a new value is achieved by: this.baudRate.setValue(new_value);
     *    
     * Example:
     * 
     *    This example assumes that the ${artifactType} has two ports:
     *        - A provides (input) port of type bulkio::InShortPort called dataShort_in
     *        - A uses (output) port of type bulkio::InFloatPort called dataFloat_out
     *    The mapping between the port and the class is found the class of the same name.
     *    This example also makes use of the following Properties:
     *        - A float value called amplitude with a default value of 2.0
     *        - A boolean called increaseAmplitude with a default value of true
     *    
     *    InShortPort.Packet data = this.port_dataShort_in.getPacket(125);
     *
     *    if (data != null) {
     *        float[] outData = new float[data.getData().length];
     *        for (int i = 0; i < data.getData().length; i++) {
     *            if (this.increaseAmplitude.getValue()) {
     *                outData[i] = (float)data.getData()[i] * this.amplitude.getValue();
     *            } else {
     *                outData[i] = (float)data.getData()[i];
     *            }
     *        }
     *
     *        // NOTE: You must make at least one valid pushSRI call
     *        if (data.sriChanged()) {
     *            this.port_dataFloat_out.pushSRI(data.getSRI());
     *        }
     *        this.port_dataFloat_out.pushPacket(outData, data.getTime(), data.getEndOfStream(), data.getStreamID());
     *    }
     *      
     * <!-- end-user-doc -->
     * 
     * @generated
     */
    public void run() 
    {
        //begin-user-code
        //end-user-code
        
        while(this.started())
        {
            //begin-user-code
            // Process data here
            try {
                logger.debug("run() example log message");
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                break;
            }
            
            //end-user-code
        }
        
        //begin-user-code
        //end-user-code
    }

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

        //begin-user-code
        // TODO You may add extra startup code here, for example:
        // orbProps.put("com.sun.CORBA.giop.ORBFragmentSize", Integer.toString(fragSize));
        //end-user-code

        try {
            ${superClass}.start_${artifactType}(${classname}.class, args, orbProps);
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

        //begin-user-code
        // TODO You may add extra shutdown code here
        //end-user-code
    }
}
