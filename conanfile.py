from conans import ConanFile
from conans import tools
import os, shutil

class QSqlCipherConan(ConanFile):
    name = 'qsqlcipher'
    branch = '5.15'
    url = 'https://github.com/umogSlayer/conan-qsqlcipher'
    version = '1.0' + branch
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'qmake'
    requires = ['sqlcipher/4.4.2']

    def source(self):
        sources_git = tools.Git(folder='qsqlcipher')
        sources_git.clone('https://github.com/sjemens/qsqlcipher-qt5.git',
                          branch=self.branch,
                          shallow=True)
