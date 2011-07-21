# @file ast.py
#
# Objects used to create an Abstract Syntax Tree
##########################################################################################


#-----------------------------------------------------------------------------------------
# Enumeration of the possible "virtualities" of a method
#-----------------------------------------------------------------------------------------
class VIRTUALITY:
    NOT_VIRTUAL     = 0
    VIRTUAL         = 1
    PURE_VIRTUAL    = 2


#-----------------------------------------------------------------------------------------
# Enumeration of the possible access modifiers for members of a class
#-----------------------------------------------------------------------------------------
class ACCESS:
    PUBLIC          = 0
    PROTECTED       = 1
    PRIVATE         = 2
    
    @staticmethod
    def toString(access):
        if access == ACCESS.PUBLIC:
            return "public"
        elif access == ACCESS.PROTECTED:
            return "protected"
        elif access == ACCESS.PRIVATE:
            return "private"

        return "-"


#-----------------------------------------------------------------------------------------
# Represents a list of declarations
#-----------------------------------------------------------------------------------------
class DeclarationsList:

    def __init__(self):
        self.declarations = []

    def add(self, declaration):
        assert(declaration is not None)
        self.declarations.append(declaration)

    def remove(self, declaration):
        assert(declaration is not None)
        self.declarations.remove(declaration)
    
    def clear(self):
        self.declarations = []

    def get(self, name=None, type=None):
        l = self.declarations
        
        if type is not None:
            l = filter(lambda x: isinstance(x, type), l)

        if name is not None:
            l = filter(lambda x: x.name == name, l)

        return l

    def size(self):
        return len(self.declarations)

    def __getitem__(self, i):
        return self.declarations[i]

    def sort(self):
        self.declarations.sort() 


#-----------------------------------------------------------------------------------------
# Base class for all the declarations
#-----------------------------------------------------------------------------------------
class Declaration:

    availableAnnotations = { 'PyName': None
                           }
    type_name     = '-'
    accessibility = None
    virtuality    = VIRTUALITY.NOT_VIRTUAL
    static        = False
    const         = False

    def __init__(self, name, unique_id=None, parent=None, ignorable=True):
        assert(id is not None)

        self.name        = name
        self.unique_id   = unique_id
        self.parent      = parent
        self.children    = DeclarationsList()
        self.annotations = {}
        self.ignorable   = ignorable
        self.exported    = not(ignorable)
        
        if self.parent:
            self.parent.children.add(self)

    def toString(self):
        return self.name

    def getChild(self, name, type=None):
        assert(name is not None)

        l = self.children.get(name, type)
        if len(l) == 1:
            return l[0]

        return None

    def getChildren(self, name=None, type=None):
        return self.children.get(name, type)

    def export(self, exported):
        if self.ignorable:
            self.exported = exported

    def isExported(self):
        return not(self.ignorable) or self.exported

    def isIgnorable(self):
        return self.ignorable

    def __cmp__(self, other):
        return cmp(self.name, other.name)


#-----------------------------------------------------------------------------------------
# Represent a namespace
#-----------------------------------------------------------------------------------------
class Namespace(Declaration):

    type_name = 'Namespace'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)


#-----------------------------------------------------------------------------------------
# Represent a class
#-----------------------------------------------------------------------------------------
class Class(Declaration):

    availableAnnotations = { 'Abstract': False,
                             'DelayDtor': False,
                             'External': False,
                             'NoDefaultCtors': False,
                             'PyName': None
                           }

    type_name = 'Class'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)

    def getMethod(self, name):
        assert(name is not None)
        return self.getChild(name, Method)

    def getMethods(self):
        return self.getChildren(name, Method)

    def getOperator(self, name):
        assert(name is not None)
        return self.getChild(name, Operator)

    def getOperators(self):
        return self.getChildren(name, Operator)

    def getAttribute(self, name):
        assert(name is not None)
        return self.getChild(name, Attribute)

    def getAttributes(self):
        return self.getChildren(name, Attribute)


#-----------------------------------------------------------------------------------------
# Represent a link to a base class
#-----------------------------------------------------------------------------------------
class Base(Declaration):

    type_name = 'Base'

    def __init__(self, name, parent):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)


#-----------------------------------------------------------------------------------------
# Represent a structure
#-----------------------------------------------------------------------------------------
class Struct(Declaration):

    type_name = 'Struct'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)


#-----------------------------------------------------------------------------------------
# Represent a typedef
#-----------------------------------------------------------------------------------------
class Typedef(Declaration):

    type_name = 'Typedef'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)


#-----------------------------------------------------------------------------------------
# Represent an enumeration
#-----------------------------------------------------------------------------------------
class Enumeration(Declaration):

    type_name = 'Enum'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)

        if (len(name) >= 3) and name[0].islower() and name[1].isupper():
            self.annotations['PyName'] = name[1].lower() + name[2:]


#-----------------------------------------------------------------------------------------
# Represent an enumeration value
#-----------------------------------------------------------------------------------------
class EnumerationValue(Declaration):

    type_name = 'Value'

    def __init__(self, name, value, unique_id=None, parent=None):
        Declaration.__init__(self, '[Value] ' + name, name=name, unique_id=unique_id, parent=parent)
        self.value = value


#-----------------------------------------------------------------------------------------
# Represent a return type
#-----------------------------------------------------------------------------------------
class ReturnType(Declaration):

    type_name = 'ReturnType'

    def __init__(self, name, parent=None):
        Declaration.__init__(self, name, parent=parent, ignorable=False)


#-----------------------------------------------------------------------------------------
# Represent an argument (of a function or of a method)
#-----------------------------------------------------------------------------------------
class Argument(Declaration):

    availableAnnotations = { 'Array': False,
                             'ArraySize': None,
                             'Constrained': False,
                             'In': False,
                             'Out': False,
                             'Transfer': False,
                             'TransferBack': False,
                             'TransferThis': False,
                           }

    type_name = 'Argument'

    def __init__(self, name, typename, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent, ignorable=False)
        self.typename = typename


#-----------------------------------------------------------------------------------------
# Represent a constructor
#-----------------------------------------------------------------------------------------
class Constructor(Declaration):

    availableAnnotations = { 'Default': False,
                             'NoDerived': False,
                             'Constrained': False,
                             'In': False,
                             'Out': False,
                             'Transfer': False,
                             'TransferBack': False,
                             'TransferThis': False,
                            }

    type_name = 'Constructor'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)

    def toString(self):
        return '%s(%s)' % (self.name, ', '.join([ '%s %s' % (arg.typename, arg.name) for arg in self.children ]))


#-----------------------------------------------------------------------------------------
# Represent a destructor
#-----------------------------------------------------------------------------------------
class Destructor(Declaration):

    type_name = 'Destructor'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)
        self.virtuality  = VIRTUALITY.NOT_VIRTUAL

    def toString(self):
        return '~' + self.name + '()'


#-----------------------------------------------------------------------------------------
# Base class for the member functions of a class (methods and operators)
#-----------------------------------------------------------------------------------------
class MemberFunction(Declaration):

    availableAnnotations = { 'AutoGen': None,
                             'Factory': False,
                             'HoldGIL': False,
                             'NewThread': False,
                             'PostHook': None,
                             'PreHook': None,
                             'ReleaseGIL': False,
                             'Transfer': False,
                             'TransferBack': False,
                             'PyName': None
                           }

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)

        self.static      = False
        self.const       = False
        self.virtuality  = VIRTUALITY.NOT_VIRTUAL

    def toString(self):
        ret = self.children.get(type=ReturnType)
        if len(ret) == 0:
            ret = 'void'
        else:
            ret = ret[0].name
        
        return '%s %s(%s)' % (ret, self.name, ', '.join([ '%s %s' % (arg.typename, arg.name) for arg in self.children.get(type=Argument) ]))


#-----------------------------------------------------------------------------------------
# Represent a method
#-----------------------------------------------------------------------------------------
class Method(MemberFunction):

    type_name = 'Method'

    def __init__(self, name, unique_id=None, parent=None):
        MemberFunction.__init__(self, name, unique_id=unique_id, parent=parent)

        if (len(name) >= 3) and name[0].isupper() and name[1].islower():
            self.annotations['PyName'] = name[0].lower() + name[1:]


#-----------------------------------------------------------------------------------------
# Represent a method
#-----------------------------------------------------------------------------------------
class Operator(MemberFunction):

    availableAnnotations = { 'AutoGen': None,
                             'Factory': False,
                             'HoldGIL': False,
                             'NewThread': False,
                             'PostHook': None,
                             'PreHook': None,
                             'ReleaseGIL': False,
                             'Transfer': False,
                             'TransferBack': False,
                             'PyName': None,
                             'Numeric': False
                           }

    type_name = 'Operator'

    def __init__(self, name, unique_id=None, parent=None):
        MemberFunction.__init__(self, name, unique_id=unique_id, parent=parent)


#-----------------------------------------------------------------------------------------
# Represent an attribute
#-----------------------------------------------------------------------------------------
class Attribute(Declaration):

    type_name = 'Attribute'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)


#-----------------------------------------------------------------------------------------
# Represent a variable
#-----------------------------------------------------------------------------------------
class Variable(Declaration):

    type_name = 'Variable'

    def __init__(self, name, unique_id=None, parent=None):
        Declaration.__init__(self, name, unique_id=unique_id, parent=parent)
