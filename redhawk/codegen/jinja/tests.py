from redhawk.codegen.model.softwarecomponent import ComponentTypes

def is_always(obj, value):
    return False not in (o == value for o in obj)

def is_sometimes(obj, value):
    return True in (o == value for o in obj)

def is_never(obj, value):
    return True not in (o == value for o in obj)

def is_resource(component):
    """
    Returns True if the component is a REDHAWK resource.
    """
    return component['type'] == ComponentTypes.RESOURCE

def is_device(component):
    """
    Returns True if the component is a REDHAWK device.
    """
    return component['type'] == ComponentTypes.DEVICE or component['type'] == ComponentTypes.LOADABLEDEVICE or component['type'] == ComponentTypes.EXECUTABLEDEVICE

def is_loadabledevice(component):
    """
    Returns True if the component is a REDHAWK loadable device.
    """
    return component['type'] == ComponentTypes.LOADABLEDEVICE

def is_executabledevice(component):
    """
    Returns True if the component is a REDHAWK executable device.
    """
    return component['type'] == ComponentTypes.EXECUTABLEDEVICE

def is_service(component):
    """
    Returns True if the component is a REDHAWK service.
    """
    return component['type'] == ComponentTypes.SERVICE

def is_simple(prop):
    """
    Returns True if the property is a simple property.
    """
    return prop['class'] == 'simple'

def is_simplesequence(prop):
    """
    Returns True if the property is a simplesequence property.
    """
    return prop['class'] == 'simplesequence'

def is_struct(prop):
    """
    Returns True if the property is a struct property.
    """
    return prop['class'] == 'struct'

def is_structsequence(prop):
    """
    Returns True if the property is a structsequence property.
    """
    return prop['class'] == 'structsequence'

def _getvalue(obj, name):
    """
    Looks up the item or attribute 'name' in obj. If the item is callable,
    return the result of a no-argument call, otherwise return the item.
    """
    try:
        value = obj[name]
    except TypeError:
        value = getattr(obj, name)
    if callable(value):
        return value()
    else:
        return value

def is_provides(port):
    """
    Returns True if 'port' is a provides port.
    """
    direction = _getvalue(port, 'direction')
    return direction in ('provides','bidir')

def is_uses(port):
    """
    Returns True if 'port' is a uses port.
    """
    direction = _getvalue(port, 'direction')
    return direction in ('uses','bidir')

def is_bidir(port):
    """
    Returns True if 'port' is both a provides and uses port.
    """
    direction = _getvalue(port, 'direction')
    return direction == 'bidir'
