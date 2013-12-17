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
//% set className = component.userclass.name
//% set baseName = component.baseclass.name
/*{% from "mFunction/gpl.cpp" import gplHeader%}*/
${gplHeader(component)}

/**************************************************************************

    This is the ${component.userclass.name} code. This file contains the child class where
    custom functionality can be added to the ${component.userclass.name}. Custom
    functionality to the base class can be extended here.

    Port data before and after Octave processing may be accessed using
    this->inputPackets and this->inputPackets, respectfully.
**************************************************************************/


#include "${component.userclass.header}"

PREPARE_LOGGING(${className})

${className}::${className}(const char *uuid, const char *label) :
    ${baseName}(uuid, label)
{
    /* Indicate whether or not buffering should be turned on.  If buffering
     * is turned on, the component will wait for EOS flags on all ports before
     * calling the M function.  If buffering is turned off, the component will
     * send incoming packets to the M function without waiting for EOS flags.
     *
     * If working with streaming data (i.e., data should be processed before
     * an EOS is encountered), the _enableBuffering variable should be set to
     * false.
     */
    _enableBuffering = true;

    /* Indicate whether or not the service function should only be run once.
     * If the component is a file source that should only read the input
     * file once, this should be set to FINISH.  Otherwise, if the service
     * function should be called indefinitely, this should be set to NORMAL.
     */
    _serviceFunctionReturnVal = NORMAL;
}

${className}::~${className}()
{
}

/**
 * This method is called after the inputPackets map has been populated, but
 * before the Octave function is called (before the outputPackets map has been
 * populated).  This is the appropriate place to modify property values based
 * on incoming SRI.
 */
int ${className}::preProcess()
{
    return NORMAL;
}

/**
 * This method is called after the Octave function is called (after the 
 * outputPackets map has been populated), but before data is sent to the output
 * port(s).  This is the appropriate place to modify property values and
 * outgoing SRI based on the output of the M function and the incoming SRI.
 */
int ${className}::postProcess()
{
    return NORMAL;
}
