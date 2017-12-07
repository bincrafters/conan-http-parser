[![Build Status](https://travis-ci.org/theirix/conan-http-parser.svg)](https://travis-ci.org/theirix/conan-http-parser)
[![Build status](https://ci.appveyor.com/api/projects/status/18pdj80qtc0q1p64?svg=true)](https://ci.appveyor.com/project/theirix/conan-http-parser)

# conan-http-parser

[Conan.io](https://conan.io) package for [http-parser](https://github.com/open-source-parsers/http-parser) library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/http-parser/2.7.1/theirix/stable).

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload http-parser/2.7.1@theirix/stable --all
    
## Reuse the packages

### basic setup

    $ conan install http-parser/2.7.1@theirix/stable

### Prerequirements

    JsonCpp needs at least cmake 3.1 for building.
		If you do not have one, specify flag http-parser:use_cmake_installer=True
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    http-parser/2.7.1@theirix/stable

    [options]
    http-parser:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
