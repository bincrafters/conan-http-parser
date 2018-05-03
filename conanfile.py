#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools

class HttpParserConan(ConanFile):
    name = "http-parser"
    version = "2.8.1"
    description = "http request/response parser for c"
    url = "https://github.com/bincrafters/conan-http-parser"
    homepage = "https://github.com/nodejs/http-parser"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports = "LICENSE.md"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
        if self.settings.compiler == "Visual Studio" and self.options.shared:
            raise Exception("Shared builds on Windows are not supported")

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        upstream_ver = self.version.split("p")[0]
        tools.get("https://github.com/nodejs/http-parser/archive/v%s.tar.gz" % upstream_ver)
        os.rename('http-parser-%s' % upstream_ver, self.source_subfolder)

        shutil.copy("CMakeLists.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.definitions['WITH_CONAN'] = True
        cmake.definitions['WITH_TESTS'] = False
        # BUILD_SHARED_LIBS is set automatically
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE-MIT", dst="licenses", src=self.source_subfolder, ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.cpp_info.libs:
            raise Exception("No libs collected")
