//% set className = component.baseclass.name
//% set baseClass = component.superclass.name
//% set artifactType = component.superclass.artifactType
#include "${component.baseclass.header}"

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

    The following class functions are for the base class for the ${artifactType} class. To
    customize any of these functions, do not modify them here. Instead, overload them
    on the child class

******************************************************************************************/

${className}::${className}(char *devMgr_ior, char *name) :
    ${baseClass}(devMgr_ior, name)
{
}

void ${className}::registerServiceWithDevMgr ()
{
    _deviceManager->registerService(this->_this(), this->_name.c_str());
}

void ${className}::terminateService ()
{
    try {
        _deviceManager->unregisterService(this->_this(), this->_name.c_str());
    } catch (...) {
    }
    
    PortableServer::POA_ptr root_poa = ossie::corba::RootPOA();
    PortableServer::ObjectId_var oid = root_poa->servant_to_id(this);
    root_poa->deactivate_object(oid);
}
    
