from conans import ConanFile, MSBuild
from conans import tools
import os, shutil

class QSqlCipherConan(ConanFile):
    name = 'qsqlcipher'
    version = '5.15-3'
    url = 'https://github.com/umogSlayer/conan-qsqlcipher'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'qmake'
    requires = ['sqlcipher/4.4.2', 'qt/5.15.2@bincrafters/stable']
    exports = ["patches/*.patch"]

    def source(self):
        sources_git = tools.Git(folder='qsqlcipher')
        sources_git.clone('https://github.com/sjemens/qsqlcipher-qt5.git',
                          branch='v%s' % self.version,
                          shallow=True)

    def _make_program(self):
        return "make"

    def build(self):
        tools.patch(base_path="qsqlcipher", patch_file="patches/qsqlcipher.pro-%s.patch" % self.version, strip=1)
        if self.settings.compiler == "Visual Studio":
            with tools.vcvars(self.settings):
                self.run("qmake -spec win32-msvc -tp vc CONFIG+=\"staticlib conan-sqlcipher\" qsqlcipher\\qsqlcipher\\qsqlcipher.pro", run_environment=True)
            msbuild = MSBuild(self)
            msbuild.build("qsqlcipher.vcxproj")
        else:
            self.run("qmake CONFIG+=\"staticlib conan-sqlcipher\" qsqlcipher/qsqlcipher.pro", run_environment=True)
            self.run(self._make_program(), run_environment=True)

    def package(self):
        if self.settings.compiler == "Visual Studio":
            self.copy('*.lib', dst='lib', src='plugins/sqldrivers')
        else:
            self.copy('*.a', dst='lib', src='qsqlcipher/plugins/sqldrivers')

    def package_info(self):
        self.cpp_info.libs = ['qsqlcipher']
