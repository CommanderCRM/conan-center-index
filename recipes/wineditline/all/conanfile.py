import os

from conan import ConanFile
from conan.tools.files import get, copy, export_conandata_patches, apply_conandata_patches
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.errors import ConanInvalidConfiguration

required_conan_version = ">=1.52.0"

class WineditlineConan(ConanFile):
    name = "wineditline"
    description = (
        "A BSD-licensed EditLine API implementation for the native "
        "Windows Console"
    )
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://mingweditline.sourceforge.net/"
    topics = ("readline", "editline", "windows")
    license = "BSD-3-Clause"
    settings = ("os", "arch", "compiler", "build_type")
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
    }
    exports_sources = ("CMakeLists.txt")

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        if self.settings.os != "Windows":
            message = "wineditline is supported only on Windows."
            raise ConanInvalidConfiguration(message)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package_id(self):
        del self.info.settings.compiler

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "COPYING", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["edit"]
