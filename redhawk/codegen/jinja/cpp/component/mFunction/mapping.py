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
