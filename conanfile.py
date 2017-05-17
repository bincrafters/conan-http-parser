from conans import ConanFile, AutoToolsBuildEnvironment
from conans.tools import download, untargz, check_sha1, environment_append
import os

class HttpParserConan(ConanFile):
    name = "http-parser"
    version = "2.7.1"
    description = "http request/response parser for c"
    url = "https://github.com/theirix/conan-http-parser"
    license = "https://github.com/nodejs/http-parser/blob/release-%s/LICENSE-MIT" % version
    FOLDER_NAME = 'http-parser-%s' % version
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "%s.patch" % name

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tarball_name = self.FOLDER_NAME + '.tar.gz'
        download("https://github.com/nodejs/http-parser/archive/v%s.tar.gz"
                 % (self.version), tarball_name)
        check_sha1(tarball_name, "e122b1178ec5c9920186cc8293aca9eca7584b12")
        untargz(tarball_name)
        os.unlink(tarball_name)
        self.run("cd %s && patch -p1 < %s/%s.patch" % (self.FOLDER_NAME, self.conanfile_directory, self.name))

    def build(self):

        env_build = AutoToolsBuildEnvironment(self)

        if self.settings.os == "Linux" or self.settings.os == "Macos":

            suffix = ''
            if self.options.shared:
                suffix = 'install'
            else:
                suffix = 'install-static'

            with environment_append(env_build.vars):
                cmd = 'cd %s && make PREFIX=%s/%s/distr %s' % (self.FOLDER_NAME, self.conanfile_directory, self.FOLDER_NAME, suffix)
                self.output.warn('Running: ' + cmd)
                self.run(cmd)

    def package(self):
        self.copy("*.h", dst="include", src="%s/distr/include" % (self.FOLDER_NAME))
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.cpp_info.libs = ['http_parser']
