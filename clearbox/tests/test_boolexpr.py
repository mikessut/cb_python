import unittest
from clearbox.boolexpr import *

class TestBoolExpr(unittest.TestCase):

    def test_classparameter(self):

        class Thing:
            a = 123

        t = Thing()

        cp = ClassParameter(Thing, 'a')

        self.assertTrue(cp.eval(t), 123)

    def test_expr(self):

        class ThingA(BoolExprEnabledClass):
            pass

        class ThingB(BoolExprEnabledClass):
            pass

        a = ThingA()
        a.a = 123
        b = ThingB()
        b.b = 456
        b.mylist = [1,2,3,4]

        e = ThingA.a < ThingB.b
        self.assertTrue(e.eval(a, b))

        e = 0 < ThingA.a
        self.assertTrue(e.eval(a,b))

        e2 = ThingB.mylist.len > 2
        self.assertTrue(e2.eval(a,b))

        e2 = 2 < ThingB.mylist.len
        self.assertTrue(e2.eval(a,b))

        e = ThingB.mylist.len != 1
        self.assertTrue(e.eval(b))

        e3 = (ThingA.a == 123)
        self.assertTrue(e3.eval(a,b))

        e3 = (123 == ThingA.a)
        self.assertTrue(e3.eval(a,b))

        e4 = (ThingB.mylist.len > 2) & (ThingA.a == 123)
        self.assertTrue(e4.eval(a,b))

        e = (ThingB.mylist.len > 2) & (ThingA.a == 122)
        self.assertFalse(e.eval(a,b))

        e = ThingB.mylist.max == 4
        self.assertTrue(e.eval(b))

        e = (ThingA.a + 1) == (123+1)
        self.assertTrue(e.eval(a))

        e = (ThingA.a - 1) == (123-1)
        self.assertTrue(e.eval(a))

        e = (ThingA.a + 1) > (123)
        self.assertTrue(e.eval(a))

        e = (ThingA.a - 1) < (123)
        self.assertTrue(e.eval(a))

    def test_expr_proxy(self):
        class ThingA:
            pass

        class ThingAProxy(BoolExprEnabledClass):
            __proxy_class__ = ThingA

        class ThingB:
            pass

        class ThingBProxy(BoolExprEnabledClass):
            __proxy_class__ = ThingB

        a = ThingA()
        a.a = 123
        b = ThingB()
        b.b = 456
        b.mylist = [1,2,3,4]

        e = ThingAProxy.a < ThingBProxy.b
        self.assertTrue(e.eval(a, b))

        e = 0 < ThingAProxy.a
        self.assertTrue(e.eval(a,b))

        e2 = ThingBProxy.mylist.len > 2
        self.assertTrue(e2.eval(a,b))

        e2 = 2 < ThingBProxy.mylist.len
        self.assertTrue(e2.eval(a,b))

        e3 = (ThingAProxy.a == 123)
        self.assertTrue(e3.eval(a,b))

        e3 = (123 == ThingAProxy.a)
        self.assertTrue(e3.eval(a,b))

        e4 = (ThingBProxy.mylist.len > 2) & (ThingAProxy.a == 123)
        self.assertTrue(e4.eval(a,b))

        e = (ThingBProxy.mylist.len > 2) & (ThingAProxy.a == 122)
        self.assertFalse(e.eval(a,b))

        e = ThingBProxy.mylist.max == 4
        self.assertTrue(e.eval(b))

    def test_none_result_mismatch(self):
        class ThingA(BoolExprEnabledClass):
            __none_result__ = False

        class ThingB(BoolExprEnabledClass):
              __none_result__ = True

        e = (ThingA.foo > 3) & (ThingB.bar == 3)
        a = ThingA()
        a.foo = None
        b = ThingB()
        b.bar = 3

        self.assertRaises(BoolExprNoneResultMismatchException, e.eval, *(a, b))

    def test_none_result(self):

        class ThingA(BoolExprEnabledClass):
                __none_result__ = False

        a = ThingA()
        a.none_param = None
        e = ThingA.none_param == 4
        self.assertFalse(e.eval(a))

        ThingA.__none_result__ = True
        self.assertTrue(e.eval(a))

        ThingA.__none_result__ = BoolExprNoneResultException
        self.assertRaises(BoolExprNoneResultException, e.eval, a)

        ThingA.__none_result__ = None
        e = ThingA.none_param
        self.assertTrue(e.eval(a) is None)

    def test_doc_demo(self):
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

        # 2) Return true, false, or None when a parameter is None.
        # Note: all classes for an expression must have the same __none_result__
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


    def test_non_existant_param(self):

        class ThingA(BoolExprEnabledClass):
            pass

        e = ThingA.foo == 123
        self.assertRaises(AttributeError, e.eval, ThingA())
        # This could be customized to do other things in the future if we want...

    def test_class_func(self):
        class Thing(BoolExprEnabledClass):
            __none_result__ = True

            def func(self):
                return 123

            def bool_func(self):
                return True

            def bool_func_not(self):
                return False

            def none_func(self):
                return None

        e = Thing.func == 124
        t = Thing()
        self.assertFalse(e.eval(t))

        e = Thing.func == 123
        self.assertTrue(e.eval(t))

        e = Thing.bool_func
        self.assertTrue(e.eval(t))
        e = Thing.bool_func_not
        self.assertFalse(e.eval(t))

        e = Thing.none_func
        self.assertTrue(e.eval(t))

        e = Thing.none_param
        t.none_param = None
        self.assertTrue(e.eval(t))
        Thing.__none_result__ = False
        self.assertFalse(e.eval(t))
        Thing.__none_result__ = None
        self.assertTrue(e.eval(t) is None)

        # Test with __proxy_class__
        class Thing:
            def func(self):
                return 123

        class ThingProxy(BoolExprEnabledClass):
            __proxy_class__ = Thing

        e = ThingProxy.func == 124
        t = Thing()
        self.assertFalse(e.eval(t))

        e = ThingProxy.func == 123
        self.assertTrue(e.eval(t))

    def test_class_func_func(self):
        class Thing(BoolExprEnabledClass):
            __none_result__ = False
            def func(self):
                return [1,2,3,4,5]

            def none_func(self):
                return None

        e = Thing.func.len > 2
        t = Thing()
        self.assertTrue(e.eval(t))

        e = Thing.none_func.len > 2
        self.assertFalse(e.eval(t))

        e = Thing.none_func.len == 0
        self.assertFalse(e.eval(t))

    def test_not_op(self):
        class Thing(BoolExprEnabledClass):
            foo = False

        e = Thing.foo != True
        # Note following doesn't work
        # e = not Thing.foo
        t = Thing()
        self.assertTrue(e.eval(t))

        e = ~Thing.foo
        self.assertTrue(e.eval(t))

        t.foo = True
        e = Thing.foo
        self.assertTrue(e.eval(t))
