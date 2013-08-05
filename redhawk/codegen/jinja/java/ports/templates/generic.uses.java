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

    public void disconnectPort(final String connectionId) {
        // don't want to process while command information is coming in
        synchronized (this.updatingPortsLock) {
            super.disconnectPort(connectionId);
            this.outConnections.remove(connectionId);
            this.active = (this.outConnections.size() != 0);
        }
    }
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
