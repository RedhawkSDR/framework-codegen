/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

    Source: ${component.profile.spd}

*******************************************************************************************/

#include "${component.userclass.header}"

/*{% for portgen in component.portgenerators if portgen.hasImplementation() %}*/
// ----------------------------------------------------------------------------------------
// ${portgen.className()} definition
// ----------------------------------------------------------------------------------------
/*{% include portgen.implementation() %}*/

/*{% endfor %}*/
