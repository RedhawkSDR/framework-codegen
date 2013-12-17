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
/*{%extends "pull/resource_base.cpp"%}*/
/*{%block license%}*/
/*{% from "gpl.cpp" import gplHeader%}*/
${gplHeader(component)}
/*{%endblock%}*/

/*{% block componentConstructor %}*/
${className}::${className}(const char *uuid, const char *label):
    ${baseClass}(uuid, label)
{
    // start up octave
    const char * argvv [] = {"",  /* program name*/
                             "--silent"};
    octave_main (2, (char **) argvv, true /* embedded */);

/*{% for port in component.ports if port is uses %}*/
    std::string streamID_${component.name}_${port.cppname} = "${component.name}_${port.cppname}";
    outputPackets["${port.cppname}"] = createDefaultDataTransferType(streamID_${component.name}_${port.cppname});
/*{% endfor %}*/

    construct();
}
/*{% endblock %}*/

${className}::~${className}()
{
    // Deallocate the allocated DataTransferType objects for the output packets
    std::map<std::string, bulkio::InDoublePort::DataTransferType*>::iterator iter;
    for (iter = outputPackets.begin(); iter != outputPackets.end(); ++iter) {
       delete iter->second;
    }

    // Prevent octave from leaving around temporary files after shutdown.
    do_octave_atexit();
}

/*{%block extensions%}*/
void ${className}::setCurrentWorkingDirectory(std::string& cwd)
{ 
    Resource_impl::setCurrentWorkingDirectory(cwd);

    // set the OCTAVEPATH to the same directory as the component executable
    octave_value_list functionArguments; // pass to octave
    functionArguments(0) = octave_value(getCurrentWorkingDirectory());
    feval("addpath", functionArguments);
}

/**
 * Initialize a new DataTransferType with some default values.
 *
 * The returned DataTransferType object must be deleted later.
 */
bulkio::InDoublePort::DataTransferType* ${className}::createDefaultDataTransferType(
    std::string& streamID)
{
    const PortTypes::DoubleSequence emptyVector;

    CORBA::Boolean EOS     = true;
    bool inputQueueFlushed = false;
    bool sriChanged        = true;
    bool blocking          = true;

    BULKIO::PrecisionUTCTime timestamp = BULKIO::PrecisionUTCTime();

    BULKIO::StreamSRI SRI = bulkio::sri::create(
        streamID,           /* stream ID    */
        -1,                 /* sample rate  */
        BULKIO::UNITS_NONE, /* units        */
        blocking);          /* blocking     */

    return new bulkio::InDoublePort::DataTransferType(
        emptyVector,        /* default value        */
        timestamp,          /* timestamp            */
        EOS,                /* EOS                  */
        streamID.c_str(),   /* stream ID            */
        SRI,                /* SRI                  */
        sriChanged,         /* SRI-chaged flag      */
        inputQueueFlushed); /* flush-to-report flag */
}

/*# bulkio will only be imported if ports are defined #*/
/*{%if component.ports%}*/
/**
 * Sub-method of appendInputPacketToFunctionArguments.
 */
void appendComplexInputPacketToFunctionArguments(
    octave_value_list&                        functionArguments, /* output */
    const bulkio::InDoublePort::dataTransfer* inputPacket)       /* input  */
{
    // create a complex list from the list of interleaved real/imag values
    std::vector<std::complex<double> >* complexList = 
        (std::vector<std::complex<double> >*) &(inputPacket->dataBuffer);

    if (inputPacket->SRI.subsize == 0) 
    { // vector data
        // convert std::vector<std::complex> to ComplexRowVector
        ComplexRowVector mRowVector(complexList->size());
        for (unsigned int i=0; i < complexList->size(); i++) {
            mRowVector(i) = (*complexList)[i];
        }
        functionArguments.append(octave_value(mRowVector));
    } // end vector data
    else
    { // Matrix (framed) data
        unsigned int numRows = complexList->size() / inputPacket->SRI.subsize;
        unsigned int numCols = inputPacket->SRI.subsize;
        ComplexMatrix mMatrix(numRows, numCols);
        unsigned int bulkioIndex = 0;
        for (unsigned int rowNum=0; rowNum < numRows; rowNum++) {
            for (unsigned int colNum=0; colNum <numCols; colNum++) {
                mMatrix(rowNum, colNum) = (*complexList)[bulkioIndex++];
            }
        }
        functionArguments.append(octave_value(mMatrix));
    } // end matrix data
}

/**
 * Sub-method of appendInputPacketToFunctionArguments.
 */
void appendScalarInputPacketToFunctionArguments(
    octave_value_list&                        functionArguments, /* output */
    const bulkio::InDoublePort::dataTransfer* inputPacket)       /* input  */
{
    if (inputPacket->SRI.subsize == 0) 
    { // vector data
        // convert std::vector to RowVector
        RowVector mRowVector(inputPacket->dataBuffer.size());
        for (unsigned int i=0; i < inputPacket->dataBuffer.size(); i++) {
            mRowVector(i) = (double)inputPacket->dataBuffer[i];
        }
        functionArguments.append(octave_value(mRowVector));
    } // end vector data
    else
    { // Matrix (framed) data
        unsigned int numRows = inputPacket->dataBuffer.size() / inputPacket->SRI.subsize;
        unsigned int numCols = inputPacket->SRI.subsize;
        Matrix mMatrix(numRows, numCols);
        unsigned int bulkioIndex = 0;
        for (unsigned int rowNum=0; rowNum < numRows; rowNum++) {
            for (unsigned int colNum=0; colNum <numCols; colNum++) {
                mMatrix(rowNum, colNum) = (double)inputPacket->dataBuffer[bulkioIndex++];
            }
        }
        functionArguments.append(octave_value(mMatrix));
    } // end matrix data
}

/**
 * Convert the inputPacket to a RowVector or matrix and append it to
 * functionArguments
 */
void appendInputPacketToFunctionArguments(
    octave_value_list&                        functionArguments, /* output */
    const bulkio::InDoublePort::dataTransfer* inputPacket)       /* input  */
{
    if (inputPacket->SRI.mode) {
        appendComplexInputPacketToFunctionArguments(
            functionArguments,
            inputPacket);
    } else {
        appendScalarInputPacketToFunctionArguments(
            functionArguments,
            inputPacket);
    }
}

/**
 * Buffer data until an EOS flag is encountered.
 *
 * Populates inputPackets[portName].  SRI, other than EOS, inputQueueFlushed,
 * and sriChanged, is assumed to be the same for all incoming sub-packets.
 * All subpacket data is appended to inputPackets[portName]->dataBuffer.
 *
 * Note that buffering requires an additional data copy.
 */
int ${className}::buffer(std::string portName, bulkio::InDoublePort* port)
{
    while (inputPackets[portName]->EOS == false) {
        // put data on the buffer
        bulkio::InDoublePort::DataTransferType* tmpPkt = port->getPacket(-1);
        if (not tmpPkt) {
            // No data is available because component is being killed
            return NOOP;
        }

        // copy the incoming packet data into the master packet
        inputPackets[portName]->dataBuffer.insert(
            inputPackets[portName]->dataBuffer.end(),
            tmpPkt->dataBuffer.begin(),
            tmpPkt->dataBuffer.end());

        if (tmpPkt->sriChanged) {
            // if any of the input packets in the stream indicated a change in
            // SRI, set sriChanged to true.
            inputPackets[portName]->sriChanged = true;
        }
        if (tmpPkt->inputQueueFlushed) {
            // if any of the input packets in the stream indicated a change in
            // SRI, set sriChanged to true.
            inputPackets[portName]->inputQueueFlushed = true;
        }
        inputPackets[portName]->EOS = tmpPkt->EOS;
        delete tmpPkt;
    }
    return NORMAL;
}

/**
 * Push a packet whose payload cannot fit within the CORBA limit.
 * The packet is broken down into sub-packets and sent via multiple pushPacket
 * calls.  The EOS is set to false for all of the sub-packets, except for
 * the last sub-packet, who uses the EOS outputPacket.
 */
void pushOversizedPacket(
    bulkio::OutDoublePort*                  outputPort,   /* port to push to */
    bulkio::InDoublePort::DataTransferType* outputPacket) /* input */
{
    // If there is no data to break into smaller packets, skip
    // straight to the pushPacket call and return.
    if (outputPacket->dataBuffer.size() == 0) {
        outputPort->pushPacket(
            outputPacket->dataBuffer, /* data      */
            outputPacket->T,          /* timestamp */
            outputPacket->EOS,        /* EOS       */
            outputPacket->streamID);  /* stream ID */
        return;
    }

    // Multiply by some number < 1 to leave some margin for the CORBA header
    size_t maxPayloadSize    = (size_t) (bulkio::Const::MAX_TRANSFER_BYTES * .9);
    size_t numSamplesPerPush = maxPayloadSize/sizeof(outputPacket->dataBuffer.front());

    // Determine how many sub-packets to send.
    size_t numFullPackets    = outputPacket->dataBuffer.size()/numSamplesPerPush;
    size_t lenOfLastPacket   = outputPacket->dataBuffer.size()%numSamplesPerPush;

    // Send all of the sub-packets of length numSamplesPerPush.
    // Always send EOS false, (the EOS of the parent packet will be sent
    // eith the last sub-packet).
    bool EOS = false;
    unsigned int rowNum;
    for (rowNum = 0; rowNum < numFullPackets; rowNum++) {
        if ( (rowNum == numFullPackets -1) && (lenOfLastPacket == 0)) {
            // This is the last sub-packet.
            EOS = outputPacket->EOS;
        }

        std::vector<double> subPacket(
            outputPacket->dataBuffer.begin() + rowNum*numSamplesPerPush,
            outputPacket->dataBuffer.begin() + rowNum*numSamplesPerPush + numSamplesPerPush);
        outputPort->pushPacket(
            subPacket,               /* data      */
            outputPacket->T,         /* timestamp */
            EOS,                     /* EOS       */
            outputPacket->streamID); /* stream ID */
    }

    if (lenOfLastPacket != 0) {
        // Send the last sub-packet, whose length is less than
        // numSamplesPerPush.  Note that the EOS of the master packet is
        // sent with the last sub-packet.
        std::vector<double> subPacket(
            outputPacket->dataBuffer.begin() + numFullPackets*numSamplesPerPush,
            outputPacket->dataBuffer.begin() + numFullPackets*numSamplesPerPush + lenOfLastPacket);
        outputPort->pushPacket(
            subPacket,               /* data      */
            outputPacket->T,         /* timestamp */
            outputPacket->EOS,       /* EOS       */
            outputPacket->streamID); /* stream ID */
    }
}

/**
 * Sub-method of populateOutputPacket.
 */
void populateComplexOutputPacket(
    bulkio::InDoublePort::DataTransferType* outputPacket, /* output */
    const octave_value_list&                result,       /* input  */
    const int                               resultIndex)  /* input  */
{
    if (result(resultIndex).ndims() == 1)
    { // Vector Data
        // convert RowVector to std::vector
        // (with alternating real/complex values)
        ComplexRowVector outputVector = result(resultIndex).complex_array_value();
        outputPacket->dataBuffer.resize(outputVector.length()*2);
        for (int i = 0; i < outputVector.length(); i++) {
            outputPacket->dataBuffer[i*2]   = (CORBA::Double)outputVector(i).real();
            outputPacket->dataBuffer[i*2+1] = (CORBA::Double)outputVector(i).imag();
        }
    } // end vector data 
    else if (result(resultIndex).ndims() == 2) 
    { // 2-D matrix
        ComplexMatrix outputMatrix = result(resultIndex).complex_matrix_value();
        outputPacket->dataBuffer.resize(outputMatrix.nelem()*2);
        for (int i = 0; i < outputMatrix.nelem(); i++) {
            outputPacket->dataBuffer[i*2]   = (CORBA::Double)outputMatrix(i).real();
            outputPacket->dataBuffer[i*2+1] = (CORBA::Double)outputMatrix(i).imag();
        }
        outputPacket->SRI.subsize = outputMatrix.cols();
    } // end 2-D matrix
    else
    { // more thank 2 dimensions
        throw std::invalid_argument("BULKIO cannot support matricies with more than 2 dimensions.");
    }
    outputPacket->SRI.mode = true;
}

/**
 * Sub-method of populateOutputPacket.
 */
void populateScalarOutputPacket(
    bulkio::InDoublePort::DataTransferType* outputPacket, /* output */
    const octave_value_list&                result,       /* input  */
    const int                               resultIndex)  /* input  */
{
    if (result(resultIndex).ndims() == 1)
    { // Vector Data
        // convert RowVector to std::vector
        RowVector outputVector = result(resultIndex).array_value();
        outputPacket->dataBuffer.resize(outputVector.length());
        for (int i = 0; i <  outputVector.length(); i++) {
            outputPacket->dataBuffer[i] = (CORBA::Double)outputVector(i);
        }
    }
    else if (result(resultIndex).ndims() == 2) 
    { // 2-D matrix
        Matrix outputMatrix = result(resultIndex).matrix_value();
        outputPacket->dataBuffer.resize(outputMatrix.nelem());
        for (int i = 0; i < outputMatrix.nelem(); i++) {
            outputPacket->dataBuffer[i] = (CORBA::Double)outputMatrix(i);
        }
        outputPacket->SRI.subsize = outputMatrix.cols();
    } // end 2-D matrix
    else
    { // more thank 2 dimensions
        throw std::invalid_argument("BULKIO cannot support matricies with more than 2 dimensions.");
    }
    outputPacket->SRI.mode = false;
}

/**
 * Convert the item number resultIndex of result into a std::vector.
 * Populates and returns outputPacket.
 */
void populateOutputPacket(
    bulkio::InDoublePort::DataTransferType* outputPacket, /* output */
    const octave_value_list&                result,       /* input  */
    const int                               resultIndex)  /* input  */
{
    outputPacket->T = bulkio::time::utils::now();

    if (result(resultIndex).is_complex_type()) {
        populateComplexOutputPacket(outputPacket, result, resultIndex);
    } else {
        populateScalarOutputPacket(outputPacket, result, resultIndex);
    }
}
/*# end bulkio conditional #*/
/*{%endif%}*/

int ${className}::preProcess(){return NORMAL;}
int ${className}::postProcess(){return NORMAL;}

int ${className}::serviceFunction()
{
/*{% from "mFunction/octaveEmbedding.cpp" import octaveEmbedding%}*/
    ${octaveEmbedding(component)|indent(4)}
}
/*{%endblock%}*/
