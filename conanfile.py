from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class HttpParserConan(ConanFile):
    name = "http-parser"
    version = "2.7.1"
    description = "http request/response parser for c"
    url = "https://github.com/theirix/conan-http-parser"
    license = "https://github.com/nodejs/http-parser/blob/release-%s/LICENSE-MIT" % version
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "%s.patch" % name

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("https://github.com/nodejs/http-parser/archive/v%s.tar.gz" % (self.version))
        os.rename('http-parser-%s' % (self.version), self.name)

    def build(self):
        tools.patch(patch_file=os.path.join(self.build_folder, 'http-parser.patch'),
                    base_path=self.name)

        env_build = AutoToolsBuildEnvironment(self)

        if self.settings.os == "Linux" or self.settings.os == "Macos":

            target = 'install' if self.options.shared else 'install-static'

            with tools.environment_append(env_build.vars):
                with tools.chdir(self.name):
                    cmd = 'make PREFIX=distr CFLAGS_FAST_EXTRA=-Wno-error CFLAGS_DEBUG_EXTRA=-Wno-error %s' % (target)
                    self.output.warn(cmd)
                    self.run(cmd)

    def package(self):
        self.copy("*.h", dst="include", src="%s/distr/include" % (self.name))
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="%s/distr/lib/*.dylib" % self.name, dst="lib", keep_path=False)
            else:
                self.copy(pattern="%s/distr/lib/*.so*" % self.name, dst="lib", keep_path=False)
        else:
            self.copy(pattern="%s/distr/lib/*.a" % self.name, dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.cpp_info.libs = ['http_parser']
