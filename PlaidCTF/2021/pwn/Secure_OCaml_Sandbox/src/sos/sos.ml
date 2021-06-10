open struct
  let blocked = `Blocked

  module Blocked = struct
    let blocked = blocked
  end
end

module Fixed_stdlib = struct
  let open_in = blocked
  let open_in_bin = blocked
  let open_in_gen = blocked
  let open_out = blocked
  let open_out_bin = blocked
  let open_out_gen = blocked
  let unsafe_really_input = blocked

  module Fixed_arg = struct
    include Arg

    let read_arg = blocked
    let read_arg0 = blocked
    let write_arg = blocked
    let write_arg0 = blocked
  end

  module Fixed_array = struct
    include Array

    let unsafe_set = blocked
    let unsafe_get = blocked

    module Floatarray = struct
      let unsafe_set = blocked
      let unsafe_get = blocked
    end
  end

  module Fixed_arrayLabels = struct
    include ArrayLabels

    let unsafe_set = blocked
    let unsafe_get = blocked

    module Floatarray = struct
      let unsafe_set = blocked
      let unsafe_get = blocked
    end
  end

  module Fixed_bytes = struct
    include Bytes

    let unsafe_blit = blocked
    let unsafe_blit_string = blocked
    let unsafe_fill = blocked
    let unsafe_get = blocked
    let unsafe_set = blocked
    let unsafe_of_string = blocked
    let unsafe_to_string = blocked
  end

  module Fixed_bytesLabels = struct
    include Bytes

    let unsafe_blit = blocked
    let unsafe_blit_string = blocked
    let unsafe_fill = blocked
    let unsafe_get = blocked
    let unsafe_set = blocked
    let unsafe_of_string = blocked
    let unsafe_to_string = blocked
  end

  module Fixed_char = struct
    include Char

    let unsafe_chr = blocked
  end

  module Fixed_filename = struct
    include Filename

    let open_temp_file = blocked
    let temp_file = blocked
  end

  module Fixed_float = struct
    include Float

    module Array = struct
      include Array

      let unsafe_set = blocked
      let unsafe_get = blocked
    end

    module ArrayLabels = struct
      include ArrayLabels

      let unsafe_set = blocked
      let unsafe_get = blocked
    end
  end

  module Fixed_scanf = struct
    include Scanf

    module Scanning = struct
      include Scanning

      let open_in = blocked
      let open_in_bin = blocked
      let close_in = blocked
      let from_file = blocked
      let from_file_bin = blocked
    end
  end

  module Fixed_string = struct
    include String

    let unsafe_blit = blocked
    let unsafe_fill = blocked
    let unsafe_get = blocked
    let unsafe_set = blocked
  end

  module Fixed_stringLabels = struct
    include StringLabels

    let unsafe_blit = blocked
    let unsafe_fill = blocked
    let unsafe_get = blocked
    let unsafe_set = blocked
  end

  module Fixed_stdLabels = struct
    module Array = Fixed_arrayLabels
    module Bytes = Fixed_bytesLabels
    module List = ListLabels
    module String = Fixed_stringLabels
  end

  module Fixed_uchar = struct
    include Uchar

    let unsafe_of_int = blocked
    let unsafe_to_char = blocked
  end

  module Arg = Fixed_arg
  module Array = Fixed_array
  module ArrayLabels = Fixed_arrayLabels
  module Bigarray = Blocked
  module Bytes = Fixed_bytes
  module BytesLabels = Fixed_bytesLabels
  module Char = Fixed_char
  module Filename = Fixed_filename
  module Float = Fixed_float
  module Marshal = Blocked
  module Obj = Blocked
  module Pervasives = Blocked
  module Printexc = Blocked
  module Scanf = Fixed_scanf
  module Spacetime = Blocked
  module StdLabels = Fixed_stdLabels
  module String = Fixed_string
  module StringLabels = Fixed_stringLabels
  module Sys = Blocked
  module Uchar = Fixed_uchar
end

include Fixed_stdlib
module CamlinternalLazy = Blocked
module CamlinternalMod = Blocked
module CamlinternalOO = Blocked
module Dynlink = Blocked
module Profiling = Blocked
module Raw_spacetime_lib = Blocked
module Stdlib = Fixed_stdlib
module Topdirs = Blocked
module Unix = Blocked
module UnixLabels = Blocked
module Stdlib__arg = Fixed_arg
module Stdlib__array = Fixed_array
module Stdlib__arrayLabels = Fixed_arrayLabels
module Stdlib__bigarray = Blocked
module Stdlib__bytes = Fixed_bytes
module Stdlib__bytesLabels = Fixed_bytesLabels
module Stdlib__char = Fixed_char
module Stdlib__filename = Fixed_filename
module Stdlib__float = Fixed_float
module Stdlib__marshal = Blocked
module Stdlib__obj = Blocked
module Stdlib__pervasives = Blocked
module Stdlib__printexc = Blocked
module Stdlib__scanf = Fixed_scanf
module Stdlib__spacetime = Blocked
module Stdlib__stdLabels = Fixed_stdLabels
module Stdlib__string = Fixed_string
module Stdlib__stringLabels = Fixed_stringLabels
module Stdlib__sys = Blocked
module Stdlib__uchar = Fixed_uchar
