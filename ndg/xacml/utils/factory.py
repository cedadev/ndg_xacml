"""
Class Factory

NERC DataGrid project
"""
__author__ = "Philip Kershaw"
__date__ = "15/02/10"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import traceback
import logging, os, sys
log = logging.getLogger(__name__)


def importModuleObject(moduleName, objectName=None, objectType=None):
    '''Import from a string module name and object name.  Object can be
    any entity contained in a module
    
    @param moduleName: Name of module containing the class
    @type moduleName: str 
    @param objectName: Name of the class to import.  If none is given, the 
    class name will be assumed to be the last component of modulePath
    @type objectName: str
    @rtype: class object
    @return: imported class'''
    if objectName is None:
        if ':' in moduleName:
            # Support Paste style import syntax with rhs of colon denoting 
            # module content to import
            _moduleName, objectName = moduleName.rsplit(':', 1)
            if '.' in objectName:
                objectName = objectName.split('.')
        else: 
            _moduleName, objectName = moduleName.rsplit('.', 1)
    else:
        _moduleName = moduleName
        
    if isinstance(objectName, basestring):
        objectName = [objectName]
    
    module = __import__(_moduleName, globals(), locals(), [])
    components = _moduleName.split('.')
    try:
        for component in components[1:]:
            module = getattr(module, component)
    except AttributeError:
        raise AttributeError("Error importing %r: %s" %
                             (objectName[0], traceback.format_exc()))

    importedObject = module
    for i in objectName:
        importedObject = getattr(importedObject, i)

    # Check class inherits from a base class
    if objectType and not issubclass(importedObject, objectType):
        raise TypeError("Specified class %r must be derived from %r; got %r" %
                        (objectName, objectType, importedObject))
    
    return importedObject


def callModuleObject(moduleName, objectName=None, moduleFilePath=None, 
                     objectType=None, objectArgs=None, objectProperties=None):
    '''
    Create and return an instance of the specified class or invoke callable
    @param moduleName: Name of module containing the class
    @type moduleName: str 
    @param objectName: Name of the class to instantiate.  May be None in 
    which case, the class name is parsed from the moduleName last element
    @type objectName: str
    @param moduleFilePath: Path to the module - if unset, assume module on 
    system path already
    @type moduleFilePath: str
    @param objectProperties: dict of properties to use when instantiating the 
    class
    @type objectProperties: dict
    @param objectType: expected type for the object to instantiate - to 
    enforce use of specific interfaces 
    @type objectType: object
    @return: object - instance of the class specified 
    '''
    
    # ensure that properties is a dict - NB, it may be passed in as a null
    # value which can override the default val
    if not objectProperties:
        objectProperties = {}

    if not objectArgs:
        objectArgs = ()

    # variable to store original state of the system path
    sysPathBak = None
    try:
        try:
            # Module file path may be None if the new module to be loaded
            # can be found in the existing system path            
            if moduleFilePath:
                if not os.path.exists(moduleFilePath):
                    raise IOError("Module file path '%s' doesn't exist" % 
                                  moduleFilePath)
                          
                # Temporarily extend system path ready for import
                sysPathBak = sys.path
                          
                sys.path.append(moduleFilePath)

            
            # Import module name specified in properties file
            importedObject = importModuleObject(moduleName, 
                                                objectName=objectName,
                                                objectType=objectType)
        finally:
            # revert back to original sys path, if necessary
            # NB, python requires the use of a try/finally OR a try/except 
            # block - not both combined
            if sysPathBak:
                sys.path = sysPathBak
                            
    except Exception, e:
        log.debug('%r module import raised %r type exception: %s', 
                  moduleName, e.__class__, traceback.format_exc())
        raise 

    # Instantiate class
    if objectArgs:
        obj = importedObject(*objectArgs, **objectProperties)
    else:
        obj = importedObject(**objectProperties)
        
    return obj
