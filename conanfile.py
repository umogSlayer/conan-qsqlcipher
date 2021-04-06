from conans import ConanFile
from conans import tools
import os, shutil

class QSqlCipherConan(ConanFile):
    name = 'qsqlcipher'
    version = '5.15-3'
    url = 'https://github.com/umogSlayer/conan-qsqlcipher'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'qmake'
    requires = ['sqlcipher/4.4.2', 'qt/5.15.2@bincrafters/stable']
    exports = ["conan-qsqlcipher.pro", "patches/*.patch"]

    def source(self):
        sources_git = tools.Git(folder='qsqlcipher')
        sources_git.clone('https://github.com/sjemens/qsqlcipher-qt5.git',
                          branch='v%s' % self.version,
                          shallow=True)

    def _make_program(self):
        return "make"

    def build(self):
        tools.patch(base_path="qsqlcipher", patch_file="patches/qsqlcipher.pro-%s.patch" % self.version, strip=1)
        with tools.vcvars(self.settings) if self.settings.compiler == "Visual Studio" else tools.no_op():
            self.run("qmake CONFIG+=\"staticlib conan-sqlcipher\" qsqlcipher/qsqlcipher.pro", run_environment=True)
        if self.settings.compiler != "Visual Studio":
            self.run(self._make_program(), run_environment=True)
        else:
            pass
