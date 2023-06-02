from conan import ConanFile
from conan.errors import ConanInvalidConfiguration

from conan.tools.env import VirtualRunEnv
from conan.tools.files import patch, copy
from conan.tools.scm import Git
from conan.tools.apple import is_apple_os
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake

import os, shutil

class QSqlCipherConan(ConanFile):
    name = 'qsqlcipher'
    package_type = "library"
    version_prefix = '5.15'
    version_suffix = '-3'
    branch_name = "%s%s" % (version_prefix, version_suffix)
    url = 'https://github.com/umogSlayer/conan-qsqlcipher'
    settings = 'os', 'compiler', 'build_type', 'arch'
    requires = ['sqlcipher/4.4.3', 'qt/5.15.2@onyxcorp/stable']
    exports = ["patches/*.patch", "CMakeLists.txt"]
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
    }

    def generate(self):
        VirtualRunEnv(self).generate(scope="build")
        CMakeToolchain(self).generate()
        CMakeDeps(self).generate()

    def set_version(self):
        if self.version is None:
            self.version = self.version_prefix + self.version_suffix

    def validate(self):
        if self.version[:len(self.version_prefix)] != self.version_prefix \
                or self.version[-len(self.version_suffix):] != self.version_suffix:
            raise ConanInvalidConfiguration(
                "Invalid version number, should be %s.X%s" \
                % (self.version_prefix, self.version_suffix))
        # else "compatibility mode"
        if self.version != self.version_prefix + self.version_suffix:
            qt = self.dependencies["qt"].ref
            if qt.version != self.version[:-len(self.version_suffix)]:
                raise ConanInvalidConfiguration("Package version should match Qt version "
                                                + qt.version)

    def source(self):
        sources_git = Git(self)
        clone_args = ['--depth', '1', '--branch', 'v%s' % self.branch_name]
        sources_git.clone('https://github.com/sjemens/qsqlcipher-qt5.git',
                          args=clone_args)
        copy(self, "CMakeLists.txt", ".", "qsqlcipher-qt5")

    def _make_program(self):
        return "make"

    def build(self):
        cm = CMake(self)
        cm.configure(build_script_folder="qsqlcipher-qt5")
        cm.build()

    def package(self):
        cm = CMake(self)
        cm.install()

    def package_info(self):
        if not self.options.shared:
            self.cpp_info.libs = ['qsqlcipher']
