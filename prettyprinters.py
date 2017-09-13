from printutils import *

try:
    import gdb
except ImportError:
    print("Not running inside of GDB, exiting...")
    exit()

class malloc_par_printer:
    "pretty printer for the malloc_par struct (mp_)"

    def __init__(self, val):
        self.val = val

    def to_string(self):
        mp = color_title("struct malloc_par {")
        mp += "\n{:16} = ".format("trim_threshold")
        mp += color_value("{:#x}".format(self.val['trim_threshold']))
        mp += "\n{:16} = ".format("top_pad")
        mp += color_value("{:#x}".format(self.val['top_pad']))
        mp += "\n{:16} = ".format("mmap_threshold")
        mp += color_value("{:#x}".format(self.val['mmap_threshold']))
        mp += "\n{:16} = ".format("arena_test")
        mp += color_value("{:#x}".format(self.val['arena_test']))
        mp += "\n{:16} = ".format("arena_max")
        mp += color_value("{:#x}".format(self.val['arena_max']))
        mp += "\n{:16} = ".format("n_mmaps")
        mp += color_value("{:#x}".format(self.val['n_mmaps']))
        mp += "\n{:16} = ".format("n_mmaps_max")
        mp += color_value("{:#x}".format(self.val['n_mmaps_max']))
        mp += "\n{:16} = ".format("max_n_mmaps")
        mp += color_value("{:#x}".format(self.val['max_n_mmaps']))
        mp += "\n{:16} = ".format("no_dyn_threshold")
        mp += color_value("{:#x}".format(self.val['no_dyn_threshold']))
        mp += "\n{:16} = ".format("mmapped_mem")
        mp += color_value("{:#x}".format(self.val['mmapped_mem']))
        mp += "\n{:16} = ".format("max_mmapped_mem")
        mp += color_value("{:#x}".format(self.val['max_mmapped_mem']))
        mp += "\n{:16} = ".format("max_total_mem")
        mp += color_value("{:#x}".format(self.val['max_total_mem']))
        mp += "\n{:16} = ".format("sbrk_base")
        mp += color_value("{:#x}".format(self.val['sbrk_base']))
        return mp

class malloc_state_printer:
    "pretty printer for the malloc_state struct (ar_ptr/main_arena)"

    def __init__(self, val):
        self.val = val

    def to_string(self):
        ms = color_title("struct malloc_state {")
        ms += "\n{:14} = ".format("mutex")
        ms += color_value("{:#x}".format(self.val['mutex']))
        ms += "\n{:14} = ".format("flags")
        ms += color_value("{:#x}".format(self.val['flags']))
        ms += "\n{:14} = ".format("fastbinsY")
        ms += color_value("{}".format("{...}"))
        ms += "\n{:14} = ".format("top")
        ms += color_value("{:#x}".format(self.val['top']))
        ms += "\n{:14} = ".format("last_remainder")
        ms += color_value("{:#x}".format(self.val['last_remainder']))
        ms += "\n{:14} = ".format("bins")
        ms += color_value("{}".format("{...}"))
        ms += "\n{:14} = ".format("binmap")
        ms += color_value("{}".format("{...}"))
        ms += "\n{:14} = ".format("next")
        ms += color_value("{:#x}".format(self.val['next']))
        ms += "\n{:14} = ".format("system_mem")
        ms += color_value("{:#x}".format(self.val['system_mem']))
        ms += "\n{:14} = ".format("max_system_mem")
        ms += color_value("{:#x}".format(self.val['max_system_mem']))
        return ms

class malloc_chunk_printer:
    "pretty printer for the malloc_chunk struct"

    def __init__(self, val):
        self.val = val

    def to_string(self):
        mc = color_title("struct malloc_chunk {")
        mc += "\n{:11} = ".format("prev_size")
        mc += color_value("{:#x}".format(self.val['prev_size']))
        mc += "\n{:11} = ".format("size")
        mc += color_value("{:#x}".format(self.val['size']))
        mc += "\n{:11} = ".format("fd")
        mc += color_value("{:#x}".format(self.val['fd']))
        mc += "\n{:11} = ".format("bk")
        mc += color_value("{:#x}".format(self.val['bk']))
        mc += "\n{:11} = ".format("fd_nextsize")
        mc += color_value("{:#x}".format(self.val['fd_nextsize']))
        mc += "\n{:11} = ".format("bk_nextsize")
        mc += color_value("{:#x}".format(self.val['bk_nextsize']))
        return mc

class heap_info_printer:
    "pretty printer for the heap_info struct (_heap_info)"

    def __init__(self, val):
        self.val = val

    def to_string(self):
        hi = color_title("struct heap_info {")
        hi += "\n{:13} = ".format("ar_ptr")
        hi += color_value("{:#x}".format(self.val['ar_ptr']))
        hi += "\n{:13} = ".format("prev")
        hi += color_value("{:#x}".format(self.val['prev']))
        hi += "\n{:13} = ".format("size")
        hi += color_value("{:#x}".format(self.val['size']))
        hi += "\n{:13} = ".format("mprotect_size")
        hi += color_value("{:#x}".format(self.val['mprotect_size']))
        return hi

def pretty_print_heap_lookup(val):
    "Look-up and return a pretty printer that can print val."

    val_type = val.type

    # If it points to a reference, get the reference.
    if val_type.code == gdb.TYPE_CODE_REF:
        val_type = val_type.target()

    # Get the unqualified type, stripped of typedefs.
    val_type = val_type.unqualified().strip_typedefs()

    # Get the type name.
    typename = val_type.tag
    if typename == None:
        return None
    elif typename == "malloc_par":
        return malloc_par_printer(val)
    elif typename == "malloc_state":
        return malloc_state_printer(val)
    elif typename == "malloc_chunk":
        return malloc_chunk_printer(val)
    elif typename == "_heap_info":
        return heap_info_printer(val)
    else:
        print(typename)

    # Cannot find a pretty printer for type(val)
    return None

gdb.pretty_printers.append(pretty_print_heap_lookup)
