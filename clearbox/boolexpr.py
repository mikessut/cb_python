

class Expression:

    __none_result__ = False

    def __init__(self, a, b, op):
        self.a = a
        self.b = b
        self.op = op

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

    def _eval(self, class_parameter_list, class_parameter_result, *objs):
        if isinstance(self.a, ClassParameter):
                a = self.a.eval(*objs)
                class_parameter_list.append(self.a)
                class_parameter_result.append(a)
        elif isinstance(self.a, Expression):
                a = self.a._eval(class_parameter_list, class_parameter_result, *objs)
        else:
                a = self.a

        if isinstance(self.b, ClassParameter):
                b = self.b.eval(*objs)
                class_parameter_list.append(self.b)
                class_parameter_result.append(b)
        elif isinstance(self.b, Expression):
                b = self.b._eval(class_parameter_list, class_parameter_result, *objs)
        else:
                b = self.b

        if (a is None) or (b is None):
                return None  # actual expression return will be determined by BoolExprEnabledClass.__none_result__
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

    def eval(self, *objs):
        #print(type(objs))
        #print([type(x) for x in objs])
        #print(self._cls)
        #print(isinstance(objs[0], self._cls))
        #print(self._cls.__proxy_class__)
        obj = next(x for x in objs
                if (isinstance(x, self._cls) or
                (('__proxy_class__' in self._cls.__dict__.keys()) and
                isinstance(x, self._cls.__proxy_class__))))
        if self._op is not None:
            return self._op(getattr(obj, self._name))
        else:
            return getattr(obj, self._name)

    def __getattr__(self, func):
        """Run function on parameter.

        E.g. ThingA.a.len will run len(ThingA().a) when evaluated
        """
        return ClassParameter(self._cls, self._name, eval(func))
    #def len(self):
    #  return ClassParameter(self._cls, self._name, len)

class BoolExprClass(type):

    def __getattr__(self, attr):
        #print("getattr", self)
        return ClassParameter(self, attr)

class BoolExprEnabledClass(metaclass=BoolExprClass):
    __proxy_class__ = None
    __none_result__ = None

class BoolExprNoneResultMismatchException(Exception):
        pass

class BoolExprNoneResultException(Exception):
        pass
