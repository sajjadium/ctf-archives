return (function()
  local CRYPTEDlIIIIlIl = "Here we go!"
  local CRYPTEDlIIlIllI = function(a)
    local b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    a = string.gsub(a, "[^" .. b .. "=]", "")
    return a:gsub(".", function(c)
      if c == "=" then
        return ""
      end
      local d, e = "", b:find(c) - 1
      for f = 6, 1, -1 do
        d = d .. (e % 2 ^ f - e % 2 ^ (f - 1) > 0 and "1" or "0")
      end
      return d
    end):gsub("%d%d%d?%d?%d?%d?%d?%d?", function(c)
      if #c ~= 8 then
        return ""
      end
      local g = 0
      for f = 1, 8 do
        g = g + (c:sub(f, f) == "1" and 2 ^ (8 - f) or 0)
      end
      return string.char(g)
    end)
  end
  local CRYPTEDlIIlllIl = 290
  local CRYPTEDlIIlIlIl = (function()
    local function a(b)
      local c = {}
      for d = 0, 255 do
        c[d] = {}
      end
      c[0][0] = b[1] * 255
      local e = 1
      for f = 0, 7 do
        for d = 0, e - 1 do
          for g = 0, e - 1 do
            local h = c[d][g] - b[1] * e
            c[d][g + e] = h + b[2] * e
            c[d + e][g] = h + b[3] * e
            c[d + e][g + e] = h + b[4] * e
          end
        end
        e = e * 2
      end
      return c
    end
    local i = a({ 0, 1, 1, 0 })
    local function j(self, k)
      local l, d, g = self.S, self.i, self.j
      local m = {}
      local n = string.char
      for o = 1, k do
        d = (d + 1) % 256
        g = (g + l[d]) % 256
        l[d], l[g] = l[g], l[d]
        m[o] = n(l[(l[d] + l[g]) % 256])
      end
      self.i, self.j = d, g
      return table.concat(m)
    end
    local function p(self, q)
      local r = j(self, #q)
      local s = {}
      local t = string.byte
      local n = string.char
      for d = 1, #q do
        s[d] = n(i[t(q, d)][t(r, d)])
      end
      return table.concat(s)
    end
    local function u(self, v)
      local l = self.S
      local g, w = 0, #v
      local t = string.byte
      for d = 0, 255 do
        g = (g + l[d] + t(v, d % w + 1)) % 256
        l[d], l[g] = l[g], l[d]
      end
    end
    function new(v)
      local l = {}
      local s = { S = l, i = 0, j = 0, generate = j, cipher = p, schedule = u }
      for d = 0, 255 do
        l[d] = d
      end
      if v then
        s:schedule(v)
      end
      return s
    end
    return new
  end)()
  local fev = getfenv or function()
    return _ENV
  end
  local CRYPTEDlIIlIlII = (function()
    if not bit then
      local bit_ = nil
      pcall(function()
        bit_ = require("bit")
      end)
      bit = bit_
    end
    local bit = bit
      or bit32
      or (function()
        local a = { _TYPE = "module", _NAME = "bit.numberlua", _VERSION = "0.3.1.20120131" }
        local b = math.floor
        local c = 2 ^ 32
        local d = c - 1
        local function e(f)
          local g = {}
          local h = setmetatable({}, g)
          function g:__index(i)
            local j = f(i)
            h[i] = j
            return j
          end
          return h
        end
        local function k(h, l)
          local function m(n, o)
            local p, q = 0, 1
            while n ~= 0 and o ~= 0 do
              local r, s = n % l, o % l
              p = p + h[r][s] * q
              n = (n - r) / l
              o = (o - s) / l
              q = q * l
            end
            p = p + (n + o) * q
            return p
          end
          return m
        end
        local function t(h)
          local u = k(h, 2 ^ 1)
          local v = e(function(n)
            return e(function(o)
              return u(n, o)
            end)
          end)
          return k(v, 2 ^ (h.n or 1))
        end
        function a.tobit(w)
          return w % 2 ^ 32
        end
        a.bxor = t({ [0] = { [0] = 0, [1] = 1 }, [1] = { [0] = 1, [1] = 0 }, n = 4 })
        local x = a.bxor
        function a.bnot(n)
          return d - n
        end
        local y = a.bnot
        function a.band(n, o)
          return (n + o - x(n, o)) / 2
        end
        local z = a.band
        function a.bor(n, o)
          return d - z(d - n, d - o)
        end
        local A = a.bor
        local B, C
        function a.rshift(n, D)
          if D < 0 then
            return B(n, -D)
          end
          return b(n % 2 ^ 32 / 2 ^ D)
        end
        C = a.rshift
        function a.lshift(n, D)
          if D < 0 then
            return C(n, -D)
          end
          return n * 2 ^ D % 2 ^ 32
        end
        B = a.lshift
        function a.tohex(w, E)
          E = E or 8
          local F
          if E <= 0 then
            if E == 0 then
              return ""
            end
            F = true
            E = -E
          end
          w = z(w, 16 ^ E - 1)
          return ("%0" .. E .. (F and "X" or "x")):format(w)
        end
        local G = a.tohex
        function a.extract(E, H, I)
          I = I or 1
          return z(C(E, H), 2 ^ I - 1)
        end
        local J = a.extract
        function a.replace(E, j, H, I)
          I = I or 1
          local K = 2 ^ I - 1
          j = z(j, K)
          local L = y(B(K, H))
          return z(E, L) + B(j, H)
        end
        local M = a.replace
        function a.bswap(w)
          local n = z(w, 0xff)
          w = C(w, 8)
          local o = z(w, 0xff)
          w = C(w, 8)
          local N = z(w, 0xff)
          w = C(w, 8)
          local O = z(w, 0xff)
          return B(B(B(n, 8) + o, 8) + N, 8) + O
        end
        local P = a.bswap
        function a.rrotate(w, D)
          D = D % 32
          local Q = z(w, 2 ^ D - 1)
          return C(w, D) + B(Q, 32 - D)
        end
        local R = a.rrotate
        function a.lrotate(w, D)
          return R(w, -D)
        end
        local S = a.lrotate
        a.rol = a.lrotate
        a.ror = a.rrotate
        function a.arshift(w, D)
          local T = C(w, D)
          if w >= 0x80000000 then
            T = T + B(2 ^ D - 1, 32 - D)
          end
          return T
        end
        local U = a.arshift
        function a.btest(w, V)
          return z(w, V) ~= 0
        end
        a.bit32 = {}
        local function W(w)
          return (-1 - w) % c
        end
        a.bit32.bnot = W
        local function X(n, o, N, ...)
          local T
          if o then
            n = n % c
            o = o % c
            T = x(n, o)
            if N then
              T = X(T, N, ...)
            end
            return T
          elseif n then
            return n % c
          else
            return 0
          end
        end
        a.bit32.bxor = X
        local function Y(n, o, N, ...)
          local T
          if o then
            n = n % c
            o = o % c
            T = (n + o - x(n, o)) / 2
            if N then
              T = Y(T, N, ...)
            end
            return T
          elseif n then
            return n % c
          else
            return d
          end
        end
        a.bit32.band = Y
        local function Z(n, o, N, ...)
          local T
          if o then
            n = n % c
            o = o % c
            T = d - z(d - n, d - o)
            if N then
              T = Z(T, N, ...)
            end
            return T
          elseif n then
            return n % c
          else
            return 0
          end
        end
        a.bit32.bor = Z
        function a.bit32.btest(...)
          return Y(...) ~= 0
        end
        function a.bit32.lrotate(w, D)
          return S(w % c, D)
        end
        function a.bit32.rrotate(w, D)
          return R(w % c, D)
        end
        function a.bit32.lshift(w, D)
          if D > 31 or D < -31 then
            return 0
          end
          return B(w % c, D)
        end
        function a.bit32.rshift(w, D)
          if D > 31 or D < -31 then
            return 0
          end
          return C(w % c, D)
        end
        function a.bit32.arshift(w, D)
          w = w % c
          if D >= 0 then
            if D > 31 then
              return w >= 0x80000000 and d or 0
            else
              local T = C(w, D)
              if w >= 0x80000000 then
                T = T + B(2 ^ D - 1, 32 - D)
              end
              return T
            end
          else
            return B(w, -D)
          end
        end
        function a.bit32.extract(w, H, ...)
          local I = ... or 1
          if H < 0 or H > 31 or I < 0 or H + I > 32 then
            error("out of range")
          end
          w = w % c
          return J(w, H, ...)
        end
        function a.bit32.replace(w, j, H, ...)
          local I = ... or 1
          if H < 0 or H > 31 or I < 0 or H + I > 32 then
            error("out of range")
          end
          w = w % c
          j = j % c
          return M(w, j, H, ...)
        end
        a.bit = {}
        function a.bit.tobit(w)
          w = w % c
          if w >= 0x80000000 then
            w = w - c
          end
          return w
        end
        local _ = a.bit.tobit
        function a.bit.tohex(w, ...)
          return G(w % c, ...)
        end
        function a.bit.bnot(w)
          return _(y(w % c))
        end
        local function a0(n, o, N, ...)
          if N then
            return a0(a0(n, o), N, ...)
          elseif o then
            return _(A(n % c, o % c))
          else
            return _(n)
          end
        end
        a.bit.bor = a0
        local function a1(n, o, N, ...)
          if N then
            return a1(a1(n, o), N, ...)
          elseif o then
            return _(z(n % c, o % c))
          else
            return _(n)
          end
        end
        a.bit.band = a1
        local function a2(n, o, N, ...)
          if N then
            return a2(a2(n, o), N, ...)
          elseif o then
            return _(x(n % c, o % c))
          else
            return _(n)
          end
        end
        a.bit.bxor = a2
        function a.bit.lshift(w, E)
          return _(B(w % c, E % 32))
        end
        function a.bit.rshift(w, E)
          return _(C(w % c, E % 32))
        end
        function a.bit.arshift(w, E)
          return _(U(w % c, E % 32))
        end
        function a.bit.rol(w, E)
          return _(S(w % c, E % 32))
        end
        function a.bit.ror(w, E)
          return _(R(w % c, E % 32))
        end
        function a.bit.bswap(w)
          return _(P(w % c))
        end
        return a
      end)()
    local unpack = table.unpack or unpack
    local a3
    local a4
    local a5
    local a6 = 50
    local a7 = {
      [22] = 18,
      [31] = 8,
      [33] = 28,
      [0] = 3,
      [1] = 13,
      [2] = 23,
      [26] = 33,
      [12] = 1,
      [13] = 6,
      [14] = 10,
      [15] = 16,
      [16] = 20,
      [17] = 26,
      [18] = 30,
      [19] = 36,
      [3] = 0,
      [4] = 2,
      [5] = 4,
      [6] = 7,
      [7] = 9,
      [8] = 12,
      [9] = 14,
      [10] = 17,
      [20] = 19,
      [21] = 22,
      [23] = 24,
      [24] = 27,
      [25] = 29,
      [27] = 32,
      [32] = 34,
      [34] = 37,
      [11] = 5,
      [28] = 11,
      [29] = 15,
      [30] = 21,
      [35] = 25,
      [36] = 31,
      [37] = 35,
    }
    local a8 = {
      [0] = "ABC",
      "ABx",
      "ABC",
      "ABC",
      "ABC",
      "ABx",
      "ABC",
      "ABx",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "AsBx",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "ABC",
      "AsBx",
      "AsBx",
      "ABC",
      "ABC",
      "ABC",
      "ABx",
      "ABC",
    }
    local a9 = {
      [0] = { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgK", c = "OpArgN" },
      { b = "OpArgU", c = "OpArgU" },
      { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgU", c = "OpArgN" },
      { b = "OpArgK", c = "OpArgN" },
      { b = "OpArgR", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgN" },
      { b = "OpArgU", c = "OpArgN" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgU", c = "OpArgU" },
      { b = "OpArgR", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgR", c = "OpArgR" },
      { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgK", c = "OpArgK" },
      { b = "OpArgR", c = "OpArgU" },
      { b = "OpArgR", c = "OpArgU" },
      { b = "OpArgU", c = "OpArgU" },
      { b = "OpArgU", c = "OpArgU" },
      { b = "OpArgU", c = "OpArgN" },
      { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgR", c = "OpArgN" },
      { b = "OpArgN", c = "OpArgU" },
      { b = "OpArgU", c = "OpArgU" },
      { b = "OpArgN", c = "OpArgN" },
      { b = "OpArgU", c = "OpArgN" },
      { b = "OpArgU", c = "OpArgN" },
    }
    local function aa(ab, s, e, d)
      local ac = 0
      for i = s, e, d do
        ac = ac + string.byte(ab, i, i) * 256 ^ (i - s)
      end
      return ac
    end
    local function ad(ae, af, ag, ah)
      local ai = (-1) ^ bit.rshift(ah, 7)
      local aj = bit.rshift(ag, 7) + bit.lshift(bit.band(ah, 0x7F), 1)
      local ak = ae + bit.lshift(af, 8) + bit.lshift(bit.band(ag, 0x7F), 16)
      local al = 1
      if aj == 0 then
        if ak == 0 then
          return ai * 0
        else
          al = 0
          aj = 1
        end
      elseif aj == 0x7F then
        if ak == 0 then
          return ai * 1 / 0
        else
          return ai * 0 / 0
        end
      end
      return ai * 2 ^ (aj - 127) * (1 + al / 2 ^ 23)
    end
    local function am(ae, af, ag, ah, an, ao, ap, aq)
      local ai = (-1) ^ bit.rshift(aq, 7)
      local aj = bit.lshift(bit.band(aq, 0x7F), 4) + bit.rshift(ap, 4)
      local ak = bit.band(ap, 0x0F) * 2 ^ 48
      local al = 1
      ak = ak + ao * 2 ^ 40 + an * 2 ^ 32 + ah * 2 ^ 24 + ag * 2 ^ 16 + af * 2 ^ 8 + ae
      if aj == 0 then
        if ak == 0 then
          return ai * 0
        else
          al = 0
          aj = 1
        end
      elseif aj == 0x7FF then
        if ak == 0 then
          return ai * 1 / 0
        else
          return ai * 0 / 0
        end
      end
      return ai * 2 ^ (aj - 1023) * (al + ak / 2 ^ 52)
    end
    local function ar(ab, s, e)
      return aa(ab, s, e - 1, 1)
    end
    local function as(ab, s, e)
      return aa(ab, e - 1, s, -1)
    end
    local function at(ab, s)
      return ad(string.byte(ab, s, s + 3))
    end
    local function au(ab, s)
      local ae, af, ag, ah = string.byte(ab, s, s + 3)
      return ad(ah, ag, af, ae)
    end
    local function av(ab, s)
      return am(string.byte(ab, s, s + 7))
    end
    local function aw(ab, s)
      local ae, af, ag, ah, an, ao, ap, aq = string.byte(ab, s, s + 7)
      return am(aq, ap, ao, an, ah, ag, af, ae)
    end
    local ax = { [4] = { little = at, big = au }, [8] = { little = av, big = aw } }
    local function ay(S)
      local az = S.index
      local aA = string.byte(S.source, az, az)
      S.index = az + 1
      return aA
    end
    local function aB(S, aC)
      local aD = S.index + aC
      local aE = string.sub(S.source, S.index, aD - 1)
      S.index = aD
      return aE
    end
    local function aF(S)
      local aC = S:s_szt()
      local aE
      if aC ~= 0 then
        aE = string.sub(aB(S, aC), 1, -2)
      end
      return aE
    end
    local function aG(aC, aH)
      return function(S)
        local aD = S.index + aC
        local aI = aH(S.source, S.index, aD)
        S.index = aD
        return aI
      end
    end
    local function aJ(aC, aH)
      return function(S)
        local aK = aH(S.source, S.index)
        S.index = S.index + aC
        return aK
      end
    end
    local function aL(S)
      local aM = S:s_int()
      local aN = {}
      for i = 1, aM do
        local aO = S:s_ins()
        local aP = bit.band(aO, 0x3F)
        local aQ = a8[aP]
        local aR = a9[aP]
        local aS = { value = aO, op = a7[aP], A = bit.band(bit.rshift(aO, 6), 0xFF) }
        if aQ == "ABC" then
          aS.B = bit.band(bit.rshift(aO, 23), 0x1FF)
          aS.C = bit.band(bit.rshift(aO, 14), 0x1FF)
          aS.is_KB = aR.b == "OpArgK" and aS.B > 0xFF
          aS.is_KC = aR.c == "OpArgK" and aS.C > 0xFF
        elseif aQ == "ABx" then
          aS.Bx = bit.band(bit.rshift(aO, 14), 0x3FFFF)
          aS.is_K = aR.b == "OpArgK"
        elseif aQ == "AsBx" then
          aS.sBx = bit.band(bit.rshift(aO, 14), 0x3FFFF) - 131071
        end
        aN[i] = aS
      end
      return aN
    end
    local function aT(S)
      local aM = S:s_int()
      local aU = {}
      for i = 1, aM do
        local aV = ay(S)
        local k
        if aV == 1 then
          k = ay(S) ~= 0
        elseif aV == 3 then
          k = S:s_num()
        elseif aV == 4 then
          k = aF(S)
        end
        aU[i] = k
      end
      return aU
    end
    local function aW(S, ab)
      local aM = S:s_int()
      local aX = {}
      for i = 1, aM do
        aX[i] = a5(S, ab)
      end
      return aX
    end
    local function aY(S)
      local aM = S:s_int()
      local aZ = {}
      for i = 1, aM do
        aZ[i] = S:s_int()
      end
      return aZ
    end
    local function a_(S)
      local aM = S:s_int()
      local b0 = {}
      for i = 1, aM do
        b0[i] = { varname = aF(S), startpc = S:s_int(), endpc = S:s_int() }
      end
      return b0
    end
    local function b1(S)
      local aM = S:s_int()
      local b2 = {}
      for i = 1, aM do
        b2[i] = aF(S)
      end
      return b2
    end
    function a5(S, b3)
      local b4 = {}
      local ab = aF(S) or b3
      b4.source = ab
      S:s_int()
      S:s_int()
      b4.numupvals = ay(S)
      b4.numparams = ay(S)
      ay(S)
      ay(S)
      b4.code = aL(S)
      b4.const = aT(S)
      b4.subs = aW(S, ab)
      b4.lines = aY(S)
      a_(S)
      b1(S)
      for _, v in ipairs(b4.code) do
        if v.is_K then
          v.const = b4.const[v.Bx + 1]
        else
          if v.is_KB then
            v.const_B = b4.const[v.B - 0xFF]
          end
          if v.is_KC then
            v.const_C = b4.const[v.C - 0xFF]
          end
        end
      end
      return b4
    end
    function a3(ab)
      local b5
      local b6
      local b7
      local b8
      local b9
      local ba
      local bb
      local bc = { index = 1, source = ab }
      assert(aB(bc, 4) == "\27Lua", "invalid Lua signature")
      assert(ay(bc) == 0x51, "invalid Lua version")
      assert(ay(bc) == 0, "invalid Lua format")
      b6 = ay(bc) ~= 0
      b7 = ay(bc)
      b8 = ay(bc)
      b9 = ay(bc)
      ba = ay(bc)
      bb = ay(bc) ~= 0
      b5 = b6 and ar or as
      bc.s_int = aG(b7, b5)
      bc.s_szt = aG(b8, b5)
      bc.s_ins = aG(b9, b5)
      if bb then
        bc.s_num = aG(ba, b5)
      elseif ax[ba] then
        bc.s_num = aJ(ba, ax[ba][b6 and "little" or "big"])
      else
        error("unsupported float size")
      end
      return a5(bc, "@virtual")
    end
    local function bd(be, bf)
      for i, bg in pairs(be) do
        if bg.index >= bf then
          bg.value = bg.store[bg.index]
          bg.store = bg
          bg.index = "value"
          be[i] = nil
        end
      end
    end
    local function bh(be, bf, bi)
      local bj = be[bf]
      if not bj then
        bj = { index = bf, store = bi }
        be[bf] = bj
      end
      return bj
    end
    local function bk(...)
      return select("#", ...), { ... }
    end
    local function bl(bm, bn)
      local ab = bm.source
      local bo = bm.lines[bm.pc - 1]
      local b3, bp, bq = string.match(bn, "^(.-):(%d+):%s+(.+)")
      local br = "%s:%i: [%s:%i] %s"
      bo = bo or "0"
      b3 = b3 or "?"
      bp = bp or "0"
      bq = bq or bn
      error(string.format(br, ab, bo, b3, bp, bq), 0)
    end
    local function bs(bm)
      local aN = bm.code
      local bt = bm.subs
      local bu = bm.env
      local bv = bm.upvals
      local bw = bm.varargs
      local bx = -1
      local by = {}
      local bi = bm.stack
      local bz = bm.pc
      while true do
        local bA = aN[bz]
        local aP = bA.op
        bz = bz + 1
        if aP < 18 then
          if aP < 8 then
            if aP < 3 then
              if aP < 1 then
                for i = bA.A, bA.B do
                  bi[i] = nil
                end
              elseif aP > 1 then
                local bg = bv[bA.B]
                bi[bA.A] = bg.store[bg.index]
              else
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                bi[bA.A] = bB + bC
              end
            elseif aP > 3 then
              if aP < 6 then
                if aP > 4 then
                  local A = bA.A
                  local B = bA.B
                  local bf
                  if bA.is_KC then
                    bf = bA.const_C
                  else
                    bf = bi[bA.C]
                  end
                  bi[A + 1] = bi[B]
                  bi[A] = bi[B][bf]
                else
                  bi[bA.A] = bu[bA.const]
                end
              elseif aP > 6 then
                local bf
                if bA.is_KC then
                  bf = bA.const_C
                else
                  bf = bi[bA.C]
                end
                bi[bA.A] = bi[bA.B][bf]
              else
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                bi[bA.A] = bB - bC
              end
            else
              bi[bA.A] = bi[bA.B]
            end
          elseif aP > 8 then
            if aP < 13 then
              if aP < 10 then
                bu[bA.const] = bi[bA.A]
              elseif aP > 10 then
                if aP < 12 then
                  local A = bA.A
                  local B = bA.B
                  local C = bA.C
                  local bD
                  local bE, bF
                  if B == 0 then
                    bD = bx - A
                  else
                    bD = B - 1
                  end
                  bE, bF = bk(bi[A](unpack(bi, A + 1, A + bD)))
                  if C == 0 then
                    bx = A + bE - 1
                  else
                    bE = C - 1
                  end
                  for i = 1, bE do
                    bi[A + i - 1] = bF[i]
                  end
                else
                  local bg = bv[bA.B]
                  bg.store[bg.index] = bi[bA.A]
                end
              else
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                bi[bA.A] = bB * bC
              end
            elseif aP > 13 then
              if aP < 16 then
                if aP > 14 then
                  local A = bA.A
                  local B = bA.B
                  local bD
                  if B == 0 then
                    bD = bx - A
                  else
                    bD = B - 1
                  end
                  bd(by, 0)
                  return bk(bi[A](unpack(bi, A + 1, A + bD)))
                else
                  local bf, bG
                  if bA.is_KB then
                    bf = bA.const_B
                  else
                    bf = bi[bA.B]
                  end
                  if bA.is_KC then
                    bG = bA.const_C
                  else
                    bG = bi[bA.C]
                  end
                  bi[bA.A][bf] = bG
                end
              elseif aP > 16 then
                bi[bA.A] = {}
              else
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                bi[bA.A] = bB / bC
              end
            else
              bi[bA.A] = bA.const
            end
          else
            local A = bA.A
            local bH = bi[A + 2]
            local bf = bi[A] + bH
            local bI = bi[A + 1]
            local bJ
            if bH == math.abs(bH) then
              bJ = bf <= bI
            else
              bJ = bf >= bI
            end
            if bJ then
              bi[bA.A] = bf
              bi[bA.A + 3] = bf
              bz = bz + bA.sBx
            end
          end
        elseif aP > 18 then
          if aP < 28 then
            if aP < 23 then
              if aP < 20 then
                bi[bA.A] = #bi[bA.B]
              elseif aP > 20 then
                if aP < 22 then
                  local A = bA.A
                  local B = bA.B
                  local bK = {}
                  local aM
                  if B == 0 then
                    aM = bx - A + 1
                  else
                    aM = B - 1
                  end
                  for i = 1, aM do
                    bK[i] = bi[A + i - 1]
                  end
                  bd(by, 0)
                  return aM, bK
                else
                  local aE = bi[bA.B]
                  for i = bA.B + 1, bA.C do
                    aE = aE .. bi[i]
                  end
                  bi[bA.A] = aE
                end
              else
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                bi[bA.A] = bB % bC
              end
            elseif aP > 23 then
              if aP < 26 then
                if aP > 24 then
                  bd(by, bA.A)
                else
                  local bB, bC
                  if bA.is_KB then
                    bB = bA.const_B
                  else
                    bB = bi[bA.B]
                  end
                  if bA.is_KC then
                    bC = bA.const_C
                  else
                    bC = bi[bA.C]
                  end
                  if bB == bC == (bA.A ~= 0) then
                    bz = bz + aN[bz].sBx
                  end
                  bz = bz + 1
                end
              elseif aP > 26 then
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                if bB < bC == (bA.A ~= 0) then
                  bz = bz + aN[bz].sBx
                end
                bz = bz + 1
              else
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                bi[bA.A] = bB ^ bC
              end
            else
              bi[bA.A] = bA.B ~= 0
              if bA.C ~= 0 then
                bz = bz + 1
              end
            end
          elseif aP > 28 then
            if aP < 33 then
              if aP < 30 then
                local bB, bC
                if bA.is_KB then
                  bB = bA.const_B
                else
                  bB = bi[bA.B]
                end
                if bA.is_KC then
                  bC = bA.const_C
                else
                  bC = bi[bA.C]
                end
                if bB <= bC == (bA.A ~= 0) then
                  bz = bz + aN[bz].sBx
                end
                bz = bz + 1
              elseif aP > 30 then
                if aP < 32 then
                  local aX = bt[bA.Bx + 1]
                  local bL = aX.numupvals
                  local bM
                  if bL ~= 0 then
                    bM = {}
                    for i = 1, bL do
                      local bN = aN[bz + i - 1]
                      if bN.op == a7[0] then
                        bM[i - 1] = bh(by, bN.B, bi)
                      elseif bN.op == a7[4] then
                        bM[i - 1] = bv[bN.B]
                      end
                    end
                    bz = bz + bL
                  end
                  bi[bA.A] = a4(aX, bu, bM)
                else
                  local A = bA.A
                  local B = bA.B
                  if not bi[B] == (bA.C ~= 0) then
                    bz = bz + 1
                  else
                    bi[A] = bi[B]
                  end
                end
              else
                bi[bA.A] = -bi[bA.B]
              end
            elseif aP > 33 then
              if aP < 36 then
                if aP > 34 then
                  local A = bA.A
                  local aM = bA.B
                  if aM == 0 then
                    aM = bw.size
                    bx = A + aM - 1
                  end
                  for i = 1, aM do
                    bi[A + i - 1] = bw.list[i]
                  end
                else
                  local A = bA.A
                  local bO, bI, bH
                  bO = assert(tonumber(bi[A]), "`for` initial value must be a number")
                  bI = assert(tonumber(bi[A + 1]), "`for` limit must be a number")
                  bH = assert(tonumber(bi[A + 2]), "`for` step must be a number")
                  bi[A] = bO - bH
                  bi[A + 1] = bI
                  bi[A + 2] = bH
                  bz = bz + bA.sBx
                end
              elseif aP > 36 then
                local A = bA.A
                local C = bA.C
                local aM = bA.B
                local bP = bi[A]
                local bQ
                if aM == 0 then
                  aM = bx - A
                end
                if C == 0 then
                  C = bA[bz].value
                  bz = bz + 1
                end
                bQ = (C - 1) * a6
                for i = 1, aM do
                  bP[i + bQ] = bi[A + i]
                end
              else
                bi[bA.A] = not bi[bA.B]
              end
            else
              if not bi[bA.A] == (bA.C ~= 0) then
                bz = bz + 1
              end
            end
          else
            local A = bA.A
            local aH = bi[A]
            local bR = bi[A + 1]
            local bf = bi[A + 2]
            local bS = A + 3
            local bK
            bi[bS + 2] = bf
            bi[bS + 1] = bR
            bi[bS] = aH
            bK = { aH(bR, bf) }
            for i = 1, bA.C do
              bi[bS + i - 1] = bK[i]
            end
            if bi[bS] ~= nil then
              bi[A + 2] = bi[bS]
            else
              bz = bz + 1
            end
          end
        else
          bz = bz + bA.sBx
        end
        bm.pc = bz
      end
    end
    function a4(bR, bu, b2)
      local bT = bR.code
      local bU = bR.subs
      local bV = bR.lines
      local bW = bR.source
      local bX = bR.numparams
      local function bY(...)
        local bi = {}
        local bZ = {}
        local b_ = 0
        local c0, c1 = bk(...)
        local bm
        local c2, bn, bK
        for i = 1, bX do
          bi[i - 1] = c1[i]
        end
        if bX < c0 then
          b_ = c0 - bX
          for i = 1, b_ do
            bZ[i] = c1[bX + i]
          end
        end
        bm =
          { varargs = { list = bZ, size = b_ }, code = bT, subs = bU, lines = bV, source = bW, env = bu, upvals = b2, stack = bi, pc = 1 }
        c2, bn, bK = pcall(bs, bm, ...)
        if c2 then
          return unpack(bK, 1, bn)
        else
          bl(bm, bn)
        end
        return
      end
      return bY
    end
    return function(c3, bu)
      return a4(a3(c3), bu or fev(0))
    end
  end)()
  local CRYPTEDlIIllIIl = "Lua is a best programming language in the world."
  local CRYPTEDlIIlIIIl =
    "\104\78\90\56\110\71\120\101\74\113\78\48\106\80\111\57\112\54\118\86\47\74\73\121\106\115\55\72\101\88\47\51\102\72\66\71\99\65\116\102\106\79\54\98\55\80\104\87\104\66\101\118\66\72\70\85\109\112\110\80\108\86\87\104\101\54\86\87\106\88\48\120\99\109\106\120\71\104\83\108\108\47\115\66\89\76\51\110\102\82\120\106\86\88\68\120\120\57\71\80\48\102\75\120\113\109\88\121\122\57\75\67\55\71\121\52\99\70\84\100\55\74\84\52\77\52\48\51\55\82\116\72\122\113\67\77\122\79\68\88\66\79\112\102\78\121\119\68\109\121\80\105\51\112\48\74\51\104\99\105\70\118\67\71\51\75\98\85\117\120\68\100\81\43\97\117\115\67\109\121\65\49\82\122\121\108\50\114\70\101\111\77\112\43\106\97\98\90\109\50\69\43\117\68\89\104\53\51\55\104\56\78\76\112\99\70\110\76\89\87\115\109\75\99\119\90\74\101\77\74\111\47\108\97\75\67\118\56\101\43\81\52\69\120\78\70\119\122\88\88\111\108\121\89\57\68\104\97\73\55\107\51\51\97\114\86\65\49\52\114\70\70\86\57\57\89\121\86\120\49\53\105\108\97\97\100\103\53\69\65\57\87\90\114\69\101\119\82\73\109\99\120\115\78\67\71\53\73\72\112\52\88\115\66\49\52\110\55\103\65\120\47\114\121\115\48\67\57\78\51\67\79\122\119\99\52\49\47\119\66\65\115\78\74\49\71\103\117\88\51\83\102\111\48\53\103\115\111\86\79\56\47\114\100\88\80\78\56\122\82\77\80\71\107\115\105\122\89\115\57\114\110\108\71\110\107\114\79\51\79\117\83\86\103\71\73\83\87\54\51\90\79\97\121\80\76\55\82\67\79\87\52\47\111\57\116\116\78\111\43\47\73\73\121\73\100\53\76\108\71\88\100\122\51\114\70\121\105\84\66\79\52\118\103\49\107\85\72\116\56\98\100\88\56\109\111\101\122\47\107\113\72\54\120\109\109\117\112\98\52\121\114\52\90\110\49\106\74\66\75\113\76\116\118\69\86\75\71\99\99\122\73\106\48\81\90\86\83\89\77\103\72\98\112\112\47\87\99\99\57\84\112\106\115\51\86\51\85\55\71\115\85\71\70\88\73\70\55\69\99\109\105\119\65\51\57\119\120\54\107\51\98\72\70\86\116\52\122\67\57\111\84\78\69\65\54\66\89\100\121\87\51\84\84\70\43\105\74\99\98\53\54\47\66\90\83\49\86\114\121\78\65\99\102\114\107\74\110\112\55\85\73\66\71\50\53\106\55\122\73\105\114\110\52\117\115\72\47\117\83\50\106\78\105\50\113\65\43\111\75\52\57\88\54\103\112\114\117\51\120\87\52\121\104\112\120\57\76\49\72\109\73\110\111\115\65\88\53\79\98\121\81\75\116\80\88\90\113\115\77\82\111\67\115\72\43\113\70\78\43\112\56\90\43\108\43\50\108\120\90\89\121\115\74\111\120\47\73\90\70\55\84\74\116\69\67\49\117\111\115\88\104\71\68\56\69\115\98\101\74\79\65\119\102\76\68\108\90\77\88\112\119\83\101\87\67\116\79\106\107\56\98\115\77\73\75\86\77\88\65\65\79\118\50\89\83\68\115\54\53\71\51\73\65\71\111\104\102\104\72\116\122\104\66\118\81\71\50\79\76\80\106\66\110\78\77\43\105\52\68\97\68\110\55\115\65\57\100\50\65\116\53\101\113\67\119\56\111\88\99\104\97\70\86\101\104\86\79\89\69\100\66\108\112\66\48\51\65\84\97\116\49\69\77\65\86\122\119\106\66\114\73\73\76\77\109\80\48\52\102\98\51\80\104\51\74\108\100\116\109\114\86\118\65\61\61"
  local CRYPTEDlIIllIll =
    "\97\121\107\116\88\49\78\108\75\108\112\53\99\106\86\111\100\106\111\114\78\107\66\79\77\119\61\61"
  local CRYPTEDlIIllIII = "NGI2d3Q8YSp3KmsvYWc9K0c6dw=="
  local CRYPTEDlIIlIIlI = function(a, b)
    local c = CRYPTEDlIIlIlIl(CRYPTEDlIIlIllI(a))
    local d = c["\99\105\112\104\101\114"](c, CRYPTEDlIIlIllI(b))
    return CRYPTEDlIIlIllI(d)
  end
  local CRYPTEDlIIllIll =
    "\97\121\107\116\88\49\78\108\75\108\112\53\99\106\86\111\100\106\111\114\78\107\66\79\77\119\61\61"
  local CRYPTEDlIIllIll =
    "\97\121\107\116\88\49\78\108\75\108\112\53\99\106\86\111\100\106\111\114\78\107\66\79\77\119\61\61"
  local CRYPTEDlIIlIIII = "OS5nRkJxRlY8XydZaSZ2OXdEb3t7I2EkNmcvbyxdZVYvZy86Mjg="
  function CRYPTEDlIIlIlll(a, b)
    local c = CRYPTEDlIIlIllI(a, b)
    local d = CRYPTEDlIIllIlI
    return c, d
  end
  return CRYPTEDlIIlIlII(CRYPTEDlIIlIIlI(CRYPTEDlIIllIll, CRYPTEDlIIlIIIl), getfenv(0))()
end)()
