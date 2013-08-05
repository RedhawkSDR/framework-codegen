#% set name = component['name']
#% set dirname = name + '-' + component['version']
#% set tarfile = dirname + '.tar.gz'
#!/bin/sh

if [ "$1" = "rpm" ]; then
    # A very simplistic RPM build scenario
    if [ -e {{name}}.spec ]; then
        mydir=`dirname $0`
        tmpdir=`mktemp -d`
        cp -r ${mydir} ${tmpdir}/{{dirname}}
        tar czf ${tmpdir}/{{tarfile}} --exclude=".svn" -C ${tmpdir} {{dirname}}
        rpmbuild -ta ${tmpdir}/{{tarfile}}
        rm -rf $tmpdir
    else
        echo "Missing RPM spec file in" `pwd`
        exit 1
    fi
else
    for impl in {{ component['subdirs']|join(' ') }} ; do
        cd $impl
        if [ -e build.sh ]; then
            ./build.sh $*
        elif [ -e reconf ]; then
            ./reconf && ./configure && make
        else
            echo "No build.sh found for $impl"
        fi
        cd -
    done
fi
