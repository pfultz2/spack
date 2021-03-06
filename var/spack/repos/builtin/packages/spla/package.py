# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spla(CMakePackage):
    """Specialized Parallel Linear Algebra, providing distributed GEMM
    functionality for specific matrix distributions with optional GPU
    acceleration."""

    homepage = "https://github.com/eth-cscs/spla"
    url      = "https://github.com/eth-cscs/spla/archive/v1.0.0.tar.gz"
    git = 'https://github.com/eth-cscs/spla.git'

    version('1.1.0', sha256='b0c4ebe4988abc2b3434e6c50e7eb0612f3f401bc1aa79ad58a6a92dc87fa65b')
    version('1.0.0', sha256='a0eb269b84d7525b223dc650de12170bba30fbb3ae4f93eb2b5cbdce335e4da1')
    version('develop', branch='develop')
    version('master', branch='master')

    variant('openmp', default=True, description="Build with OpenMP support")
    variant('static', default=False, description="Build as static library")
    variant('cuda', default=False, description="CUDA backend")
    variant('rocm', default=False, description="ROCm backend")

    conflicts("+cuda", when="+rocm", msg="+cuda and +rocm are mutually exclusive")

    depends_on('mpi')
    depends_on('blas')
    depends_on('cmake@3.10:', type='build')

    depends_on('cuda', when='+cuda')
    depends_on('rocblas', when='+rocm')
    depends_on('hip', when='+rocm')
    depends_on('hsakmt-roct', when='+rocm', type='link')
    depends_on('hsa-rocr-dev', when='+rocm', type='link')

    def cmake_args(self):
        args = []

        if '+openmp' in self.spec:
            args += ["-DSPLA_OMP=ON"]
        else:
            args += ["-DSPLA_OMP=OFF"]

        if '+cuda' in self.spec:
            args += ["-DSPLA_GPU_BACKEND=CUDA"]
        else:
            args += ["-DSPLA_GPU_BACKEND=OFF"]

        if '+rocm' in self.spec:
            args += ["-DSPLA_GPU_BACKEND=ROCM"]
        else:
            args += ["-DSPLA_GPU_BACKEND=OFF"]

        if '+static' in self.spec:
            args += ["-DSPLA_STATIC=ON"]
        else:
            args += ["-DSPLA_STATIC=OFF"]
        return args
