# cpile

Automatic inline c++ and c compilation within python. 

The goal of this project is to create a library that you can use
to interactively explore C code and just-in-time compilation.

### Installation

    python setup.py install

### Usage

    import cpile
    code = """
    int sum(int a, int b)
    {
        return a+b;
    }
    """
    lib = cpile.build(code)
    print lib.sum(1,2)


### Interactive C

You can get even more interactive by compiling functions on the fly:

    import cpile
    f = cpile.func("int f(int a){ return a * a;}")
    print f(10)