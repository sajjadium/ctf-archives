#!/usr/bin/env python3
import numpy as np
class T:
 npz=np.load("tz.npz")
 c_c=npz["compute_check"]
 c_c.flags.writeable=False
 c_h=npz["compute_hash"]
 c_h.flags.writeable=False
 f_c=npz["flag_check"]
 f_c.flags.writeable=False
 f_h=npz["flag_hash"]
 f_h.flags.writeable=False
 r_c=npz["reg_check"]
 r_c.flags.writeable=False
 r_h=npz["reg_hash"]
 r_h.flags.writeable=False
 masks=npz["masks"]
 masks.flags.writeable=False
 r_s=npz["reg_scrable"]
 r_s.flags.writeable=False
# Created by pyminifier (https://github.com/liftoff/pyminifier)
