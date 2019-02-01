
"""
boolexpr

module that allows boolean expressions, whose evaluation can be deferred until
a time later when it is desired.  It is similar to a lambda function, but provides
more flexibility. Here is an example of its use:

class ThingA(BoolExprEnabledClass):

    foo = 123
    bar = [1,2,3,4,5]

# Instance doesn't need to exist to create the expression.
e = ThingA.foo == 123
a = ThingA()
assert(e.eval(a))

# Can still access instance parameters
print("ThingA parameters:", a.foo, a.bar)

# Any function can be run on the parameter using .syntax. For example,
# the following runs the len() function on the .bar parameter:
e = ThingA.bar.len == 5
assert(e.eval(a))

# If multiple objects are used for comparison, they are pass as multiple
# *args to eval function. Example:

class ThingB(BoolExprEnabledClass):
    bparam = 456

e = (ThingA.foo == 123) & (ThingB.bparam == 456)
b = ThingB()
assert(e.eval(a,b))

# If a parameter doesn't exist, the behavior is to raise an AttributeError

# If a parameter is None, the behavior is customizable.
# 1) Raise an exception
class Thing(BoolExprEnabledClass):
    __none_result__ = BoolExprNoneResultException

e = Thing.foo > 45
t = Thing()
t.foo = None
self.assertRaises(BoolExprNoneResultException, e.eval, t)

# 2) Return true or false when a parameter is None
Thing.__none_result__ = False
e = Thing.foo > 45
assert(e.eval(t) == False)

# There are times when the class you want to use as an expression
# already has __getattribute__ overridden and conflicts with how boolexpr
# works.  In this case, a proxy class can be used.

class Thing:
    # class where __getattr__ or __getattribute__ conflict with boolexpr
    # and class cannot inherit from BoolExprEnabledClass
    pass

class ThingProxy(BoolExprEnabledClass):
    __proxy_class__ = Thing

e = ThingProxy.foo == 45
t = Thing()
t.foo = 45
assert(e.eval(t) == True)
"""

class Expression:

    __none_result__ = False

    def __init__(self, a, b, op, func=None):
        self.a = a
        self.b = b
        self.op = op
        self.func = func

    def __and__(self, other):
        return Expression(self, other, '__and__')

    def __or__(self, other):
        return Expression(self, other, '__or__')

    def __eq__(self, other):
        return Expression(self, other, '__eq__')

    def __gt__(self, other):
        return Expression(self, other, '__gt__')

    def __lt__(self, other):
        return Expression(self, other, '__lt__')

    def __invert__(self):
        return Expression(self, False, '__eq__')

    def abs(self):
        return Expression(self.a, self.b, self.op, abs)

    def _eval(self, class_parameter_list, class_parameter_result, *objs):
        if isinstance(self.a, ClassParameter):
                a = self.a._eval(*objs)
                class_parameter_list.append(self.a)
                class_parameter_result.append(a)
        elif isinstance(self.a, Expression):
                a = self.a._eval(class_parameter_list, class_parameter_result, *objs)
        else:
                a = self.a

        if isinstance(self.b, ClassParameter):
                b = self.b._eval(*objs)
                class_parameter_list.append(self.b)
                class_parameter_result.append(b)
        elif isinstance(self.b, Expression):
                b = self.b._eval(class_parameter_list, class_parameter_result, *objs)
        else:
                b = self.b

        if (a is None) or (b is None):
                return None  # actual expression return will be determined by BoolExprEnabledClass.__none_result__
        if self.func is not None:
            return self.func(getattr(a, self.op)(b))
        else:
            return getattr(a, self.op)(b)

    def eval(self, *objs):
        class_parameter_list = []
        class_parameter_result = []
        result = self._eval(class_parameter_list, class_parameter_result, *objs)
        #print(class_parameter_list, class_parameter_result)
        if not all([x._cls.__none_result__ == class_parameter_list[0]._cls.__none_result__ for x in class_parameter_list]):
            raise BoolExprNoneResultMismatchException("All BoolExprEnabledClass must have the same __none_result__")

        if any([x is None for x in class_parameter_result]):
                if class_parameter_list[0]._cls.__none_result__ == BoolExprNoneResultException:
                    raise BoolExprNoneResultException()
                return class_parameter_list[0]._cls.__none_result__

        return result


class ClassParameter:

    def __init__(self, cls, name, op=None):
        self._cls = cls
        self._name = name
        self._op = op

    def __lt__(self, other):
        return Expression(self, other, '__lt__')

    def __gt__(self, other):
        return Expression(self, other, '__gt__')

    def __eq__(self, other):
        return Expression(self, other, '__eq__')

    def __add__(self, other):
        return Expression(self, other, '__add__')

    def __sub__(self, other):
        return Expression(self, other, '__sub__')

    def __ne__(self, other):
        return Expression(self, other, '__ne__')

    def __invert__(self):
        return Expression(self, False, '__eq__')

    def __floordiv__(self, other):
        return Expression(self, other, '__floordiv__')

    def contains(self, other):
        return Expression(self, other, '__contains__')

    def _eval(self, *objs, **kwargs):
        obj = next(x for x in objs
                if (isinstance(x, self._cls) or
                (('__proxy_class__' in self._cls.__dict__.keys()) and
                isinstance(x, self._cls.__proxy_class__))))

        result = getattr(obj, self._name)
        if callable(result):
            result = result()
        if result is None:
            if ('return_none_result' in kwargs.keys()) and kwargs['return_none_result']:
                return self._cls.__none_result__
            else:
                return None
        if self._op is not None:
            if self._op in [x for x in dir(result)]:
                return getattr(result, self._op)()
            else:
                func = eval(self._op)
                return func(result)
        else:
            return result

    def eval(self, *args):
        #import pdb; pdb.set_trace()
        return self._eval(*args, return_none_result=True)

    def __getattr__(self, func):
        """Run function on parameter.

        E.g. ThingA.a.len will run len(ThingA().a) when evaluated
        """
        #print("getattr:",func)
        return ClassParameter(self._cls, self._name, func)


class BoolExprClass(type):

    _PRESERVED_GETATTRIBUTES = ['__dict__', '__proxy_class__', '__none_result__']

    def __getattribute__(self, attr):
        if (attr == '_PRESERVED_GETATTRIBUTES') or (attr in self._PRESERVED_GETATTRIBUTES):
            #print(self, attr)
            return super().__getattribute__(attr)
            #return super().__getattribute__(self, attr)
        # Preserve a few "normal" members
        #print("getattr", self, attr)
        return ClassParameter(self, attr)

class BoolExprEnabledClass(metaclass=BoolExprClass):
    __proxy_class__ = None
    __none_result__ = None

class BoolExprNoneResultMismatchException(Exception):
        pass

class BoolExprNoneResultException(Exception):
        pass
