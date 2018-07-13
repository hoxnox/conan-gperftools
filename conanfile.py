from nxtools import NxConanFile
from conans import AutoToolsBuildEnvironment, tools

class GperfToolsConan(NxConanFile):
    name = "gperftools"
    description = "The fastest malloc we have seen."
    version = "2.5"
    options = {"shared":[True, False], "cpuprof":[True, False], "heapprof":[True, False], "heapchecker":[True, False]}
    default_options = "shared=False", "cpuprof=False", "heapprof=False", "heapchecker=False"
    url = "https://github.com/hoxnox/conan-gperftools"
    license = "https://github.com/gperftools/gperftools/blob/master/COPYING"

    def requirements(self):
        if self.options.cpuprof or self.options.heapprof or self.options.heapchecker:
            self.requires("libunwind/1.2@hoxnox/stable")

    def do_source(self):
        self.retrieve("6fa2748f1acdf44d750253e160cf6e2e72571329b42e563b455bde09e9e85173",
            [
                'vendor://google/gperftools/gperftools-{version}.tar.gz'.format(version=self.version),
                'https://github.com/gperftools/gperftools/releases/download/gperftools-{version}/gperftools-{version}.tar.gz'.format(version=self.version)
            ], "gperftools-{v}.tar.gz".format(v = self.version))

    def do_build(self):
        build_dir = "{staging_dir}/src".format(staging_dir=self.staging_dir)
        tools.untargz("gperftools-{v}.tar.gz".format(v=self.version), build_dir)
        env_build = AutoToolsBuildEnvironment(self)
        
        with tools.environment_append(env_build.vars):
            self.run("cd {build_dir}/gperftools-{v} && ./configure --prefix=\"{staging}\" {is_minimal}"
                     " {shared} {cpuprof} {heapprof} {heapchecker}".format(
                         v = self.version,
                         build_dir=build_dir,
                         staging=self.staging_dir,
                         is_minimal="" if self.options.cpuprof or self.options.heapprof or self.options.heapchecker else "--enable-minimal",
                         shared="--enable-shared --disable-static" if self.options.shared else "--enable-static --disable-shared",
                         cpuprof="--enable-cpu-profiler" if self.options.cpuprof else "--disable-cpu-profiler",
                         heapprof="--enable-heap-profiler" if self.options.heapprof else "--disable-heap-profiler",
                         heapchecker="--enable-heap-checker" if self.options.heapchecker else "--disable-heap-checker"))
            self.run("cd {build_dir}/gperftools-{v} && make install".format(v = self.version, build_dir = build_dir))

    def do_package_info(self):
        if self.options.cpuprof or self.options.heapprof or self.options.heapchecker:
            self.cpp_info.libs = ["tcmalloc"]
        else:
            self.cpp_info.libs = ["tcmalloc_minimal"]


