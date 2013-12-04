pile
====

Automatic inline c++ and c compilation within python

Installation
============

    python setup.py install

Usage
=====

    import pile
    code = """
    int sum(int a, int b)
    {
        return a+b;
    }
    """
    lib = pile.build(code)
    print lib.sum(1,2)
