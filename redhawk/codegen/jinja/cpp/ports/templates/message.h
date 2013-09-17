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
//% set className = portgen.className()
class ${className} : public MessageSupplierPort
{
    public:
        ${className}(std::string port_name) : MessageSupplierPort(port_name) {
        };
/*{% for property in component.messages %}*/
/*{%   set msgtype = property.cpptype %}*/
/*{%   set vectype = 'std::vector<'+msgtype+'>' %}*/

        void sendMessage(${msgtype} message) {
            CF::Properties outProps;
            CORBA::Any data;
            outProps.length(1);
            outProps[0].id = CORBA::string_dup(message.getId().c_str());
            outProps[0].value <<= message;
            data <<= outProps;
            push(data);
        }

        void sendMessages(${vectype|replace('>>', '> >')} messages) {
            CF::Properties outProps;
            CORBA::Any data;
            outProps.length(messages.size());
            for (unsigned int i=0; i<messages.size(); i++) {
                outProps[i].id = CORBA::string_dup(messages[i].getId().c_str());
                outProps[i].value <<= messages[i];
            }
            data <<= outProps;
            push(data);
        }
/*{% endfor %}*/
};

