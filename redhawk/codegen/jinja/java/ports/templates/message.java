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
//% set classname = portgenerator.className()
package ${package};

import java.util.HashMap;
import java.util.Map;
import org.ossie.component.QueryableUsesPort;
import java.util.ArrayList;
import java.util.List;
import CF.PropertiesHelper;
import CF.DataType;
import org.omg.CORBA.ORB;
import org.omg.CORBA.Any;
import ${component.package}.${component.baseclass.name}.*;
import org.ossie.events.*;

/**
 * @generated
 */
public class ${classname} extends MessageSupplierPort {
    public ${classname}(String portName) {
        super(portName);
    }
/*{% for prop in component.messages %}*/

    public void sendMessage(final ${prop.javatype} message) {
        final List<DataType> outProps = new ArrayList<DataType>();
        final List<DataType> propStruct = new ArrayList<DataType>();
        Any propStruct_any = ORB.init().create_any();
/*{%   for field in prop.fields %}*/
        propStruct.add(new DataType("${field.identifier}", message.${field.javaname}.toAny()));
/*{%   endfor %}*/
        PropertiesHelper.insert(propStruct_any, propStruct.toArray(new DataType[propStruct.size()]));
        outProps.add(new DataType("${prop.identifier}", propStruct_any));
        Any outProps_any = ORB.init().create_any();
        PropertiesHelper.insert(outProps_any, outProps.toArray(new DataType[outProps.size()]));
        this.push(outProps_any);
    }
    
    public void sendMessages(final ArrayList<${prop.javatype}> messages) {
        final List<DataType> outProps = new ArrayList<DataType>();
        for (${prop.javatype} message : messages) {
            final List<DataType> propStruct = new ArrayList<DataType>();
            Any propStruct_any = ORB.init().create_any();
/*{%   for field in prop.fields %}*/
            propStruct.add(new DataType("${field.identifier}", message.${field.javaname}.toAny()));
/*{%   endfor %}*/
            PropertiesHelper.insert(propStruct_any, propStruct.toArray(new DataType[propStruct.size()]));
            outProps.add(new DataType("${prop.identifier}", propStruct_any));
        }
        Any outProps_any = ORB.init().create_any();
        PropertiesHelper.insert(outProps_any, outProps.toArray(new DataType[outProps.size()]));
        this.push(outProps_any);
    }
/*{% endfor %}*/
}
