# Copyright (c) Huy Nguyen 2013, 
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.

# * Neither the name of cpile nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import tempfile
import subprocess as sp
import os.path as pth
import os
import ctypes as ct


def build(code, lang="c", cflags=None, lflags=None):

    # create tempfile to host code
    working_dir = tempfile.mkdtemp()
    code_pth = pth.join(working_dir, "code.%s" % lang)
    with open(code_pth, "w") as fh:
        fh.write(code)

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
    
    os.unlink(soname)
    import shutil
    shutil.rmtree(working_dir)
    return lib

def func(code, name="f", lang="c", cflags=None, lflags=None):
    """
    Quick utility to build and return a function corresponding to
    `name`

    """    
    lib = build(code, lang, cflags, lflags)
    f = getattr(lib, name)
    return f
    
def test_build():
    code = """
    int sum(int a, int b)
    {
        return a+b;
    }
    """
    lib = build(code,lang="c")
    r = lib.sum(1,2)
    assert r == 3
    print r

def test_func():
    code = """
    int sum(int a, int b)
    {
        return a+b;
    }
    """
    sum_c = func(code,name="sum", lang="c")
    r = sum_c(1,2)
    assert r == 3
    print r

if __name__ == '__main__':
    test_build()
    test_func()
