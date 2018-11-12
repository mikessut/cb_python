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
        #import pdb; pdb.set_trace()
        self.assertTrue(e.eval(a, b))

        e = 0 < ThingA.a
        self.assertTrue(e.eval(a,b))

        e2 = ThingB.mylist.len > 2
        self.assertTrue(e2.eval(a,b))

        e2 = 2 < ThingB.mylist.len
        self.assertTrue(e2.eval(a,b))

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
        #import pdb; pdb.set_trace()
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
