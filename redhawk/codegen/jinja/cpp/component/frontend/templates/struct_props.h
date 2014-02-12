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
/*{% block header %}*/
#ifndef STRUCTPROPS_H
#define STRUCTPROPS_H

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

*******************************************************************************************/
/*{% endblock %}*/

/*{% block includes %}*/
#include <ossie/CorbaUtils.h>
#include <ossie/PropertyInterface.h>
/*{% set includedFile = False %}*/
/*{% for struct in component.structdefs %}*/
/*{%   if struct.cppname == "frontend_tuner_status_struct" and
           includedFile == False %}*/
#include <frontend/fe_tuner_struct_props.h>
/*{%     set includedFile = True %}*/
/*{%   endif %}*/
/*{% endfor %}*/
/*{% if component.hasmultioutport %}*/ 
#include <bulkio/bulkio.h>
typedef bulkio::connection_descriptor_struct connection_descriptor_struct;
/*{% endif %}*/
/*{% endblock %}*/

/*{% block struct %}*/
/*{% from "frontend_properties.cpp" import frontendstructdef with context %}*/
/*{% for struct in component.structdefs %}*/
/*{%     if (struct.cppname != "frontend_tuner_allocation" and
             struct.cppname != "frontend_listener_allocation") %}*/ 
${frontendstructdef(struct)}
/*{%     endif %}*/
/*{% endfor %}*/
/*{% endblock %}*/

#endif
