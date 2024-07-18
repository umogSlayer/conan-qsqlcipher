from conan import ConanFile

from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout

class QSqlCipherConan(ConanFile):
    name = 'qsqlcipher-qt6'
    package_type = "library"
    version = '6.7-1'
    url = 'https://github.com/umogSlayer/conan-qsqlcipher'
    settings = 'os', 'compiler', 'build_type', 'arch'
    exports_sources = ["CMakeLists.txt", "src/*"]
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": True,
    }

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("sqlcipher/4.4.3")
        self.requires("qt/[>=6.7.0]")

    def generate(self):
        CMakeDeps(self).generate()
        CMakeToolchain(self).generate()

    def build(self):
        cm = CMake(self)
        cm.configure()
        cm.build()

    def package(self):
        cm = CMake(self)
        cm.install()

    def package_info(self):
        if not self.options.shared:
            self.cpp_info.libs = ['qsqlcipher']
