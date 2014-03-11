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
//% set interface = portgenerator.interfaceClass()
//% set helper = portgenerator.helperClass()
package ${package};

import java.util.HashMap;
import java.util.Map;
import org.ossie.component.QueryableUsesPort;

/**
 * @generated
 */
public class ${classname} extends QueryableUsesPort<${interface}> implements ${interface} {

    /**
     * Map of connection Ids to port objects
     * @generated
     */
    protected Map<String, ${interface}> outConnections = new HashMap<String, ${interface}>();

    /**
     * @generated
     */
    public ${classname}(String portName) 
    {
        super(portName);

        this.outConnections = new HashMap<String, ${interface}>();
        //begin-user-code
        //end-user-code
    }

    /**
     * @generated
     */
    protected ${interface} narrow(org.omg.CORBA.Object connection) 
    {
        ${interface} ops = ${helper}.narrow(connection);
        
        //begin-user-code 
        //end-user-code 
        
        return ops; 
    }

//% if interface != "CF.PortOperations" 
    public void connectPort(final org.omg.CORBA.Object connection, final String connectionId) throws CF.PortPackage.InvalidPort, CF.PortPackage.OccupiedPort
    {
        try {
            // don't want to process while command information is coming in
            synchronized (this.updatingPortsLock) {
                super.connectPort(connection, connectionId);
                final ${interface} port = ${helper}.narrow(connection);
                this.outConnections.put(connectionId, port);
                this.active = true;
            }
        } catch (final Throwable t) {
            t.printStackTrace();
        }

    }

    public void disconnectPort(final String connectionId) throws CF.PortPackage.InvalidPort{
        // don't want to process while command information is coming in
        synchronized (this.updatingPortsLock) {
            super.disconnectPort(connectionId);
            this.outConnections.remove(connectionId);
            this.active = (this.outConnections.size() != 0);
        }
    }
//% endif
/*{% for operation in portgenerator.operations() %}*/

   /**
     * @generated
     */
    public ${operation.returns} ${operation.name}(${operation.arglist})${" throws " + operation.throws if operation.throws}
    {
//% set hasreturn = operation.returns != 'void'
/*{% if hasreturn %}*/
        ${operation.returns} retval = ${java.defaultValue(operation.returns)};

/*{% endif %}*/
        synchronized(this.updatingPortsLock) {    // don't want to process while command information is coming in
            if (this.active) {
                //begin-user-code
                //end-user-code
                
                for (${interface} p : this.outConnections.values()) {
                    ${'retval = ' if hasreturn}p.${operation.name}(${operation.argnames|join(', ')});
                }
            }
        }    // don't want to process while command information is coming in
        
        //begin-user-code
        //end-user-code
        
/*{% if hasreturn %}*/
        return retval;
/*{% else %}*/
        return;
/*{% endif %}*/
    }
 /*{% endfor %}*/
}
