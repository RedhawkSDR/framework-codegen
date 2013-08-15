import os
import sys
import stat

from redhawk.codegen.lang.idl import IDLInterface
from redhawk.codegen import utils

from environment import CodegenEnvironment

class Generator(object):
    def __init__(self, outputdir, overwrite=False, crcs={}, **options):
        self.outputdir = outputdir
        self.overwrite = overwrite
        self.parseopts(**options)

        # Read MD5 sums for testing file changes.
        self.md5file = os.path.join(self.outputdir, '.md5sums')
        self.md5sums = {}
        if os.path.exists(self.md5file):
            for line in open(self.md5file, 'r'):
                try:
                    digest, filename = line.rstrip().split(None, 1)
                    self.md5sums[filename] = digest
                except:
                    pass

        # Migrate legacy CRCs to MD5 sums. If the file is unchanged, calculate
        # the MD5; otherwise, leave it out of the table--it will be treated as
        # modified.
        for filename in crcs:
            if filename in self.md5sums:
                # Assume MD5 sum is more recent
                continue
            # Check if the file has changed since the last CRC32.
            pathname = os.path.join(self.outputdir, filename)
            if not os.path.exists(pathname):
                # The file has been removed, and can be regenerated.
                continue
            if crcs[filename] == str(utils.fileCRC(pathname, stripnewlines=True)):
                # File is unchanged, calculate MD5 sum.
                self.md5sums[filename] = utils.fileMD5(pathname)

    def parseopts(self):
        """
        Parse additional options passed to the constructor. Subclasses should
        implement this method if they have template-specific options.
        """
        pass

    def loader(self, component):
        raise NotImplementedError, 'CodeGenerator.loader'

    def templates(self, component):
        raise NotImplementedError, 'CodeGenerator.templates'

    def filenames(self, softpkg):
        component = self.map(softpkg)
        return [t.filename for t in self.templates(component)]

    def fileChanged(self, filename):
        pathname = os.path.join(self.outputdir, filename)
        if not os.path.exists(pathname):
            return False
        lastHash = self.md5sums.get(filename, None)
        currentHash = utils.fileMD5(pathname)
        return lastHash != currentHash

    def generate(self, softpkg, *filenames):
        if not os.path.exists(self.outputdir):
            os.mkdir(self.outputdir)

        loader = self.loader(softpkg)

        # Map the component model into a language-specific version
        component = self.map(softpkg)

        generated = []
        skipped = []
        for template in self.templates(component):
            # If a file list was given, skip files not explicitly listed.
            if filenames and template.filename not in filenames:
                continue

            filename = os.path.join(self.outputdir, template.filename)

            if os.path.exists(filename):
                # Check if the file has been modified since last generation.
                if self.fileChanged(template.filename) and not self.overwrite:
                    skipped.append(template.filename)
                    continue

            # Attempt to ensure that the full required path exists for files
            # that are more deeply nested.
            if not os.path.isdir(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))

            env = CodegenEnvironment(loader=loader, **template.options())
            env.filters.update(template.filters())
            tmpl = env.get_template(template.template)
            outfile = open(filename, 'w')
            try:
                # Start with the template-specific context, then add the mapped
                # component and a reference to this generator with known names.
                context = template.context()
                context['component'] = component
                context['generator'] = self

                # Evaluate the template in streaming mode (rather than all at
                # once), dumping to the output file.
                tmpl.stream(**context).dump(outfile)
                # Add a trailing newline to work around a Jinja bug.
                outfile.write('\n')

                # Set the executable bit, if requested by the template.
                if template.executable:
                    fd = outfile.fileno()
                    st = os.fstat(fd)
                    os.chmod(filename, st.st_mode|stat.S_IEXEC)
            finally:
                outfile.close()

            generated.append(template.filename)

            # Update the MD5 digest
            self.md5sums[template.filename] = utils.fileMD5(filename)

        # Remove old files that were not generated on this pass and are unchanged
        for existing in self.md5sums.keys():
            if existing in generated or existing in skipped:
                continue
            filename = os.path.join(self.outputdir, existing)
            if os.path.exists(filename) and not self.fileChanged(filename):
                os.unlink(filename)
                del self.md5sums[existing]

        # Save updated MD5 digests
        md5out = open(self.md5file, 'w')
        for name, digest in self.md5sums.items():
            print >>md5out, "%s %s" % (digest, name)
        md5out.close()

        return generated, skipped

    def getOutputDir(self):
        return self.outputdir

    def relativeBasePath(self):
        return os.path.relpath('.', self.getOutputDir()) + '/'

class TopLevelGenerator(Generator):
    def projectMapper(self):
        raise NotImplementedError, 'TopLevelGenerator.projectMapper'

    def map(self, softpkg):
        return self.projectMapper().mapProject(softpkg)

class CodeGenerator(Generator):
    def __init__(self, implId, **opts):
        super(CodeGenerator,self).__init__(**opts)
        self.implId = implId

    def componentMapper(self):
        raise NotImplementedError, 'CodeGenerator.componentMapper'

    def propertyMapper(self):
        raise NotImplementedError, 'CodeGenerator.propertyMapper'

    def portMapper(self):
        raise NotImplementedError, 'CodeGenerator.portMapper'

    def portFactory(self):
        raise NotImplementedError, 'CodeGenerator.portFactory'
    
    def map(self, softpkg):
        # Apply template-specific mapping for component.
        compmapper = self.componentMapper()
        component = compmapper.mapComponent(softpkg)
        impl = softpkg.getImplementation(self.implId)
        component['impl'] = compmapper.mapImplementation(impl)

        # If generator has a mapping for properties, apply that.
        propmapper = self.propertyMapper()
        if propmapper:
            properties = propmapper.mapProperties(softpkg)
            component.update(properties)

        # If generator has a mapping for ports, apply that.
        portmapper = self.portMapper()
        if portmapper:
            portfactory = self.portFactory()
            ports = self.portMapper().mapPorts(softpkg, portfactory)
            component.update(ports)

        return component
