import pile
code = """
int sum(int a, int b)
{
    return a+b;
}
"""
lib = pile.build(code)

print lib.sum(1,2)
