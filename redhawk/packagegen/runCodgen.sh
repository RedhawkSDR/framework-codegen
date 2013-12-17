COMPONENT_NAME=$1
#python genXmlAndStubs.py $COMPONENT_NAME.xml
../../redhawk-codegen -m $COMPONENT_NAME.m -f $COMPONENT_NAME/$COMPONENT_NAME.spd.xml
