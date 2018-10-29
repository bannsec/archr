import logging
import angr
import os

l = logging.getLogger("archr.bows.angr")

from . import Bow

class angrProjectBow(Bow):
    """
    Describes a target in the form of a Docker image.
    """

    def __init__(self, target, mapping_bow):
        super(angrProjectBow, self).__init__(target)
        self.mapping_bow = mapping_bow
        self.project = None
        self.target.mount_local()

    def fire(self, **kwargs): #pylint:disable=arguments-differ
        if self.project is None:
            lib_mapping = self.mapping_bow.fire()
            the_libs = [ self.target.resolve_local_path(lib) for lib in lib_mapping if lib.startswith("/") ]
            lib_opts = { os.path.basename(lib) : {'base_addr' : libaddr} for lib, libaddr in lib_mapping.items() }
            bin_opts = { "base_addr": 0x555555554000 }
            the_binary = self.target.resolve_local_path(self.target.target_path)

            self.project =angr.Project(the_binary, force_load_libs=the_libs, lib_opts=lib_opts, main_opts=bin_opts, **kwargs)
        return self.project