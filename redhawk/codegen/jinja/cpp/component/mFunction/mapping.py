#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK code-generator.
#
# REDHAWK code-generator is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK code-generator is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#
from redhawk.codegen.jinja.cpp.component.pull.mapping import PullComponentMapper

class MFunctionMapper(PullComponentMapper):
    def _mapComponent(self, softpkg):
        '''
        Extends the pull mapper _mapComponent method by defining the
        'mFunction' and 'license' key/value pairs to the component dictionary.

        '''

        component = {}

        component['mFunction'] = {'name'      : softpkg.mFileFunctionName(),
                                  'inputs'    : softpkg.mFileInputs(),
                                  'numInputs' : len(softpkg.mFileInputs()),
                                  'outputs'   : softpkg.mFileOutputs()}
        component['license'] = "GPL"

        component.update(PullComponentMapper._mapComponent(self, softpkg))

        return component