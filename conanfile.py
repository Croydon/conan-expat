from conans import ConanFile, CMake, tools

class ExpatConan(ConanFile):
    name = "Expat"
    version = "2.2.5"
    description = "Recipe for Expat library"
    topics = ("conan", "expat", "xml", "parsing")
    url = "https://github.com/Pix4D/conan-expat"
    homepage = "https://github.com/piponazo/conan-expat"
    author = "piponazo"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {'shared': 'False'}
    generators = "cmake"
    exports_sources = ['FindExpat.cmake', 'patches/*']

    def source(self):
        self.run("git clone --depth 1 --branch R_2_2_5 %s" % self.source_url)

    def build(self):
        tools.patch(base_path = "libexpat", patch_file="patches/useConanFileAndIncreaseCMakeVersion.patch")

        cmake = CMake(self, parallel=True)

        cmake_args = { "BUILD_doc" : "OFF",
                       "BUILD_examples" : "OFF",
                       "BUILD_shared" : self.options.shared,
                       "BUILD_tests" : "OFF",
                       "BUILD_tools" : "OFF",
                       "CMAKE_POSITION_INDEPENDENT_CODE": "ON",
                     }

        cmake.configure(source_dir="../libexpat/expat", build_dir="build", defs=cmake_args)
        cmake.build(target="install")

    def package(self):
        self.copy("FindExpat.cmake", ".", ".")

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["expatd"]
        else:
            self.cpp_info.libs = ["expat"]
        if not self.options.shared:
            self.cpp_info.defines = ["XML_STATIC"]

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
