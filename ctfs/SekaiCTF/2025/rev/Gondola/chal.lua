local rt = (function()
local module = {}

local bit = require("bit")
local ffi = require("ffi")

local u32 = ffi.typeof("uint32_t")
local u64 = ffi.typeof("uint64_t")
local i64 = ffi.typeof("int64_t")

local math_ceil = math.ceil
local math_floor = math.floor
local to_number = tonumber
local to_signed = bit.tobit

local NUM_ZERO = i64(0)
local NUM_ONE = i64(1)

local function truncate_f64(num)
	if num >= 0 then
		return (math_floor(num))
	else
		return (math_ceil(num))
	end
end

do
	local add = {}
	local sub = {}
	local mul = {}
	local div = {}
	local rem = {}
	local neg = {}
	local min = {}
	local max = {}
	local copysign = {}
	local nearest = {}

	local math_abs = math.abs
	local math_min = math.min
	local math_max = math.max

	local RE_INSTANCE = ffi.new([[union {
		double f64;
		struct { int32_t a32, b32; };
	}]])

	local function round(num)
		if num >= 0 then
			return (math_floor(num + 0.5))
		else
			return (math_ceil(num - 0.5))
		end
	end

	function add.i32(lhs, rhs)
		return (to_signed(lhs + rhs))
	end

	function sub.i32(lhs, rhs)
		return (to_signed(lhs - rhs))
	end

	function mul.i32(lhs, rhs)
		return (to_signed(NUM_ONE * lhs * rhs))
	end

	function div.i32(lhs, rhs)
		assert(rhs ~= 0, "division by zero")

		return (truncate_f64(lhs / rhs))
	end

	function div.u32(lhs, rhs)
		assert(rhs ~= 0, "division by zero")

		lhs = to_number(u32(lhs))
		rhs = to_number(u32(rhs))

		return (to_signed(math_floor(lhs / rhs)))
	end

	function rem.u32(lhs, rhs)
		assert(rhs ~= 0, "division by zero")

		lhs = to_number(u32(lhs))
		rhs = to_number(u32(rhs))

		return (to_signed(lhs % rhs))
	end

	function div.u64(lhs, rhs)
		assert(rhs ~= 0, "division by zero")

		return (i64(u64(lhs) / u64(rhs)))
	end

	function rem.u64(lhs, rhs)
		assert(rhs ~= 0, "division by zero")

		return (i64(u64(lhs) % u64(rhs)))
	end

	function neg.f32(num)
		return -num
	end

	function min.f32(lhs, rhs)
		if lhs ~= lhs then
			return lhs
		elseif rhs ~= rhs then
			return rhs
		else
			return (math_min(lhs, rhs))
		end
	end

	function max.f32(lhs, rhs)
		if lhs ~= lhs then
			return lhs
		elseif rhs ~= rhs then
			return rhs
		else
			return (math_max(lhs, rhs))
		end
	end

	function copysign.f32(lhs, rhs)
		RE_INSTANCE.f64 = rhs

		if RE_INSTANCE.b32 >= 0 then
			return (math_abs(lhs))
		else
			return -math_abs(lhs)
		end
	end

	function nearest.f32(num)
		local result = round(num)

		if (math_abs(num) + 0.5) % 2 == 1 then
			if result >= 0 then
				result = result - 1
			else
				result = result + 1
			end
		end

		return result
	end

	neg.f64 = neg.f32
	min.f64 = min.f32
	max.f64 = max.f32
	copysign.f64 = copysign.f32
	nearest.f64 = nearest.f32

	module.add = add
	module.sub = sub
	module.mul = mul
	module.div = div
	module.rem = rem
	module.min = min
	module.max = max
	module.neg = neg
	module.copysign = copysign
	module.nearest = nearest
end

do
	local clz = {}
	local ctz = {}
	local popcnt = {}

	local bit_and = bit.band
	local bit_lshift = bit.lshift
	local bit_rshift = bit.rshift

	function clz.i32(num)
		if num == 0 then
			return 32
		end

		local count = 0

		if bit_rshift(num, 16) == 0 then
			num = bit_lshift(num, 16)
			count = count + 16
		end

		if bit_rshift(num, 24) == 0 then
			num = bit_lshift(num, 8)
			count = count + 8
		end

		if bit_rshift(num, 28) == 0 then
			num = bit_lshift(num, 4)
			count = count + 4
		end

		if bit_rshift(num, 30) == 0 then
			num = bit_lshift(num, 2)
			count = count + 2
		end

		if bit_rshift(num, 31) == 0 then
			count = count + 1
		end

		return count
	end

	function ctz.i32(num)
		if num == 0 then
			return 32
		end

		local count = 0

		if bit_lshift(num, 16) == 0 then
			num = bit_rshift(num, 16)
			count = count + 16
		end

		if bit_lshift(num, 24) == 0 then
			num = bit_rshift(num, 8)
			count = count + 8
		end

		if bit_lshift(num, 28) == 0 then
			num = bit_rshift(num, 4)
			count = count + 4
		end

		if bit_lshift(num, 30) == 0 then
			num = bit_rshift(num, 2)
			count = count + 2
		end

		if bit_lshift(num, 31) == 0 then
			count = count + 1
		end

		return count
	end

	function popcnt.i32(num)
		local count = 0

		while num ~= 0 do
			num = bit_and(num, num - 1)
			count = count + 1
		end

		return count
	end

	function clz.i64(num)
		if num == 0 then
			return 64 * NUM_ONE
		end

		local count = NUM_ZERO

		if bit_rshift(num, 32) == NUM_ZERO then
			num = bit_lshift(num, 32)
			count = count + 32
		end

		if bit_rshift(num, 48) == NUM_ZERO then
			num = bit_lshift(num, 16)
			count = count + 16
		end

		if bit_rshift(num, 56) == NUM_ZERO then
			num = bit_lshift(num, 8)
			count = count + 8
		end

		if bit_rshift(num, 60) == NUM_ZERO then
			num = bit_lshift(num, 4)
			count = count + 4
		end

		if bit_rshift(num, 62) == NUM_ZERO then
			num = bit_lshift(num, 2)
			count = count + 2
		end

		if bit_rshift(num, 63) == NUM_ZERO then
			count = count + NUM_ONE
		end

		return count
	end

	function ctz.i64(num)
		if num == 0 then
			return 64 * NUM_ONE
		end

		local count = NUM_ZERO

		if bit_lshift(num, 32) == NUM_ZERO then
			num = bit_rshift(num, 32)
			count = count + 32
		end

		if bit_lshift(num, 48) == NUM_ZERO then
			num = bit_rshift(num, 16)
			count = count + 16
		end

		if bit_lshift(num, 56) == NUM_ZERO then
			num = bit_rshift(num, 8)
			count = count + 8
		end

		if bit_lshift(num, 60) == NUM_ZERO then
			num = bit_rshift(num, 4)
			count = count + 4
		end

		if bit_lshift(num, 62) == NUM_ZERO then
			num = bit_rshift(num, 2)
			count = count + 2
		end

		if bit_lshift(num, 63) == NUM_ZERO then
			count = count + NUM_ONE
		end

		return count
	end

	function popcnt.i64(num)
		local count = NUM_ZERO

		while num ~= NUM_ZERO do
			num = bit_and(num, num - NUM_ONE)
			count = count + NUM_ONE
		end

		return count
	end

	module.clz = clz
	module.ctz = ctz
	module.popcnt = popcnt
end

do
	local le = {}
	local lt = {}
	local ge = {}
	local gt = {}

	function le.u32(lhs, rhs)
		return u32(lhs) <= u32(rhs)
	end

	function lt.u32(lhs, rhs)
		return u32(lhs) < u32(rhs)
	end

	function ge.u32(lhs, rhs)
		return u32(lhs) >= u32(rhs)
	end

	function gt.u32(lhs, rhs)
		return u32(lhs) > u32(rhs)
	end

	function le.u64(lhs, rhs)
		return u64(lhs) <= u64(rhs)
	end

	function lt.u64(lhs, rhs)
		return u64(lhs) < u64(rhs)
	end

	function ge.u64(lhs, rhs)
		return u64(lhs) >= u64(rhs)
	end

	function gt.u64(lhs, rhs)
		return u64(lhs) > u64(rhs)
	end

	module.le = le
	module.lt = lt
	module.ge = ge
	module.gt = gt
end

do
	local wrap = {}
	local truncate = {}
	local saturate = {}
	local extend = {}
	local convert = {}
	local promote = {}
	local demote = {}
	local reinterpret = {}

	local bit_and = bit.band

	local NUM_MIN_I64 = bit.lshift(NUM_ONE, 63)
	local NUM_MAX_I64 = bit.bnot(NUM_MIN_I64)
	local NUM_MAX_U64 = bit.bnot(NUM_ZERO)

	local RE_INSTANCE = ffi.new([[union {
		int32_t i32;
		int64_t i64;
		float f32;
		double f64;
	}]])

	function wrap.i32_i64(num)
		RE_INSTANCE.i64 = num

		return RE_INSTANCE.i32
	end

	truncate.i32_f32 = truncate_f64
	truncate.i32_f64 = truncate_f64

	function truncate.u32_f32(num)
		return (to_signed(truncate_f64(num)))
	end

	truncate.u32_f64 = truncate.u32_f32

	truncate.i64_f32 = i64
	truncate.i64_f64 = i64
	truncate.u64_f32 = i64

	function truncate.u64_f64(num)
		return (i64(u64(num)))
	end

	truncate.f32 = truncate_f64
	truncate.f64 = truncate_f64

	function saturate.i32_f32(num)
		if num <= -0x80000000 then
			return -0x80000000
		elseif num >= 0x7FFFFFFF then
			return 0x7FFFFFFF
		else
			return to_signed(truncate_f64(num))
		end
	end

	saturate.i32_f64 = saturate.i32_f32

	function saturate.u32_f32(num)
		if num <= 0 then
			return 0
		elseif num >= 0xFFFFFFFF then
			return -1
		else
			return to_signed(truncate_f64(num))
		end
	end

	saturate.u32_f64 = saturate.u32_f32

	function saturate.i64_f32(num)
		if num >= 2 ^ 63 - 1 then
			return NUM_MAX_I64
		elseif num <= -2 ^ 63 then
			return NUM_MIN_I64
		elseif num ~= num then
			return NUM_ZERO
		else
			return i64(num)
		end
	end

	saturate.i64_f64 = saturate.i64_f32

	function saturate.u64_f32(num)
		if num >= 2 ^ 64 then
			return NUM_MAX_U64
		elseif num <= 0 or num ~= num then
			return NUM_ZERO
		else
			return i64(u64(num))
		end
	end

	saturate.u64_f64 = saturate.u64_f32

	function extend.i32_n8(num)
		num = bit_and(num, 0xFF)

		if num >= 0x80 then
			return num - 0x100
		else
			return num
		end
	end

	function extend.i32_n16(num)
		num = bit_and(num, 0xFFFF)

		if num >= 0x8000 then
			return num - 0x10000
		else
			return num
		end
	end

	function extend.i64_n8(num)
		num = bit_and(num, 0xFF * NUM_ONE)

		if num >= 0x80 then
			return num - 0x100
		else
			return num
		end
	end

	function extend.i64_n16(num)
		num = bit_and(num, 0xFFFF * NUM_ONE)

		if num >= 0x8000 then
			return num - 0x10000
		else
			return num
		end
	end

	function extend.i64_n32(num)
		num = bit_and(num, 0xFFFFFFFF * NUM_ONE)

		if num >= 0x80000000 then
			return num - 0x100000000
		else
			return num
		end
	end

	extend.i64_i32 = i64

	function extend.i64_u32(num)
		RE_INSTANCE.i64 = NUM_ZERO
		RE_INSTANCE.i32 = num

		return RE_INSTANCE.i64
	end

	function convert.f32_i32(num)
		return num
	end

	function convert.f32_u32(num)
		return (to_number(u32(num)))
	end

	function convert.f32_u64(num)
		return (to_number(u64(num)))
	end

	convert.f64_i32 = convert.f32_i32
	convert.f64_u32 = convert.f32_u32
	convert.f64_u64 = convert.f32_u64

	function demote.f32_f64(num)
		return num
	end

	promote.f64_f32 = demote.f32_f64

	function reinterpret.i32_f32(num)
		RE_INSTANCE.f32 = num

		return RE_INSTANCE.i32
	end

	function reinterpret.i64_f64(num)
		RE_INSTANCE.f64 = num

		return RE_INSTANCE.i64
	end

	function reinterpret.f32_i32(num)
		RE_INSTANCE.i32 = num

		return RE_INSTANCE.f32
	end

	function reinterpret.f64_i64(num)
		RE_INSTANCE.i64 = num

		return RE_INSTANCE.f64
	end

	module.wrap = wrap
	module.truncate = truncate
	module.saturate = saturate
	module.extend = extend
	module.convert = convert
	module.demote = demote
	module.promote = promote
	module.reinterpret = reinterpret
end

do
	local load = {}
	local store = {}
	local allocator = {}

	ffi.cdef([[
	union Any {
		int8_t i8;
		int16_t i16;
		int32_t i32;
		int64_t i64;

		uint8_t u8;
		uint16_t u16;
		uint32_t u32;
		uint64_t u64;

		float f32;
		double f64;
	};

	struct Memory {
		uint32_t min;
		uint32_t max;
		union Any *data;
	};

	void *calloc(size_t num, size_t size);
	void *realloc(void *ptr, size_t size);
	void free(void *ptr);
	]])

	local alias_t = ffi.typeof("uint8_t *")
	local any_t = ffi.typeof("union Any *")
	local cast = ffi.cast

	local function by_offset(pointer, offset)
		local aliased = cast(alias_t, pointer)

		return cast(any_t, aliased + offset)
	end

	function load.i32_i8(memory, addr)
		return by_offset(memory.data, addr).i8
	end

	function load.i32_u8(memory, addr)
		return by_offset(memory.data, addr).u8
	end

	function load.i32_i16(memory, addr)
		return by_offset(memory.data, addr).i16
	end

	function load.i32_u16(memory, addr)
		return by_offset(memory.data, addr).u16
	end

	function load.i32(memory, addr)
		return by_offset(memory.data, addr).i32
	end

	function load.i64_i8(memory, addr)
		return (i64(by_offset(memory.data, addr).i8))
	end

	function load.i64_u8(memory, addr)
		return (i64(by_offset(memory.data, addr).u8))
	end

	function load.i64_i16(memory, addr)
		return (i64(by_offset(memory.data, addr).i16))
	end

	function load.i64_u16(memory, addr)
		return (i64(by_offset(memory.data, addr).u16))
	end

	function load.i64_i32(memory, addr)
		return (i64(by_offset(memory.data, addr).i32))
	end

	function load.i64_u32(memory, addr)
		return (i64(by_offset(memory.data, addr).u32))
	end

	function load.i64(memory, addr)
		return by_offset(memory.data, addr).i64
	end

	function load.f32(memory, addr)
		return by_offset(memory.data, addr).f32
	end

	function load.f64(memory, addr)
		return by_offset(memory.data, addr).f64
	end

	function load.string(memory, addr, len)
		local start = cast(alias_t, memory.data) + addr

		return ffi.string(start, len)
	end

	function store.i32_n8(memory, addr, value)
		by_offset(memory.data, addr).i8 = value
	end

	function store.i32_n16(memory, addr, value)
		by_offset(memory.data, addr).i16 = value
	end

	function store.i32(memory, addr, value)
		by_offset(memory.data, addr).i32 = value
	end

	function store.i64_n8(memory, addr, value)
		by_offset(memory.data, addr).i8 = value
	end

	function store.i64_n16(memory, addr, value)
		by_offset(memory.data, addr).i16 = value
	end

	function store.i64_n32(memory, addr, value)
		by_offset(memory.data, addr).i32 = value
	end

	function store.i64(memory, addr, value)
		by_offset(memory.data, addr).i64 = value
	end

	function store.f32(memory, addr, value)
		by_offset(memory.data, addr).f32 = value
	end

	function store.f64(memory, addr, value)
		by_offset(memory.data, addr).f64 = value
	end

	function store.string(memory, addr, data, len)
		local start = by_offset(memory.data, addr)

		ffi.copy(start, data, len or #data)
	end

	function store.copy(memory_1, addr_1, memory_2, addr_2, len)
		local start_1 = by_offset(memory_1.data, addr_1)
		local start_2 = by_offset(memory_2.data, addr_2)

		ffi.copy(start_1, start_2, len)
	end

	function store.fill(memory, addr, len, value)
		local start = by_offset(memory.data, addr)

		ffi.fill(start, len, value)
	end

	local WASM_PAGE_SIZE = 65536

	local function finalizer(memory)
		ffi.C.free(memory.data)
	end

	local function grow_unchecked(memory, old, new)
		memory.data = ffi.C.realloc(memory.data, new)

		assert(memory.data ~= nil, "failed to reallocate")

		ffi.fill(by_offset(memory.data, old), new - old, 0)
	end

	function allocator.new(min, max)
		local data = ffi.C.calloc(min, WASM_PAGE_SIZE)

		assert(data ~= nil, "failed to allocate")

		local memory = ffi.new("struct Memory", min, max, data)

		return ffi.gc(memory, finalizer)
	end

	function allocator.grow(memory, num)
		if num == 0 then
			return memory.min
		end

		local old = memory.min
		local new = old + num

		if new > memory.max then
			return -1
		else
			grow_unchecked(memory, old * WASM_PAGE_SIZE, new * WASM_PAGE_SIZE)
			memory.min = new

			return old
		end
	end

	module.load = load
	module.store = store
	module.allocator = allocator
end

return module

end)()
local abs_f64 = math.abs
local add_i32 = rt.add.i32
local band_i32 = bit.band
local band_i64 = bit.band
local bor_i32 = bit.bor
local bor_i64 = bit.bor
local bxor_i32 = bit.bxor
local bxor_i64 = bit.bxor
local clz_i32 = rt.clz.i32
local convert_f32_i32 = rt.convert.f32_i32
local convert_f64_i32 = rt.convert.f64_i32
local convert_f64_u32 = rt.convert.f64_u32
local copysign_f64 = rt.copysign.f64
local ctz_i32 = rt.ctz.i32
local demote_f32_f64 = rt.demote.f32_f64
local div_i32 = rt.div.i32
local div_u32 = rt.div.u32
local div_u64 = rt.div.u64
local extend_i32_n8 = rt.extend.i32_n8
local extend_i64_i32 = rt.extend.i64_i32
local extend_i64_u32 = rt.extend.i64_u32
local ge_u32 = rt.ge.u32
local ge_u64 = rt.ge.u64
local gt_u32 = rt.gt.u32
local gt_u64 = rt.gt.u64
local le_u32 = rt.le.u32
local le_u64 = rt.le.u64
local load_f64 = rt.load.f64
local load_i32 = rt.load.i32
local load_i32_i8 = rt.load.i32_i8
local load_i32_u16 = rt.load.i32_u16
local load_i32_u8 = rt.load.i32_u8
local load_i64 = rt.load.i64
local load_i64_i16 = rt.load.i64_i16
local load_i64_i32 = rt.load.i64_i32
local load_i64_i8 = rt.load.i64_i8
local load_i64_u16 = rt.load.i64_u16
local load_i64_u32 = rt.load.i64_u32
local load_i64_u8 = rt.load.i64_u8
local lt_u32 = rt.lt.u32
local lt_u64 = rt.lt.u64
local mul_i32 = rt.mul.i32
local neg_f64 = rt.neg.f64
local promote_f64_f32 = rt.promote.f64_f32
local reinterpret_f64_i64 = rt.reinterpret.f64_i64
local reinterpret_i64_f64 = rt.reinterpret.i64_f64
local rem_i32 = math.fmod
local rem_u32 = rt.rem.u32
local rotl_i32 = bit.rol
local rotl_i64 = bit.rol
local rotr_i64 = bit.ror
local saturate_i32_f64 = rt.saturate.i32_f64
local saturate_u32_f64 = rt.saturate.u32_f64
local shl_i32 = bit.lshift
local shl_i64 = bit.lshift
local shr_i32 = bit.arshift
local shr_i64 = bit.arshift
local shr_u32 = bit.rshift
local shr_u64 = bit.rshift
local store_f32 = rt.store.f32
local store_f64 = rt.store.f64
local store_i32 = rt.store.i32
local store_i32_n16 = rt.store.i32_n16
local store_i32_n8 = rt.store.i32_n8
local store_i64 = rt.store.i64
local store_i64_n16 = rt.store.i64_n16
local store_i64_n32 = rt.store.i64_n32
local store_i64_n8 = rt.store.i64_n8
local sub_i32 = rt.sub.i32
local truncate_f64 = rt.truncate.f64
local wrap_i32_i64 = rt.wrap.i32_i64
local memory_at_0
local table_new = require("table.new")
local FUNC_LIST = table_new(79, 1)
local TABLE_LIST = table_new(0, 1)
local MEMORY_LIST = table_new(0, 1)
local GLOBAL_LIST = table_new(1, 1)
FUNC_LIST[6] = function()
end
FUNC_LIST[7] = function()
	local loc_0 = 0
	local reg_0
	if load_i32(memory_at_0, add_i32(GLOBAL_LIST[1].value, 4480)) ~= 0 then
		goto continue_at_2
	end
	store_i32(memory_at_0, add_i32(GLOBAL_LIST[1].value, 4480), 1)
	FUNC_LIST[6]()
	reg_0 = FUNC_LIST[78]()
	loc_0 = reg_0
	FUNC_LIST[24]()
	if loc_0 ~= 0 then
		goto continue_at_1
	end
	goto continue_at_0
	::continue_at_2::
	error("out of code bounds")
	::continue_at_1::
	FUNC_LIST[20](loc_0)
	error("out of code bounds")
	::continue_at_0::
end
FUNC_LIST[8] = function(loc_0)
	local reg_0
	reg_0 = FUNC_LIST[9](loc_0)
	return reg_0
end
FUNC_LIST[9] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	local loc_9 = 0
	local loc_10 = 0
	local loc_11 = 0
	local reg_0
	loc_1 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_1
	loc_2 = load_i32(memory_at_0, 0 + 4512)
	if loc_2 ~= 0 then
		goto continue_at_13
	end
	loc_3 = load_i32(memory_at_0, 0 + 4960)
	if loc_3 ~= 0 then
		goto continue_at_14
	end
	store_i64(memory_at_0, 0 + 4972, -1LL)
	store_i64(memory_at_0, 0 + 4964, 281474976776192LL)
	loc_3 = bxor_i32(band_i32(add_i32(loc_1, 8), -16), 1431655768)
	store_i32(memory_at_0, 0 + 4960, loc_3)
	store_i32(memory_at_0, 0 + 4980, 0)
	store_i32(memory_at_0, 0 + 4932, 0)
	::continue_at_14::
	if lt_u32(131072, 72640) then
		goto continue_at_12
	end
	loc_2 = 0
	if lt_u32(sub_i32(131072, 72640), 89) then
		goto continue_at_13
	end
	loc_4 = 0
	store_i32(memory_at_0, 0 + 4936, 72640)
	store_i32(memory_at_0, 0 + 4504, 72640)
	store_i32(memory_at_0, 0 + 4524, loc_3)
	store_i32(memory_at_0, 0 + 4520, -1)
	loc_3 = sub_i32(131072, 72640)
	store_i32(memory_at_0, 0 + 4940, loc_3)
	store_i32(memory_at_0, 0 + 4924, loc_3)
	store_i32(memory_at_0, 0 + 4920, loc_3)
	::continue_at_15::
	while true do
		loc_3 = add_i32(loc_4, 4536)
		store_i32(memory_at_0, add_i32(loc_4, 4548), loc_3)
		loc_5 = add_i32(loc_4, 4528)
		store_i32(memory_at_0, loc_3, loc_5)
		store_i32(memory_at_0, add_i32(loc_4, 4540), loc_5)
		loc_5 = add_i32(loc_4, 4544)
		store_i32(memory_at_0, add_i32(loc_4, 4556), loc_5)
		store_i32(memory_at_0, loc_5, loc_3)
		loc_3 = add_i32(loc_4, 4552)
		store_i32(memory_at_0, add_i32(loc_4, 4564), loc_3)
		store_i32(memory_at_0, loc_3, loc_5)
		store_i32(memory_at_0, add_i32(loc_4, 4560), loc_3)
		loc_4 = add_i32(loc_4, 32)
		if loc_4 ~= 256 then
			goto continue_at_15
		end
		break
	end
	store_i32(memory_at_0, add_i32(131072, -52), 56)
	store_i32(memory_at_0, 0 + 4516, load_i32(memory_at_0, 0 + 4976))
	loc_4 = band_i32(sub_i32(-8, 72640), 15)
	loc_2 = add_i32(72640, loc_4)
	store_i32(memory_at_0, 0 + 4512, loc_2)
	loc_4 = add_i32(sub_i32(sub_i32(131072, 72640), loc_4), -56)
	store_i32(memory_at_0, 0 + 4500, loc_4)
	store_i32(memory_at_0, loc_2 + 4, bor_i32(loc_4, 1))
	::continue_at_13::
	if gt_u32(loc_0, 236) then
		goto continue_at_17
	end
	loc_6 = load_i32(memory_at_0, 0 + 4488)
	loc_5 = (lt_u32(loc_0, 11) and 16 or band_i32(add_i32(loc_0, 19), 496))
	loc_3 = shr_u32(loc_5, 3)
	loc_4 = shr_u32(loc_6, loc_3)
	if band_i32(loc_4, 3) == 0 then
		goto continue_at_18
	end
	loc_5 = bxor_i32(bor_i32(band_i32(loc_4, 1), loc_3), 1)
	loc_3 = shl_i32(loc_5, 3)
	loc_4 = add_i32(loc_3, 4528)
	loc_3 = load_i32(memory_at_0, add_i32(loc_3, 4536))
	loc_0 = load_i32(memory_at_0, loc_3 + 8)
	if loc_4 ~= loc_0 then
		goto continue_at_20
	end
	store_i32(memory_at_0, 0 + 4488, band_i32(loc_6, rotl_i32(-2, loc_5)))
	goto continue_at_19
	::continue_at_20::
	store_i32(memory_at_0, loc_4 + 8, loc_0)
	store_i32(memory_at_0, loc_0 + 12, loc_4)
	::continue_at_19::
	loc_4 = add_i32(loc_3, 8)
	loc_5 = shl_i32(loc_5, 3)
	store_i32(memory_at_0, loc_3 + 4, bor_i32(loc_5, 3))
	loc_3 = add_i32(loc_3, loc_5)
	store_i32(memory_at_0, loc_3 + 4, bor_i32(load_i32(memory_at_0, loc_3 + 4), 1))
	goto continue_at_1
	::continue_at_18::
	loc_7 = load_i32(memory_at_0, 0 + 4496)
	if le_u32(loc_5, loc_7) then
		goto continue_at_16
	end
	if loc_4 == 0 then
		goto continue_at_21
	end
	reg_0 = shl_i32(loc_4, loc_3)
	loc_4 = shl_i32(2, loc_3)
	loc_3 = ctz_i32(band_i32(reg_0, bor_i32(loc_4, sub_i32(0, loc_4))))
	loc_4 = shl_i32(loc_3, 3)
	loc_0 = add_i32(loc_4, 4528)
	loc_4 = load_i32(memory_at_0, add_i32(loc_4, 4536))
	loc_8 = load_i32(memory_at_0, loc_4 + 8)
	if loc_0 ~= loc_8 then
		goto continue_at_23
	end
	loc_6 = band_i32(loc_6, rotl_i32(-2, loc_3))
	store_i32(memory_at_0, 0 + 4488, loc_6)
	goto continue_at_22
	::continue_at_23::
	store_i32(memory_at_0, loc_0 + 8, loc_8)
	store_i32(memory_at_0, loc_8 + 12, loc_0)
	::continue_at_22::
	store_i32(memory_at_0, loc_4 + 4, bor_i32(loc_5, 3))
	loc_3 = shl_i32(loc_3, 3)
	loc_0 = sub_i32(loc_3, loc_5)
	store_i32(memory_at_0, add_i32(loc_4, loc_3), loc_0)
	loc_8 = add_i32(loc_4, loc_5)
	store_i32(memory_at_0, loc_8 + 4, bor_i32(loc_0, 1))
	if loc_7 == 0 then
		goto continue_at_24
	end
	loc_5 = add_i32(band_i32(loc_7, -8), 4528)
	loc_3 = load_i32(memory_at_0, 0 + 4508)
	loc_9 = shl_i32(1, shr_u32(loc_7, 3))
	if band_i32(loc_6, loc_9) ~= 0 then
		goto continue_at_26
	end
	store_i32(memory_at_0, 0 + 4488, bor_i32(loc_6, loc_9))
	loc_9 = loc_5
	goto continue_at_25
	::continue_at_26::
	loc_9 = load_i32(memory_at_0, loc_5 + 8)
	::continue_at_25::
	store_i32(memory_at_0, loc_9 + 12, loc_3)
	store_i32(memory_at_0, loc_5 + 8, loc_3)
	store_i32(memory_at_0, loc_3 + 12, loc_5)
	store_i32(memory_at_0, loc_3 + 8, loc_9)
	::continue_at_24::
	loc_4 = add_i32(loc_4, 8)
	store_i32(memory_at_0, 0 + 4508, loc_8)
	store_i32(memory_at_0, 0 + 4496, loc_0)
	goto continue_at_1
	::continue_at_21::
	loc_10 = load_i32(memory_at_0, 0 + 4492)
	if loc_10 == 0 then
		goto continue_at_16
	end
	loc_8 = load_i32(memory_at_0, add_i32(shl_i32(ctz_i32(loc_10), 2), 4792))
	loc_3 = sub_i32(band_i32(load_i32(memory_at_0, loc_8 + 4), -8), loc_5)
	loc_0 = loc_8
	::continue_at_28::
	while true do
		loc_4 = load_i32(memory_at_0, loc_0 + 16)
		if loc_4 ~= 0 then
			goto continue_at_29
		end
		loc_4 = load_i32(memory_at_0, loc_0 + 20)
		if loc_4 == 0 then
			goto continue_at_27
		end
		::continue_at_29::
		loc_0 = sub_i32(band_i32(load_i32(memory_at_0, loc_4 + 4), -8), loc_5)
		reg_0 = loc_0
		loc_0 = (lt_u32(loc_0, loc_3) and 1 or 0)
		loc_3 = (loc_0 ~= 0 and reg_0 or loc_3)
		loc_8 = (loc_0 ~= 0 and loc_4 or loc_8)
		loc_0 = loc_4
		goto continue_at_28
	end
	::continue_at_27::
	loc_2 = load_i32(memory_at_0, loc_8 + 24)
	loc_4 = load_i32(memory_at_0, loc_8 + 12)
	if loc_4 == loc_8 then
		goto continue_at_30
	end
	loc_0 = load_i32(memory_at_0, loc_8 + 8)
	store_i32(memory_at_0, loc_0 + 12, loc_4)
	store_i32(memory_at_0, loc_4 + 8, loc_0)
	goto continue_at_2
	::continue_at_30::
	loc_0 = load_i32(memory_at_0, loc_8 + 20)
	if loc_0 == 0 then
		goto continue_at_32
	end
	loc_9 = add_i32(loc_8, 20)
	goto continue_at_31
	::continue_at_32::
	loc_0 = load_i32(memory_at_0, loc_8 + 16)
	if loc_0 == 0 then
		goto continue_at_11
	end
	loc_9 = add_i32(loc_8, 16)
	::continue_at_31::
	::continue_at_33::
	while true do
		loc_11 = loc_9
		loc_4 = loc_0
		loc_9 = add_i32(loc_4, 20)
		loc_0 = load_i32(memory_at_0, loc_4 + 20)
		if loc_0 ~= 0 then
			goto continue_at_33
		end
		loc_9 = add_i32(loc_4, 16)
		loc_0 = load_i32(memory_at_0, loc_4 + 16)
		if loc_0 ~= 0 then
			goto continue_at_33
		end
		break
	end
	store_i32(memory_at_0, loc_11, 0)
	goto continue_at_2
	::continue_at_17::
	loc_5 = -1
	if gt_u32(loc_0, -65) then
		goto continue_at_16
	end
	loc_4 = add_i32(loc_0, 19)
	loc_5 = band_i32(loc_4, -16)
	loc_10 = load_i32(memory_at_0, 0 + 4492)
	if loc_10 == 0 then
		goto continue_at_16
	end
	loc_7 = 31
	if gt_u32(loc_0, 16777196) then
		goto continue_at_34
	end
	loc_4 = clz_i32(shr_u32(loc_4, 8))
	loc_7 = add_i32(sub_i32(band_i32(shr_u32(loc_5, sub_i32(38, loc_4)), 1), shl_i32(loc_4, 1)), 62)
	::continue_at_34::
	loc_3 = sub_i32(0, loc_5)
	loc_0 = load_i32(memory_at_0, add_i32(shl_i32(loc_7, 2), 4792))
	if loc_0 ~= 0 then
		goto continue_at_38
	end
	loc_4 = 0
	loc_9 = 0
	goto continue_at_37
	::continue_at_38::
	loc_4 = 0
	loc_8 = shl_i32(loc_5, (loc_7 == 31 and 0 or sub_i32(25, shr_u32(loc_7, 1))))
	loc_9 = 0
	::continue_at_39::
	while true do
		loc_6 = sub_i32(band_i32(load_i32(memory_at_0, loc_0 + 4), -8), loc_5)
		if ge_u32(loc_6, loc_3) then
			goto continue_at_40
		end
		loc_3 = loc_6
		loc_9 = loc_0
		if loc_6 ~= 0 then
			goto continue_at_40
		end
		loc_3 = 0
		loc_9 = loc_0
		loc_4 = loc_0
		goto continue_at_36
		::continue_at_40::
		loc_6 = load_i32(memory_at_0, loc_0 + 20)
		loc_11 = load_i32(memory_at_0, add_i32(loc_0, band_i32(shr_u32(loc_8, 29), 4)) + 16)
		loc_4 = (loc_6 ~= 0 and (loc_6 == loc_11 and loc_4 or loc_6) or loc_4)
		loc_8 = shl_i32(loc_8, 1)
		loc_0 = loc_11
		if loc_11 ~= 0 then
			goto continue_at_39
		end
		break
	end
	::continue_at_37::
	if bor_i32(loc_4, loc_9) ~= 0 then
		goto continue_at_41
	end
	loc_9 = 0
	loc_4 = shl_i32(2, loc_7)
	loc_4 = band_i32(bor_i32(loc_4, sub_i32(0, loc_4)), loc_10)
	if loc_4 == 0 then
		goto continue_at_16
	end
	loc_4 = load_i32(memory_at_0, add_i32(shl_i32(ctz_i32(loc_4), 2), 4792))
	::continue_at_41::
	if loc_4 == 0 then
		goto continue_at_35
	end
	::continue_at_36::
	::continue_at_42::
	while true do
		loc_6 = sub_i32(band_i32(load_i32(memory_at_0, loc_4 + 4), -8), loc_5)
		loc_8 = (lt_u32(loc_6, loc_3) and 1 or 0)
		loc_0 = load_i32(memory_at_0, loc_4 + 16)
		if loc_0 ~= 0 then
			goto continue_at_43
		end
		loc_0 = load_i32(memory_at_0, loc_4 + 20)
		::continue_at_43::
		loc_3 = (loc_8 ~= 0 and loc_6 or loc_3)
		loc_9 = (loc_8 ~= 0 and loc_4 or loc_9)
		loc_4 = loc_0
		if loc_0 ~= 0 then
			goto continue_at_42
		end
		break
	end
	::continue_at_35::
	if loc_9 == 0 then
		goto continue_at_16
	end
	if ge_u32(loc_3, sub_i32(load_i32(memory_at_0, 0 + 4496), loc_5)) then
		goto continue_at_16
	end
	loc_11 = load_i32(memory_at_0, loc_9 + 24)
	loc_4 = load_i32(memory_at_0, loc_9 + 12)
	if loc_4 == loc_9 then
		goto continue_at_44
	end
	loc_0 = load_i32(memory_at_0, loc_9 + 8)
	store_i32(memory_at_0, loc_0 + 12, loc_4)
	store_i32(memory_at_0, loc_4 + 8, loc_0)
	goto continue_at_3
	::continue_at_44::
	loc_0 = load_i32(memory_at_0, loc_9 + 20)
	if loc_0 == 0 then
		goto continue_at_46
	end
	loc_8 = add_i32(loc_9, 20)
	goto continue_at_45
	::continue_at_46::
	loc_0 = load_i32(memory_at_0, loc_9 + 16)
	if loc_0 == 0 then
		goto continue_at_10
	end
	loc_8 = add_i32(loc_9, 16)
	::continue_at_45::
	::continue_at_47::
	while true do
		loc_6 = loc_8
		loc_4 = loc_0
		loc_8 = add_i32(loc_4, 20)
		loc_0 = load_i32(memory_at_0, loc_4 + 20)
		if loc_0 ~= 0 then
			goto continue_at_47
		end
		loc_8 = add_i32(loc_4, 16)
		loc_0 = load_i32(memory_at_0, loc_4 + 16)
		if loc_0 ~= 0 then
			goto continue_at_47
		end
		break
	end
	store_i32(memory_at_0, loc_6, 0)
	goto continue_at_3
	::continue_at_16::
	loc_4 = load_i32(memory_at_0, 0 + 4496)
	if lt_u32(loc_4, loc_5) then
		goto continue_at_48
	end
	loc_3 = load_i32(memory_at_0, 0 + 4508)
	loc_0 = sub_i32(loc_4, loc_5)
	if lt_u32(loc_0, 16) then
		goto continue_at_50
	end
	loc_8 = add_i32(loc_3, loc_5)
	store_i32(memory_at_0, loc_8 + 4, bor_i32(loc_0, 1))
	store_i32(memory_at_0, add_i32(loc_3, loc_4), loc_0)
	store_i32(memory_at_0, loc_3 + 4, bor_i32(loc_5, 3))
	goto continue_at_49
	::continue_at_50::
	store_i32(memory_at_0, loc_3 + 4, bor_i32(loc_4, 3))
	loc_4 = add_i32(loc_3, loc_4)
	store_i32(memory_at_0, loc_4 + 4, bor_i32(load_i32(memory_at_0, loc_4 + 4), 1))
	loc_8 = 0
	loc_0 = 0
	::continue_at_49::
	store_i32(memory_at_0, 0 + 4496, loc_0)
	store_i32(memory_at_0, 0 + 4508, loc_8)
	loc_4 = add_i32(loc_3, 8)
	goto continue_at_1
	::continue_at_48::
	loc_0 = load_i32(memory_at_0, 0 + 4500)
	if le_u32(loc_0, loc_5) then
		goto continue_at_51
	end
	loc_4 = add_i32(loc_2, loc_5)
	loc_3 = sub_i32(loc_0, loc_5)
	store_i32(memory_at_0, loc_4 + 4, bor_i32(loc_3, 1))
	store_i32(memory_at_0, 0 + 4512, loc_4)
	store_i32(memory_at_0, 0 + 4500, loc_3)
	store_i32(memory_at_0, loc_2 + 4, bor_i32(loc_5, 3))
	loc_4 = add_i32(loc_2, 8)
	goto continue_at_1
	::continue_at_51::
	if load_i32(memory_at_0, 0 + 4960) == 0 then
		goto continue_at_53
	end
	loc_3 = load_i32(memory_at_0, 0 + 4968)
	goto continue_at_52
	::continue_at_53::
	store_i64(memory_at_0, 0 + 4972, -1LL)
	store_i64(memory_at_0, 0 + 4964, 281474976776192LL)
	store_i32(memory_at_0, 0 + 4960, bxor_i32(band_i32(add_i32(loc_1, 12), -16), 1431655768))
	store_i32(memory_at_0, 0 + 4980, 0)
	store_i32(memory_at_0, 0 + 4932, 0)
	loc_3 = 65536
	::continue_at_52::
	loc_4 = 0
	loc_11 = add_i32(loc_5, 71)
	loc_8 = add_i32(loc_3, loc_11)
	loc_6 = sub_i32(0, loc_3)
	loc_9 = band_i32(loc_8, loc_6)
	if gt_u32(loc_9, loc_5) then
		goto continue_at_54
	end
	store_i32(memory_at_0, 0 + 4484, 48)
	goto continue_at_1
	::continue_at_54::
	loc_4 = load_i32(memory_at_0, 0 + 4928)
	if loc_4 == 0 then
		goto continue_at_55
	end
	loc_3 = load_i32(memory_at_0, 0 + 4920)
	loc_7 = add_i32(loc_3, loc_9)
	if le_u32(loc_7, loc_3) then
		goto continue_at_56
	end
	if le_u32(loc_7, loc_4) then
		goto continue_at_55
	end
	::continue_at_56::
	loc_4 = 0
	store_i32(memory_at_0, 0 + 4484, 48)
	goto continue_at_1
	::continue_at_55::
	if band_i32(load_i32_u8(memory_at_0, 0 + 4932), 4) ~= 0 then
		goto continue_at_7
	end
	if loc_2 == 0 then
		goto continue_at_59
	end
	loc_4 = 4936
	::continue_at_60::
	while true do
		loc_3 = load_i32(memory_at_0, loc_4)
		if lt_u32(loc_2, loc_3) then
			goto continue_at_61
		end
		if lt_u32(loc_2, add_i32(loc_3, load_i32(memory_at_0, loc_4 + 4))) then
			goto continue_at_58
		end
		::continue_at_61::
		loc_4 = load_i32(memory_at_0, loc_4 + 8)
		if loc_4 ~= 0 then
			goto continue_at_60
		end
		break
	end
	::continue_at_59::
	reg_0 = FUNC_LIST[22](0)
	loc_8 = reg_0
	if loc_8 == -1 then
		goto continue_at_8
	end
	loc_6 = loc_9
	loc_4 = load_i32(memory_at_0, 0 + 4964)
	loc_3 = add_i32(loc_4, -1)
	if band_i32(loc_3, loc_8) == 0 then
		goto continue_at_62
	end
	loc_6 = add_i32(sub_i32(loc_9, loc_8), band_i32(add_i32(loc_3, loc_8), sub_i32(0, loc_4)))
	::continue_at_62::
	if le_u32(loc_6, loc_5) then
		goto continue_at_8
	end
	if gt_u32(loc_6, 2147483646) then
		goto continue_at_8
	end
	loc_4 = load_i32(memory_at_0, 0 + 4928)
	if loc_4 == 0 then
		goto continue_at_63
	end
	loc_3 = load_i32(memory_at_0, 0 + 4920)
	loc_0 = add_i32(loc_3, loc_6)
	if le_u32(loc_0, loc_3) then
		goto continue_at_8
	end
	if gt_u32(loc_0, loc_4) then
		goto continue_at_8
	end
	::continue_at_63::
	reg_0 = FUNC_LIST[22](loc_6)
	loc_4 = reg_0
	if loc_4 ~= loc_8 then
		goto continue_at_57
	end
	goto continue_at_6
	::continue_at_58::
	loc_6 = band_i32(sub_i32(loc_8, loc_0), loc_6)
	if gt_u32(loc_6, 2147483646) then
		goto continue_at_8
	end
	reg_0 = FUNC_LIST[22](loc_6)
	loc_8 = reg_0
	if loc_8 == add_i32(load_i32(memory_at_0, loc_4), load_i32(memory_at_0, loc_4 + 4)) then
		goto continue_at_9
	end
	loc_4 = loc_8
	::continue_at_57::
	if ge_u32(loc_6, add_i32(loc_5, 72)) then
		goto continue_at_64
	end
	if loc_4 == -1 then
		goto continue_at_64
	end
	loc_3 = load_i32(memory_at_0, 0 + 4968)
	loc_3 = band_i32(add_i32(sub_i32(loc_11, loc_6), loc_3), sub_i32(0, loc_3))
	if le_u32(loc_3, 2147483646) then
		goto continue_at_65
	end
	loc_8 = loc_4
	goto continue_at_6
	::continue_at_65::
	reg_0 = FUNC_LIST[22](loc_3)
	if reg_0 == -1 then
		goto continue_at_66
	end
	loc_6 = add_i32(loc_3, loc_6)
	loc_8 = loc_4
	goto continue_at_6
	::continue_at_66::
	reg_0 = FUNC_LIST[22](sub_i32(0, loc_6))
	goto continue_at_8
	::continue_at_64::
	loc_8 = loc_4
	if loc_4 ~= -1 then
		goto continue_at_6
	end
	goto continue_at_8
	::continue_at_12::
	error("out of code bounds")
	::continue_at_11::
	loc_4 = 0
	goto continue_at_2
	::continue_at_10::
	loc_4 = 0
	goto continue_at_3
	::continue_at_9::
	if loc_8 ~= -1 then
		goto continue_at_6
	end
	::continue_at_8::
	store_i32(memory_at_0, 0 + 4932, bor_i32(load_i32(memory_at_0, 0 + 4932), 4))
	::continue_at_7::
	if gt_u32(loc_9, 2147483646) then
		goto continue_at_5
	end
	reg_0 = FUNC_LIST[22](loc_9)
	loc_8 = reg_0
	reg_0 = FUNC_LIST[22](0)
	loc_4 = reg_0
	if loc_8 == -1 then
		goto continue_at_5
	end
	if loc_4 == -1 then
		goto continue_at_5
	end
	if ge_u32(loc_8, loc_4) then
		goto continue_at_5
	end
	loc_6 = sub_i32(loc_4, loc_8)
	if le_u32(loc_6, add_i32(loc_5, 56)) then
		goto continue_at_5
	end
	::continue_at_6::
	loc_4 = add_i32(load_i32(memory_at_0, 0 + 4920), loc_6)
	store_i32(memory_at_0, 0 + 4920, loc_4)
	if le_u32(loc_4, load_i32(memory_at_0, 0 + 4924)) then
		goto continue_at_67
	end
	store_i32(memory_at_0, 0 + 4924, loc_4)
	::continue_at_67::
	loc_3 = load_i32(memory_at_0, 0 + 4512)
	if loc_3 == 0 then
		goto continue_at_71
	end
	loc_4 = 4936
	::continue_at_72::
	while true do
		loc_0 = load_i32(memory_at_0, loc_4)
		loc_9 = load_i32(memory_at_0, loc_4 + 4)
		if loc_8 == add_i32(loc_0, loc_9) then
			goto continue_at_70
		end
		loc_4 = load_i32(memory_at_0, loc_4 + 8)
		if loc_4 ~= 0 then
			goto continue_at_72
		end
		goto continue_at_69
	end
	::continue_at_71::
	loc_4 = load_i32(memory_at_0, 0 + 4504)
	if loc_4 == 0 then
		goto continue_at_74
	end
	if ge_u32(loc_8, loc_4) then
		goto continue_at_73
	end
	::continue_at_74::
	store_i32(memory_at_0, 0 + 4504, loc_8)
	::continue_at_73::
	loc_4 = 0
	store_i32(memory_at_0, 0 + 4940, loc_6)
	store_i32(memory_at_0, 0 + 4936, loc_8)
	store_i32(memory_at_0, 0 + 4520, -1)
	store_i32(memory_at_0, 0 + 4524, load_i32(memory_at_0, 0 + 4960))
	store_i32(memory_at_0, 0 + 4948, 0)
	::continue_at_75::
	while true do
		loc_3 = add_i32(loc_4, 4536)
		store_i32(memory_at_0, add_i32(loc_4, 4548), loc_3)
		loc_0 = add_i32(loc_4, 4528)
		store_i32(memory_at_0, loc_3, loc_0)
		store_i32(memory_at_0, add_i32(loc_4, 4540), loc_0)
		loc_0 = add_i32(loc_4, 4544)
		store_i32(memory_at_0, add_i32(loc_4, 4556), loc_0)
		store_i32(memory_at_0, loc_0, loc_3)
		loc_3 = add_i32(loc_4, 4552)
		store_i32(memory_at_0, add_i32(loc_4, 4564), loc_3)
		store_i32(memory_at_0, loc_3, loc_0)
		store_i32(memory_at_0, add_i32(loc_4, 4560), loc_3)
		loc_4 = add_i32(loc_4, 32)
		if loc_4 ~= 256 then
			goto continue_at_75
		end
		break
	end
	loc_4 = band_i32(sub_i32(-8, loc_8), 15)
	loc_3 = add_i32(loc_8, loc_4)
	loc_0 = add_i32(loc_6, -56)
	loc_4 = sub_i32(loc_0, loc_4)
	store_i32(memory_at_0, loc_3 + 4, bor_i32(loc_4, 1))
	store_i32(memory_at_0, 0 + 4516, load_i32(memory_at_0, 0 + 4976))
	store_i32(memory_at_0, 0 + 4500, loc_4)
	store_i32(memory_at_0, 0 + 4512, loc_3)
	store_i32(memory_at_0, add_i32(loc_8, loc_0) + 4, 56)
	goto continue_at_68
	::continue_at_70::
	if ge_u32(loc_3, loc_8) then
		goto continue_at_69
	end
	if lt_u32(loc_3, loc_0) then
		goto continue_at_69
	end
	if band_i32(load_i32(memory_at_0, loc_4 + 12), 8) ~= 0 then
		goto continue_at_69
	end
	loc_0 = band_i32(sub_i32(-8, loc_3), 15)
	loc_8 = add_i32(loc_3, loc_0)
	loc_11 = add_i32(load_i32(memory_at_0, 0 + 4500), loc_6)
	loc_0 = sub_i32(loc_11, loc_0)
	store_i32(memory_at_0, loc_8 + 4, bor_i32(loc_0, 1))
	store_i32(memory_at_0, loc_4 + 4, add_i32(loc_9, loc_6))
	store_i32(memory_at_0, 0 + 4516, load_i32(memory_at_0, 0 + 4976))
	store_i32(memory_at_0, 0 + 4500, loc_0)
	store_i32(memory_at_0, 0 + 4512, loc_8)
	store_i32(memory_at_0, add_i32(loc_3, loc_11) + 4, 56)
	goto continue_at_68
	::continue_at_69::
	if ge_u32(loc_8, load_i32(memory_at_0, 0 + 4504)) then
		goto continue_at_76
	end
	store_i32(memory_at_0, 0 + 4504, loc_8)
	::continue_at_76::
	loc_0 = add_i32(loc_8, loc_6)
	loc_4 = 4936
	::continue_at_79::
	while true do
		loc_9 = load_i32(memory_at_0, loc_4)
		if loc_9 == loc_0 then
			goto continue_at_78
		end
		loc_4 = load_i32(memory_at_0, loc_4 + 8)
		if loc_4 ~= 0 then
			goto continue_at_79
		end
		goto continue_at_77
	end
	::continue_at_78::
	if band_i32(load_i32_u8(memory_at_0, loc_4 + 12), 8) == 0 then
		goto continue_at_4
	end
	::continue_at_77::
	loc_4 = 4936
	::continue_at_81::
	while true do
		loc_0 = load_i32(memory_at_0, loc_4)
		if lt_u32(loc_3, loc_0) then
			goto continue_at_82
		end
		loc_0 = add_i32(loc_0, load_i32(memory_at_0, loc_4 + 4))
		if lt_u32(loc_3, loc_0) then
			goto continue_at_80
		end
		::continue_at_82::
		loc_4 = load_i32(memory_at_0, loc_4 + 8)
		goto continue_at_81
	end
	::continue_at_80::
	loc_4 = band_i32(sub_i32(-8, loc_8), 15)
	loc_11 = add_i32(loc_8, loc_4)
	loc_9 = add_i32(loc_6, -56)
	loc_4 = sub_i32(loc_9, loc_4)
	store_i32(memory_at_0, loc_11 + 4, bor_i32(loc_4, 1))
	store_i32(memory_at_0, add_i32(loc_8, loc_9) + 4, 56)
	loc_9 = add_i32(add_i32(loc_0, band_i32(sub_i32(55, loc_0), 15)), -63)
	loc_9 = (lt_u32(loc_9, add_i32(loc_3, 16)) and loc_3 or loc_9)
	store_i32(memory_at_0, loc_9 + 4, 35)
	store_i32(memory_at_0, 0 + 4516, load_i32(memory_at_0, 0 + 4976))
	store_i32(memory_at_0, 0 + 4500, loc_4)
	store_i32(memory_at_0, 0 + 4512, loc_11)
	store_i64(memory_at_0, add_i32(loc_9, 16), load_i64(memory_at_0, 0 + 4944))
	store_i64(memory_at_0, loc_9 + 8, load_i64(memory_at_0, 0 + 4936))
	store_i32(memory_at_0, 0 + 4944, add_i32(loc_9, 8))
	store_i32(memory_at_0, 0 + 4940, loc_6)
	store_i32(memory_at_0, 0 + 4936, loc_8)
	store_i32(memory_at_0, 0 + 4948, 0)
	loc_4 = add_i32(loc_9, 36)
	::continue_at_83::
	while true do
		store_i32(memory_at_0, loc_4, 7)
		loc_4 = add_i32(loc_4, 4)
		if lt_u32(loc_4, loc_0) then
			goto continue_at_83
		end
		break
	end
	if loc_9 == loc_3 then
		goto continue_at_68
	end
	store_i32(memory_at_0, loc_9 + 4, band_i32(load_i32(memory_at_0, loc_9 + 4), -2))
	loc_8 = sub_i32(loc_9, loc_3)
	store_i32(memory_at_0, loc_9, loc_8)
	store_i32(memory_at_0, loc_3 + 4, bor_i32(loc_8, 1))
	if gt_u32(loc_8, 255) then
		goto continue_at_85
	end
	loc_4 = add_i32(band_i32(loc_8, -8), 4528)
	loc_0 = load_i32(memory_at_0, 0 + 4488)
	loc_8 = shl_i32(1, shr_u32(loc_8, 3))
	if band_i32(loc_0, loc_8) ~= 0 then
		goto continue_at_87
	end
	store_i32(memory_at_0, 0 + 4488, bor_i32(loc_0, loc_8))
	loc_0 = loc_4
	goto continue_at_86
	::continue_at_87::
	loc_0 = load_i32(memory_at_0, loc_4 + 8)
	::continue_at_86::
	store_i32(memory_at_0, loc_0 + 12, loc_3)
	store_i32(memory_at_0, loc_4 + 8, loc_3)
	loc_8 = 12
	loc_9 = 8
	goto continue_at_84
	::continue_at_85::
	loc_4 = 31
	if gt_u32(loc_8, 16777215) then
		goto continue_at_88
	end
	loc_4 = clz_i32(shr_u32(loc_8, 8))
	loc_4 = add_i32(sub_i32(band_i32(shr_u32(loc_8, sub_i32(38, loc_4)), 1), shl_i32(loc_4, 1)), 62)
	::continue_at_88::
	store_i32(memory_at_0, loc_3 + 28, loc_4)
	store_i64(memory_at_0, loc_3 + 16, 0LL)
	loc_0 = add_i32(shl_i32(loc_4, 2), 4792)
	loc_9 = load_i32(memory_at_0, 0 + 4492)
	loc_6 = shl_i32(1, loc_4)
	if band_i32(loc_9, loc_6) ~= 0 then
		goto continue_at_91
	end
	store_i32(memory_at_0, loc_0, loc_3)
	store_i32(memory_at_0, 0 + 4492, bor_i32(loc_9, loc_6))
	store_i32(memory_at_0, loc_3 + 24, loc_0)
	goto continue_at_90
	::continue_at_91::
	loc_4 = shl_i32(loc_8, (loc_4 == 31 and 0 or sub_i32(25, shr_u32(loc_4, 1))))
	loc_9 = load_i32(memory_at_0, loc_0)
	::continue_at_92::
	while true do
		loc_0 = loc_9
		if band_i32(load_i32(memory_at_0, loc_0 + 4), -8) == loc_8 then
			goto continue_at_89
		end
		loc_9 = shr_u32(loc_4, 29)
		loc_4 = shl_i32(loc_4, 1)
		loc_6 = add_i32(loc_0, band_i32(loc_9, 4))
		loc_9 = load_i32(memory_at_0, loc_6 + 16)
		if loc_9 ~= 0 then
			goto continue_at_92
		end
		break
	end
	store_i32(memory_at_0, add_i32(loc_6, 16), loc_3)
	store_i32(memory_at_0, loc_3 + 24, loc_0)
	::continue_at_90::
	loc_8 = 8
	loc_9 = 12
	loc_0 = loc_3
	loc_4 = loc_3
	goto continue_at_84
	::continue_at_89::
	loc_4 = load_i32(memory_at_0, loc_0 + 8)
	store_i32(memory_at_0, loc_0 + 8, loc_3)
	store_i32(memory_at_0, loc_4 + 12, loc_3)
	store_i32(memory_at_0, loc_3 + 8, loc_4)
	loc_4 = 0
	loc_8 = 24
	loc_9 = 12
	::continue_at_84::
	store_i32(memory_at_0, add_i32(loc_3, loc_9), loc_0)
	store_i32(memory_at_0, add_i32(loc_3, loc_8), loc_4)
	::continue_at_68::
	loc_4 = load_i32(memory_at_0, 0 + 4500)
	if le_u32(loc_4, loc_5) then
		goto continue_at_5
	end
	loc_3 = load_i32(memory_at_0, 0 + 4512)
	loc_0 = add_i32(loc_3, loc_5)
	loc_4 = sub_i32(loc_4, loc_5)
	store_i32(memory_at_0, loc_0 + 4, bor_i32(loc_4, 1))
	store_i32(memory_at_0, 0 + 4500, loc_4)
	store_i32(memory_at_0, 0 + 4512, loc_0)
	store_i32(memory_at_0, loc_3 + 4, bor_i32(loc_5, 3))
	loc_4 = add_i32(loc_3, 8)
	goto continue_at_1
	::continue_at_5::
	loc_4 = 0
	store_i32(memory_at_0, 0 + 4484, 48)
	goto continue_at_1
	::continue_at_4::
	store_i32(memory_at_0, loc_4, loc_8)
	store_i32(memory_at_0, loc_4 + 4, add_i32(load_i32(memory_at_0, loc_4 + 4), loc_6))
	reg_0 = FUNC_LIST[10](loc_8, loc_9, loc_5)
	loc_4 = reg_0
	goto continue_at_1
	::continue_at_3::
	if loc_11 == 0 then
		goto continue_at_93
	end
	loc_8 = load_i32(memory_at_0, loc_9 + 28)
	loc_0 = add_i32(shl_i32(loc_8, 2), 4792)
	if loc_9 ~= load_i32(memory_at_0, loc_0) then
		goto continue_at_95
	end
	store_i32(memory_at_0, loc_0, loc_4)
	if loc_4 ~= 0 then
		goto continue_at_94
	end
	loc_10 = band_i32(loc_10, rotl_i32(-2, loc_8))
	store_i32(memory_at_0, 0 + 4492, loc_10)
	goto continue_at_93
	::continue_at_95::
	if load_i32(memory_at_0, loc_11 + 16) ~= loc_9 then
		goto continue_at_97
	end
	store_i32(memory_at_0, loc_11 + 16, loc_4)
	goto continue_at_96
	::continue_at_97::
	store_i32(memory_at_0, loc_11 + 20, loc_4)
	::continue_at_96::
	if loc_4 == 0 then
		goto continue_at_93
	end
	::continue_at_94::
	store_i32(memory_at_0, loc_4 + 24, loc_11)
	loc_0 = load_i32(memory_at_0, loc_9 + 16)
	if loc_0 == 0 then
		goto continue_at_98
	end
	store_i32(memory_at_0, loc_4 + 16, loc_0)
	store_i32(memory_at_0, loc_0 + 24, loc_4)
	::continue_at_98::
	loc_0 = load_i32(memory_at_0, loc_9 + 20)
	if loc_0 == 0 then
		goto continue_at_93
	end
	store_i32(memory_at_0, loc_4 + 20, loc_0)
	store_i32(memory_at_0, loc_0 + 24, loc_4)
	::continue_at_93::
	if gt_u32(loc_3, 15) then
		goto continue_at_100
	end
	loc_4 = bor_i32(loc_3, loc_5)
	store_i32(memory_at_0, loc_9 + 4, bor_i32(loc_4, 3))
	loc_4 = add_i32(loc_9, loc_4)
	store_i32(memory_at_0, loc_4 + 4, bor_i32(load_i32(memory_at_0, loc_4 + 4), 1))
	goto continue_at_99
	::continue_at_100::
	loc_8 = add_i32(loc_9, loc_5)
	store_i32(memory_at_0, loc_8 + 4, bor_i32(loc_3, 1))
	store_i32(memory_at_0, loc_9 + 4, bor_i32(loc_5, 3))
	store_i32(memory_at_0, add_i32(loc_8, loc_3), loc_3)
	if gt_u32(loc_3, 255) then
		goto continue_at_101
	end
	loc_4 = add_i32(band_i32(loc_3, -8), 4528)
	loc_5 = load_i32(memory_at_0, 0 + 4488)
	loc_3 = shl_i32(1, shr_u32(loc_3, 3))
	if band_i32(loc_5, loc_3) ~= 0 then
		goto continue_at_103
	end
	store_i32(memory_at_0, 0 + 4488, bor_i32(loc_5, loc_3))
	loc_3 = loc_4
	goto continue_at_102
	::continue_at_103::
	loc_3 = load_i32(memory_at_0, loc_4 + 8)
	::continue_at_102::
	store_i32(memory_at_0, loc_3 + 12, loc_8)
	store_i32(memory_at_0, loc_4 + 8, loc_8)
	store_i32(memory_at_0, loc_8 + 12, loc_4)
	store_i32(memory_at_0, loc_8 + 8, loc_3)
	goto continue_at_99
	::continue_at_101::
	loc_4 = 31
	if gt_u32(loc_3, 16777215) then
		goto continue_at_104
	end
	loc_4 = clz_i32(shr_u32(loc_3, 8))
	loc_4 = add_i32(sub_i32(band_i32(shr_u32(loc_3, sub_i32(38, loc_4)), 1), shl_i32(loc_4, 1)), 62)
	::continue_at_104::
	store_i32(memory_at_0, loc_8 + 28, loc_4)
	store_i64(memory_at_0, loc_8 + 16, 0LL)
	loc_5 = add_i32(shl_i32(loc_4, 2), 4792)
	loc_0 = shl_i32(1, loc_4)
	if band_i32(loc_10, loc_0) ~= 0 then
		goto continue_at_105
	end
	store_i32(memory_at_0, loc_5, loc_8)
	store_i32(memory_at_0, 0 + 4492, bor_i32(loc_10, loc_0))
	store_i32(memory_at_0, loc_8 + 24, loc_5)
	store_i32(memory_at_0, loc_8 + 8, loc_8)
	store_i32(memory_at_0, loc_8 + 12, loc_8)
	goto continue_at_99
	::continue_at_105::
	loc_4 = shl_i32(loc_3, (loc_4 == 31 and 0 or sub_i32(25, shr_u32(loc_4, 1))))
	loc_0 = load_i32(memory_at_0, loc_5)
	::continue_at_107::
	while true do
		loc_5 = loc_0
		if band_i32(load_i32(memory_at_0, loc_5 + 4), -8) == loc_3 then
			goto continue_at_106
		end
		loc_0 = shr_u32(loc_4, 29)
		loc_4 = shl_i32(loc_4, 1)
		loc_6 = add_i32(loc_5, band_i32(loc_0, 4))
		loc_0 = load_i32(memory_at_0, loc_6 + 16)
		if loc_0 ~= 0 then
			goto continue_at_107
		end
		break
	end
	store_i32(memory_at_0, add_i32(loc_6, 16), loc_8)
	store_i32(memory_at_0, loc_8 + 24, loc_5)
	store_i32(memory_at_0, loc_8 + 12, loc_8)
	store_i32(memory_at_0, loc_8 + 8, loc_8)
	goto continue_at_99
	::continue_at_106::
	loc_4 = load_i32(memory_at_0, loc_5 + 8)
	store_i32(memory_at_0, loc_4 + 12, loc_8)
	store_i32(memory_at_0, loc_5 + 8, loc_8)
	store_i32(memory_at_0, loc_8 + 24, 0)
	store_i32(memory_at_0, loc_8 + 12, loc_5)
	store_i32(memory_at_0, loc_8 + 8, loc_4)
	::continue_at_99::
	loc_4 = add_i32(loc_9, 8)
	goto continue_at_1
	::continue_at_2::
	if loc_2 == 0 then
		goto continue_at_108
	end
	loc_9 = load_i32(memory_at_0, loc_8 + 28)
	loc_0 = add_i32(shl_i32(loc_9, 2), 4792)
	if loc_8 ~= load_i32(memory_at_0, loc_0) then
		goto continue_at_110
	end
	store_i32(memory_at_0, loc_0, loc_4)
	if loc_4 ~= 0 then
		goto continue_at_109
	end
	store_i32(memory_at_0, 0 + 4492, band_i32(loc_10, rotl_i32(-2, loc_9)))
	goto continue_at_108
	::continue_at_110::
	if load_i32(memory_at_0, loc_2 + 16) ~= loc_8 then
		goto continue_at_112
	end
	store_i32(memory_at_0, loc_2 + 16, loc_4)
	goto continue_at_111
	::continue_at_112::
	store_i32(memory_at_0, loc_2 + 20, loc_4)
	::continue_at_111::
	if loc_4 == 0 then
		goto continue_at_108
	end
	::continue_at_109::
	store_i32(memory_at_0, loc_4 + 24, loc_2)
	loc_0 = load_i32(memory_at_0, loc_8 + 16)
	if loc_0 == 0 then
		goto continue_at_113
	end
	store_i32(memory_at_0, loc_4 + 16, loc_0)
	store_i32(memory_at_0, loc_0 + 24, loc_4)
	::continue_at_113::
	loc_0 = load_i32(memory_at_0, loc_8 + 20)
	if loc_0 == 0 then
		goto continue_at_108
	end
	store_i32(memory_at_0, loc_4 + 20, loc_0)
	store_i32(memory_at_0, loc_0 + 24, loc_4)
	::continue_at_108::
	if gt_u32(loc_3, 15) then
		goto continue_at_115
	end
	loc_4 = bor_i32(loc_3, loc_5)
	store_i32(memory_at_0, loc_8 + 4, bor_i32(loc_4, 3))
	loc_4 = add_i32(loc_8, loc_4)
	store_i32(memory_at_0, loc_4 + 4, bor_i32(load_i32(memory_at_0, loc_4 + 4), 1))
	goto continue_at_114
	::continue_at_115::
	loc_0 = add_i32(loc_8, loc_5)
	store_i32(memory_at_0, loc_0 + 4, bor_i32(loc_3, 1))
	store_i32(memory_at_0, loc_8 + 4, bor_i32(loc_5, 3))
	store_i32(memory_at_0, add_i32(loc_0, loc_3), loc_3)
	if loc_7 == 0 then
		goto continue_at_116
	end
	loc_5 = add_i32(band_i32(loc_7, -8), 4528)
	loc_4 = load_i32(memory_at_0, 0 + 4508)
	loc_9 = shl_i32(1, shr_u32(loc_7, 3))
	if band_i32(loc_9, loc_6) ~= 0 then
		goto continue_at_118
	end
	store_i32(memory_at_0, 0 + 4488, bor_i32(loc_9, loc_6))
	loc_9 = loc_5
	goto continue_at_117
	::continue_at_118::
	loc_9 = load_i32(memory_at_0, loc_5 + 8)
	::continue_at_117::
	store_i32(memory_at_0, loc_9 + 12, loc_4)
	store_i32(memory_at_0, loc_5 + 8, loc_4)
	store_i32(memory_at_0, loc_4 + 12, loc_5)
	store_i32(memory_at_0, loc_4 + 8, loc_9)
	::continue_at_116::
	store_i32(memory_at_0, 0 + 4508, loc_0)
	store_i32(memory_at_0, 0 + 4496, loc_3)
	::continue_at_114::
	loc_4 = add_i32(loc_8, 8)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_1, 16)
	reg_0 = loc_4
	return reg_0
end
FUNC_LIST[10] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	local loc_9 = 0
	local reg_0
	loc_3 = add_i32(loc_0, band_i32(sub_i32(-8, loc_0), 15))
	store_i32(memory_at_0, loc_3 + 4, bor_i32(loc_2, 3))
	loc_4 = add_i32(loc_1, band_i32(sub_i32(-8, loc_1), 15))
	loc_5 = add_i32(loc_3, loc_2)
	loc_0 = sub_i32(loc_4, loc_5)
	if loc_4 ~= load_i32(memory_at_0, 0 + 4512) then
		goto continue_at_2
	end
	store_i32(memory_at_0, 0 + 4512, loc_5)
	loc_2 = add_i32(load_i32(memory_at_0, 0 + 4500), loc_0)
	store_i32(memory_at_0, 0 + 4500, loc_2)
	store_i32(memory_at_0, loc_5 + 4, bor_i32(loc_2, 1))
	goto continue_at_1
	::continue_at_2::
	if loc_4 ~= load_i32(memory_at_0, 0 + 4508) then
		goto continue_at_3
	end
	store_i32(memory_at_0, 0 + 4508, loc_5)
	loc_2 = add_i32(load_i32(memory_at_0, 0 + 4496), loc_0)
	store_i32(memory_at_0, 0 + 4496, loc_2)
	store_i32(memory_at_0, loc_5 + 4, bor_i32(loc_2, 1))
	store_i32(memory_at_0, add_i32(loc_5, loc_2), loc_2)
	goto continue_at_1
	::continue_at_3::
	loc_1 = load_i32(memory_at_0, loc_4 + 4)
	if band_i32(loc_1, 3) ~= 1 then
		goto continue_at_4
	end
	loc_6 = band_i32(loc_1, -8)
	loc_2 = load_i32(memory_at_0, loc_4 + 12)
	if gt_u32(loc_1, 255) then
		goto continue_at_6
	end
	loc_7 = load_i32(memory_at_0, loc_4 + 8)
	if loc_2 ~= loc_7 then
		goto continue_at_7
	end
	store_i32(memory_at_0, 0 + 4488, band_i32(load_i32(memory_at_0, 0 + 4488), rotl_i32(-2, shr_u32(loc_1, 3))))
	goto continue_at_5
	::continue_at_7::
	store_i32(memory_at_0, loc_2 + 8, loc_7)
	store_i32(memory_at_0, loc_7 + 12, loc_2)
	goto continue_at_5
	::continue_at_6::
	loc_8 = load_i32(memory_at_0, loc_4 + 24)
	if loc_2 == loc_4 then
		goto continue_at_9
	end
	loc_1 = load_i32(memory_at_0, loc_4 + 8)
	store_i32(memory_at_0, loc_1 + 12, loc_2)
	store_i32(memory_at_0, loc_2 + 8, loc_1)
	goto continue_at_8
	::continue_at_9::
	loc_1 = load_i32(memory_at_0, loc_4 + 20)
	if loc_1 == 0 then
		goto continue_at_12
	end
	loc_7 = add_i32(loc_4, 20)
	goto continue_at_11
	::continue_at_12::
	loc_1 = load_i32(memory_at_0, loc_4 + 16)
	if loc_1 == 0 then
		goto continue_at_10
	end
	loc_7 = add_i32(loc_4, 16)
	::continue_at_11::
	::continue_at_13::
	while true do
		loc_9 = loc_7
		loc_2 = loc_1
		loc_7 = add_i32(loc_2, 20)
		loc_1 = load_i32(memory_at_0, loc_2 + 20)
		if loc_1 ~= 0 then
			goto continue_at_13
		end
		loc_7 = add_i32(loc_2, 16)
		loc_1 = load_i32(memory_at_0, loc_2 + 16)
		if loc_1 ~= 0 then
			goto continue_at_13
		end
		break
	end
	store_i32(memory_at_0, loc_9, 0)
	goto continue_at_8
	::continue_at_10::
	loc_2 = 0
	::continue_at_8::
	if loc_8 == 0 then
		goto continue_at_5
	end
	loc_7 = load_i32(memory_at_0, loc_4 + 28)
	loc_1 = add_i32(shl_i32(loc_7, 2), 4792)
	if loc_4 ~= load_i32(memory_at_0, loc_1) then
		goto continue_at_15
	end
	store_i32(memory_at_0, loc_1, loc_2)
	if loc_2 ~= 0 then
		goto continue_at_14
	end
	store_i32(memory_at_0, 0 + 4492, band_i32(load_i32(memory_at_0, 0 + 4492), rotl_i32(-2, loc_7)))
	goto continue_at_5
	::continue_at_15::
	if load_i32(memory_at_0, loc_8 + 16) ~= loc_4 then
		goto continue_at_17
	end
	store_i32(memory_at_0, loc_8 + 16, loc_2)
	goto continue_at_16
	::continue_at_17::
	store_i32(memory_at_0, loc_8 + 20, loc_2)
	::continue_at_16::
	if loc_2 == 0 then
		goto continue_at_5
	end
	::continue_at_14::
	store_i32(memory_at_0, loc_2 + 24, loc_8)
	loc_1 = load_i32(memory_at_0, loc_4 + 16)
	if loc_1 == 0 then
		goto continue_at_18
	end
	store_i32(memory_at_0, loc_2 + 16, loc_1)
	store_i32(memory_at_0, loc_1 + 24, loc_2)
	::continue_at_18::
	loc_1 = load_i32(memory_at_0, loc_4 + 20)
	if loc_1 == 0 then
		goto continue_at_5
	end
	store_i32(memory_at_0, loc_2 + 20, loc_1)
	store_i32(memory_at_0, loc_1 + 24, loc_2)
	::continue_at_5::
	loc_0 = add_i32(loc_6, loc_0)
	loc_4 = add_i32(loc_4, loc_6)
	loc_1 = load_i32(memory_at_0, loc_4 + 4)
	::continue_at_4::
	store_i32(memory_at_0, loc_4 + 4, band_i32(loc_1, -2))
	store_i32(memory_at_0, add_i32(loc_5, loc_0), loc_0)
	store_i32(memory_at_0, loc_5 + 4, bor_i32(loc_0, 1))
	if gt_u32(loc_0, 255) then
		goto continue_at_19
	end
	loc_2 = add_i32(band_i32(loc_0, -8), 4528)
	loc_1 = load_i32(memory_at_0, 0 + 4488)
	loc_0 = shl_i32(1, shr_u32(loc_0, 3))
	if band_i32(loc_1, loc_0) ~= 0 then
		goto continue_at_21
	end
	store_i32(memory_at_0, 0 + 4488, bor_i32(loc_1, loc_0))
	loc_0 = loc_2
	goto continue_at_20
	::continue_at_21::
	loc_0 = load_i32(memory_at_0, loc_2 + 8)
	::continue_at_20::
	store_i32(memory_at_0, loc_0 + 12, loc_5)
	store_i32(memory_at_0, loc_2 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 12, loc_2)
	store_i32(memory_at_0, loc_5 + 8, loc_0)
	goto continue_at_1
	::continue_at_19::
	loc_2 = 31
	if gt_u32(loc_0, 16777215) then
		goto continue_at_22
	end
	loc_2 = clz_i32(shr_u32(loc_0, 8))
	loc_2 = add_i32(sub_i32(band_i32(shr_u32(loc_0, sub_i32(38, loc_2)), 1), shl_i32(loc_2, 1)), 62)
	::continue_at_22::
	store_i32(memory_at_0, loc_5 + 28, loc_2)
	store_i64(memory_at_0, loc_5 + 16, 0LL)
	loc_1 = add_i32(shl_i32(loc_2, 2), 4792)
	loc_7 = load_i32(memory_at_0, 0 + 4492)
	loc_4 = shl_i32(1, loc_2)
	if band_i32(loc_7, loc_4) ~= 0 then
		goto continue_at_23
	end
	store_i32(memory_at_0, loc_1, loc_5)
	store_i32(memory_at_0, 0 + 4492, bor_i32(loc_7, loc_4))
	store_i32(memory_at_0, loc_5 + 24, loc_1)
	store_i32(memory_at_0, loc_5 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 12, loc_5)
	goto continue_at_1
	::continue_at_23::
	loc_2 = shl_i32(loc_0, (loc_2 == 31 and 0 or sub_i32(25, shr_u32(loc_2, 1))))
	loc_7 = load_i32(memory_at_0, loc_1)
	::continue_at_25::
	while true do
		loc_1 = loc_7
		if band_i32(load_i32(memory_at_0, loc_1 + 4), -8) == loc_0 then
			goto continue_at_24
		end
		loc_7 = shr_u32(loc_2, 29)
		loc_2 = shl_i32(loc_2, 1)
		loc_4 = add_i32(loc_1, band_i32(loc_7, 4))
		loc_7 = load_i32(memory_at_0, loc_4 + 16)
		if loc_7 ~= 0 then
			goto continue_at_25
		end
		break
	end
	store_i32(memory_at_0, add_i32(loc_4, 16), loc_5)
	store_i32(memory_at_0, loc_5 + 24, loc_1)
	store_i32(memory_at_0, loc_5 + 12, loc_5)
	store_i32(memory_at_0, loc_5 + 8, loc_5)
	goto continue_at_1
	::continue_at_24::
	loc_2 = load_i32(memory_at_0, loc_1 + 8)
	store_i32(memory_at_0, loc_2 + 12, loc_5)
	store_i32(memory_at_0, loc_1 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 24, 0)
	store_i32(memory_at_0, loc_5 + 12, loc_1)
	store_i32(memory_at_0, loc_5 + 8, loc_2)
	::continue_at_1::
	reg_0 = add_i32(loc_3, 8)
	return reg_0
end
FUNC_LIST[11] = function(loc_0)
	FUNC_LIST[12](loc_0)
end
FUNC_LIST[12] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	if loc_0 == 0 then
		goto continue_at_1
	end
	loc_1 = add_i32(loc_0, -8)
	loc_2 = load_i32(memory_at_0, add_i32(loc_0, -4))
	loc_0 = band_i32(loc_2, -8)
	loc_3 = add_i32(loc_1, loc_0)
	if band_i32(loc_2, 1) ~= 0 then
		goto continue_at_2
	end
	if band_i32(loc_2, 2) == 0 then
		goto continue_at_1
	end
	loc_4 = load_i32(memory_at_0, loc_1)
	loc_1 = sub_i32(loc_1, loc_4)
	if lt_u32(loc_1, load_i32(memory_at_0, 0 + 4504)) then
		goto continue_at_1
	end
	loc_0 = add_i32(loc_4, loc_0)
	if loc_1 == load_i32(memory_at_0, 0 + 4508) then
		goto continue_at_6
	end
	loc_2 = load_i32(memory_at_0, loc_1 + 12)
	if gt_u32(loc_4, 255) then
		goto continue_at_7
	end
	loc_5 = load_i32(memory_at_0, loc_1 + 8)
	if loc_2 ~= loc_5 then
		goto continue_at_5
	end
	store_i32(memory_at_0, 0 + 4488, band_i32(load_i32(memory_at_0, 0 + 4488), rotl_i32(-2, shr_u32(loc_4, 3))))
	goto continue_at_2
	::continue_at_7::
	loc_6 = load_i32(memory_at_0, loc_1 + 24)
	if loc_2 == loc_1 then
		goto continue_at_8
	end
	loc_4 = load_i32(memory_at_0, loc_1 + 8)
	store_i32(memory_at_0, loc_4 + 12, loc_2)
	store_i32(memory_at_0, loc_2 + 8, loc_4)
	goto continue_at_3
	::continue_at_8::
	loc_4 = load_i32(memory_at_0, loc_1 + 20)
	if loc_4 == 0 then
		goto continue_at_10
	end
	loc_5 = add_i32(loc_1, 20)
	goto continue_at_9
	::continue_at_10::
	loc_4 = load_i32(memory_at_0, loc_1 + 16)
	if loc_4 == 0 then
		goto continue_at_4
	end
	loc_5 = add_i32(loc_1, 16)
	::continue_at_9::
	::continue_at_11::
	while true do
		loc_7 = loc_5
		loc_2 = loc_4
		loc_5 = add_i32(loc_2, 20)
		loc_4 = load_i32(memory_at_0, loc_2 + 20)
		if loc_4 ~= 0 then
			goto continue_at_11
		end
		loc_5 = add_i32(loc_2, 16)
		loc_4 = load_i32(memory_at_0, loc_2 + 16)
		if loc_4 ~= 0 then
			goto continue_at_11
		end
		break
	end
	store_i32(memory_at_0, loc_7, 0)
	goto continue_at_3
	::continue_at_6::
	loc_2 = load_i32(memory_at_0, loc_3 + 4)
	if band_i32(loc_2, 3) ~= 3 then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_3 + 4, band_i32(loc_2, -2))
	store_i32(memory_at_0, 0 + 4496, loc_0)
	store_i32(memory_at_0, loc_3, loc_0)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(loc_0, 1))
	goto continue_at_0
	::continue_at_5::
	store_i32(memory_at_0, loc_2 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 12, loc_2)
	goto continue_at_2
	::continue_at_4::
	loc_2 = 0
	::continue_at_3::
	if loc_6 == 0 then
		goto continue_at_2
	end
	loc_5 = load_i32(memory_at_0, loc_1 + 28)
	loc_4 = add_i32(shl_i32(loc_5, 2), 4792)
	if loc_1 ~= load_i32(memory_at_0, loc_4) then
		goto continue_at_13
	end
	store_i32(memory_at_0, loc_4, loc_2)
	if loc_2 ~= 0 then
		goto continue_at_12
	end
	store_i32(memory_at_0, 0 + 4492, band_i32(load_i32(memory_at_0, 0 + 4492), rotl_i32(-2, loc_5)))
	goto continue_at_2
	::continue_at_13::
	if load_i32(memory_at_0, loc_6 + 16) ~= loc_1 then
		goto continue_at_15
	end
	store_i32(memory_at_0, loc_6 + 16, loc_2)
	goto continue_at_14
	::continue_at_15::
	store_i32(memory_at_0, loc_6 + 20, loc_2)
	::continue_at_14::
	if loc_2 == 0 then
		goto continue_at_2
	end
	::continue_at_12::
	store_i32(memory_at_0, loc_2 + 24, loc_6)
	loc_4 = load_i32(memory_at_0, loc_1 + 16)
	if loc_4 == 0 then
		goto continue_at_16
	end
	store_i32(memory_at_0, loc_2 + 16, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_2)
	::continue_at_16::
	loc_4 = load_i32(memory_at_0, loc_1 + 20)
	if loc_4 == 0 then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_2 + 20, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_2)
	::continue_at_2::
	if ge_u32(loc_1, loc_3) then
		goto continue_at_1
	end
	loc_4 = load_i32(memory_at_0, loc_3 + 4)
	if band_i32(loc_4, 1) == 0 then
		goto continue_at_1
	end
	if band_i32(loc_4, 2) ~= 0 then
		goto continue_at_21
	end
	if loc_3 ~= load_i32(memory_at_0, 0 + 4512) then
		goto continue_at_22
	end
	store_i32(memory_at_0, 0 + 4512, loc_1)
	loc_0 = add_i32(load_i32(memory_at_0, 0 + 4500), loc_0)
	store_i32(memory_at_0, 0 + 4500, loc_0)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(loc_0, 1))
	if loc_1 ~= load_i32(memory_at_0, 0 + 4508) then
		goto continue_at_1
	end
	store_i32(memory_at_0, 0 + 4496, 0)
	store_i32(memory_at_0, 0 + 4508, 0)
	goto continue_at_0
	::continue_at_22::
	loc_6 = load_i32(memory_at_0, 0 + 4508)
	if loc_3 ~= loc_6 then
		goto continue_at_23
	end
	store_i32(memory_at_0, 0 + 4508, loc_1)
	loc_0 = add_i32(load_i32(memory_at_0, 0 + 4496), loc_0)
	store_i32(memory_at_0, 0 + 4496, loc_0)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(loc_0, 1))
	store_i32(memory_at_0, add_i32(loc_1, loc_0), loc_0)
	goto continue_at_0
	::continue_at_23::
	loc_0 = add_i32(band_i32(loc_4, -8), loc_0)
	loc_2 = load_i32(memory_at_0, loc_3 + 12)
	if gt_u32(loc_4, 255) then
		goto continue_at_24
	end
	loc_5 = load_i32(memory_at_0, loc_3 + 8)
	if loc_2 ~= loc_5 then
		goto continue_at_25
	end
	store_i32(memory_at_0, 0 + 4488, band_i32(load_i32(memory_at_0, 0 + 4488), rotl_i32(-2, shr_u32(loc_4, 3))))
	goto continue_at_18
	::continue_at_25::
	store_i32(memory_at_0, loc_2 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 12, loc_2)
	goto continue_at_18
	::continue_at_24::
	loc_8 = load_i32(memory_at_0, loc_3 + 24)
	if loc_2 == loc_3 then
		goto continue_at_26
	end
	loc_4 = load_i32(memory_at_0, loc_3 + 8)
	store_i32(memory_at_0, loc_4 + 12, loc_2)
	store_i32(memory_at_0, loc_2 + 8, loc_4)
	goto continue_at_19
	::continue_at_26::
	loc_4 = load_i32(memory_at_0, loc_3 + 20)
	if loc_4 == 0 then
		goto continue_at_28
	end
	loc_5 = add_i32(loc_3, 20)
	goto continue_at_27
	::continue_at_28::
	loc_4 = load_i32(memory_at_0, loc_3 + 16)
	if loc_4 == 0 then
		goto continue_at_20
	end
	loc_5 = add_i32(loc_3, 16)
	::continue_at_27::
	::continue_at_29::
	while true do
		loc_7 = loc_5
		loc_2 = loc_4
		loc_5 = add_i32(loc_2, 20)
		loc_4 = load_i32(memory_at_0, loc_2 + 20)
		if loc_4 ~= 0 then
			goto continue_at_29
		end
		loc_5 = add_i32(loc_2, 16)
		loc_4 = load_i32(memory_at_0, loc_2 + 16)
		if loc_4 ~= 0 then
			goto continue_at_29
		end
		break
	end
	store_i32(memory_at_0, loc_7, 0)
	goto continue_at_19
	::continue_at_21::
	store_i32(memory_at_0, loc_3 + 4, band_i32(loc_4, -2))
	store_i32(memory_at_0, add_i32(loc_1, loc_0), loc_0)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(loc_0, 1))
	goto continue_at_17
	::continue_at_20::
	loc_2 = 0
	::continue_at_19::
	if loc_8 == 0 then
		goto continue_at_18
	end
	loc_5 = load_i32(memory_at_0, loc_3 + 28)
	loc_4 = add_i32(shl_i32(loc_5, 2), 4792)
	if loc_3 ~= load_i32(memory_at_0, loc_4) then
		goto continue_at_31
	end
	store_i32(memory_at_0, loc_4, loc_2)
	if loc_2 ~= 0 then
		goto continue_at_30
	end
	store_i32(memory_at_0, 0 + 4492, band_i32(load_i32(memory_at_0, 0 + 4492), rotl_i32(-2, loc_5)))
	goto continue_at_18
	::continue_at_31::
	if load_i32(memory_at_0, loc_8 + 16) ~= loc_3 then
		goto continue_at_33
	end
	store_i32(memory_at_0, loc_8 + 16, loc_2)
	goto continue_at_32
	::continue_at_33::
	store_i32(memory_at_0, loc_8 + 20, loc_2)
	::continue_at_32::
	if loc_2 == 0 then
		goto continue_at_18
	end
	::continue_at_30::
	store_i32(memory_at_0, loc_2 + 24, loc_8)
	loc_4 = load_i32(memory_at_0, loc_3 + 16)
	if loc_4 == 0 then
		goto continue_at_34
	end
	store_i32(memory_at_0, loc_2 + 16, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_2)
	::continue_at_34::
	loc_4 = load_i32(memory_at_0, loc_3 + 20)
	if loc_4 == 0 then
		goto continue_at_18
	end
	store_i32(memory_at_0, loc_2 + 20, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_2)
	::continue_at_18::
	store_i32(memory_at_0, add_i32(loc_1, loc_0), loc_0)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(loc_0, 1))
	if loc_1 ~= loc_6 then
		goto continue_at_17
	end
	store_i32(memory_at_0, 0 + 4496, loc_0)
	goto continue_at_0
	::continue_at_17::
	if gt_u32(loc_0, 255) then
		goto continue_at_35
	end
	loc_2 = add_i32(band_i32(loc_0, -8), 4528)
	loc_4 = load_i32(memory_at_0, 0 + 4488)
	loc_0 = shl_i32(1, shr_u32(loc_0, 3))
	if band_i32(loc_4, loc_0) ~= 0 then
		goto continue_at_37
	end
	store_i32(memory_at_0, 0 + 4488, bor_i32(loc_4, loc_0))
	loc_0 = loc_2
	goto continue_at_36
	::continue_at_37::
	loc_0 = load_i32(memory_at_0, loc_2 + 8)
	::continue_at_36::
	store_i32(memory_at_0, loc_0 + 12, loc_1)
	store_i32(memory_at_0, loc_2 + 8, loc_1)
	store_i32(memory_at_0, loc_1 + 12, loc_2)
	store_i32(memory_at_0, loc_1 + 8, loc_0)
	goto continue_at_0
	::continue_at_35::
	loc_2 = 31
	if gt_u32(loc_0, 16777215) then
		goto continue_at_38
	end
	loc_2 = clz_i32(shr_u32(loc_0, 8))
	loc_2 = add_i32(sub_i32(band_i32(shr_u32(loc_0, sub_i32(38, loc_2)), 1), shl_i32(loc_2, 1)), 62)
	::continue_at_38::
	store_i32(memory_at_0, loc_1 + 28, loc_2)
	store_i64(memory_at_0, loc_1 + 16, 0LL)
	loc_5 = add_i32(shl_i32(loc_2, 2), 4792)
	loc_4 = load_i32(memory_at_0, 0 + 4492)
	loc_3 = shl_i32(1, loc_2)
	if band_i32(loc_4, loc_3) ~= 0 then
		goto continue_at_42
	end
	store_i32(memory_at_0, loc_5, loc_1)
	store_i32(memory_at_0, 0 + 4492, bor_i32(loc_4, loc_3))
	loc_0 = 8
	loc_2 = 24
	goto continue_at_41
	::continue_at_42::
	loc_2 = shl_i32(loc_0, (loc_2 == 31 and 0 or sub_i32(25, shr_u32(loc_2, 1))))
	loc_5 = load_i32(memory_at_0, loc_5)
	::continue_at_43::
	while true do
		loc_4 = loc_5
		if band_i32(load_i32(memory_at_0, loc_4 + 4), -8) == loc_0 then
			goto continue_at_40
		end
		loc_5 = shr_u32(loc_2, 29)
		loc_2 = shl_i32(loc_2, 1)
		loc_3 = add_i32(loc_4, band_i32(loc_5, 4))
		loc_5 = load_i32(memory_at_0, loc_3 + 16)
		if loc_5 ~= 0 then
			goto continue_at_43
		end
		break
	end
	store_i32(memory_at_0, add_i32(loc_3, 16), loc_1)
	loc_0 = 8
	loc_2 = 24
	loc_5 = loc_4
	::continue_at_41::
	loc_4 = loc_1
	loc_3 = loc_1
	goto continue_at_39
	::continue_at_40::
	loc_5 = load_i32(memory_at_0, loc_4 + 8)
	store_i32(memory_at_0, loc_5 + 12, loc_1)
	store_i32(memory_at_0, loc_4 + 8, loc_1)
	loc_3 = 0
	loc_0 = 24
	loc_2 = 8
	::continue_at_39::
	store_i32(memory_at_0, add_i32(loc_1, loc_2), loc_5)
	store_i32(memory_at_0, loc_1 + 12, loc_4)
	store_i32(memory_at_0, add_i32(loc_1, loc_0), loc_3)
	loc_1 = add_i32(load_i32(memory_at_0, 0 + 4520), -1)
	store_i32(memory_at_0, 0 + 4520, (loc_1 ~= 0 and loc_1 or -1))
	::continue_at_1::
	::continue_at_0::
end
FUNC_LIST[13] = function(loc_0, loc_1)
	local loc_2 = 0
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	local loc_9 = 0
	local loc_10 = 0
	local loc_11 = 0
	local loc_12 = 0
	local reg_0
	if loc_0 ~= 0 then
		goto continue_at_1
	end
	reg_0 = FUNC_LIST[9](loc_1)
	goto continue_at_0
	::continue_at_1::
	if lt_u32(loc_1, -64) then
		goto continue_at_2
	end
	store_i32(memory_at_0, 0 + 4484, 48)
	reg_0 = 0
	goto continue_at_0
	::continue_at_2::
	loc_2 = (lt_u32(loc_1, 11) and 16 or band_i32(add_i32(loc_1, 19), -16))
	loc_3 = add_i32(loc_0, -4)
	loc_4 = load_i32(memory_at_0, loc_3)
	loc_5 = band_i32(loc_4, -8)
	if band_i32(loc_4, 3) ~= 0 then
		goto continue_at_5
	end
	if lt_u32(loc_2, 256) then
		goto continue_at_4
	end
	if lt_u32(loc_5, bor_i32(loc_2, 4)) then
		goto continue_at_4
	end
	if le_u32(sub_i32(loc_5, loc_2), shl_i32(load_i32(memory_at_0, 0 + 4968), 1)) then
		goto continue_at_3
	end
	goto continue_at_4
	::continue_at_5::
	loc_6 = add_i32(loc_0, -8)
	loc_7 = add_i32(loc_6, loc_5)
	if lt_u32(loc_5, loc_2) then
		goto continue_at_6
	end
	loc_1 = sub_i32(loc_5, loc_2)
	if lt_u32(loc_1, 16) then
		goto continue_at_3
	end
	store_i32(memory_at_0, loc_3, bor_i32(bor_i32(loc_2, band_i32(loc_4, 1)), 2))
	loc_2 = add_i32(loc_6, loc_2)
	store_i32(memory_at_0, loc_2 + 4, bor_i32(loc_1, 3))
	store_i32(memory_at_0, loc_7 + 4, bor_i32(load_i32(memory_at_0, loc_7 + 4), 1))
	FUNC_LIST[14](loc_2, loc_1)
	reg_0 = loc_0
	goto continue_at_0
	::continue_at_6::
	if loc_7 ~= load_i32(memory_at_0, 0 + 4512) then
		goto continue_at_7
	end
	loc_5 = add_i32(load_i32(memory_at_0, 0 + 4500), loc_5)
	if le_u32(loc_5, loc_2) then
		goto continue_at_4
	end
	store_i32(memory_at_0, loc_3, bor_i32(bor_i32(loc_2, band_i32(loc_4, 1)), 2))
	loc_1 = add_i32(loc_6, loc_2)
	store_i32(memory_at_0, 0 + 4512, loc_1)
	loc_2 = sub_i32(loc_5, loc_2)
	store_i32(memory_at_0, 0 + 4500, loc_2)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(loc_2, 1))
	reg_0 = loc_0
	goto continue_at_0
	::continue_at_7::
	if loc_7 ~= load_i32(memory_at_0, 0 + 4508) then
		goto continue_at_8
	end
	loc_5 = add_i32(load_i32(memory_at_0, 0 + 4496), loc_5)
	if lt_u32(loc_5, loc_2) then
		goto continue_at_4
	end
	loc_1 = sub_i32(loc_5, loc_2)
	if lt_u32(loc_1, 16) then
		goto continue_at_10
	end
	store_i32(memory_at_0, loc_3, bor_i32(bor_i32(loc_2, band_i32(loc_4, 1)), 2))
	loc_2 = add_i32(loc_6, loc_2)
	store_i32(memory_at_0, loc_2 + 4, bor_i32(loc_1, 1))
	loc_5 = add_i32(loc_6, loc_5)
	store_i32(memory_at_0, loc_5, loc_1)
	store_i32(memory_at_0, loc_5 + 4, band_i32(load_i32(memory_at_0, loc_5 + 4), -2))
	goto continue_at_9
	::continue_at_10::
	store_i32(memory_at_0, loc_3, bor_i32(bor_i32(band_i32(loc_4, 1), loc_5), 2))
	loc_1 = add_i32(loc_6, loc_5)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(load_i32(memory_at_0, loc_1 + 4), 1))
	loc_1 = 0
	loc_2 = 0
	::continue_at_9::
	store_i32(memory_at_0, 0 + 4508, loc_2)
	store_i32(memory_at_0, 0 + 4496, loc_1)
	reg_0 = loc_0
	goto continue_at_0
	::continue_at_8::
	loc_8 = load_i32(memory_at_0, loc_7 + 4)
	if band_i32(loc_8, 2) ~= 0 then
		goto continue_at_4
	end
	loc_9 = add_i32(band_i32(loc_8, -8), loc_5)
	if lt_u32(loc_9, loc_2) then
		goto continue_at_4
	end
	loc_10 = sub_i32(loc_9, loc_2)
	loc_1 = load_i32(memory_at_0, loc_7 + 12)
	if gt_u32(loc_8, 255) then
		goto continue_at_12
	end
	loc_5 = load_i32(memory_at_0, loc_7 + 8)
	if loc_1 ~= loc_5 then
		goto continue_at_13
	end
	store_i32(memory_at_0, 0 + 4488, band_i32(load_i32(memory_at_0, 0 + 4488), rotl_i32(-2, shr_u32(loc_8, 3))))
	goto continue_at_11
	::continue_at_13::
	store_i32(memory_at_0, loc_1 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 12, loc_1)
	goto continue_at_11
	::continue_at_12::
	loc_11 = load_i32(memory_at_0, loc_7 + 24)
	if loc_1 == loc_7 then
		goto continue_at_15
	end
	loc_5 = load_i32(memory_at_0, loc_7 + 8)
	store_i32(memory_at_0, loc_5 + 12, loc_1)
	store_i32(memory_at_0, loc_1 + 8, loc_5)
	goto continue_at_14
	::continue_at_15::
	loc_5 = load_i32(memory_at_0, loc_7 + 20)
	if loc_5 == 0 then
		goto continue_at_18
	end
	loc_8 = add_i32(loc_7, 20)
	goto continue_at_17
	::continue_at_18::
	loc_5 = load_i32(memory_at_0, loc_7 + 16)
	if loc_5 == 0 then
		goto continue_at_16
	end
	loc_8 = add_i32(loc_7, 16)
	::continue_at_17::
	::continue_at_19::
	while true do
		loc_12 = loc_8
		loc_1 = loc_5
		loc_8 = add_i32(loc_1, 20)
		loc_5 = load_i32(memory_at_0, loc_1 + 20)
		if loc_5 ~= 0 then
			goto continue_at_19
		end
		loc_8 = add_i32(loc_1, 16)
		loc_5 = load_i32(memory_at_0, loc_1 + 16)
		if loc_5 ~= 0 then
			goto continue_at_19
		end
		break
	end
	store_i32(memory_at_0, loc_12, 0)
	goto continue_at_14
	::continue_at_16::
	loc_1 = 0
	::continue_at_14::
	if loc_11 == 0 then
		goto continue_at_11
	end
	loc_8 = load_i32(memory_at_0, loc_7 + 28)
	loc_5 = add_i32(shl_i32(loc_8, 2), 4792)
	if loc_7 ~= load_i32(memory_at_0, loc_5) then
		goto continue_at_21
	end
	store_i32(memory_at_0, loc_5, loc_1)
	if loc_1 ~= 0 then
		goto continue_at_20
	end
	store_i32(memory_at_0, 0 + 4492, band_i32(load_i32(memory_at_0, 0 + 4492), rotl_i32(-2, loc_8)))
	goto continue_at_11
	::continue_at_21::
	if load_i32(memory_at_0, loc_11 + 16) ~= loc_7 then
		goto continue_at_23
	end
	store_i32(memory_at_0, loc_11 + 16, loc_1)
	goto continue_at_22
	::continue_at_23::
	store_i32(memory_at_0, loc_11 + 20, loc_1)
	::continue_at_22::
	if loc_1 == 0 then
		goto continue_at_11
	end
	::continue_at_20::
	store_i32(memory_at_0, loc_1 + 24, loc_11)
	loc_5 = load_i32(memory_at_0, loc_7 + 16)
	if loc_5 == 0 then
		goto continue_at_24
	end
	store_i32(memory_at_0, loc_1 + 16, loc_5)
	store_i32(memory_at_0, loc_5 + 24, loc_1)
	::continue_at_24::
	loc_5 = load_i32(memory_at_0, loc_7 + 20)
	if loc_5 == 0 then
		goto continue_at_11
	end
	store_i32(memory_at_0, loc_1 + 20, loc_5)
	store_i32(memory_at_0, loc_5 + 24, loc_1)
	::continue_at_11::
	if gt_u32(loc_10, 15) then
		goto continue_at_25
	end
	store_i32(memory_at_0, loc_3, bor_i32(bor_i32(band_i32(loc_4, 1), loc_9), 2))
	loc_1 = add_i32(loc_6, loc_9)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(load_i32(memory_at_0, loc_1 + 4), 1))
	reg_0 = loc_0
	goto continue_at_0
	::continue_at_25::
	store_i32(memory_at_0, loc_3, bor_i32(bor_i32(loc_2, band_i32(loc_4, 1)), 2))
	loc_1 = add_i32(loc_6, loc_2)
	store_i32(memory_at_0, loc_1 + 4, bor_i32(loc_10, 3))
	loc_2 = add_i32(loc_6, loc_9)
	store_i32(memory_at_0, loc_2 + 4, bor_i32(load_i32(memory_at_0, loc_2 + 4), 1))
	FUNC_LIST[14](loc_1, loc_10)
	reg_0 = loc_0
	goto continue_at_0
	::continue_at_4::
	reg_0 = FUNC_LIST[9](loc_1)
	loc_2 = reg_0
	if loc_2 ~= 0 then
		goto continue_at_26
	end
	reg_0 = 0
	goto continue_at_0
	::continue_at_26::
	loc_5 = load_i32(memory_at_0, loc_3)
	loc_5 = add_i32((band_i32(loc_5, 3) ~= 0 and -4 or -8), band_i32(loc_5, -8))
	loc_1 = (lt_u32(loc_5, loc_1) and loc_5 or loc_1)
	if loc_1 == 0 then
		goto continue_at_27
	end
	rt.store.copy(memory_at_0, loc_2, memory_at_0, loc_0, loc_1)
	::continue_at_27::
	FUNC_LIST[12](loc_0)
	loc_0 = loc_2
	::continue_at_3::
	reg_0 = loc_0
	::continue_at_0::
	return reg_0
end
FUNC_LIST[14] = function(loc_0, loc_1)
	local loc_2 = 0
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	loc_2 = add_i32(loc_0, loc_1)
	loc_3 = load_i32(memory_at_0, loc_0 + 4)
	if band_i32(loc_3, 1) ~= 0 then
		goto continue_at_2
	end
	if band_i32(loc_3, 2) == 0 then
		goto continue_at_1
	end
	loc_4 = load_i32(memory_at_0, loc_0)
	loc_1 = add_i32(loc_4, loc_1)
	loc_0 = sub_i32(loc_0, loc_4)
	if loc_0 == load_i32(memory_at_0, 0 + 4508) then
		goto continue_at_6
	end
	loc_3 = load_i32(memory_at_0, loc_0 + 12)
	if gt_u32(loc_4, 255) then
		goto continue_at_7
	end
	loc_5 = load_i32(memory_at_0, loc_0 + 8)
	if loc_3 ~= loc_5 then
		goto continue_at_5
	end
	store_i32(memory_at_0, 0 + 4488, band_i32(load_i32(memory_at_0, 0 + 4488), rotl_i32(-2, shr_u32(loc_4, 3))))
	goto continue_at_2
	::continue_at_7::
	loc_6 = load_i32(memory_at_0, loc_0 + 24)
	if loc_3 == loc_0 then
		goto continue_at_8
	end
	loc_4 = load_i32(memory_at_0, loc_0 + 8)
	store_i32(memory_at_0, loc_4 + 12, loc_3)
	store_i32(memory_at_0, loc_3 + 8, loc_4)
	goto continue_at_3
	::continue_at_8::
	loc_4 = load_i32(memory_at_0, loc_0 + 20)
	if loc_4 == 0 then
		goto continue_at_10
	end
	loc_5 = add_i32(loc_0, 20)
	goto continue_at_9
	::continue_at_10::
	loc_4 = load_i32(memory_at_0, loc_0 + 16)
	if loc_4 == 0 then
		goto continue_at_4
	end
	loc_5 = add_i32(loc_0, 16)
	::continue_at_9::
	::continue_at_11::
	while true do
		loc_7 = loc_5
		loc_3 = loc_4
		loc_5 = add_i32(loc_3, 20)
		loc_4 = load_i32(memory_at_0, loc_3 + 20)
		if loc_4 ~= 0 then
			goto continue_at_11
		end
		loc_5 = add_i32(loc_3, 16)
		loc_4 = load_i32(memory_at_0, loc_3 + 16)
		if loc_4 ~= 0 then
			goto continue_at_11
		end
		break
	end
	store_i32(memory_at_0, loc_7, 0)
	goto continue_at_3
	::continue_at_6::
	loc_3 = load_i32(memory_at_0, loc_2 + 4)
	if band_i32(loc_3, 3) ~= 3 then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_2 + 4, band_i32(loc_3, -2))
	store_i32(memory_at_0, 0 + 4496, loc_1)
	store_i32(memory_at_0, loc_2, loc_1)
	store_i32(memory_at_0, loc_0 + 4, bor_i32(loc_1, 1))
	goto continue_at_0
	::continue_at_5::
	store_i32(memory_at_0, loc_3 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 12, loc_3)
	goto continue_at_2
	::continue_at_4::
	loc_3 = 0
	::continue_at_3::
	if loc_6 == 0 then
		goto continue_at_2
	end
	loc_5 = load_i32(memory_at_0, loc_0 + 28)
	loc_4 = add_i32(shl_i32(loc_5, 2), 4792)
	if loc_0 ~= load_i32(memory_at_0, loc_4) then
		goto continue_at_13
	end
	store_i32(memory_at_0, loc_4, loc_3)
	if loc_3 ~= 0 then
		goto continue_at_12
	end
	store_i32(memory_at_0, 0 + 4492, band_i32(load_i32(memory_at_0, 0 + 4492), rotl_i32(-2, loc_5)))
	goto continue_at_2
	::continue_at_13::
	if load_i32(memory_at_0, loc_6 + 16) ~= loc_0 then
		goto continue_at_15
	end
	store_i32(memory_at_0, loc_6 + 16, loc_3)
	goto continue_at_14
	::continue_at_15::
	store_i32(memory_at_0, loc_6 + 20, loc_3)
	::continue_at_14::
	if loc_3 == 0 then
		goto continue_at_2
	end
	::continue_at_12::
	store_i32(memory_at_0, loc_3 + 24, loc_6)
	loc_4 = load_i32(memory_at_0, loc_0 + 16)
	if loc_4 == 0 then
		goto continue_at_16
	end
	store_i32(memory_at_0, loc_3 + 16, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_3)
	::continue_at_16::
	loc_4 = load_i32(memory_at_0, loc_0 + 20)
	if loc_4 == 0 then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_3 + 20, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_3)
	::continue_at_2::
	loc_4 = load_i32(memory_at_0, loc_2 + 4)
	if band_i32(loc_4, 2) ~= 0 then
		goto continue_at_21
	end
	if loc_2 ~= load_i32(memory_at_0, 0 + 4512) then
		goto continue_at_22
	end
	store_i32(memory_at_0, 0 + 4512, loc_0)
	loc_1 = add_i32(load_i32(memory_at_0, 0 + 4500), loc_1)
	store_i32(memory_at_0, 0 + 4500, loc_1)
	store_i32(memory_at_0, loc_0 + 4, bor_i32(loc_1, 1))
	if loc_0 ~= load_i32(memory_at_0, 0 + 4508) then
		goto continue_at_1
	end
	store_i32(memory_at_0, 0 + 4496, 0)
	store_i32(memory_at_0, 0 + 4508, 0)
	goto continue_at_0
	::continue_at_22::
	loc_6 = load_i32(memory_at_0, 0 + 4508)
	if loc_2 ~= loc_6 then
		goto continue_at_23
	end
	store_i32(memory_at_0, 0 + 4508, loc_0)
	loc_1 = add_i32(load_i32(memory_at_0, 0 + 4496), loc_1)
	store_i32(memory_at_0, 0 + 4496, loc_1)
	store_i32(memory_at_0, loc_0 + 4, bor_i32(loc_1, 1))
	store_i32(memory_at_0, add_i32(loc_0, loc_1), loc_1)
	goto continue_at_0
	::continue_at_23::
	loc_1 = add_i32(band_i32(loc_4, -8), loc_1)
	loc_3 = load_i32(memory_at_0, loc_2 + 12)
	if gt_u32(loc_4, 255) then
		goto continue_at_24
	end
	loc_5 = load_i32(memory_at_0, loc_2 + 8)
	if loc_3 ~= loc_5 then
		goto continue_at_25
	end
	store_i32(memory_at_0, 0 + 4488, band_i32(load_i32(memory_at_0, 0 + 4488), rotl_i32(-2, shr_u32(loc_4, 3))))
	goto continue_at_18
	::continue_at_25::
	store_i32(memory_at_0, loc_3 + 8, loc_5)
	store_i32(memory_at_0, loc_5 + 12, loc_3)
	goto continue_at_18
	::continue_at_24::
	loc_8 = load_i32(memory_at_0, loc_2 + 24)
	if loc_3 == loc_2 then
		goto continue_at_26
	end
	loc_4 = load_i32(memory_at_0, loc_2 + 8)
	store_i32(memory_at_0, loc_4 + 12, loc_3)
	store_i32(memory_at_0, loc_3 + 8, loc_4)
	goto continue_at_19
	::continue_at_26::
	loc_4 = load_i32(memory_at_0, loc_2 + 20)
	if loc_4 == 0 then
		goto continue_at_28
	end
	loc_5 = add_i32(loc_2, 20)
	goto continue_at_27
	::continue_at_28::
	loc_4 = load_i32(memory_at_0, loc_2 + 16)
	if loc_4 == 0 then
		goto continue_at_20
	end
	loc_5 = add_i32(loc_2, 16)
	::continue_at_27::
	::continue_at_29::
	while true do
		loc_7 = loc_5
		loc_3 = loc_4
		loc_5 = add_i32(loc_3, 20)
		loc_4 = load_i32(memory_at_0, loc_3 + 20)
		if loc_4 ~= 0 then
			goto continue_at_29
		end
		loc_5 = add_i32(loc_3, 16)
		loc_4 = load_i32(memory_at_0, loc_3 + 16)
		if loc_4 ~= 0 then
			goto continue_at_29
		end
		break
	end
	store_i32(memory_at_0, loc_7, 0)
	goto continue_at_19
	::continue_at_21::
	store_i32(memory_at_0, loc_2 + 4, band_i32(loc_4, -2))
	store_i32(memory_at_0, add_i32(loc_0, loc_1), loc_1)
	store_i32(memory_at_0, loc_0 + 4, bor_i32(loc_1, 1))
	goto continue_at_17
	::continue_at_20::
	loc_3 = 0
	::continue_at_19::
	if loc_8 == 0 then
		goto continue_at_18
	end
	loc_5 = load_i32(memory_at_0, loc_2 + 28)
	loc_4 = add_i32(shl_i32(loc_5, 2), 4792)
	if loc_2 ~= load_i32(memory_at_0, loc_4) then
		goto continue_at_31
	end
	store_i32(memory_at_0, loc_4, loc_3)
	if loc_3 ~= 0 then
		goto continue_at_30
	end
	store_i32(memory_at_0, 0 + 4492, band_i32(load_i32(memory_at_0, 0 + 4492), rotl_i32(-2, loc_5)))
	goto continue_at_18
	::continue_at_31::
	if load_i32(memory_at_0, loc_8 + 16) ~= loc_2 then
		goto continue_at_33
	end
	store_i32(memory_at_0, loc_8 + 16, loc_3)
	goto continue_at_32
	::continue_at_33::
	store_i32(memory_at_0, loc_8 + 20, loc_3)
	::continue_at_32::
	if loc_3 == 0 then
		goto continue_at_18
	end
	::continue_at_30::
	store_i32(memory_at_0, loc_3 + 24, loc_8)
	loc_4 = load_i32(memory_at_0, loc_2 + 16)
	if loc_4 == 0 then
		goto continue_at_34
	end
	store_i32(memory_at_0, loc_3 + 16, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_3)
	::continue_at_34::
	loc_4 = load_i32(memory_at_0, loc_2 + 20)
	if loc_4 == 0 then
		goto continue_at_18
	end
	store_i32(memory_at_0, loc_3 + 20, loc_4)
	store_i32(memory_at_0, loc_4 + 24, loc_3)
	::continue_at_18::
	store_i32(memory_at_0, add_i32(loc_0, loc_1), loc_1)
	store_i32(memory_at_0, loc_0 + 4, bor_i32(loc_1, 1))
	if loc_0 ~= loc_6 then
		goto continue_at_17
	end
	store_i32(memory_at_0, 0 + 4496, loc_1)
	goto continue_at_0
	::continue_at_17::
	if gt_u32(loc_1, 255) then
		goto continue_at_35
	end
	loc_3 = add_i32(band_i32(loc_1, -8), 4528)
	loc_4 = load_i32(memory_at_0, 0 + 4488)
	loc_1 = shl_i32(1, shr_u32(loc_1, 3))
	if band_i32(loc_4, loc_1) ~= 0 then
		goto continue_at_37
	end
	store_i32(memory_at_0, 0 + 4488, bor_i32(loc_4, loc_1))
	loc_1 = loc_3
	goto continue_at_36
	::continue_at_37::
	loc_1 = load_i32(memory_at_0, loc_3 + 8)
	::continue_at_36::
	store_i32(memory_at_0, loc_1 + 12, loc_0)
	store_i32(memory_at_0, loc_3 + 8, loc_0)
	store_i32(memory_at_0, loc_0 + 12, loc_3)
	store_i32(memory_at_0, loc_0 + 8, loc_1)
	goto continue_at_0
	::continue_at_35::
	loc_3 = 31
	if gt_u32(loc_1, 16777215) then
		goto continue_at_38
	end
	loc_3 = clz_i32(shr_u32(loc_1, 8))
	loc_3 = add_i32(sub_i32(band_i32(shr_u32(loc_1, sub_i32(38, loc_3)), 1), shl_i32(loc_3, 1)), 62)
	::continue_at_38::
	store_i32(memory_at_0, loc_0 + 28, loc_3)
	store_i64(memory_at_0, loc_0 + 16, 0LL)
	loc_4 = add_i32(shl_i32(loc_3, 2), 4792)
	loc_5 = load_i32(memory_at_0, 0 + 4492)
	loc_2 = shl_i32(1, loc_3)
	if band_i32(loc_5, loc_2) ~= 0 then
		goto continue_at_39
	end
	store_i32(memory_at_0, loc_4, loc_0)
	store_i32(memory_at_0, 0 + 4492, bor_i32(loc_5, loc_2))
	store_i32(memory_at_0, loc_0 + 24, loc_4)
	store_i32(memory_at_0, loc_0 + 8, loc_0)
	store_i32(memory_at_0, loc_0 + 12, loc_0)
	goto continue_at_0
	::continue_at_39::
	loc_3 = shl_i32(loc_1, (loc_3 == 31 and 0 or sub_i32(25, shr_u32(loc_3, 1))))
	loc_5 = load_i32(memory_at_0, loc_4)
	::continue_at_41::
	while true do
		loc_4 = loc_5
		if band_i32(load_i32(memory_at_0, loc_4 + 4), -8) == loc_1 then
			goto continue_at_40
		end
		loc_5 = shr_u32(loc_3, 29)
		loc_3 = shl_i32(loc_3, 1)
		loc_2 = add_i32(loc_4, band_i32(loc_5, 4))
		loc_5 = load_i32(memory_at_0, loc_2 + 16)
		if loc_5 ~= 0 then
			goto continue_at_41
		end
		break
	end
	store_i32(memory_at_0, add_i32(loc_2, 16), loc_0)
	store_i32(memory_at_0, loc_0 + 24, loc_4)
	store_i32(memory_at_0, loc_0 + 12, loc_0)
	store_i32(memory_at_0, loc_0 + 8, loc_0)
	goto continue_at_0
	::continue_at_40::
	loc_1 = load_i32(memory_at_0, loc_4 + 8)
	store_i32(memory_at_0, loc_1 + 12, loc_0)
	store_i32(memory_at_0, loc_4 + 8, loc_0)
	store_i32(memory_at_0, loc_0 + 24, 0)
	store_i32(memory_at_0, loc_0 + 12, loc_4)
	store_i32(memory_at_0, loc_0 + 8, loc_1)
	::continue_at_1::
	::continue_at_0::
end
FUNC_LIST[15] = function(loc_0)
	local reg_0
	reg_0 = FUNC_LIST[0](loc_0)
	reg_0 = band_i32(reg_0, 65535)
	return reg_0
end
FUNC_LIST[16] = function(loc_0, loc_1)
	local reg_0
	reg_0 = FUNC_LIST[1](loc_0, loc_1)
	reg_0 = band_i32(reg_0, 65535)
	return reg_0
end
FUNC_LIST[17] = function(loc_0, loc_1, loc_2, loc_3)
	local reg_0
	reg_0 = FUNC_LIST[2](loc_0, loc_1, loc_2, loc_3)
	reg_0 = band_i32(reg_0, 65535)
	return reg_0
end
FUNC_LIST[18] = function(loc_0, loc_1, loc_2, loc_3)
	local reg_0
	reg_0 = FUNC_LIST[3](loc_0, loc_1, loc_2, loc_3)
	reg_0 = band_i32(reg_0, 65535)
	return reg_0
end
FUNC_LIST[19] = function(loc_0, loc_1, loc_2, loc_3)
	local reg_0
	reg_0 = FUNC_LIST[4](loc_0, loc_1, loc_2, loc_3)
	reg_0 = band_i32(reg_0, 65535)
	return reg_0
end
FUNC_LIST[20] = function(loc_0)
	FUNC_LIST[5](loc_0)
	error("out of code bounds")
end
FUNC_LIST[21] = function()
	error("out of code bounds")
end
FUNC_LIST[22] = function(loc_0)
	local reg_0
	if loc_0 ~= 0 then
		goto continue_at_1
	end
	reg_0 = shl_i32(memory_at_0.min, 16)
	goto continue_at_0
	::continue_at_1::
	if band_i32(loc_0, 65535) ~= 0 then
		goto continue_at_2
	end
	if loc_0 <= -1 then
		goto continue_at_2
	end
	reg_0 = rt.allocator.grow(memory_at_0, shr_u32(loc_0, 16))
	loc_0 = reg_0
	if loc_0 ~= -1 then
		goto continue_at_3
	end
	store_i32(memory_at_0, 0 + 4484, 48)
	reg_0 = -1
	goto continue_at_0
	::continue_at_3::
	reg_0 = shl_i32(loc_0, 16)
	goto continue_at_0
	::continue_at_2::
	FUNC_LIST[21]()
	error("out of code bounds")
	::continue_at_0::
	return reg_0
end
FUNC_LIST[23] = function()
end
FUNC_LIST[24] = function()
	FUNC_LIST[23]()
	FUNC_LIST[37]()
end
FUNC_LIST[25] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local loc_3 = 0
	local reg_0
	loc_1 = loc_0
	if band_i32(loc_0, 3) == 0 then
		goto continue_at_2
	end
	if load_i32_u8(memory_at_0, loc_0) ~= 0 then
		goto continue_at_3
	end
	reg_0 = sub_i32(loc_0, loc_0)
	goto continue_at_0
	::continue_at_3::
	loc_1 = add_i32(loc_0, 1)
	if band_i32(loc_1, 3) == 0 then
		goto continue_at_2
	end
	if load_i32_u8(memory_at_0, loc_1) == 0 then
		goto continue_at_1
	end
	loc_1 = add_i32(loc_0, 2)
	if band_i32(loc_1, 3) == 0 then
		goto continue_at_2
	end
	if load_i32_u8(memory_at_0, loc_1) == 0 then
		goto continue_at_1
	end
	loc_1 = add_i32(loc_0, 3)
	if band_i32(loc_1, 3) == 0 then
		goto continue_at_2
	end
	if load_i32_u8(memory_at_0, loc_1) == 0 then
		goto continue_at_1
	end
	loc_1 = add_i32(loc_0, 4)
	if band_i32(loc_1, 3) ~= 0 then
		goto continue_at_1
	end
	::continue_at_2::
	loc_2 = add_i32(loc_1, -4)
	loc_1 = add_i32(loc_1, -5)
	::continue_at_4::
	while true do
		loc_1 = add_i32(loc_1, 4)
		loc_2 = add_i32(loc_2, 4)
		loc_3 = load_i32(memory_at_0, loc_2)
		if band_i32(bor_i32(sub_i32(16843008, loc_3), loc_3), -2139062144) == -2139062144 then
			goto continue_at_4
		end
		break
	end
	::continue_at_5::
	while true do
		loc_1 = add_i32(loc_1, 1)
		loc_3 = load_i32_u8(memory_at_0, loc_2)
		loc_2 = add_i32(loc_2, 1)
		if loc_3 ~= 0 then
			goto continue_at_5
		end
		break
	end
	::continue_at_1::
	reg_0 = sub_i32(loc_1, loc_0)
	::continue_at_0::
	return reg_0
end
FUNC_LIST[26] = function()
end
FUNC_LIST[27] = function(loc_0)
	local reg_0
	FUNC_LIST[26]()
	reg_0 = FUNC_LIST[15](loc_0)
	loc_0 = reg_0
	if loc_0 ~= 0 then
		goto continue_at_1
	end
	reg_0 = 0
	goto continue_at_0
	::continue_at_1::
	store_i32(memory_at_0, 0 + 4484, loc_0)
	reg_0 = -1
	::continue_at_0::
	return reg_0
end
FUNC_LIST[28] = function(loc_0)
	local reg_0
	reg_0 = FUNC_LIST[27](load_i32(memory_at_0, loc_0 + 56))
	return reg_0
end
FUNC_LIST[29] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local reg_0
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_3
	loc_4 = -1
	if loc_2 > -1 then
		goto continue_at_2
	end
	store_i32(memory_at_0, 0 + 4484, 28)
	goto continue_at_1
	::continue_at_2::
	reg_0 = FUNC_LIST[19](loc_0, loc_1, loc_2, add_i32(loc_3, 12))
	loc_2 = reg_0
	if loc_2 == 0 then
		goto continue_at_3
	end
	store_i32(memory_at_0, 0 + 4484, loc_2)
	loc_4 = -1
	goto continue_at_1
	::continue_at_3::
	loc_4 = load_i32(memory_at_0, loc_3 + 12)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 16)
	reg_0 = loc_4
	return reg_0
end
FUNC_LIST[30] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	local loc_9 = 0
	local reg_0
	local reg_1
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_3
	store_i32(memory_at_0, loc_3 + 12, loc_2)
	store_i32(memory_at_0, loc_3 + 8, loc_1)
	loc_1 = load_i32(memory_at_0, loc_0 + 24)
	store_i32(memory_at_0, loc_3, loc_1)
	loc_4 = sub_i32(load_i32(memory_at_0, loc_0 + 20), loc_1)
	store_i32(memory_at_0, loc_3 + 4, loc_4)
	loc_5 = 2
	reg_0 = FUNC_LIST[29](load_i32(memory_at_0, loc_0 + 56), loc_3, 2)
	loc_1 = reg_0
	loc_6 = add_i32(loc_4, loc_2)
	if loc_1 == loc_6 then
		goto continue_at_2
	end
	loc_4 = loc_3
	::continue_at_3::
	while true do
		if loc_1 > -1 then
			goto continue_at_4
		end
		loc_1 = 0
		store_i32(memory_at_0, loc_0 + 24, 0)
		store_i64(memory_at_0, loc_0 + 16, 0LL)
		store_i32(memory_at_0, loc_0, bor_i32(load_i32(memory_at_0, loc_0), 32))
		if loc_5 == 2 then
			goto continue_at_1
		end
		loc_1 = sub_i32(loc_2, load_i32(memory_at_0, loc_4 + 4))
		goto continue_at_1
		::continue_at_4::
		loc_7 = load_i32(memory_at_0, loc_4 + 4)
		loc_8 = (gt_u32(loc_1, loc_7) and 1 or 0)
		loc_9 = add_i32(loc_4, shl_i32(loc_8, 3))
		loc_7 = sub_i32(loc_1, (loc_8 ~= 0 and loc_7 or 0))
		store_i32(memory_at_0, loc_9, add_i32(load_i32(memory_at_0, loc_9), loc_7))
		loc_4 = add_i32(loc_4, (loc_8 ~= 0 and 12 or 4))
		store_i32(memory_at_0, loc_4, sub_i32(load_i32(memory_at_0, loc_4), loc_7))
		loc_4 = loc_9
		loc_6 = sub_i32(loc_6, loc_1)
		loc_5 = sub_i32(loc_5, loc_8)
		reg_1 = FUNC_LIST[29](load_i32(memory_at_0, loc_0 + 56), loc_9, loc_5)
		loc_1 = reg_1
		if loc_6 ~= loc_1 then
			goto continue_at_3
		end
		break
	end
	::continue_at_2::
	loc_1 = load_i32(memory_at_0, loc_0 + 40)
	store_i32(memory_at_0, loc_0 + 24, loc_1)
	store_i32(memory_at_0, loc_0 + 20, loc_1)
	store_i32(memory_at_0, loc_0 + 16, add_i32(loc_1, load_i32(memory_at_0, loc_0 + 44)))
	loc_1 = loc_2
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 16)
	reg_0 = loc_1
	return reg_0
end
FUNC_LIST[31] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local reg_0
	loc_1 = sub_i32(GLOBAL_LIST[0].value, 32)
	GLOBAL_LIST[0].value = loc_1
	reg_0 = FUNC_LIST[16](loc_0, add_i32(loc_1, 8))
	loc_0 = reg_0
	if loc_0 ~= 0 then
		goto continue_at_2
	end
	loc_0 = 59
	if load_i32_u8(memory_at_0, loc_1 + 8) ~= 2 then
		goto continue_at_2
	end
	if band_i32(load_i32_u8(memory_at_0, loc_1 + 16), 36) ~= 0 then
		goto continue_at_2
	end
	loc_2 = 1
	goto continue_at_1
	::continue_at_2::
	loc_2 = 0
	store_i32(memory_at_0, 0 + 4484, loc_0)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_1, 32)
	reg_0 = loc_2
	return reg_0
end
FUNC_LIST[32] = function(loc_0, loc_1, loc_2)
	local reg_0
	store_i32(memory_at_0, loc_0 + 32, 1)
	if band_i32(load_i32_u8(memory_at_0, loc_0), 64) ~= 0 then
		goto continue_at_1
	end
	reg_0 = FUNC_LIST[31](load_i32(memory_at_0, loc_0 + 56))
	if reg_0 ~= 0 then
		goto continue_at_1
	end
	store_i32(memory_at_0, loc_0 + 64, -1)
	::continue_at_1::
	reg_0 = FUNC_LIST[30](loc_0, loc_1, loc_2)
	return reg_0
end
FUNC_LIST[33] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local reg_0
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_3
	reg_0 = FUNC_LIST[18](loc_0, loc_1, band_i32(loc_2, 255), add_i32(loc_3, 8))
	loc_2 = reg_0
	if loc_2 == 0 then
		goto continue_at_2
	end
	store_i32(memory_at_0, 0 + 4484, (loc_2 == 76 and 70 or loc_2))
	loc_1 = -1LL
	goto continue_at_1
	::continue_at_2::
	loc_1 = load_i64(memory_at_0, loc_3 + 8)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 16)
	reg_0 = loc_1
	return reg_0
end
FUNC_LIST[34] = function(loc_0, loc_1, loc_2)
	local reg_0
	reg_0 = FUNC_LIST[33](load_i32(memory_at_0, loc_0 + 56), loc_1, loc_2)
	return reg_0
end
FUNC_LIST[35] = function()
	local reg_0
	reg_0 = 6024
	return reg_0
end
FUNC_LIST[36] = function()
end
FUNC_LIST[37] = function()
	local loc_0 = 0
	local loc_1 = 0
	local loc_2 = 0
	local reg_0
	reg_0 = FUNC_LIST[35]()
	loc_0 = load_i32(memory_at_0, reg_0)
	if loc_0 == 0 then
		goto continue_at_1
	end
	::continue_at_2::
	while true do
		if load_i32(memory_at_0, loc_0 + 20) == load_i32(memory_at_0, loc_0 + 24) then
			goto continue_at_3
		end
		reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
		::continue_at_3::
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		loc_2 = load_i32(memory_at_0, loc_0 + 8)
		if loc_1 == loc_2 then
			goto continue_at_4
		end
		reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 36)](loc_0, extend_i64_i32(sub_i32(loc_1, loc_2)), 1)
		::continue_at_4::
		loc_0 = load_i32(memory_at_0, loc_0 + 52)
		if loc_0 ~= 0 then
			goto continue_at_2
		end
		break
	end
	::continue_at_1::
	loc_0 = load_i32(memory_at_0, 0 + 4336)
	if loc_0 == 0 then
		goto continue_at_5
	end
	if load_i32(memory_at_0, loc_0 + 20) == load_i32(memory_at_0, loc_0 + 24) then
		goto continue_at_6
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
	::continue_at_6::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	loc_2 = load_i32(memory_at_0, loc_0 + 8)
	if loc_1 == loc_2 then
		goto continue_at_5
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 36)](loc_0, extend_i64_i32(sub_i32(loc_1, loc_2)), 1)
	::continue_at_5::
	loc_0 = load_i32(memory_at_0, 0 + 4096)
	if loc_0 == 0 then
		goto continue_at_7
	end
	if load_i32(memory_at_0, loc_0 + 20) == load_i32(memory_at_0, loc_0 + 24) then
		goto continue_at_8
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
	::continue_at_8::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	loc_2 = load_i32(memory_at_0, loc_0 + 8)
	if loc_1 == loc_2 then
		goto continue_at_7
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 36)](loc_0, extend_i64_i32(sub_i32(loc_1, loc_2)), 1)
	::continue_at_7::
	loc_0 = load_i32(memory_at_0, 0 + 4216)
	if loc_0 == 0 then
		goto continue_at_9
	end
	if load_i32(memory_at_0, loc_0 + 20) == load_i32(memory_at_0, loc_0 + 24) then
		goto continue_at_10
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
	::continue_at_10::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	loc_2 = load_i32(memory_at_0, loc_0 + 8)
	if loc_1 == loc_2 then
		goto continue_at_9
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 36)](loc_0, extend_i64_i32(sub_i32(loc_1, loc_2)), 1)
	::continue_at_9::
end
FUNC_LIST[38] = function(loc_0)
	local loc_1 = 0
	local reg_0
	loc_1 = load_i32(memory_at_0, loc_0 + 60)
	store_i32(memory_at_0, loc_0 + 60, bor_i32(add_i32(loc_1, -1), loc_1))
	loc_1 = load_i32(memory_at_0, loc_0)
	if band_i32(loc_1, 8) == 0 then
		goto continue_at_1
	end
	store_i32(memory_at_0, loc_0, bor_i32(loc_1, 32))
	reg_0 = -1
	goto continue_at_0
	::continue_at_1::
	store_i64(memory_at_0, loc_0 + 4, 0LL)
	loc_1 = load_i32(memory_at_0, loc_0 + 40)
	store_i32(memory_at_0, loc_0 + 24, loc_1)
	store_i32(memory_at_0, loc_0 + 20, loc_1)
	store_i32(memory_at_0, loc_0 + 16, add_i32(loc_1, load_i32(memory_at_0, loc_0 + 44)))
	reg_0 = 0
	::continue_at_0::
	return reg_0
end
FUNC_LIST[39] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local reg_0
	loc_3 = load_i32(memory_at_0, loc_2 + 16)
	if loc_3 ~= 0 then
		goto continue_at_2
	end
	loc_4 = 0
	reg_0 = FUNC_LIST[38](loc_2)
	if reg_0 ~= 0 then
		goto continue_at_1
	end
	loc_3 = load_i32(memory_at_0, loc_2 + 16)
	::continue_at_2::
	loc_5 = load_i32(memory_at_0, loc_2 + 20)
	if le_u32(loc_1, sub_i32(loc_3, loc_5)) then
		goto continue_at_3
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_2 + 32)](loc_2, loc_0, loc_1)
	goto continue_at_0
	::continue_at_3::
	loc_6 = 0
	if load_i32(memory_at_0, loc_2 + 64) < 0 then
		goto continue_at_4
	end
	if loc_1 == 0 then
		goto continue_at_4
	end
	loc_4 = add_i32(loc_0, loc_1)
	loc_3 = 0
	::continue_at_6::
	while true do
		if load_i32_u8(memory_at_0, add_i32(add_i32(loc_4, loc_3), -1)) == 10 then
			goto continue_at_5
		end
		loc_3 = add_i32(loc_3, -1)
		if add_i32(loc_1, loc_3) ~= 0 then
			goto continue_at_6
		end
		break
	end
	loc_6 = 0
	goto continue_at_4
	::continue_at_5::
	loc_6 = add_i32(loc_1, loc_3)
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_2 + 32)](loc_2, loc_0, loc_6)
	loc_4 = reg_0
	if lt_u32(loc_4, loc_6) then
		goto continue_at_1
	end
	loc_0 = add_i32(loc_6, loc_0)
	loc_1 = sub_i32(0, loc_3)
	loc_5 = load_i32(memory_at_0, loc_2 + 20)
	::continue_at_4::
	if loc_1 == 0 then
		goto continue_at_7
	end
	rt.store.copy(memory_at_0, loc_5, memory_at_0, loc_0, loc_1)
	::continue_at_7::
	store_i32(memory_at_0, loc_2 + 20, add_i32(load_i32(memory_at_0, loc_2 + 20), loc_1))
	loc_4 = add_i32(loc_6, loc_1)
	::continue_at_1::
	reg_0 = loc_4
	::continue_at_0::
	return reg_0
end
FUNC_LIST[40] = function(loc_0, loc_1, loc_2, loc_3)
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	local reg_0
	loc_4 = mul_i32(loc_2, loc_1)
	loc_5 = load_i32(memory_at_0, loc_3 + 16)
	if loc_5 ~= 0 then
		goto continue_at_2
	end
	loc_6 = 0
	reg_0 = FUNC_LIST[38](loc_3)
	if reg_0 ~= 0 then
		goto continue_at_1
	end
	loc_5 = load_i32(memory_at_0, loc_3 + 16)
	::continue_at_2::
	loc_7 = load_i32(memory_at_0, loc_3 + 20)
	if le_u32(loc_4, sub_i32(loc_5, loc_7)) then
		goto continue_at_3
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_3 + 32)](loc_3, loc_0, loc_4)
	loc_6 = reg_0
	goto continue_at_1
	::continue_at_3::
	loc_8 = 0
	if loc_4 ~= 0 then
		goto continue_at_5
	end
	loc_5 = loc_4
	goto continue_at_4
	::continue_at_5::
	loc_5 = 0
	if load_i32(memory_at_0, loc_3 + 64) >= 0 then
		goto continue_at_6
	end
	loc_5 = loc_4
	goto continue_at_4
	::continue_at_6::
	loc_6 = add_i32(loc_0, loc_4)
	::continue_at_8::
	while true do
		if load_i32_u8(memory_at_0, add_i32(add_i32(loc_6, loc_5), -1)) == 10 then
			goto continue_at_7
		end
		loc_5 = add_i32(loc_5, -1)
		if add_i32(loc_4, loc_5) ~= 0 then
			goto continue_at_8
		end
		break
	end
	loc_8 = 0
	loc_5 = loc_4
	goto continue_at_4
	::continue_at_7::
	loc_8 = add_i32(loc_4, loc_5)
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_3 + 32)](loc_3, loc_0, loc_8)
	loc_6 = reg_0
	if lt_u32(loc_6, loc_8) then
		goto continue_at_1
	end
	loc_0 = add_i32(loc_8, loc_0)
	loc_5 = sub_i32(0, loc_5)
	loc_7 = load_i32(memory_at_0, loc_3 + 20)
	::continue_at_4::
	if loc_5 == 0 then
		goto continue_at_9
	end
	rt.store.copy(memory_at_0, loc_7, memory_at_0, loc_0, loc_5)
	::continue_at_9::
	store_i32(memory_at_0, loc_3 + 20, add_i32(load_i32(memory_at_0, loc_3 + 20), loc_5))
	loc_6 = add_i32(loc_8, loc_5)
	::continue_at_1::
	if loc_6 ~= loc_4 then
		goto continue_at_10
	end
	reg_0 = (loc_1 ~= 0 and loc_2 or 0)
	goto continue_at_0
	::continue_at_10::
	reg_0 = div_u32(loc_6, loc_1)
	::continue_at_0::
	return reg_0
end
FUNC_LIST[41] = function(loc_0, loc_1)
	local reg_0
	reg_0 = loc_0
	return reg_0
end
FUNC_LIST[42] = function(loc_0, loc_1)
	local reg_0
	reg_0 = FUNC_LIST[41](loc_0, loc_1)
	return reg_0
end
FUNC_LIST[43] = function(loc_0)
	local loc_1 = 0
	local reg_0
	loc_1 = load_i32(memory_at_0, 0 + 6052)
	if loc_1 ~= 0 then
		goto continue_at_1
	end
	loc_1 = 6028
	store_i32(memory_at_0, 0 + 6052, 6028)
	::continue_at_1::
	reg_0 = FUNC_LIST[42](add_i32(load_i32_u16(memory_at_0, add_i32(shl_i32((gt_u32(loc_0, 76) and 0 or loc_0), 1), 2592)), 1028), load_i32(memory_at_0, loc_1 + 20))
	return reg_0
end
FUNC_LIST[44] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local reg_0
	loc_3 = (loc_2 ~= 0 and 1 or 0)
	if band_i32(loc_0, 3) == 0 then
		goto continue_at_4
	end
	if loc_2 == 0 then
		goto continue_at_4
	end
	if load_i32_u8(memory_at_0, loc_0) ~= band_i32(loc_1, 255) then
		goto continue_at_5
	end
	loc_4 = loc_0
	loc_5 = loc_2
	goto continue_at_2
	::continue_at_5::
	loc_5 = add_i32(loc_2, -1)
	loc_3 = (loc_5 ~= 0 and 1 or 0)
	loc_4 = add_i32(loc_0, 1)
	if band_i32(loc_4, 3) == 0 then
		goto continue_at_3
	end
	if loc_5 == 0 then
		goto continue_at_3
	end
	if load_i32_u8(memory_at_0, loc_4) == band_i32(loc_1, 255) then
		goto continue_at_2
	end
	loc_5 = add_i32(loc_2, -2)
	loc_3 = (loc_5 ~= 0 and 1 or 0)
	loc_4 = add_i32(loc_0, 2)
	if band_i32(loc_4, 3) == 0 then
		goto continue_at_3
	end
	if loc_5 == 0 then
		goto continue_at_3
	end
	if load_i32_u8(memory_at_0, loc_4) == band_i32(loc_1, 255) then
		goto continue_at_2
	end
	loc_5 = add_i32(loc_2, -3)
	loc_3 = (loc_5 ~= 0 and 1 or 0)
	loc_4 = add_i32(loc_0, 3)
	if band_i32(loc_4, 3) == 0 then
		goto continue_at_3
	end
	if loc_5 == 0 then
		goto continue_at_3
	end
	if load_i32_u8(memory_at_0, loc_4) == band_i32(loc_1, 255) then
		goto continue_at_2
	end
	loc_4 = add_i32(loc_0, 4)
	loc_5 = add_i32(loc_2, -4)
	loc_3 = (loc_5 ~= 0 and 1 or 0)
	goto continue_at_3
	::continue_at_4::
	loc_5 = loc_2
	loc_4 = loc_0
	::continue_at_3::
	if loc_3 == 0 then
		goto continue_at_1
	end
	if load_i32_u8(memory_at_0, loc_4) == band_i32(loc_1, 255) then
		goto continue_at_6
	end
	if lt_u32(loc_5, 4) then
		goto continue_at_6
	end
	loc_0 = mul_i32(band_i32(loc_1, 255), 16843009)
	::continue_at_7::
	while true do
		loc_2 = bxor_i32(load_i32(memory_at_0, loc_4), loc_0)
		if band_i32(bor_i32(sub_i32(16843008, loc_2), loc_2), -2139062144) ~= -2139062144 then
			goto continue_at_2
		end
		loc_4 = add_i32(loc_4, 4)
		loc_5 = add_i32(loc_5, -4)
		if gt_u32(loc_5, 3) then
			goto continue_at_7
		end
		break
	end
	::continue_at_6::
	if loc_5 == 0 then
		goto continue_at_1
	end
	::continue_at_2::
	loc_2 = band_i32(loc_1, 255)
	::continue_at_8::
	while true do
		if load_i32_u8(memory_at_0, loc_4) ~= loc_2 then
			goto continue_at_9
		end
		reg_0 = loc_4
		goto continue_at_0
		::continue_at_9::
		loc_4 = add_i32(loc_4, 1)
		loc_5 = add_i32(loc_5, -1)
		if loc_5 ~= 0 then
			goto continue_at_8
		end
		break
	end
	::continue_at_1::
	reg_0 = 0
	::continue_at_0::
	return reg_0
end
FUNC_LIST[45] = function(loc_0, loc_1)
	local loc_2 = 0
	local reg_0
	reg_0 = FUNC_LIST[44](loc_0, 0, loc_1)
	loc_2 = reg_0
	reg_0 = (loc_2 ~= 0 and sub_i32(loc_2, loc_0) or loc_1)
	return reg_0
end
FUNC_LIST[46] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local reg_0
	loc_3 = 1
	if loc_0 == 0 then
		goto continue_at_1
	end
	if gt_u32(loc_1, 127) then
		goto continue_at_2
	end
	store_i32_n8(memory_at_0, loc_0, loc_1)
	reg_0 = 1
	goto continue_at_0
	::continue_at_2::
	loc_3 = load_i32(memory_at_0, 0 + 6052)
	if loc_3 ~= 0 then
		goto continue_at_3
	end
	loc_3 = 6028
	store_i32(memory_at_0, 0 + 6052, 6028)
	::continue_at_3::
	if load_i32(memory_at_0, loc_3) ~= 0 then
		goto continue_at_5
	end
	if band_i32(loc_1, -128) == 57216 then
		goto continue_at_6
	end
	store_i32(memory_at_0, 0 + 4484, 25)
	goto continue_at_4
	::continue_at_6::
	store_i32_n8(memory_at_0, loc_0, loc_1)
	reg_0 = 1
	goto continue_at_0
	::continue_at_5::
	if gt_u32(loc_1, 2047) then
		goto continue_at_7
	end
	store_i32_n8(memory_at_0, loc_0 + 1, bor_i32(band_i32(loc_1, 63), 128))
	store_i32_n8(memory_at_0, loc_0, bor_i32(shr_u32(loc_1, 6), 192))
	reg_0 = 2
	goto continue_at_0
	::continue_at_7::
	if lt_u32(loc_1, 55296) then
		goto continue_at_9
	end
	if band_i32(loc_1, -8192) ~= 57344 then
		goto continue_at_8
	end
	::continue_at_9::
	store_i32_n8(memory_at_0, loc_0 + 2, bor_i32(band_i32(loc_1, 63), 128))
	store_i32_n8(memory_at_0, loc_0, bor_i32(shr_u32(loc_1, 12), 224))
	store_i32_n8(memory_at_0, loc_0 + 1, bor_i32(band_i32(shr_u32(loc_1, 6), 63), 128))
	reg_0 = 3
	goto continue_at_0
	::continue_at_8::
	if gt_u32(add_i32(loc_1, -65536), 1048575) then
		goto continue_at_10
	end
	store_i32_n8(memory_at_0, loc_0 + 3, bor_i32(band_i32(loc_1, 63), 128))
	store_i32_n8(memory_at_0, loc_0, bor_i32(shr_u32(loc_1, 18), 240))
	store_i32_n8(memory_at_0, loc_0 + 2, bor_i32(band_i32(shr_u32(loc_1, 6), 63), 128))
	store_i32_n8(memory_at_0, loc_0 + 1, bor_i32(band_i32(shr_u32(loc_1, 12), 63), 128))
	reg_0 = 4
	goto continue_at_0
	::continue_at_10::
	store_i32(memory_at_0, 0 + 4484, 25)
	::continue_at_4::
	loc_3 = -1
	::continue_at_1::
	reg_0 = loc_3
	::continue_at_0::
	return reg_0
end
FUNC_LIST[47] = function(loc_0, loc_1)
	local reg_0
	if loc_0 ~= 0 then
		goto continue_at_1
	end
	reg_0 = 0
	goto continue_at_0
	::continue_at_1::
	reg_0 = FUNC_LIST[46](loc_0, loc_1, 0)
	::continue_at_0::
	return reg_0
end
FUNC_LIST[48] = function(loc_0, loc_1)
	local loc_2 = 0LL
	local loc_3 = 0
	local reg_0
	loc_2 = reinterpret_i64_f64(loc_0)
	loc_3 = band_i32(wrap_i32_i64(shr_u64(loc_2, 52LL)), 2047)
	if loc_3 == 2047 then
		goto continue_at_1
	end
	if loc_3 ~= 0 then
		goto continue_at_2
	end
	if loc_0 ~= 0e0 then
		goto continue_at_3
	end
	store_i32(memory_at_0, loc_1, 0)
	reg_0 = loc_0
	goto continue_at_0
	::continue_at_3::
	reg_0 = FUNC_LIST[48]((loc_0 * 1.8446744073709552e19), loc_1)
	loc_0 = reg_0
	store_i32(memory_at_0, loc_1, add_i32(load_i32(memory_at_0, loc_1), -64))
	reg_0 = loc_0
	goto continue_at_0
	::continue_at_2::
	store_i32(memory_at_0, loc_1, add_i32(loc_3, -1022))
	loc_0 = reinterpret_f64_i64(bor_i64(band_i64(loc_2, -9218868437227405313LL), 4602678819172646912LL))
	::continue_at_1::
	reg_0 = loc_0
	::continue_at_0::
	return reg_0
end
FUNC_LIST[49] = function(loc_0, loc_1)
	local loc_2 = 0
	local reg_0
	local reg_1
	local reg_2
	local reg_3
	reg_0 = FUNC_LIST[25](loc_0)
	loc_2 = reg_0
	reg_3 = FUNC_LIST[40](loc_0, 1, loc_2, loc_1)
	reg_0 = (loc_2 ~= reg_3 and -1 or 0)
	return reg_0
end
FUNC_LIST[50] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local reg_0
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 208)
	GLOBAL_LIST[0].value = loc_3
	store_i32(memory_at_0, loc_3 + 204, loc_2)
	store_i64(memory_at_0, add_i32(add_i32(loc_3, 160), 32), 0LL)
	store_i64(memory_at_0, add_i32(loc_3, 184), 0LL)
	store_i64(memory_at_0, add_i32(loc_3, 176), 0LL)
	store_i64(memory_at_0, loc_3 + 168, 0LL)
	store_i64(memory_at_0, loc_3 + 160, 0LL)
	store_i32(memory_at_0, loc_3 + 200, loc_2)
	reg_0 = FUNC_LIST[51](0, loc_1, add_i32(loc_3, 200), add_i32(loc_3, 80), add_i32(loc_3, 160))
	if reg_0 >= 0 then
		goto continue_at_2
	end
	loc_0 = -1
	goto continue_at_1
	::continue_at_2::
	loc_4 = load_i32(memory_at_0, loc_0)
	store_i32(memory_at_0, loc_0, band_i32(loc_4, -33))
	if load_i32(memory_at_0, loc_0 + 44) ~= 0 then
		goto continue_at_6
	end
	store_i32(memory_at_0, loc_0 + 44, 80)
	store_i32(memory_at_0, loc_0 + 24, 0)
	store_i64(memory_at_0, loc_0 + 16, 0LL)
	loc_5 = load_i32(memory_at_0, loc_0 + 40)
	store_i32(memory_at_0, loc_0 + 40, loc_3)
	goto continue_at_5
	::continue_at_6::
	loc_5 = 0
	if load_i32(memory_at_0, loc_0 + 16) ~= 0 then
		goto continue_at_4
	end
	::continue_at_5::
	loc_2 = -1
	reg_0 = FUNC_LIST[38](loc_0)
	if reg_0 ~= 0 then
		goto continue_at_3
	end
	::continue_at_4::
	reg_0 = FUNC_LIST[51](loc_0, loc_1, add_i32(loc_3, 200), add_i32(loc_3, 80), add_i32(loc_3, 160))
	loc_2 = reg_0
	::continue_at_3::
	loc_1 = band_i32(loc_4, 32)
	if loc_5 == 0 then
		goto continue_at_7
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
	store_i32(memory_at_0, loc_0 + 44, 0)
	store_i32(memory_at_0, loc_0 + 40, loc_5)
	store_i32(memory_at_0, loc_0 + 24, 0)
	loc_5 = load_i32(memory_at_0, loc_0 + 20)
	store_i64(memory_at_0, loc_0 + 16, 0LL)
	loc_2 = (loc_5 ~= 0 and loc_2 or -1)
	::continue_at_7::
	loc_5 = load_i32(memory_at_0, loc_0)
	store_i32(memory_at_0, loc_0, bor_i32(loc_5, loc_1))
	loc_0 = (band_i32(loc_5, 32) ~= 0 and -1 or loc_2)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 208)
	reg_0 = loc_0
	return reg_0
end
FUNC_LIST[51] = function(loc_0, loc_1, loc_2, loc_3, loc_4)
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local loc_8 = 0
	local loc_9 = 0
	local loc_10 = 0
	local loc_11 = 0
	local loc_12 = 0
	local loc_13 = 0
	local loc_14 = 0
	local loc_15 = 0
	local loc_16 = 0
	local loc_17 = 0
	local loc_18 = 0
	local loc_19 = 0
	local loc_20 = 0
	local loc_21 = 0
	local loc_22 = 0
	local loc_23 = 0
	local loc_24 = 0
	local loc_25 = 0
	local loc_26 = 0
	local loc_27 = 0
	local loc_28 = 0
	local loc_29 = 0
	local loc_30 = 0LL
	local loc_31 = 0LL
	local loc_32 = 0.0
	local loc_33 = 0
	local loc_34 = 0
	local loc_35 = 0
	local loc_36 = 0
	local loc_37 = 0
	local loc_38 = 0LL
	local loc_39 = 0
	local loc_40 = 0
	local loc_41 = 0.0
	local reg_0
	local reg_1
	local br_map, temp = {}, nil
	loc_5 = sub_i32(GLOBAL_LIST[0].value, 864)
	GLOBAL_LIST[0].value = loc_5
	loc_6 = add_i32(add_i32(loc_5, 52), 12)
	loc_7 = add_i32(add_i32(loc_5, 96), -4)
	loc_8 = add_i32(loc_5, 39)
	loc_9 = add_i32(add_i32(loc_5, 52), 11)
	loc_10 = add_i32(add_i32(loc_5, 64), -1)
	loc_11 = bor_i32(add_i32(loc_5, 64), 8)
	loc_12 = bor_i32(add_i32(loc_5, 64), 9)
	loc_13 = add_i32(add_i32(loc_5, 52), 10)
	loc_14 = add_i32(loc_5, 40)
	loc_15 = 0
	loc_16 = 0
	::continue_at_3::
	while true do
		loc_17 = 0
		::continue_at_5::
		while true do
			loc_18 = loc_1
			if loc_17 > bxor_i32(loc_16, 2147483647) then
				goto continue_at_4
			end
			loc_16 = add_i32(loc_17, loc_16)
			loc_17 = load_i32_u8(memory_at_0, loc_18)
			if loc_17 == 0 then
				goto continue_at_15
			end
			loc_1 = loc_18
			::continue_at_16::
			while true do
				loc_17 = band_i32(loc_17, 255)
				if loc_17 == 0 then
					goto continue_at_19
				end
				if loc_17 ~= 37 then
					goto continue_at_17
				end
				loc_17 = loc_1
				::continue_at_20::
				while true do
					if load_i32_u8(memory_at_0, add_i32(loc_1, 1)) ~= 37 then
						goto continue_at_18
					end
					loc_17 = add_i32(loc_17, 1)
					loc_1 = add_i32(loc_1, 2)
					if load_i32_u8(memory_at_0, loc_1) == 37 then
						goto continue_at_20
					end
					goto continue_at_18
				end
				::continue_at_19::
				loc_17 = loc_1
				::continue_at_18::
				loc_17 = sub_i32(loc_17, loc_18)
				loc_19 = bxor_i32(loc_16, 2147483647)
				if loc_17 > loc_19 then
					goto continue_at_4
				end
				if loc_0 == 0 then
					goto continue_at_21
				end
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_21
				end
				reg_0 = FUNC_LIST[39](loc_18, loc_17, loc_0)
				::continue_at_21::
				if loc_17 ~= 0 then
					goto continue_at_5
				end
				loc_20 = add_i32(loc_1, 1)
				loc_21 = -1
				loc_22 = load_i32_i8(memory_at_0, loc_1 + 1)
				loc_17 = add_i32(loc_22, -48)
				if gt_u32(loc_17, 9) then
					goto continue_at_22
				end
				if load_i32_u8(memory_at_0, loc_1 + 2) ~= 36 then
					goto continue_at_22
				end
				loc_20 = add_i32(loc_1, 3)
				loc_22 = load_i32_i8(memory_at_0, loc_1 + 3)
				loc_15 = 1
				loc_21 = loc_17
				::continue_at_22::
				loc_23 = 0
				loc_1 = add_i32(loc_22, -32)
				if le_u32(loc_1, 31) then
					goto continue_at_24
				end
				loc_1 = loc_20
				goto continue_at_23
				::continue_at_24::
				loc_17 = shl_i32(1, loc_1)
				if band_i32(loc_17, 75913) ~= 0 then
					goto continue_at_25
				end
				loc_1 = loc_20
				goto continue_at_23
				::continue_at_25::
				loc_20 = add_i32(loc_20, 1)
				loc_23 = 0
				::continue_at_26::
				while true do
					loc_23 = bor_i32(loc_17, loc_23)
					loc_1 = loc_20
					loc_22 = load_i32_i8(memory_at_0, loc_1)
					loc_17 = add_i32(loc_22, -32)
					if ge_u32(loc_17, 32) then
						goto continue_at_23
					end
					loc_20 = add_i32(loc_1, 1)
					loc_17 = shl_i32(1, loc_17)
					if band_i32(loc_17, 75913) ~= 0 then
						goto continue_at_26
					end
					break
				end
				::continue_at_23::
				if loc_22 ~= 42 then
					goto continue_at_27
				end
				loc_17 = add_i32(load_i32_i8(memory_at_0, loc_1 + 1), -48)
				if gt_u32(loc_17, 9) then
					goto continue_at_29
				end
				if load_i32_u8(memory_at_0, loc_1 + 2) ~= 36 then
					goto continue_at_29
				end
				if loc_0 ~= 0 then
					goto continue_at_31
				end
				store_i32(memory_at_0, add_i32(loc_4, shl_i32(loc_17, 2)), 10)
				loc_24 = 0
				goto continue_at_30
				::continue_at_31::
				loc_24 = load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_17, 3)))
				::continue_at_30::
				loc_1 = add_i32(loc_1, 3)
				loc_15 = 1
				goto continue_at_28
				::continue_at_29::
				if loc_15 ~= 0 then
					goto continue_at_13
				end
				loc_1 = add_i32(loc_1, 1)
				if loc_0 ~= 0 then
					goto continue_at_32
				end
				loc_15 = 0
				loc_24 = 0
				goto continue_at_14
				::continue_at_32::
				loc_17 = load_i32(memory_at_0, loc_2)
				store_i32(memory_at_0, loc_2, add_i32(loc_17, 4))
				loc_24 = load_i32(memory_at_0, loc_17)
				loc_15 = 0
				::continue_at_28::
				if loc_24 > -1 then
					goto continue_at_14
				end
				loc_24 = sub_i32(0, loc_24)
				loc_23 = bor_i32(loc_23, 8192)
				goto continue_at_14
				::continue_at_27::
				loc_24 = 0
				loc_20 = add_i32(loc_22, -48)
				if gt_u32(loc_20, 9) then
					goto continue_at_14
				end
				loc_17 = loc_1
				::continue_at_33::
				while true do
					if gt_u32(loc_24, 214748364) then
						goto continue_at_34
					end
					loc_1 = mul_i32(loc_24, 10)
					loc_22 = (gt_u32(loc_20, bxor_i32(loc_1, 2147483647)) and 1 or 0)
					loc_24 = (loc_22 ~= 0 and -1 or add_i32(loc_1, loc_20))
					loc_20 = load_i32_i8(memory_at_0, loc_17 + 1)
					loc_1 = add_i32(loc_17, 1)
					loc_17 = loc_1
					loc_20 = add_i32(loc_20, -48)
					if lt_u32(loc_20, 10) then
						goto continue_at_33
					end
					if loc_22 ~= 0 then
						goto continue_at_4
					end
					goto continue_at_14
					::continue_at_34::
					loc_1 = load_i32_i8(memory_at_0, loc_17 + 1)
					loc_24 = -1
					loc_17 = add_i32(loc_17, 1)
					loc_20 = add_i32(loc_1, -48)
					if lt_u32(loc_20, 10) then
						goto continue_at_33
					end
					goto continue_at_4
				end
				::continue_at_17::
				loc_1 = add_i32(loc_1, 1)
				loc_17 = load_i32_u8(memory_at_0, loc_1)
				goto continue_at_16
			end
			::continue_at_15::
			if loc_0 ~= 0 then
				goto continue_at_1
			end
			if loc_15 ~= 0 then
				goto continue_at_35
			end
			loc_16 = 0
			goto continue_at_1
			::continue_at_35::
			loc_1 = load_i32(memory_at_0, loc_4 + 4)
			if loc_1 ~= 0 then
				goto continue_at_38
			end
			loc_1 = 1
			goto continue_at_37
			::continue_at_38::
			FUNC_LIST[52](add_i32(loc_3, 8), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 8)
			if loc_1 ~= 0 then
				goto continue_at_39
			end
			loc_1 = 2
			goto continue_at_37
			::continue_at_39::
			FUNC_LIST[52](add_i32(loc_3, 16), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 12)
			if loc_1 ~= 0 then
				goto continue_at_40
			end
			loc_1 = 3
			goto continue_at_37
			::continue_at_40::
			FUNC_LIST[52](add_i32(loc_3, 24), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 16)
			if loc_1 ~= 0 then
				goto continue_at_41
			end
			loc_1 = 4
			goto continue_at_37
			::continue_at_41::
			FUNC_LIST[52](add_i32(loc_3, 32), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 20)
			if loc_1 ~= 0 then
				goto continue_at_42
			end
			loc_1 = 5
			goto continue_at_37
			::continue_at_42::
			FUNC_LIST[52](add_i32(loc_3, 40), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 24)
			if loc_1 ~= 0 then
				goto continue_at_43
			end
			loc_1 = 6
			goto continue_at_37
			::continue_at_43::
			FUNC_LIST[52](add_i32(loc_3, 48), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 28)
			if loc_1 ~= 0 then
				goto continue_at_44
			end
			loc_1 = 7
			goto continue_at_37
			::continue_at_44::
			FUNC_LIST[52](add_i32(loc_3, 56), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 32)
			if loc_1 ~= 0 then
				goto continue_at_45
			end
			loc_1 = 8
			goto continue_at_37
			::continue_at_45::
			FUNC_LIST[52](add_i32(loc_3, 64), loc_1, loc_2)
			loc_1 = load_i32(memory_at_0, loc_4 + 36)
			if loc_1 ~= 0 then
				goto continue_at_36
			end
			loc_1 = 9
			::continue_at_37::
			loc_1 = shl_i32(loc_1, 2)
			::continue_at_46::
			while true do
				if load_i32(memory_at_0, add_i32(loc_4, loc_1)) ~= 0 then
					goto continue_at_13
				end
				loc_1 = add_i32(loc_1, 4)
				if loc_1 ~= 40 then
					goto continue_at_46
				end
				break
			end
			loc_16 = 1
			goto continue_at_1
			::continue_at_36::
			FUNC_LIST[52](add_i32(loc_3, 72), loc_1, loc_2)
			loc_16 = 1
			goto continue_at_1
			::continue_at_14::
			loc_17 = 0
			if load_i32_u8(memory_at_0, loc_1) == 46 then
				goto continue_at_48
			end
			loc_22 = -1
			loc_25 = 0
			goto continue_at_47
			::continue_at_48::
			loc_20 = load_i32_i8(memory_at_0, loc_1 + 1)
			if loc_20 ~= 42 then
				goto continue_at_49
			end
			loc_20 = add_i32(load_i32_i8(memory_at_0, loc_1 + 2), -48)
			if gt_u32(loc_20, 9) then
				goto continue_at_50
			end
			if load_i32_u8(memory_at_0, loc_1 + 3) ~= 36 then
				goto continue_at_50
			end
			if loc_0 ~= 0 then
				goto continue_at_51
			end
			store_i32(memory_at_0, add_i32(loc_4, shl_i32(loc_20, 2)), 10)
			loc_22 = 0
			loc_1 = add_i32(loc_1, 4)
			loc_25 = (0 > -1 and 1 or 0)
			goto continue_at_47
			::continue_at_51::
			loc_1 = add_i32(loc_1, 4)
			loc_22 = load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_20, 3)))
			loc_25 = (loc_22 > -1 and 1 or 0)
			goto continue_at_47
			::continue_at_50::
			if loc_15 ~= 0 then
				goto continue_at_13
			end
			loc_1 = add_i32(loc_1, 2)
			if loc_0 ~= 0 then
				goto continue_at_52
			end
			loc_22 = 0
			loc_25 = (0 > -1 and 1 or 0)
			goto continue_at_47
			::continue_at_52::
			loc_20 = load_i32(memory_at_0, loc_2)
			store_i32(memory_at_0, loc_2, add_i32(loc_20, 4))
			loc_22 = load_i32(memory_at_0, loc_20)
			loc_25 = (loc_22 > -1 and 1 or 0)
			goto continue_at_47
			::continue_at_49::
			loc_1 = add_i32(loc_1, 1)
			loc_26 = add_i32(loc_20, -48)
			if le_u32(loc_26, 9) then
				goto continue_at_53
			end
			loc_25 = 1
			loc_22 = 0
			goto continue_at_47
			::continue_at_53::
			loc_20 = 0
			::continue_at_54::
			while true do
				loc_22 = -1
				if gt_u32(loc_20, 214748364) then
					goto continue_at_55
				end
				loc_20 = mul_i32(loc_20, 10)
				loc_22 = (gt_u32(loc_26, bxor_i32(loc_20, 2147483647)) and -1 or add_i32(loc_20, loc_26))
				::continue_at_55::
				loc_25 = 1
				loc_20 = loc_22
				loc_1 = add_i32(loc_1, 1)
				loc_26 = add_i32(load_i32_i8(memory_at_0, loc_1), -48)
				if lt_u32(loc_26, 10) then
					goto continue_at_54
				end
				break
			end
			::continue_at_47::
			::continue_at_56::
			while true do
				loc_20 = loc_17
				loc_17 = load_i32_i8(memory_at_0, loc_1)
				if lt_u32(add_i32(loc_17, -123), -58) then
					goto continue_at_13
				end
				loc_1 = add_i32(loc_1, 1)
				loc_17 = load_i32_u8(memory_at_0, add_i32(add_i32(loc_17, mul_i32(loc_20, 58)), 2927))
				if lt_u32(band_i32(add_i32(loc_17, -1), 255), 8) then
					goto continue_at_56
				end
				break
			end
			if loc_17 == 27 then
				goto continue_at_58
			end
			if loc_17 == 0 then
				goto continue_at_13
			end
			if loc_21 < 0 then
				goto continue_at_59
			end
			if loc_0 ~= 0 then
				goto continue_at_60
			end
			store_i32(memory_at_0, add_i32(loc_4, shl_i32(loc_21, 2)), loc_17)
			goto continue_at_3
			::continue_at_60::
			store_i64(memory_at_0, loc_5 + 40, load_i64(memory_at_0, add_i32(loc_3, shl_i32(loc_21, 3))))
			goto continue_at_57
			::continue_at_59::
			if loc_0 ~= 0 then
				goto continue_at_61
			end
			loc_16 = 0
			goto continue_at_1
			::continue_at_61::
			FUNC_LIST[52](add_i32(loc_5, 40), loc_17, loc_2)
			goto continue_at_57
			::continue_at_58::
			if loc_21 > -1 then
				goto continue_at_13
			end
			loc_17 = 0
			if loc_0 == 0 then
				goto continue_at_5
			end
			::continue_at_57::
			loc_21 = load_i32(memory_at_0, loc_0)
			if band_i32(loc_21, 32) ~= 0 then
				goto continue_at_2
			end
			loc_26 = band_i32(loc_23, -65537)
			loc_27 = (band_i32(loc_23, 8192) ~= 0 and loc_26 or loc_23)
			loc_23 = load_i32_u8(memory_at_0, add_i32(loc_1, -1))
			loc_17 = extend_i32_n8(loc_23)
			loc_28 = (loc_20 ~= 0 and (band_i32(loc_23, 15) == 3 and band_i32(loc_17, -45) or loc_17) or loc_17)
			if not br_map[1] then
				br_map[1] = (function()
					return { [0] = 17, 19, 12, 19, 17, 17, 17, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 13, 19, 19, 19, 19, 3, 19, 19, 19, 19, 19, 19, 19, 19, 17, 19, 8, 5, 17, 17, 17, 19, 5, 19, 19, 19, 9, 1, 4, 2, 19, 19, 10, 19, 0, 19, 19, 3, }
				end)()
			end
			temp = br_map[1][add_i32(loc_28, -65)] or 19
			if temp < 8 then
				if temp < 3 then
					if temp < 1 then
						goto continue_at_79
					elseif temp > 1 then
						goto continue_at_77
					else
						goto continue_at_78
					end
				elseif temp > 3 then
					if temp < 5 then
						goto continue_at_75
					else
						goto continue_at_74
					end
				else
					goto continue_at_76
				end
			elseif temp > 8 then
				if temp < 13 then
					if temp < 10 then
						goto continue_at_70
					elseif temp > 10 then
						goto continue_at_67
					else
						goto continue_at_69
					end
				elseif temp > 13 then
					if temp < 19 then
						goto continue_at_62
					else
						goto continue_at_12
					end
				else
					goto continue_at_66
				end
			else
				goto continue_at_71
			end
			::continue_at_79::
			loc_21 = 0
			loc_29 = 2746
			loc_30 = load_i64(memory_at_0, loc_5 + 40)
			goto continue_at_73
			::continue_at_78::
			loc_17 = 0
			if not br_map[2] then
				br_map[2] = (function()
					return { [0] = 0, 1, 2, 3, 4, 31, 5, 6, }
				end)()
			end
			temp = br_map[2][loc_20] or 31
			if temp < 4 then
				if temp < 2 then
					if temp < 1 then
						goto continue_at_86
					else
						goto continue_at_85
					end
				elseif temp > 2 then
					goto continue_at_83
				else
					goto continue_at_84
				end
			elseif temp > 4 then
				if temp < 6 then
					goto continue_at_81
				elseif temp > 6 then
					goto continue_at_5
				else
					goto continue_at_80
				end
			else
				goto continue_at_82
			end
			::continue_at_86::
			store_i32(memory_at_0, load_i32(memory_at_0, loc_5 + 40), loc_16)
			goto continue_at_5
			::continue_at_85::
			store_i32(memory_at_0, load_i32(memory_at_0, loc_5 + 40), loc_16)
			goto continue_at_5
			::continue_at_84::
			store_i64(memory_at_0, load_i32(memory_at_0, loc_5 + 40), extend_i64_i32(loc_16))
			goto continue_at_5
			::continue_at_83::
			store_i32_n16(memory_at_0, load_i32(memory_at_0, loc_5 + 40), loc_16)
			goto continue_at_5
			::continue_at_82::
			store_i32_n8(memory_at_0, load_i32(memory_at_0, loc_5 + 40), loc_16)
			goto continue_at_5
			::continue_at_81::
			store_i32(memory_at_0, load_i32(memory_at_0, loc_5 + 40), loc_16)
			goto continue_at_5
			::continue_at_80::
			store_i64(memory_at_0, load_i32(memory_at_0, loc_5 + 40), extend_i64_i32(loc_16))
			goto continue_at_5
			::continue_at_77::
			loc_22 = (gt_u32(loc_22, 8) and loc_22 or 8)
			loc_27 = bor_i32(loc_27, 8)
			loc_28 = 120
			::continue_at_76::
			loc_21 = 0
			loc_29 = 2746
			loc_30 = load_i64(memory_at_0, loc_5 + 40)
			if (loc_30 == 0LL and 1 or 0) == 0 then
				goto continue_at_87
			end
			loc_18 = loc_14
			goto continue_at_72
			::continue_at_87::
			loc_20 = band_i32(loc_28, 32)
			loc_18 = loc_14
			::continue_at_88::
			while true do
				loc_18 = add_i32(loc_18, -1)
				store_i32_n8(memory_at_0, loc_18, bor_i32(load_i32_u8(memory_at_0, add_i32(band_i32(wrap_i32_i64(loc_30), 15), 3456)), loc_20))
				loc_17 = (gt_u64(loc_30, 15LL) and 1 or 0)
				loc_30 = shr_u64(loc_30, 4LL)
				if loc_17 ~= 0 then
					goto continue_at_88
				end
				break
			end
			if band_i32(loc_27, 8) == 0 then
				goto continue_at_72
			end
			loc_29 = add_i32(shr_i32(loc_28, 4), 2746)
			loc_21 = 2
			goto continue_at_72
			::continue_at_75::
			loc_18 = loc_14
			loc_30 = load_i64(memory_at_0, loc_5 + 40)
			if loc_30 == 0LL then
				goto continue_at_89
			end
			loc_18 = loc_14
			::continue_at_90::
			while true do
				loc_18 = add_i32(loc_18, -1)
				store_i32_n8(memory_at_0, loc_18, bor_i32(band_i32(wrap_i32_i64(loc_30), 7), 48))
				loc_17 = (gt_u64(loc_30, 7LL) and 1 or 0)
				loc_30 = shr_u64(loc_30, 3LL)
				if loc_17 ~= 0 then
					goto continue_at_90
				end
				break
			end
			::continue_at_89::
			loc_21 = 0
			loc_29 = 2746
			if band_i32(loc_27, 8) == 0 then
				goto continue_at_72
			end
			loc_17 = sub_i32(loc_14, loc_18)
			loc_22 = (loc_22 > loc_17 and loc_22 or add_i32(loc_17, 1))
			goto continue_at_72
			::continue_at_74::
			loc_30 = load_i64(memory_at_0, loc_5 + 40)
			if loc_30 > -1LL then
				goto continue_at_91
			end
			loc_30 = (0LL - loc_30)
			store_i64(memory_at_0, loc_5 + 40, loc_30)
			loc_21 = 1
			loc_29 = 2746
			goto continue_at_73
			::continue_at_91::
			if band_i32(loc_27, 2048) == 0 then
				goto continue_at_92
			end
			loc_21 = 1
			loc_29 = 2747
			goto continue_at_73
			::continue_at_92::
			loc_21 = band_i32(loc_27, 1)
			loc_29 = (loc_21 ~= 0 and 2748 or 2746)
			::continue_at_73::
			if ge_u64(loc_30, 4294967296LL) then
				goto continue_at_94
			end
			loc_31 = loc_30
			loc_18 = loc_14
			goto continue_at_93
			::continue_at_94::
			loc_18 = loc_14
			::continue_at_95::
			while true do
				loc_18 = add_i32(loc_18, -1)
				loc_31 = div_u64(loc_30, 10LL)
				store_i32_n8(memory_at_0, loc_18, bor_i32(wrap_i32_i64((loc_30 - (loc_31 * 10LL))), 48))
				loc_17 = (gt_u64(loc_30, 42949672959LL) and 1 or 0)
				loc_30 = loc_31
				if loc_17 ~= 0 then
					goto continue_at_95
				end
				break
			end
			::continue_at_93::
			if loc_31 == 0LL then
				goto continue_at_72
			end
			loc_17 = wrap_i32_i64(loc_31)
			::continue_at_96::
			while true do
				loc_18 = add_i32(loc_18, -1)
				loc_20 = div_u32(loc_17, 10)
				store_i32_n8(memory_at_0, loc_18, bor_i32(sub_i32(loc_17, mul_i32(loc_20, 10)), 48))
				loc_23 = (gt_u32(loc_17, 9) and 1 or 0)
				loc_17 = loc_20
				if loc_23 ~= 0 then
					goto continue_at_96
				end
				break
			end
			::continue_at_72::
			if band_i32(loc_25, (loc_22 < 0 and 1 or 0)) ~= 0 then
				goto continue_at_4
			end
			loc_26 = (loc_25 ~= 0 and band_i32(loc_27, -65537) or loc_27)
			loc_30 = load_i64(memory_at_0, loc_5 + 40)
			if loc_30 ~= 0LL then
				goto continue_at_97
			end
			loc_23 = 0
			if loc_22 ~= 0 then
				goto continue_at_97
			end
			loc_18 = loc_14
			loc_17 = loc_14
			goto continue_at_6
			::continue_at_97::
			loc_17 = add_i32(sub_i32(loc_14, loc_18), (loc_30 == 0LL and 1 or 0))
			loc_23 = (loc_22 > loc_17 and loc_22 or loc_17)
			loc_17 = loc_14
			goto continue_at_6
			::continue_at_71::
			loc_17 = load_i32_u8(memory_at_0, loc_5 + 40)
			goto continue_at_7
			::continue_at_70::
			reg_0 = FUNC_LIST[43](load_i32(memory_at_0, 0 + 4484))
			loc_18 = reg_0
			goto continue_at_68
			::continue_at_69::
			loc_17 = load_i32(memory_at_0, loc_5 + 40)
			loc_18 = (loc_17 ~= 0 and loc_17 or 2796)
			::continue_at_68::
			reg_1 = FUNC_LIST[45](loc_18, (lt_u32(loc_22, 2147483647) and loc_22 or 2147483647))
			loc_23 = reg_1
			loc_17 = add_i32(loc_18, loc_23)
			loc_21 = 0
			loc_29 = 2746
			if loc_22 > -1 then
				goto continue_at_6
			end
			if load_i32_u8(memory_at_0, loc_17) == 0 then
				goto continue_at_6
			end
			goto continue_at_4
			::continue_at_67::
			loc_30 = load_i64(memory_at_0, loc_5 + 40)
			if (loc_30 == 0LL and 1 or 0) == 0 then
				goto continue_at_65
			end
			loc_17 = 0
			goto continue_at_7
			::continue_at_66::
			if loc_22 == 0 then
				goto continue_at_98
			end
			loc_20 = load_i32(memory_at_0, loc_5 + 40)
			goto continue_at_64
			::continue_at_98::
			loc_17 = 0
			FUNC_LIST[53](loc_0, 32, loc_24, 0, loc_27)
			goto continue_at_63
			::continue_at_65::
			store_i32(memory_at_0, loc_5 + 12, 0)
			store_i64_n32(memory_at_0, loc_5 + 8, loc_30)
			store_i32(memory_at_0, loc_5 + 40, add_i32(loc_5, 8))
			loc_20 = add_i32(loc_5, 8)
			loc_22 = -1
			::continue_at_64::
			loc_17 = 0
			loc_18 = loc_20
			::continue_at_100::
			while true do
				loc_19 = load_i32(memory_at_0, loc_18)
				if loc_19 == 0 then
					goto continue_at_99
				end
				reg_0 = FUNC_LIST[47](add_i32(loc_5, 4), loc_19)
				loc_19 = reg_0
				if loc_19 < 0 then
					goto continue_at_2
				end
				if gt_u32(loc_19, sub_i32(loc_22, loc_17)) then
					goto continue_at_99
				end
				loc_18 = add_i32(loc_18, 4)
				loc_17 = add_i32(loc_19, loc_17)
				if lt_u32(loc_17, loc_22) then
					goto continue_at_100
				end
				break
			end
			::continue_at_99::
			if loc_17 < 0 then
				goto continue_at_4
			end
			FUNC_LIST[53](loc_0, 32, loc_24, loc_17, loc_27)
			if loc_17 ~= 0 then
				goto continue_at_101
			end
			loc_17 = 0
			goto continue_at_63
			::continue_at_101::
			loc_18 = 0
			::continue_at_102::
			while true do
				loc_19 = load_i32(memory_at_0, loc_20)
				if loc_19 == 0 then
					goto continue_at_63
				end
				reg_0 = FUNC_LIST[47](add_i32(loc_5, 4), loc_19)
				loc_19 = reg_0
				loc_18 = add_i32(loc_19, loc_18)
				if gt_u32(loc_18, loc_17) then
					goto continue_at_63
				end
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_103
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 4), loc_19, loc_0)
				::continue_at_103::
				loc_20 = add_i32(loc_20, 4)
				if lt_u32(loc_18, loc_17) then
					goto continue_at_102
				end
				break
			end
			::continue_at_63::
			FUNC_LIST[53](loc_0, 32, loc_24, loc_17, bxor_i32(loc_27, 8192))
			loc_17 = (loc_24 > loc_17 and loc_24 or loc_17)
			goto continue_at_5
			::continue_at_62::
			loc_17 = (loc_22 < 0 and 1 or 0)
			if band_i32(loc_25, loc_17) ~= 0 then
				goto continue_at_4
			end
			loc_32 = load_f64(memory_at_0, loc_5 + 40)
			store_i32(memory_at_0, loc_5 + 92, 0)
			if reinterpret_i64_f64(loc_32) > -1LL then
				goto continue_at_105
			end
			loc_32 = neg_f64(loc_32)
			loc_33 = 1
			loc_34 = 0
			loc_35 = 2756
			goto continue_at_104
			::continue_at_105::
			if band_i32(loc_27, 2048) == 0 then
				goto continue_at_106
			end
			loc_33 = 1
			loc_34 = 0
			loc_35 = 2759
			goto continue_at_104
			::continue_at_106::
			loc_33 = band_i32(loc_27, 1)
			loc_35 = (loc_33 ~= 0 and 2762 or 2757)
			loc_34 = (loc_33 == 0 and 1 or 0)
			::continue_at_104::
			if loc_32 < math.huge then
				goto continue_at_107
			end
			loc_18 = add_i32(loc_33, 3)
			if band_i32(loc_27, 8192) ~= 0 then
				goto continue_at_108
			end
			if le_u32(loc_24, loc_18) then
				goto continue_at_108
			end
			loc_17 = sub_i32(loc_24, loc_18)
			loc_19 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_20 = (loc_19 ~= 0 and loc_17 or 256)
			if loc_20 == 0 then
				goto continue_at_109
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_20, 32)
			::continue_at_109::
			if loc_19 ~= 0 then
				goto continue_at_110
			end
			::continue_at_111::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_112
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_112::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_111
				end
				break
			end
			loc_21 = load_i32(memory_at_0, loc_0)
			::continue_at_110::
			if band_i32(loc_21, 32) ~= 0 then
				goto continue_at_108
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			loc_21 = load_i32(memory_at_0, loc_0)
			::continue_at_108::
			if band_i32(loc_21, 32) ~= 0 then
				goto continue_at_113
			end
			reg_0 = FUNC_LIST[39](loc_35, loc_33, loc_0)
			loc_21 = load_i32(memory_at_0, loc_0)
			::continue_at_113::
			if band_i32(loc_21, 32) ~= 0 then
				goto continue_at_114
			end
			loc_17 = band_i32(loc_28, 32)
			reg_0 = FUNC_LIST[39]((loc_32 ~= loc_32 and (loc_17 ~= 0 and 2778 or 2786) or (loc_17 ~= 0 and 2782 or 2790)), 3, loc_0)
			::continue_at_114::
			if band_i32(loc_27, 73728) ~= 8192 then
				goto continue_at_115
			end
			if le_u32(loc_24, loc_18) then
				goto continue_at_115
			end
			loc_17 = sub_i32(loc_24, loc_18)
			loc_19 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_20 = (loc_19 ~= 0 and loc_17 or 256)
			if loc_20 == 0 then
				goto continue_at_116
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_20, 32)
			::continue_at_116::
			if loc_19 ~= 0 then
				goto continue_at_117
			end
			::continue_at_118::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_119
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_119::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_118
				end
				break
			end
			::continue_at_117::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_115
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_115::
			loc_17 = (gt_u32(loc_24, loc_18) and loc_24 or loc_18)
			goto continue_at_8
			::continue_at_107::
			reg_0 = FUNC_LIST[48](loc_32, add_i32(loc_5, 92))
			loc_32 = reg_0
			loc_32 = (loc_32 + loc_32)
			if loc_32 == 0e0 then
				goto continue_at_122
			end
			loc_18 = load_i32(memory_at_0, loc_5 + 92)
			store_i32(memory_at_0, loc_5 + 92, add_i32(loc_18, -1))
			loc_36 = bor_i32(loc_28, 32)
			if loc_36 ~= 97 then
				goto continue_at_121
			end
			goto continue_at_9
			::continue_at_122::
			loc_36 = bor_i32(loc_28, 32)
			if loc_36 == 97 then
				goto continue_at_9
			end
			loc_21 = (loc_17 ~= 0 and 6 or loc_22)
			loc_20 = load_i32(memory_at_0, loc_5 + 92)
			goto continue_at_120
			::continue_at_121::
			loc_20 = add_i32(loc_18, -29)
			store_i32(memory_at_0, loc_5 + 92, loc_20)
			loc_21 = (loc_17 ~= 0 and 6 or loc_22)
			loc_32 = (loc_32 * 2.68435456e8)
			::continue_at_120::
			loc_37 = (loc_20 < 0 and 1 or 0)
			loc_29 = add_i32(add_i32(loc_5, 96), (loc_37 ~= 0 and 0 or 288))
			loc_18 = loc_29
			::continue_at_123::
			while true do
				loc_17 = saturate_u32_f64(loc_32)
				store_i32(memory_at_0, loc_18, loc_17)
				loc_18 = add_i32(loc_18, 4)
				loc_32 = ((loc_32 - convert_f64_u32(loc_17)) * 1e9)
				if loc_32 ~= 0e0 then
					goto continue_at_123
				end
				break
			end
			if loc_20 >= 1 then
				goto continue_at_125
			end
			loc_17 = loc_18
			loc_19 = loc_29
			goto continue_at_124
			::continue_at_125::
			loc_19 = loc_29
			::continue_at_126::
			while true do
				loc_20 = (lt_u32(loc_20, 29) and loc_20 or 29)
				loc_17 = add_i32(loc_18, -4)
				if lt_u32(loc_17, loc_19) then
					goto continue_at_127
				end
				loc_38 = extend_i64_u32(loc_20)
				loc_30 = 0LL
				::continue_at_128::
				while true do
					loc_31 = (shl_i64(load_i64_u32(memory_at_0, loc_17), loc_38) + band_i64(loc_30, 4294967295LL))
					loc_30 = div_u64(loc_31, 1000000000LL)
					store_i64_n32(memory_at_0, loc_17, (loc_31 - (loc_30 * 1000000000LL)))
					loc_17 = add_i32(loc_17, -4)
					if ge_u32(loc_17, loc_19) then
						goto continue_at_128
					end
					break
				end
				if lt_u64(loc_31, 1000000000LL) then
					goto continue_at_127
				end
				loc_19 = add_i32(loc_19, -4)
				store_i64_n32(memory_at_0, loc_19, loc_30)
				::continue_at_127::
				::continue_at_130::
				while true do
					loc_17 = loc_18
					if le_u32(loc_17, loc_19) then
						goto continue_at_129
					end
					loc_18 = add_i32(loc_17, -4)
					if load_i32(memory_at_0, loc_18) == 0 then
						goto continue_at_130
					end
					break
				end
				::continue_at_129::
				loc_20 = sub_i32(load_i32(memory_at_0, loc_5 + 92), loc_20)
				store_i32(memory_at_0, loc_5 + 92, loc_20)
				loc_18 = loc_17
				if loc_20 > 0 then
					goto continue_at_126
				end
				break
			end
			::continue_at_124::
			if loc_20 > -1 then
				goto continue_at_131
			end
			loc_39 = add_i32(div_u32(add_i32(loc_21, 25), 9), 1)
			loc_40 = (loc_36 == 102 and 1 or 0)
			::continue_at_132::
			while true do
				loc_18 = sub_i32(0, loc_20)
				loc_22 = (lt_u32(loc_18, 9) and loc_18 or 9)
				if lt_u32(loc_19, loc_17) then
					goto continue_at_134
				end
				loc_18 = shl_i32((load_i32(memory_at_0, loc_19) == 0 and 1 or 0), 2)
				goto continue_at_133
				::continue_at_134::
				loc_26 = shr_u32(1000000000, loc_22)
				loc_25 = bxor_i32(shl_i32(-1, loc_22), -1)
				loc_20 = 0
				loc_18 = loc_19
				::continue_at_135::
				while true do
					loc_23 = load_i32(memory_at_0, loc_18)
					store_i32(memory_at_0, loc_18, add_i32(shr_u32(loc_23, loc_22), loc_20))
					loc_20 = mul_i32(band_i32(loc_23, loc_25), loc_26)
					loc_18 = add_i32(loc_18, 4)
					if lt_u32(loc_18, loc_17) then
						goto continue_at_135
					end
					break
				end
				loc_18 = shl_i32((load_i32(memory_at_0, loc_19) == 0 and 1 or 0), 2)
				if loc_20 == 0 then
					goto continue_at_133
				end
				store_i32(memory_at_0, loc_17, loc_20)
				loc_17 = add_i32(loc_17, 4)
				::continue_at_133::
				loc_20 = add_i32(load_i32(memory_at_0, loc_5 + 92), loc_22)
				store_i32(memory_at_0, loc_5 + 92, loc_20)
				loc_19 = add_i32(loc_19, loc_18)
				loc_18 = (loc_40 ~= 0 and loc_29 or loc_19)
				loc_17 = (shr_i32(sub_i32(loc_17, loc_18), 2) > loc_39 and add_i32(loc_18, shl_i32(loc_39, 2)) or loc_17)
				if loc_20 < 0 then
					goto continue_at_132
				end
				break
			end
			::continue_at_131::
			loc_23 = 0
			if ge_u32(loc_19, loc_17) then
				goto continue_at_136
			end
			loc_23 = mul_i32(shr_i32(sub_i32(loc_29, loc_19), 2), 9)
			loc_20 = load_i32(memory_at_0, loc_19)
			if lt_u32(loc_20, 10) then
				goto continue_at_136
			end
			loc_18 = 10
			::continue_at_137::
			while true do
				loc_23 = add_i32(loc_23, 1)
				loc_18 = mul_i32(loc_18, 10)
				if ge_u32(loc_20, loc_18) then
					goto continue_at_137
				end
				break
			end
			::continue_at_136::
			loc_25 = (loc_36 == 103 and 1 or 0)
			loc_18 = sub_i32(sub_i32(loc_21, (loc_36 == 102 and 0 or loc_23)), band_i32((loc_21 ~= 0 and 1 or 0), loc_25))
			if loc_18 >= add_i32(mul_i32(shr_i32(sub_i32(loc_17, loc_29), 2), 9), -9) then
				goto continue_at_138
			end
			loc_36 = (loc_37 ~= 0 and -4092 or -3804)
			loc_20 = add_i32(loc_18, 9216)
			loc_22 = div_i32(loc_20, 9)
			loc_37 = shl_i32(loc_22, 2)
			loc_26 = add_i32(add_i32(add_i32(loc_5, 96), loc_36), loc_37)
			loc_18 = 10
			loc_22 = sub_i32(loc_20, mul_i32(loc_22, 9))
			if loc_22 > 7 then
				goto continue_at_139
			end
			loc_39 = sub_i32(8, loc_22)
			loc_20 = band_i32(loc_39, 7)
			loc_18 = 10
			if lt_u32(add_i32(loc_22, -1), 7) then
				goto continue_at_140
			end
			loc_22 = band_i32(loc_39, -8)
			loc_18 = 10
			::continue_at_141::
			while true do
				loc_18 = mul_i32(loc_18, 100000000)
				loc_22 = add_i32(loc_22, -8)
				if loc_22 ~= 0 then
					goto continue_at_141
				end
				break
			end
			::continue_at_140::
			if loc_20 == 0 then
				goto continue_at_139
			end
			::continue_at_142::
			while true do
				loc_18 = mul_i32(loc_18, 10)
				loc_20 = add_i32(loc_20, -1)
				if loc_20 ~= 0 then
					goto continue_at_142
				end
				break
			end
			::continue_at_139::
			loc_39 = add_i32(loc_26, 4)
			loc_20 = load_i32(memory_at_0, loc_26)
			loc_40 = div_u32(loc_20, loc_18)
			loc_22 = sub_i32(loc_20, mul_i32(loc_40, loc_18))
			if loc_22 ~= 0 then
				goto continue_at_144
			end
			if loc_39 == loc_17 then
				goto continue_at_143
			end
			::continue_at_144::
			if band_i32(loc_40, 1) ~= 0 then
				goto continue_at_146
			end
			loc_32 = 9.007199254740992e15
			if loc_18 ~= 1000000000 then
				goto continue_at_145
			end
			if le_u32(loc_26, loc_19) then
				goto continue_at_145
			end
			if band_i32(load_i32_u8(memory_at_0, add_i32(loc_26, -4)), 1) == 0 then
				goto continue_at_145
			end
			::continue_at_146::
			loc_32 = 9.007199254740994e15
			::continue_at_145::
			reg_1 = (loc_39 == loc_17 and 1e0 or 1.5e0)
			loc_39 = shr_u32(loc_18, 1)
			loc_41 = (lt_u32(loc_22, loc_39) and 5e-1 or (loc_22 == loc_39 and reg_1 or 1.5e0))
			if loc_34 ~= 0 then
				goto continue_at_147
			end
			if load_i32_u8(memory_at_0, loc_35) ~= 45 then
				goto continue_at_147
			end
			loc_41 = neg_f64(loc_41)
			loc_32 = neg_f64(loc_32)
			::continue_at_147::
			loc_20 = sub_i32(loc_20, loc_22)
			store_i32(memory_at_0, loc_26, loc_20)
			if (loc_32 + loc_41) == loc_32 then
				goto continue_at_143
			end
			loc_18 = add_i32(loc_20, loc_18)
			store_i32(memory_at_0, loc_26, loc_18)
			if lt_u32(loc_18, 1000000000) then
				goto continue_at_148
			end
			loc_18 = add_i32(loc_7, add_i32(loc_36, loc_37))
			::continue_at_149::
			while true do
				store_i32(memory_at_0, add_i32(loc_18, 4), 0)
				if ge_u32(loc_18, loc_19) then
					goto continue_at_150
				end
				loc_19 = add_i32(loc_19, -4)
				store_i32(memory_at_0, loc_19, 0)
				::continue_at_150::
				loc_20 = add_i32(load_i32(memory_at_0, loc_18), 1)
				store_i32(memory_at_0, loc_18, loc_20)
				loc_18 = add_i32(loc_18, -4)
				if gt_u32(loc_20, 999999999) then
					goto continue_at_149
				end
				break
			end
			loc_26 = add_i32(loc_18, 4)
			::continue_at_148::
			loc_23 = mul_i32(shr_i32(sub_i32(loc_29, loc_19), 2), 9)
			loc_20 = load_i32(memory_at_0, loc_19)
			if lt_u32(loc_20, 10) then
				goto continue_at_143
			end
			loc_18 = 10
			::continue_at_151::
			while true do
				loc_23 = add_i32(loc_23, 1)
				loc_18 = mul_i32(loc_18, 10)
				if ge_u32(loc_20, loc_18) then
					goto continue_at_151
				end
				break
			end
			::continue_at_143::
			loc_18 = add_i32(loc_26, 4)
			loc_17 = (gt_u32(loc_17, loc_18) and loc_18 or loc_17)
			::continue_at_138::
			loc_18 = sub_i32(loc_17, loc_29)
			::continue_at_153::
			while true do
				loc_20 = loc_18
				loc_26 = loc_17
				loc_22 = (le_u32(loc_26, loc_19) and 1 or 0)
				if loc_22 ~= 0 then
					goto continue_at_152
				end
				loc_18 = add_i32(loc_20, -4)
				loc_17 = add_i32(loc_26, -4)
				if load_i32(memory_at_0, loc_17) == 0 then
					goto continue_at_153
				end
				break
			end
			::continue_at_152::
			if loc_25 ~= 0 then
				goto continue_at_155
			end
			loc_39 = band_i32(loc_27, 8)
			goto continue_at_154
			::continue_at_155::
			loc_17 = (loc_21 ~= 0 and loc_21 or 1)
			loc_18 = band_i32((loc_17 > loc_23 and 1 or 0), (loc_23 > -5 and 1 or 0))
			loc_21 = add_i32((loc_18 ~= 0 and bxor_i32(loc_23, -1) or -1), loc_17)
			loc_28 = add_i32((loc_18 ~= 0 and -1 or -2), loc_28)
			loc_39 = band_i32(loc_27, 8)
			if loc_39 ~= 0 then
				goto continue_at_154
			end
			loc_17 = -9
			if loc_22 ~= 0 then
				goto continue_at_156
			end
			loc_22 = load_i32(memory_at_0, add_i32(loc_26, -4))
			if loc_22 == 0 then
				goto continue_at_156
			end
			loc_17 = 0
			if rem_u32(loc_22, 10) ~= 0 then
				goto continue_at_156
			end
			loc_18 = 10
			loc_17 = 0
			::continue_at_157::
			while true do
				loc_17 = add_i32(loc_17, -1)
				loc_18 = mul_i32(loc_18, 10)
				if rem_u32(loc_22, loc_18) == 0 then
					goto continue_at_157
				end
				break
			end
			::continue_at_156::
			loc_18 = mul_i32(shr_i32(loc_20, 2), 9)
			if band_i32(loc_28, -33) ~= 70 then
				goto continue_at_158
			end
			loc_39 = 0
			loc_17 = add_i32(add_i32(loc_18, loc_17), -9)
			loc_17 = (loc_17 > 0 and loc_17 or 0)
			loc_21 = (loc_21 < loc_17 and loc_21 or loc_17)
			goto continue_at_154
			::continue_at_158::
			loc_39 = 0
			loc_17 = add_i32(add_i32(add_i32(loc_23, loc_18), loc_17), -9)
			loc_17 = (loc_17 > 0 and loc_17 or 0)
			loc_21 = (loc_21 < loc_17 and loc_21 or loc_17)
			::continue_at_154::
			loc_36 = bor_i32(loc_21, loc_39)
			if loc_21 > (loc_36 ~= 0 and 2147483645 or 2147483646) then
				goto continue_at_4
			end
			loc_40 = add_i32(add_i32(loc_21, (loc_36 ~= 0 and 1 or 0)), 1)
			loc_37 = (band_i32(loc_28, -33) ~= 70 and 1 or 0)
			if loc_37 ~= 0 then
				goto continue_at_160
			end
			if loc_23 > bxor_i32(loc_40, 2147483647) then
				goto continue_at_4
			end
			loc_17 = (loc_23 > 0 and loc_23 or 0)
			goto continue_at_159
			::continue_at_160::
			if loc_23 ~= 0 then
				goto continue_at_162
			end
			loc_20 = loc_6
			loc_18 = loc_6
			goto continue_at_161
			::continue_at_162::
			loc_17 = shr_i32(loc_23, 31)
			loc_17 = sub_i32(bxor_i32(loc_23, loc_17), loc_17)
			loc_20 = loc_6
			loc_18 = loc_6
			::continue_at_163::
			while true do
				loc_18 = add_i32(loc_18, -1)
				loc_22 = div_u32(loc_17, 10)
				store_i32_n8(memory_at_0, loc_18, bor_i32(sub_i32(loc_17, mul_i32(loc_22, 10)), 48))
				loc_20 = add_i32(loc_20, -1)
				loc_25 = (gt_u32(loc_17, 9) and 1 or 0)
				loc_17 = loc_22
				if loc_25 ~= 0 then
					goto continue_at_163
				end
				break
			end
			::continue_at_161::
			if sub_i32(loc_6, loc_20) > 1 then
				goto continue_at_164
			end
			loc_18 = add_i32(loc_18, sub_i32(loc_13, loc_20))
			loc_17 = add_i32(sub_i32(loc_20, add_i32(loc_5, 52)), -10)
			if loc_17 == 0 then
				goto continue_at_164
			end
			rt.store.fill(memory_at_0, loc_18, loc_17, 48)
			::continue_at_164::
			loc_34 = add_i32(loc_18, -2)
			store_i32_n8(memory_at_0, loc_34, loc_28)
			store_i32_n8(memory_at_0, add_i32(loc_18, -1), (loc_23 < 0 and 45 or 43))
			loc_17 = sub_i32(loc_6, loc_34)
			if loc_17 > bxor_i32(loc_40, 2147483647) then
				goto continue_at_4
			end
			::continue_at_159::
			loc_17 = add_i32(loc_17, loc_40)
			if loc_17 > bxor_i32(loc_33, 2147483647) then
				goto continue_at_4
			end
			loc_25 = add_i32(loc_17, loc_33)
			loc_27 = band_i32(loc_27, 73728)
			if loc_27 ~= 0 then
				goto continue_at_165
			end
			if loc_24 <= loc_25 then
				goto continue_at_165
			end
			loc_17 = sub_i32(loc_24, loc_25)
			loc_18 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_20 = (loc_18 ~= 0 and loc_17 or 256)
			if loc_20 == 0 then
				goto continue_at_166
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_20, 32)
			::continue_at_166::
			if loc_18 ~= 0 then
				goto continue_at_167
			end
			::continue_at_168::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_169
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_169::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_168
				end
				break
			end
			::continue_at_167::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_165
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_165::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_170
			end
			reg_0 = FUNC_LIST[39](loc_35, loc_33, loc_0)
			::continue_at_170::
			if loc_27 ~= 65536 then
				goto continue_at_171
			end
			if loc_24 <= loc_25 then
				goto continue_at_171
			end
			loc_17 = sub_i32(loc_24, loc_25)
			loc_18 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_20 = (loc_18 ~= 0 and loc_17 or 256)
			if loc_20 == 0 then
				goto continue_at_172
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_20, 48)
			::continue_at_172::
			if loc_18 ~= 0 then
				goto continue_at_173
			end
			::continue_at_174::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_175
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_175::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_174
				end
				break
			end
			::continue_at_173::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_171
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_171::
			if loc_37 ~= 0 then
				goto continue_at_11
			end
			loc_23 = (gt_u32(loc_19, loc_29) and loc_29 or loc_19)
			loc_22 = loc_23
			::continue_at_176::
			while true do
				loc_17 = load_i32(memory_at_0, loc_22)
				if loc_17 == 0 then
					goto continue_at_180
				end
				loc_18 = 8
				::continue_at_181::
				while true do
					loc_19 = div_u32(loc_17, 10)
					store_i32_n8(memory_at_0, add_i32(add_i32(loc_5, 64), loc_18), bor_i32(sub_i32(loc_17, mul_i32(loc_19, 10)), 48))
					loc_18 = add_i32(loc_18, -1)
					loc_20 = (gt_u32(loc_17, 9) and 1 or 0)
					loc_17 = loc_19
					if loc_20 ~= 0 then
						goto continue_at_181
					end
					break
				end
				loc_19 = add_i32(loc_18, 1)
				loc_17 = add_i32(loc_19, add_i32(loc_5, 64))
				if loc_22 == loc_23 then
					goto continue_at_182
				end
				if add_i32(loc_18, 2) < 2 then
					goto continue_at_177
				end
				goto continue_at_178
				::continue_at_182::
				if loc_18 ~= 8 then
					goto continue_at_177
				end
				goto continue_at_179
				::continue_at_180::
				loc_19 = 9
				if loc_22 ~= loc_23 then
					goto continue_at_178
				end
				::continue_at_179::
				store_i32_n8(memory_at_0, loc_5 + 72, 48)
				loc_17 = loc_11
				goto continue_at_177
				::continue_at_178::
				loc_17 = add_i32(loc_10, loc_19)
				loc_17 = (lt_u32(add_i32(loc_5, 64), loc_17) and add_i32(loc_5, 64) or loc_17)
				loc_18 = sub_i32(add_i32(loc_19, add_i32(loc_5, 64)), loc_17)
				if loc_18 == 0 then
					goto continue_at_177
				end
				rt.store.fill(memory_at_0, loc_17, loc_18, 48)
				::continue_at_177::
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_183
				end
				reg_0 = FUNC_LIST[39](loc_17, sub_i32(loc_12, loc_17), loc_0)
				::continue_at_183::
				loc_22 = add_i32(loc_22, 4)
				if le_u32(loc_22, loc_29) then
					goto continue_at_176
				end
				break
			end
			if loc_36 == 0 then
				goto continue_at_184
			end
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_184
			end
			reg_0 = FUNC_LIST[39](2794, 1, loc_0)
			::continue_at_184::
			if loc_21 >= 1 then
				goto continue_at_186
			end
			loc_17 = loc_21
			goto continue_at_185
			::continue_at_186::
			if lt_u32(loc_22, loc_26) then
				goto continue_at_187
			end
			loc_17 = loc_21
			goto continue_at_185
			::continue_at_187::
			::continue_at_188::
			while true do
				loc_17 = load_i32(memory_at_0, loc_22)
				if loc_17 ~= 0 then
					goto continue_at_191
				end
				loc_18 = loc_12
				loc_19 = loc_12
				goto continue_at_190
				::continue_at_191::
				loc_19 = loc_12
				loc_18 = loc_12
				::continue_at_192::
				while true do
					loc_18 = add_i32(loc_18, -1)
					loc_20 = div_u32(loc_17, 10)
					store_i32_n8(memory_at_0, loc_18, bor_i32(sub_i32(loc_17, mul_i32(loc_20, 10)), 48))
					loc_19 = add_i32(loc_19, -1)
					loc_23 = (gt_u32(loc_17, 9) and 1 or 0)
					loc_17 = loc_20
					if loc_23 ~= 0 then
						goto continue_at_192
					end
					break
				end
				if le_u32(loc_18, add_i32(loc_5, 64)) then
					goto continue_at_189
				end
				::continue_at_190::
				loc_18 = sub_i32(add_i32(loc_18, add_i32(loc_5, 64)), loc_19)
				loc_17 = sub_i32(loc_19, add_i32(loc_5, 64))
				if loc_17 == 0 then
					goto continue_at_189
				end
				rt.store.fill(memory_at_0, loc_18, loc_17, 48)
				::continue_at_189::
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_193
				end
				reg_0 = FUNC_LIST[39](loc_18, (loc_21 < 9 and loc_21 or 9), loc_0)
				::continue_at_193::
				loc_17 = add_i32(loc_21, -9)
				loc_22 = add_i32(loc_22, 4)
				if ge_u32(loc_22, loc_26) then
					goto continue_at_185
				end
				loc_18 = (loc_21 > 9 and 1 or 0)
				loc_21 = loc_17
				if loc_18 ~= 0 then
					goto continue_at_188
				end
				break
			end
			::continue_at_185::
			FUNC_LIST[53](loc_0, 48, add_i32(loc_17, 9), 9, 0)
			goto continue_at_10
			::continue_at_13::
			store_i32(memory_at_0, 0 + 4484, 28)
			goto continue_at_2
			::continue_at_12::
			loc_21 = 0
			loc_29 = 2746
			loc_17 = loc_14
			loc_26 = loc_27
			loc_23 = loc_22
			goto continue_at_6
			::continue_at_11::
			if loc_21 < 0 then
				goto continue_at_194
			end
			loc_26 = (gt_u32(loc_26, loc_19) and loc_26 or add_i32(loc_19, 4))
			loc_22 = loc_19
			::continue_at_195::
			while true do
				loc_17 = load_i32(memory_at_0, loc_22)
				if loc_17 == 0 then
					goto continue_at_197
				end
				loc_18 = loc_12
				::continue_at_198::
				while true do
					loc_18 = add_i32(loc_18, -1)
					loc_20 = div_u32(loc_17, 10)
					store_i32_n8(memory_at_0, loc_18, bor_i32(sub_i32(loc_17, mul_i32(loc_20, 10)), 48))
					loc_23 = (lt_u32(loc_17, 10) and 1 or 0)
					loc_17 = loc_20
					if loc_23 == 0 then
						goto continue_at_198
					end
					goto continue_at_196
				end
				::continue_at_197::
				store_i32_n8(memory_at_0, loc_5 + 72, 48)
				loc_18 = loc_11
				::continue_at_196::
				if loc_22 == loc_19 then
					goto continue_at_200
				end
				if le_u32(loc_18, add_i32(loc_5, 64)) then
					goto continue_at_199
				end
				loc_17 = sub_i32(loc_18, add_i32(loc_5, 64))
				if loc_17 == 0 then
					goto continue_at_201
				end
				rt.store.fill(memory_at_0, add_i32(loc_5, 64), loc_17, 48)
				::continue_at_201::
				loc_18 = add_i32(loc_5, 64)
				goto continue_at_199
				::continue_at_200::
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_202
				end
				reg_0 = FUNC_LIST[39](loc_18, 1, loc_0)
				::continue_at_202::
				loc_18 = add_i32(loc_18, 1)
				if loc_39 ~= 0 then
					goto continue_at_203
				end
				if loc_21 < 1 then
					goto continue_at_199
				end
				::continue_at_203::
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_199
				end
				reg_0 = FUNC_LIST[39](2794, 1, loc_0)
				::continue_at_199::
				loc_17 = sub_i32(loc_12, loc_18)
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_204
				end
				reg_0 = FUNC_LIST[39](loc_18, (loc_17 < loc_21 and loc_17 or loc_21), loc_0)
				::continue_at_204::
				loc_21 = sub_i32(loc_21, loc_17)
				loc_22 = add_i32(loc_22, 4)
				if ge_u32(loc_22, loc_26) then
					goto continue_at_194
				end
				if loc_21 > -1 then
					goto continue_at_195
				end
				break
			end
			::continue_at_194::
			FUNC_LIST[53](loc_0, 48, add_i32(loc_21, 18), 18, 0)
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_10
			end
			reg_0 = FUNC_LIST[39](loc_34, sub_i32(loc_6, loc_34), loc_0)
			::continue_at_10::
			if loc_27 ~= 8192 then
				goto continue_at_205
			end
			if loc_24 <= loc_25 then
				goto continue_at_205
			end
			loc_17 = sub_i32(loc_24, loc_25)
			loc_18 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_19 = (loc_18 ~= 0 and loc_17 or 256)
			if loc_19 == 0 then
				goto continue_at_206
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_19, 32)
			::continue_at_206::
			if loc_18 ~= 0 then
				goto continue_at_207
			end
			::continue_at_208::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_209
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_209::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_208
				end
				break
			end
			::continue_at_207::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_205
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_205::
			loc_17 = (loc_24 > loc_25 and loc_24 or loc_25)
			goto continue_at_8
			::continue_at_9::
			loc_21 = add_i32(loc_35, band_i32(shr_i32(shl_i32(loc_28, 26), 31), 9))
			if gt_u32(loc_22, 11) then
				goto continue_at_210
			end
			loc_17 = sub_i32(12, loc_22)
			loc_18 = band_i32(loc_17, 7)
			if loc_18 ~= 0 then
				goto continue_at_212
			end
			loc_41 = 1.6e1
			goto continue_at_211
			::continue_at_212::
			loc_17 = add_i32(loc_22, -12)
			loc_41 = 1.6e1
			::continue_at_213::
			while true do
				loc_17 = add_i32(loc_17, 1)
				loc_41 = (loc_41 * 1.6e1)
				loc_18 = add_i32(loc_18, -1)
				if loc_18 ~= 0 then
					goto continue_at_213
				end
				break
			end
			loc_17 = sub_i32(0, loc_17)
			::continue_at_211::
			if gt_u32(loc_22, 4) then
				goto continue_at_214
			end
			::continue_at_215::
			while true do
				loc_41 = ((((((((loc_41 * 1.6e1) * 1.6e1) * 1.6e1) * 1.6e1) * 1.6e1) * 1.6e1) * 1.6e1) * 1.6e1)
				loc_17 = add_i32(loc_17, -8)
				if loc_17 ~= 0 then
					goto continue_at_215
				end
				break
			end
			::continue_at_214::
			if load_i32_u8(memory_at_0, loc_21) ~= 45 then
				goto continue_at_216
			end
			loc_32 = neg_f64((loc_41 + (neg_f64(loc_32) - loc_41)))
			goto continue_at_210
			::continue_at_216::
			loc_32 = ((loc_32 + loc_41) - loc_41)
			::continue_at_210::
			loc_23 = load_i32(memory_at_0, loc_5 + 92)
			if loc_23 == 0 then
				goto continue_at_218
			end
			loc_17 = shr_i32(loc_23, 31)
			loc_17 = sub_i32(bxor_i32(loc_23, loc_17), loc_17)
			loc_18 = loc_6
			::continue_at_219::
			while true do
				loc_18 = add_i32(loc_18, -1)
				loc_19 = div_u32(loc_17, 10)
				store_i32_n8(memory_at_0, loc_18, bor_i32(sub_i32(loc_17, mul_i32(loc_19, 10)), 48))
				loc_20 = (lt_u32(loc_17, 10) and 1 or 0)
				loc_17 = loc_19
				if loc_20 == 0 then
					goto continue_at_219
				end
				goto continue_at_217
			end
			::continue_at_218::
			store_i32_n8(memory_at_0, loc_5 + 63, 48)
			loc_18 = loc_9
			::continue_at_217::
			loc_26 = bor_i32(loc_33, 2)
			loc_19 = band_i32(loc_28, 32)
			loc_25 = add_i32(loc_18, -2)
			store_i32_n8(memory_at_0, loc_25, add_i32(loc_28, 15))
			store_i32_n8(memory_at_0, add_i32(loc_18, -1), (loc_23 < 0 and 45 or 43))
			loc_20 = band_i32((band_i32(loc_27, 8) == 0 and 1 or 0), (loc_22 < 1 and 1 or 0))
			loc_18 = add_i32(loc_5, 64)
			::continue_at_220::
			while true do
				loc_17 = loc_18
				loc_18 = saturate_i32_f64(loc_32)
				store_i32_n8(memory_at_0, loc_17, bor_i32(load_i32_u8(memory_at_0, add_i32(loc_18, 3456)), loc_19))
				loc_32 = ((loc_32 - convert_f64_i32(loc_18)) * 1.6e1)
				loc_18 = add_i32(loc_17, 1)
				if sub_i32(loc_18, add_i32(loc_5, 64)) ~= 1 then
					goto continue_at_221
				end
				if band_i32(loc_20, (loc_32 == 0e0 and 1 or 0)) ~= 0 then
					goto continue_at_221
				end
				store_i32_n8(memory_at_0, loc_17 + 1, 46)
				loc_18 = add_i32(loc_17, 2)
				::continue_at_221::
				if loc_32 ~= 0e0 then
					goto continue_at_220
				end
				break
			end
			loc_29 = sub_i32(loc_6, loc_25)
			loc_17 = add_i32(loc_29, loc_26)
			if loc_22 > sub_i32(2147483645, loc_17) then
				goto continue_at_4
			end
			loc_19 = sub_i32(loc_18, add_i32(loc_5, 64))
			loc_23 = (loc_22 ~= 0 and (add_i32(loc_19, -2) < loc_22 and add_i32(loc_22, 2) or loc_19) or loc_19)
			loc_18 = add_i32(loc_23, loc_17)
			loc_20 = band_i32(loc_27, 73728)
			if loc_20 ~= 0 then
				goto continue_at_222
			end
			if loc_24 <= loc_18 then
				goto continue_at_222
			end
			loc_17 = sub_i32(loc_24, loc_18)
			loc_22 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_27 = (loc_22 ~= 0 and loc_17 or 256)
			if loc_27 == 0 then
				goto continue_at_223
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_27, 32)
			::continue_at_223::
			if loc_22 ~= 0 then
				goto continue_at_224
			end
			::continue_at_225::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_226
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_226::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_225
				end
				break
			end
			::continue_at_224::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_222
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_222::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_227
			end
			reg_0 = FUNC_LIST[39](loc_21, loc_26, loc_0)
			::continue_at_227::
			if loc_20 ~= 65536 then
				goto continue_at_228
			end
			if loc_24 <= loc_18 then
				goto continue_at_228
			end
			loc_17 = sub_i32(loc_24, loc_18)
			loc_22 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_26 = (loc_22 ~= 0 and loc_17 or 256)
			if loc_26 == 0 then
				goto continue_at_229
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_26, 48)
			::continue_at_229::
			if loc_22 ~= 0 then
				goto continue_at_230
			end
			::continue_at_231::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_232
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_232::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_231
				end
				break
			end
			::continue_at_230::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_228
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_228::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_233
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 64), loc_19, loc_0)
			::continue_at_233::
			loc_17 = sub_i32(loc_23, loc_19)
			if loc_17 < 1 then
				goto continue_at_234
			end
			loc_19 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_23 = (loc_19 ~= 0 and loc_17 or 256)
			if loc_23 == 0 then
				goto continue_at_235
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_23, 48)
			::continue_at_235::
			if loc_19 ~= 0 then
				goto continue_at_236
			end
			::continue_at_237::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_238
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_238::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_237
				end
				break
			end
			::continue_at_236::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_234
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_234::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_239
			end
			reg_0 = FUNC_LIST[39](loc_25, loc_29, loc_0)
			::continue_at_239::
			if loc_20 ~= 8192 then
				goto continue_at_240
			end
			if loc_24 <= loc_18 then
				goto continue_at_240
			end
			loc_17 = sub_i32(loc_24, loc_18)
			loc_19 = (lt_u32(loc_17, 256) and 1 or 0)
			loc_20 = (loc_19 ~= 0 and loc_17 or 256)
			if loc_20 == 0 then
				goto continue_at_241
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 608), loc_20, 32)
			::continue_at_241::
			if loc_19 ~= 0 then
				goto continue_at_242
			end
			::continue_at_243::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_244
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), 256, loc_0)
				::continue_at_244::
				loc_17 = add_i32(loc_17, -256)
				if gt_u32(loc_17, 255) then
					goto continue_at_243
				end
				break
			end
			::continue_at_242::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_240
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 608), loc_17, loc_0)
			::continue_at_240::
			loc_17 = (loc_24 > loc_18 and loc_24 or loc_18)
			::continue_at_8::
			if loc_17 >= 0 then
				goto continue_at_5
			end
			goto continue_at_4
			::continue_at_7::
			store_i32_n8(memory_at_0, loc_5 + 39, loc_17)
			loc_21 = 0
			loc_29 = 2746
			loc_23 = 1
			loc_18 = loc_8
			loc_17 = loc_14
			::continue_at_6::
			loc_22 = sub_i32(loc_17, loc_18)
			loc_25 = (loc_23 > loc_22 and loc_23 or loc_22)
			if loc_25 > bxor_i32(loc_21, 2147483647) then
				goto continue_at_4
			end
			loc_20 = add_i32(loc_21, loc_25)
			loc_17 = (loc_24 > loc_20 and loc_24 or loc_20)
			if loc_17 > loc_19 then
				goto continue_at_4
			end
			loc_26 = band_i32(loc_26, 73728)
			if loc_26 ~= 0 then
				goto continue_at_245
			end
			if loc_24 <= loc_20 then
				goto continue_at_245
			end
			loc_19 = sub_i32(loc_17, loc_20)
			loc_27 = (lt_u32(loc_19, 256) and 1 or 0)
			loc_39 = (loc_27 ~= 0 and loc_19 or 256)
			if loc_39 == 0 then
				goto continue_at_246
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 96), loc_39, 32)
			::continue_at_246::
			if loc_27 ~= 0 then
				goto continue_at_247
			end
			::continue_at_248::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_249
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), 256, loc_0)
				::continue_at_249::
				loc_19 = add_i32(loc_19, -256)
				if gt_u32(loc_19, 255) then
					goto continue_at_248
				end
				break
			end
			::continue_at_247::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_245
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), loc_19, loc_0)
			::continue_at_245::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_250
			end
			reg_0 = FUNC_LIST[39](loc_29, loc_21, loc_0)
			::continue_at_250::
			if loc_26 ~= 65536 then
				goto continue_at_251
			end
			if loc_24 <= loc_20 then
				goto continue_at_251
			end
			loc_19 = sub_i32(loc_17, loc_20)
			loc_21 = (lt_u32(loc_19, 256) and 1 or 0)
			loc_29 = (loc_21 ~= 0 and loc_19 or 256)
			if loc_29 == 0 then
				goto continue_at_252
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 96), loc_29, 48)
			::continue_at_252::
			if loc_21 ~= 0 then
				goto continue_at_253
			end
			::continue_at_254::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_255
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), 256, loc_0)
				::continue_at_255::
				loc_19 = add_i32(loc_19, -256)
				if gt_u32(loc_19, 255) then
					goto continue_at_254
				end
				break
			end
			::continue_at_253::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_251
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), loc_19, loc_0)
			::continue_at_251::
			if loc_23 <= loc_22 then
				goto continue_at_256
			end
			loc_19 = sub_i32(loc_25, loc_22)
			loc_23 = (lt_u32(loc_19, 256) and 1 or 0)
			loc_25 = (loc_23 ~= 0 and loc_19 or 256)
			if loc_25 == 0 then
				goto continue_at_257
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 96), loc_25, 48)
			::continue_at_257::
			if loc_23 ~= 0 then
				goto continue_at_258
			end
			::continue_at_259::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_260
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), 256, loc_0)
				::continue_at_260::
				loc_19 = add_i32(loc_19, -256)
				if gt_u32(loc_19, 255) then
					goto continue_at_259
				end
				break
			end
			::continue_at_258::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_256
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), loc_19, loc_0)
			::continue_at_256::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_261
			end
			reg_0 = FUNC_LIST[39](loc_18, loc_22, loc_0)
			::continue_at_261::
			if loc_26 ~= 8192 then
				goto continue_at_5
			end
			if loc_24 <= loc_20 then
				goto continue_at_5
			end
			loc_18 = sub_i32(loc_17, loc_20)
			loc_19 = (lt_u32(loc_18, 256) and 1 or 0)
			loc_20 = (loc_19 ~= 0 and loc_18 or 256)
			if loc_20 == 0 then
				goto continue_at_262
			end
			rt.store.fill(memory_at_0, add_i32(loc_5, 96), loc_20, 32)
			::continue_at_262::
			if loc_19 ~= 0 then
				goto continue_at_263
			end
			::continue_at_264::
			while true do
				if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
					goto continue_at_265
				end
				reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), 256, loc_0)
				::continue_at_265::
				loc_18 = add_i32(loc_18, -256)
				if gt_u32(loc_18, 255) then
					goto continue_at_264
				end
				break
			end
			::continue_at_263::
			if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
				goto continue_at_5
			end
			reg_0 = FUNC_LIST[39](add_i32(loc_5, 96), loc_18, loc_0)
			goto continue_at_5
		end
		::continue_at_4::
		break
	end
	store_i32(memory_at_0, 0 + 4484, 61)
	::continue_at_2::
	loc_16 = -1
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_5, 864)
	reg_0 = loc_16
	return reg_0
end
FUNC_LIST[52] = function(loc_0, loc_1, loc_2)
	local br_map, temp = {}, nil
	if not br_map[1] then
		br_map[1] = (function()
			return { [0] = 17, 0, 1, 4, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, }
		end)()
	end
	temp = br_map[1][add_i32(loc_1, -9)] or 18
	if temp < 9 then
		if temp < 4 then
			if temp < 2 then
				if temp < 1 then
					goto continue_at_19
				else
					goto continue_at_18
				end
			elseif temp > 2 then
				goto continue_at_16
			else
				goto continue_at_17
			end
		elseif temp > 4 then
			if temp < 7 then
				if temp < 6 then
					goto continue_at_14
				else
					goto continue_at_13
				end
			elseif temp > 7 then
				goto continue_at_11
			else
				goto continue_at_12
			end
		else
			goto continue_at_15
		end
	elseif temp > 9 then
		if temp < 14 then
			if temp < 12 then
				if temp < 11 then
					goto continue_at_9
				else
					goto continue_at_8
				end
			elseif temp > 12 then
				goto continue_at_6
			else
				goto continue_at_7
			end
		elseif temp > 14 then
			if temp < 17 then
				if temp < 16 then
					goto continue_at_4
				else
					goto continue_at_3
				end
			elseif temp > 17 then
				goto continue_at_1
			else
				goto continue_at_2
			end
		else
			goto continue_at_5
		end
	else
		goto continue_at_10
	end
	::continue_at_19::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_i32(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_18::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_u32(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_17::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_i32(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_16::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_u32(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_15::
	loc_1 = band_i32(add_i32(load_i32(memory_at_0, loc_2), 7), -8)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 8))
	store_i64(memory_at_0, loc_0, load_i64(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_14::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_i16(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_13::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_u16(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_12::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_i8(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_11::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_u8(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_10::
	loc_1 = band_i32(add_i32(load_i32(memory_at_0, loc_2), 7), -8)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 8))
	store_i64(memory_at_0, loc_0, load_i64(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_9::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_u32(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_8::
	loc_1 = band_i32(add_i32(load_i32(memory_at_0, loc_2), 7), -8)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 8))
	store_i64(memory_at_0, loc_0, load_i64(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_7::
	loc_1 = band_i32(add_i32(load_i32(memory_at_0, loc_2), 7), -8)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 8))
	store_i64(memory_at_0, loc_0, load_i64(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_6::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_i32(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_5::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i64(memory_at_0, loc_0, load_i64_u32(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_4::
	loc_1 = band_i32(add_i32(load_i32(memory_at_0, loc_2), 7), -8)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 8))
	store_f64(memory_at_0, loc_0, load_f64(memory_at_0, loc_1))
	goto continue_at_0
	::continue_at_3::
	FUNC_LIST[54]()
	error("out of code bounds")
	::continue_at_2::
	loc_1 = load_i32(memory_at_0, loc_2)
	store_i32(memory_at_0, loc_2, add_i32(loc_1, 4))
	store_i32(memory_at_0, loc_0, load_i32(memory_at_0, loc_1))
	::continue_at_1::
	::continue_at_0::
end
FUNC_LIST[53] = function(loc_0, loc_1, loc_2, loc_3, loc_4)
	local loc_5 = 0
	local reg_0
	loc_5 = sub_i32(GLOBAL_LIST[0].value, 256)
	GLOBAL_LIST[0].value = loc_5
	if loc_2 <= loc_3 then
		goto continue_at_1
	end
	if band_i32(loc_4, 73728) ~= 0 then
		goto continue_at_1
	end
	loc_3 = sub_i32(loc_2, loc_3)
	loc_2 = (lt_u32(loc_3, 256) and 1 or 0)
	loc_4 = (loc_2 ~= 0 and loc_3 or 256)
	if loc_4 == 0 then
		goto continue_at_2
	end
	rt.store.fill(memory_at_0, loc_5, loc_4, loc_1)
	::continue_at_2::
	if loc_2 ~= 0 then
		goto continue_at_3
	end
	::continue_at_4::
	while true do
		if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
			goto continue_at_5
		end
		reg_0 = FUNC_LIST[39](loc_5, 256, loc_0)
		::continue_at_5::
		loc_3 = add_i32(loc_3, -256)
		if gt_u32(loc_3, 255) then
			goto continue_at_4
		end
		break
	end
	::continue_at_3::
	if band_i32(load_i32_u8(memory_at_0, loc_0), 32) ~= 0 then
		goto continue_at_1
	end
	reg_0 = FUNC_LIST[39](loc_5, loc_3, loc_0)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_5, 256)
end
FUNC_LIST[54] = function()
	local reg_0
	reg_0 = FUNC_LIST[49](2846, 4104)
	FUNC_LIST[21]()
	error("out of code bounds")
end
FUNC_LIST[55] = function(loc_0, loc_1)
	local loc_2 = 0
	local reg_0
	loc_2 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_2
	store_i32(memory_at_0, loc_2 + 12, loc_1)
	reg_0 = FUNC_LIST[50](3984, loc_0, loc_1)
	loc_1 = reg_0
	GLOBAL_LIST[0].value = add_i32(loc_2, 16)
	reg_0 = loc_1
	return reg_0
end
FUNC_LIST[56] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local loc_3 = 0
	local reg_0
	if loc_0 ~= 0 then
		goto continue_at_1
	end
	loc_1 = 0
	if load_i32(memory_at_0, 0 + 4096) == 0 then
		goto continue_at_2
	end
	reg_0 = FUNC_LIST[56](load_i32(memory_at_0, 0 + 4096))
	loc_1 = reg_0
	::continue_at_2::
	if load_i32(memory_at_0, 0 + 4216) == 0 then
		goto continue_at_3
	end
	reg_0 = FUNC_LIST[56](load_i32(memory_at_0, 0 + 4216))
	loc_1 = bor_i32(reg_0, loc_1)
	::continue_at_3::
	reg_0 = FUNC_LIST[35]()
	loc_0 = load_i32(memory_at_0, reg_0)
	if loc_0 == 0 then
		goto continue_at_4
	end
	::continue_at_5::
	while true do
		if load_i32(memory_at_0, loc_0 + 20) == load_i32(memory_at_0, loc_0 + 24) then
			goto continue_at_6
		end
		reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
		if load_i32(memory_at_0, loc_0 + 20) ~= 0 then
			goto continue_at_8
		end
		loc_2 = -1
		goto continue_at_7
		::continue_at_8::
		loc_2 = load_i32(memory_at_0, loc_0 + 4)
		loc_3 = load_i32(memory_at_0, loc_0 + 8)
		if loc_2 == loc_3 then
			goto continue_at_9
		end
		reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 36)](loc_0, extend_i64_i32(sub_i32(loc_2, loc_3)), 1)
		::continue_at_9::
		loc_2 = 0
		store_i32(memory_at_0, loc_0 + 24, 0)
		store_i64(memory_at_0, loc_0 + 16, 0LL)
		store_i64(memory_at_0, loc_0 + 4, 0LL)
		::continue_at_7::
		loc_1 = bor_i32(loc_2, loc_1)
		::continue_at_6::
		loc_0 = load_i32(memory_at_0, loc_0 + 52)
		if loc_0 ~= 0 then
			goto continue_at_5
		end
		break
	end
	::continue_at_4::
	FUNC_LIST[36]()
	reg_0 = loc_1
	goto continue_at_0
	::continue_at_1::
	if load_i32(memory_at_0, loc_0 + 20) == load_i32(memory_at_0, loc_0 + 24) then
		goto continue_at_10
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
	if load_i32(memory_at_0, loc_0 + 20) ~= 0 then
		goto continue_at_10
	end
	reg_0 = -1
	goto continue_at_0
	::continue_at_10::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	loc_2 = load_i32(memory_at_0, loc_0 + 8)
	if loc_1 == loc_2 then
		goto continue_at_11
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 36)](loc_0, extend_i64_i32(sub_i32(loc_1, loc_2)), 1)
	::continue_at_11::
	store_i32(memory_at_0, loc_0 + 24, 0)
	store_i64(memory_at_0, loc_0 + 16, 0LL)
	store_i64(memory_at_0, loc_0 + 4, 0LL)
	reg_0 = 0
	::continue_at_0::
	return reg_0
end
FUNC_LIST[57] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local reg_0
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_3
	loc_4 = -1
	if loc_2 > -1 then
		goto continue_at_2
	end
	store_i32(memory_at_0, 0 + 4484, 28)
	goto continue_at_1
	::continue_at_2::
	reg_0 = FUNC_LIST[17](loc_0, loc_1, loc_2, add_i32(loc_3, 12))
	loc_2 = reg_0
	if loc_2 == 0 then
		goto continue_at_3
	end
	store_i32(memory_at_0, 0 + 4484, loc_2)
	loc_4 = -1
	goto continue_at_1
	::continue_at_3::
	loc_4 = load_i32(memory_at_0, loc_3 + 12)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 16)
	reg_0 = loc_4
	return reg_0
end
FUNC_LIST[58] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local reg_0
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_3
	store_i32(memory_at_0, loc_3 + 12, loc_2)
	store_i32(memory_at_0, loc_3 + 8, loc_1)
	reg_0 = FUNC_LIST[17](loc_0, add_i32(loc_3, 8), 1, add_i32(loc_3, 4))
	loc_2 = reg_0
	if loc_2 == 0 then
		goto continue_at_2
	end
	store_i32(memory_at_0, 0 + 4484, (loc_2 == 76 and 8 or loc_2))
	loc_2 = -1
	goto continue_at_1
	::continue_at_2::
	loc_2 = load_i32(memory_at_0, loc_3 + 4)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 16)
	reg_0 = loc_2
	return reg_0
end
FUNC_LIST[59] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local reg_0
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_3
	store_i32(memory_at_0, loc_3, loc_1)
	loc_4 = load_i32(memory_at_0, loc_0 + 44)
	store_i32(memory_at_0, loc_3 + 12, loc_4)
	loc_5 = load_i32(memory_at_0, loc_0 + 40)
	store_i32(memory_at_0, loc_3 + 8, loc_5)
	loc_6 = sub_i32(loc_2, (loc_4 ~= 0 and 1 or 0))
	store_i32(memory_at_0, loc_3 + 4, loc_6)
	loc_7 = load_i32(memory_at_0, loc_0 + 56)
	if loc_6 == 0 then
		goto continue_at_2
	end
	reg_0 = FUNC_LIST[57](loc_7, loc_3, 2)
	loc_4 = reg_0
	goto continue_at_1
	::continue_at_2::
	reg_0 = FUNC_LIST[58](loc_7, loc_5, loc_4)
	loc_4 = reg_0
	::continue_at_1::
	loc_6 = 0
	if loc_4 > 0 then
		goto continue_at_4
	end
	store_i32(memory_at_0, loc_0, bor_i32(load_i32(memory_at_0, loc_0), (loc_4 ~= 0 and 32 or 16)))
	goto continue_at_3
	::continue_at_4::
	loc_7 = load_i32(memory_at_0, loc_3 + 4)
	if gt_u32(loc_4, loc_7) then
		goto continue_at_5
	end
	loc_6 = loc_4
	goto continue_at_3
	::continue_at_5::
	loc_6 = load_i32(memory_at_0, loc_0 + 40)
	store_i32(memory_at_0, loc_0 + 4, loc_6)
	store_i32(memory_at_0, loc_0 + 8, add_i32(loc_6, sub_i32(loc_4, loc_7)))
	if load_i32(memory_at_0, loc_0 + 44) == 0 then
		goto continue_at_6
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_6, 1))
	store_i32_n8(memory_at_0, add_i32(add_i32(loc_1, loc_2), -1), load_i32_u8(memory_at_0, loc_6))
	::continue_at_6::
	loc_6 = loc_2
	::continue_at_3::
	GLOBAL_LIST[0].value = add_i32(loc_3, 16)
	reg_0 = loc_6
	return reg_0
end
FUNC_LIST[60] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local reg_0
	loc_1 = load_i32(memory_at_0, loc_0 + 60)
	store_i32(memory_at_0, loc_0 + 60, bor_i32(add_i32(loc_1, -1), loc_1))
	if load_i32(memory_at_0, loc_0 + 20) == load_i32(memory_at_0, loc_0 + 24) then
		goto continue_at_1
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, 0, 0)
	::continue_at_1::
	store_i32(memory_at_0, loc_0 + 24, 0)
	store_i64(memory_at_0, loc_0 + 16, 0LL)
	loc_1 = load_i32(memory_at_0, loc_0)
	if band_i32(loc_1, 4) == 0 then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_0, bor_i32(loc_1, 32))
	reg_0 = -1
	goto continue_at_0
	::continue_at_2::
	loc_2 = add_i32(load_i32(memory_at_0, loc_0 + 40), load_i32(memory_at_0, loc_0 + 44))
	store_i32(memory_at_0, loc_0 + 8, loc_2)
	store_i32(memory_at_0, loc_0 + 4, loc_2)
	reg_0 = shr_i32(shl_i32(loc_1, 27), 31)
	::continue_at_0::
	return reg_0
end
FUNC_LIST[61] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local reg_0
	loc_1 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_1
	loc_2 = -1
	reg_0 = FUNC_LIST[60](loc_0)
	if reg_0 ~= 0 then
		goto continue_at_1
	end
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 28)](loc_0, add_i32(loc_1, 15), 1)
	if reg_0 ~= 1 then
		goto continue_at_1
	end
	loc_2 = load_i32_u8(memory_at_0, loc_1 + 15)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_1, 16)
	reg_0 = loc_2
	return reg_0
end
FUNC_LIST[62] = function(loc_0, loc_1)
	local loc_2 = 0
	local loc_3 = 0
	store_i64(memory_at_0, loc_0 + 88, loc_1)
	loc_2 = load_i32(memory_at_0, loc_0 + 4)
	store_i64(memory_at_0, loc_0 + 96, extend_i64_i32(sub_i32(load_i32(memory_at_0, loc_0 + 40), loc_2)))
	loc_3 = load_i32(memory_at_0, loc_0 + 8)
	if loc_1 == 0LL then
		goto continue_at_1
	end
	if loc_1 >= extend_i64_i32(sub_i32(loc_3, loc_2)) then
		goto continue_at_1
	end
	loc_3 = add_i32(loc_2, wrap_i32_i64(loc_1))
	::continue_at_1::
	store_i32(memory_at_0, loc_0 + 84, loc_3)
end
FUNC_LIST[63] = function(loc_0)
	local loc_1 = 0
	local loc_2 = 0
	local loc_3 = 0LL
	local loc_4 = 0LL
	local loc_5 = 0
	local reg_0
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	loc_2 = load_i32(memory_at_0, loc_0 + 40)
	loc_3 = (load_i64(memory_at_0, loc_0 + 96) + extend_i64_i32(sub_i32(loc_1, loc_2)))
	loc_4 = load_i64(memory_at_0, loc_0 + 88)
	if loc_4 == 0LL then
		goto continue_at_3
	end
	if loc_3 >= loc_4 then
		goto continue_at_2
	end
	::continue_at_3::
	reg_0 = FUNC_LIST[61](loc_0)
	loc_2 = reg_0
	if loc_2 > -1 then
		goto continue_at_1
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	loc_2 = load_i32(memory_at_0, loc_0 + 40)
	::continue_at_2::
	store_i64(memory_at_0, loc_0 + 88, -1LL)
	store_i32(memory_at_0, loc_0 + 84, loc_1)
	store_i64(memory_at_0, loc_0 + 96, (loc_3 + extend_i64_i32(sub_i32(loc_2, loc_1))))
	reg_0 = -1
	goto continue_at_0
	::continue_at_1::
	loc_3 = (loc_3 + 1LL)
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	loc_5 = load_i32(memory_at_0, loc_0 + 8)
	loc_4 = load_i64(memory_at_0, loc_0 + 88)
	if loc_4 == 0LL then
		goto continue_at_4
	end
	loc_4 = (loc_4 - loc_3)
	if loc_4 >= extend_i64_i32(sub_i32(loc_5, loc_1)) then
		goto continue_at_4
	end
	loc_5 = add_i32(loc_1, wrap_i32_i64(loc_4))
	::continue_at_4::
	store_i32(memory_at_0, loc_0 + 84, loc_5)
	loc_5 = load_i32(memory_at_0, loc_0 + 40)
	store_i64(memory_at_0, loc_0 + 96, (loc_3 + extend_i64_i32(sub_i32(loc_5, loc_1))))
	if gt_u32(loc_1, loc_5) then
		goto continue_at_5
	end
	store_i32_n8(memory_at_0, add_i32(loc_1, -1), loc_2)
	::continue_at_5::
	reg_0 = loc_2
	::continue_at_0::
	return reg_0
end
FUNC_LIST[64] = function(loc_0, loc_1, loc_2, loc_3)
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0LL
	local loc_8 = 0LL
	local loc_9 = 0LL
	local loc_10 = 0
	local loc_11 = 0LL
	local loc_12 = 0
	local loc_13 = 0
	local reg_0
	local br_map, temp = {}, nil
	loc_4 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_4
	if gt_u32(loc_1, 36) then
		goto continue_at_5
	end
	if loc_1 == 1 then
		goto continue_at_5
	end
	::continue_at_8::
	while true do
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_10
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_9
		::continue_at_10::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_9::
		if lt_u32(add_i32(loc_5, -9), 5) then
			goto continue_at_8
		end
		if not br_map[1] then
			br_map[1] = (function()
				return { [0] = 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, }
			end)()
		end
		temp = br_map[1][add_i32(loc_5, -32)] or 2
		if temp < 1 then
			goto continue_at_11
		elseif temp > 1 then
			goto continue_at_7
		else
			goto continue_at_8
		end
		::continue_at_11::
		break
	end
	loc_6 = (loc_5 == 45 and -1 or 0)
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_12
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
	loc_5 = load_i32_u8(memory_at_0, loc_5)
	goto continue_at_6
	::continue_at_12::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_5 = reg_0
	goto continue_at_6
	::continue_at_7::
	loc_6 = 0
	::continue_at_6::
	if band_i32((loc_1 ~= 0 and 1 or 0), (loc_1 ~= 16 and 1 or 0)) ~= 0 then
		goto continue_at_14
	end
	if loc_5 ~= 48 then
		goto continue_at_14
	end
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_16
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
	loc_5 = load_i32_u8(memory_at_0, loc_5)
	goto continue_at_15
	::continue_at_16::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_5 = reg_0
	::continue_at_15::
	if band_i32(loc_5, -33) ~= 88 then
		goto continue_at_17
	end
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_19
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
	loc_5 = load_i32_u8(memory_at_0, loc_5)
	goto continue_at_18
	::continue_at_19::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_5 = reg_0
	::continue_at_18::
	loc_1 = 16
	if lt_u32(load_i32_u8(memory_at_0, add_i32(loc_5, 3473)), 16) then
		goto continue_at_4
	end
	loc_3 = 0LL
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_21
	end
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, -1))
	if loc_2 == 0 then
		goto continue_at_20
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, -2))
	goto continue_at_1
	::continue_at_21::
	if loc_2 ~= 0 then
		goto continue_at_1
	end
	::continue_at_20::
	loc_3 = 0LL
	FUNC_LIST[62](loc_0, 0LL)
	goto continue_at_1
	::continue_at_17::
	if loc_1 ~= 0 then
		goto continue_at_13
	end
	loc_1 = 8
	goto continue_at_4
	::continue_at_14::
	loc_1 = (loc_1 ~= 0 and loc_1 or 10)
	if gt_u32(loc_1, load_i32_u8(memory_at_0, add_i32(loc_5, 3473))) then
		goto continue_at_13
	end
	loc_3 = 0LL
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_22
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_22::
	FUNC_LIST[62](loc_0, 0LL)
	store_i32(memory_at_0, 0 + 4484, 28)
	goto continue_at_1
	::continue_at_13::
	if loc_1 ~= 10 then
		goto continue_at_4
	end
	loc_7 = 0LL
	loc_2 = add_i32(loc_5, -48)
	if gt_u32(loc_2, 9) then
		goto continue_at_23
	end
	loc_5 = 0
	::continue_at_24::
	while true do
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_26
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
		loc_1 = load_i32_u8(memory_at_0, loc_1)
		goto continue_at_25
		::continue_at_26::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_1 = reg_0
		::continue_at_25::
		loc_5 = add_i32(mul_i32(loc_5, 10), loc_2)
		loc_2 = add_i32(loc_1, -48)
		if gt_u32(loc_2, 9) then
			goto continue_at_27
		end
		if lt_u32(loc_5, 429496729) then
			goto continue_at_24
		end
		::continue_at_27::
		break
	end
	loc_7 = extend_i64_u32(loc_5)
	::continue_at_23::
	if gt_u32(loc_2, 9) then
		goto continue_at_2
	end
	loc_8 = (loc_7 * 10LL)
	loc_9 = extend_i64_u32(loc_2)
	::continue_at_28::
	while true do
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_30
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_29
		::continue_at_30::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_29::
		loc_7 = (loc_8 + loc_9)
		loc_1 = add_i32(loc_5, -48)
		if gt_u32(loc_1, 9) then
			goto continue_at_32
		end
		if lt_u64(loc_7, 1844674407370955162LL) then
			goto continue_at_31
		end
		::continue_at_32::
		if gt_u32(loc_1, 9) then
			goto continue_at_2
		end
		loc_1 = 10
		goto continue_at_3
		::continue_at_31::
		loc_8 = (loc_7 * 10LL)
		loc_9 = extend_i64_u32(loc_1)
		if le_u64(loc_8, bxor_i64(loc_9, -1LL)) then
			goto continue_at_28
		end
		break
	end
	loc_1 = 10
	goto continue_at_3
	::continue_at_5::
	store_i32(memory_at_0, 0 + 4484, 28)
	loc_3 = 0LL
	goto continue_at_1
	::continue_at_4::
	if band_i32(loc_1, add_i32(loc_1, -1)) == 0 then
		goto continue_at_33
	end
	loc_7 = 0LL
	loc_10 = load_i32_u8(memory_at_0, add_i32(loc_5, 3473))
	if le_u32(loc_1, loc_10) then
		goto continue_at_34
	end
	loc_2 = 0
	::continue_at_35::
	while true do
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_37
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_36
		::continue_at_37::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_36::
		loc_2 = add_i32(loc_10, mul_i32(loc_2, loc_1))
		loc_10 = load_i32_u8(memory_at_0, add_i32(loc_5, 3473))
		if le_u32(loc_1, loc_10) then
			goto continue_at_38
		end
		if lt_u32(loc_2, 119304647) then
			goto continue_at_35
		end
		::continue_at_38::
		break
	end
	loc_7 = extend_i64_u32(loc_2)
	::continue_at_34::
	if le_u32(loc_1, loc_10) then
		goto continue_at_3
	end
	loc_8 = extend_i64_u32(loc_1)
	::continue_at_39::
	while true do
		loc_9 = (loc_7 * loc_8)
		loc_11 = band_i64(extend_i64_u32(loc_10), 255LL)
		if gt_u64(loc_9, bxor_i64(loc_11, -1LL)) then
			goto continue_at_3
		end
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_41
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_40
		::continue_at_41::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_40::
		loc_7 = (loc_9 + loc_11)
		loc_10 = load_i32_u8(memory_at_0, add_i32(loc_5, 3473))
		if le_u32(loc_1, loc_10) then
			goto continue_at_3
		end
		FUNC_LIST[79](loc_4, loc_8, 0LL, loc_7, 0LL)
		if load_i64(memory_at_0, loc_4 + 8) ~= 0LL then
			goto continue_at_3
		end
		goto continue_at_39
	end
	::continue_at_33::
	loc_12 = load_i32_i8(memory_at_0, add_i32(band_i32(shr_u32(mul_i32(loc_1, 23), 5), 7), 3729))
	loc_7 = 0LL
	loc_2 = load_i32_u8(memory_at_0, add_i32(loc_5, 3473))
	if le_u32(loc_1, loc_2) then
		goto continue_at_42
	end
	loc_10 = 0
	::continue_at_43::
	while true do
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_45
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_44
		::continue_at_45::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_44::
		loc_13 = shl_i32(loc_10, loc_12)
		loc_10 = bor_i32(loc_2, loc_13)
		loc_2 = load_i32_u8(memory_at_0, add_i32(loc_5, 3473))
		if le_u32(loc_1, loc_2) then
			goto continue_at_46
		end
		if lt_u32(loc_13, 134217728) then
			goto continue_at_43
		end
		::continue_at_46::
		break
	end
	loc_7 = extend_i64_u32(loc_10)
	::continue_at_42::
	if le_u32(loc_1, loc_2) then
		goto continue_at_3
	end
	loc_9 = extend_i64_u32(loc_12)
	loc_11 = shr_u64(-1LL, loc_9)
	if lt_u64(loc_11, loc_7) then
		goto continue_at_3
	end
	::continue_at_47::
	while true do
		loc_8 = band_i64(extend_i64_u32(loc_2), 255LL)
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_49
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_48
		::continue_at_49::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_48::
		loc_7 = bor_i64(shl_i64(loc_7, loc_9), loc_8)
		loc_2 = load_i32_u8(memory_at_0, add_i32(loc_5, 3473))
		if le_u32(loc_1, loc_2) then
			goto continue_at_3
		end
		if le_u64(loc_7, loc_11) then
			goto continue_at_47
		end
		break
	end
	::continue_at_3::
	if le_u32(loc_1, load_i32_u8(memory_at_0, add_i32(loc_5, 3473))) then
		goto continue_at_2
	end
	::continue_at_50::
	while true do
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_52
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_51
		::continue_at_52::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_51::
		if gt_u32(loc_1, load_i32_u8(memory_at_0, add_i32(loc_5, 3473))) then
			goto continue_at_50
		end
		break
	end
	store_i32(memory_at_0, 0 + 4484, 68)
	loc_6 = (band_i64(loc_3, 1LL) == 0LL and loc_6 or 0)
	loc_7 = loc_3
	::continue_at_2::
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_53
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_53::
	if lt_u64(loc_7, loc_3) then
		goto continue_at_54
	end
	if band_i32(wrap_i32_i64(loc_3), 1) ~= 0 then
		goto continue_at_55
	end
	if loc_6 ~= 0 then
		goto continue_at_55
	end
	store_i32(memory_at_0, 0 + 4484, 68)
	loc_3 = (loc_3 + -1LL)
	goto continue_at_1
	::continue_at_55::
	if le_u64(loc_7, loc_3) then
		goto continue_at_54
	end
	store_i32(memory_at_0, 0 + 4484, 68)
	goto continue_at_1
	::continue_at_54::
	loc_3 = extend_i64_i32(loc_6)
	loc_3 = (bxor_i64(loc_7, loc_3) - loc_3)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_4, 16)
	reg_0 = loc_3
	return reg_0
end
FUNC_LIST[65] = function(loc_0, loc_1)
	local reg_0
	if loc_1 < 1024 then
		goto continue_at_2
	end
	loc_0 = (loc_0 * 8.98846567431158e307)
	if ge_u32(loc_1, 2047) then
		goto continue_at_3
	end
	loc_1 = add_i32(loc_1, -1023)
	goto continue_at_1
	::continue_at_3::
	loc_0 = (loc_0 * 8.98846567431158e307)
	loc_1 = add_i32((lt_u32(loc_1, 3069) and loc_1 or 3069), -2046)
	goto continue_at_1
	::continue_at_2::
	if loc_1 > -1023 then
		goto continue_at_1
	end
	loc_0 = (loc_0 * 2.004168360008973e-292)
	if le_u32(loc_1, -1992) then
		goto continue_at_4
	end
	loc_1 = add_i32(loc_1, 969)
	goto continue_at_1
	::continue_at_4::
	loc_0 = (loc_0 * 2.004168360008973e-292)
	loc_1 = add_i32((gt_u32(loc_1, -2960) and loc_1 or -2960), 1938)
	::continue_at_1::
	reg_0 = (loc_0 * reinterpret_f64_i64(shl_i64(extend_i64_u32(add_i32(loc_1, 1023)), 52LL)))
	return reg_0
end
FUNC_LIST[66] = function(loc_0, loc_1)
	local loc_2 = 0LL
	local loc_3 = 0LL
	local loc_4 = 0LL
	local loc_5 = 0
	local loc_6 = 0LL
	local loc_7 = 0
	local reg_0
	loc_2 = reinterpret_i64_f64(loc_1)
	loc_3 = shl_i64(loc_2, 1LL)
	if loc_3 == 0LL then
		goto continue_at_2
	end
	if loc_1 ~= loc_1 then
		goto continue_at_2
	end
	loc_4 = reinterpret_i64_f64(loc_0)
	loc_5 = band_i32(wrap_i32_i64(shr_u64(loc_4, 52LL)), 2047)
	if loc_5 ~= 2047 then
		goto continue_at_1
	end
	::continue_at_2::
	loc_1 = (loc_0 * loc_1)
	reg_0 = (loc_1 / loc_1)
	goto continue_at_0
	::continue_at_1::
	loc_6 = shl_i64(loc_4, 1LL)
	if gt_u64(loc_6, loc_3) then
		goto continue_at_3
	end
	reg_0 = (loc_6 == loc_3 and (loc_0 * 0e0) or loc_0)
	goto continue_at_0
	::continue_at_3::
	loc_7 = band_i32(wrap_i32_i64(shr_u64(loc_2, 52LL)), 2047)
	if loc_5 ~= 0 then
		goto continue_at_5
	end
	loc_5 = 0
	loc_3 = shl_i64(loc_4, 12LL)
	if loc_3 < 0LL then
		goto continue_at_6
	end
	::continue_at_7::
	while true do
		loc_5 = add_i32(loc_5, -1)
		loc_3 = shl_i64(loc_3, 1LL)
		if loc_3 > -1LL then
			goto continue_at_7
		end
		break
	end
	::continue_at_6::
	loc_3 = shl_i64(loc_4, extend_i64_u32(sub_i32(1, loc_5)))
	goto continue_at_4
	::continue_at_5::
	loc_3 = bor_i64(band_i64(loc_4, 4503599627370495LL), 4503599627370496LL)
	::continue_at_4::
	if loc_7 ~= 0 then
		goto continue_at_9
	end
	loc_7 = 0
	loc_6 = shl_i64(loc_2, 12LL)
	if loc_6 < 0LL then
		goto continue_at_10
	end
	::continue_at_11::
	while true do
		loc_7 = add_i32(loc_7, -1)
		loc_6 = shl_i64(loc_6, 1LL)
		if loc_6 > -1LL then
			goto continue_at_11
		end
		break
	end
	::continue_at_10::
	loc_2 = shl_i64(loc_2, extend_i64_u32(sub_i32(1, loc_7)))
	goto continue_at_8
	::continue_at_9::
	loc_2 = bor_i64(band_i64(loc_2, 4503599627370495LL), 4503599627370496LL)
	::continue_at_8::
	if loc_5 <= loc_7 then
		goto continue_at_12
	end
	::continue_at_13::
	while true do
		loc_6 = (loc_3 - loc_2)
		if loc_6 < 0LL then
			goto continue_at_14
		end
		loc_3 = loc_6
		if loc_6 ~= 0LL then
			goto continue_at_14
		end
		reg_0 = (loc_0 * 0e0)
		goto continue_at_0
		::continue_at_14::
		loc_3 = shl_i64(loc_3, 1LL)
		loc_5 = add_i32(loc_5, -1)
		if loc_5 > loc_7 then
			goto continue_at_13
		end
		break
	end
	loc_5 = loc_7
	::continue_at_12::
	loc_6 = (loc_3 - loc_2)
	if loc_6 < 0LL then
		goto continue_at_15
	end
	loc_3 = loc_6
	if loc_6 ~= 0LL then
		goto continue_at_15
	end
	reg_0 = (loc_0 * 0e0)
	goto continue_at_0
	::continue_at_15::
	if le_u64(loc_3, 4503599627370495LL) then
		goto continue_at_17
	end
	loc_6 = loc_3
	goto continue_at_16
	::continue_at_17::
	::continue_at_18::
	while true do
		loc_5 = add_i32(loc_5, -1)
		loc_7 = (lt_u64(loc_3, 2251799813685248LL) and 1 or 0)
		loc_6 = shl_i64(loc_3, 1LL)
		loc_3 = loc_6
		if loc_7 ~= 0 then
			goto continue_at_18
		end
		break
	end
	::continue_at_16::
	loc_3 = band_i64(loc_4, -9223372036854775808LL)
	if loc_5 < 1 then
		goto continue_at_20
	end
	loc_6 = bor_i64((loc_6 + -4503599627370496LL), shl_i64(extend_i64_u32(loc_5), 52LL))
	goto continue_at_19
	::continue_at_20::
	loc_6 = shr_u64(loc_6, extend_i64_u32(sub_i32(1, loc_5)))
	::continue_at_19::
	reg_0 = reinterpret_f64_i64(bor_i64(loc_6, loc_3))
	::continue_at_0::
	return reg_0
end
FUNC_LIST[67] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0.0
	local loc_8 = 0
	local loc_9 = 0
	local loc_10 = 0LL
	local loc_11 = 0
	local loc_12 = 0
	local loc_13 = 0
	local loc_14 = 0
	local loc_15 = 0
	local loc_16 = 0
	local loc_17 = 0
	local loc_18 = 0LL
	local loc_19 = 0
	local loc_20 = 0LL
	local loc_21 = 0
	local loc_22 = 0
	local loc_23 = 0.0
	local loc_24 = 0.0
	local loc_25 = 0.0
	local reg_0
	local reg_1
	local reg_2
	local reg_3
	local br_map, temp = {}, nil
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 512)
	GLOBAL_LIST[0].value = loc_3
	loc_4 = -149
	loc_5 = 24
	loc_6 = 0
	loc_7 = 0e0
	if not br_map[1] then
		br_map[1] = (function()
			return { [0] = 1, 0, 0, }
		end)()
	end
	temp = br_map[1][loc_1] or 2
	if temp < 1 then
		goto continue_at_3
	elseif temp > 1 then
		goto continue_at_1
	else
		goto continue_at_2
	end
	::continue_at_3::
	loc_4 = -1074
	loc_5 = 53
	loc_6 = 1
	::continue_at_2::
	::continue_at_6::
	while true do
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_8
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
		loc_1 = load_i32_u8(memory_at_0, loc_1)
		goto continue_at_7
		::continue_at_8::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_1 = reg_0
		::continue_at_7::
		if lt_u32(add_i32(loc_1, -9), 5) then
			goto continue_at_6
		end
		if not br_map[2] then
			br_map[2] = (function()
				return { [0] = 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, }
			end)()
		end
		temp = br_map[2][add_i32(loc_1, -32)] or 2
		if temp < 1 then
			goto continue_at_9
		elseif temp > 1 then
			goto continue_at_5
		else
			goto continue_at_6
		end
		::continue_at_9::
		break
	end
	loc_8 = (loc_1 == 45 and -1 or 1)
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_10
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_4
	::continue_at_10::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	goto continue_at_4
	::continue_at_5::
	loc_8 = 1
	::continue_at_4::
	loc_9 = band_i32(loc_1, -33)
	if loc_9 ~= 73 then
		goto continue_at_13
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_15
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_14
	::continue_at_15::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_14::
	if band_i32(loc_1, -33) ~= 78 then
		goto continue_at_12
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_17
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_16
	::continue_at_17::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_16::
	if band_i32(loc_1, -33) ~= 70 then
		goto continue_at_12
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_19
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_9 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_18
	::continue_at_19::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_9 = reg_0
	::continue_at_18::
	loc_1 = 3
	loc_9 = band_i32(loc_9, -33)
	if loc_9 ~= 73 then
		goto continue_at_21
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_23
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_22
	::continue_at_23::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_22::
	if band_i32(loc_1, -33) == 78 then
		goto continue_at_25
	end
	loc_1 = 4
	goto continue_at_24
	::continue_at_25::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_27
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_26
	::continue_at_27::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_26::
	if band_i32(loc_1, -33) == 73 then
		goto continue_at_28
	end
	loc_1 = 5
	goto continue_at_24
	::continue_at_28::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_30
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_29
	::continue_at_30::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_29::
	if band_i32(loc_1, -33) == 84 then
		goto continue_at_31
	end
	loc_1 = 6
	goto continue_at_24
	::continue_at_31::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_33
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_32
	::continue_at_33::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_32::
	if band_i32(loc_1, -33) == 89 then
		goto continue_at_20
	end
	loc_1 = 7
	::continue_at_24::
	if loc_2 == 0 then
		goto continue_at_12
	end
	::continue_at_21::
	loc_10 = load_i64(memory_at_0, loc_0 + 88)
	if loc_10 < 0LL then
		goto continue_at_34
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_34::
	if loc_2 == 0 then
		goto continue_at_20
	end
	if loc_9 ~= 73 then
		goto continue_at_20
	end
	if loc_10 < 0LL then
		goto continue_at_35
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_35::
	if gt_u32(add_i32(loc_1, -5), -5) then
		goto continue_at_20
	end
	if loc_10 < 0LL then
		goto continue_at_36
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_36::
	if gt_u32(add_i32(loc_1, -6), -5) then
		goto continue_at_20
	end
	if loc_10 < 0LL then
		goto continue_at_37
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_37::
	if gt_u32(add_i32(loc_1, -7), -5) then
		goto continue_at_20
	end
	if loc_10 < 0LL then
		goto continue_at_20
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_20::
	loc_7 = promote_f64_f32((convert_f32_i32(loc_8) * math.huge))
	goto continue_at_1
	::continue_at_13::
	if loc_9 ~= 78 then
		goto continue_at_11
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_39
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_38
	::continue_at_39::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_38::
	if band_i32(loc_1, -33) ~= 65 then
		goto continue_at_12
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_41
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_40
	::continue_at_41::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_40::
	if band_i32(loc_1, -33) ~= 78 then
		goto continue_at_12
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_43
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_42
	::continue_at_43::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_42::
	if loc_1 ~= 40 then
		goto continue_at_45
	end
	loc_11 = 1
	loc_9 = 1
	goto continue_at_44
	::continue_at_45::
	loc_7 = -(0.0 / 0.0)
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_1
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	goto continue_at_1
	::continue_at_44::
	::continue_at_46::
	while true do
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_48
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
		loc_1 = load_i32_u8(memory_at_0, loc_1)
		goto continue_at_47
		::continue_at_48::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_1 = reg_0
		::continue_at_47::
		loc_12 = add_i32(loc_1, -65)
		if lt_u32(add_i32(loc_1, -48), 10) then
			goto continue_at_50
		end
		if lt_u32(loc_12, 26) then
			goto continue_at_50
		end
		loc_12 = add_i32(loc_1, -97)
		if loc_1 == 95 then
			goto continue_at_50
		end
		if ge_u32(loc_12, 26) then
			goto continue_at_49
		end
		::continue_at_50::
		loc_11 = add_i32(loc_11, 1)
		loc_9 = add_i32(loc_9, 1)
		goto continue_at_46
		::continue_at_49::
		break
	end
	if loc_1 ~= 41 then
		goto continue_at_51
	end
	loc_7 = -(0.0 / 0.0)
	goto continue_at_1
	::continue_at_51::
	loc_10 = load_i64(memory_at_0, loc_0 + 88)
	if loc_10 < 0LL then
		goto continue_at_52
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_52::
	if loc_2 == 0 then
		goto continue_at_54
	end
	if loc_9 ~= 0 then
		goto continue_at_55
	end
	loc_7 = -(0.0 / 0.0)
	goto continue_at_1
	::continue_at_55::
	loc_12 = add_i32(loc_9, -1)
	if band_i32(loc_9, 3) == 0 then
		goto continue_at_56
	end
	loc_11 = band_i32(loc_11, 3)
	loc_1 = 0
	::continue_at_57::
	while true do
		if loc_10 < 0LL then
			goto continue_at_58
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
		::continue_at_58::
		loc_1 = add_i32(loc_1, 1)
		if loc_11 ~= loc_1 then
			goto continue_at_57
		end
		break
	end
	loc_9 = sub_i32(loc_9, loc_1)
	::continue_at_56::
	if ge_u32(loc_12, 3) then
		goto continue_at_53
	end
	loc_7 = -(0.0 / 0.0)
	goto continue_at_1
	::continue_at_54::
	store_i32(memory_at_0, 0 + 4484, 28)
	FUNC_LIST[62](loc_0, 0LL)
	goto continue_at_1
	::continue_at_53::
	loc_1 = (loc_10 < 0LL and 1 or 0)
	::continue_at_59::
	while true do
		if loc_1 ~= 0 then
			goto continue_at_60
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -3))
		::continue_at_60::
		if loc_1 ~= 0 then
			goto continue_at_61
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
		::continue_at_61::
		loc_9 = add_i32(loc_9, -4)
		if loc_9 ~= 0 then
			goto continue_at_59
		end
		break
	end
	loc_7 = -(0.0 / 0.0)
	goto continue_at_1
	::continue_at_12::
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_62
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_62::
	store_i32(memory_at_0, 0 + 4484, 28)
	FUNC_LIST[62](loc_0, 0LL)
	goto continue_at_1
	::continue_at_11::
	if loc_1 ~= 48 then
		goto continue_at_68
	end
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_70
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_69
	::continue_at_70::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_69::
	if band_i32(loc_1, -33) ~= 88 then
		goto continue_at_71
	end
	reg_0 = FUNC_LIST[68](loc_0, loc_5, loc_4, loc_8, loc_2)
	loc_7 = reg_0
	goto continue_at_1
	::continue_at_71::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_72
	end
	loc_1 = add_i32(loc_1, -1)
	store_i32(memory_at_0, loc_0 + 4, loc_1)
	::continue_at_72::
	loc_13 = sub_i32(0, loc_4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_67
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_66
	::continue_at_68::
	loc_14 = 0
	loc_13 = sub_i32(0, loc_4)
	loc_15 = sub_i32(loc_13, loc_5)
	if loc_1 == 46 then
		goto continue_at_65
	end
	loc_10 = 0LL
	loc_16 = 0
	goto continue_at_63
	::continue_at_67::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_66::
	loc_15 = sub_i32(loc_13, loc_5)
	::continue_at_74::
	while true do
		if loc_1 == 48 then
			goto continue_at_75
		end
		if loc_1 ~= 46 then
			goto continue_at_73
		end
		loc_14 = 1
		goto continue_at_65
		::continue_at_75::
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_76
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
		loc_1 = load_i32_u8(memory_at_0, loc_1)
		goto continue_at_74
		::continue_at_76::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_1 = reg_0
		goto continue_at_74
	end
	::continue_at_73::
	loc_16 = 0
	loc_14 = 1
	goto continue_at_64
	::continue_at_65::
	loc_1 = load_i32(memory_at_0, loc_0 + 4)
	if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_78
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
	loc_1 = load_i32_u8(memory_at_0, loc_1)
	goto continue_at_77
	::continue_at_78::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_1 = reg_0
	::continue_at_77::
	if loc_1 == 48 then
		goto continue_at_79
	end
	loc_16 = 1
	goto continue_at_64
	::continue_at_79::
	loc_10 = 0LL
	::continue_at_80::
	while true do
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_82
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
		loc_1 = load_i32_u8(memory_at_0, loc_1)
		goto continue_at_81
		::continue_at_82::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_1 = reg_0
		::continue_at_81::
		loc_10 = (loc_10 + -1LL)
		if loc_1 == 48 then
			goto continue_at_80
		end
		break
	end
	loc_14 = 1
	loc_16 = 1
	goto continue_at_63
	::continue_at_64::
	loc_10 = 0LL
	::continue_at_63::
	loc_17 = 0
	store_i32(memory_at_0, loc_3, 0)
	loc_11 = add_i32(loc_1, -48)
	loc_9 = (loc_1 == 46 and 1 or 0)
	if loc_9 ~= 0 then
		goto continue_at_88
	end
	loc_18 = 0LL
	if le_u32(loc_11, 9) then
		goto continue_at_88
	end
	loc_12 = 0
	loc_19 = 0
	goto continue_at_87
	::continue_at_88::
	loc_18 = 0LL
	loc_19 = 0
	loc_12 = 0
	loc_17 = 0
	::continue_at_89::
	while true do
		if band_i32(loc_9, 1) == 0 then
			goto continue_at_91
		end
		if loc_16 ~= 0 then
			goto continue_at_92
		end
		loc_10 = loc_18
		loc_16 = 1
		goto continue_at_90
		::continue_at_92::
		loc_9 = (loc_14 == 0 and 1 or 0)
		goto continue_at_86
		::continue_at_91::
		loc_18 = (loc_18 + 1LL)
		if loc_12 > 124 then
			goto continue_at_93
		end
		loc_14 = wrap_i32_i64(loc_18)
		loc_9 = add_i32(loc_3, shl_i32(loc_12, 2))
		if loc_19 == 0 then
			goto continue_at_94
		end
		loc_11 = add_i32(add_i32(loc_1, mul_i32(load_i32(memory_at_0, loc_9), 10)), -48)
		::continue_at_94::
		loc_17 = (loc_1 == 48 and loc_17 or loc_14)
		store_i32(memory_at_0, loc_9, loc_11)
		loc_14 = 1
		loc_1 = add_i32(loc_19, 1)
		reg_1 = loc_1
		loc_1 = (loc_1 == 9 and 1 or 0)
		loc_19 = (loc_1 ~= 0 and 0 or reg_1)
		loc_12 = add_i32(loc_12, loc_1)
		goto continue_at_90
		::continue_at_93::
		if loc_1 == 48 then
			goto continue_at_90
		end
		store_i32(memory_at_0, loc_3 + 496, bor_i32(load_i32(memory_at_0, loc_3 + 496), 1))
		loc_17 = 1116
		::continue_at_90::
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_96
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
		loc_1 = load_i32_u8(memory_at_0, loc_1)
		goto continue_at_95
		::continue_at_96::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_1 = reg_0
		::continue_at_95::
		loc_11 = add_i32(loc_1, -48)
		loc_9 = (loc_1 == 46 and 1 or 0)
		if loc_9 ~= 0 then
			goto continue_at_89
		end
		if lt_u32(loc_11, 10) then
			goto continue_at_89
		end
		break
	end
	::continue_at_87::
	loc_10 = (loc_16 ~= 0 and loc_10 or loc_18)
	if loc_14 == 0 then
		goto continue_at_97
	end
	if band_i32(loc_1, -33) ~= 69 then
		goto continue_at_97
	end
	reg_0 = FUNC_LIST[69](loc_0, loc_2)
	loc_20 = reg_0
	if loc_20 ~= -9223372036854775808LL then
		goto continue_at_98
	end
	if loc_2 == 0 then
		goto continue_at_84
	end
	loc_20 = 0LL
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_98
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_98::
	loc_10 = (loc_20 + loc_10)
	goto continue_at_83
	::continue_at_97::
	loc_9 = (loc_14 == 0 and 1 or 0)
	if loc_1 < 0 then
		goto continue_at_85
	end
	::continue_at_86::
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_85
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_85::
	if loc_9 == 0 then
		goto continue_at_83
	end
	store_i32(memory_at_0, 0 + 4484, 28)
	FUNC_LIST[62](loc_0, 0LL)
	loc_7 = 0e0
	goto continue_at_1
	::continue_at_84::
	FUNC_LIST[62](loc_0, 0LL)
	loc_7 = 0e0
	goto continue_at_1
	::continue_at_83::
	loc_0 = load_i32(memory_at_0, loc_3)
	if loc_0 ~= 0 then
		goto continue_at_99
	end
	loc_7 = copysign_f64(0e0, convert_f64_i32(loc_8))
	goto continue_at_1
	::continue_at_99::
	if loc_18 > 9LL then
		goto continue_at_100
	end
	if loc_10 ~= loc_18 then
		goto continue_at_100
	end
	if bor_i32(loc_6, (shr_u32(loc_0, loc_5) == 0 and 1 or 0)) ~= 1 then
		goto continue_at_100
	end
	loc_7 = (convert_f64_i32(loc_8) * convert_f64_u32(loc_0))
	goto continue_at_1
	::continue_at_100::
	if loc_10 <= extend_i64_u32(shr_u32(loc_13, 1)) then
		goto continue_at_101
	end
	store_i32(memory_at_0, 0 + 4484, 68)
	loc_7 = ((convert_f64_i32(loc_8) * 1.7976931348623157e308) * 1.7976931348623157e308)
	goto continue_at_1
	::continue_at_101::
	if loc_10 >= extend_i64_i32(add_i32(loc_4, -106)) then
		goto continue_at_102
	end
	store_i32(memory_at_0, 0 + 4484, 68)
	loc_7 = ((convert_f64_i32(loc_8) * 2.2250738585072014e-308) * 2.2250738585072014e-308)
	goto continue_at_1
	::continue_at_102::
	if loc_19 == 0 then
		goto continue_at_103
	end
	if loc_19 > 8 then
		goto continue_at_104
	end
	loc_11 = add_i32(loc_3, shl_i32(loc_12, 2))
	loc_0 = load_i32(memory_at_0, loc_11)
	loc_9 = band_i32(sub_i32(1, loc_19), 7)
	if loc_9 ~= 0 then
		goto continue_at_106
	end
	loc_1 = loc_19
	goto continue_at_105
	::continue_at_106::
	loc_1 = loc_19
	::continue_at_107::
	while true do
		loc_1 = add_i32(loc_1, 1)
		loc_0 = mul_i32(loc_0, 10)
		loc_9 = add_i32(loc_9, -1)
		if loc_9 ~= 0 then
			goto continue_at_107
		end
		break
	end
	::continue_at_105::
	if lt_u32(add_i32(loc_19, -2), 7) then
		goto continue_at_108
	end
	loc_1 = add_i32(loc_1, -9)
	::continue_at_109::
	while true do
		loc_0 = mul_i32(loc_0, 100000000)
		loc_1 = add_i32(loc_1, 8)
		if loc_1 ~= 0 then
			goto continue_at_109
		end
		break
	end
	::continue_at_108::
	store_i32(memory_at_0, loc_11, loc_0)
	::continue_at_104::
	loc_12 = add_i32(loc_12, 1)
	::continue_at_103::
	loc_6 = wrap_i32_i64(loc_10)
	if loc_17 >= 9 then
		goto continue_at_110
	end
	if loc_10 > 17LL then
		goto continue_at_110
	end
	if loc_17 > loc_6 then
		goto continue_at_110
	end
	if loc_10 ~= 9LL then
		goto continue_at_111
	end
	loc_7 = (convert_f64_i32(loc_8) * convert_f64_u32(load_i32(memory_at_0, loc_3)))
	goto continue_at_1
	::continue_at_111::
	if loc_10 > 8LL then
		goto continue_at_112
	end
	loc_7 = ((convert_f64_i32(loc_8) * convert_f64_u32(load_i32(memory_at_0, loc_3))) / convert_f64_i32(load_i32(memory_at_0, add_i32(shl_i32(sub_i32(8, loc_6), 2), 3744))))
	goto continue_at_1
	::continue_at_112::
	loc_0 = load_i32(memory_at_0, loc_3)
	loc_1 = add_i32(add_i32(loc_5, mul_i32(loc_6, -3)), 27)
	if loc_1 > 30 then
		goto continue_at_113
	end
	if shr_u32(loc_0, loc_1) ~= 0 then
		goto continue_at_110
	end
	::continue_at_113::
	loc_7 = ((convert_f64_i32(loc_8) * convert_f64_u32(loc_0)) * convert_f64_i32(load_i32(memory_at_0, add_i32(shl_i32(loc_6, 2), 3704))))
	goto continue_at_1
	::continue_at_110::
	loc_11 = add_i32(loc_12, 1)
	loc_0 = add_i32(add_i32(shl_i32(loc_12, 2), loc_3), 4)
	::continue_at_114::
	while true do
		loc_11 = add_i32(loc_11, -1)
		loc_1 = add_i32(loc_0, -8)
		loc_12 = add_i32(loc_0, -4)
		loc_0 = loc_12
		if load_i32(memory_at_0, loc_1) == 0 then
			goto continue_at_114
		end
		break
	end
	loc_17 = 0
	loc_0 = rem_i32(loc_6, 9)
	if loc_0 ~= 0 then
		goto continue_at_116
	end
	loc_9 = 0
	goto continue_at_115
	::continue_at_116::
	loc_21 = (loc_10 < 0LL and add_i32(loc_0, 9) or loc_0)
	if loc_11 ~= 0 then
		goto continue_at_118
	end
	loc_9 = 0
	loc_11 = 0
	goto continue_at_117
	::continue_at_118::
	loc_19 = load_i32(memory_at_0, add_i32(shl_i32(sub_i32(8, loc_21), 2), 3744))
	loc_13 = div_i32(1000000000, loc_19)
	loc_16 = 0
	loc_0 = loc_3
	loc_1 = 0
	loc_9 = 0
	::continue_at_119::
	while true do
		loc_2 = load_i32(memory_at_0, loc_0)
		loc_14 = div_u32(loc_2, loc_19)
		loc_16 = add_i32(loc_14, loc_16)
		store_i32(memory_at_0, loc_0, loc_16)
		loc_16 = band_i32((loc_1 == loc_9 and 1 or 0), (loc_16 == 0 and 1 or 0))
		loc_9 = (loc_16 ~= 0 and band_i32(add_i32(loc_9, 1), 127) or loc_9)
		loc_6 = (loc_16 ~= 0 and add_i32(loc_6, -9) or loc_6)
		loc_0 = add_i32(loc_0, 4)
		loc_16 = mul_i32(sub_i32(loc_2, mul_i32(loc_14, loc_19)), loc_13)
		loc_1 = add_i32(loc_1, 1)
		if loc_11 ~= loc_1 then
			goto continue_at_119
		end
		break
	end
	if loc_16 == 0 then
		goto continue_at_117
	end
	store_i32(memory_at_0, loc_12, loc_16)
	loc_11 = add_i32(loc_11, 1)
	::continue_at_117::
	loc_6 = add_i32(sub_i32(loc_6, loc_21), 9)
	::continue_at_115::
	::continue_at_120::
	while true do
		loc_14 = add_i32(loc_3, shl_i32(loc_9, 2))
		loc_2 = (loc_6 < 18 and 1 or 0)
		::continue_at_122::
		while true do
			if loc_2 ~= 0 then
				goto continue_at_123
			end
			if loc_6 ~= 18 then
				goto continue_at_121
			end
			if gt_u32(load_i32(memory_at_0, loc_14), 9007198) then
				goto continue_at_121
			end
			::continue_at_123::
			loc_16 = add_i32(loc_11, 127)
			loc_12 = 0
			::continue_at_124::
			while true do
				loc_1 = loc_11
				loc_0 = band_i32(loc_16, 127)
				loc_11 = add_i32(loc_3, shl_i32(loc_0, 2))
				loc_10 = (shl_i64(load_i64_u32(memory_at_0, loc_11), 29LL) + extend_i64_u32(loc_12))
				if ge_u64(loc_10, 1000000001LL) then
					goto continue_at_126
				end
				loc_12 = 0
				goto continue_at_125
				::continue_at_126::
				loc_18 = div_u64(loc_10, 1000000000LL)
				loc_10 = (loc_10 - (loc_18 * 1000000000LL))
				loc_12 = wrap_i32_i64(loc_18)
				::continue_at_125::
				store_i64_n32(memory_at_0, loc_11, loc_10)
				loc_19 = band_i32(add_i32(loc_1, -1), 127)
				loc_11 = (loc_0 ~= loc_19 and loc_1 or (loc_0 == loc_9 and loc_1 or (loc_10 == 0LL and loc_0 or loc_1)))
				loc_16 = add_i32(loc_0, -1)
				if loc_0 ~= loc_9 then
					goto continue_at_124
				end
				break
			end
			loc_17 = add_i32(loc_17, -29)
			loc_11 = loc_1
			if loc_12 == 0 then
				goto continue_at_122
			end
			break
		end
		loc_9 = band_i32(add_i32(loc_9, -1), 127)
		if loc_9 == loc_1 then
			goto continue_at_128
		end
		loc_11 = loc_1
		goto continue_at_127
		::continue_at_128::
		loc_0 = add_i32(loc_3, shl_i32(band_i32(add_i32(loc_1, 126), 127), 2))
		store_i32(memory_at_0, loc_0, bor_i32(load_i32(memory_at_0, loc_0), load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_19, 2)))))
		loc_11 = loc_19
		::continue_at_127::
		loc_6 = add_i32(loc_6, 9)
		store_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_9, 2)), loc_12)
		goto continue_at_120
		::continue_at_121::
		break
	end
	::continue_at_130::
	while true do
		loc_21 = add_i32(loc_3, shl_i32(band_i32(loc_11, 127), 2))
		loc_14 = add_i32(loc_3, shl_i32(band_i32(add_i32(loc_11, -1), 127), 2))
		loc_13 = band_i32(add_i32(loc_11, 1), 127)
		loc_22 = add_i32(loc_3, shl_i32(loc_13, 2))
		::continue_at_132::
		while true do
			loc_0 = band_i32(loc_9, 127)
			if loc_0 == loc_11 then
				goto continue_at_134
			end
			loc_0 = load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_0, 2)))
			if lt_u32(loc_0, 9007199) then
				goto continue_at_135
			end
			if loc_0 ~= 9007199 then
				goto continue_at_133
			end
			loc_1 = band_i32(add_i32(loc_9, 1), 127)
			if loc_1 == loc_11 then
				goto continue_at_135
			end
			if gt_u32(load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_1, 2))), 254740991) then
				goto continue_at_133
			end
			if loc_6 ~= 18 then
				goto continue_at_133
			end
			loc_0 = 9007199
			loc_1 = loc_11
			goto continue_at_129
			::continue_at_135::
			if loc_6 ~= 18 then
				goto continue_at_133
			end
			loc_1 = loc_11
			goto continue_at_129
			::continue_at_134::
			if loc_6 == 18 then
				goto continue_at_131
			end
			::continue_at_133::
			loc_16 = (loc_6 > 27 and 9 or 1)
			if loc_9 == loc_11 then
				goto continue_at_137
			end
			loc_17 = add_i32(loc_16, loc_17)
			loc_19 = shr_u32(1000000000, loc_16)
			loc_2 = bxor_i32(shl_i32(-1, loc_16), -1)
			loc_1 = 0
			loc_0 = loc_9
			::continue_at_138::
			while true do
				loc_12 = add_i32(loc_3, shl_i32(loc_0, 2))
				reg_0 = loc_12
				loc_12 = load_i32(memory_at_0, loc_12)
				loc_1 = add_i32(shr_u32(loc_12, loc_16), loc_1)
				store_i32(memory_at_0, reg_0, loc_1)
				loc_1 = band_i32((loc_0 == loc_9 and 1 or 0), (loc_1 == 0 and 1 or 0))
				loc_9 = (loc_1 ~= 0 and band_i32(add_i32(loc_9, 1), 127) or loc_9)
				loc_6 = (loc_1 ~= 0 and add_i32(loc_6, -9) or loc_6)
				loc_1 = mul_i32(band_i32(loc_12, loc_2), loc_19)
				loc_0 = band_i32(add_i32(loc_0, 1), 127)
				if loc_0 ~= loc_11 then
					goto continue_at_138
				end
				break
			end
			if loc_1 == 0 then
				goto continue_at_132
			end
			if loc_13 == loc_9 then
				goto continue_at_136
			end
			store_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_11, 2)), loc_1)
			loc_11 = loc_13
			goto continue_at_130
			::continue_at_137::
			loc_17 = add_i32(loc_16, loc_17)
			loc_1 = (lt_u32(loc_11, 128) and 1 or 0)
			loc_9 = (loc_6 == 18 and 1 or 0)
			loc_12 = (loc_13 == loc_11 and 1 or 0)
			::continue_at_139::
			while true do
				if loc_1 == 0 then
					goto continue_at_141
				end
				if loc_9 == 0 then
					goto continue_at_140
				end
				loc_9 = loc_11
				goto continue_at_131
				::continue_at_141::
				loc_0 = load_i32(memory_at_0, loc_21)
				if lt_u32(loc_0, 9007199) then
					goto continue_at_143
				end
				if loc_0 ~= 9007199 then
					goto continue_at_140
				end
				if loc_12 ~= 0 then
					goto continue_at_143
				end
				if gt_u32(load_i32(memory_at_0, loc_22), 254740991) then
					goto continue_at_140
				end
				if loc_9 == 0 then
					goto continue_at_140
				end
				loc_0 = 9007199
				goto continue_at_142
				::continue_at_143::
				if loc_9 == 0 then
					goto continue_at_140
				end
				::continue_at_142::
				loc_9 = loc_11
				loc_1 = loc_11
				goto continue_at_129
				::continue_at_140::
				loc_17 = add_i32(loc_17, loc_16)
				goto continue_at_139
			end
			::continue_at_136::
			store_i32(memory_at_0, loc_14, bor_i32(load_i32(memory_at_0, loc_14), 1))
			goto continue_at_132
		end
		::continue_at_131::
		break
	end
	loc_1 = band_i32(add_i32(loc_11, 1), 127)
	store_i32(memory_at_0, add_i32(add_i32(shl_i32(loc_1, 2), loc_3), -4), 0)
	loc_0 = load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_11, 2)))
	::continue_at_129::
	loc_7 = convert_f64_u32(loc_0)
	loc_0 = band_i32(add_i32(loc_9, 1), 127)
	if loc_0 ~= loc_1 then
		goto continue_at_144
	end
	loc_1 = band_i32(add_i32(loc_9, 2), 127)
	store_i32(memory_at_0, add_i32(add_i32(shl_i32(loc_1, 2), loc_3), -4), 0)
	::continue_at_144::
	loc_23 = convert_f64_i32(loc_8)
	loc_24 = (((loc_7 * 1e9) + convert_f64_u32(load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_0, 2))))) * loc_23)
	loc_7 = 0e0
	loc_12 = add_i32(loc_17, 53)
	loc_0 = sub_i32(loc_12, loc_4)
	loc_6 = (loc_5 > loc_0 and 1 or 0)
	loc_11 = (loc_6 ~= 0 and (loc_0 > 0 and loc_0 or 0) or loc_5)
	if le_u32(loc_11, 52) then
		goto continue_at_146
	end
	loc_25 = 0e0
	goto continue_at_145
	::continue_at_146::
	reg_0 = FUNC_LIST[65](1e0, sub_i32(105, loc_11))
	loc_25 = copysign_f64(reg_0, loc_24)
	reg_3 = FUNC_LIST[65](1e0, sub_i32(53, loc_11))
	reg_2 = FUNC_LIST[66](loc_24, reg_3)
	loc_7 = reg_2
	loc_24 = (loc_25 + (loc_24 - loc_7))
	::continue_at_145::
	loc_16 = band_i32(add_i32(loc_9, 2), 127)
	if loc_16 == loc_1 then
		goto continue_at_147
	end
	loc_16 = load_i32(memory_at_0, add_i32(loc_3, shl_i32(loc_16, 2)))
	if gt_u32(loc_16, 499999999) then
		goto continue_at_149
	end
	if loc_16 ~= 0 then
		goto continue_at_150
	end
	if band_i32(add_i32(loc_9, 3), 127) == loc_1 then
		goto continue_at_148
	end
	::continue_at_150::
	loc_7 = ((loc_23 * 2.5e-1) + loc_7)
	goto continue_at_148
	::continue_at_149::
	if loc_16 == 500000000 then
		goto continue_at_151
	end
	loc_7 = ((loc_23 * 7.5e-1) + loc_7)
	goto continue_at_148
	::continue_at_151::
	if band_i32(add_i32(loc_9, 3), 127) ~= loc_1 then
		goto continue_at_152
	end
	loc_7 = ((loc_23 * 5e-1) + loc_7)
	goto continue_at_148
	::continue_at_152::
	loc_7 = ((loc_23 * 7.5e-1) + loc_7)
	::continue_at_148::
	loc_7 = (gt_u32(loc_11, 51) and loc_7 or (copysign_f64((loc_7 - truncate_f64(loc_7)), loc_7) ~= 0e0 and loc_7 or (loc_7 + 1e0)))
	::continue_at_147::
	loc_24 = ((loc_24 + loc_7) - loc_25)
	if band_i32(loc_12, 2147483647) <= add_i32(loc_15, -2) then
		goto continue_at_153
	end
	loc_1 = (abs_f64(loc_24) >= 9.007199254740992e15 and 1 or 0)
	loc_24 = (loc_1 ~= 0 and (loc_24 * 5e-1) or loc_24)
	loc_17 = add_i32(loc_17, loc_1)
	if add_i32(loc_17, 50) > loc_15 then
		goto continue_at_154
	end
	if band_i32(band_i32(loc_6, bor_i32((loc_11 ~= loc_0 and 1 or 0), bxor_i32(loc_1, -1))), (loc_7 ~= 0e0 and 1 or 0)) == 0 then
		goto continue_at_153
	end
	::continue_at_154::
	store_i32(memory_at_0, 0 + 4484, 68)
	::continue_at_153::
	reg_0 = FUNC_LIST[65](loc_24, loc_17)
	loc_7 = reg_0
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 512)
	reg_0 = loc_7
	return reg_0
end
FUNC_LIST[68] = function(loc_0, loc_1, loc_2, loc_3, loc_4)
	local loc_5 = 0
	local loc_6 = 0LL
	local loc_7 = 0
	local loc_8 = 0
	local loc_9 = 0
	local loc_10 = 0LL
	local loc_11 = 0.0
	local loc_12 = 0.0
	local loc_13 = 0
	local loc_14 = 0
	local loc_15 = 0
	local loc_16 = 0LL
	local loc_17 = 0LL
	local loc_18 = 0.0
	local reg_0
	local br_map, temp = {}, nil
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
	loc_5 = load_i32_u8(memory_at_0, loc_5)
	goto continue_at_1
	::continue_at_2::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_5 = reg_0
	::continue_at_1::
	loc_6 = 0LL
	loc_7 = 0
	loc_8 = 0
	loc_9 = 0
	loc_10 = 0LL
	if not br_map[1] then
		br_map[1] = (function()
			return { [0] = 1, 3, 0, }
		end)()
	end
	temp = br_map[1][add_i32(loc_5, -46)] or 3
	if temp < 1 then
		goto continue_at_6
	elseif temp > 1 then
		goto continue_at_3
	else
		goto continue_at_5
	end
	::continue_at_6::
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_8
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
	loc_5 = load_i32_u8(memory_at_0, loc_5)
	goto continue_at_7
	::continue_at_8::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_5 = reg_0
	::continue_at_7::
	::continue_at_10::
	while true do
		if loc_5 == 48 then
			goto continue_at_11
		end
		if loc_5 ~= 46 then
			goto continue_at_9
		end
		loc_7 = 1
		goto continue_at_5
		::continue_at_11::
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_12
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_10
		::continue_at_12::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		goto continue_at_10
	end
	::continue_at_9::
	loc_9 = 1
	loc_8 = 0
	goto continue_at_4
	::continue_at_5::
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_14
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
	loc_5 = load_i32_u8(memory_at_0, loc_5)
	goto continue_at_13
	::continue_at_14::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_5 = reg_0
	::continue_at_13::
	if loc_5 == 48 then
		goto continue_at_15
	end
	loc_8 = 1
	loc_9 = loc_7
	goto continue_at_4
	::continue_at_15::
	loc_10 = 0LL
	::continue_at_16::
	while true do
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_18
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_17
		::continue_at_18::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		::continue_at_17::
		loc_10 = (loc_10 + -1LL)
		if loc_5 == 48 then
			goto continue_at_16
		end
		break
	end
	loc_8 = 1
	loc_9 = 1
	goto continue_at_3
	::continue_at_4::
	loc_10 = 0LL
	::continue_at_3::
	loc_11 = 1e0
	loc_12 = 0e0
	loc_13 = 0
	loc_14 = 0
	::continue_at_20::
	while true do
		loc_7 = loc_5
		loc_15 = add_i32(loc_5, -48)
		if lt_u32(loc_15, 10) then
			goto continue_at_22
		end
		loc_7 = bor_i32(loc_5, 32)
		if loc_5 == 46 then
			goto continue_at_23
		end
		if gt_u32(add_i32(loc_7, -97), 5) then
			goto continue_at_19
		end
		::continue_at_23::
		if loc_5 ~= 46 then
			goto continue_at_22
		end
		if loc_8 ~= 0 then
			goto continue_at_19
		end
		loc_8 = 1
		loc_10 = loc_6
		goto continue_at_21
		::continue_at_22::
		loc_5 = (loc_5 > 57 and add_i32(loc_7, -87) or loc_15)
		if loc_6 > 7LL then
			goto continue_at_25
		end
		loc_13 = add_i32(loc_5, shl_i32(loc_13, 4))
		goto continue_at_24
		::continue_at_25::
		if gt_u64(loc_6, 13LL) then
			goto continue_at_26
		end
		loc_11 = (loc_11 * 6.25e-2)
		loc_12 = ((convert_f64_i32(loc_5) * loc_11) + loc_12)
		goto continue_at_24
		::continue_at_26::
		loc_5 = bor_i32((loc_5 == 0 and 1 or 0), (loc_14 ~= 0 and 1 or 0))
		loc_12 = (loc_5 ~= 0 and loc_12 or ((loc_11 * 5e-1) + loc_12))
		loc_14 = (loc_5 ~= 0 and loc_14 or 1)
		::continue_at_24::
		loc_6 = (loc_6 + 1LL)
		loc_9 = 1
		::continue_at_21::
		loc_5 = load_i32(memory_at_0, loc_0 + 4)
		if loc_5 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_27
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, 1))
		loc_5 = load_i32_u8(memory_at_0, loc_5)
		goto continue_at_20
		::continue_at_27::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_5 = reg_0
		goto continue_at_20
	end
	::continue_at_19::
	if loc_9 ~= 0 then
		goto continue_at_28
	end
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_31
	end
	loc_5 = load_i32(memory_at_0, loc_0 + 4)
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, -1))
	if loc_4 == 0 then
		goto continue_at_30
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, -2))
	if loc_8 == 0 then
		goto continue_at_29
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_5, -3))
	goto continue_at_29
	::continue_at_31::
	if loc_4 ~= 0 then
		goto continue_at_29
	end
	::continue_at_30::
	FUNC_LIST[62](loc_0, 0LL)
	::continue_at_29::
	reg_0 = copysign_f64(0e0, convert_f64_i32(loc_3))
	goto continue_at_0
	::continue_at_28::
	if loc_6 > 7LL then
		goto continue_at_32
	end
	loc_16 = band_i64((0LL - loc_6), 7LL)
	if (loc_16 == 0LL and 1 or 0) == 0 then
		goto continue_at_34
	end
	loc_17 = loc_6
	goto continue_at_33
	::continue_at_34::
	loc_17 = loc_6
	::continue_at_35::
	while true do
		loc_17 = (loc_17 + 1LL)
		loc_13 = shl_i32(loc_13, 4)
		loc_16 = (loc_16 + -1LL)
		if loc_16 ~= 0LL then
			goto continue_at_35
		end
		break
	end
	::continue_at_33::
	if lt_u64((loc_6 + -1LL), 7LL) then
		goto continue_at_32
	end
	loc_17 = (loc_17 + -8LL)
	::continue_at_36::
	while true do
		loc_17 = (loc_17 + 8LL)
		if loc_17 ~= 0LL then
			goto continue_at_36
		end
		break
	end
	loc_13 = 0
	::continue_at_32::
	if band_i32(loc_5, -33) ~= 80 then
		goto continue_at_40
	end
	reg_0 = FUNC_LIST[69](loc_0, loc_4)
	loc_17 = reg_0
	if loc_17 ~= -9223372036854775808LL then
		goto continue_at_37
	end
	if loc_4 == 0 then
		goto continue_at_41
	end
	if load_i64(memory_at_0, loc_0 + 88) > -1LL then
		goto continue_at_39
	end
	goto continue_at_38
	::continue_at_41::
	FUNC_LIST[62](loc_0, 0LL)
	reg_0 = 0e0
	goto continue_at_0
	::continue_at_40::
	loc_17 = 0LL
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_37
	end
	::continue_at_39::
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_38::
	loc_17 = 0LL
	::continue_at_37::
	if loc_13 ~= 0 then
		goto continue_at_42
	end
	reg_0 = copysign_f64(0e0, convert_f64_i32(loc_3))
	goto continue_at_0
	::continue_at_42::
	loc_6 = ((shl_i64((loc_8 ~= 0 and loc_10 or loc_6), 2LL) + loc_17) + -32LL)
	if loc_6 <= extend_i64_u32(sub_i32(0, loc_2)) then
		goto continue_at_43
	end
	store_i32(memory_at_0, 0 + 4484, 68)
	reg_0 = ((convert_f64_i32(loc_3) * 1.7976931348623157e308) * 1.7976931348623157e308)
	goto continue_at_0
	::continue_at_43::
	if loc_6 < extend_i64_i32(add_i32(loc_2, -106)) then
		goto continue_at_44
	end
	if loc_13 < 0 then
		goto continue_at_45
	end
	::continue_at_46::
	while true do
		loc_5 = shl_i32(loc_13, 1)
		loc_0 = (loc_12 >= 5e-1 and 1 or 0)
		loc_13 = bor_i32(loc_5, loc_0)
		loc_12 = (loc_12 + (loc_0 ~= 0 and (loc_12 + -1e0) or loc_12))
		loc_6 = (loc_6 + -1LL)
		if loc_5 > -1 then
			goto continue_at_46
		end
		break
	end
	::continue_at_45::
	loc_10 = (loc_6 + extend_i64_u32(sub_i32(32, loc_2)))
	loc_5 = wrap_i32_i64(loc_10)
	loc_5 = (loc_10 < extend_i64_u32(loc_1) and (loc_5 > 0 and loc_5 or 0) or loc_1)
	if lt_u32(loc_5, 53) then
		goto continue_at_48
	end
	loc_11 = convert_f64_i32(loc_3)
	loc_18 = 0e0
	goto continue_at_47
	::continue_at_48::
	reg_0 = FUNC_LIST[65](1e0, sub_i32(84, loc_5))
	loc_11 = convert_f64_i32(loc_3)
	loc_18 = copysign_f64(reg_0, loc_11)
	::continue_at_47::
	loc_5 = band_i32((band_i32(loc_13, 1) == 0 and 1 or 0), band_i32((lt_u32(loc_5, 32) and 1 or 0), (loc_12 ~= 0e0 and 1 or 0)))
	loc_12 = (((loc_11 * (loc_5 ~= 0 and 0e0 or loc_12)) + ((loc_11 * convert_f64_u32(bor_i32(loc_13, loc_5))) + loc_18)) - loc_18)
	if loc_12 ~= 0e0 then
		goto continue_at_49
	end
	store_i32(memory_at_0, 0 + 4484, 68)
	::continue_at_49::
	reg_0 = FUNC_LIST[65](loc_12, wrap_i32_i64(loc_6))
	goto continue_at_0
	::continue_at_44::
	store_i32(memory_at_0, 0 + 4484, 68)
	reg_0 = ((convert_f64_i32(loc_3) * 2.2250738585072014e-308) * 2.2250738585072014e-308)
	::continue_at_0::
	return reg_0
end
FUNC_LIST[69] = function(loc_0, loc_1)
	local loc_2 = 0
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0LL
	local reg_0
	local br_map, temp = {}, nil
	loc_2 = load_i32(memory_at_0, loc_0 + 4)
	if loc_2 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_2, 1))
	loc_3 = load_i32_u8(memory_at_0, loc_2)
	goto continue_at_1
	::continue_at_2::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_3 = reg_0
	::continue_at_1::
	if not br_map[1] then
		br_map[1] = (function()
			return { [0] = 0, 1, 0, }
		end)()
	end
	temp = br_map[1][add_i32(loc_3, -43)] or 1
	if temp < 1 then
		goto continue_at_7
	else
		goto continue_at_6
	end
	::continue_at_7::
	loc_2 = load_i32(memory_at_0, loc_0 + 4)
	if loc_2 == load_i32(memory_at_0, loc_0 + 84) then
		goto continue_at_9
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(loc_2, 1))
	loc_2 = load_i32_u8(memory_at_0, loc_2)
	goto continue_at_8
	::continue_at_9::
	reg_0 = FUNC_LIST[63](loc_0)
	loc_2 = reg_0
	::continue_at_8::
	loc_4 = (loc_3 == 45 and 1 or 0)
	loc_5 = add_i32(loc_2, -58)
	if loc_1 == 0 then
		goto continue_at_5
	end
	if gt_u32(loc_5, -11) then
		goto continue_at_5
	end
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_4
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	goto continue_at_4
	::continue_at_6::
	loc_5 = add_i32(loc_3, -58)
	loc_4 = 0
	loc_2 = loc_3
	::continue_at_5::
	if lt_u32(loc_5, -10) then
		goto continue_at_4
	end
	loc_6 = 0LL
	if gt_u32(add_i32(loc_2, -48), 9) then
		goto continue_at_10
	end
	loc_3 = 0
	::continue_at_11::
	while true do
		loc_3 = add_i32(loc_2, mul_i32(loc_3, 10))
		loc_2 = load_i32(memory_at_0, loc_0 + 4)
		if loc_2 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_13
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_2, 1))
		loc_2 = load_i32_u8(memory_at_0, loc_2)
		goto continue_at_12
		::continue_at_13::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_2 = reg_0
		::continue_at_12::
		loc_3 = add_i32(loc_3, -48)
		loc_5 = add_i32(loc_2, -48)
		if gt_u32(loc_5, 9) then
			goto continue_at_14
		end
		if loc_3 < 214748364 then
			goto continue_at_11
		end
		::continue_at_14::
		break
	end
	loc_6 = extend_i64_i32(loc_3)
	if gt_u32(loc_5, 9) then
		goto continue_at_10
	end
	::continue_at_15::
	while true do
		loc_6 = (extend_i64_u32(loc_2) + (loc_6 * 10LL))
		loc_2 = load_i32(memory_at_0, loc_0 + 4)
		if loc_2 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_17
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_2, 1))
		loc_2 = load_i32_u8(memory_at_0, loc_2)
		goto continue_at_16
		::continue_at_17::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_2 = reg_0
		::continue_at_16::
		loc_6 = (loc_6 + -48LL)
		loc_3 = add_i32(loc_2, -48)
		if gt_u32(loc_3, 9) then
			goto continue_at_18
		end
		if loc_6 < 92233720368547758LL then
			goto continue_at_15
		end
		::continue_at_18::
		break
	end
	if gt_u32(loc_3, 9) then
		goto continue_at_10
	end
	::continue_at_19::
	while true do
		loc_2 = load_i32(memory_at_0, loc_0 + 4)
		if loc_2 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_21
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_2, 1))
		loc_2 = load_i32_u8(memory_at_0, loc_2)
		goto continue_at_20
		::continue_at_21::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_2 = reg_0
		::continue_at_20::
		if lt_u32(add_i32(loc_2, -48), 10) then
			goto continue_at_19
		end
		break
	end
	::continue_at_10::
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_22
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	::continue_at_22::
	loc_6 = (loc_4 ~= 0 and (0LL - loc_6) or loc_6)
	goto continue_at_3
	::continue_at_4::
	loc_6 = -9223372036854775808LL
	if load_i64(memory_at_0, loc_0 + 88) < 0LL then
		goto continue_at_3
	end
	store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
	reg_0 = -9223372036854775808LL
	goto continue_at_0
	::continue_at_3::
	reg_0 = loc_6
	::continue_at_0::
	return reg_0
end
FUNC_LIST[70] = function(loc_0, loc_1, loc_2, loc_3)
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0
	local reg_0
	loc_4 = (loc_3 ~= 0 and loc_3 or 7096)
	loc_3 = load_i32(memory_at_0, loc_4)
	if loc_1 ~= 0 then
		goto continue_at_4
	end
	if loc_3 ~= 0 then
		goto continue_at_3
	end
	reg_0 = 0
	goto continue_at_0
	::continue_at_4::
	loc_5 = -2
	if loc_2 == 0 then
		goto continue_at_2
	end
	if loc_3 == 0 then
		goto continue_at_6
	end
	loc_6 = loc_2
	goto continue_at_5
	::continue_at_6::
	loc_5 = load_i32_u8(memory_at_0, loc_1)
	loc_3 = extend_i32_n8(loc_5)
	if loc_3 < 0 then
		goto continue_at_7
	end
	if loc_0 == 0 then
		goto continue_at_8
	end
	store_i32(memory_at_0, loc_0, loc_5)
	::continue_at_8::
	reg_0 = (loc_3 ~= 0 and 1 or 0)
	goto continue_at_0
	::continue_at_7::
	loc_7 = load_i32(memory_at_0, 0 + 6052)
	if loc_7 ~= 0 then
		goto continue_at_9
	end
	loc_7 = 6028
	store_i32(memory_at_0, 0 + 6052, 6028)
	::continue_at_9::
	if load_i32(memory_at_0, loc_7) ~= 0 then
		goto continue_at_10
	end
	loc_5 = 1
	if loc_0 == 0 then
		goto continue_at_2
	end
	store_i32(memory_at_0, loc_0, band_i32(loc_3, 57343))
	reg_0 = 1
	goto continue_at_0
	::continue_at_10::
	loc_3 = add_i32(loc_5, -194)
	if gt_u32(loc_3, 50) then
		goto continue_at_3
	end
	loc_3 = load_i32(memory_at_0, add_i32(shl_i32(loc_3, 2), 3776))
	loc_6 = add_i32(loc_2, -1)
	if loc_6 == 0 then
		goto continue_at_1
	end
	loc_1 = add_i32(loc_1, 1)
	::continue_at_5::
	loc_5 = load_i32_u8(memory_at_0, loc_1)
	loc_7 = shr_u32(loc_5, 3)
	if gt_u32(bor_i32(add_i32(loc_7, -16), add_i32(shr_i32(loc_3, 26), loc_7)), 7) then
		goto continue_at_3
	end
	loc_7 = add_i32(loc_1, 1)
	loc_1 = add_i32(loc_6, -1)
	::continue_at_11::
	while true do
		loc_3 = bor_i32(add_i32(band_i32(loc_5, 255), -128), shl_i32(loc_3, 6))
		if loc_3 < 0 then
			goto continue_at_12
		end
		store_i32(memory_at_0, loc_4, 0)
		if loc_0 == 0 then
			goto continue_at_13
		end
		store_i32(memory_at_0, loc_0, loc_3)
		::continue_at_13::
		reg_0 = sub_i32(loc_2, loc_1)
		goto continue_at_0
		::continue_at_12::
		if loc_1 == 0 then
			goto continue_at_1
		end
		loc_1 = add_i32(loc_1, -1)
		loc_5 = load_i32_i8(memory_at_0, loc_7)
		loc_7 = add_i32(loc_7, 1)
		if loc_5 < -64 then
			goto continue_at_11
		end
		break
	end
	::continue_at_3::
	store_i32(memory_at_0, 0 + 4484, 25)
	store_i32(memory_at_0, loc_4, 0)
	loc_5 = -1
	::continue_at_2::
	reg_0 = loc_5
	goto continue_at_0
	::continue_at_1::
	store_i32(memory_at_0, loc_4, loc_3)
	reg_0 = -2
	::continue_at_0::
	return reg_0
end
FUNC_LIST[71] = function(loc_0)
	local reg_0
	if loc_0 ~= 0 then
		goto continue_at_1
	end
	reg_0 = 1
	goto continue_at_0
	::continue_at_1::
	reg_0 = (load_i32(memory_at_0, loc_0) == 0 and 1 or 0)
	::continue_at_0::
	return reg_0
end
FUNC_LIST[72] = function(loc_0, loc_1, loc_2)
	local loc_3 = 0
	local loc_4 = 0
	local loc_5 = 0
	local loc_6 = 0
	local loc_7 = 0LL
	local loc_8 = 0
	local loc_9 = 0
	local loc_10 = 0
	local loc_11 = 0
	local loc_12 = 0
	local loc_13 = 0
	local loc_14 = 0
	local loc_15 = 0
	local loc_16 = 0
	local loc_17 = 0
	local loc_18 = 0LL
	local loc_19 = 0.0
	local loc_20 = 0
	local loc_21 = 0LL
	local reg_0
	local br_map, temp = {}, nil
	loc_3 = sub_i32(GLOBAL_LIST[0].value, 304)
	GLOBAL_LIST[0].value = loc_3
	if load_i32(memory_at_0, loc_0 + 4) ~= 0 then
		goto continue_at_3
	end
	reg_0 = FUNC_LIST[60](loc_0)
	if load_i32(memory_at_0, loc_0 + 4) == 0 then
		goto continue_at_2
	end
	::continue_at_3::
	loc_4 = bor_i32(add_i32(loc_3, 16), 1)
	loc_5 = bor_i32(add_i32(loc_3, 16), 10)
	loc_6 = 0
	loc_7 = 0LL
	::continue_at_8::
	while true do
		if not br_map[1] then
			br_map[1] = (function()
				return { [0] = 12, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1, }
			end)()
		end
		temp = br_map[1][load_i32_u8(memory_at_0, loc_1)] or 2
		if temp < 2 then
			if temp < 1 then
				goto continue_at_14
			else
				goto continue_at_13
			end
		elseif temp > 2 then
			goto continue_at_1
		else
			goto continue_at_12
		end
		::continue_at_14::
		::continue_at_15::
		while true do
			loc_8 = loc_1
			loc_1 = add_i32(loc_8, 1)
			loc_9 = load_i32_u8(memory_at_0, loc_1)
			if lt_u32(add_i32(loc_9, -9), 5) then
				goto continue_at_15
			end
			if loc_9 == 32 then
				goto continue_at_15
			end
			break
		end
		FUNC_LIST[62](loc_0, 0LL)
		::continue_at_16::
		while true do
			loc_1 = load_i32(memory_at_0, loc_0 + 4)
			if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
				goto continue_at_18
			end
			store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
			loc_1 = load_i32_u8(memory_at_0, loc_1)
			goto continue_at_17
			::continue_at_18::
			reg_0 = FUNC_LIST[63](loc_0)
			loc_1 = reg_0
			::continue_at_17::
			if lt_u32(add_i32(loc_1, -9), 5) then
				goto continue_at_16
			end
			if loc_1 == 32 then
				goto continue_at_16
			end
			break
		end
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if load_i64(memory_at_0, loc_0 + 88) < 0LL then
			goto continue_at_19
		end
		loc_1 = add_i32(loc_1, -1)
		store_i32(memory_at_0, loc_0 + 4, loc_1)
		::continue_at_19::
		loc_7 = ((load_i64(memory_at_0, loc_0 + 96) + loc_7) + extend_i64_i32(sub_i32(loc_1, load_i32(memory_at_0, loc_0 + 40))))
		loc_1 = add_i32(loc_8, 1)
		goto continue_at_8
		::continue_at_13::
		loc_9 = load_i32_u8(memory_at_0, loc_1 + 1)
		if not br_map[2] then
			br_map[2] = (function()
				return { [0] = 0, 2, 2, 2, 2, 1, }
			end)()
		end
		temp = br_map[2][add_i32(loc_9, -37)] or 2
		if temp < 1 then
			goto continue_at_12
		elseif temp > 1 then
			goto continue_at_10
		else
			goto continue_at_11
		end
		::continue_at_12::
		FUNC_LIST[62](loc_0, 0LL)
		if load_i32_u8(memory_at_0, loc_1) ~= 37 then
			goto continue_at_21
		end
		::continue_at_22::
		while true do
			loc_9 = load_i32(memory_at_0, loc_0 + 4)
			if loc_9 == load_i32(memory_at_0, loc_0 + 84) then
				goto continue_at_24
			end
			store_i32(memory_at_0, loc_0 + 4, add_i32(loc_9, 1))
			loc_9 = load_i32_u8(memory_at_0, loc_9)
			goto continue_at_23
			::continue_at_24::
			reg_0 = FUNC_LIST[63](loc_0)
			loc_9 = reg_0
			::continue_at_23::
			if lt_u32(add_i32(loc_9, -9), 5) then
				goto continue_at_22
			end
			if loc_9 == 32 then
				goto continue_at_22
			end
			break
		end
		loc_1 = add_i32(loc_1, 1)
		goto continue_at_20
		::continue_at_21::
		loc_9 = load_i32(memory_at_0, loc_0 + 4)
		if loc_9 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_25
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_9, 1))
		loc_9 = load_i32_u8(memory_at_0, loc_9)
		goto continue_at_20
		::continue_at_25::
		reg_0 = FUNC_LIST[63](loc_0)
		loc_9 = reg_0
		::continue_at_20::
		if loc_9 == load_i32_u8(memory_at_0, loc_1) then
			goto continue_at_26
		end
		if load_i64(memory_at_0, loc_0 + 88) < 0LL then
			goto continue_at_27
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
		::continue_at_27::
		if loc_9 > -1 then
			goto continue_at_1
		end
		if loc_6 ~= 0 then
			goto continue_at_1
		end
		goto continue_at_2
		::continue_at_26::
		loc_7 = ((load_i64(memory_at_0, loc_0 + 96) + loc_7) + extend_i64_i32(sub_i32(load_i32(memory_at_0, loc_0 + 4), load_i32(memory_at_0, loc_0 + 40))))
		loc_1 = add_i32(loc_1, 1)
		goto continue_at_8
		::continue_at_11::
		loc_1 = add_i32(loc_1, 2)
		loc_10 = 0
		goto continue_at_9
		::continue_at_10::
		loc_9 = add_i32(loc_9, -48)
		if gt_u32(loc_9, 9) then
			goto continue_at_28
		end
		if load_i32_u8(memory_at_0, loc_1 + 2) ~= 36 then
			goto continue_at_28
		end
		store_i32(memory_at_0, loc_3 + 300, loc_2)
		loc_9 = (gt_u32(loc_9, 1) and add_i32(add_i32(loc_2, shl_i32(loc_9, 2)), -4) or loc_2)
		store_i32(memory_at_0, loc_3 + 296, add_i32(loc_9, 4))
		loc_10 = load_i32(memory_at_0, loc_9)
		loc_1 = add_i32(loc_1, 3)
		goto continue_at_9
		::continue_at_28::
		loc_1 = add_i32(loc_1, 1)
		loc_10 = load_i32(memory_at_0, loc_2)
		loc_2 = add_i32(loc_2, 4)
		::continue_at_9::
		loc_11 = 0
		loc_9 = load_i32_u8(memory_at_0, loc_1)
		if le_u32(band_i32(add_i32(loc_9, -48), 255), 9) then
			goto continue_at_30
		end
		loc_8 = 0
		goto continue_at_29
		::continue_at_30::
		loc_8 = 0
		::continue_at_31::
		while true do
			loc_8 = add_i32(add_i32(mul_i32(loc_8, 10), band_i32(loc_9, 255)), -48)
			loc_1 = add_i32(loc_1, 1)
			loc_9 = load_i32_u8(memory_at_0, loc_1)
			if lt_u32(band_i32(add_i32(loc_9, -48), 255), 10) then
				goto continue_at_31
			end
			break
		end
		::continue_at_29::
		if band_i32(loc_9, 255) == 109 then
			goto continue_at_33
		end
		loc_12 = loc_1
		goto continue_at_32
		::continue_at_33::
		loc_12 = add_i32(loc_1, 1)
		loc_13 = 0
		loc_11 = (loc_10 ~= 0 and 1 or 0)
		loc_9 = load_i32_u8(memory_at_0, loc_1 + 1)
		loc_14 = 0
		::continue_at_32::
		loc_15 = add_i32(loc_12, 1)
		loc_16 = 3
		if not br_map[3] then
			br_map[3] = (function()
				return { [0] = 4, 9, 4, 9, 4, 4, 4, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 4, 9, 9, 9, 9, 4, 9, 9, 4, 9, 9, 9, 9, 9, 4, 9, 4, 4, 4, 4, 4, 0, 4, 5, 9, 1, 9, 4, 4, 4, 9, 9, 4, 2, 4, 9, 9, 4, 9, 2, }
			end)()
		end
		temp = br_map[3][add_i32(band_i32(loc_9, 255), -65)] or 9
		if temp < 3 then
			if temp < 1 then
				goto continue_at_39
			elseif temp > 1 then
				goto continue_at_37
			else
				goto continue_at_38
			end
		elseif temp > 3 then
			if temp < 5 then
				goto continue_at_35
			elseif temp > 5 then
				goto continue_at_5
			else
				goto continue_at_34
			end
		else
			goto continue_at_36
		end
		::continue_at_39::
		loc_1 = (load_i32_u8(memory_at_0, loc_12 + 1) == 104 and 1 or 0)
		loc_15 = (loc_1 ~= 0 and add_i32(loc_12, 2) or loc_15)
		loc_16 = (loc_1 ~= 0 and -2 or -1)
		goto continue_at_34
		::continue_at_38::
		loc_1 = (load_i32_u8(memory_at_0, loc_12 + 1) == 108 and 1 or 0)
		loc_15 = (loc_1 ~= 0 and add_i32(loc_12, 2) or loc_15)
		loc_16 = (loc_1 ~= 0 and 3 or 1)
		goto continue_at_34
		::continue_at_37::
		loc_16 = 1
		goto continue_at_34
		::continue_at_36::
		loc_16 = 2
		goto continue_at_34
		::continue_at_35::
		loc_16 = 0
		loc_15 = loc_12
		::continue_at_34::
		loc_1 = load_i32_u8(memory_at_0, loc_15)
		loc_9 = (band_i32(loc_1, 47) == 3 and 1 or 0)
		loc_17 = (loc_9 ~= 0 and 1 or loc_16)
		loc_16 = (loc_9 ~= 0 and bor_i32(loc_1, 32) or loc_1)
		if not br_map[4] then
			br_map[4] = (function()
				return { [0] = 3, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, }
			end)()
		end
		temp = br_map[4][add_i32(loc_16, -91)] or 2
		if temp < 2 then
			if temp < 1 then
				goto continue_at_45
			else
				goto continue_at_44
			end
		elseif temp > 2 then
			goto continue_at_42
		else
			goto continue_at_43
		end
		::continue_at_45::
		loc_8 = (loc_8 > 1 and loc_8 or 1)
		goto continue_at_42
		::continue_at_44::
		if loc_10 == 0 then
			goto continue_at_41
		end
		if not br_map[5] then
			br_map[5] = (function()
				return { [0] = 0, 1, 2, 2, 6, 3, }
			end)()
		end
		temp = br_map[5][add_i32(loc_17, 2)] or 6
		if temp < 2 then
			if temp < 1 then
				goto continue_at_49
			else
				goto continue_at_48
			end
		elseif temp > 2 then
			if temp < 6 then
				goto continue_at_46
			else
				goto continue_at_41
			end
		else
			goto continue_at_47
		end
		::continue_at_49::
		store_i64_n8(memory_at_0, loc_10, loc_7)
		loc_1 = add_i32(loc_15, 1)
		goto continue_at_8
		::continue_at_48::
		store_i64_n16(memory_at_0, loc_10, loc_7)
		loc_1 = add_i32(loc_15, 1)
		goto continue_at_8
		::continue_at_47::
		store_i64_n32(memory_at_0, loc_10, loc_7)
		loc_1 = add_i32(loc_15, 1)
		goto continue_at_8
		::continue_at_46::
		store_i64(memory_at_0, loc_10, loc_7)
		loc_1 = add_i32(loc_15, 1)
		goto continue_at_8
		::continue_at_43::
		FUNC_LIST[62](loc_0, 0LL)
		::continue_at_50::
		while true do
			loc_1 = load_i32(memory_at_0, loc_0 + 4)
			if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
				goto continue_at_52
			end
			store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
			loc_1 = load_i32_u8(memory_at_0, loc_1)
			goto continue_at_51
			::continue_at_52::
			reg_0 = FUNC_LIST[63](loc_0)
			loc_1 = reg_0
			::continue_at_51::
			if lt_u32(add_i32(loc_1, -9), 5) then
				goto continue_at_50
			end
			if loc_1 == 32 then
				goto continue_at_50
			end
			break
		end
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if load_i64(memory_at_0, loc_0 + 88) < 0LL then
			goto continue_at_53
		end
		loc_1 = add_i32(loc_1, -1)
		store_i32(memory_at_0, loc_0 + 4, loc_1)
		::continue_at_53::
		loc_7 = ((load_i64(memory_at_0, loc_0 + 96) + loc_7) + extend_i64_i32(sub_i32(loc_1, load_i32(memory_at_0, loc_0 + 40))))
		::continue_at_42::
		loc_18 = extend_i64_i32(loc_8)
		FUNC_LIST[62](loc_0, loc_18)
		loc_1 = load_i32(memory_at_0, loc_0 + 4)
		if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
			goto continue_at_55
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
		goto continue_at_54
		::continue_at_55::
		reg_0 = FUNC_LIST[63](loc_0)
		if reg_0 < 0 then
			goto continue_at_5
		end
		::continue_at_54::
		if load_i64(memory_at_0, loc_0 + 88) < 0LL then
			goto continue_at_56
		end
		store_i32(memory_at_0, loc_0 + 4, add_i32(load_i32(memory_at_0, loc_0 + 4), -1))
		::continue_at_56::
		loc_1 = 16
		if not br_map[6] then
			br_map[6] = (function()
				return { [0] = 5, 9, 9, 9, 5, 5, 5, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 4, 9, 9, 0, 9, 9, 9, 9, 9, 5, 9, 0, 2, 5, 5, 5, 9, 3, 9, 9, 9, 9, 9, 1, 4, 9, 9, 0, 9, 2, 9, 9, 4, }
			end)()
		end
		temp = br_map[6][add_i32(loc_16, -65)] or 9
		if temp < 3 then
			if temp < 1 then
				goto continue_at_66
			elseif temp > 1 then
				goto continue_at_64
			else
				goto continue_at_65
			end
		elseif temp > 3 then
			if temp < 5 then
				goto continue_at_62
			elseif temp > 5 then
				goto continue_at_57
			else
				goto continue_at_61
			end
		else
			goto continue_at_63
		end
		::continue_at_66::
		if not br_map[7] then
			br_map[7] = (function()
				return { [0] = 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, }
			end)()
		end
		temp = br_map[7][add_i32(loc_16, -99)] or 1
		if temp < 1 then
			goto continue_at_68
		else
			goto continue_at_67
		end
		::continue_at_68::
		if 257 == 0 then
			goto continue_at_69
		end
		rt.store.fill(memory_at_0, add_i32(loc_3, 16), 257, 255)
		::continue_at_69::
		store_i32_n8(memory_at_0, loc_3 + 16, 0)
		if loc_16 ~= 115 then
			goto continue_at_58
		end
		store_i32(memory_at_0, loc_5, 0)
		store_i32_n8(memory_at_0, add_i32(loc_5, 4), 0)
		store_i32_n8(memory_at_0, loc_3 + 49, 0)
		goto continue_at_58
		::continue_at_67::
		loc_9 = (load_i32_u8(memory_at_0, loc_15 + 1) == 94 and 1 or 0)
		if 257 == 0 then
			goto continue_at_70
		end
		rt.store.fill(memory_at_0, add_i32(loc_3, 16), 257, loc_9)
		::continue_at_70::
		store_i32_n8(memory_at_0, loc_3 + 16, 0)
		loc_1 = (loc_9 ~= 0 and add_i32(loc_15, 2) or add_i32(loc_15, 1))
		loc_15 = load_i32_u8(memory_at_0, add_i32(loc_15, (loc_9 ~= 0 and 2 or 1)))
		if loc_15 == 45 then
			goto continue_at_73
		end
		if loc_15 == 93 then
			goto continue_at_72
		end
		loc_15 = bxor_i32(loc_9, 1)
		goto continue_at_60
		::continue_at_73::
		loc_15 = bxor_i32(loc_9, 1)
		store_i32_n8(memory_at_0, loc_3 + 62, loc_15)
		goto continue_at_71
		::continue_at_72::
		loc_15 = bxor_i32(loc_9, 1)
		store_i32_n8(memory_at_0, loc_3 + 110, loc_15)
		::continue_at_71::
		loc_9 = 0
		goto continue_at_59
		::continue_at_65::
		loc_1 = 8
		goto continue_at_62
		::continue_at_64::
		loc_1 = 10
		goto continue_at_62
		::continue_at_63::
		loc_1 = 0
		::continue_at_62::
		reg_0 = FUNC_LIST[64](loc_0, loc_1, 0, -1LL)
		loc_18 = reg_0
		if load_i64(memory_at_0, loc_0 + 96) == (0LL - extend_i64_i32(sub_i32(load_i32(memory_at_0, loc_0 + 4), load_i32(memory_at_0, loc_0 + 40)))) then
			goto continue_at_4
		end
		if loc_16 ~= 112 then
			goto continue_at_74
		end
		if loc_10 == 0 then
			goto continue_at_74
		end
		store_i64_n32(memory_at_0, loc_10, loc_18)
		goto continue_at_57
		::continue_at_74::
		if loc_10 == 0 then
			goto continue_at_57
		end
		if not br_map[8] then
			br_map[8] = (function()
				return { [0] = 0, 1, 2, 2, 8, 3, }
			end)()
		end
		temp = br_map[8][add_i32(loc_17, 2)] or 8
		if temp < 2 then
			if temp < 1 then
				goto continue_at_78
			else
				goto continue_at_77
			end
		elseif temp > 2 then
			if temp < 8 then
				goto continue_at_75
			else
				goto continue_at_57
			end
		else
			goto continue_at_76
		end
		::continue_at_78::
		store_i64_n8(memory_at_0, loc_10, loc_18)
		goto continue_at_57
		::continue_at_77::
		store_i64_n16(memory_at_0, loc_10, loc_18)
		goto continue_at_57
		::continue_at_76::
		store_i64_n32(memory_at_0, loc_10, loc_18)
		goto continue_at_57
		::continue_at_75::
		store_i64(memory_at_0, loc_10, loc_18)
		goto continue_at_57
		::continue_at_61::
		reg_0 = FUNC_LIST[67](loc_0, loc_17, 0)
		loc_19 = reg_0
		if load_i64(memory_at_0, loc_0 + 96) == (0LL - extend_i64_i32(sub_i32(load_i32(memory_at_0, loc_0 + 4), load_i32(memory_at_0, loc_0 + 40)))) then
			goto continue_at_4
		end
		if loc_10 == 0 then
			goto continue_at_57
		end
		if not br_map[9] then
			br_map[9] = (function()
				return { [0] = 0, 1, 2, }
			end)()
		end
		temp = br_map[9][loc_17] or 6
		if temp < 2 then
			if temp < 1 then
				goto continue_at_81
			else
				goto continue_at_80
			end
		elseif temp > 2 then
			goto continue_at_57
		else
			goto continue_at_79
		end
		::continue_at_81::
		store_f32(memory_at_0, loc_10, demote_f32_f64(loc_19))
		goto continue_at_57
		::continue_at_80::
		store_f64(memory_at_0, loc_10, loc_19)
		goto continue_at_57
		::continue_at_79::
		FUNC_LIST[73]()
		error("out of code bounds")
		::continue_at_60::
		loc_9 = 1
		::continue_at_59::
		::continue_at_82::
		while true do
			if not br_map[10] then
				br_map[10] = (function()
					return { [0] = 0, 1, }
				end)()
			end
			temp = br_map[10][loc_9] or 1
			if temp < 1 then
				goto continue_at_84
			else
				goto continue_at_83
			end
			::continue_at_84::
			loc_1 = add_i32(loc_1, 1)
			loc_9 = 1
			goto continue_at_82
			::continue_at_83::
			loc_9 = load_i32_u8(memory_at_0, loc_1)
			if loc_9 == 45 then
				goto continue_at_86
			end
			if loc_9 == 0 then
				goto continue_at_5
			end
			if loc_9 ~= 93 then
				goto continue_at_85
			end
			loc_15 = loc_1
			goto continue_at_58
			::continue_at_86::
			loc_9 = 45
			loc_20 = load_i32_u8(memory_at_0, loc_1 + 1)
			if loc_20 == 0 then
				goto continue_at_85
			end
			if loc_20 == 93 then
				goto continue_at_85
			end
			loc_12 = add_i32(loc_1, 1)
			loc_1 = load_i32_u8(memory_at_0, add_i32(loc_1, -1))
			if lt_u32(loc_1, loc_20) then
				goto continue_at_88
			end
			loc_9 = loc_20
			goto continue_at_87
			::continue_at_88::
			::continue_at_89::
			while true do
				store_i32_n8(memory_at_0, add_i32(loc_4, loc_1), loc_15)
				loc_1 = add_i32(loc_1, 1)
				loc_9 = load_i32_u8(memory_at_0, loc_12)
				if lt_u32(loc_1, loc_9) then
					goto continue_at_89
				end
				break
			end
			::continue_at_87::
			loc_1 = loc_12
			::continue_at_85::
			store_i32_n8(memory_at_0, add_i32(loc_9, add_i32(loc_3, 16)) + 1, loc_15)
			loc_9 = 0
			goto continue_at_82
		end
		::continue_at_58::
		loc_20 = (loc_16 ~= 99 and 1 or 0)
		loc_12 = (loc_20 ~= 0 and 31 or add_i32(loc_8, 1))
		if loc_17 ~= 1 then
			goto continue_at_91
		end
		loc_9 = loc_10
		if loc_11 == 0 then
			goto continue_at_92
		end
		reg_0 = FUNC_LIST[8](shl_i32(loc_12, 2))
		loc_9 = reg_0
		if loc_9 == 0 then
			goto continue_at_6
		end
		::continue_at_92::
		store_i64(memory_at_0, loc_3 + 288, 0LL)
		loc_1 = 0
		::continue_at_94::
		while true do
			loc_8 = loc_9
			::continue_at_95::
			while true do
				loc_9 = load_i32(memory_at_0, loc_0 + 4)
				if loc_9 == load_i32(memory_at_0, loc_0 + 84) then
					goto continue_at_97
				end
				store_i32(memory_at_0, loc_0 + 4, add_i32(loc_9, 1))
				loc_9 = load_i32_u8(memory_at_0, loc_9)
				goto continue_at_96
				::continue_at_97::
				reg_0 = FUNC_LIST[63](loc_0)
				loc_9 = reg_0
				::continue_at_96::
				if load_i32_u8(memory_at_0, add_i32(add_i32(loc_9, add_i32(loc_3, 16)), 1)) == 0 then
					goto continue_at_93
				end
				store_i32_n8(memory_at_0, loc_3 + 11, loc_9)
				reg_0 = FUNC_LIST[70](add_i32(loc_3, 12), add_i32(loc_3, 11), 1, add_i32(loc_3, 288))
				loc_9 = reg_0
				if loc_9 == -2 then
					goto continue_at_95
				end
				if loc_9 == -1 then
					goto continue_at_40
				end
				if loc_8 == 0 then
					goto continue_at_98
				end
				store_i32(memory_at_0, add_i32(loc_8, shl_i32(loc_1, 2)), load_i32(memory_at_0, loc_3 + 12))
				loc_1 = add_i32(loc_1, 1)
				::continue_at_98::
				if loc_11 == 0 then
					goto continue_at_95
				end
				if loc_1 ~= loc_12 then
					goto continue_at_95
				end
				break
			end
			loc_12 = bor_i32(shl_i32(loc_12, 1), 1)
			reg_0 = FUNC_LIST[13](loc_8, shl_i32(loc_12, 2))
			loc_9 = reg_0
			if loc_9 ~= 0 then
				goto continue_at_94
			end
			break
		end
		loc_13 = 0
		loc_14 = loc_8
		loc_11 = 1
		goto continue_at_5
		::continue_at_93::
		loc_13 = 0
		loc_14 = loc_8
		reg_0 = FUNC_LIST[71](add_i32(loc_3, 288))
		if reg_0 ~= 0 then
			goto continue_at_90
		end
		goto continue_at_7
		::continue_at_91::
		if loc_11 == 0 then
			goto continue_at_99
		end
		reg_0 = FUNC_LIST[8](loc_12)
		loc_9 = reg_0
		if loc_9 == 0 then
			goto continue_at_6
		end
		loc_1 = 0
		::continue_at_100::
		while true do
			loc_8 = loc_9
			::continue_at_101::
			while true do
				loc_9 = load_i32(memory_at_0, loc_0 + 4)
				if loc_9 == load_i32(memory_at_0, loc_0 + 84) then
					goto continue_at_103
				end
				store_i32(memory_at_0, loc_0 + 4, add_i32(loc_9, 1))
				loc_9 = load_i32_u8(memory_at_0, loc_9)
				goto continue_at_102
				::continue_at_103::
				reg_0 = FUNC_LIST[63](loc_0)
				loc_9 = reg_0
				::continue_at_102::
				if load_i32_u8(memory_at_0, add_i32(add_i32(loc_9, add_i32(loc_3, 16)), 1)) ~= 0 then
					goto continue_at_104
				end
				loc_14 = 0
				loc_13 = loc_8
				goto continue_at_90
				::continue_at_104::
				store_i32_n8(memory_at_0, add_i32(loc_8, loc_1), loc_9)
				loc_1 = add_i32(loc_1, 1)
				if loc_12 ~= loc_1 then
					goto continue_at_101
				end
				break
			end
			loc_12 = bor_i32(shl_i32(loc_12, 1), 1)
			reg_0 = FUNC_LIST[13](loc_8, loc_12)
			loc_9 = reg_0
			if loc_9 ~= 0 then
				goto continue_at_100
			end
			break
		end
		loc_14 = 0
		loc_13 = loc_8
		loc_11 = 1
		goto continue_at_5
		::continue_at_99::
		if loc_10 == 0 then
			goto continue_at_105
		end
		loc_1 = 0
		::continue_at_106::
		while true do
			loc_9 = load_i32(memory_at_0, loc_0 + 4)
			if loc_9 == load_i32(memory_at_0, loc_0 + 84) then
				goto continue_at_108
			end
			store_i32(memory_at_0, loc_0 + 4, add_i32(loc_9, 1))
			loc_9 = load_i32_u8(memory_at_0, loc_9)
			goto continue_at_107
			::continue_at_108::
			reg_0 = FUNC_LIST[63](loc_0)
			loc_9 = reg_0
			::continue_at_107::
			if load_i32_u8(memory_at_0, add_i32(add_i32(loc_9, add_i32(loc_3, 16)), 1)) ~= 0 then
				goto continue_at_109
			end
			loc_14 = 0
			loc_8 = loc_10
			loc_13 = loc_10
			goto continue_at_90
			::continue_at_109::
			store_i32_n8(memory_at_0, add_i32(loc_10, loc_1), loc_9)
			loc_1 = add_i32(loc_1, 1)
			goto continue_at_106
		end
		::continue_at_105::
		::continue_at_110::
		while true do
			loc_1 = load_i32(memory_at_0, loc_0 + 4)
			if loc_1 == load_i32(memory_at_0, loc_0 + 84) then
				goto continue_at_112
			end
			store_i32(memory_at_0, loc_0 + 4, add_i32(loc_1, 1))
			loc_1 = load_i32_u8(memory_at_0, loc_1)
			goto continue_at_111
			::continue_at_112::
			reg_0 = FUNC_LIST[63](loc_0)
			loc_1 = reg_0
			::continue_at_111::
			if load_i32_u8(memory_at_0, add_i32(add_i32(loc_1, add_i32(loc_3, 16)), 1)) ~= 0 then
				goto continue_at_110
			end
			break
		end
		loc_8 = 0
		loc_13 = 0
		loc_14 = 0
		loc_1 = 0
		::continue_at_90::
		loc_9 = load_i32(memory_at_0, loc_0 + 4)
		if load_i64(memory_at_0, loc_0 + 88) < 0LL then
			goto continue_at_113
		end
		loc_9 = add_i32(loc_9, -1)
		store_i32(memory_at_0, loc_0 + 4, loc_9)
		::continue_at_113::
		loc_21 = (load_i64(memory_at_0, loc_0 + 96) + extend_i64_i32(sub_i32(loc_9, load_i32(memory_at_0, loc_0 + 40))))
		if loc_21 == 0LL then
			goto continue_at_4
		end
		if bor_i32(loc_20, (loc_21 == loc_18 and 1 or 0)) == 0 then
			goto continue_at_4
		end
		if loc_11 == 0 then
			goto continue_at_114
		end
		store_i32(memory_at_0, loc_10, loc_8)
		::continue_at_114::
		if loc_16 == 99 then
			goto continue_at_57
		end
		if loc_14 == 0 then
			goto continue_at_115
		end
		store_i32(memory_at_0, add_i32(loc_14, shl_i32(loc_1, 2)), 0)
		::continue_at_115::
		if loc_13 ~= 0 then
			goto continue_at_116
		end
		loc_13 = 0
		goto continue_at_57
		::continue_at_116::
		store_i32_n8(memory_at_0, add_i32(loc_13, loc_1), 0)
		::continue_at_57::
		loc_7 = ((load_i64(memory_at_0, loc_0 + 96) + loc_7) + extend_i64_i32(sub_i32(load_i32(memory_at_0, loc_0 + 4), load_i32(memory_at_0, loc_0 + 40))))
		loc_6 = add_i32(loc_6, (loc_10 ~= 0 and 1 or 0))
		::continue_at_41::
		loc_1 = add_i32(loc_15, 1)
		goto continue_at_8
		::continue_at_40::
		break
	end
	loc_13 = 0
	::continue_at_7::
	loc_14 = loc_8
	goto continue_at_5
	::continue_at_6::
	loc_11 = 1
	loc_13 = 0
	loc_14 = 0
	::continue_at_5::
	loc_6 = (loc_6 ~= 0 and loc_6 or -1)
	::continue_at_4::
	if loc_11 == 0 then
		goto continue_at_1
	end
	FUNC_LIST[11](loc_13)
	FUNC_LIST[11](loc_14)
	goto continue_at_1
	::continue_at_2::
	loc_6 = -1
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_3, 304)
	reg_0 = loc_6
	return reg_0
end
FUNC_LIST[73] = function()
	local reg_0
	reg_0 = FUNC_LIST[49](2846, 4104)
	FUNC_LIST[21]()
	error("out of code bounds")
end
FUNC_LIST[74] = function(loc_0, loc_1)
	local reg_0
	reg_0 = FUNC_LIST[72](4224, loc_0, loc_1)
	return reg_0
end
FUNC_LIST[75] = function(loc_0, loc_1)
	local loc_2 = 0
	local reg_0
	loc_2 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_2
	store_i32(memory_at_0, loc_2 + 12, loc_1)
	reg_0 = FUNC_LIST[74](loc_0, loc_1)
	loc_1 = reg_0
	GLOBAL_LIST[0].value = add_i32(loc_2, 16)
	reg_0 = loc_1
	return reg_0
end
FUNC_LIST[76] = function(loc_0, loc_1)
	local loc_2 = 0
	local loc_3 = 0
	local loc_4 = 0
	local reg_0
	loc_2 = sub_i32(GLOBAL_LIST[0].value, 16)
	GLOBAL_LIST[0].value = loc_2
	store_i32_n8(memory_at_0, loc_2 + 15, loc_1)
	loc_3 = load_i32(memory_at_0, loc_0 + 16)
	if loc_3 ~= 0 then
		goto continue_at_2
	end
	reg_0 = FUNC_LIST[38](loc_0)
	if reg_0 == 0 then
		goto continue_at_3
	end
	loc_3 = -1
	goto continue_at_1
	::continue_at_3::
	loc_3 = load_i32(memory_at_0, loc_0 + 16)
	::continue_at_2::
	loc_4 = load_i32(memory_at_0, loc_0 + 20)
	if loc_4 == loc_3 then
		goto continue_at_4
	end
	loc_3 = band_i32(loc_1, 255)
	if load_i32(memory_at_0, loc_0 + 64) == loc_3 then
		goto continue_at_4
	end
	store_i32(memory_at_0, loc_0 + 20, add_i32(loc_4, 1))
	store_i32_n8(memory_at_0, loc_4, loc_1)
	goto continue_at_1
	::continue_at_4::
	reg_0 = TABLE_LIST[0].data[load_i32(memory_at_0, loc_0 + 32)](loc_0, add_i32(loc_2, 15), 1)
	if reg_0 == 1 then
		goto continue_at_5
	end
	loc_3 = -1
	goto continue_at_1
	::continue_at_5::
	loc_3 = load_i32_u8(memory_at_0, loc_2 + 15)
	::continue_at_1::
	GLOBAL_LIST[0].value = add_i32(loc_2, 16)
	reg_0 = loc_3
	return reg_0
end
FUNC_LIST[77] = function(loc_0)
	local reg_0
	reg_0 = FUNC_LIST[49](loc_0, 3984)
	if reg_0 >= 0 then
		goto continue_at_1
	end
	reg_0 = -1
	goto continue_at_0
	::continue_at_1::
	if load_i32(memory_at_0, 0 + 4048) == 10 then
		goto continue_at_2
	end
	loc_0 = load_i32(memory_at_0, 0 + 4004)
	if loc_0 == load_i32(memory_at_0, 0 + 4000) then
		goto continue_at_2
	end
	store_i32(memory_at_0, 0 + 4004, add_i32(loc_0, 1))
	store_i32_n8(memory_at_0, loc_0, 10)
	reg_0 = 0
	goto continue_at_0
	::continue_at_2::
	reg_0 = FUNC_LIST[76](3984, 10)
	reg_0 = shr_i32(reg_0, 31)
	::continue_at_0::
	return reg_0
end
FUNC_LIST[78] = function()
	local loc_0 = 0
	local loc_1 = 0
	local loc_2 = 0
	local loc_3 = 0
	local loc_4 = 0LL
	local loc_5 = 0LL
	local loc_6 = 0LL
	local loc_7 = 0LL
	local loc_8 = 0LL
	local loc_9 = 0LL
	local loc_10 = 0LL
	local loc_11 = 0LL
	local loc_12 = 0LL
	local loc_13 = 0LL
	local loc_14 = 0
	local loc_15 = 0
	local loc_16 = 0LL
	local loc_17 = 0LL
	local loc_18 = 0LL
	local loc_19 = 0LL
	local reg_0
	local br_map, temp = {}, nil
	loc_0 = sub_i32(GLOBAL_LIST[0].value, 128)
	GLOBAL_LIST[0].value = loc_0
	loc_1 = 0
	reg_0 = FUNC_LIST[55](2833, 0)
	reg_0 = FUNC_LIST[56](load_i32(memory_at_0, 0 + 1024))
	store_i32(memory_at_0, loc_0, add_i32(loc_0, 16))
	reg_0 = FUNC_LIST[75](2775, loc_0)
	loc_2 = 2803
	reg_0 = FUNC_LIST[25](add_i32(loc_0, 16))
	if reg_0 == 32 then
		goto continue_at_2
	end
	loc_3 = 1
	goto continue_at_1
	::continue_at_2::
	loc_4 = load_i64(memory_at_0, 0 + 4384)
	loc_5 = bor_i64(bor_i64(bor_i64(shl_i64(loc_4, 56LL), shl_i64(band_i64(loc_4, 65280LL), 40LL)), bor_i64(shl_i64(band_i64(loc_4, 16711680LL), 24LL), shl_i64(band_i64(loc_4, 4278190080LL), 8LL))), bor_i64(bor_i64(band_i64(shr_u64(loc_4, 8LL), 4278190080LL), band_i64(shr_u64(loc_4, 24LL), 16711680LL)), bor_i64(band_i64(shr_u64(loc_4, 40LL), 65280LL), shr_u64(loc_4, 56LL))))
	loc_6 = (load_i64(memory_at_0, 0 + 4400) * -511LL)
	loc_7 = (load_i64(memory_at_0, 0 + 4408) * -511LL)
	loc_8 = load_i64(memory_at_0, 0 + 4352)
	loc_9 = bxor_i64(rotl_i64(loc_8, 39LL), loc_8)
	loc_10 = load_i64(memory_at_0, 0 + 4360)
	loc_11 = load_i64(memory_at_0, 0 + 4368)
	loc_12 = load_i64(memory_at_0, 0 + 4376)
	loc_13 = load_i64(memory_at_0, 0 + 4392)
	loc_14 = 4416
	loc_15 = add_i32(loc_0, 16)
	::continue_at_3::
	while true do
		loc_4 = load_i64_u32(memory_at_0, loc_15)
		if not br_map[1] then
			br_map[1] = (function()
				return { [0] = 0, 1, 2, 3, 4, 5, 6, 7, }
			end)()
		end
		temp = br_map[1][loc_1] or 0
		if temp < 4 then
			if temp < 2 then
				if temp < 1 then
					goto continue_at_12
				else
					goto continue_at_11
				end
			elseif temp > 2 then
				goto continue_at_9
			else
				goto continue_at_10
			end
		elseif temp > 4 then
			if temp < 6 then
				goto continue_at_7
			elseif temp > 6 then
				goto continue_at_5
			else
				goto continue_at_6
			end
		else
			goto continue_at_8
		end
		::continue_at_12::
		loc_16 = band_i64(loc_4, 62LL)
		loc_17 = bor_i64(loc_16, 1LL)
		loc_18 = (bxor_i64(rotl_i64(loc_8, (band_i64(shl_i64(-2841402449925361436LL, loc_16), 36LL) + 49LL)), loc_9) + bxor_i64((rotr_i64(shr_u64(4759118972362874166LL, loc_16), loc_17) - loc_4), -3306012594466711124LL))
		loc_17 = rotl_i64((shl_i64(loc_18, bor_i64(band_i64((band_i64(shr_u64(4356822460271002287LL, loc_16), loc_4) + 28LL), 62LL), 1LL)) + loc_18), bor_i64(band_i64(rotl_i64(-3599654368322586570LL, loc_17), 14LL), 1LL))
		loc_17 = bxor_i64(shl_i64(loc_17, bor_i64(band_i64(((shr_u64((loc_4 * 742925643253982954LL), 56LL) + loc_4) * 47LL), 62LL), 1LL)), loc_17)
		loc_4 = bxor_i64(bxor_i64(rotr_i64(loc_17, bor_i64((shl_i64(-4774275202249070850LL, loc_16) * loc_4), 1LL)), rotl_i64(loc_17, 57LL)), loc_17)
		goto continue_at_4
		::continue_at_11::
		loc_18 = (loc_10 * bor_i64((loc_4 * 180512385711709LL), 7380094324862376181LL))
		loc_16 = band_i64(loc_4, 62LL)
		loc_17 = bor_i64(loc_16, 1LL)
		loc_18 = bxor_i64(shr_u64(loc_18, bor_i64(band_i64(rotr_i64((band_i64(shr_u64(1383475029465073410LL, loc_16), loc_4) - loc_4), loc_17), 62LL), 1LL)), loc_18)
		loc_4 = bxor_i64(bxor_i64(rotl_i64(loc_18, bor_i64(shr_u64(((loc_4 * -8341237817759413455LL) + 5858299301512691920LL), loc_17), 1LL)), rotl_i64(loc_18, bor_i64(shr_u64(shl_i64((1003390LL - loc_4), loc_17), 15LL), 1LL))), loc_18)
		loc_4 = (bor_i64(bor_i64(bor_i64(shl_i64(loc_4, 56LL), shl_i64(band_i64(loc_4, 65280LL), 40LL)), bor_i64(shl_i64(band_i64(loc_4, 16711680LL), 24LL), shl_i64(band_i64(loc_4, 4278190080LL), 8LL))), bor_i64(bor_i64(band_i64(shr_u64(loc_4, 8LL), 4278190080LL), band_i64(shr_u64(loc_4, 24LL), 16711680LL)), bor_i64(band_i64(shr_u64(loc_4, 40LL), 65280LL), shr_u64(loc_4, 56LL)))) + band_i64((shl_i64(-6512376135701343602LL, loc_16) + 9021780107656055508LL), 4886913136624203210LL))
		goto continue_at_4
		::continue_at_10::
		loc_16 = band_i64(loc_4, 62LL)
		loc_17 = (bxor_i64(bxor_i64(rotr_i64(loc_11, bor_i64(bxor_i64((loc_4 * 52LL), loc_4), 1LL)), rotr_i64(loc_11, bxor_i64(shl_i64(1150443877981745306LL, loc_16), 11LL))), loc_11) * bor_i64(bxor_i64((shl_i64(-1314727533138742334LL, loc_16) + loc_4), -1LL), 1LL))
		loc_17 = bxor_i64(bxor_i64(rotl_i64(loc_17, bor_i64(shr_u64(((band_i64(loc_4, 81990LL) * 48316LL) + 15360LL), 11LL), 1LL)), rotl_i64(loc_17, 53LL)), loc_17)
		loc_16 = bxor_i64(bxor_i64(rotl_i64(loc_17, bor_i64(shr_u64((shl_i64(shr_u64(6474080420971629382LL, loc_16), 11LL) + 1321443404618737664LL), 56LL), 1LL)), rotl_i64(loc_17, bor_i64((0LL - band_i64(loc_4, 14LL)), 27LL))), loc_17)
		loc_16 = (loc_16 - shl_i64(loc_16, bor_i64(band_i64((29LL - loc_4), 62LL), 1LL)))
		loc_4 = bxor_i64(bxor_i64(rotl_i64(loc_16, 63LL), rotr_i64(loc_16, bor_i64((band_i64((rotr_i64(499867118132017422LL, bor_i64(loc_4, 1LL)) - loc_4), loc_4) - loc_4), 1LL))), loc_16)
		goto continue_at_4
		::continue_at_9::
		loc_16 = band_i64(loc_4, 62LL)
		loc_17 = bor_i64(loc_16, 1LL)
		loc_18 = bxor_i64((rotl_i64(loc_12, bor_i64(rotr_i64(rotl_i64(-3680473152504818101LL, loc_17), loc_17), 1LL)) + rotl_i64(bxor_i64(band_i64((2924367758LL - loc_4), loc_4), -1LL), 49LL)), rotl_i64(shr_u64(bor_i64(loc_4, 323389404160168651LL), loc_17), loc_17))
		loc_19 = shr_u64(4824063971456177356LL, loc_16)
		loc_18 = bxor_i64(shr_u64(loc_18, bor_i64(shr_u64(bor_i64(shl_i64(band_i64(loc_19, 1792LL), 40LL), shl_i64(band_i64(loc_19, 12582912LL), 24LL)), 45LL), 1LL)), loc_18)
		loc_18 = bxor_i64(bxor_i64(rotl_i64(loc_18, bor_i64(shr_u64((loc_4 + 565LL), 5LL), 1LL)), rotr_i64(loc_18, bor_i64(shr_u64(shl_i64(-7575533352951092208LL, loc_16), 56LL), 1LL))), loc_18)
		loc_18 = bxor_i64(shl_i64(loc_18, bor_i64(band_i64(loc_4, 46LL), 17LL)), loc_18)
		loc_18 = (shl_i64(loc_18, bor_i64(band_i64((bxor_i64(shl_i64(-5156880989505199132LL, loc_16), -1LL) * loc_4), 62LL), 1LL)) + loc_18)
		loc_4 = (loc_18 - shl_i64(loc_18, bor_i64(band_i64(shl_i64((shr_u64(5172634985249747992LL, loc_16) - loc_4), loc_17), 62LL), 1LL)))
		goto continue_at_4
		::continue_at_8::
		reg_0 = bxor_i64(rotl_i64(loc_5, bor_i64((loc_4 * 55LL), 1LL)), -4619238845427684646LL)
		loc_4 = bxor_i64((loc_4 + -4616715144965187269LL), -8569173798327520083LL)
		loc_4 = ((reg_0 + bor_i64(band_i64(shr_u64(loc_4, 8LL), 3741319168LL), bor_i64(bor_i64(shl_i64(loc_4, 56LL), shl_i64(band_i64(loc_4, 65280LL), 40LL)), bor_i64(shl_i64(band_i64(loc_4, 16711680LL), 24LL), shl_i64(band_i64(loc_4, 4278190080LL), 8LL))))) + 1047094LL)
		loc_4 = bxor_i64(shl_i64(loc_4, 39LL), loc_4)
		goto continue_at_4
		::continue_at_7::
		loc_17 = (loc_13 + bxor_i64(loc_4, 36051668767407190LL))
		loc_18 = band_i64(loc_4, 62LL)
		loc_16 = bor_i64(loc_18, 1LL)
		loc_17 = ((loc_17 - bor_i64(rotl_i64(rotr_i64(-7384894205260299553LL, loc_16), loc_16), -2299178146027875472LL)) + shl_i64(loc_17, bor_i64(band_i64(((band_i64(loc_4, 8LL) * loc_4) + 26LL), 58LL), 1LL)))
		loc_4 = bxor_i64(bxor_i64(loc_17, shl_i64(loc_17, bor_i64(band_i64((shl_i64(shr_i64(-4331792876883399301LL, loc_18), loc_16) + loc_4), 62LL), 1LL))), 5185608289172264064LL)
		goto continue_at_4
		::continue_at_6::
		loc_16 = band_i64(loc_4, 62LL)
		loc_17 = bor_i64(loc_16, 1LL)
		loc_17 = (loc_6 + band_i64(rotr_i64(shr_u64(bor_i64(loc_4, -5056680446052056208LL), loc_17), loc_17), -7361207612496853418LL))
		loc_17 = bxor_i64(bxor_i64(rotr_i64(loc_17, bxor_i64(band_i64(loc_16, (loc_4 + 40LL)), 13LL)), rotl_i64(loc_17, bor_i64((bxor_i64((loc_4 + 22LL), 30LL) - loc_4), 1LL))), loc_17)
		loc_4 = (((((-6610288770926234540LL - loc_4) * 3123491549520060319LL) + bxor_i64(loc_17, -1LL)) + shl_i64((loc_17 + 1LL), bor_i64(band_i64(bor_i64(shr_u64(2315141858787142786LL, loc_16), loc_4), 62LL), 1LL))) * 8796093022209LL)
		goto continue_at_4
		::continue_at_5::
		loc_16 = band_i64(loc_4, 62LL)
		loc_17 = bor_i64(loc_16, 1LL)
		loc_17 = (loc_7 + band_i64(rotr_i64(shr_u64(bor_i64(loc_4, -5056680446052056208LL), loc_17), loc_17), -7361207612496853418LL))
		loc_17 = bxor_i64(bxor_i64(rotr_i64(loc_17, bxor_i64(band_i64(loc_16, (loc_4 + 40LL)), 13LL)), rotl_i64(loc_17, bor_i64((bxor_i64((loc_4 + 22LL), 30LL) - loc_4), 1LL))), loc_17)
		loc_4 = (((((-6610288770926234540LL - loc_4) * 3123491549520060319LL) + bxor_i64(loc_17, -1LL)) + shl_i64((loc_17 + 1LL), bor_i64(band_i64(bor_i64(shr_u64(2315141858787142786LL, loc_16), loc_4), 62LL), 1LL))) * 8796093022209LL)
		::continue_at_4::
		loc_3 = 0
		if loc_4 ~= load_i64(memory_at_0, loc_14) then
			goto continue_at_1
		end
		loc_15 = add_i32(loc_15, 4)
		loc_14 = add_i32(loc_14, 8)
		loc_1 = add_i32(loc_1, 1)
		if loc_1 ~= 8 then
			goto continue_at_3
		end
		break
	end
	loc_2 = 2819
	::continue_at_1::
	reg_0 = FUNC_LIST[77](loc_2)
	GLOBAL_LIST[0].value = add_i32(loc_0, 128)
	reg_0 = loc_3
	return reg_0
end
FUNC_LIST[79] = function(loc_0, loc_1, loc_2, loc_3, loc_4)
	local loc_5 = 0LL
	local reg_0
	local reg_1
	reg_1 = ((loc_4 * loc_1) + (loc_2 * loc_3))
	loc_2 = shr_u64(loc_3, 32LL)
	loc_4 = shr_u64(loc_1, 32LL)
	loc_3 = band_i64(loc_3, 4294967295LL)
	loc_1 = band_i64(loc_1, 4294967295LL)
	loc_5 = (loc_3 * loc_1)
	loc_3 = (shr_u64(loc_5, 32LL) + (loc_3 * loc_4))
	loc_1 = (band_i64(loc_3, 4294967295LL) + (loc_2 * loc_1))
	store_i64(memory_at_0, loc_0 + 8, (((reg_1 + (loc_2 * loc_4)) + shr_u64(loc_3, 32LL)) + shr_u64(loc_1, 32LL)))
	store_i64(memory_at_0, loc_0, bor_i64(shl_i64(loc_1, 32LL), band_i64(loc_5, 4294967295LL)))
end
local function run_init_code()
	TABLE_LIST[0] = { min = 6, max = 6, data = {} }
	MEMORY_LIST[0] = rt.allocator.new(2, 65535)
	GLOBAL_LIST[0] = { value = 72640 }
	GLOBAL_LIST[1] = { value = 0 }
	do
		local target = TABLE_LIST[0].data
		local offset = 1
		local data = { FUNC_LIST[30],FUNC_LIST[28],FUNC_LIST[32],FUNC_LIST[34],FUNC_LIST[59], }
		table.move(data, 1, #data, offset, target)
	end
	rt.store.string(MEMORY_LIST[0], 1024,"\x90\x0f\x00\x00Success\x00Illegal byte sequence\x00Domain error\x00Result not representable\x00Not a tty\x00Permission denied\x00Operation not permitted\x00No such file or directory\x00No such process\x00File exists\x00Value too large for data type\x00No space left on device\x00Out of memory\x00Resource busy\x00Interrupted system call\x00Resource temporarily unavailable\x00Invalid seek\x00Cross-device link\x00Read-only file system\x00Directory not empty\x00Connection reset by peer\x00Operation timed out\x00Connection refused\x00Host is unreachable\x00Address in use\x00Broken pipe\x00I/O error\x00No such device or address\x00No such device\x00Not a directory\x00Is a directory\x00Text file busy\x00Exec format error\x00Invalid argument\x00Argument list too long\x00Symbolic link loop\x00Filename too long\x00Too many open files in system\x00No file descriptors available\x00Bad file descriptor\x00No child process\x00Bad address\x00File too large\x00Too many links\x00No locks available\x00Resource deadlock would occur\x00State not recoverable\x00Previous owner died\x00Operation canceled\x00Function not implemented\x00No message of desired type\x00Identifier removed\x00Link has been severed\x00Protocol error\x00Bad message\x00Not a socket\x00Destination address required\x00Message too large\x00Protocol wrong type for socket\x00Protocol not available\x00Protocol not supported\x00Not supported\x00Address family not supported by protocol\x00Address not available\x00Network is down\x00Network unreachable\x00Connection reset by network\x00Connection aborted\x00No buffer space available\x00Socket is connected\x00Socket not connected\x00Operation already in progress\x00Operation in progress\x00Stale file handle\x00Quota exceeded\x00Multihop attempted\x00Capabilities insufficient\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00u\x02N\x00\xd6\x01\xe2\x04\xb9\x04\x18\x01\x8e\x05\xed\x02\x16\x04\xf2\x00\x97\x03\x01\x038\x05\xaf\x01\x82\x01O\x03/\x04\x1e\x00\xd4\x05\xa2\x00\x12\x03\x1e\x03\xc2\x01\xde\x03\x08\x00\xac\x05\x00\x01d\x02\xf1\x01e\x054\x02\x8c\x02\xcf\x02-\x03L\x04\xe3\x05\x9f\x02\xf8\x04\x1c\x05\x08\x05\xb1\x02K\x05\x15\x02x\x00R\x02<\x03\xf1\x03\xe4\x00\xc3\x03}\x04\xcc\x00\xaa\x03y\x05$\x02n\x01m\x03\"\x04\xab\x04D\x00\xfb\x01\xae\x00\x83\x03`\x00\xe5\x01\x07\x04\x94\x04^\x04+\x00X\x019\x01\x92\x00\xc2\x05\x9b\x01C\x02F\x01\xf6\x05-+   0X0x\x00-0X+0X 0X-0x+0x 0x\x00%s\x00nan\x00inf\x00NAN\x00INF\x00.\x00(null)\x00Incorrect flag!\x00Correct flag!\x00Enter flag: \x00Support for formatting long double values is currently disabled.\nTo enable it, add -lc-printscan-long-double to the link command.\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x19\x00\x0b\x00\x19\x19\x19\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x19\x00\n\n\x19\x19\x19\x03\n\x07\x00\x01\x1b\t\x0b\x18\x00\x00\t\x06\x0b\x00\x00\x0b\x00\x06\x19\x00\x00\x00\x19\x19\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x19\x00\x0b\r\x19\x19\x19\x00\r\x00\x00\x02\x00\t\x0e\x00\x00\x00\t\x00\x0e\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x13\x00\x00\x00\x00\t\x0c\x00\x00\x00\x00\x00\x0c\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x04\x0f\x00\x00\x00\x00\t\x10\x00\x00\x00\x00\x00\x10\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x11\x00\x00\x00\x00\t\x12\x00\x00\x00\x00\x00\x12\x00\x00\x12\x00\x00\x1a\x00\x00\x00\x1a\x1a\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00\x1a\x1a\x1a\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00\x00\x17\x00\x00\x00\x00\t\x14\x00\x00\x00\x00\x00\x14\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x00\x00\x15\x00\x00\x00\x00\t\x16\x00\x00\x00\x00\x00\x16\x00\x00\x16\x00\x000123456789ABCDEF\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\xff\xff\xff\xff\xff\xff\xff\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !\"#\xff\xff\xff\xff\xff\xff\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !\"#\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x01\x02\x04\x07\x03\x06\x05\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00d\x00\x00\x00\xe8\x03\x00\x00\x10\'\x00\x00\xa0\x86\x01\x00@B\x0f\x00\x80\x96\x98\x00\x00\xe1\xf5\x05\x02\x00\x00\xc0\x03\x00\x00\xc0\x04\x00\x00\xc0\x05\x00\x00\xc0\x06\x00\x00\xc0\x07\x00\x00\xc0\x08\x00\x00\xc0\t\x00\x00\xc0\n\x00\x00\xc0\x0b\x00\x00\xc0\x0c\x00\x00\xc0\r\x00\x00\xc0\x0e\x00\x00\xc0\x0f\x00\x00\xc0\x10\x00\x00\xc0\x11\x00\x00\xc0\x12\x00\x00\xc0\x13\x00\x00\xc0\x14\x00\x00\xc0\x15\x00\x00\xc0\x16\x00\x00\xc0\x17\x00\x00\xc0\x18\x00\x00\xc0\x19\x00\x00\xc0\x1a\x00\x00\xc0\x1b\x00\x00\xc0\x1c\x00\x00\xc0\x1d\x00\x00\xc0\x1e\x00\x00\xc0\x1f\x00\x00\xc0\x00\x00\x00\xb3\x01\x00\x00\xc3\x02\x00\x00\xc3\x03\x00\x00\xc3\x04\x00\x00\xc3\x05\x00\x00\xc3\x06\x00\x00\xc3\x07\x00\x00\xc3\x08\x00\x00\xc3\t\x00\x00\xc3\n\x00\x00\xc3\x0b\x00\x00\xc3\x0c\x00\x00\xc3\r\x00\x00\xd3\x0e\x00\x00\xc3\x0f\x00\x00\xc3\x00\x00\x0c\xbb\x01\x00\x0c\xc3\x02\x00\x0c\xc3\x03\x00\x0c\xc3\x04\x00\x0c\xdb")
	rt.store.string(MEMORY_LIST[0], 3984,"\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x88\x13\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\x0f\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\xb0\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\xb8\x17\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00J\x04in\xd1;\xabw\x8c6\xb3\xa1\x1b>a(\'\xd0\xdf\'\x04\xa9\x80[\xc0s\x12\xac\xe0\x93\xd0}_w XCG,\xed\x18b\x8d\xc1\x00\xfal\xd8\xd4i\x07(\x12\x1a\xa2^\x8d0B2l$\r\xf4\\\xe8:j\xc6Z\x1b)\x90|@\xbdh\xf2\x1e\xdfzyy\x1bU\x98\xf7\xa9Zs\x05\xce\xef\xb6\xe5\x91u|\xa0C/\xb9e\xf5\xbd\x07\x91MM\xc3=\x8e$\x1b\x18\xc0\xbf53\xb4\xeb\xc4\xd8\xad\x8b\xcci\xd5")
end
local FILE_BUFFER = {}
local FILE_HANDLER = {}
local stdin_buffer = ""
local table_insert = table.insert
local table_concat = table.concat
local table_clear = table.clear or function(t) for k in pairs(t) do t[k] = nil end end
local string_gmatch = string.gmatch
local string_sub = string.sub
local function file_initialize(handler)
    table_insert(FILE_BUFFER, {})
    table_insert(FILE_HANDLER, handler)
end
local function file_flush(file)
    local result = table_concat(FILE_BUFFER[file])
    table_clear(FILE_BUFFER[file])
    if result == "" then
        return
    end
    local lines = {}
    local current_line = ""
    for i = 1, #result do
        local char = string_sub(result, i, i)
        if char == '\n' then
            table_insert(lines, current_line)
            current_line = ""
        else
            current_line = current_line .. char
        end
    end
    for _, line in ipairs(lines) do
        FILE_HANDLER[file](line)
    end
    if current_line ~= "" then
        FILE_HANDLER[file](current_line)
    end
end
local function fd_close(fd)
    return 0
end
local function fd_fdstat_get(fd, fdstat_ptr)
    if fd >= 0 and fd <= 2 then
        rt.store.i32_n8(memory_at_0, fdstat_ptr, 2)
        rt.store.i32_n16(memory_at_0, fdstat_ptr + 2, 0)
        if fd == 0 then
            rt.store.i64(memory_at_0, fdstat_ptr + 8, 0x2)
            rt.store.i64(memory_at_0, fdstat_ptr + 16, 0x2)
        else
            rt.store.i64(memory_at_0, fdstat_ptr + 8, 0x40)
            rt.store.i64(memory_at_0, fdstat_ptr + 16, 0x40)
        end
        return 0
    end
    return 8
end
local function fd_read(fd, iovs, iovs_len, nread_ptr)
    if fd ~= 0 then
        return 8
    end
    if stdin_buffer == "" then
        io.flush()
        io.stderr:flush()
        
        stdin_buffer = io.read("*line") or ""
        if stdin_buffer then
            stdin_buffer = stdin_buffer .. "\n"
        else
            stdin_buffer = ""
        end
    end
    local total_read = 0
    local buffer_pos = 1
    for i = 0, iovs_len - 1 do
        local iov_ptr = iovs + (i * 8)
        local buf_ptr = rt.load.i32(memory_at_0, iov_ptr)
        local buf_len = rt.load.i32(memory_at_0, iov_ptr + 4)
        local to_copy = math.min(buf_len, #stdin_buffer - buffer_pos + 1)
        if to_copy > 0 then
            local data = string_sub(stdin_buffer, buffer_pos, buffer_pos + to_copy - 1)
            rt.store.string(memory_at_0, buf_ptr, data, to_copy)
            total_read = total_read + to_copy
            buffer_pos = buffer_pos + to_copy
        end
        if buffer_pos > #stdin_buffer then
            break
        end
    end
    if buffer_pos > #stdin_buffer then
        stdin_buffer = ""
    else
        stdin_buffer = string_sub(stdin_buffer, buffer_pos)
    end
    rt.store.i32(memory_at_0, nread_ptr, total_read)
    return 0
end
local function fd_seek(fd, offset, whence, newoffset_ptr)
    return 29
end
local function fd_write(fd, iovs, iovs_len, nwritten_ptr)
    if fd == 0 then
        return 8
    end
    local file = fd
    local buffer = FILE_BUFFER[file]
    if not buffer then 
        return 8
    end
    local total = 0
    for i = 0, iovs_len - 1 do
        local iov_ptr = iovs + (i * 8)
        local buf_ptr = rt.load.i32(memory_at_0, iov_ptr)
        local buf_len = rt.load.i32(memory_at_0, iov_ptr + 4)
        local data = rt.load.string(memory_at_0, buf_ptr, buf_len)
        table_insert(buffer, data)
        total = total + buf_len
    end
    rt.store.i32(memory_at_0, nwritten_ptr, total)
    file_flush(file)
    return 0
end
file_initialize(function(data) io.write(data); io.flush() end)
file_initialize(function(data) io.stderr:write(data); io.stderr:flush() end)
FUNC_LIST[0] = fd_close
FUNC_LIST[1] = fd_fdstat_get
FUNC_LIST[2] = fd_read
FUNC_LIST[3] = fd_seek
FUNC_LIST[4] = fd_write
FUNC_LIST[5] = os.exit
run_init_code()
memory_at_0 = MEMORY_LIST[0]
FUNC_LIST[7]()
