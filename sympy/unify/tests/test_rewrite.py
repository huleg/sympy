from sympy.unify.rewrite import rewriterule
from sympy import sin, cos, Basic, Symbol, S
from sympy.abc import x, y, z
from sympy.core.compatibility import next
from sympy.rules.rl import rebuild
from sympy.assumptions import Q

p, q = Symbol('p'), Symbol('q')

def test_simple():
    rl = rewriterule(Basic(p, 1), Basic(p, 2), variables=(p,))
    assert list(rl(Basic(3, 1))) == [Basic(3, 2)]

    p1 = p**2
    p2 = p**3
    rl = rewriterule(p1, p2, variables=(p,))

    expr = x**2
    assert list(rl(expr)) == [x**3]

def test_simple_variables():
    rl = rewriterule(Basic(x, 1), Basic(x, 2), variables=(x,))
    assert list(rl(Basic(3, 1))) == [Basic(3, 2)]

    rl = rewriterule(x**2, x**3, variables=(x,))
    assert list(rl(y**2)) == [y**3]

def test_moderate():
    p1 = p**2 + q**3
    p2 = (p*q)**4
    rl = rewriterule(p1, p2, (p, q))

    expr = x**2 + y**3
    assert list(rl(expr)) == [(x*y)**4]

def test_sincos():
    p1 = sin(p)**2 + sin(p)**2
    p2 = 1
    rl = rewriterule(p1, p2, (p, q))

    assert list(rl(sin(x)**2 + sin(x)**2)) == [1]
    assert list(rl(sin(y)**2 + sin(y)**2)) == [1]

def test_Exprs_ok():
    rl = rewriterule(p+q, q+p, (p, q))
    next(rl(x+y)).is_commutative
    str(next(rl(x+y)))

def test_condition_simple():
    rl = rewriterule(x, x+1, [x], lambda x: x < 10)
    assert not list(rl(S(15)))
    assert rebuild(next(rl(S(5)))) == 6


def test_condition_multiple():
    rl = rewriterule(x + y, x**y, [x,y], lambda x, y: x.is_integer)

    a = Symbol('a')
    b = Symbol('b', integer=True)
    expr = a + b
    assert list(rl(expr)) == [b**a]

    c = Symbol('c', integer=True)
    d = Symbol('d', integer=True)
    assert set(rl(c + d)) == set([c**d, d**c])

def test_assumptions():
    rl = rewriterule(x + y, x**y, [x, y], assume=Q.integer(x))

    a, b = map(Symbol, 'ab')
    expr = a + b
    assert list(rl(expr, Q.integer(b))) == [b**a]