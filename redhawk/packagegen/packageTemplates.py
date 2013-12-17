xmlTemplate = 'BEGIN_SPD\n\
<?xml version="1.0" encoding="UTF-8"?>\n\
<!DOCTYPE softpkg PUBLIC "-//JTRS//DTD SCA V2.2.2 SPD//EN" "softpkg.dtd">\n\
<softpkg id="__COMPONENT_NAME" name="__COMPONENT_NAME" type="sca_compliant">\n\
  <title></title>\n\
  <author>\n\
    <name>null</name>\n\
  </author>\n\
  <propertyfile type="PRF">\n\
    <localfile name="__COMPONENT_NAME.prf.xml"/>\n\
  </propertyfile>\n\
  <descriptor>\n\
    <localfile name="__COMPONENT_NAME.scd.xml"/>\n\
  </descriptor>\n\
  <implementation id="cpp">\n\
    <description>The implementation contains descriptive information about the template for a software component.</description>\n\
    <code type="Executable">\n\
      <localfile name="cpp"/>\n\
      <entrypoint>cpp/__COMPONENT_NAME</entrypoint>\n\
    </code>\n\
    <compiler name="/usr/bin/gcc" version="4.1.2"/>\n\
    <programminglanguage name="C++"/>\n\
    <humanlanguage name="EN"/>\n\
    <os name="Linux"/>\n\
    __DEPENDENCY\n\
    <processor name="x86"/>\n\
    <processor name="x86_64"/>\n\
  </implementation>\n\
</softpkg>\n\
END_SPD\n\
\n\
BEGIN_SCD\n\
<?xml version="1.0" encoding="UTF-8"?>\n\
<!DOCTYPE softwarecomponent PUBLIC "-//JTRS//DTD SCA V2.2.2 SCD//EN" "softwarecomponent.dtd">\n\
<softwarecomponent>\n\
  <corbaversion>2.2</corbaversion>\n\
  <componentrepid repid="IDL:CF/Resource:1.0"/>\n\
  <componenttype>resource</componenttype>\n\
  <componentfeatures>\n\
    <supportsinterface repid="IDL:CF/Resource:1.0" supportsname="Resource"/>\n\
    <supportsinterface repid="IDL:CF/LifeCycle:1.0" supportsname="LifeCycle"/>\n\
    <supportsinterface repid="IDL:CF/PortSupplier:1.0" supportsname="PortSupplier"/>\n\
    <supportsinterface repid="IDL:CF/PropertySet:1.0" supportsname="PropertySet"/>\n\
    <supportsinterface repid="IDL:CF/TestableObject:1.0" supportsname="TestableObject"/>\n\
    <ports>\n\
      <!-- __PORTS -->\n\
    </ports>\n\
  </componentfeatures>\n\
  <interfaces>\n\
    <interface name="Resource" repid="IDL:CF/Resource:1.0">\n\
      <inheritsinterface repid="IDL:CF/LifeCycle:1.0"/>\n\
      <inheritsinterface repid="IDL:CF/PortSupplier:1.0"/>\n\
      <inheritsinterface repid="IDL:CF/PropertySet:1.0"/>\n\
      <inheritsinterface repid="IDL:CF/TestableObject:1.0"/>\n\
    </interface>\n\
    <interface name="LifeCycle" repid="IDL:CF/LifeCycle:1.0"/>\n\
    <interface name="PortSupplier" repid="IDL:CF/PortSupplier:1.0"/>\n\
    <interface name="PropertySet" repid="IDL:CF/PropertySet:1.0"/>\n\
    <interface name="TestableObject" repid="IDL:CF/TestableObject:1.0"/>\n\
    <interface name="ProvidesPortStatisticsProvider" repid="IDL:BULKIO/ProvidesPortStatisticsProvider:1.0"/>\n\
    <interface name="updateSRI" repid="IDL:BULKIO/updateSRI:1.0"/>\n\
  </interfaces>\n\
</softwarecomponent>\n\
END_SCD\n\
\n\
BEGIN_PRF\n\
<?xml version="1.0" encoding="UTF-8"?>\n\
<!DOCTYPE properties PUBLIC "-//JTRS//DTD SCA V2.2.2 PRF//EN" "properties.dtd">\n\
<properties>\n\
  <!-- __PROPERTIES -->\n\
</properties>\n\
END_PRF\n\
\n\
BEGIN_WAVEDEV\n\
<?xml version="1.0" encoding="ASCII"?>\n\
<codegen:WaveDevSettings xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:codegen="http://www.redhawk.gov/model/codegen">\n\
  <implSettings key="cpp">\n\
    <value outputDir="cpp" template="redhawk.codegen.jinja.cpp.component.__GENERATOR" generatorId="redhawk.codegen.jinja.cpp.component.__GENERATOR" primary="true"/>\n\
  </implSettings>\n\
</codegen:WaveDevSettings>\n\
END_WAVEDEV'
