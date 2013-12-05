import cpile
code = """
int sum(int a, int b)
{
    return a+b;
}
"""
lib = cpile.build(code)

print lib.sum(1,2)
