from __future__ import print_function
import codecs
import os
from setuptools import setup
from setuptools.command.build_py import build_py
from shutil import copy2, rmtree, copytree
import subprocess
from sys import platform
from tempfile import mkdtemp


__version__ = 3, 0, 0
# "gopkg.in/src-d/go-git.v%d" % __version__[0]
GOGIT_ORIGIN = "github.com/vmarkovtsev/go-git"
SHLIBEXT = "dylib" if platform == "darwin" else "so"


class GoBuildPy(build_py):
    def run(self):
        if not self.dry_run:
            self._build()
        super(GoBuildPy, self).run()

    def get_outputs(self, *args, **kwargs):
        outputs = super(GoBuildPy, self).get_outputs(*args, **kwargs)
        outputs.extend(self.go_generated_files)
        return outputs

    def _build(self, builddir=None):
        header = os.getenv("GOGIT_HEADER", None)
        library = os.getenv("GOGIT_LIBRARY", None)
        sd = os.path.dirname(__file__)
        iheader = "libgogit.h"
        ilibrary = "libgogit." + SHLIBEXT

        def install_files():
            self.go_generated_files = []
            dest_dir = os.path.join(self.build_lib, "gypogit")
            self.mkpath(dest_dir)
            header_dest = os.path.join(dest_dir, iheader)
            print("copy %s -> %s" % (header, header_dest))
            copy2(header, header_dest)
            library_dest = os.path.join(dest_dir, ilibrary)
            print("copy %s -> %s" % (library, library_dest))
            copy2(library, library_dest)
            self.go_generated_files.extend((header_dest, library_dest))
            print("write gopaths.py")
            with codecs.open(os.path.join(sd, "gypogit", "go_paths.py"),
                             "w", "utf-8") as fout:
                fout.write("# -*- coding: utf-8 -*-\n")
                fout.write("HEADER = \"%s\"\n" % iheader)
                fout.write("LIBRARY = \"%s\"\n" % ilibrary)

        if header is not None and library is not None:
            print("Skipping the build because GOGIT_HEADER and GOGIT_LIBRARY "
                  "are set")
            install_files()
            return
        if builddir is None:
            builddir = mkdtemp(prefix="setuptools-go-")
        print("Building in %s" % builddir)
        try:
            goenv = os.environ.copy()
            goenv["GOPATH"] = builddir
            print("go get")
            subprocess.check_call(("go", "get", GOGIT_ORIGIN), env=goenv,
                                  cwd=builddir)
            print("go build")
            subprocess.check_call((
                "go", "build", "-o", ilibrary, "-buildmode=c-shared",
                os.path.join(GOGIT_ORIGIN, "cshared")), env=goenv,
                cwd=builddir)
            header = os.path.join(builddir, iheader)
            library = os.path.join(builddir, ilibrary)
            if not os.path.exists(library):
                raise RuntimeError("Looks like go failed to build the shared "
                                   "library")
            if not os.path.exists(header):
                raise RuntimeError("Looks like go did not create the header "
                                   "file")
            install_files()
        finally:
            clean = os.getenv("GOGIT_NOCLEAN", None)
            if clean is None:
                print("Removing the build directory (export GOGIT_NOCLEAN to "
                      "avoid this)")
                rmtree(builddir)

setup(
    name="gypogit",
    description="Go-git Python wrapper",
    version="%d.%d.%d" % __version__,
    license="MIT",
    author="Vadim Markovtsev",
    author_email="vadim@sourced.tech",
    url="https://github.com/src-d/gypogit",
    download_url='https://github.com/src-d/gypogit',
    packages=["gypogit"],
    install_requires=["six>=1.0", "cffi>=1.6"],
    package_data={"gypogit": ["README.md", "LICENSE"]},
    cmdclass={'build_py': GoBuildPy},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)