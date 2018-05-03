from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class HttpParserConan(ConanFile):
    name = "http-parser"
    version = "2.7.1p1"
    description = "http request/response parser for c"
    url = "https://github.com/theirix/conan-http-parser"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["LICENSE.md", "%s.patch" % name]

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        upstream_ver = self.version.split("p")[0]
        tools.get("https://github.com/nodejs/http-parser/archive/v%s.tar.gz" % upstream_ver)
        os.rename('http-parser-%s' % upstream_ver, self.name)

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
        self.copy("license*", dst="licenses", src="%s" % (self.name), ignore_case=True, keep_path=False)
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
