import tempfile
import subprocess as sp
import os.path as pth
import ctypes as ct


def build(code, lang="c", cflags=None, lflags=None):

    # create tempfile to host code
    fh = tempfile.NamedTemporaryFile(suffix=".%s" % lang)
    fh.write(code)
    fh.flush()
    working_dir = pth.dirname(fh.name)

    # build up compilation args
    if lang == "c":
        cc = "gcc"
    elif lang == "cpp":
        cc = "g++"

    default_cflags = ["-fPIC", "-O3", "-Wall"]
    default_lflags = ["-shared"]
    cflags = cflags if cflags else []
    lflags = lflags if lflags else []
    flags = list(set(default_cflags + default_lflags + cflags + lflags))

    soname = pth.join(working_dir, "lib.so")
    sp.check_call([cc, "-o", soname, fh.name] + flags)
    lib = ct.cdll.LoadLibrary(soname)
    fh.close()
    return lib

if __name__ == '__main__':
    code = """
    int sum(int a, int b)
    {
        int acc = 0;
        for (int i = 0; i < 1000; ++i) {
            acc += a;
            acc += b;
            acc += b;
            acc += b;
            acc += b;
            acc += b;
        }

        return acc;
    }
    """
    lib = build(code,lang="c")
    print lib.sum(1,2)
