# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.module_cmd import (
    load_module, module, get_path_args_from_module_line
)


class CrayLibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    homepage = "https://docs.nersc.gov/programming/libraries/libsci/"
    url = "https://docs.nersc.gov/programming/libraries/libsci/"

    version('0.0.0', '')

    variant("shared", default=True, description="enable shared libs")
    variant("openmp", default=False, description="link with openmp")
    variant("mpi", default=False, description="link with mpi libs")

    provides("blas")
    provides("lapack")
    provides("scalapack")

    canonical_names = {
        'gcc': 'GNU',
        'cce': 'CRAY',
        'intel': 'INTEL',
    }

    @property
    def fetcher(self):
        raise InstallError("""This package is intended to be a placeholder for Cray's
libsci, usually provided via the module system as 'cray-libsci'.

Add to your packages.yaml:

    packages:
        cray-libsci:
            buildable: false
            modules:
                cray-libsci+mpi+openmp@18.07.1: cray-libsci/18.07.1
                cray-libsci+mpi~openmp@18.07.1: cray-libsci/18.07.1
                cray-libsci~mpi+openmp@18.07.1: cray-libsci/18.07.1
                cray-libsci~mpi~openmp@18.07.1: cray-libsci/18.07.1

Replace the version numbers with the ones matching the module(s).
        """)

    @property
    def modname(self):
        return "cray-libsci/{0}".format(self.version)

    @property
    def external_prefix(self):
        libsci_module = module("show", self.modname).splitlines()

        for line in libsci_module:
            if "CRAY_LIBSCI_PREFIX_DIR" in line:
                return get_path_args_from_module_line(line)[0]

    @property
    def blas_libs(self):
        shared = True if "+shared" in self.spec else False
        compiler = self.spec.compiler.name

        if "+openmp" in self.spec and "+mpi" in self.spec:
            lib = "libsci_{0}_mpi_mp"
        elif "+openmp" in self.spec:
            lib = "libsci_{0}_mp"
        elif "+mpi" in self.spec:
            lib = "libsci_{0}_mpi"
        else:
            lib = "libsci_{0}"

        libname = lib.format(self.canonical_names[compiler].lower())

        return find_libraries(
            libname,
            root=self.prefix.lib,
            shared=shared,
            recursive=False)

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """ Load the module into the environment for dependents """
        version = self.version
        mod = 'cray-libsci/{0}'.format(version)
        load_module(mod)

    def install(self, spec, prefix):
        pass
