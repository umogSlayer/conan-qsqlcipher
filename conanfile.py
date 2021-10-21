from conans import ConanFile, MSBuild
from conans import tools
from conans.errors import ConanInvalidConfiguration
import os, shutil

class QSqlCipherConan(ConanFile):
    name = 'qsqlcipher'
    version_prefix = '5.15'
    version_suffix = '-3'
    branch_name = "%s%s" % (version_prefix, version_suffix)
    url = 'https://github.com/umogSlayer/conan-qsqlcipher'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'qmake'
    requires = ['sqlcipher/4.4.3', 'qt/5.15.2@onyxcorp/stable']
    exports = ["patches/*.patch"]
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
    }

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
        sources_git = tools.Git(folder='qsqlcipher')
        sources_git.clone('https://github.com/sjemens/qsqlcipher-qt5.git',
                          branch='v%s' % self.branch_name,
                          shallow=True)

    def _make_program(self):
        return "make"

    def build(self):
        tools.patch(base_path="qsqlcipher", patch_file="patches/qsqlcipher.pro-%s.patch" % self.branch_name, strip=1)
        qmake_config_flags = ["conan-sqlcipher"]
        if not self.options.shared:
            qmake_config_flags += ["staticlib"]
        qmake_config_flags_as_param = " ".join(qmake_config_flags)
        if self.settings.compiler == "Visual Studio":
            with tools.vcvars(self.settings):
                self.run("qmake -spec win32-msvc -tp vc CONFIG+=\"%s\" qsqlcipher\\qsqlcipher\\qsqlcipher.pro" % qmake_config_flags_as_param, run_environment=True)
            msbuild = MSBuild(self)
            msbuild.build("qsqlcipher.vcxproj")
        else:
            additional_libs = ""
            if tools.is_apple_os(self.settings.os):
                additional_libs = "LIBS+=\"-framework AppKit -framework Security -framework Foundation\""
            self.run("qmake CONFIG+=\"{config_flags}\" {additional_libs} qsqlcipher/qsqlcipher.pro".format(
                    config_flags=qmake_config_flags_as_param,
                    additional_libs=additional_libs),
                run_environment=True)

            self.run(self._make_program(), run_environment=True)

    def package(self):
        if self.settings.compiler == "Visual Studio":
            self.copy('*.lib', dst='lib', src='plugins/sqldrivers')
            self.copy('*.dll', dst='plugins/sqldrivers', src='plugins/sqldrivers')
        else:
            self.copy('*.a', dst='lib', src='qsqlcipher/plugins/sqldrivers')
            self.copy('*.so*', dst='plugins/sqldrivers', src='qsqlcipher/plugins/sqldrivers')
            self.copy('*.dylib', dst='plugins/sqldrivers', src='qsqlcipher/plugins/sqldrivers')

    def package_info(self):
        if not self.options.shared:
            if self.settings.compiler == "Visual Studio" and self.settings.build_type == "Debug":
                self.cpp_info.libs = ['qsqlcipherd']
            else:
                self.cpp_info.libs = ['qsqlcipher']

    def package_id(self):
        self.info.shared_library_package_id()
