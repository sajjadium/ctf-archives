; ModuleID = '/Users/dusk/Documents/OOCTF/rev_3/src/main.deus'
source_filename = "/Users/dusk/Documents/OOCTF/rev_3/src/main.deus"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-n32:64-S128-Fn32"
target triple = "arm64-apple-darwin25.6.0"

%Result = type { i32, [5 x i64] }
%deus.unit = type {}
%deus.fat = type { ptr, i64 }
%Range = type { i64, i64 }
%deus.vec = type { ptr, i64, i64 }
%IoError = type { %deus.vec, %ErrorKind, %Option }
%ErrorKind = type { i32, [0 x i8] }
%Option = type { i32, [1 x i32] }
%Result.0 = type { i32, [5 x i64] }
%Stdin = type {}
%Option.1 = type { i32, [1 x i8] }
%Option.3 = type { ptr }
%Result.2 = type { i32, [5 x i64] }
%Option.4 = type { i32, [1 x i32] }
%Result.5 = type { i32, [2 x i64] }
%Utf8Error = type { i64 }
%Result.6 = type { i32, [0 x i8] }

@str = private unnamed_addr constant [16 x i8] c"Enter the flag: "
@panic = private unnamed_addr constant [19 x i8] c"index out of bounds"
@path = private unnamed_addr constant [47 x i8] c"/Users/dusk/Documents/OOCTF/rev_3/src/main.deus"
@loc = private constant { ptr, i64, i32, i32 } { ptr @path, i64 47, i32 17, i32 25 }
@loc.1 = private constant { ptr, i64, i32, i32 } { ptr @path, i64 47, i32 17, i32 40 }
@str.2 = private unnamed_addr constant [16 x i8] c"Wow you made it!"
@str.3 = private unnamed_addr constant [1 x i8] c"\0A"
@str.4 = private unnamed_addr constant [15 x i8] c"Wrong answer :/"
@path.6 = private unnamed_addr constant [46 x i8] c"/Users/dusk/Documents/OOCTF/rev_3/src/lib.deus"
@loc.7 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 34, i32 47 }
@loc.8 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 37, i32 37 }
@path.9 = private unnamed_addr constant [64 x i8] c"/Users/dusk/Documents/project_deus/proto/library/std/src/io.deus"
@loc.10 = private constant { ptr, i64, i32, i32 } { ptr @path.9, i64 64, i32 239, i32 19 }
@str.11 = private unnamed_addr constant [12 x i8] c"end of input"
@loc.12 = private constant { ptr, i64, i32, i32 } { ptr @path.9, i64 64, i32 240, i32 27 }
@panic.13 = private unnamed_addr constant [28 x i8] c"attempt to add with overflow"
@path.14 = private unnamed_addr constant [67 x i8] c"/Users/dusk/Documents/project_deus/proto/library/core/src/iter.deus"
@loc.15 = private constant { ptr, i64, i32, i32 } { ptr @path.14, i64 67, i32 228, i32 15 }
@str.16 = private unnamed_addr constant [42 x i8] c"called `Option.unwrap()` on a `None` value"
@path.17 = private unnamed_addr constant [69 x i8] c"/Users/dusk/Documents/project_deus/proto/library/core/src/option.deus"
@loc.18 = private constant { ptr, i64, i32, i32 } { ptr @path.17, i64 69, i32 25, i32 18 }
@panic.19 = private unnamed_addr constant [25 x i8] c"attempt to divide by zero"
@loc.20 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 19, i32 25 }
@loc.21 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 19, i32 30 }
@loc.22 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 19, i32 48 }
@panic.23 = private unnamed_addr constant [30 x i8] c"attempt to shift with overflow"
@loc.24 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 20, i32 22 }
@loc.25 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 21, i32 31 }
@loc.26 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 6, i32 16 }
@panic.27 = private unnamed_addr constant [33 x i8] c"attempt to subtract with overflow"
@loc.28 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 6, i32 34 }
@loc.29 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 6, i32 27 }
@path.30 = private unnamed_addr constant [68 x i8] c"/Users/dusk/Documents/project_deus/proto/library/core/src/slice.deus"
@loc.31 = private constant { ptr, i64, i32, i32 } { ptr @path.30, i64 68, i32 141, i32 92 }
@loc.32 = private constant { ptr, i64, i32, i32 } { ptr @path.30, i64 68, i32 141, i32 80 }
@panic.33 = private unnamed_addr constant [19 x i8] c"range out of bounds"
@path.34 = private unnamed_addr constant [70 x i8] c"/Users/dusk/Documents/project_deus/proto/library/alloc/src/string.deus"
@loc.35 = private constant { ptr, i64, i32, i32 } { ptr @path.34, i64 70, i32 121, i32 56 }
@loc.36 = private constant { ptr, i64, i32, i32 } { ptr @path.34, i64 70, i32 121, i32 67 }
@loc.37 = private constant { ptr, i64, i32, i32 } { ptr @path.34, i64 70, i32 124, i32 37 }
@loc.38 = private constant { ptr, i64, i32, i32 } { ptr @path.34, i64 70, i32 125, i32 81 }
@loc.39 = private constant { ptr, i64, i32, i32 } { ptr @path.34, i64 70, i32 125, i32 52 }
@loc.40 = private constant { ptr, i64, i32, i32 } { ptr @path.34, i64 70, i32 126, i32 33 }
@loc.41 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 12, i32 16 }
@loc.42 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 12, i32 34 }
@loc.43 = private constant { ptr, i64, i32, i32 } { ptr @path.6, i64 46, i32 12, i32 27 }
@path.44 = private unnamed_addr constant [66 x i8] c"/Users/dusk/Documents/project_deus/proto/library/core/src/str.deus"
@loc.45 = private constant { ptr, i64, i32, i32 } { ptr @path.44, i64 66, i32 284, i32 22 }
@loc.46 = private constant { ptr, i64, i32, i32 } { ptr @path.44, i64 66, i32 290, i32 24 }
@loc.47 = private constant { ptr, i64, i32, i32 } { ptr @path.44, i64 66, i32 292, i32 24 }
@loc.48 = private constant { ptr, i64, i32, i32 } { ptr @path.44, i64 66, i32 292, i32 21 }
@loc.49 = private constant { ptr, i64, i32, i32 } { ptr @path.44, i64 66, i32 294, i32 37 }
@loc.50 = private constant { ptr, i64, i32, i32 } { ptr @path.44, i64 66, i32 294, i32 34 }
@loc.51 = private constant { ptr, i64, i32, i32 } { ptr @path.44, i64 66, i32 298, i32 11 }
@str.52 = private unnamed_addr constant [44 x i8] c"called `Result.unwrap()` on an `Err` value: "
@path.53 = private unnamed_addr constant [69 x i8] c"/Users/dusk/Documents/project_deus/proto/library/core/src/result.deus"
@loc.54 = private constant { ptr, i64, i32, i32 } { ptr @path.53, i64 69, i32 35, i32 20 }
@loc.55 = private constant { ptr, i64, i32, i32 } { ptr @path.9, i64 64, i32 53, i32 50 }
@str.56 = private unnamed_addr constant [9 x i8] c"Utf8Error"
@str.57 = private unnamed_addr constant [3 x i8] c" { "
@str.58 = private unnamed_addr constant [13 x i8] c"valid_up_to: "
@str.59 = private unnamed_addr constant [2 x i8] c" }"
@str.60 = private unnamed_addr constant [7 x i8] c"error: "
@str.61 = private unnamed_addr constant [8 x i8] c"IoError("
@str.62 = private unnamed_addr constant [2 x i8] c", "
@str.63 = private unnamed_addr constant [1 x i8] c")"
@str.64 = private unnamed_addr constant [5 x i8] c"Other"
@str.65 = private unnamed_addr constant [8 x i8] c"NotFound"
@str.66 = private unnamed_addr constant [16 x i8] c"PermissionDenied"
@str.67 = private unnamed_addr constant [17 x i8] c"ConnectionRefused"
@str.68 = private unnamed_addr constant [15 x i8] c"ConnectionReset"
@str.69 = private unnamed_addr constant [17 x i8] c"ConnectionAborted"
@str.70 = private unnamed_addr constant [12 x i8] c"NotConnected"
@str.71 = private unnamed_addr constant [9 x i8] c"AddrInUse"
@str.72 = private unnamed_addr constant [16 x i8] c"AddrNotAvailable"
@str.73 = private unnamed_addr constant [10 x i8] c"BrokenPipe"
@str.74 = private unnamed_addr constant [13 x i8] c"AlreadyExists"
@str.75 = private unnamed_addr constant [10 x i8] c"WouldBlock"
@str.76 = private unnamed_addr constant [12 x i8] c"InvalidInput"
@str.77 = private unnamed_addr constant [8 x i8] c"TimedOut"
@str.78 = private unnamed_addr constant [11 x i8] c"Interrupted"
@str.79 = private unnamed_addr constant [13 x i8] c"NotADirectory"
@str.80 = private unnamed_addr constant [12 x i8] c"IsADirectory"
@str.81 = private unnamed_addr constant [17 x i8] c"DirectoryNotEmpty"
@str.82 = private unnamed_addr constant [11 x i8] c"StorageFull"
@str.83 = private unnamed_addr constant [18 x i8] c"ReadOnlyFilesystem"
@str.84 = private unnamed_addr constant [11 x i8] c"OutOfMemory"
@str.85 = private unnamed_addr constant [11 x i8] c"InvalidData"
@str.86 = private unnamed_addr constant [13 x i8] c"UnexpectedEof"
@str.87 = private unnamed_addr constant [9 x i8] c"WriteZero"
@str.88 = private unnamed_addr constant [11 x i8] c"Unsupported"

define internal %Result @deus.main() #0 {
entry:
  %variant12 = alloca %Result, align 8
  %b11 = alloca i8, align 1
  %a10 = alloca i8, align 1
  %b7 = alloca i64, align 8
  %a6 = alloca i64, align 8
  %b5 = alloca i64, align 8
  %a4 = alloca i64, align 8
  %b2 = alloca i64, align 8
  %a1 = alloca i64, align 8
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %variant = alloca %Result, align 8
  %"%t35" = alloca %deus.unit, align 8
  %"%t34" = alloca i1, align 1
  %"%t33" = alloca i64, align 8
  %"%t32" = alloca i64, align 8
  %"%t31" = alloca i1, align 1
  %"%t30" = alloca i64, align 8
  %"%t29" = alloca i64, align 8
  %"%t28" = alloca i1, align 1
  %"%t27" = alloca %deus.unit, align 8
  %i = alloca i64, align 8
  %"%t25" = alloca i1, align 1
  %"%t24" = alloca i64, align 8
  %"%t23" = alloca i64, align 8
  %"%t22" = alloca i64, align 8
  %"%t21" = alloca ptr, align 8
  %"%t20" = alloca %deus.fat, align 8
  %"%t19" = alloca i64, align 8
  %"%t18" = alloca %Range, align 8
  %"%t17" = alloca %deus.unit, align 8
  %"%t16" = alloca ptr, align 8
  %"%t15" = alloca %deus.fat, align 8
  %"%t14" = alloca i64, align 8
  %"%t13" = alloca ptr, align 8
  %"%t12" = alloca %deus.fat, align 8
  %"%t11" = alloca i64, align 8
  %ok = alloca i1, align 1
  %encrypted = alloca %deus.vec, align 8
  %"%err1" = alloca %IoError, align 8
  %"%t7" = alloca i32, align 4
  %"%v0" = alloca %deus.vec, align 8
  %"%t5" = alloca i32, align 4
  %"%t4" = alloca %Result.0, align 8
  %input = alloca %deus.vec, align 8
  %"%t2" = alloca %deus.unit, align 8
  %expected = alloca [41 x i8], align 1
  %_0 = alloca %Result, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  store [41 x i8] c"q\11\B5\F23\FD\02x\D8r\A2\D1f\FD\86\85\C6\D9x\EAjPO\91\DD\EB\B8^!\A2d&\CD\19\B6\07\C9'\BBk\8B", ptr %expected, align 1
  call void @deus_write(i32 1, ptr @str, i64 16)
  br label %bb2

bb1:                                              ; preds = %bb28, %bb8
  %0 = load %Result, ptr %_0, align 8
  ret %Result %0

bb2:                                              ; preds = %bb0
  %1 = call %Result.0 @deus.read_line()
  store %Result.0 %1, ptr %"%t4", align 8
  br label %bb3

bb3:                                              ; preds = %bb2
  %2 = load %Result.0, ptr %"%t4", align 8
  %3 = extractvalue %Result.0 %2, 0
  store i32 %3, ptr %"%t5", align 4
  %4 = load i32, ptr %"%t5", align 4
  switch i32 %4, label %bb5 [
    i32 0, label %bb6
  ]

bb4:                                              ; preds = %bb9, %bb6
  %5 = load %deus.vec, ptr %input, align 8
  %6 = call %deus.vec @deus.algorithm(%deus.vec %5)
  store %deus.vec %6, ptr %encrypted, align 8
  br label %bb10

bb5:                                              ; preds = %bb3
  %7 = load %Result.0, ptr %"%t4", align 8
  %8 = extractvalue %Result.0 %7, 0
  store i32 %8, ptr %"%t7", align 4
  %9 = load i32, ptr %"%t7", align 4
  switch i32 %9, label %bb7 [
    i32 1, label %bb8
  ]

bb6:                                              ; preds = %bb3
  %10 = getelementptr inbounds nuw %Result.0, ptr %"%t4", i32 0, i32 1
  %11 = getelementptr inbounds nuw { %deus.vec }, ptr %10, i32 0, i32 0
  %12 = load %deus.vec, ptr %11, align 8
  store %deus.vec %12, ptr %"%v0", align 8
  %13 = load %deus.vec, ptr %"%v0", align 8
  store %deus.vec %13, ptr %input, align 8
  br label %bb4

bb7:                                              ; preds = %bb5
  unreachable

bb8:                                              ; preds = %bb5
  %14 = getelementptr inbounds nuw %Result.0, ptr %"%t4", i32 0, i32 1
  %15 = getelementptr inbounds nuw { %IoError }, ptr %14, i32 0, i32 0
  %16 = load %IoError, ptr %15, align 8
  store %IoError %16, ptr %"%err1", align 8
  %17 = load %IoError, ptr %"%err1", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant, i8 0, i64 48, i1 false)
  %18 = getelementptr inbounds nuw %Result, ptr %variant, i32 0, i32 0
  store i32 1, ptr %18, align 4
  %19 = getelementptr inbounds nuw %Result, ptr %variant, i32 0, i32 1
  %20 = getelementptr inbounds nuw { %IoError }, ptr %19, i32 0, i32 0
  store %IoError %17, ptr %20, align 8
  %21 = load %Result, ptr %variant, align 8
  store %Result %21, ptr %_0, align 8
  br label %bb1

bb9:                                              ; No predecessors!
  br label %bb4

bb10:                                             ; preds = %bb4
  store ptr %encrypted, ptr %"%t13", align 8
  %22 = load ptr, ptr %"%t13", align 8
  %23 = load %deus.vec, ptr %22, align 8
  %24 = extractvalue %deus.vec %23, 0
  %25 = icmp eq ptr %24, null
  %buf = select i1 %25, ptr inttoptr (i64 1 to ptr), ptr %24
  %26 = extractvalue %deus.vec %23, 1
  %27 = insertvalue %deus.fat undef, ptr %buf, 0
  %28 = insertvalue %deus.fat %27, i64 %26, 1
  store %deus.fat %28, ptr %"%t12", align 8
  %29 = load %deus.fat, ptr %"%t12", align 8
  %30 = extractvalue %deus.fat %29, 0
  %31 = extractvalue %deus.fat %29, 1
  store i64 %31, ptr %"%t11", align 8
  br label %bb11

bb11:                                             ; preds = %bb10
  store ptr %expected, ptr %"%t16", align 8
  %32 = load ptr, ptr %"%t16", align 8
  %33 = insertvalue %deus.fat undef, ptr %32, 0
  %34 = insertvalue %deus.fat %33, i64 41, 1
  store %deus.fat %34, ptr %"%t15", align 8
  %35 = load %deus.fat, ptr %"%t15", align 8
  %36 = extractvalue %deus.fat %35, 0
  %37 = extractvalue %deus.fat %35, 1
  store i64 %37, ptr %"%t14", align 8
  br label %bb12

bb12:                                             ; preds = %bb11
  %38 = load i64, ptr %"%t11", align 8
  %39 = load i64, ptr %"%t14", align 8
  store i64 %38, ptr %a, align 8
  store i64 %39, ptr %b, align 8
  %40 = call i32 @cmp.usize(ptr %a, ptr %b)
  %41 = icmp eq i32 %40, 0
  store i1 %41, ptr %ok, align 1
  %42 = load i1, ptr %ok, align 1
  %43 = zext i1 %42 to i32
  switch i32 %43, label %bb14 [
    i32 1, label %bb13
  ]

bb13:                                             ; preds = %bb12
  store ptr %expected, ptr %"%t21", align 8
  %44 = load ptr, ptr %"%t21", align 8
  %45 = insertvalue %deus.fat undef, ptr %44, 0
  %46 = insertvalue %deus.fat %45, i64 41, 1
  store %deus.fat %46, ptr %"%t20", align 8
  %47 = load %deus.fat, ptr %"%t20", align 8
  %48 = extractvalue %deus.fat %47, 0
  %49 = extractvalue %deus.fat %47, 1
  store i64 %49, ptr %"%t19", align 8
  br label %bb20

bb14:                                             ; preds = %bb12
  br label %bb15

bb15:                                             ; preds = %bb19, %bb14
  %50 = load i1, ptr %ok, align 1
  %51 = zext i1 %50 to i32
  switch i32 %51, label %bb27 [
    i32 1, label %bb26
  ]

bb16:                                             ; preds = %bb20, %bb18
  %52 = load i64, ptr %"%t22", align 8
  %53 = load i64, ptr %"%t23", align 8
  store i64 %52, ptr %a1, align 8
  store i64 %53, ptr %b2, align 8
  %54 = call i32 @cmp.usize(ptr %a1, ptr %b2)
  %55 = icmp slt i32 %54, 0
  store i1 %55, ptr %"%t25", align 1
  %56 = load i1, ptr %"%t25", align 1
  %57 = zext i1 %56 to i32
  switch i32 %57, label %bb19 [
    i32 1, label %bb17
  ]

bb17:                                             ; preds = %bb16
  %58 = load i64, ptr %"%t22", align 8
  store i64 %58, ptr %i, align 8
  %59 = load %deus.vec, ptr %encrypted, align 8
  %60 = extractvalue %deus.vec %59, 0
  %61 = icmp eq ptr %60, null
  %buf3 = select i1 %61, ptr inttoptr (i64 1 to ptr), ptr %60
  %62 = extractvalue %deus.vec %59, 1
  store i64 %62, ptr %"%t29", align 8
  %63 = load i64, ptr %i, align 8
  store i64 %63, ptr %"%t30", align 8
  %64 = load i64, ptr %"%t30", align 8
  %65 = load i64, ptr %"%t29", align 8
  store i64 %64, ptr %a4, align 8
  store i64 %65, ptr %b5, align 8
  %66 = call i32 @cmp.usize(ptr %a4, ptr %b5)
  %67 = icmp slt i32 %66, 0
  store i1 %67, ptr %"%t31", align 1
  %68 = load i1, ptr %"%t31", align 1
  br i1 %68, label %bb24, label %assert.fail

bb18:                                             ; preds = %bb23
  %69 = load i64, ptr %"%t22", align 8
  %70 = load i64, ptr %"%t24", align 8
  %71 = add i64 %69, %70
  store i64 %71, ptr %"%t22", align 8
  br label %bb16

bb19:                                             ; preds = %bb16
  br label %bb15

bb20:                                             ; preds = %bb13
  %72 = load i64, ptr %"%t19", align 8
  %73 = insertvalue %Range { i64 0, i64 undef }, i64 %72, 1
  store %Range %73, ptr %"%t18", align 8
  %74 = getelementptr inbounds nuw %Range, ptr %"%t18", i32 0, i32 0
  %75 = load i64, ptr %74, align 8
  store i64 %75, ptr %"%t22", align 8
  %76 = getelementptr inbounds nuw %Range, ptr %"%t18", i32 0, i32 1
  %77 = load i64, ptr %76, align 8
  store i64 %77, ptr %"%t23", align 8
  store i64 1, ptr %"%t24", align 8
  br label %bb16

bb21:                                             ; preds = %bb25
  store i1 false, ptr %ok, align 1
  br label %bb23

bb22:                                             ; preds = %bb25
  br label %bb23

bb23:                                             ; preds = %bb22, %bb21
  br label %bb18

bb24:                                             ; preds = %bb17
  store i64 41, ptr %"%t32", align 8
  %78 = load i64, ptr %i, align 8
  store i64 %78, ptr %"%t33", align 8
  %79 = load i64, ptr %"%t33", align 8
  %80 = load i64, ptr %"%t32", align 8
  store i64 %79, ptr %a6, align 8
  store i64 %80, ptr %b7, align 8
  %81 = call i32 @cmp.usize(ptr %a6, ptr %b7)
  %82 = icmp slt i32 %81, 0
  store i1 %82, ptr %"%t34", align 1
  %83 = load i1, ptr %"%t34", align 1
  br i1 %83, label %bb25, label %assert.fail8

bb25:                                             ; preds = %bb24
  %84 = load i64, ptr %"%t30", align 8
  %85 = load %deus.vec, ptr %encrypted, align 8
  %86 = extractvalue %deus.vec %85, 0
  %87 = getelementptr inbounds i8, ptr %86, i64 %84
  %88 = load i8, ptr %87, align 1
  %89 = load i64, ptr %"%t33", align 8
  %90 = getelementptr inbounds [41 x i8], ptr %expected, i64 0, i64 %89
  %91 = load i8, ptr %90, align 1
  store i8 %88, ptr %a10, align 1
  store i8 %91, ptr %b11, align 1
  %92 = call i32 @cmp.u8(ptr %a10, ptr %b11)
  %93 = icmp eq i32 %92, 0
  %94 = xor i1 %93, true
  store i1 %94, ptr %"%t28", align 1
  %95 = load i1, ptr %"%t28", align 1
  %96 = zext i1 %95 to i32
  switch i32 %96, label %bb22 [
    i32 1, label %bb21
  ]

bb26:                                             ; preds = %bb15
  call void @deus_write(i32 1, ptr @str.2, i64 16)
  call void @deus_write(i32 1, ptr @str.3, i64 1)
  br label %bb29

bb27:                                             ; preds = %bb15
  call void @deus_write(i32 1, ptr @str.4, i64 15)
  call void @deus_write(i32 1, ptr @str.3, i64 1)
  br label %bb30

bb28:                                             ; preds = %bb30, %bb29
  call void @llvm.memset.p0.i64(ptr align 8 %variant12, i8 0, i64 48, i1 false)
  %97 = getelementptr inbounds nuw %Result, ptr %variant12, i32 0, i32 0
  store i32 0, ptr %97, align 4
  %98 = getelementptr inbounds nuw %Result, ptr %variant12, i32 0, i32 1
  %99 = getelementptr inbounds nuw { %deus.unit }, ptr %98, i32 0, i32 0
  store %deus.unit undef, ptr %99, align 1
  %100 = load %Result, ptr %variant12, align 8
  store %Result %100, ptr %_0, align 8
  call void @"drop.Vec[u8]"(ptr %encrypted)
  br label %bb1

bb29:                                             ; preds = %bb26
  br label %bb28

bb30:                                             ; preds = %bb27
  br label %bb28

assert.fail:                                      ; preds = %bb17
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc) #2
  unreachable

dead:                                             ; No predecessors!
  unreachable

assert.fail8:                                     ; preds = %bb24
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.1) #2
  unreachable

dead9:                                            ; No predecessors!
  unreachable
}

declare void @deus_write(i32, ptr, i64)

define internal %Result.0 @deus.read_line() #0 {
entry:
  %"%t3" = alloca ptr, align 8
  %"%t2" = alloca %Stdin, align 8
  %"%t1" = alloca ptr, align 8
  %_0 = alloca %Result.0, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %0 = call %Stdin @deus.stdin()
  br label %bb2

bb1:                                              ; preds = %bb3
  %1 = load %Result.0, ptr %_0, align 8
  ret %Result.0 %1

bb2:                                              ; preds = %bb0
  store ptr %"%t2", ptr %"%t1", align 8
  %2 = load ptr, ptr %"%t1", align 8
  store ptr %2, ptr %"%t3", align 8
  %3 = load ptr, ptr %"%t3", align 8
  %4 = call %Result.0 @deus.read_line.5(ptr %3)
  store %Result.0 %4, ptr %_0, align 8
  br label %bb3

bb3:                                              ; preds = %bb2
  br label %bb1
}

define internal %deus.vec @deus.algorithm(%deus.vec %0) #0 {
entry:
  %b4 = alloca i64, align 8
  %a3 = alloca i64, align 8
  %x = alloca i8, align 1
  %iter = alloca { i32, i32, i64, ptr, ptr, i64, i64, i64, i64, i32, i32, ptr, ptr, i32, ptr, i32 }, align 8
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %v = alloca %deus.vec, align 8
  %"%t30" = alloca %deus.unit, align 8
  %"%t29" = alloca i1, align 1
  %"%t28" = alloca i64, align 8
  %"%t27" = alloca i64, align 8
  %"%t26" = alloca i8, align 1
  %"%t25" = alloca i8, align 1
  %"%t24" = alloca i8, align 1
  %"%t23" = alloca %deus.unit, align 8
  %"%t22" = alloca ptr, align 8
  %"%t21" = alloca ptr, align 8
  %"%t20" = alloca ptr, align 8
  %"%t19" = alloca %deus.fat, align 8
  %"%t18" = alloca ptr, align 8
  %"%t17" = alloca %Option.1, align 8
  %"%t16" = alloca i8, align 1
  %"%t15" = alloca i8, align 1
  %"%t14" = alloca %deus.unit, align 8
  %"%t13" = alloca %deus.unit, align 8
  %i = alloca i64, align 8
  %"%t11" = alloca i1, align 1
  %"%t10" = alloca i64, align 8
  %"%t9" = alloca i64, align 8
  %"%t8" = alloca i64, align 8
  %"%t7" = alloca ptr, align 8
  %"%t6" = alloca i64, align 8
  %"%t5" = alloca %Range, align 8
  %"%t4" = alloca %deus.unit, align 8
  %output = alloca %deus.vec, align 8
  %state = alloca i8, align 1
  %input = alloca %deus.vec, align 8
  %_0 = alloca %deus.vec, align 8
  %1 = freeze %deus.vec %0
  store %deus.vec %1, ptr %input, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  store i8 -89, ptr %state, align 1
  call void @deus_vec_init(ptr %v)
  %2 = load %deus.vec, ptr %v, align 8
  store %deus.vec %2, ptr %output, align 8
  br label %bb2

bb1:                                              ; preds = %bb15, %bb6
  call void @drop.String(ptr %input)
  %3 = load %deus.vec, ptr %_0, align 8
  ret %deus.vec %3

bb2:                                              ; preds = %bb0
  store ptr %input, ptr %"%t7", align 8
  %4 = load ptr, ptr %"%t7", align 8
  %5 = load %deus.vec, ptr %4, align 8
  %6 = extractvalue %deus.vec %5, 0
  %7 = icmp eq ptr %6, null
  %buf = select i1 %7, ptr inttoptr (i64 1 to ptr), ptr %6
  %8 = extractvalue %deus.vec %5, 1
  store i64 %8, ptr %"%t6", align 8
  br label %bb7

bb3:                                              ; preds = %bb7, %bb5
  %9 = load i64, ptr %"%t8", align 8
  %10 = load i64, ptr %"%t9", align 8
  store i64 %9, ptr %a, align 8
  store i64 %10, ptr %b, align 8
  %11 = call i32 @cmp.usize(ptr %a, ptr %b)
  %12 = icmp slt i32 %11, 0
  store i1 %12, ptr %"%t11", align 1
  %13 = load i1, ptr %"%t11", align 1
  %14 = zext i1 %13 to i32
  switch i32 %14, label %bb6 [
    i32 1, label %bb4
  ]

bb4:                                              ; preds = %bb3
  %15 = load i64, ptr %"%t8", align 8
  store i64 %15, ptr %i, align 8
  store ptr %input, ptr %"%t20", align 8
  %16 = load ptr, ptr %"%t20", align 8
  %17 = load %deus.vec, ptr %16, align 8
  %18 = extractvalue %deus.vec %17, 0
  %19 = icmp eq ptr %18, null
  %buf1 = select i1 %19, ptr inttoptr (i64 1 to ptr), ptr %18
  %20 = extractvalue %deus.vec %17, 1
  %21 = insertvalue %deus.fat undef, ptr %buf1, 0
  %22 = insertvalue %deus.fat %21, i64 %20, 1
  store %deus.fat %22, ptr %"%t19", align 8
  %23 = load %deus.fat, ptr %"%t19", align 8
  %24 = extractvalue %deus.fat %23, 0
  %25 = extractvalue %deus.fat %23, 1
  call void @deus_iter_init(ptr %iter, i32 12, i64 1)
  %26 = getelementptr inbounds nuw { i32, i32, i64, ptr, ptr, i64, i64, i64, i64, i32, i32, ptr, ptr, i32, ptr, i32 }, ptr %iter, i32 0, i32 4
  store ptr %24, ptr %26, align 8
  %27 = getelementptr inbounds nuw { i32, i32, i64, ptr, ptr, i64, i64, i64, i64, i32, i32, ptr, ptr, i32, ptr, i32 }, ptr %iter, i32 0, i32 6
  store i64 0, ptr %27, align 8
  %28 = getelementptr inbounds nuw { i32, i32, i64, ptr, ptr, i64, i64, i64, i64, i32, i32, ptr, ptr, i32, ptr, i32 }, ptr %iter, i32 0, i32 7
  store i64 %25, ptr %28, align 8
  store ptr %iter, ptr %"%t18", align 8
  br label %bb8

bb5:                                              ; preds = %bb14
  %29 = load i64, ptr %"%t8", align 8
  %30 = load i64, ptr %"%t10", align 8
  %31 = add i64 %29, %30
  store i64 %31, ptr %"%t8", align 8
  br label %bb3

bb6:                                              ; preds = %bb3
  %32 = load %deus.vec, ptr %output, align 8
  store %deus.vec %32, ptr %_0, align 8
  br label %bb1

bb7:                                              ; preds = %bb2
  %33 = load i64, ptr %"%t6", align 8
  %34 = insertvalue %Range { i64 0, i64 undef }, i64 %33, 1
  store %Range %34, ptr %"%t5", align 8
  %35 = getelementptr inbounds nuw %Range, ptr %"%t5", i32 0, i32 0
  %36 = load i64, ptr %35, align 8
  store i64 %36, ptr %"%t8", align 8
  %37 = getelementptr inbounds nuw %Range, ptr %"%t5", i32 0, i32 1
  %38 = load i64, ptr %37, align 8
  store i64 %38, ptr %"%t9", align 8
  store i64 1, ptr %"%t10", align 8
  br label %bb3

bb8:                                              ; preds = %bb4
  %39 = load ptr, ptr %"%t18", align 8
  %40 = load i64, ptr %i, align 8
  %41 = call %Option.1 @deus.nth.T_u8(ptr %39, i64 %40)
  store %Option.1 %41, ptr %"%t17", align 4
  br label %bb9

bb9:                                              ; preds = %bb8
  %42 = load %Option.1, ptr %"%t17", align 4
  %43 = call i8 @deus.unwrap.T_u8(%Option.1 %42, ptr @loc.7)
  store i8 %43, ptr %"%t16", align 1
  br label %bb10

bb10:                                             ; preds = %bb9
  %44 = load i8, ptr %"%t16", align 1
  %45 = load i64, ptr %i, align 8
  %46 = load i8, ptr %state, align 1
  %47 = call i8 @deus.transform(i8 %44, i64 %45, i8 %46)
  store i8 %47, ptr %"%t15", align 1
  br label %bb11

bb11:                                             ; preds = %bb10
  store ptr %output, ptr %"%t21", align 8
  %48 = load ptr, ptr %"%t21", align 8
  store ptr %48, ptr %"%t22", align 8
  %49 = load ptr, ptr %"%t22", align 8
  %50 = load i8, ptr %"%t15", align 1
  store i8 %50, ptr %x, align 1
  call void @deus_vec_push(ptr %49, ptr %x, i64 1)
  br label %bb12

bb12:                                             ; preds = %bb11
  %51 = load %deus.vec, ptr %output, align 8
  %52 = extractvalue %deus.vec %51, 0
  %53 = icmp eq ptr %52, null
  %buf2 = select i1 %53, ptr inttoptr (i64 1 to ptr), ptr %52
  %54 = extractvalue %deus.vec %51, 1
  store i64 %54, ptr %"%t27", align 8
  %55 = load i64, ptr %i, align 8
  store i64 %55, ptr %"%t28", align 8
  %56 = load i64, ptr %"%t28", align 8
  %57 = load i64, ptr %"%t27", align 8
  store i64 %56, ptr %a3, align 8
  store i64 %57, ptr %b4, align 8
  %58 = call i32 @cmp.usize(ptr %a3, ptr %b4)
  %59 = icmp slt i32 %58, 0
  store i1 %59, ptr %"%t29", align 1
  %60 = load i1, ptr %"%t29", align 1
  br i1 %60, label %bb13, label %assert.fail

bb13:                                             ; preds = %bb12
  %61 = load i8, ptr %state, align 1
  %62 = load i64, ptr %"%t28", align 8
  %63 = load %deus.vec, ptr %output, align 8
  %64 = extractvalue %deus.vec %63, 0
  %65 = getelementptr inbounds i8, ptr %64, i64 %62
  %66 = load i8, ptr %65, align 1
  %67 = xor i8 %61, %66
  store i8 %67, ptr %"%t26", align 1
  %68 = load i8, ptr %"%t26", align 1
  %69 = call i8 @deus.rol8(i8 %68, i32 3)
  store i8 %69, ptr %"%t25", align 1
  br label %bb14

bb14:                                             ; preds = %bb13
  %70 = load i8, ptr %"%t25", align 1
  %71 = add i8 %70, 41
  store i8 %71, ptr %"%t24", align 1
  %72 = load i8, ptr %"%t24", align 1
  store i8 %72, ptr %state, align 1
  br label %bb5

bb15:                                             ; No predecessors!
  br label %bb1

assert.fail:                                      ; preds = %bb12
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.8) #2
  unreachable

dead:                                             ; No predecessors!
  unreachable
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #1

define internal i32 @cmp.usize(ptr %0, ptr %1) #0 {
entry:
  %2 = load i64, ptr %0, align 8
  %3 = load i64, ptr %1, align 8
  %4 = icmp ult i64 %2, %3
  %5 = icmp ugt i64 %2, %3
  %6 = select i1 %5, i32 1, i32 0
  %7 = select i1 %4, i32 -1, i32 %6
  ret i32 %7
}

; Function Attrs: noreturn
declare void @deus_panic_at(ptr, i64, ptr) #2

define internal i32 @cmp.u8(ptr %0, ptr %1) #0 {
entry:
  %2 = load i8, ptr %0, align 1
  %3 = load i8, ptr %1, align 1
  %4 = icmp ult i8 %2, %3
  %5 = icmp ugt i8 %2, %3
  %6 = select i1 %5, i32 1, i32 0
  %7 = select i1 %4, i32 -1, i32 %6
  ret i32 %7
}

define internal void @"drop.Vec[u8]"(ptr %0) #0 {
entry:
  %1 = load %deus.vec, ptr %0, align 8
  %2 = extractvalue %deus.vec %1, 2
  %3 = icmp sgt i64 %2, 0
  br i1 %3, label %free, label %freed

free:                                             ; preds = %entry
  %4 = extractvalue %deus.vec %1, 0
  call void @deus_free(ptr %4)
  br label %freed

freed:                                            ; preds = %free, %entry
  ret void
}

define internal %Stdin @deus.stdin() #0 {
entry:
  %_0 = alloca %Stdin, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  br label %bb1

bb1:                                              ; preds = %bb0
  %0 = load %Stdin, ptr %_0, align 1
  ret %Stdin %0
}

define internal %Result.0 @deus.read_line.5(ptr %0) #0 {
entry:
  %variant17 = alloca %Result.0, align 8
  %b16 = alloca i8, align 1
  %a15 = alloca i8, align 1
  %variant13 = alloca %Option.1, align 8
  %variant12 = alloca %Option.1, align 8
  %p = alloca i8, align 1
  %x = alloca i8, align 1
  %b11 = alloca i8, align 1
  %a10 = alloca i8, align 1
  %b7 = alloca i64, align 8
  %a6 = alloca i64, align 8
  %variant5 = alloca %Result.0, align 8
  %variant4 = alloca %ErrorKind, align 8
  %b3 = alloca i64, align 8
  %a2 = alloca i64, align 8
  %variant = alloca %Result.0, align 8
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %v = alloca %deus.vec, align 8
  %"%t51" = alloca ptr, align 8
  %"%t50" = alloca %deus.fat, align 8
  %"%t49" = alloca %deus.vec, align 8
  %"%t48" = alloca ptr, align 8
  %"%t47" = alloca ptr, align 8
  %"%t46" = alloca %Option.1, align 8
  %"%t45" = alloca i1, align 1
  %"%t44" = alloca i32, align 4
  %"%t43" = alloca ptr, align 8
  %"%t42" = alloca %deus.fat, align 8
  %"%t41" = alloca %Option.3, align 8
  %"%t40" = alloca %deus.unit, align 8
  %"%t39" = alloca ptr, align 8
  %"%t38" = alloca ptr, align 8
  %"%t37" = alloca i8, align 1
  %"%t36" = alloca i1, align 1
  %"%t35" = alloca i64, align 8
  %"%t34" = alloca i64, align 8
  %"%t33" = alloca %deus.unit, align 8
  %"%t32" = alloca i1, align 1
  %"%t31" = alloca i64, align 8
  %"%t30" = alloca i64, align 8
  %"%t29" = alloca i1, align 1
  %"%t28" = alloca %deus.unit, align 8
  %"%t27" = alloca %deus.unit, align 8
  %"%t26" = alloca %ErrorKind, align 8
  %"%t25" = alloca %IoError, align 8
  %"%t24" = alloca %deus.unit, align 8
  %"%t23" = alloca ptr, align 8
  %"%t22" = alloca %deus.fat, align 8
  %"%t21" = alloca i1, align 1
  %"%t20" = alloca %deus.unit, align 8
  %"%t19" = alloca i1, align 1
  %"%t18" = alloca %deus.unit, align 8
  %"%err1" = alloca %IoError, align 8
  %"%t16" = alloca i32, align 4
  %"%v0" = alloca i64, align 8
  %"%t14" = alloca i32, align 4
  %"%t13" = alloca ptr, align 8
  %"%t12" = alloca ptr, align 8
  %"%t11" = alloca %deus.fat, align 8
  %"%t10" = alloca ptr, align 8
  %"%t9" = alloca ptr, align 8
  %"%t8" = alloca %deus.fat, align 8
  %"%t7" = alloca %Result.2, align 8
  %n = alloca i64, align 8
  %"%t5" = alloca %deus.unit, align 8
  %"%t4" = alloca %deus.unit, align 8
  %one = alloca [1 x i8], align 1
  %bytes = alloca %deus.vec, align 8
  %self = alloca ptr, align 8
  %_0 = alloca %Result.0, align 8
  store ptr %0, ptr %self, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  call void @deus_vec_init(ptr %v)
  %1 = load %deus.vec, ptr %v, align 8
  store %deus.vec %1, ptr %bytes, align 8
  br label %bb2

bb1:                                              ; preds = %bb39, %bb19, %bb10
  %2 = load %Result.0, ptr %_0, align 8
  ret %Result.0 %2

bb2:                                              ; preds = %bb0
  call void @llvm.memset.p0.i64(ptr align 1 %one, i8 0, i64 1, i1 false)
  br label %bb3

bb3:                                              ; preds = %bb28, %bb2
  store ptr %one, ptr %"%t9", align 8
  %3 = load ptr, ptr %"%t9", align 8
  store ptr %3, ptr %"%t10", align 8
  %4 = load ptr, ptr %"%t10", align 8
  %5 = insertvalue %deus.fat undef, ptr %4, 0
  %6 = insertvalue %deus.fat %5, i64 1, 1
  store %deus.fat %6, ptr %"%t8", align 8
  %7 = load %deus.fat, ptr %"%t8", align 8
  %8 = extractvalue %deus.fat %7, 0
  %9 = extractvalue %deus.fat %7, 1
  %10 = insertvalue %deus.fat undef, ptr %8, 0
  %11 = insertvalue %deus.fat %10, i64 %9, 1
  store %deus.fat %11, ptr %"%t11", align 8
  %12 = load ptr, ptr %self, align 8
  store ptr %12, ptr %"%t12", align 8
  %13 = load ptr, ptr %"%t12", align 8
  store ptr %13, ptr %"%t13", align 8
  %14 = load ptr, ptr %"%t13", align 8
  %15 = load %deus.fat, ptr %"%t11", align 8
  %16 = call %Result.2 @deus.read(ptr %14, %deus.fat %15)
  store %Result.2 %16, ptr %"%t7", align 8
  br label %bb5

bb4:                                              ; preds = %bb22, %bb17
  store ptr %bytes, ptr %"%t43", align 8
  %17 = load ptr, ptr %"%t43", align 8
  %18 = load %deus.vec, ptr %17, align 8
  %19 = extractvalue %deus.vec %18, 0
  %20 = icmp eq ptr %19, null
  %buf = select i1 %20, ptr inttoptr (i64 1 to ptr), ptr %19
  %21 = extractvalue %deus.vec %18, 1
  %22 = insertvalue %deus.fat undef, ptr %buf, 0
  %23 = insertvalue %deus.fat %22, i64 %21, 1
  store %deus.fat %23, ptr %"%t42", align 8
  %24 = load %deus.fat, ptr %"%t42", align 8
  %25 = call %Option.3 @deus.last.T_u8(%deus.fat %24)
  store %Option.3 %25, ptr %"%t41", align 8
  br label %bb32

bb5:                                              ; preds = %bb3
  %26 = load %Result.2, ptr %"%t7", align 8
  %27 = extractvalue %Result.2 %26, 0
  store i32 %27, ptr %"%t14", align 4
  %28 = load i32, ptr %"%t14", align 4
  switch i32 %28, label %bb7 [
    i32 0, label %bb8
  ]

bb6:                                              ; preds = %bb11, %bb8
  call void @"drop.usize ! IoError"(ptr %"%t7")
  %29 = load i64, ptr %n, align 8
  store i64 %29, ptr %a, align 8
  store i64 0, ptr %b, align 8
  %30 = call i32 @cmp.usize(ptr %a, ptr %b)
  %31 = icmp eq i32 %30, 0
  store i1 %31, ptr %"%t19", align 1
  %32 = load i1, ptr %"%t19", align 1
  %33 = zext i1 %32 to i32
  switch i32 %33, label %bb13 [
    i32 1, label %bb12
  ]

bb7:                                              ; preds = %bb5
  %34 = load %Result.2, ptr %"%t7", align 8
  %35 = extractvalue %Result.2 %34, 0
  store i32 %35, ptr %"%t16", align 4
  %36 = load i32, ptr %"%t16", align 4
  switch i32 %36, label %bb9 [
    i32 1, label %bb10
  ]

bb8:                                              ; preds = %bb5
  %37 = getelementptr inbounds nuw %Result.2, ptr %"%t7", i32 0, i32 1
  %38 = getelementptr inbounds nuw { i64 }, ptr %37, i32 0, i32 0
  %39 = load i64, ptr %38, align 8
  store i64 %39, ptr %"%v0", align 8
  %40 = load i64, ptr %"%v0", align 8
  store i64 %40, ptr %n, align 8
  br label %bb6

bb9:                                              ; preds = %bb7
  unreachable

bb10:                                             ; preds = %bb7
  %41 = getelementptr inbounds nuw %Result.2, ptr %"%t7", i32 0, i32 1
  %42 = getelementptr inbounds nuw { %IoError }, ptr %41, i32 0, i32 0
  %43 = load %IoError, ptr %42, align 8
  store %IoError %43, ptr %"%err1", align 8
  %44 = load %IoError, ptr %"%err1", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant, i8 0, i64 48, i1 false)
  %45 = getelementptr inbounds nuw %Result.0, ptr %variant, i32 0, i32 0
  store i32 1, ptr %45, align 4
  %46 = getelementptr inbounds nuw %Result.0, ptr %variant, i32 0, i32 1
  %47 = getelementptr inbounds nuw { %IoError }, ptr %46, i32 0, i32 0
  store %IoError %44, ptr %47, align 8
  %48 = load %Result.0, ptr %variant, align 8
  store %Result.0 %48, ptr %_0, align 8
  call void @"drop.Vec[u8]"(ptr %bytes)
  br label %bb1

bb11:                                             ; No predecessors!
  br label %bb6

bb12:                                             ; preds = %bb6
  store ptr %bytes, ptr %"%t23", align 8
  %49 = load ptr, ptr %"%t23", align 8
  %50 = load %deus.vec, ptr %49, align 8
  %51 = extractvalue %deus.vec %50, 0
  %52 = icmp eq ptr %51, null
  %buf1 = select i1 %52, ptr inttoptr (i64 1 to ptr), ptr %51
  %53 = extractvalue %deus.vec %50, 1
  %54 = insertvalue %deus.fat undef, ptr %buf1, 0
  %55 = insertvalue %deus.fat %54, i64 %53, 1
  store %deus.fat %55, ptr %"%t22", align 8
  %56 = load %deus.fat, ptr %"%t22", align 8
  %57 = call i1 @deus.is_empty.T_u8(%deus.fat %56)
  store i1 %57, ptr %"%t21", align 1
  br label %bb18

bb13:                                             ; preds = %bb6
  br label %bb14

bb14:                                             ; preds = %bb21, %bb13
  store i64 1, ptr %"%t30", align 8
  store i64 0, ptr %"%t31", align 8
  %58 = load i64, ptr %"%t31", align 8
  %59 = load i64, ptr %"%t30", align 8
  store i64 %58, ptr %a2, align 8
  store i64 %59, ptr %b3, align 8
  %60 = call i32 @cmp.usize(ptr %a2, ptr %b3)
  %61 = icmp slt i32 %60, 0
  store i1 %61, ptr %"%t32", align 1
  %62 = load i1, ptr %"%t32", align 1
  br i1 %62, label %bb25, label %assert.fail

bb15:                                             ; preds = %bb18
  call void @llvm.memset.p0.i64(ptr align 4 %variant4, i8 0, i64 4, i1 false)
  %63 = getelementptr inbounds nuw %ErrorKind, ptr %variant4, i32 0, i32 0
  store i32 22, ptr %63, align 4
  %64 = load %ErrorKind, ptr %variant4, align 4
  store %ErrorKind %64, ptr %"%t26", align 4
  %65 = load %ErrorKind, ptr %"%t26", align 4
  %66 = call %IoError @deus.new(%ErrorKind %65, %deus.fat { ptr @str.11, i64 12 })
  store %IoError %66, ptr %"%t25", align 8
  br label %bb19

bb16:                                             ; preds = %bb18
  br label %bb17

bb17:                                             ; preds = %bb20, %bb16
  br label %bb4

bb18:                                             ; preds = %bb12
  %67 = load i1, ptr %"%t21", align 1
  %68 = zext i1 %67 to i32
  switch i32 %68, label %bb16 [
    i32 1, label %bb15
  ]

bb19:                                             ; preds = %bb15
  %69 = load %IoError, ptr %"%t25", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant5, i8 0, i64 48, i1 false)
  %70 = getelementptr inbounds nuw %Result.0, ptr %variant5, i32 0, i32 0
  store i32 1, ptr %70, align 4
  %71 = getelementptr inbounds nuw %Result.0, ptr %variant5, i32 0, i32 1
  %72 = getelementptr inbounds nuw { %IoError }, ptr %71, i32 0, i32 0
  store %IoError %69, ptr %72, align 8
  %73 = load %Result.0, ptr %variant5, align 8
  store %Result.0 %73, ptr %_0, align 8
  call void @"drop.Vec[u8]"(ptr %bytes)
  br label %bb1

bb20:                                             ; No predecessors!
  br label %bb17

bb21:                                             ; No predecessors!
  br label %bb14

bb22:                                             ; preds = %bb25
  br label %bb4

bb23:                                             ; preds = %bb25
  br label %bb24

bb24:                                             ; preds = %bb26, %bb23
  store i64 1, ptr %"%t34", align 8
  store i64 0, ptr %"%t35", align 8
  %74 = load i64, ptr %"%t35", align 8
  %75 = load i64, ptr %"%t34", align 8
  store i64 %74, ptr %a6, align 8
  store i64 %75, ptr %b7, align 8
  %76 = call i32 @cmp.usize(ptr %a6, ptr %b7)
  %77 = icmp slt i32 %76, 0
  store i1 %77, ptr %"%t36", align 1
  %78 = load i1, ptr %"%t36", align 1
  br i1 %78, label %bb27, label %assert.fail8

bb25:                                             ; preds = %bb14
  %79 = load i64, ptr %"%t31", align 8
  %80 = getelementptr inbounds [1 x i8], ptr %one, i64 0, i64 %79
  %81 = load i8, ptr %80, align 1
  store i8 %81, ptr %a10, align 1
  store i8 10, ptr %b11, align 1
  %82 = call i32 @cmp.u8(ptr %a10, ptr %b11)
  %83 = icmp eq i32 %82, 0
  store i1 %83, ptr %"%t29", align 1
  %84 = load i1, ptr %"%t29", align 1
  %85 = zext i1 %84 to i32
  switch i32 %85, label %bb23 [
    i32 1, label %bb22
  ]

bb26:                                             ; No predecessors!
  br label %bb24

bb27:                                             ; preds = %bb24
  %86 = load i64, ptr %"%t35", align 8
  %87 = getelementptr inbounds [1 x i8], ptr %one, i64 0, i64 %86
  %88 = load i8, ptr %87, align 1
  store i8 %88, ptr %"%t37", align 1
  store ptr %bytes, ptr %"%t38", align 8
  %89 = load ptr, ptr %"%t38", align 8
  store ptr %89, ptr %"%t39", align 8
  %90 = load ptr, ptr %"%t39", align 8
  %91 = load i8, ptr %"%t37", align 1
  store i8 %91, ptr %x, align 1
  call void @deus_vec_push(ptr %90, ptr %x, i64 1)
  br label %bb28

bb28:                                             ; preds = %bb27
  br label %bb3

bb29:                                             ; preds = %bb34
  store ptr %bytes, ptr %"%t47", align 8
  %92 = load ptr, ptr %"%t47", align 8
  store ptr %92, ptr %"%t48", align 8
  %93 = load ptr, ptr %"%t48", align 8
  %94 = call i1 @deus_vec_pop(ptr %93, ptr %p, i64 1)
  %95 = load i8, ptr %p, align 1
  call void @llvm.memset.p0.i64(ptr align 4 %variant12, i8 0, i64 8, i1 false)
  %96 = getelementptr inbounds nuw %Option.1, ptr %variant12, i32 0, i32 0
  store i32 1, ptr %96, align 4
  %97 = getelementptr inbounds nuw %Option.1, ptr %variant12, i32 0, i32 1
  %98 = getelementptr inbounds nuw { i8 }, ptr %97, i32 0, i32 0
  store i8 %95, ptr %98, align 1
  %99 = load %Option.1, ptr %variant12, align 4
  call void @llvm.memset.p0.i64(ptr align 4 %variant13, i8 0, i64 8, i1 false)
  %100 = getelementptr inbounds nuw %Option.1, ptr %variant13, i32 0, i32 0
  store i32 0, ptr %100, align 4
  %101 = load %Option.1, ptr %variant13, align 4
  %102 = select i1 %94, %Option.1 %99, %Option.1 %101
  store %Option.1 %102, ptr %"%t46", align 4
  br label %bb35

bb30:                                             ; preds = %bb33, %bb32
  br label %bb31

bb31:                                             ; preds = %bb37, %bb30
  store ptr %bytes, ptr %"%t51", align 8
  %103 = load ptr, ptr %"%t51", align 8
  %104 = load %deus.vec, ptr %103, align 8
  %105 = extractvalue %deus.vec %104, 0
  %106 = icmp eq ptr %105, null
  %buf14 = select i1 %106, ptr inttoptr (i64 1 to ptr), ptr %105
  %107 = extractvalue %deus.vec %104, 1
  %108 = insertvalue %deus.fat undef, ptr %buf14, 0
  %109 = insertvalue %deus.fat %108, i64 %107, 1
  store %deus.fat %109, ptr %"%t50", align 8
  br label %bb38

bb32:                                             ; preds = %bb4
  %110 = load %Option.3, ptr %"%t41", align 8
  %111 = extractvalue %Option.3 %110, 0
  %112 = icmp eq ptr %111, null
  %113 = select i1 %112, i32 0, i32 1
  store i32 %113, ptr %"%t44", align 4
  %114 = load i32, ptr %"%t44", align 4
  switch i32 %114, label %bb30 [
    i32 1, label %bb33
  ]

bb33:                                             ; preds = %bb32
  %115 = getelementptr inbounds nuw { ptr }, ptr %"%t41", i32 0, i32 0
  %116 = load ptr, ptr %115, align 8
  %117 = load i8, ptr %116, align 1
  store i8 %117, ptr %a15, align 1
  store i8 13, ptr %b16, align 1
  %118 = call i32 @cmp.u8(ptr %a15, ptr %b16)
  %119 = icmp eq i32 %118, 0
  store i1 %119, ptr %"%t45", align 1
  %120 = load i1, ptr %"%t45", align 1
  %121 = zext i1 %120 to i32
  switch i32 %121, label %bb30 [
    i32 1, label %bb34
  ]

bb34:                                             ; preds = %bb33
  br label %bb29

bb35:                                             ; preds = %bb29
  br label %bb37

bb36:                                             ; No predecessors!
  unreachable

bb37:                                             ; preds = %bb35
  br label %bb31

bb38:                                             ; preds = %bb31
  %122 = load %deus.fat, ptr %"%t50", align 8
  %123 = call %deus.vec @deus.from_utf8_lossy(%deus.fat %122)
  store %deus.vec %123, ptr %"%t49", align 8
  br label %bb39

bb39:                                             ; preds = %bb38
  %124 = load %deus.vec, ptr %"%t49", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant17, i8 0, i64 48, i1 false)
  %125 = getelementptr inbounds nuw %Result.0, ptr %variant17, i32 0, i32 0
  store i32 0, ptr %125, align 4
  %126 = getelementptr inbounds nuw %Result.0, ptr %variant17, i32 0, i32 1
  %127 = getelementptr inbounds nuw { %deus.vec }, ptr %126, i32 0, i32 0
  store %deus.vec %124, ptr %127, align 8
  %128 = load %Result.0, ptr %variant17, align 8
  store %Result.0 %128, ptr %_0, align 8
  call void @"drop.Vec[u8]"(ptr %bytes)
  br label %bb1

assert.fail:                                      ; preds = %bb14
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.10) #2
  unreachable

dead:                                             ; No predecessors!
  unreachable

assert.fail8:                                     ; preds = %bb24
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.12) #2
  unreachable

dead9:                                            ; No predecessors!
  unreachable
}

declare void @deus_vec_init(ptr)

define internal void @drop.String(ptr %0) #0 {
entry:
  %1 = load %deus.vec, ptr %0, align 8
  %2 = extractvalue %deus.vec %1, 2
  %3 = icmp sgt i64 %2, 0
  br i1 %3, label %free, label %freed

free:                                             ; preds = %entry
  %4 = extractvalue %deus.vec %1, 0
  call void @deus_free(ptr %4)
  br label %freed

freed:                                            ; preds = %free, %entry
  ret void
}

declare void @deus_iter_init(ptr, i32, i64)

define internal %Option.1 @deus.nth.T_u8(ptr %0, i64 %1) #0 {
entry:
  %variant4 = alloca %Option.1, align 8
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %variant3 = alloca %Option.1, align 8
  %variant2 = alloca %Option.1, align 8
  %variant = alloca %Option.1, align 8
  %n1 = alloca i8, align 1
  %"%t15" = alloca %deus.unit, align 8
  %"%t14" = alloca %deus.unit, align 8
  %"%t13" = alloca i1, align 1
  %"%t12" = alloca %deus.unit, align 8
  %x = alloca i8, align 1
  %"%t10" = alloca i32, align 4
  %"%t9" = alloca ptr, align 8
  %"%t8" = alloca ptr, align 8
  %"%t7" = alloca %Option.1, align 8
  %"%t6" = alloca %deus.unit, align 8
  %"%t5" = alloca %deus.unit, align 8
  %k = alloca i64, align 8
  %it = alloca ptr, align 8
  %n = alloca i64, align 8
  %self = alloca ptr, align 8
  %_0 = alloca %Option.1, align 8
  store ptr %0, ptr %self, align 8
  store i64 %1, ptr %n, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load ptr, ptr %self, align 8
  store ptr %2, ptr %it, align 8
  store i64 0, ptr %k, align 8
  br label %bb2

bb1:                                              ; preds = %bb9, %bb3
  %3 = load %Option.1, ptr %_0, align 4
  ret %Option.1 %3

bb2:                                              ; preds = %bb6, %bb0
  store ptr %it, ptr %"%t8", align 8
  %4 = load ptr, ptr %"%t8", align 8
  store ptr %4, ptr %"%t9", align 8
  %5 = load ptr, ptr %"%t9", align 8
  %6 = load ptr, ptr %5, align 8
  %7 = call i1 @deus_iter_next(ptr %6, ptr %n1)
  %8 = load i8, ptr %n1, align 1
  call void @llvm.memset.p0.i64(ptr align 4 %variant, i8 0, i64 8, i1 false)
  %9 = getelementptr inbounds nuw %Option.1, ptr %variant, i32 0, i32 0
  store i32 1, ptr %9, align 4
  %10 = getelementptr inbounds nuw %Option.1, ptr %variant, i32 0, i32 1
  %11 = getelementptr inbounds nuw { i8 }, ptr %10, i32 0, i32 0
  store i8 %8, ptr %11, align 1
  %12 = load %Option.1, ptr %variant, align 4
  call void @llvm.memset.p0.i64(ptr align 4 %variant2, i8 0, i64 8, i1 false)
  %13 = getelementptr inbounds nuw %Option.1, ptr %variant2, i32 0, i32 0
  store i32 0, ptr %13, align 4
  %14 = load %Option.1, ptr %variant2, align 4
  %15 = select i1 %7, %Option.1 %12, %Option.1 %14
  store %Option.1 %15, ptr %"%t7", align 4
  br label %bb7

bb3:                                              ; preds = %bb5
  call void @llvm.memset.p0.i64(ptr align 4 %variant3, i8 0, i64 8, i1 false)
  %16 = getelementptr inbounds nuw %Option.1, ptr %variant3, i32 0, i32 0
  store i32 0, ptr %16, align 4
  %17 = load %Option.1, ptr %variant3, align 4
  store %Option.1 %17, ptr %_0, align 4
  call void @"drop.Iter[u8]"(ptr %it)
  br label %bb1

bb4:                                              ; preds = %bb8
  %18 = load i64, ptr %k, align 8
  %19 = load i64, ptr %n, align 8
  store i64 %18, ptr %a, align 8
  store i64 %19, ptr %b, align 8
  %20 = call i32 @cmp.usize(ptr %a, ptr %b)
  %21 = icmp eq i32 %20, 0
  store i1 %21, ptr %"%t13", align 1
  %22 = load i1, ptr %"%t13", align 1
  %23 = zext i1 %22 to i32
  switch i32 %23, label %bb10 [
    i32 1, label %bb9
  ]

bb5:                                              ; preds = %bb7
  br label %bb3

bb6:                                              ; preds = %bb13, %ok
  br label %bb2

bb7:                                              ; preds = %bb2
  %24 = load %Option.1, ptr %"%t7", align 4
  %25 = extractvalue %Option.1 %24, 0
  store i32 %25, ptr %"%t10", align 4
  %26 = load i32, ptr %"%t10", align 4
  switch i32 %26, label %bb5 [
    i32 1, label %bb8
  ]

bb8:                                              ; preds = %bb7
  %27 = getelementptr inbounds nuw %Option.1, ptr %"%t7", i32 0, i32 1
  %28 = getelementptr inbounds nuw { i8 }, ptr %27, i32 0, i32 0
  %29 = load i8, ptr %28, align 1
  store i8 %29, ptr %x, align 1
  br label %bb4

bb9:                                              ; preds = %bb4
  %30 = load i8, ptr %x, align 1
  call void @llvm.memset.p0.i64(ptr align 4 %variant4, i8 0, i64 8, i1 false)
  %31 = getelementptr inbounds nuw %Option.1, ptr %variant4, i32 0, i32 0
  store i32 1, ptr %31, align 4
  %32 = getelementptr inbounds nuw %Option.1, ptr %variant4, i32 0, i32 1
  %33 = getelementptr inbounds nuw { i8 }, ptr %32, i32 0, i32 0
  store i8 %30, ptr %33, align 1
  %34 = load %Option.1, ptr %variant4, align 4
  store %Option.1 %34, ptr %_0, align 4
  call void @"drop.Iter[u8]"(ptr %it)
  br label %bb1

bb10:                                             ; preds = %bb4
  br label %bb11

bb11:                                             ; preds = %bb12, %bb10
  %35 = load i64, ptr %k, align 8
  %36 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %35, i64 1)
  %37 = extractvalue { i64, i1 } %36, 0
  %38 = extractvalue { i64, i1 } %36, 1
  %39 = xor i1 %38, true
  br i1 %39, label %ok, label %fail

bb12:                                             ; No predecessors!
  br label %bb11

bb13:                                             ; No predecessors!
  br label %bb6

fail:                                             ; preds = %bb11
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.15) #2
  unreachable

ok:                                               ; preds = %bb11
  store i64 %37, ptr %k, align 8
  br label %bb6

dead:                                             ; No predecessors!
  unreachable
}

define internal i8 @deus.unwrap.T_u8(%Option.1 %0, ptr %1) #0 {
entry:
  %"%t6" = alloca %deus.unit, align 8
  %"%t5" = alloca %deus.unit, align 8
  %"%t4" = alloca i32, align 4
  %x = alloca i8, align 1
  %"%t2" = alloca i32, align 4
  %self = alloca %Option.1, align 8
  %_0 = alloca i8, align 1
  %2 = freeze %Option.1 %0
  store %Option.1 %2, ptr %self, align 4
  br label %bb0

bb0:                                              ; preds = %entry
  %3 = load %Option.1, ptr %self, align 4
  %4 = extractvalue %Option.1 %3, 0
  store i32 %4, ptr %"%t2", align 4
  %5 = load i32, ptr %"%t2", align 4
  switch i32 %5, label %bb3 [
    i32 1, label %bb4
  ]

bb1:                                              ; preds = %bb2
  %6 = load i8, ptr %_0, align 1
  ret i8 %6

bb2:                                              ; preds = %bb7, %bb4
  br label %bb1

bb3:                                              ; preds = %bb0
  %7 = load %Option.1, ptr %self, align 4
  %8 = extractvalue %Option.1 %7, 0
  store i32 %8, ptr %"%t4", align 4
  %9 = load i32, ptr %"%t4", align 4
  switch i32 %9, label %bb5 [
    i32 0, label %bb6
  ]

bb4:                                              ; preds = %bb0
  %10 = getelementptr inbounds nuw %Option.1, ptr %self, i32 0, i32 1
  %11 = getelementptr inbounds nuw { i8 }, ptr %10, i32 0, i32 0
  %12 = load i8, ptr %11, align 1
  store i8 %12, ptr %x, align 1
  %13 = load i8, ptr %x, align 1
  store i8 %13, ptr %_0, align 1
  br label %bb2

bb5:                                              ; preds = %bb3
  unreachable

bb6:                                              ; preds = %bb3
  %14 = icmp eq ptr %1, null
  %15 = select i1 %14, ptr @loc.18, ptr %1
  call void @deus_panic_at(ptr @str.16, i64 42, ptr %15) #2
  unreachable

bb7:                                              ; No predecessors!
  br label %bb2

dead:                                             ; No predecessors!
  unreachable
}

define internal i8 @deus.transform(i8 %0, i64 %1, i8 %2) #0 {
entry:
  %variant4 = alloca %Option.4, align 8
  %variant = alloca %Option.4, align 8
  %"%t30" = alloca %deus.unit, align 8
  %"%t29" = alloca %deus.unit, align 8
  %"%t28" = alloca i8, align 1
  %"%t27" = alloca i32, align 4
  %"%t26" = alloca i8, align 1
  %"%t25" = alloca i8, align 1
  %"%t24" = alloca %deus.unit, align 8
  %"%t23" = alloca i8, align 1
  %"%t22" = alloca i8, align 1
  %"%t21" = alloca %deus.unit, align 8
  %"%t20" = alloca i8, align 1
  %"%t19" = alloca i8, align 1
  %"%t18" = alloca i8, align 1
  %"%t17" = alloca i8, align 1
  %"%t16" = alloca i8, align 1
  %"%t15" = alloca %deus.unit, align 8
  %"%t14" = alloca i64, align 8
  %"%t13" = alloca i64, align 8
  %"%t12" = alloca %Option.4, align 8
  %"%t11" = alloca i32, align 4
  %"%t10" = alloca i8, align 1
  %"%t9" = alloca i8, align 1
  %"%t8" = alloca %deus.unit, align 8
  %"%t7" = alloca i64, align 8
  %"%t6" = alloca i64, align 8
  %"%t5" = alloca i8, align 1
  %"%t4" = alloca %deus.unit, align 8
  %state = alloca i8, align 1
  %index = alloca i64, align 8
  %x = alloca i8, align 1
  %_0 = alloca i8, align 1
  store i8 %0, ptr %x, align 1
  store i64 %1, ptr %index, align 8
  store i8 %2, ptr %state, align 1
  br label %bb0

bb0:                                              ; preds = %entry
  %3 = load i64, ptr %index, align 8
  %4 = mul i64 %3, 13
  store i64 %4, ptr %"%t7", align 8
  %5 = load i64, ptr %"%t7", align 8
  %6 = add i64 %5, 55
  store i64 %6, ptr %"%t6", align 8
  %7 = load i64, ptr %"%t6", align 8
  %8 = trunc i64 %7 to i8
  store i8 %8, ptr %"%t5", align 1
  br label %bb2

bb1:                                              ; preds = %bb7, %bb6
  %9 = load i8, ptr %_0, align 1
  ret i8 %9

bb2:                                              ; preds = %bb0
  %10 = load i8, ptr %x, align 1
  %11 = load i8, ptr %"%t5", align 1
  %12 = xor i8 %10, %11
  store i8 %12, ptr %x, align 1
  %13 = load i8, ptr %x, align 1
  store i8 %13, ptr %"%t10", align 1
  %14 = load i64, ptr %index, align 8
  br i1 true, label %ok, label %fail

bb3:                                              ; preds = %ok2
  %15 = load %Option.4, ptr %"%t12", align 4
  %16 = call i32 @deus.unwrap.T_u32(%Option.4 %15, ptr @loc.22)
  store i32 %16, ptr %"%t11", align 4
  br label %bb4

bb4:                                              ; preds = %bb3
  %17 = load i8, ptr %"%t10", align 1
  %18 = load i32, ptr %"%t11", align 4
  %19 = call i8 @deus.rol8(i8 %17, i32 %18)
  store i8 %19, ptr %"%t9", align 1
  br label %bb5

bb5:                                              ; preds = %bb4
  %20 = load i8, ptr %"%t9", align 1
  store i8 %20, ptr %x, align 1
  %21 = load i8, ptr %x, align 1
  %22 = and i8 %21, -86
  store i8 %22, ptr %"%t18", align 1
  %23 = load i8, ptr %"%t18", align 1
  br i1 true, label %ok6, label %fail5

bb6:                                              ; preds = %ok9
  %24 = load i8, ptr %"%t25", align 1
  store i8 %24, ptr %x, align 1
  %25 = load i8, ptr %x, align 1
  %26 = load i8, ptr %state, align 1
  %27 = xor i8 %25, %26
  store i8 %27, ptr %x, align 1
  %28 = load i8, ptr %x, align 1
  store i8 %28, ptr %_0, align 1
  br label %bb1

bb7:                                              ; No predecessors!
  br label %bb1

fail:                                             ; preds = %bb2
  call void @deus_panic_at(ptr @panic.19, i64 25, ptr @loc.20) #2
  unreachable

ok:                                               ; preds = %bb2
  %29 = urem i64 %14, 5
  store i64 %29, ptr %"%t14", align 8
  %30 = load i64, ptr %"%t14", align 8
  %31 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %30, i64 1)
  %32 = extractvalue { i64, i1 } %31, 0
  %33 = extractvalue { i64, i1 } %31, 1
  %34 = xor i1 %33, true
  br i1 %34, label %ok2, label %fail1

dead:                                             ; No predecessors!
  unreachable

fail1:                                            ; preds = %ok
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.21) #2
  unreachable

ok2:                                              ; preds = %ok
  store i64 %32, ptr %"%t13", align 8
  %35 = load i64, ptr %"%t13", align 8
  %36 = zext i64 %35 to i66
  %37 = icmp slt i66 %36, 0
  %38 = icmp sgt i66 %36, 4294967295
  %39 = trunc i66 %36 to i32
  %40 = or i1 %37, %38
  call void @llvm.memset.p0.i64(ptr align 4 %variant, i8 0, i64 8, i1 false)
  %41 = getelementptr inbounds nuw %Option.4, ptr %variant, i32 0, i32 0
  store i32 0, ptr %41, align 4
  %42 = load %Option.4, ptr %variant, align 4
  call void @llvm.memset.p0.i64(ptr align 4 %variant4, i8 0, i64 8, i1 false)
  %43 = getelementptr inbounds nuw %Option.4, ptr %variant4, i32 0, i32 0
  store i32 1, ptr %43, align 4
  %44 = getelementptr inbounds nuw %Option.4, ptr %variant4, i32 0, i32 1
  %45 = getelementptr inbounds nuw { i32 }, ptr %44, i32 0, i32 0
  store i32 %39, ptr %45, align 4
  %46 = load %Option.4, ptr %variant4, align 4
  %47 = select i1 %40, %Option.4 %42, %Option.4 %46
  store %Option.4 %47, ptr %"%t12", align 4
  br label %bb3

dead3:                                            ; No predecessors!
  unreachable

fail5:                                            ; preds = %bb5
  call void @deus_panic_at(ptr @panic.23, i64 30, ptr @loc.24) #2
  unreachable

ok6:                                              ; preds = %bb5
  %48 = lshr i8 %23, 1
  store i8 %48, ptr %"%t17", align 1
  %49 = load i8, ptr %x, align 1
  %50 = and i8 %49, 85
  store i8 %50, ptr %"%t20", align 1
  %51 = load i8, ptr %"%t20", align 1
  br i1 true, label %ok9, label %fail8

dead7:                                            ; No predecessors!
  unreachable

fail8:                                            ; preds = %ok6
  call void @deus_panic_at(ptr @panic.23, i64 30, ptr @loc.25) #2
  unreachable

ok9:                                              ; preds = %ok6
  %52 = shl i8 %51, 1
  store i8 %52, ptr %"%t19", align 1
  %53 = load i8, ptr %"%t17", align 1
  %54 = load i8, ptr %"%t19", align 1
  %55 = or i8 %53, %54
  store i8 %55, ptr %"%t16", align 1
  %56 = load i8, ptr %"%t16", align 1
  store i8 %56, ptr %x, align 1
  %57 = load i8, ptr %x, align 1
  %58 = mul i8 %57, 93
  store i8 %58, ptr %"%t23", align 1
  %59 = load i8, ptr %"%t23", align 1
  %60 = add i8 %59, 59
  store i8 %60, ptr %"%t22", align 1
  %61 = load i8, ptr %"%t22", align 1
  store i8 %61, ptr %x, align 1
  %62 = load i8, ptr %x, align 1
  store i8 %62, ptr %"%t26", align 1
  %63 = load i8, ptr %state, align 1
  %64 = and i8 %63, 7
  store i8 %64, ptr %"%t28", align 1
  %65 = load i8, ptr %"%t28", align 1
  %66 = zext i8 %65 to i32
  store i32 %66, ptr %"%t27", align 4
  %67 = load i8, ptr %"%t26", align 1
  %68 = load i32, ptr %"%t27", align 4
  %69 = call i8 @deus.ror8(i8 %67, i32 %68)
  store i8 %69, ptr %"%t25", align 1
  br label %bb6

dead10:                                           ; No predecessors!
  unreachable
}

declare void @deus_vec_push(ptr, ptr, i64)

define internal i8 @deus.rol8(i8 %0, i32 %1) #0 {
entry:
  %"%t8" = alloca i32, align 4
  %"%t7" = alloca i32, align 4
  %"%t6" = alloca i8, align 1
  %"%t5" = alloca i8, align 1
  %"%t4" = alloca %deus.unit, align 8
  %"%t3" = alloca %deus.unit, align 8
  %n = alloca i32, align 4
  %x = alloca i8, align 1
  %_0 = alloca i8, align 1
  store i8 %0, ptr %x, align 1
  store i32 %1, ptr %n, align 4
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load i32, ptr %n, align 4
  %3 = and i32 %2, 7
  store i32 %3, ptr %n, align 4
  %4 = load i8, ptr %x, align 1
  %5 = load i32, ptr %n, align 4
  %6 = trunc i32 %5 to i8
  %7 = icmp ult i8 %6, 8
  br i1 %7, label %ok, label %fail

bb1:                                              ; preds = %bb2, %ok5
  %8 = load i8, ptr %_0, align 1
  ret i8 %8

bb2:                                              ; No predecessors!
  br label %bb1

fail:                                             ; preds = %bb0
  call void @deus_panic_at(ptr @panic.23, i64 30, ptr @loc.26) #2
  unreachable

ok:                                               ; preds = %bb0
  %9 = shl i8 %4, %6
  store i8 %9, ptr %"%t5", align 1
  %10 = load i32, ptr %n, align 4
  %11 = call { i32, i1 } @llvm.usub.with.overflow.i32(i32 8, i32 %10)
  %12 = extractvalue { i32, i1 } %11, 0
  %13 = extractvalue { i32, i1 } %11, 1
  %14 = xor i1 %13, true
  br i1 %14, label %ok2, label %fail1

dead:                                             ; No predecessors!
  unreachable

fail1:                                            ; preds = %ok
  call void @deus_panic_at(ptr @panic.27, i64 33, ptr @loc.28) #2
  unreachable

ok2:                                              ; preds = %ok
  store i32 %12, ptr %"%t8", align 4
  %15 = load i32, ptr %"%t8", align 4
  %16 = and i32 %15, 7
  store i32 %16, ptr %"%t7", align 4
  %17 = load i8, ptr %x, align 1
  %18 = load i32, ptr %"%t7", align 4
  %19 = trunc i32 %18 to i8
  %20 = icmp ult i8 %19, 8
  br i1 %20, label %ok5, label %fail4

dead3:                                            ; No predecessors!
  unreachable

fail4:                                            ; preds = %ok2
  call void @deus_panic_at(ptr @panic.23, i64 30, ptr @loc.29) #2
  unreachable

ok5:                                              ; preds = %ok2
  %21 = lshr i8 %17, %19
  store i8 %21, ptr %"%t6", align 1
  %22 = load i8, ptr %"%t5", align 1
  %23 = load i8, ptr %"%t6", align 1
  %24 = or i8 %22, %23
  store i8 %24, ptr %_0, align 1
  br label %bb1

dead6:                                            ; No predecessors!
  unreachable
}

define internal %Result.2 @deus.read(ptr %0, %deus.fat %1) #0 {
entry:
  %"%t10" = alloca %deus.fat, align 8
  %"%t9" = alloca i64, align 8
  %"%t8" = alloca ptr, align 8
  %"%t7" = alloca %deus.fat, align 8
  %"%t6" = alloca %deus.fat, align 8
  %"%t5" = alloca ptr, align 8
  %"%t4" = alloca ptr, align 8
  %"%t3" = alloca i64, align 8
  %buf = alloca %deus.fat, align 8
  %self = alloca ptr, align 8
  %_0 = alloca %Result.2, align 8
  store ptr %0, ptr %self, align 8
  %2 = freeze %deus.fat %1
  store %deus.fat %2, ptr %buf, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %3 = load %deus.fat, ptr %buf, align 8
  %4 = extractvalue %deus.fat %3, 0
  %5 = extractvalue %deus.fat %3, 1
  %6 = insertvalue %deus.fat undef, ptr %4, 0
  %7 = insertvalue %deus.fat %6, i64 %5, 1
  store %deus.fat %7, ptr %"%t6", align 8
  %8 = load %deus.fat, ptr %"%t6", align 8
  %9 = extractvalue %deus.fat %8, 0
  %10 = extractvalue %deus.fat %8, 1
  %11 = insertvalue %deus.fat undef, ptr %9, 0
  %12 = insertvalue %deus.fat %11, i64 %10, 1
  store %deus.fat %12, ptr %"%t7", align 8
  %13 = load %deus.fat, ptr %"%t7", align 8
  %14 = extractvalue %deus.fat %13, 0
  %15 = extractvalue %deus.fat %13, 1
  store ptr %14, ptr %"%t5", align 8
  br label %bb2

bb1:                                              ; preds = %bb6
  %16 = load %Result.2, ptr %_0, align 8
  ret %Result.2 %16

bb2:                                              ; preds = %bb0
  %17 = load ptr, ptr %"%t5", align 8
  store ptr %17, ptr %"%t4", align 8
  br label %bb3

bb3:                                              ; preds = %bb2
  %18 = load ptr, ptr %"%t4", align 8
  store ptr %18, ptr %"%t8", align 8
  %19 = load %deus.fat, ptr %buf, align 8
  %20 = extractvalue %deus.fat %19, 0
  %21 = extractvalue %deus.fat %19, 1
  %22 = insertvalue %deus.fat undef, ptr %20, 0
  %23 = insertvalue %deus.fat %22, i64 %21, 1
  store %deus.fat %23, ptr %"%t10", align 8
  %24 = load %deus.fat, ptr %"%t10", align 8
  %25 = extractvalue %deus.fat %24, 0
  %26 = extractvalue %deus.fat %24, 1
  store i64 %26, ptr %"%t9", align 8
  br label %bb4

bb4:                                              ; preds = %bb3
  %27 = load ptr, ptr %"%t8", align 8
  %28 = load i64, ptr %"%t9", align 8
  %29 = call i64 @read(i32 0, ptr %27, i64 %28)
  store i64 %29, ptr %"%t3", align 8
  br label %bb5

bb5:                                              ; preds = %bb4
  %30 = load i64, ptr %"%t3", align 8
  %31 = call %Result.2 @deus.check(i64 %30)
  store %Result.2 %31, ptr %_0, align 8
  br label %bb6

bb6:                                              ; preds = %bb5
  br label %bb1
}

define internal %Option.3 @deus.last.T_u8(%deus.fat %0) #0 {
entry:
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %"%t9" = alloca i1, align 1
  %"%t8" = alloca %deus.fat, align 8
  %"%t7" = alloca i64, align 8
  %"%t6" = alloca i64, align 8
  %"%t5" = alloca i64, align 8
  %"%t4" = alloca ptr, align 8
  %"%t3" = alloca %deus.fat, align 8
  %"%t2" = alloca i1, align 1
  %self = alloca %deus.fat, align 8
  %_0 = alloca %Option.3, align 8
  %1 = freeze %deus.fat %0
  store %deus.fat %1, ptr %self, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load %deus.fat, ptr %self, align 8
  %3 = extractvalue %deus.fat %2, 0
  %4 = extractvalue %deus.fat %2, 1
  %5 = insertvalue %deus.fat undef, ptr %3, 0
  %6 = insertvalue %deus.fat %5, i64 %4, 1
  store %deus.fat %6, ptr %"%t3", align 8
  %7 = load %deus.fat, ptr %"%t3", align 8
  %8 = call i1 @deus.is_empty.T_u8(%deus.fat %7)
  store i1 %8, ptr %"%t2", align 1
  br label %bb5

bb1:                                              ; preds = %bb4
  %9 = load %Option.3, ptr %_0, align 8
  ret %Option.3 %9

bb2:                                              ; preds = %bb5
  store %Option.3 zeroinitializer, ptr %_0, align 8
  br label %bb4

bb3:                                              ; preds = %bb5
  %10 = load %deus.fat, ptr %self, align 8
  %11 = extractvalue %deus.fat %10, 0
  %12 = extractvalue %deus.fat %10, 1
  store i64 %12, ptr %"%t5", align 8
  %13 = load %deus.fat, ptr %self, align 8
  %14 = extractvalue %deus.fat %13, 0
  %15 = extractvalue %deus.fat %13, 1
  %16 = insertvalue %deus.fat undef, ptr %14, 0
  %17 = insertvalue %deus.fat %16, i64 %15, 1
  store %deus.fat %17, ptr %"%t8", align 8
  %18 = load %deus.fat, ptr %"%t8", align 8
  %19 = extractvalue %deus.fat %18, 0
  %20 = extractvalue %deus.fat %18, 1
  store i64 %20, ptr %"%t7", align 8
  br label %bb6

bb4:                                              ; preds = %bb7, %bb2
  br label %bb1

bb5:                                              ; preds = %bb0
  %21 = load i1, ptr %"%t2", align 1
  %22 = zext i1 %21 to i32
  switch i32 %22, label %bb3 [
    i32 1, label %bb2
  ]

bb6:                                              ; preds = %bb3
  %23 = load i64, ptr %"%t7", align 8
  %24 = call { i64, i1 } @llvm.usub.with.overflow.i64(i64 %23, i64 1)
  %25 = extractvalue { i64, i1 } %24, 0
  %26 = extractvalue { i64, i1 } %24, 1
  %27 = xor i1 %26, true
  br i1 %27, label %ok, label %fail

bb7:                                              ; preds = %ok
  %28 = load %deus.fat, ptr %self, align 8
  %29 = extractvalue %deus.fat %28, 0
  %30 = extractvalue %deus.fat %28, 1
  %31 = load i64, ptr %"%t6", align 8
  %32 = getelementptr inbounds i8, ptr %29, i64 %31
  store ptr %32, ptr %"%t4", align 8
  %33 = load ptr, ptr %"%t4", align 8
  %34 = insertvalue %Option.3 undef, ptr %33, 0
  store %Option.3 %34, ptr %_0, align 8
  br label %bb4

fail:                                             ; preds = %bb6
  call void @deus_panic_at(ptr @panic.27, i64 33, ptr @loc.31) #2
  unreachable

ok:                                               ; preds = %bb6
  store i64 %25, ptr %"%t6", align 8
  %35 = load i64, ptr %"%t6", align 8
  %36 = load i64, ptr %"%t5", align 8
  store i64 %35, ptr %a, align 8
  store i64 %36, ptr %b, align 8
  %37 = call i32 @cmp.usize(ptr %a, ptr %b)
  %38 = icmp slt i32 %37, 0
  store i1 %38, ptr %"%t9", align 1
  %39 = load i1, ptr %"%t9", align 1
  br i1 %39, label %bb7, label %assert.fail

dead:                                             ; No predecessors!
  unreachable

assert.fail:                                      ; preds = %ok
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.32) #2
  unreachable

dead1:                                            ; No predecessors!
  unreachable
}

define internal void @"drop.usize ! IoError"(ptr %0) #0 {
entry:
  %1 = load %Result.2, ptr %0, align 8
  %2 = extractvalue %Result.2 %1, 0
  switch i32 %2, label %done [
    i32 1, label %variant
  ]

done:                                             ; preds = %variant, %entry
  ret void

variant:                                          ; preds = %entry
  %3 = getelementptr inbounds nuw %Result.2, ptr %0, i32 0, i32 1
  %4 = getelementptr inbounds nuw { %IoError }, ptr %3, i32 0, i32 0
  call void @drop.IoError(ptr %4)
  br label %done
}

define internal i1 @deus.is_empty.T_u8(%deus.fat %0) #0 {
entry:
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %"%t3" = alloca %deus.fat, align 8
  %"%t2" = alloca i64, align 8
  %self = alloca %deus.fat, align 8
  %_0 = alloca i1, align 1
  %1 = freeze %deus.fat %0
  store %deus.fat %1, ptr %self, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load %deus.fat, ptr %self, align 8
  %3 = extractvalue %deus.fat %2, 0
  %4 = extractvalue %deus.fat %2, 1
  %5 = insertvalue %deus.fat undef, ptr %3, 0
  %6 = insertvalue %deus.fat %5, i64 %4, 1
  store %deus.fat %6, ptr %"%t3", align 8
  %7 = load %deus.fat, ptr %"%t3", align 8
  %8 = extractvalue %deus.fat %7, 0
  %9 = extractvalue %deus.fat %7, 1
  store i64 %9, ptr %"%t2", align 8
  br label %bb2

bb1:                                              ; preds = %bb2
  %10 = load i1, ptr %_0, align 1
  ret i1 %10

bb2:                                              ; preds = %bb0
  %11 = load i64, ptr %"%t2", align 8
  store i64 %11, ptr %a, align 8
  store i64 0, ptr %b, align 8
  %12 = call i32 @cmp.usize(ptr %a, ptr %b)
  %13 = icmp eq i32 %12, 0
  store i1 %13, ptr %_0, align 1
  br label %bb1
}

define internal %IoError @deus.new(%ErrorKind %0, %deus.fat %1) #0 {
entry:
  %variant = alloca %Option, align 8
  %"%t4" = alloca %deus.vec, align 8
  %"%t3" = alloca %Option, align 8
  %message = alloca %deus.fat, align 8
  %kind = alloca %ErrorKind, align 8
  %_0 = alloca %IoError, align 8
  %2 = freeze %ErrorKind %0
  store %ErrorKind %2, ptr %kind, align 4
  %3 = freeze %deus.fat %1
  store %deus.fat %3, ptr %message, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  call void @llvm.memset.p0.i64(ptr align 4 %variant, i8 0, i64 8, i1 false)
  %4 = getelementptr inbounds nuw %Option, ptr %variant, i32 0, i32 0
  store i32 0, ptr %4, align 4
  %5 = load %Option, ptr %variant, align 4
  store %Option %5, ptr %"%t3", align 4
  %6 = load %deus.fat, ptr %message, align 8
  %7 = call %deus.vec @deus.into.Self__str_T_String(%deus.fat %6)
  store %deus.vec %7, ptr %"%t4", align 8
  br label %bb2

bb1:                                              ; preds = %bb2
  %8 = load %IoError, ptr %_0, align 8
  ret %IoError %8

bb2:                                              ; preds = %bb0
  %9 = load %ErrorKind, ptr %kind, align 4
  %10 = insertvalue %IoError undef, %ErrorKind %9, 1
  %11 = load %Option, ptr %"%t3", align 4
  %12 = insertvalue %IoError %10, %Option %11, 2
  %13 = load %deus.vec, ptr %"%t4", align 8
  %14 = insertvalue %IoError %12, %deus.vec %13, 0
  store %IoError %14, ptr %_0, align 8
  br label %bb1
}

declare i1 @deus_vec_pop(ptr, ptr, i64)

define internal %deus.vec @deus.from_utf8_lossy(%deus.fat %0) #0 {
entry:
  %b21 = alloca i64, align 8
  %a20 = alloca i64, align 8
  %b19 = alloca i64, align 8
  %a18 = alloca i64, align 8
  %b17 = alloca i8, align 1
  %a16 = alloca i8, align 1
  %b15 = alloca i64, align 8
  %a14 = alloca i64, align 8
  %b11 = alloca i64, align 8
  %a10 = alloca i64, align 8
  %b3 = alloca i64, align 8
  %a2 = alloca i64, align 8
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %s1 = alloca %deus.vec, align 8
  %"%t54" = alloca i1, align 1
  %"%t53" = alloca i1, align 1
  %"%t52" = alloca i1, align 1
  %"%t51" = alloca i64, align 8
  %"%t50" = alloca i64, align 8
  %"%t49" = alloca %deus.fat, align 8
  %"%t48" = alloca i64, align 8
  %"%t47" = alloca %Range, align 8
  %"%t46" = alloca i64, align 8
  %"%t45" = alloca %deus.fat, align 8
  %"%t44" = alloca %deus.unit, align 8
  %"%t43" = alloca i1, align 1
  %"%t42" = alloca i64, align 8
  %"%t41" = alloca i64, align 8
  %"%t40" = alloca i8, align 1
  %"%t39" = alloca %deus.fat, align 8
  %"%t38" = alloca i64, align 8
  %"%t37" = alloca i1, align 1
  %"%t36" = alloca i1, align 1
  %"%t35" = alloca %deus.unit, align 8
  %"%t34" = alloca %deus.unit, align 8
  %skip = alloca i64, align 8
  %"%t32" = alloca ptr, align 8
  %"%t31" = alloca ptr, align 8
  %"%t30" = alloca %deus.unit, align 8
  %"%t29" = alloca ptr, align 8
  %"%t28" = alloca ptr, align 8
  %"%t27" = alloca i1, align 1
  %"%t26" = alloca i1, align 1
  %"%t25" = alloca i1, align 1
  %"%t24" = alloca i64, align 8
  %"%t23" = alloca i64, align 8
  %"%t22" = alloca %Range, align 8
  %"%t21" = alloca i64, align 8
  %"%t20" = alloca %deus.fat, align 8
  %"%t19" = alloca %Result.5, align 8
  %"%t18" = alloca %deus.fat, align 8
  %"%t17" = alloca %deus.unit, align 8
  %"%t16" = alloca ptr, align 8
  %good = alloca i64, align 8
  %e = alloca %Utf8Error, align 8
  %"%t13" = alloca i32, align 4
  %"%t12" = alloca ptr, align 8
  %"%t11" = alloca ptr, align 8
  %"%t10" = alloca %deus.unit, align 8
  %"%t9" = alloca %deus.unit, align 8
  %s = alloca %deus.fat, align 8
  %"%t7" = alloca i32, align 4
  %"%t6" = alloca %Result.5, align 8
  %"%t5" = alloca %deus.unit, align 8
  %"%t4" = alloca %deus.unit, align 8
  %rest = alloca %deus.fat, align 8
  %r = alloca %deus.vec, align 8
  %bytes = alloca %deus.fat, align 8
  %_0 = alloca %deus.vec, align 8
  %1 = freeze %deus.fat %0
  store %deus.fat %1, ptr %bytes, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  call void @deus_string_init(ptr %s1)
  %2 = load %deus.vec, ptr %s1, align 8
  store %deus.vec %2, ptr %r, align 8
  br label %bb2

bb1:                                              ; preds = %bb9, %bb4
  %3 = load %deus.vec, ptr %_0, align 8
  ret %deus.vec %3

bb2:                                              ; preds = %bb0
  %4 = load %deus.fat, ptr %bytes, align 8
  store %deus.fat %4, ptr %rest, align 8
  br label %bb3

bb3:                                              ; preds = %bb6, %bb2
  %5 = load %deus.fat, ptr %rest, align 8
  %6 = call %Result.5 @deus.from_utf8(%deus.fat %5)
  store %Result.5 %6, ptr %"%t6", align 8
  br label %bb5

bb4:                                              ; No predecessors!
  br label %bb1

bb5:                                              ; preds = %bb3
  %7 = load %Result.5, ptr %"%t6", align 8
  %8 = extractvalue %Result.5 %7, 0
  store i32 %8, ptr %"%t7", align 4
  %9 = load i32, ptr %"%t7", align 4
  switch i32 %9, label %bb7 [
    i32 0, label %bb8
  ]

bb6:                                              ; preds = %bb31, %bb10
  br label %bb3

bb7:                                              ; preds = %bb5
  %10 = load %Result.5, ptr %"%t6", align 8
  %11 = extractvalue %Result.5 %10, 0
  store i32 %11, ptr %"%t13", align 4
  %12 = load i32, ptr %"%t13", align 4
  switch i32 %12, label %bb11 [
    i32 1, label %bb12
  ]

bb8:                                              ; preds = %bb5
  %13 = getelementptr inbounds nuw %Result.5, ptr %"%t6", i32 0, i32 1
  %14 = getelementptr inbounds nuw { %deus.fat }, ptr %13, i32 0, i32 0
  %15 = load %deus.fat, ptr %14, align 8
  store %deus.fat %15, ptr %s, align 8
  store ptr %r, ptr %"%t11", align 8
  %16 = load ptr, ptr %"%t11", align 8
  store ptr %16, ptr %"%t12", align 8
  %17 = load ptr, ptr %"%t12", align 8
  %18 = load %deus.fat, ptr %s, align 8
  %19 = load %deus.vec, ptr %17, align 8
  %20 = extractvalue %deus.vec %19, 0
  %21 = icmp eq ptr %20, null
  %buf = select i1 %21, ptr inttoptr (i64 1 to ptr), ptr %20
  %22 = extractvalue %deus.vec %19, 1
  %23 = extractvalue %deus.fat %18, 0
  %24 = extractvalue %deus.fat %18, 1
  call void @deus_string_push_str(ptr %17, ptr %23, i64 %24)
  br label %bb9

bb9:                                              ; preds = %bb8
  %25 = load %deus.vec, ptr %r, align 8
  store %deus.vec %25, ptr %_0, align 8
  br label %bb1

bb10:                                             ; No predecessors!
  br label %bb6

bb11:                                             ; preds = %bb7
  unreachable

bb12:                                             ; preds = %bb7
  %26 = getelementptr inbounds nuw %Result.5, ptr %"%t6", i32 0, i32 1
  %27 = getelementptr inbounds nuw { %Utf8Error }, ptr %26, i32 0, i32 0
  %28 = load %Utf8Error, ptr %27, align 8
  store %Utf8Error %28, ptr %e, align 8
  store ptr %e, ptr %"%t16", align 8
  %29 = load ptr, ptr %"%t16", align 8
  %30 = call i64 @deus.valid_up_to(ptr %29)
  store i64 %30, ptr %good, align 8
  br label %bb13

bb13:                                             ; preds = %bb12
  %31 = load %deus.fat, ptr %rest, align 8
  %32 = extractvalue %deus.fat %31, 0
  %33 = extractvalue %deus.fat %31, 1
  store i64 %33, ptr %"%t21", align 8
  %34 = load i64, ptr %good, align 8
  %35 = insertvalue %Range { i64 0, i64 undef }, i64 %34, 1
  store %Range %35, ptr %"%t22", align 8
  %36 = getelementptr inbounds nuw %Range, ptr %"%t22", i32 0, i32 0
  %37 = load i64, ptr %36, align 8
  store i64 %37, ptr %"%t23", align 8
  %38 = getelementptr inbounds nuw %Range, ptr %"%t22", i32 0, i32 1
  %39 = load i64, ptr %38, align 8
  store i64 %39, ptr %"%t24", align 8
  %40 = load i64, ptr %"%t23", align 8
  %41 = load i64, ptr %"%t24", align 8
  store i64 %40, ptr %a, align 8
  store i64 %41, ptr %b, align 8
  %42 = call i32 @cmp.usize(ptr %a, ptr %b)
  %43 = icmp sle i32 %42, 0
  store i1 %43, ptr %"%t25", align 1
  %44 = load i64, ptr %"%t24", align 8
  %45 = load i64, ptr %"%t21", align 8
  store i64 %44, ptr %a2, align 8
  store i64 %45, ptr %b3, align 8
  %46 = call i32 @cmp.usize(ptr %a2, ptr %b3)
  %47 = icmp sle i32 %46, 0
  store i1 %47, ptr %"%t26", align 1
  %48 = load i1, ptr %"%t25", align 1
  %49 = load i1, ptr %"%t26", align 1
  %50 = and i1 %48, %49
  store i1 %50, ptr %"%t27", align 1
  %51 = load i1, ptr %"%t27", align 1
  br i1 %51, label %bb14, label %assert.fail

bb14:                                             ; preds = %bb13
  %52 = load %deus.fat, ptr %rest, align 8
  %53 = extractvalue %deus.fat %52, 0
  %54 = extractvalue %deus.fat %52, 1
  %55 = load i64, ptr %"%t23", align 8
  %56 = load i64, ptr %"%t24", align 8
  %57 = getelementptr inbounds i8, ptr %53, i64 %55
  %58 = sub i64 %56, %55
  %59 = insertvalue %deus.fat undef, ptr %57, 0
  %60 = insertvalue %deus.fat %59, i64 %58, 1
  store %deus.fat %60, ptr %"%t20", align 8
  %61 = load %deus.fat, ptr %"%t20", align 8
  %62 = call %Result.5 @deus.from_utf8(%deus.fat %61)
  store %Result.5 %62, ptr %"%t19", align 8
  br label %bb15

bb15:                                             ; preds = %bb14
  %63 = load %Result.5, ptr %"%t19", align 8
  %64 = call %deus.fat @deus.unwrap.E_Utf8Error_T__str(%Result.5 %63, ptr @loc.36)
  store %deus.fat %64, ptr %"%t18", align 8
  br label %bb16

bb16:                                             ; preds = %bb15
  store ptr %r, ptr %"%t28", align 8
  %65 = load ptr, ptr %"%t28", align 8
  store ptr %65, ptr %"%t29", align 8
  %66 = load ptr, ptr %"%t29", align 8
  %67 = load %deus.fat, ptr %"%t18", align 8
  %68 = load %deus.vec, ptr %66, align 8
  %69 = extractvalue %deus.vec %68, 0
  %70 = icmp eq ptr %69, null
  %buf4 = select i1 %70, ptr inttoptr (i64 1 to ptr), ptr %69
  %71 = extractvalue %deus.vec %68, 1
  %72 = extractvalue %deus.fat %67, 0
  %73 = extractvalue %deus.fat %67, 1
  call void @deus_string_push_str(ptr %66, ptr %72, i64 %73)
  br label %bb17

bb17:                                             ; preds = %bb16
  store ptr %r, ptr %"%t31", align 8
  %74 = load ptr, ptr %"%t31", align 8
  store ptr %74, ptr %"%t32", align 8
  %75 = load ptr, ptr %"%t32", align 8
  %76 = load %deus.vec, ptr %75, align 8
  %77 = extractvalue %deus.vec %76, 0
  %78 = icmp eq ptr %77, null
  %buf5 = select i1 %78, ptr inttoptr (i64 1 to ptr), ptr %77
  %79 = extractvalue %deus.vec %76, 1
  call void @deus_string_push_char(ptr %75, i32 65533)
  br label %bb18

bb18:                                             ; preds = %bb17
  %80 = load i64, ptr %good, align 8
  %81 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %80, i64 1)
  %82 = extractvalue { i64, i1 } %81, 0
  %83 = extractvalue { i64, i1 } %81, 1
  %84 = xor i1 %83, true
  br i1 %84, label %ok, label %fail

bb19:                                             ; preds = %bb23, %ok
  %85 = load %deus.fat, ptr %rest, align 8
  %86 = extractvalue %deus.fat %85, 0
  %87 = extractvalue %deus.fat %85, 1
  %88 = insertvalue %deus.fat undef, ptr %86, 0
  %89 = insertvalue %deus.fat %88, i64 %87, 1
  store %deus.fat %89, ptr %"%t39", align 8
  %90 = load %deus.fat, ptr %"%t39", align 8
  %91 = extractvalue %deus.fat %90, 0
  %92 = extractvalue %deus.fat %90, 1
  store i64 %92, ptr %"%t38", align 8
  br label %bb27

bb20:                                             ; preds = %bb22
  %93 = load %deus.fat, ptr %rest, align 8
  %94 = extractvalue %deus.fat %93, 0
  %95 = extractvalue %deus.fat %93, 1
  store i64 %95, ptr %"%t46", align 8
  %96 = load %deus.fat, ptr %rest, align 8
  %97 = extractvalue %deus.fat %96, 0
  %98 = extractvalue %deus.fat %96, 1
  %99 = insertvalue %deus.fat undef, ptr %97, 0
  %100 = insertvalue %deus.fat %99, i64 %98, 1
  store %deus.fat %100, ptr %"%t49", align 8
  %101 = load %deus.fat, ptr %"%t49", align 8
  %102 = extractvalue %deus.fat %101, 0
  %103 = extractvalue %deus.fat %101, 1
  store i64 %103, ptr %"%t48", align 8
  br label %bb30

bb21:                                             ; preds = %bb26
  %104 = load i64, ptr %skip, align 8
  %105 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %104, i64 1)
  %106 = extractvalue { i64, i1 } %105, 0
  %107 = extractvalue { i64, i1 } %105, 1
  %108 = xor i1 %107, true
  br i1 %108, label %ok8, label %fail7

bb22:                                             ; preds = %bb26
  br label %bb20

bb23:                                             ; preds = %bb29, %ok8
  br label %bb19

bb24:                                             ; preds = %bb27
  %109 = load %deus.fat, ptr %rest, align 8
  %110 = extractvalue %deus.fat %109, 0
  %111 = extractvalue %deus.fat %109, 1
  store i64 %111, ptr %"%t41", align 8
  %112 = load i64, ptr %skip, align 8
  store i64 %112, ptr %"%t42", align 8
  %113 = load i64, ptr %"%t42", align 8
  %114 = load i64, ptr %"%t41", align 8
  store i64 %113, ptr %a10, align 8
  store i64 %114, ptr %b11, align 8
  %115 = call i32 @cmp.usize(ptr %a10, ptr %b11)
  %116 = icmp slt i32 %115, 0
  store i1 %116, ptr %"%t43", align 1
  %117 = load i1, ptr %"%t43", align 1
  br i1 %117, label %bb28, label %assert.fail12

bb25:                                             ; preds = %bb27
  store i1 false, ptr %"%t36", align 1
  br label %bb26

bb26:                                             ; preds = %bb28, %bb25
  %118 = load i1, ptr %"%t36", align 1
  %119 = zext i1 %118 to i32
  switch i32 %119, label %bb22 [
    i32 1, label %bb21
  ]

bb27:                                             ; preds = %bb19
  %120 = load i64, ptr %skip, align 8
  %121 = load i64, ptr %"%t38", align 8
  store i64 %120, ptr %a14, align 8
  store i64 %121, ptr %b15, align 8
  %122 = call i32 @cmp.usize(ptr %a14, ptr %b15)
  %123 = icmp slt i32 %122, 0
  store i1 %123, ptr %"%t37", align 1
  %124 = load i1, ptr %"%t37", align 1
  %125 = zext i1 %124 to i32
  switch i32 %125, label %bb25 [
    i32 1, label %bb24
  ]

bb28:                                             ; preds = %bb24
  %126 = load %deus.fat, ptr %rest, align 8
  %127 = extractvalue %deus.fat %126, 0
  %128 = extractvalue %deus.fat %126, 1
  %129 = load i64, ptr %"%t42", align 8
  %130 = getelementptr inbounds i8, ptr %127, i64 %129
  %131 = load i8, ptr %130, align 1
  %132 = and i8 %131, -64
  store i8 %132, ptr %"%t40", align 1
  %133 = load i8, ptr %"%t40", align 1
  store i8 %133, ptr %a16, align 1
  store i8 -128, ptr %b17, align 1
  %134 = call i32 @cmp.u8(ptr %a16, ptr %b17)
  %135 = icmp eq i32 %134, 0
  store i1 %135, ptr %"%t36", align 1
  br label %bb26

bb29:                                             ; No predecessors!
  br label %bb23

bb30:                                             ; preds = %bb20
  %136 = load i64, ptr %skip, align 8
  %137 = insertvalue %Range undef, i64 %136, 0
  %138 = load i64, ptr %"%t48", align 8
  %139 = insertvalue %Range %137, i64 %138, 1
  store %Range %139, ptr %"%t47", align 8
  %140 = getelementptr inbounds nuw %Range, ptr %"%t47", i32 0, i32 0
  %141 = load i64, ptr %140, align 8
  store i64 %141, ptr %"%t50", align 8
  %142 = getelementptr inbounds nuw %Range, ptr %"%t47", i32 0, i32 1
  %143 = load i64, ptr %142, align 8
  store i64 %143, ptr %"%t51", align 8
  %144 = load i64, ptr %"%t50", align 8
  %145 = load i64, ptr %"%t51", align 8
  store i64 %144, ptr %a18, align 8
  store i64 %145, ptr %b19, align 8
  %146 = call i32 @cmp.usize(ptr %a18, ptr %b19)
  %147 = icmp sle i32 %146, 0
  store i1 %147, ptr %"%t52", align 1
  %148 = load i64, ptr %"%t51", align 8
  %149 = load i64, ptr %"%t46", align 8
  store i64 %148, ptr %a20, align 8
  store i64 %149, ptr %b21, align 8
  %150 = call i32 @cmp.usize(ptr %a20, ptr %b21)
  %151 = icmp sle i32 %150, 0
  store i1 %151, ptr %"%t53", align 1
  %152 = load i1, ptr %"%t52", align 1
  %153 = load i1, ptr %"%t53", align 1
  %154 = and i1 %152, %153
  store i1 %154, ptr %"%t54", align 1
  %155 = load i1, ptr %"%t54", align 1
  br i1 %155, label %bb31, label %assert.fail22

bb31:                                             ; preds = %bb30
  %156 = load %deus.fat, ptr %rest, align 8
  %157 = extractvalue %deus.fat %156, 0
  %158 = extractvalue %deus.fat %156, 1
  %159 = load i64, ptr %"%t50", align 8
  %160 = load i64, ptr %"%t51", align 8
  %161 = getelementptr inbounds i8, ptr %157, i64 %159
  %162 = sub i64 %160, %159
  %163 = insertvalue %deus.fat undef, ptr %161, 0
  %164 = insertvalue %deus.fat %163, i64 %162, 1
  store %deus.fat %164, ptr %"%t45", align 8
  %165 = load %deus.fat, ptr %"%t45", align 8
  store %deus.fat %165, ptr %rest, align 8
  br label %bb6

assert.fail:                                      ; preds = %bb13
  call void @deus_panic_at(ptr @panic.33, i64 19, ptr @loc.35) #2
  unreachable

dead:                                             ; No predecessors!
  unreachable

fail:                                             ; preds = %bb18
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.37) #2
  unreachable

ok:                                               ; preds = %bb18
  store i64 %82, ptr %skip, align 8
  br label %bb19

dead6:                                            ; No predecessors!
  unreachable

fail7:                                            ; preds = %bb21
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.38) #2
  unreachable

ok8:                                              ; preds = %bb21
  store i64 %106, ptr %skip, align 8
  br label %bb23

dead9:                                            ; No predecessors!
  unreachable

assert.fail12:                                    ; preds = %bb24
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.39) #2
  unreachable

dead13:                                           ; No predecessors!
  unreachable

assert.fail22:                                    ; preds = %bb30
  call void @deus_panic_at(ptr @panic.33, i64 19, ptr @loc.40) #2
  unreachable

dead23:                                           ; No predecessors!
  unreachable
}

declare i1 @deus_iter_next(ptr, ptr)

define internal void @"drop.Iter[u8]"(ptr %0) #0 {
entry:
  %1 = load ptr, ptr %0, align 8
  call void @deus_iter_free(ptr %1)
  ret void
}

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i64, i1 } @llvm.uadd.with.overflow.i64(i64, i64) #3

define internal i32 @deus.unwrap.T_u32(%Option.4 %0, ptr %1) #0 {
entry:
  %"%t6" = alloca %deus.unit, align 8
  %"%t5" = alloca %deus.unit, align 8
  %"%t4" = alloca i32, align 4
  %x = alloca i32, align 4
  %"%t2" = alloca i32, align 4
  %self = alloca %Option.4, align 8
  %_0 = alloca i32, align 4
  %2 = freeze %Option.4 %0
  store %Option.4 %2, ptr %self, align 4
  br label %bb0

bb0:                                              ; preds = %entry
  %3 = load %Option.4, ptr %self, align 4
  %4 = extractvalue %Option.4 %3, 0
  store i32 %4, ptr %"%t2", align 4
  %5 = load i32, ptr %"%t2", align 4
  switch i32 %5, label %bb3 [
    i32 1, label %bb4
  ]

bb1:                                              ; preds = %bb2
  %6 = load i32, ptr %_0, align 4
  ret i32 %6

bb2:                                              ; preds = %bb7, %bb4
  br label %bb1

bb3:                                              ; preds = %bb0
  %7 = load %Option.4, ptr %self, align 4
  %8 = extractvalue %Option.4 %7, 0
  store i32 %8, ptr %"%t4", align 4
  %9 = load i32, ptr %"%t4", align 4
  switch i32 %9, label %bb5 [
    i32 0, label %bb6
  ]

bb4:                                              ; preds = %bb0
  %10 = getelementptr inbounds nuw %Option.4, ptr %self, i32 0, i32 1
  %11 = getelementptr inbounds nuw { i32 }, ptr %10, i32 0, i32 0
  %12 = load i32, ptr %11, align 4
  store i32 %12, ptr %x, align 4
  %13 = load i32, ptr %x, align 4
  store i32 %13, ptr %_0, align 4
  br label %bb2

bb5:                                              ; preds = %bb3
  unreachable

bb6:                                              ; preds = %bb3
  %14 = icmp eq ptr %1, null
  %15 = select i1 %14, ptr @loc.18, ptr %1
  call void @deus_panic_at(ptr @str.16, i64 42, ptr %15) #2
  unreachable

bb7:                                              ; No predecessors!
  br label %bb2

dead:                                             ; No predecessors!
  unreachable
}

define internal i8 @deus.ror8(i8 %0, i32 %1) #0 {
entry:
  %"%t8" = alloca i32, align 4
  %"%t7" = alloca i32, align 4
  %"%t6" = alloca i8, align 1
  %"%t5" = alloca i8, align 1
  %"%t4" = alloca %deus.unit, align 8
  %"%t3" = alloca %deus.unit, align 8
  %n = alloca i32, align 4
  %x = alloca i8, align 1
  %_0 = alloca i8, align 1
  store i8 %0, ptr %x, align 1
  store i32 %1, ptr %n, align 4
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load i32, ptr %n, align 4
  %3 = and i32 %2, 7
  store i32 %3, ptr %n, align 4
  %4 = load i8, ptr %x, align 1
  %5 = load i32, ptr %n, align 4
  %6 = trunc i32 %5 to i8
  %7 = icmp ult i8 %6, 8
  br i1 %7, label %ok, label %fail

bb1:                                              ; preds = %bb2, %ok5
  %8 = load i8, ptr %_0, align 1
  ret i8 %8

bb2:                                              ; No predecessors!
  br label %bb1

fail:                                             ; preds = %bb0
  call void @deus_panic_at(ptr @panic.23, i64 30, ptr @loc.41) #2
  unreachable

ok:                                               ; preds = %bb0
  %9 = lshr i8 %4, %6
  store i8 %9, ptr %"%t5", align 1
  %10 = load i32, ptr %n, align 4
  %11 = call { i32, i1 } @llvm.usub.with.overflow.i32(i32 8, i32 %10)
  %12 = extractvalue { i32, i1 } %11, 0
  %13 = extractvalue { i32, i1 } %11, 1
  %14 = xor i1 %13, true
  br i1 %14, label %ok2, label %fail1

dead:                                             ; No predecessors!
  unreachable

fail1:                                            ; preds = %ok
  call void @deus_panic_at(ptr @panic.27, i64 33, ptr @loc.42) #2
  unreachable

ok2:                                              ; preds = %ok
  store i32 %12, ptr %"%t8", align 4
  %15 = load i32, ptr %"%t8", align 4
  %16 = and i32 %15, 7
  store i32 %16, ptr %"%t7", align 4
  %17 = load i8, ptr %x, align 1
  %18 = load i32, ptr %"%t7", align 4
  %19 = trunc i32 %18 to i8
  %20 = icmp ult i8 %19, 8
  br i1 %20, label %ok5, label %fail4

dead3:                                            ; No predecessors!
  unreachable

fail4:                                            ; preds = %ok2
  call void @deus_panic_at(ptr @panic.23, i64 30, ptr @loc.43) #2
  unreachable

ok5:                                              ; preds = %ok2
  %21 = shl i8 %17, %19
  store i8 %21, ptr %"%t6", align 1
  %22 = load i8, ptr %"%t5", align 1
  %23 = load i8, ptr %"%t6", align 1
  %24 = or i8 %22, %23
  store i8 %24, ptr %_0, align 1
  br label %bb1

dead6:                                            ; No predecessors!
  unreachable
}

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i32, i1 } @llvm.usub.with.overflow.i32(i32, i32) #3

declare i64 @read(i32, ptr, i64)

define internal %Result.2 @deus.check(i64 %0) #0 {
entry:
  %variant1 = alloca %Result.2, align 8
  %variant = alloca %Result.2, align 8
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %"%t4" = alloca i64, align 8
  %"%t3" = alloca %IoError, align 8
  %"%t2" = alloca i1, align 1
  %r = alloca i64, align 8
  %_0 = alloca %Result.2, align 8
  store i64 %0, ptr %r, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %1 = load i64, ptr %r, align 8
  store i64 %1, ptr %a, align 8
  store i64 0, ptr %b, align 8
  %2 = call i32 @cmp.isize(ptr %a, ptr %b)
  %3 = icmp slt i32 %2, 0
  store i1 %3, ptr %"%t2", align 1
  %4 = load i1, ptr %"%t2", align 1
  %5 = zext i1 %4 to i32
  switch i32 %5, label %bb3 [
    i32 1, label %bb2
  ]

bb1:                                              ; preds = %bb4
  %6 = load %Result.2, ptr %_0, align 8
  ret %Result.2 %6

bb2:                                              ; preds = %bb0
  %7 = call %IoError @deus.last_os_error()
  store %IoError %7, ptr %"%t3", align 8
  br label %bb5

bb3:                                              ; preds = %bb0
  %8 = load i64, ptr %r, align 8
  store i64 %8, ptr %"%t4", align 8
  br label %bb6

bb4:                                              ; preds = %bb6, %bb5
  br label %bb1

bb5:                                              ; preds = %bb2
  %9 = load %IoError, ptr %"%t3", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant, i8 0, i64 48, i1 false)
  %10 = getelementptr inbounds nuw %Result.2, ptr %variant, i32 0, i32 0
  store i32 1, ptr %10, align 4
  %11 = getelementptr inbounds nuw %Result.2, ptr %variant, i32 0, i32 1
  %12 = getelementptr inbounds nuw { %IoError }, ptr %11, i32 0, i32 0
  store %IoError %9, ptr %12, align 8
  %13 = load %Result.2, ptr %variant, align 8
  store %Result.2 %13, ptr %_0, align 8
  br label %bb4

bb6:                                              ; preds = %bb3
  %14 = load i64, ptr %"%t4", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant1, i8 0, i64 48, i1 false)
  %15 = getelementptr inbounds nuw %Result.2, ptr %variant1, i32 0, i32 0
  store i32 0, ptr %15, align 4
  %16 = getelementptr inbounds nuw %Result.2, ptr %variant1, i32 0, i32 1
  %17 = getelementptr inbounds nuw { i64 }, ptr %16, i32 0, i32 0
  store i64 %14, ptr %17, align 8
  %18 = load %Result.2, ptr %variant1, align 8
  store %Result.2 %18, ptr %_0, align 8
  br label %bb4
}

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i64, i1 } @llvm.usub.with.overflow.i64(i64, i64) #3

define internal %deus.vec @deus.into.Self__str_T_String(%deus.fat %0) #0 {
entry:
  %self = alloca %deus.fat, align 8
  %_0 = alloca %deus.vec, align 8
  %1 = freeze %deus.fat %0
  store %deus.fat %1, ptr %self, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load %deus.fat, ptr %self, align 8
  %3 = call %deus.vec @deus.from(%deus.fat %2)
  store %deus.vec %3, ptr %_0, align 8
  br label %bb2

bb1:                                              ; preds = %bb2
  %4 = load %deus.vec, ptr %_0, align 8
  ret %deus.vec %4

bb2:                                              ; preds = %bb0
  br label %bb1
}

declare void @deus_string_init(ptr)

define internal %Result.5 @deus.from_utf8(%deus.fat %0) #0 {
entry:
  %variant63 = alloca %Result.5, align 8
  %b62 = alloca i8, align 1
  %a61 = alloca i8, align 1
  %b60 = alloca i8, align 1
  %a59 = alloca i8, align 1
  %b58 = alloca i8, align 1
  %a57 = alloca i8, align 1
  %b56 = alloca i8, align 1
  %a55 = alloca i8, align 1
  %b54 = alloca i8, align 1
  %a53 = alloca i8, align 1
  %b52 = alloca i8, align 1
  %a51 = alloca i8, align 1
  %b50 = alloca i8, align 1
  %a49 = alloca i8, align 1
  %variant45 = alloca %Result.5, align 8
  %b44 = alloca i8, align 1
  %a43 = alloca i8, align 1
  %b40 = alloca i64, align 8
  %a39 = alloca i64, align 8
  %b35 = alloca i8, align 1
  %a34 = alloca i8, align 1
  %variant33 = alloca %Result.5, align 8
  %b32 = alloca i64, align 8
  %a31 = alloca i64, align 8
  %b28 = alloca i64, align 8
  %a27 = alloca i64, align 8
  %b23 = alloca i64, align 8
  %a22 = alloca i64, align 8
  %b21 = alloca i64, align 8
  %a20 = alloca i64, align 8
  %variant = alloca %Result.5, align 8
  %b18 = alloca i8, align 1
  %a17 = alloca i8, align 1
  %b16 = alloca i8, align 1
  %a15 = alloca i8, align 1
  %b14 = alloca i8, align 1
  %a13 = alloca i8, align 1
  %b12 = alloca i8, align 1
  %a11 = alloca i8, align 1
  %b10 = alloca i64, align 8
  %a9 = alloca i64, align 8
  %b8 = alloca i8, align 1
  %a7 = alloca i8, align 1
  %b6 = alloca i8, align 1
  %a5 = alloca i8, align 1
  %b4 = alloca i64, align 8
  %a3 = alloca i64, align 8
  %b2 = alloca i64, align 8
  %a = alloca i64, align 8
  %"%t60" = alloca %deus.fat, align 8
  %"%t59" = alloca %deus.unit, align 8
  %"%t58" = alloca %Utf8Error, align 8
  %"%t57" = alloca %deus.unit, align 8
  %"%t56" = alloca i1, align 1
  %"%t55" = alloca i1, align 1
  %"%t54" = alloca i1, align 1
  %"%t53" = alloca i1, align 1
  %"%t52" = alloca i1, align 1
  %"%t51" = alloca i1, align 1
  %"%t50" = alloca i1, align 1
  %"%t49" = alloca i1, align 1
  %"%t48" = alloca %deus.unit, align 8
  %"%t47" = alloca i1, align 1
  %"%t46" = alloca i64, align 8
  %"%t45" = alloca i64, align 8
  %"%t44" = alloca i1, align 1
  %b1 = alloca i8, align 1
  %"%t42" = alloca %Utf8Error, align 8
  %"%t41" = alloca %deus.unit, align 8
  %"%t40" = alloca i1, align 1
  %"%t39" = alloca i64, align 8
  %"%t38" = alloca i64, align 8
  %"%t37" = alloca i8, align 1
  %"%t36" = alloca i1, align 1
  %"%t35" = alloca %deus.unit, align 8
  %k = alloca i64, align 8
  %"%t33" = alloca i1, align 1
  %"%t32" = alloca i64, align 8
  %"%t31" = alloca i64, align 8
  %"%t30" = alloca i64, align 8
  %"%t29" = alloca %Range, align 8
  %"%t28" = alloca %deus.unit, align 8
  %"%t27" = alloca %Utf8Error, align 8
  %"%t26" = alloca %deus.unit, align 8
  %"%t25" = alloca i64, align 8
  %"%t24" = alloca i1, align 1
  %"%t23" = alloca i1, align 1
  %"%t22" = alloca %deus.unit, align 8
  %"%t21" = alloca i8, align 1
  %"%t20" = alloca i1, align 1
  %"%t19" = alloca i1, align 1
  %"%t18" = alloca i8, align 1
  %"%t17" = alloca i1, align 1
  %"%t16" = alloca i8, align 1
  %"%t15" = alloca i1, align 1
  %"%t14" = alloca i1, align 1
  %"%t13" = alloca i1, align 1
  %w = alloca i64, align 8
  %"%t11" = alloca i1, align 1
  %"%t10" = alloca i64, align 8
  %"%t9" = alloca i64, align 8
  %b = alloca i8, align 1
  %"%t7" = alloca i1, align 1
  %"%t6" = alloca %deus.unit, align 8
  %"%t5" = alloca %deus.unit, align 8
  %i = alloca i64, align 8
  %"%t3" = alloca %deus.fat, align 8
  %n = alloca i64, align 8
  %bytes = alloca %deus.fat, align 8
  %_0 = alloca %Result.5, align 8
  %1 = freeze %deus.fat %0
  store %deus.fat %1, ptr %bytes, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load %deus.fat, ptr %bytes, align 8
  %3 = extractvalue %deus.fat %2, 0
  %4 = extractvalue %deus.fat %2, 1
  %5 = insertvalue %deus.fat undef, ptr %3, 0
  %6 = insertvalue %deus.fat %5, i64 %4, 1
  store %deus.fat %6, ptr %"%t3", align 8
  %7 = load %deus.fat, ptr %"%t3", align 8
  %8 = extractvalue %deus.fat %7, 0
  %9 = extractvalue %deus.fat %7, 1
  store i64 %9, ptr %n, align 8
  br label %bb2

bb1:                                              ; preds = %bb73, %bb47, %bb38, %bb27
  %10 = load %Result.5, ptr %_0, align 8
  ret %Result.5 %10

bb2:                                              ; preds = %bb0
  store i64 0, ptr %i, align 8
  br label %bb3

bb3:                                              ; preds = %bb7, %bb2
  %11 = load i64, ptr %i, align 8
  %12 = load i64, ptr %n, align 8
  store i64 %11, ptr %a, align 8
  store i64 %12, ptr %b2, align 8
  %13 = call i32 @cmp.usize(ptr %a, ptr %b2)
  %14 = icmp slt i32 %13, 0
  store i1 %14, ptr %"%t7", align 1
  %15 = load i1, ptr %"%t7", align 1
  %16 = zext i1 %15 to i32
  switch i32 %16, label %bb6 [
    i32 1, label %bb5
  ]

bb4:                                              ; preds = %bb6
  %17 = load %deus.fat, ptr %bytes, align 8
  store %deus.fat %17, ptr %"%t60", align 8
  br label %bb73

bb5:                                              ; preds = %bb3
  %18 = load %deus.fat, ptr %bytes, align 8
  %19 = extractvalue %deus.fat %18, 0
  %20 = extractvalue %deus.fat %18, 1
  store i64 %20, ptr %"%t9", align 8
  %21 = load i64, ptr %i, align 8
  store i64 %21, ptr %"%t10", align 8
  %22 = load i64, ptr %"%t10", align 8
  %23 = load i64, ptr %"%t9", align 8
  store i64 %22, ptr %a3, align 8
  store i64 %23, ptr %b4, align 8
  %24 = call i32 @cmp.usize(ptr %a3, ptr %b4)
  %25 = icmp slt i32 %24, 0
  store i1 %25, ptr %"%t11", align 1
  %26 = load i1, ptr %"%t11", align 1
  br i1 %26, label %bb8, label %assert.fail

bb6:                                              ; preds = %bb3
  br label %bb4

bb7:                                              ; preds = %bb72, %ok47
  br label %bb3

bb8:                                              ; preds = %bb5
  %27 = load %deus.fat, ptr %bytes, align 8
  %28 = extractvalue %deus.fat %27, 0
  %29 = extractvalue %deus.fat %27, 1
  %30 = load i64, ptr %"%t10", align 8
  %31 = getelementptr inbounds i8, ptr %28, i64 %30
  %32 = load i8, ptr %31, align 1
  store i8 %32, ptr %b, align 1
  %33 = load i8, ptr %b, align 1
  store i8 %33, ptr %a5, align 1
  store i8 -128, ptr %b6, align 1
  %34 = call i32 @cmp.u8(ptr %a5, ptr %b6)
  %35 = icmp slt i32 %34, 0
  store i1 %35, ptr %"%t13", align 1
  %36 = load i1, ptr %"%t13", align 1
  %37 = zext i1 %36 to i32
  switch i32 %37, label %bb10 [
    i32 1, label %bb9
  ]

bb9:                                              ; preds = %bb8
  store i64 1, ptr %w, align 8
  br label %bb11

bb10:                                             ; preds = %bb8
  %38 = load i8, ptr %b, align 1
  %39 = and i8 %38, -32
  store i8 %39, ptr %"%t16", align 1
  %40 = load i8, ptr %"%t16", align 1
  store i8 %40, ptr %a7, align 1
  store i8 -64, ptr %b8, align 1
  %41 = call i32 @cmp.u8(ptr %a7, ptr %b8)
  %42 = icmp eq i32 %41, 0
  store i1 %42, ptr %"%t15", align 1
  %43 = load i1, ptr %"%t15", align 1
  %44 = zext i1 %43 to i32
  switch i32 %44, label %bb16 [
    i32 1, label %bb15
  ]

bb11:                                             ; preds = %bb14, %bb9
  %45 = load i64, ptr %w, align 8
  store i64 %45, ptr %a9, align 8
  store i64 0, ptr %b10, align 8
  %46 = call i32 @cmp.usize(ptr %a9, ptr %b10)
  %47 = icmp eq i32 %46, 0
  store i1 %47, ptr %"%t24", align 1
  %48 = load i1, ptr %"%t24", align 1
  %49 = zext i1 %48 to i32
  switch i32 %49, label %bb30 [
    i32 1, label %bb31
  ]

bb12:                                             ; preds = %bb17
  store i64 2, ptr %w, align 8
  br label %bb14

bb13:                                             ; preds = %bb17
  %50 = load i8, ptr %b, align 1
  %51 = and i8 %50, -16
  store i8 %51, ptr %"%t18", align 1
  %52 = load i8, ptr %"%t18", align 1
  store i8 %52, ptr %a11, align 1
  store i8 -32, ptr %b12, align 1
  %53 = call i32 @cmp.u8(ptr %a11, ptr %b12)
  %54 = icmp eq i32 %53, 0
  store i1 %54, ptr %"%t17", align 1
  %55 = load i1, ptr %"%t17", align 1
  %56 = zext i1 %55 to i32
  switch i32 %56, label %bb19 [
    i32 1, label %bb18
  ]

bb14:                                             ; preds = %bb20, %bb12
  br label %bb11

bb15:                                             ; preds = %bb10
  %57 = load i8, ptr %b, align 1
  store i8 %57, ptr %a13, align 1
  store i8 -62, ptr %b14, align 1
  %58 = call i32 @cmp.u8(ptr %a13, ptr %b14)
  %59 = icmp sge i32 %58, 0
  store i1 %59, ptr %"%t14", align 1
  br label %bb17

bb16:                                             ; preds = %bb10
  store i1 false, ptr %"%t14", align 1
  br label %bb17

bb17:                                             ; preds = %bb16, %bb15
  %60 = load i1, ptr %"%t14", align 1
  %61 = zext i1 %60 to i32
  switch i32 %61, label %bb13 [
    i32 1, label %bb12
  ]

bb18:                                             ; preds = %bb13
  store i64 3, ptr %w, align 8
  br label %bb20

bb19:                                             ; preds = %bb13
  %62 = load i8, ptr %b, align 1
  %63 = and i8 %62, -8
  store i8 %63, ptr %"%t21", align 1
  %64 = load i8, ptr %"%t21", align 1
  store i8 %64, ptr %a15, align 1
  store i8 -16, ptr %b16, align 1
  %65 = call i32 @cmp.u8(ptr %a15, ptr %b16)
  %66 = icmp eq i32 %65, 0
  store i1 %66, ptr %"%t20", align 1
  %67 = load i1, ptr %"%t20", align 1
  %68 = zext i1 %67 to i32
  switch i32 %68, label %bb25 [
    i32 1, label %bb24
  ]

bb20:                                             ; preds = %bb23, %bb18
  br label %bb14

bb21:                                             ; preds = %bb26
  store i64 4, ptr %w, align 8
  br label %bb23

bb22:                                             ; preds = %bb26
  store i64 0, ptr %w, align 8
  br label %bb23

bb23:                                             ; preds = %bb22, %bb21
  br label %bb20

bb24:                                             ; preds = %bb19
  %69 = load i8, ptr %b, align 1
  store i8 %69, ptr %a17, align 1
  store i8 -12, ptr %b18, align 1
  %70 = call i32 @cmp.u8(ptr %a17, ptr %b18)
  %71 = icmp sle i32 %70, 0
  store i1 %71, ptr %"%t19", align 1
  br label %bb26

bb25:                                             ; preds = %bb19
  store i1 false, ptr %"%t19", align 1
  br label %bb26

bb26:                                             ; preds = %bb25, %bb24
  %72 = load i1, ptr %"%t19", align 1
  %73 = zext i1 %72 to i32
  switch i32 %73, label %bb22 [
    i32 1, label %bb21
  ]

bb27:                                             ; preds = %bb32
  %74 = load i64, ptr %i, align 8
  %75 = insertvalue %Utf8Error undef, i64 %74, 0
  store %Utf8Error %75, ptr %"%t27", align 8
  %76 = load %Utf8Error, ptr %"%t27", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant, i8 0, i64 24, i1 false)
  %77 = getelementptr inbounds nuw %Result.5, ptr %variant, i32 0, i32 0
  store i32 1, ptr %77, align 4
  %78 = getelementptr inbounds nuw %Result.5, ptr %variant, i32 0, i32 1
  %79 = getelementptr inbounds nuw { %Utf8Error }, ptr %78, i32 0, i32 0
  store %Utf8Error %76, ptr %79, align 8
  %80 = load %Result.5, ptr %variant, align 8
  store %Result.5 %80, ptr %_0, align 8
  br label %bb1

bb28:                                             ; preds = %bb32
  br label %bb29

bb29:                                             ; preds = %bb33, %bb28
  %81 = load i64, ptr %w, align 8
  %82 = insertvalue %Range { i64 1, i64 undef }, i64 %81, 1
  store %Range %82, ptr %"%t29", align 8
  %83 = getelementptr inbounds nuw %Range, ptr %"%t29", i32 0, i32 0
  %84 = load i64, ptr %83, align 8
  store i64 %84, ptr %"%t30", align 8
  %85 = getelementptr inbounds nuw %Range, ptr %"%t29", i32 0, i32 1
  %86 = load i64, ptr %85, align 8
  store i64 %86, ptr %"%t31", align 8
  store i64 1, ptr %"%t32", align 8
  br label %bb34

bb30:                                             ; preds = %bb11
  %87 = load i64, ptr %i, align 8
  %88 = load i64, ptr %w, align 8
  %89 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %87, i64 %88)
  %90 = extractvalue { i64, i1 } %89, 0
  %91 = extractvalue { i64, i1 } %89, 1
  %92 = xor i1 %91, true
  br i1 %92, label %ok, label %fail

bb31:                                             ; preds = %bb11
  store i1 true, ptr %"%t23", align 1
  br label %bb32

bb32:                                             ; preds = %bb31, %ok
  %93 = load i1, ptr %"%t23", align 1
  %94 = zext i1 %93 to i32
  switch i32 %94, label %bb28 [
    i32 1, label %bb27
  ]

bb33:                                             ; No predecessors!
  br label %bb29

bb34:                                             ; preds = %bb36, %bb29
  %95 = load i64, ptr %"%t30", align 8
  %96 = load i64, ptr %"%t31", align 8
  store i64 %95, ptr %a22, align 8
  store i64 %96, ptr %b23, align 8
  %97 = call i32 @cmp.usize(ptr %a22, ptr %b23)
  %98 = icmp slt i32 %97, 0
  store i1 %98, ptr %"%t33", align 1
  %99 = load i1, ptr %"%t33", align 1
  %100 = zext i1 %99 to i32
  switch i32 %100, label %bb37 [
    i32 1, label %bb35
  ]

bb35:                                             ; preds = %bb34
  %101 = load i64, ptr %"%t30", align 8
  store i64 %101, ptr %k, align 8
  %102 = load %deus.fat, ptr %bytes, align 8
  %103 = extractvalue %deus.fat %102, 0
  %104 = extractvalue %deus.fat %102, 1
  store i64 %104, ptr %"%t38", align 8
  %105 = load i64, ptr %i, align 8
  %106 = load i64, ptr %k, align 8
  %107 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %105, i64 %106)
  %108 = extractvalue { i64, i1 } %107, 0
  %109 = extractvalue { i64, i1 } %107, 1
  %110 = xor i1 %109, true
  br i1 %110, label %ok25, label %fail24

bb36:                                             ; preds = %bb40
  %111 = load i64, ptr %"%t30", align 8
  %112 = load i64, ptr %"%t32", align 8
  %113 = add i64 %111, %112
  store i64 %113, ptr %"%t30", align 8
  br label %bb34

bb37:                                             ; preds = %bb34
  %114 = load i64, ptr %w, align 8
  store i64 %114, ptr %a31, align 8
  store i64 1, ptr %b32, align 8
  %115 = call i32 @cmp.usize(ptr %a31, ptr %b32)
  %116 = icmp sgt i32 %115, 0
  store i1 %116, ptr %"%t44", align 1
  %117 = load i1, ptr %"%t44", align 1
  %118 = zext i1 %117 to i32
  switch i32 %118, label %bb44 [
    i32 1, label %bb43
  ]

bb38:                                             ; preds = %bb41
  %119 = load i64, ptr %i, align 8
  %120 = insertvalue %Utf8Error undef, i64 %119, 0
  store %Utf8Error %120, ptr %"%t42", align 8
  %121 = load %Utf8Error, ptr %"%t42", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant33, i8 0, i64 24, i1 false)
  %122 = getelementptr inbounds nuw %Result.5, ptr %variant33, i32 0, i32 0
  store i32 1, ptr %122, align 4
  %123 = getelementptr inbounds nuw %Result.5, ptr %variant33, i32 0, i32 1
  %124 = getelementptr inbounds nuw { %Utf8Error }, ptr %123, i32 0, i32 0
  store %Utf8Error %121, ptr %124, align 8
  %125 = load %Result.5, ptr %variant33, align 8
  store %Result.5 %125, ptr %_0, align 8
  br label %bb1

bb39:                                             ; preds = %bb41
  br label %bb40

bb40:                                             ; preds = %bb42, %bb39
  br label %bb36

bb41:                                             ; preds = %ok25
  %126 = load %deus.fat, ptr %bytes, align 8
  %127 = extractvalue %deus.fat %126, 0
  %128 = extractvalue %deus.fat %126, 1
  %129 = load i64, ptr %"%t39", align 8
  %130 = getelementptr inbounds i8, ptr %127, i64 %129
  %131 = load i8, ptr %130, align 1
  %132 = and i8 %131, -64
  store i8 %132, ptr %"%t37", align 1
  %133 = load i8, ptr %"%t37", align 1
  store i8 %133, ptr %a34, align 1
  store i8 -128, ptr %b35, align 1
  %134 = call i32 @cmp.u8(ptr %a34, ptr %b35)
  %135 = icmp eq i32 %134, 0
  %136 = xor i1 %135, true
  store i1 %136, ptr %"%t36", align 1
  %137 = load i1, ptr %"%t36", align 1
  %138 = zext i1 %137 to i32
  switch i32 %138, label %bb39 [
    i32 1, label %bb38
  ]

bb42:                                             ; No predecessors!
  br label %bb40

bb43:                                             ; preds = %bb37
  %139 = load %deus.fat, ptr %bytes, align 8
  %140 = extractvalue %deus.fat %139, 0
  %141 = extractvalue %deus.fat %139, 1
  store i64 %141, ptr %"%t45", align 8
  %142 = load i64, ptr %i, align 8
  %143 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %142, i64 1)
  %144 = extractvalue { i64, i1 } %143, 0
  %145 = extractvalue { i64, i1 } %143, 1
  %146 = xor i1 %145, true
  br i1 %146, label %ok37, label %fail36

bb44:                                             ; preds = %bb37
  store i8 0, ptr %b1, align 1
  br label %bb45

bb45:                                             ; preds = %bb46, %bb44
  %147 = load i8, ptr %b, align 1
  store i8 %147, ptr %a43, align 1
  store i8 -32, ptr %b44, align 1
  %148 = call i32 @cmp.u8(ptr %a43, ptr %b44)
  %149 = icmp eq i32 %148, 0
  store i1 %149, ptr %"%t53", align 1
  %150 = load i1, ptr %"%t53", align 1
  %151 = zext i1 %150 to i32
  switch i32 %151, label %bb60 [
    i32 1, label %bb59
  ]

bb46:                                             ; preds = %ok37
  %152 = load %deus.fat, ptr %bytes, align 8
  %153 = extractvalue %deus.fat %152, 0
  %154 = extractvalue %deus.fat %152, 1
  %155 = load i64, ptr %"%t46", align 8
  %156 = getelementptr inbounds i8, ptr %153, i64 %155
  %157 = load i8, ptr %156, align 1
  store i8 %157, ptr %b1, align 1
  br label %bb45

bb47:                                             ; preds = %bb52
  %158 = load i64, ptr %i, align 8
  %159 = insertvalue %Utf8Error undef, i64 %158, 0
  store %Utf8Error %159, ptr %"%t58", align 8
  %160 = load %Utf8Error, ptr %"%t58", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant45, i8 0, i64 24, i1 false)
  %161 = getelementptr inbounds nuw %Result.5, ptr %variant45, i32 0, i32 0
  store i32 1, ptr %161, align 4
  %162 = getelementptr inbounds nuw %Result.5, ptr %variant45, i32 0, i32 1
  %163 = getelementptr inbounds nuw { %Utf8Error }, ptr %162, i32 0, i32 0
  store %Utf8Error %160, ptr %163, align 8
  %164 = load %Result.5, ptr %variant45, align 8
  store %Result.5 %164, ptr %_0, align 8
  br label %bb1

bb48:                                             ; preds = %bb52
  br label %bb49

bb49:                                             ; preds = %bb71, %bb48
  %165 = load i64, ptr %i, align 8
  %166 = load i64, ptr %w, align 8
  %167 = call { i64, i1 } @llvm.uadd.with.overflow.i64(i64 %165, i64 %166)
  %168 = extractvalue { i64, i1 } %167, 0
  %169 = extractvalue { i64, i1 } %167, 1
  %170 = xor i1 %169, true
  br i1 %170, label %ok47, label %fail46

bb50:                                             ; preds = %bb55
  %171 = load i8, ptr %b, align 1
  store i8 %171, ptr %a49, align 1
  store i8 -12, ptr %b50, align 1
  %172 = call i32 @cmp.u8(ptr %a49, ptr %b50)
  %173 = icmp eq i32 %172, 0
  store i1 %173, ptr %"%t56", align 1
  %174 = load i1, ptr %"%t56", align 1
  %175 = zext i1 %174 to i32
  switch i32 %175, label %bb69 [
    i32 1, label %bb68
  ]

bb51:                                             ; preds = %bb55
  store i1 true, ptr %"%t49", align 1
  br label %bb52

bb52:                                             ; preds = %bb70, %bb51
  %176 = load i1, ptr %"%t49", align 1
  %177 = zext i1 %176 to i32
  switch i32 %177, label %bb48 [
    i32 1, label %bb47
  ]

bb53:                                             ; preds = %bb58
  %178 = load i8, ptr %b, align 1
  store i8 %178, ptr %a51, align 1
  store i8 -16, ptr %b52, align 1
  %179 = call i32 @cmp.u8(ptr %a51, ptr %b52)
  %180 = icmp eq i32 %179, 0
  store i1 %180, ptr %"%t55", align 1
  %181 = load i1, ptr %"%t55", align 1
  %182 = zext i1 %181 to i32
  switch i32 %182, label %bb66 [
    i32 1, label %bb65
  ]

bb54:                                             ; preds = %bb58
  store i1 true, ptr %"%t50", align 1
  br label %bb55

bb55:                                             ; preds = %bb67, %bb54
  %183 = load i1, ptr %"%t50", align 1
  %184 = zext i1 %183 to i32
  switch i32 %184, label %bb50 [
    i32 1, label %bb51
  ]

bb56:                                             ; preds = %bb61
  %185 = load i8, ptr %b, align 1
  store i8 %185, ptr %a53, align 1
  store i8 -19, ptr %b54, align 1
  %186 = call i32 @cmp.u8(ptr %a53, ptr %b54)
  %187 = icmp eq i32 %186, 0
  store i1 %187, ptr %"%t54", align 1
  %188 = load i1, ptr %"%t54", align 1
  %189 = zext i1 %188 to i32
  switch i32 %189, label %bb63 [
    i32 1, label %bb62
  ]

bb57:                                             ; preds = %bb61
  store i1 true, ptr %"%t51", align 1
  br label %bb58

bb58:                                             ; preds = %bb64, %bb57
  %190 = load i1, ptr %"%t51", align 1
  %191 = zext i1 %190 to i32
  switch i32 %191, label %bb53 [
    i32 1, label %bb54
  ]

bb59:                                             ; preds = %bb45
  %192 = load i8, ptr %b1, align 1
  store i8 %192, ptr %a55, align 1
  store i8 -96, ptr %b56, align 1
  %193 = call i32 @cmp.u8(ptr %a55, ptr %b56)
  %194 = icmp slt i32 %193, 0
  store i1 %194, ptr %"%t52", align 1
  br label %bb61

bb60:                                             ; preds = %bb45
  store i1 false, ptr %"%t52", align 1
  br label %bb61

bb61:                                             ; preds = %bb60, %bb59
  %195 = load i1, ptr %"%t52", align 1
  %196 = zext i1 %195 to i32
  switch i32 %196, label %bb56 [
    i32 1, label %bb57
  ]

bb62:                                             ; preds = %bb56
  %197 = load i8, ptr %b1, align 1
  store i8 %197, ptr %a57, align 1
  store i8 -96, ptr %b58, align 1
  %198 = call i32 @cmp.u8(ptr %a57, ptr %b58)
  %199 = icmp sge i32 %198, 0
  store i1 %199, ptr %"%t51", align 1
  br label %bb64

bb63:                                             ; preds = %bb56
  store i1 false, ptr %"%t51", align 1
  br label %bb64

bb64:                                             ; preds = %bb63, %bb62
  br label %bb58

bb65:                                             ; preds = %bb53
  %200 = load i8, ptr %b1, align 1
  store i8 %200, ptr %a59, align 1
  store i8 -112, ptr %b60, align 1
  %201 = call i32 @cmp.u8(ptr %a59, ptr %b60)
  %202 = icmp slt i32 %201, 0
  store i1 %202, ptr %"%t50", align 1
  br label %bb67

bb66:                                             ; preds = %bb53
  store i1 false, ptr %"%t50", align 1
  br label %bb67

bb67:                                             ; preds = %bb66, %bb65
  br label %bb55

bb68:                                             ; preds = %bb50
  %203 = load i8, ptr %b1, align 1
  store i8 %203, ptr %a61, align 1
  store i8 -112, ptr %b62, align 1
  %204 = call i32 @cmp.u8(ptr %a61, ptr %b62)
  %205 = icmp sge i32 %204, 0
  store i1 %205, ptr %"%t49", align 1
  br label %bb70

bb69:                                             ; preds = %bb50
  store i1 false, ptr %"%t49", align 1
  br label %bb70

bb70:                                             ; preds = %bb69, %bb68
  br label %bb52

bb71:                                             ; No predecessors!
  br label %bb49

bb72:                                             ; No predecessors!
  br label %bb7

bb73:                                             ; preds = %bb4
  %206 = load %deus.fat, ptr %"%t60", align 8
  call void @llvm.memset.p0.i64(ptr align 8 %variant63, i8 0, i64 24, i1 false)
  %207 = getelementptr inbounds nuw %Result.5, ptr %variant63, i32 0, i32 0
  store i32 0, ptr %207, align 4
  %208 = getelementptr inbounds nuw %Result.5, ptr %variant63, i32 0, i32 1
  %209 = getelementptr inbounds nuw { %deus.fat }, ptr %208, i32 0, i32 0
  store %deus.fat %206, ptr %209, align 8
  %210 = load %Result.5, ptr %variant63, align 8
  store %Result.5 %210, ptr %_0, align 8
  br label %bb1

assert.fail:                                      ; preds = %bb5
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.45) #2
  unreachable

dead:                                             ; No predecessors!
  unreachable

fail:                                             ; preds = %bb30
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.46) #2
  unreachable

ok:                                               ; preds = %bb30
  store i64 %90, ptr %"%t25", align 8
  %211 = load i64, ptr %"%t25", align 8
  %212 = load i64, ptr %n, align 8
  store i64 %211, ptr %a20, align 8
  store i64 %212, ptr %b21, align 8
  %213 = call i32 @cmp.usize(ptr %a20, ptr %b21)
  %214 = icmp sgt i32 %213, 0
  store i1 %214, ptr %"%t23", align 1
  br label %bb32

dead19:                                           ; No predecessors!
  unreachable

fail24:                                           ; preds = %bb35
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.47) #2
  unreachable

ok25:                                             ; preds = %bb35
  store i64 %108, ptr %"%t39", align 8
  %215 = load i64, ptr %"%t39", align 8
  %216 = load i64, ptr %"%t38", align 8
  store i64 %215, ptr %a27, align 8
  store i64 %216, ptr %b28, align 8
  %217 = call i32 @cmp.usize(ptr %a27, ptr %b28)
  %218 = icmp slt i32 %217, 0
  store i1 %218, ptr %"%t40", align 1
  %219 = load i1, ptr %"%t40", align 1
  br i1 %219, label %bb41, label %assert.fail29

dead26:                                           ; No predecessors!
  unreachable

assert.fail29:                                    ; preds = %ok25
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.48) #2
  unreachable

dead30:                                           ; No predecessors!
  unreachable

fail36:                                           ; preds = %bb43
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.49) #2
  unreachable

ok37:                                             ; preds = %bb43
  store i64 %144, ptr %"%t46", align 8
  %220 = load i64, ptr %"%t46", align 8
  %221 = load i64, ptr %"%t45", align 8
  store i64 %220, ptr %a39, align 8
  store i64 %221, ptr %b40, align 8
  %222 = call i32 @cmp.usize(ptr %a39, ptr %b40)
  %223 = icmp slt i32 %222, 0
  store i1 %223, ptr %"%t47", align 1
  %224 = load i1, ptr %"%t47", align 1
  br i1 %224, label %bb46, label %assert.fail41

dead38:                                           ; No predecessors!
  unreachable

assert.fail41:                                    ; preds = %ok37
  call void @deus_panic_at(ptr @panic, i64 19, ptr @loc.50) #2
  unreachable

dead42:                                           ; No predecessors!
  unreachable

fail46:                                           ; preds = %bb49
  call void @deus_panic_at(ptr @panic.13, i64 28, ptr @loc.51) #2
  unreachable

ok47:                                             ; preds = %bb49
  store i64 %168, ptr %i, align 8
  br label %bb7

dead48:                                           ; No predecessors!
  unreachable
}

declare void @deus_string_push_str(ptr, ptr, i64)

define internal i64 @deus.valid_up_to(ptr %0) #0 {
entry:
  %self = alloca ptr, align 8
  %_0 = alloca i64, align 8
  store ptr %0, ptr %self, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %1 = load ptr, ptr %self, align 8
  %2 = getelementptr inbounds nuw %Utf8Error, ptr %1, i32 0, i32 0
  %3 = load i64, ptr %2, align 8
  store i64 %3, ptr %_0, align 8
  br label %bb1

bb1:                                              ; preds = %bb0
  %4 = load i64, ptr %_0, align 8
  ret i64 %4
}

define internal %deus.fat @deus.unwrap.E_Utf8Error_T__str(%Result.5 %0, ptr %1) #0 {
entry:
  %v = alloca %Utf8Error, align 8
  %panic.sink = alloca %deus.vec, align 8
  %panic.writer = alloca { ptr, ptr, i1 }, align 8
  %panic.msg = alloca { ptr, i64, i64 }, align 8
  %panic.buf = alloca [4096 x i8], align 1
  %fmt.arg = alloca ptr, align 8
  %"%t9" = alloca %deus.unit, align 8
  %"%t8" = alloca ptr, align 8
  %"%t7" = alloca %deus.vec, align 8
  %"%t6" = alloca %deus.unit, align 8
  %e = alloca %Utf8Error, align 8
  %"%t4" = alloca i32, align 4
  %x = alloca %deus.fat, align 8
  %"%t2" = alloca i32, align 4
  %self = alloca %Result.5, align 8
  %_0 = alloca %deus.fat, align 8
  %2 = freeze %Result.5 %0
  store %Result.5 %2, ptr %self, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %3 = load %Result.5, ptr %self, align 8
  %4 = extractvalue %Result.5 %3, 0
  store i32 %4, ptr %"%t2", align 4
  %5 = load i32, ptr %"%t2", align 4
  switch i32 %5, label %bb3 [
    i32 0, label %bb4
  ]

bb1:                                              ; preds = %bb2
  %6 = load %deus.fat, ptr %_0, align 8
  ret %deus.fat %6

bb2:                                              ; preds = %bb7, %bb4
  br label %bb1

bb3:                                              ; preds = %bb0
  %7 = load %Result.5, ptr %self, align 8
  %8 = extractvalue %Result.5 %7, 0
  store i32 %8, ptr %"%t4", align 4
  %9 = load i32, ptr %"%t4", align 4
  switch i32 %9, label %bb5 [
    i32 1, label %bb6
  ]

bb4:                                              ; preds = %bb0
  %10 = getelementptr inbounds nuw %Result.5, ptr %self, i32 0, i32 1
  %11 = getelementptr inbounds nuw { %deus.fat }, ptr %10, i32 0, i32 0
  %12 = load %deus.fat, ptr %11, align 8
  store %deus.fat %12, ptr %x, align 8
  %13 = load %deus.fat, ptr %x, align 8
  store %deus.fat %13, ptr %_0, align 8
  br label %bb2

bb5:                                              ; preds = %bb3
  unreachable

bb6:                                              ; preds = %bb3
  %14 = getelementptr inbounds nuw %Result.5, ptr %self, i32 0, i32 1
  %15 = getelementptr inbounds nuw { %Utf8Error }, ptr %14, i32 0, i32 0
  %16 = load %Utf8Error, ptr %15, align 8
  store %Utf8Error %16, ptr %e, align 8
  store ptr %e, ptr %"%t8", align 8
  %17 = load ptr, ptr %"%t8", align 8
  store ptr %17, ptr %fmt.arg, align 8
  store %deus.vec zeroinitializer, ptr %"%t7", align 8
  %18 = load ptr, ptr %fmt.arg, align 8
  %19 = getelementptr inbounds nuw { ptr, i64, i64 }, ptr %panic.msg, i32 0, i32 0
  store ptr %panic.buf, ptr %19, align 8
  %20 = getelementptr inbounds nuw { ptr, i64, i64 }, ptr %panic.msg, i32 0, i32 1
  store i64 0, ptr %20, align 8
  %21 = getelementptr inbounds nuw { ptr, i64, i64 }, ptr %panic.msg, i32 0, i32 2
  store i64 4096, ptr %21, align 8
  %22 = getelementptr inbounds nuw { ptr, ptr, i1 }, ptr %panic.writer, i32 0, i32 0
  store ptr @deus_fixed_write, ptr %22, align 8
  %23 = getelementptr inbounds nuw { ptr, ptr, i1 }, ptr %panic.writer, i32 0, i32 1
  store ptr %panic.msg, ptr %23, align 8
  %24 = getelementptr inbounds nuw { ptr, ptr, i1 }, ptr %panic.writer, i32 0, i32 2
  store i1 false, ptr %24, align 1
  %25 = getelementptr inbounds nuw %deus.vec, ptr %panic.sink, i32 0, i32 0
  store ptr %panic.writer, ptr %25, align 8
  %26 = getelementptr inbounds nuw %deus.vec, ptr %panic.sink, i32 0, i32 1
  store i64 0, ptr %26, align 8
  %27 = getelementptr inbounds nuw %deus.vec, ptr %panic.sink, i32 0, i32 2
  store i64 -1, ptr %27, align 8
  call void @deus_string_push_str(ptr %panic.sink, ptr @str.52, i64 44)
  %28 = load %Utf8Error, ptr %18, align 8
  store %Utf8Error %28, ptr %v, align 8
  call void @dbg.Utf8Error(ptr %v, ptr %panic.sink)
  %29 = getelementptr inbounds nuw { ptr, i64, i64 }, ptr %panic.msg, i32 0, i32 1
  %30 = load i64, ptr %29, align 8
  %31 = icmp eq ptr %1, null
  %32 = select i1 %31, ptr @loc.54, ptr %1
  call void @deus_panic_at(ptr %panic.buf, i64 %30, ptr %32) #2
  unreachable

bb7:                                              ; No predecessors!
  br label %bb2

dead:                                             ; No predecessors!
  unreachable
}

declare void @deus_string_push_char(ptr, i32)

define internal i32 @cmp.isize(ptr %0, ptr %1) #0 {
entry:
  %2 = load i64, ptr %0, align 8
  %3 = load i64, ptr %1, align 8
  %4 = icmp slt i64 %2, %3
  %5 = icmp sgt i64 %2, %3
  %6 = select i1 %5, i32 1, i32 0
  %7 = select i1 %4, i32 -1, i32 %6
  ret i32 %7
}

define internal %IoError @deus.last_os_error() #0 {
entry:
  %"%t1" = alloca i32, align 4
  %_0 = alloca %IoError, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %0 = call i32 @deus_sys_errno()
  store i32 %0, ptr %"%t1", align 4
  br label %bb2

bb1:                                              ; preds = %bb3
  %1 = load %IoError, ptr %_0, align 8
  ret %IoError %1

bb2:                                              ; preds = %bb0
  %2 = load i32, ptr %"%t1", align 4
  %3 = call %IoError @deus.from_raw_os_error(i32 %2)
  store %IoError %3, ptr %_0, align 8
  br label %bb3

bb3:                                              ; preds = %bb2
  br label %bb1
}

define internal %deus.vec @deus.from(%deus.fat %0) #0 {
entry:
  %str = alloca %deus.vec, align 8
  %"%t2" = alloca %deus.fat, align 8
  %value = alloca %deus.fat, align 8
  %_0 = alloca %deus.vec, align 8
  %1 = freeze %deus.fat %0
  store %deus.fat %1, ptr %value, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load %deus.fat, ptr %value, align 8
  %3 = extractvalue %deus.fat %2, 0
  %4 = extractvalue %deus.fat %2, 1
  %5 = insertvalue %deus.fat undef, ptr %3, 0
  %6 = insertvalue %deus.fat %5, i64 %4, 1
  store %deus.fat %6, ptr %"%t2", align 8
  %7 = load %deus.fat, ptr %"%t2", align 8
  %8 = extractvalue %deus.fat %7, 0
  %9 = extractvalue %deus.fat %7, 1
  call void @deus_string_from(ptr %str, ptr %8, i64 %9)
  %10 = load %deus.vec, ptr %str, align 8
  store %deus.vec %10, ptr %_0, align 8
  br label %bb2

bb1:                                              ; preds = %bb2
  %11 = load %deus.vec, ptr %_0, align 8
  ret %deus.vec %11

bb2:                                              ; preds = %bb0
  br label %bb1
}

declare i1 @deus_fixed_write(ptr, ptr, i64)

define internal void @dbg.Utf8Error(ptr %0, ptr %1) #0 {
entry:
  call void @deus_string_push_str(ptr %1, ptr @str.56, i64 9)
  call void @deus_string_push_str(ptr %1, ptr @str.57, i64 3)
  call void @deus_string_push_str(ptr %1, ptr @str.58, i64 13)
  %2 = getelementptr inbounds nuw %Utf8Error, ptr %0, i32 0, i32 0
  call void @dbg.usize(ptr %2, ptr %1)
  call void @deus_string_push_str(ptr %1, ptr @str.59, i64 2)
  ret void
}

declare i32 @deus_sys_errno()

define internal %IoError @deus.from_raw_os_error(i32 %0) #0 {
entry:
  %variant = alloca %Option, align 8
  %b2 = alloca i64, align 8
  %a1 = alloca i64, align 8
  %b = alloca i64, align 8
  %a = alloca i64, align 8
  %"%t23" = alloca %Option, align 8
  %"%t22" = alloca i32, align 4
  %"%t21" = alloca %ErrorKind, align 8
  %"%t20" = alloca i1, align 1
  %"%t19" = alloca i1, align 1
  %"%t18" = alloca i1, align 1
  %"%t17" = alloca i64, align 8
  %"%t16" = alloca i64, align 8
  %"%t15" = alloca i64, align 8
  %"%t14" = alloca %Range, align 8
  %"%t13" = alloca i64, align 8
  %"%t12" = alloca %deus.fat, align 8
  %message = alloca %deus.vec, align 8
  %"%t10" = alloca %deus.fat, align 8
  %"%t9" = alloca ptr, align 8
  %"%t8" = alloca ptr, align 8
  %"%t7" = alloca %deus.fat, align 8
  %"%t6" = alloca ptr, align 8
  %"%t5" = alloca ptr, align 8
  %"%t4" = alloca i32, align 4
  %n = alloca i64, align 8
  %buf = alloca [256 x i8], align 1
  %code = alloca i32, align 4
  %_0 = alloca %IoError, align 8
  store i32 %0, ptr %code, align 4
  br label %bb0

bb0:                                              ; preds = %entry
  call void @llvm.memset.p0.i64(ptr align 1 %buf, i8 0, i64 256, i1 false)
  %1 = load i32, ptr %code, align 4
  store i32 %1, ptr %"%t4", align 4
  store ptr %buf, ptr %"%t8", align 8
  %2 = load ptr, ptr %"%t8", align 8
  store ptr %2, ptr %"%t9", align 8
  %3 = load ptr, ptr %"%t9", align 8
  %4 = insertvalue %deus.fat undef, ptr %3, 0
  %5 = insertvalue %deus.fat %4, i64 256, 1
  store %deus.fat %5, ptr %"%t7", align 8
  %6 = load %deus.fat, ptr %"%t7", align 8
  %7 = extractvalue %deus.fat %6, 0
  %8 = extractvalue %deus.fat %6, 1
  %9 = insertvalue %deus.fat undef, ptr %7, 0
  %10 = insertvalue %deus.fat %9, i64 %8, 1
  store %deus.fat %10, ptr %"%t10", align 8
  %11 = load %deus.fat, ptr %"%t10", align 8
  %12 = extractvalue %deus.fat %11, 0
  %13 = extractvalue %deus.fat %11, 1
  store ptr %12, ptr %"%t6", align 8
  br label %bb2

bb1:                                              ; preds = %bb9
  %14 = load %IoError, ptr %_0, align 8
  ret %IoError %14

bb2:                                              ; preds = %bb0
  %15 = load ptr, ptr %"%t6", align 8
  store ptr %15, ptr %"%t5", align 8
  br label %bb3

bb3:                                              ; preds = %bb2
  %16 = load i32, ptr %"%t4", align 4
  %17 = load ptr, ptr %"%t5", align 8
  %18 = call i64 @deus_sys_strerror(i32 %16, ptr %17, i64 256)
  store i64 %18, ptr %n, align 8
  br label %bb4

bb4:                                              ; preds = %bb3
  store i64 256, ptr %"%t13", align 8
  %19 = load i64, ptr %n, align 8
  store i64 %19, ptr %"%t15", align 8
  br label %bb5

bb5:                                              ; preds = %bb4
  %20 = load i64, ptr %"%t15", align 8
  %21 = insertvalue %Range { i64 0, i64 undef }, i64 %20, 1
  store %Range %21, ptr %"%t14", align 8
  %22 = getelementptr inbounds nuw %Range, ptr %"%t14", i32 0, i32 0
  %23 = load i64, ptr %22, align 8
  store i64 %23, ptr %"%t16", align 8
  %24 = getelementptr inbounds nuw %Range, ptr %"%t14", i32 0, i32 1
  %25 = load i64, ptr %24, align 8
  store i64 %25, ptr %"%t17", align 8
  %26 = load i64, ptr %"%t16", align 8
  %27 = load i64, ptr %"%t17", align 8
  store i64 %26, ptr %a, align 8
  store i64 %27, ptr %b, align 8
  %28 = call i32 @cmp.usize(ptr %a, ptr %b)
  %29 = icmp sle i32 %28, 0
  store i1 %29, ptr %"%t18", align 1
  %30 = load i64, ptr %"%t17", align 8
  %31 = load i64, ptr %"%t13", align 8
  store i64 %30, ptr %a1, align 8
  store i64 %31, ptr %b2, align 8
  %32 = call i32 @cmp.usize(ptr %a1, ptr %b2)
  %33 = icmp sle i32 %32, 0
  store i1 %33, ptr %"%t19", align 1
  %34 = load i1, ptr %"%t18", align 1
  %35 = load i1, ptr %"%t19", align 1
  %36 = and i1 %34, %35
  store i1 %36, ptr %"%t20", align 1
  %37 = load i1, ptr %"%t20", align 1
  br i1 %37, label %bb6, label %assert.fail

bb6:                                              ; preds = %bb5
  %38 = load i64, ptr %"%t16", align 8
  %39 = load i64, ptr %"%t17", align 8
  %40 = getelementptr inbounds [256 x i8], ptr %buf, i64 0, i64 %38
  %41 = sub i64 %39, %38
  %42 = insertvalue %deus.fat undef, ptr %40, 0
  %43 = insertvalue %deus.fat %42, i64 %41, 1
  store %deus.fat %43, ptr %"%t12", align 8
  %44 = load %deus.fat, ptr %"%t12", align 8
  %45 = call %deus.vec @deus.from_utf8_lossy(%deus.fat %44)
  store %deus.vec %45, ptr %message, align 8
  br label %bb7

bb7:                                              ; preds = %bb6
  %46 = load i32, ptr %code, align 4
  %47 = call i32 @deus_sys_error_kind(i32 %46)
  store i32 %47, ptr %"%t22", align 4
  br label %bb8

bb8:                                              ; preds = %bb7
  %48 = load i32, ptr %"%t22", align 4
  %49 = call %ErrorKind @deus.from_index(i32 %48)
  store %ErrorKind %49, ptr %"%t21", align 4
  br label %bb9

bb9:                                              ; preds = %bb8
  %50 = load i32, ptr %code, align 4
  call void @llvm.memset.p0.i64(ptr align 4 %variant, i8 0, i64 8, i1 false)
  %51 = getelementptr inbounds nuw %Option, ptr %variant, i32 0, i32 0
  store i32 1, ptr %51, align 4
  %52 = getelementptr inbounds nuw %Option, ptr %variant, i32 0, i32 1
  %53 = getelementptr inbounds nuw { i32 }, ptr %52, i32 0, i32 0
  store i32 %50, ptr %53, align 4
  %54 = load %Option, ptr %variant, align 4
  store %Option %54, ptr %"%t23", align 4
  %55 = load %ErrorKind, ptr %"%t21", align 4
  %56 = insertvalue %IoError undef, %ErrorKind %55, 1
  %57 = load %Option, ptr %"%t23", align 4
  %58 = insertvalue %IoError %56, %Option %57, 2
  %59 = load %deus.vec, ptr %message, align 8
  %60 = insertvalue %IoError %58, %deus.vec %59, 0
  store %IoError %60, ptr %_0, align 8
  br label %bb1

assert.fail:                                      ; preds = %bb5
  call void @deus_panic_at(ptr @panic.33, i64 19, ptr @loc.55) #2
  unreachable

dead:                                             ; No predecessors!
  unreachable
}

declare void @deus_string_from(ptr, ptr, i64)

declare i64 @deus_sys_strerror(i32, ptr, i64)

declare i32 @deus_sys_error_kind(i32)

define internal %ErrorKind @deus.from_index(i32 %0) #0 {
entry:
  %variant58 = alloca %ErrorKind, align 8
  %variant57 = alloca %ErrorKind, align 8
  %variant56 = alloca %ErrorKind, align 8
  %b55 = alloca i32, align 4
  %a54 = alloca i32, align 4
  %variant53 = alloca %ErrorKind, align 8
  %b52 = alloca i32, align 4
  %a51 = alloca i32, align 4
  %variant50 = alloca %ErrorKind, align 8
  %b49 = alloca i32, align 4
  %a48 = alloca i32, align 4
  %variant47 = alloca %ErrorKind, align 8
  %b46 = alloca i32, align 4
  %a45 = alloca i32, align 4
  %variant44 = alloca %ErrorKind, align 8
  %b43 = alloca i32, align 4
  %a42 = alloca i32, align 4
  %variant41 = alloca %ErrorKind, align 8
  %b40 = alloca i32, align 4
  %a39 = alloca i32, align 4
  %variant38 = alloca %ErrorKind, align 8
  %b37 = alloca i32, align 4
  %a36 = alloca i32, align 4
  %variant35 = alloca %ErrorKind, align 8
  %b34 = alloca i32, align 4
  %a33 = alloca i32, align 4
  %variant32 = alloca %ErrorKind, align 8
  %b31 = alloca i32, align 4
  %a30 = alloca i32, align 4
  %variant29 = alloca %ErrorKind, align 8
  %b28 = alloca i32, align 4
  %a27 = alloca i32, align 4
  %variant26 = alloca %ErrorKind, align 8
  %b25 = alloca i32, align 4
  %a24 = alloca i32, align 4
  %variant23 = alloca %ErrorKind, align 8
  %b22 = alloca i32, align 4
  %a21 = alloca i32, align 4
  %variant20 = alloca %ErrorKind, align 8
  %b19 = alloca i32, align 4
  %a18 = alloca i32, align 4
  %variant17 = alloca %ErrorKind, align 8
  %b16 = alloca i32, align 4
  %a15 = alloca i32, align 4
  %variant14 = alloca %ErrorKind, align 8
  %b13 = alloca i32, align 4
  %a12 = alloca i32, align 4
  %variant11 = alloca %ErrorKind, align 8
  %b10 = alloca i32, align 4
  %a9 = alloca i32, align 4
  %variant8 = alloca %ErrorKind, align 8
  %b7 = alloca i32, align 4
  %a6 = alloca i32, align 4
  %variant5 = alloca %ErrorKind, align 8
  %b4 = alloca i32, align 4
  %a3 = alloca i32, align 4
  %variant = alloca %ErrorKind, align 8
  %b2 = alloca i32, align 4
  %a1 = alloca i32, align 4
  %b = alloca i32, align 4
  %a = alloca i32, align 4
  %"%t21" = alloca i1, align 1
  %"%t20" = alloca i1, align 1
  %"%t19" = alloca i1, align 1
  %"%t18" = alloca i1, align 1
  %"%t17" = alloca i1, align 1
  %"%t16" = alloca i1, align 1
  %"%t15" = alloca i1, align 1
  %"%t14" = alloca i1, align 1
  %"%t13" = alloca i1, align 1
  %"%t12" = alloca i1, align 1
  %"%t11" = alloca i1, align 1
  %"%t10" = alloca i1, align 1
  %"%t9" = alloca i1, align 1
  %"%t8" = alloca i1, align 1
  %"%t7" = alloca i1, align 1
  %"%t6" = alloca i1, align 1
  %"%t5" = alloca i1, align 1
  %"%t4" = alloca i1, align 1
  %"%t3" = alloca i1, align 1
  %"%t2" = alloca i1, align 1
  %i = alloca i32, align 4
  %_0 = alloca %ErrorKind, align 8
  store i32 %0, ptr %i, align 4
  br label %bb0

bb0:                                              ; preds = %entry
  %1 = load i32, ptr %i, align 4
  store i32 %1, ptr %a, align 4
  store i32 1, ptr %b, align 4
  %2 = call i32 @cmp.i32(ptr %a, ptr %b)
  %3 = icmp eq i32 %2, 0
  store i1 %3, ptr %"%t2", align 1
  %4 = load i1, ptr %"%t2", align 1
  %5 = zext i1 %4 to i32
  switch i32 %5, label %bb3 [
    i32 1, label %bb4
  ]

bb1:                                              ; preds = %bb2
  %6 = load %ErrorKind, ptr %_0, align 4
  ret %ErrorKind %6

bb2:                                              ; preds = %bb42, %bb41, %bb40, %bb38, %bb36, %bb34, %bb32, %bb30, %bb28, %bb26, %bb24, %bb22, %bb20, %bb18, %bb16, %bb14, %bb12, %bb10, %bb8, %bb6, %bb4
  br label %bb1

bb3:                                              ; preds = %bb0
  %7 = load i32, ptr %i, align 4
  store i32 %7, ptr %a1, align 4
  store i32 2, ptr %b2, align 4
  %8 = call i32 @cmp.i32(ptr %a1, ptr %b2)
  %9 = icmp eq i32 %8, 0
  store i1 %9, ptr %"%t3", align 1
  %10 = load i1, ptr %"%t3", align 1
  %11 = zext i1 %10 to i32
  switch i32 %11, label %bb5 [
    i32 1, label %bb6
  ]

bb4:                                              ; preds = %bb0
  call void @llvm.memset.p0.i64(ptr align 4 %variant, i8 0, i64 4, i1 false)
  %12 = getelementptr inbounds nuw %ErrorKind, ptr %variant, i32 0, i32 0
  store i32 1, ptr %12, align 4
  %13 = load %ErrorKind, ptr %variant, align 4
  store %ErrorKind %13, ptr %_0, align 4
  br label %bb2

bb5:                                              ; preds = %bb3
  %14 = load i32, ptr %i, align 4
  store i32 %14, ptr %a3, align 4
  store i32 3, ptr %b4, align 4
  %15 = call i32 @cmp.i32(ptr %a3, ptr %b4)
  %16 = icmp eq i32 %15, 0
  store i1 %16, ptr %"%t4", align 1
  %17 = load i1, ptr %"%t4", align 1
  %18 = zext i1 %17 to i32
  switch i32 %18, label %bb7 [
    i32 1, label %bb8
  ]

bb6:                                              ; preds = %bb3
  call void @llvm.memset.p0.i64(ptr align 4 %variant5, i8 0, i64 4, i1 false)
  %19 = getelementptr inbounds nuw %ErrorKind, ptr %variant5, i32 0, i32 0
  store i32 2, ptr %19, align 4
  %20 = load %ErrorKind, ptr %variant5, align 4
  store %ErrorKind %20, ptr %_0, align 4
  br label %bb2

bb7:                                              ; preds = %bb5
  %21 = load i32, ptr %i, align 4
  store i32 %21, ptr %a6, align 4
  store i32 4, ptr %b7, align 4
  %22 = call i32 @cmp.i32(ptr %a6, ptr %b7)
  %23 = icmp eq i32 %22, 0
  store i1 %23, ptr %"%t5", align 1
  %24 = load i1, ptr %"%t5", align 1
  %25 = zext i1 %24 to i32
  switch i32 %25, label %bb9 [
    i32 1, label %bb10
  ]

bb8:                                              ; preds = %bb5
  call void @llvm.memset.p0.i64(ptr align 4 %variant8, i8 0, i64 4, i1 false)
  %26 = getelementptr inbounds nuw %ErrorKind, ptr %variant8, i32 0, i32 0
  store i32 3, ptr %26, align 4
  %27 = load %ErrorKind, ptr %variant8, align 4
  store %ErrorKind %27, ptr %_0, align 4
  br label %bb2

bb9:                                              ; preds = %bb7
  %28 = load i32, ptr %i, align 4
  store i32 %28, ptr %a9, align 4
  store i32 5, ptr %b10, align 4
  %29 = call i32 @cmp.i32(ptr %a9, ptr %b10)
  %30 = icmp eq i32 %29, 0
  store i1 %30, ptr %"%t6", align 1
  %31 = load i1, ptr %"%t6", align 1
  %32 = zext i1 %31 to i32
  switch i32 %32, label %bb11 [
    i32 1, label %bb12
  ]

bb10:                                             ; preds = %bb7
  call void @llvm.memset.p0.i64(ptr align 4 %variant11, i8 0, i64 4, i1 false)
  %33 = getelementptr inbounds nuw %ErrorKind, ptr %variant11, i32 0, i32 0
  store i32 4, ptr %33, align 4
  %34 = load %ErrorKind, ptr %variant11, align 4
  store %ErrorKind %34, ptr %_0, align 4
  br label %bb2

bb11:                                             ; preds = %bb9
  %35 = load i32, ptr %i, align 4
  store i32 %35, ptr %a12, align 4
  store i32 6, ptr %b13, align 4
  %36 = call i32 @cmp.i32(ptr %a12, ptr %b13)
  %37 = icmp eq i32 %36, 0
  store i1 %37, ptr %"%t7", align 1
  %38 = load i1, ptr %"%t7", align 1
  %39 = zext i1 %38 to i32
  switch i32 %39, label %bb13 [
    i32 1, label %bb14
  ]

bb12:                                             ; preds = %bb9
  call void @llvm.memset.p0.i64(ptr align 4 %variant14, i8 0, i64 4, i1 false)
  %40 = getelementptr inbounds nuw %ErrorKind, ptr %variant14, i32 0, i32 0
  store i32 5, ptr %40, align 4
  %41 = load %ErrorKind, ptr %variant14, align 4
  store %ErrorKind %41, ptr %_0, align 4
  br label %bb2

bb13:                                             ; preds = %bb11
  %42 = load i32, ptr %i, align 4
  store i32 %42, ptr %a15, align 4
  store i32 7, ptr %b16, align 4
  %43 = call i32 @cmp.i32(ptr %a15, ptr %b16)
  %44 = icmp eq i32 %43, 0
  store i1 %44, ptr %"%t8", align 1
  %45 = load i1, ptr %"%t8", align 1
  %46 = zext i1 %45 to i32
  switch i32 %46, label %bb15 [
    i32 1, label %bb16
  ]

bb14:                                             ; preds = %bb11
  call void @llvm.memset.p0.i64(ptr align 4 %variant17, i8 0, i64 4, i1 false)
  %47 = getelementptr inbounds nuw %ErrorKind, ptr %variant17, i32 0, i32 0
  store i32 6, ptr %47, align 4
  %48 = load %ErrorKind, ptr %variant17, align 4
  store %ErrorKind %48, ptr %_0, align 4
  br label %bb2

bb15:                                             ; preds = %bb13
  %49 = load i32, ptr %i, align 4
  store i32 %49, ptr %a18, align 4
  store i32 8, ptr %b19, align 4
  %50 = call i32 @cmp.i32(ptr %a18, ptr %b19)
  %51 = icmp eq i32 %50, 0
  store i1 %51, ptr %"%t9", align 1
  %52 = load i1, ptr %"%t9", align 1
  %53 = zext i1 %52 to i32
  switch i32 %53, label %bb17 [
    i32 1, label %bb18
  ]

bb16:                                             ; preds = %bb13
  call void @llvm.memset.p0.i64(ptr align 4 %variant20, i8 0, i64 4, i1 false)
  %54 = getelementptr inbounds nuw %ErrorKind, ptr %variant20, i32 0, i32 0
  store i32 7, ptr %54, align 4
  %55 = load %ErrorKind, ptr %variant20, align 4
  store %ErrorKind %55, ptr %_0, align 4
  br label %bb2

bb17:                                             ; preds = %bb15
  %56 = load i32, ptr %i, align 4
  store i32 %56, ptr %a21, align 4
  store i32 9, ptr %b22, align 4
  %57 = call i32 @cmp.i32(ptr %a21, ptr %b22)
  %58 = icmp eq i32 %57, 0
  store i1 %58, ptr %"%t10", align 1
  %59 = load i1, ptr %"%t10", align 1
  %60 = zext i1 %59 to i32
  switch i32 %60, label %bb19 [
    i32 1, label %bb20
  ]

bb18:                                             ; preds = %bb15
  call void @llvm.memset.p0.i64(ptr align 4 %variant23, i8 0, i64 4, i1 false)
  %61 = getelementptr inbounds nuw %ErrorKind, ptr %variant23, i32 0, i32 0
  store i32 8, ptr %61, align 4
  %62 = load %ErrorKind, ptr %variant23, align 4
  store %ErrorKind %62, ptr %_0, align 4
  br label %bb2

bb19:                                             ; preds = %bb17
  %63 = load i32, ptr %i, align 4
  store i32 %63, ptr %a24, align 4
  store i32 10, ptr %b25, align 4
  %64 = call i32 @cmp.i32(ptr %a24, ptr %b25)
  %65 = icmp eq i32 %64, 0
  store i1 %65, ptr %"%t11", align 1
  %66 = load i1, ptr %"%t11", align 1
  %67 = zext i1 %66 to i32
  switch i32 %67, label %bb21 [
    i32 1, label %bb22
  ]

bb20:                                             ; preds = %bb17
  call void @llvm.memset.p0.i64(ptr align 4 %variant26, i8 0, i64 4, i1 false)
  %68 = getelementptr inbounds nuw %ErrorKind, ptr %variant26, i32 0, i32 0
  store i32 9, ptr %68, align 4
  %69 = load %ErrorKind, ptr %variant26, align 4
  store %ErrorKind %69, ptr %_0, align 4
  br label %bb2

bb21:                                             ; preds = %bb19
  %70 = load i32, ptr %i, align 4
  store i32 %70, ptr %a27, align 4
  store i32 11, ptr %b28, align 4
  %71 = call i32 @cmp.i32(ptr %a27, ptr %b28)
  %72 = icmp eq i32 %71, 0
  store i1 %72, ptr %"%t12", align 1
  %73 = load i1, ptr %"%t12", align 1
  %74 = zext i1 %73 to i32
  switch i32 %74, label %bb23 [
    i32 1, label %bb24
  ]

bb22:                                             ; preds = %bb19
  call void @llvm.memset.p0.i64(ptr align 4 %variant29, i8 0, i64 4, i1 false)
  %75 = getelementptr inbounds nuw %ErrorKind, ptr %variant29, i32 0, i32 0
  store i32 10, ptr %75, align 4
  %76 = load %ErrorKind, ptr %variant29, align 4
  store %ErrorKind %76, ptr %_0, align 4
  br label %bb2

bb23:                                             ; preds = %bb21
  %77 = load i32, ptr %i, align 4
  store i32 %77, ptr %a30, align 4
  store i32 12, ptr %b31, align 4
  %78 = call i32 @cmp.i32(ptr %a30, ptr %b31)
  %79 = icmp eq i32 %78, 0
  store i1 %79, ptr %"%t13", align 1
  %80 = load i1, ptr %"%t13", align 1
  %81 = zext i1 %80 to i32
  switch i32 %81, label %bb25 [
    i32 1, label %bb26
  ]

bb24:                                             ; preds = %bb21
  call void @llvm.memset.p0.i64(ptr align 4 %variant32, i8 0, i64 4, i1 false)
  %82 = getelementptr inbounds nuw %ErrorKind, ptr %variant32, i32 0, i32 0
  store i32 11, ptr %82, align 4
  %83 = load %ErrorKind, ptr %variant32, align 4
  store %ErrorKind %83, ptr %_0, align 4
  br label %bb2

bb25:                                             ; preds = %bb23
  %84 = load i32, ptr %i, align 4
  store i32 %84, ptr %a33, align 4
  store i32 13, ptr %b34, align 4
  %85 = call i32 @cmp.i32(ptr %a33, ptr %b34)
  %86 = icmp eq i32 %85, 0
  store i1 %86, ptr %"%t14", align 1
  %87 = load i1, ptr %"%t14", align 1
  %88 = zext i1 %87 to i32
  switch i32 %88, label %bb27 [
    i32 1, label %bb28
  ]

bb26:                                             ; preds = %bb23
  call void @llvm.memset.p0.i64(ptr align 4 %variant35, i8 0, i64 4, i1 false)
  %89 = getelementptr inbounds nuw %ErrorKind, ptr %variant35, i32 0, i32 0
  store i32 12, ptr %89, align 4
  %90 = load %ErrorKind, ptr %variant35, align 4
  store %ErrorKind %90, ptr %_0, align 4
  br label %bb2

bb27:                                             ; preds = %bb25
  %91 = load i32, ptr %i, align 4
  store i32 %91, ptr %a36, align 4
  store i32 14, ptr %b37, align 4
  %92 = call i32 @cmp.i32(ptr %a36, ptr %b37)
  %93 = icmp eq i32 %92, 0
  store i1 %93, ptr %"%t15", align 1
  %94 = load i1, ptr %"%t15", align 1
  %95 = zext i1 %94 to i32
  switch i32 %95, label %bb29 [
    i32 1, label %bb30
  ]

bb28:                                             ; preds = %bb25
  call void @llvm.memset.p0.i64(ptr align 4 %variant38, i8 0, i64 4, i1 false)
  %96 = getelementptr inbounds nuw %ErrorKind, ptr %variant38, i32 0, i32 0
  store i32 13, ptr %96, align 4
  %97 = load %ErrorKind, ptr %variant38, align 4
  store %ErrorKind %97, ptr %_0, align 4
  br label %bb2

bb29:                                             ; preds = %bb27
  %98 = load i32, ptr %i, align 4
  store i32 %98, ptr %a39, align 4
  store i32 15, ptr %b40, align 4
  %99 = call i32 @cmp.i32(ptr %a39, ptr %b40)
  %100 = icmp eq i32 %99, 0
  store i1 %100, ptr %"%t16", align 1
  %101 = load i1, ptr %"%t16", align 1
  %102 = zext i1 %101 to i32
  switch i32 %102, label %bb31 [
    i32 1, label %bb32
  ]

bb30:                                             ; preds = %bb27
  call void @llvm.memset.p0.i64(ptr align 4 %variant41, i8 0, i64 4, i1 false)
  %103 = getelementptr inbounds nuw %ErrorKind, ptr %variant41, i32 0, i32 0
  store i32 14, ptr %103, align 4
  %104 = load %ErrorKind, ptr %variant41, align 4
  store %ErrorKind %104, ptr %_0, align 4
  br label %bb2

bb31:                                             ; preds = %bb29
  %105 = load i32, ptr %i, align 4
  store i32 %105, ptr %a42, align 4
  store i32 16, ptr %b43, align 4
  %106 = call i32 @cmp.i32(ptr %a42, ptr %b43)
  %107 = icmp eq i32 %106, 0
  store i1 %107, ptr %"%t17", align 1
  %108 = load i1, ptr %"%t17", align 1
  %109 = zext i1 %108 to i32
  switch i32 %109, label %bb33 [
    i32 1, label %bb34
  ]

bb32:                                             ; preds = %bb29
  call void @llvm.memset.p0.i64(ptr align 4 %variant44, i8 0, i64 4, i1 false)
  %110 = getelementptr inbounds nuw %ErrorKind, ptr %variant44, i32 0, i32 0
  store i32 15, ptr %110, align 4
  %111 = load %ErrorKind, ptr %variant44, align 4
  store %ErrorKind %111, ptr %_0, align 4
  br label %bb2

bb33:                                             ; preds = %bb31
  %112 = load i32, ptr %i, align 4
  store i32 %112, ptr %a45, align 4
  store i32 17, ptr %b46, align 4
  %113 = call i32 @cmp.i32(ptr %a45, ptr %b46)
  %114 = icmp eq i32 %113, 0
  store i1 %114, ptr %"%t18", align 1
  %115 = load i1, ptr %"%t18", align 1
  %116 = zext i1 %115 to i32
  switch i32 %116, label %bb35 [
    i32 1, label %bb36
  ]

bb34:                                             ; preds = %bb31
  call void @llvm.memset.p0.i64(ptr align 4 %variant47, i8 0, i64 4, i1 false)
  %117 = getelementptr inbounds nuw %ErrorKind, ptr %variant47, i32 0, i32 0
  store i32 16, ptr %117, align 4
  %118 = load %ErrorKind, ptr %variant47, align 4
  store %ErrorKind %118, ptr %_0, align 4
  br label %bb2

bb35:                                             ; preds = %bb33
  %119 = load i32, ptr %i, align 4
  store i32 %119, ptr %a48, align 4
  store i32 18, ptr %b49, align 4
  %120 = call i32 @cmp.i32(ptr %a48, ptr %b49)
  %121 = icmp eq i32 %120, 0
  store i1 %121, ptr %"%t19", align 1
  %122 = load i1, ptr %"%t19", align 1
  %123 = zext i1 %122 to i32
  switch i32 %123, label %bb37 [
    i32 1, label %bb38
  ]

bb36:                                             ; preds = %bb33
  call void @llvm.memset.p0.i64(ptr align 4 %variant50, i8 0, i64 4, i1 false)
  %124 = getelementptr inbounds nuw %ErrorKind, ptr %variant50, i32 0, i32 0
  store i32 17, ptr %124, align 4
  %125 = load %ErrorKind, ptr %variant50, align 4
  store %ErrorKind %125, ptr %_0, align 4
  br label %bb2

bb37:                                             ; preds = %bb35
  %126 = load i32, ptr %i, align 4
  store i32 %126, ptr %a51, align 4
  store i32 19, ptr %b52, align 4
  %127 = call i32 @cmp.i32(ptr %a51, ptr %b52)
  %128 = icmp eq i32 %127, 0
  store i1 %128, ptr %"%t20", align 1
  %129 = load i1, ptr %"%t20", align 1
  %130 = zext i1 %129 to i32
  switch i32 %130, label %bb39 [
    i32 1, label %bb40
  ]

bb38:                                             ; preds = %bb35
  call void @llvm.memset.p0.i64(ptr align 4 %variant53, i8 0, i64 4, i1 false)
  %131 = getelementptr inbounds nuw %ErrorKind, ptr %variant53, i32 0, i32 0
  store i32 18, ptr %131, align 4
  %132 = load %ErrorKind, ptr %variant53, align 4
  store %ErrorKind %132, ptr %_0, align 4
  br label %bb2

bb39:                                             ; preds = %bb37
  %133 = load i32, ptr %i, align 4
  store i32 %133, ptr %a54, align 4
  store i32 20, ptr %b55, align 4
  %134 = call i32 @cmp.i32(ptr %a54, ptr %b55)
  %135 = icmp eq i32 %134, 0
  store i1 %135, ptr %"%t21", align 1
  %136 = load i1, ptr %"%t21", align 1
  %137 = zext i1 %136 to i32
  switch i32 %137, label %bb41 [
    i32 1, label %bb42
  ]

bb40:                                             ; preds = %bb37
  call void @llvm.memset.p0.i64(ptr align 4 %variant56, i8 0, i64 4, i1 false)
  %138 = getelementptr inbounds nuw %ErrorKind, ptr %variant56, i32 0, i32 0
  store i32 19, ptr %138, align 4
  %139 = load %ErrorKind, ptr %variant56, align 4
  store %ErrorKind %139, ptr %_0, align 4
  br label %bb2

bb41:                                             ; preds = %bb39
  call void @llvm.memset.p0.i64(ptr align 4 %variant57, i8 0, i64 4, i1 false)
  %140 = getelementptr inbounds nuw %ErrorKind, ptr %variant57, i32 0, i32 0
  store i32 0, ptr %140, align 4
  %141 = load %ErrorKind, ptr %variant57, align 4
  store %ErrorKind %141, ptr %_0, align 4
  br label %bb2

bb42:                                             ; preds = %bb39
  call void @llvm.memset.p0.i64(ptr align 4 %variant58, i8 0, i64 4, i1 false)
  %142 = getelementptr inbounds nuw %ErrorKind, ptr %variant58, i32 0, i32 0
  store i32 20, ptr %142, align 4
  %143 = load %ErrorKind, ptr %variant58, align 4
  store %ErrorKind %143, ptr %_0, align 4
  br label %bb2

bb43:                                             ; No predecessors!
  unreachable
}

define internal i32 @cmp.i32(ptr %0, ptr %1) #0 {
entry:
  %2 = load i32, ptr %0, align 4
  %3 = load i32, ptr %1, align 4
  %4 = icmp slt i32 %2, %3
  %5 = icmp sgt i32 %2, %3
  %6 = select i1 %5, i32 1, i32 0
  %7 = select i1 %4, i32 -1, i32 %6
  ret i32 %7
}

declare void @deus_free(ptr)

define internal void @drop.IoError(ptr %0) #0 {
entry:
  %1 = getelementptr inbounds nuw %IoError, ptr %0, i32 0, i32 1
  %2 = getelementptr inbounds nuw %IoError, ptr %0, i32 0, i32 2
  %3 = getelementptr inbounds nuw %IoError, ptr %0, i32 0, i32 0
  call void @drop.String(ptr %3)
  ret void
}

declare void @deus_iter_free(ptr)

define internal void @dbg.usize(ptr %0, ptr %1) #0 {
entry:
  %2 = load i64, ptr %0, align 8
  call void @deus_fmt_int_plain(ptr %1, i64 %2, i64 0, i1 false)
  ret void
}

declare void @deus_fmt_int_plain(ptr, i64, i64, i1)

define i32 @main(i32 %0, ptr %1) #0 {
entry:
  %v = alloca %IoError, align 8
  %fmt = alloca %deus.vec, align 8
  %enum = alloca %Result, align 8
  call void @deus_rt_init(i32 %0, ptr %1)
  call void @deus_rt_backtrace(i32 1)
  %2 = call %Result @deus.main()
  %3 = extractvalue %Result %2, 0
  %4 = icmp eq i32 %3, 1
  br i1 %4, label %err, label %ok

err:                                              ; preds = %entry
  store %Result %2, ptr %enum, align 8
  %5 = getelementptr inbounds nuw %Result, ptr %enum, i32 0, i32 1
  %6 = getelementptr inbounds nuw { %IoError }, ptr %5, i32 0, i32 0
  %7 = load %IoError, ptr %6, align 8
  call void @deus_string_init(ptr %fmt)
  store %IoError %7, ptr %v, align 8
  call void @dbg.IoError(ptr %v, ptr %fmt)
  %8 = load %deus.vec, ptr %fmt, align 8
  %9 = extractvalue %deus.vec %8, 0
  %10 = extractvalue %deus.vec %8, 1
  call void @deus_write(i32 2, ptr @str.60, i64 7)
  call void @deus_write(i32 2, ptr %9, i64 %10)
  call void @deus_write(i32 2, ptr @str.3, i64 1)
  call void @deus_rt_exit(i32 1) #2
  unreachable

ok:                                               ; preds = %entry
  call void @deus_rt_exit(i32 0) #2
  unreachable
}

declare void @deus_rt_init(i32, ptr)

declare void @deus_rt_backtrace(i32)

define internal void @dbg.IoError(ptr %0, ptr %1) #0 {
entry:
  %formatter = alloca ptr, align 8
  store ptr %1, ptr %formatter, align 8
  %2 = call %Result.6 @deus.fmt(ptr %0, ptr %formatter)
  ret void
}

; Function Attrs: noreturn
declare void @deus_rt_exit(i32) #2

define internal %Result.6 @deus.fmt(ptr %0, ptr %1) #0 {
entry:
  %variant = alloca %Result.6, align 8
  %v = alloca %ErrorKind, align 8
  %fmt.arg1 = alloca ptr, align 8
  %fmt.arg = alloca ptr, align 8
  %"%t7" = alloca ptr, align 8
  %"%t6" = alloca ptr, align 8
  %"%t5" = alloca ptr, align 8
  %"%t4" = alloca ptr, align 8
  %"%t3" = alloca %deus.vec, align 8
  %f = alloca ptr, align 8
  %self = alloca ptr, align 8
  %_0 = alloca %Result.6, align 8
  store ptr %0, ptr %self, align 8
  store ptr %1, ptr %f, align 8
  br label %bb0

bb0:                                              ; preds = %entry
  %2 = load ptr, ptr %self, align 8
  %3 = getelementptr inbounds nuw %IoError, ptr %2, i32 0, i32 1
  store ptr %3, ptr %"%t4", align 8
  %4 = load ptr, ptr %self, align 8
  %5 = getelementptr inbounds nuw %IoError, ptr %4, i32 0, i32 0
  store ptr %5, ptr %"%t5", align 8
  %6 = load ptr, ptr %"%t4", align 8
  store ptr %6, ptr %fmt.arg, align 8
  %7 = load ptr, ptr %"%t5", align 8
  store ptr %7, ptr %fmt.arg1, align 8
  store %deus.vec zeroinitializer, ptr %"%t3", align 8
  %8 = load ptr, ptr %f, align 8
  store ptr %8, ptr %"%t6", align 8
  %9 = load ptr, ptr %"%t6", align 8
  store ptr %9, ptr %"%t7", align 8
  %10 = load ptr, ptr %fmt.arg, align 8
  %11 = load ptr, ptr %fmt.arg1, align 8
  %12 = load ptr, ptr %"%t7", align 8
  %13 = load ptr, ptr %12, align 8
  call void @deus_string_push_str(ptr %13, ptr @str.61, i64 8)
  %14 = load %ErrorKind, ptr %10, align 4
  store %ErrorKind %14, ptr %v, align 4
  call void @dbg.ErrorKind(ptr %v, ptr %13)
  call void @deus_string_push_str(ptr %13, ptr @str.62, i64 2)
  %15 = load %deus.vec, ptr %11, align 8
  %16 = extractvalue %deus.vec %15, 0
  %17 = icmp eq ptr %16, null
  %buf = select i1 %17, ptr inttoptr (i64 1 to ptr), ptr %16
  %18 = extractvalue %deus.vec %15, 1
  call void @deus_fmt_str_debug(ptr %13, ptr %buf, i64 %18)
  call void @deus_string_push_str(ptr %13, ptr @str.63, i64 1)
  call void @llvm.memset.p0.i64(ptr align 4 %variant, i8 0, i64 4, i1 false)
  %19 = getelementptr inbounds nuw %Result.6, ptr %variant, i32 0, i32 0
  store i32 0, ptr %19, align 4
  %20 = getelementptr inbounds nuw %Result.6, ptr %variant, i32 0, i32 1
  %21 = getelementptr inbounds nuw { %deus.unit }, ptr %20, i32 0, i32 0
  store %deus.unit undef, ptr %21, align 1
  %22 = load %Result.6, ptr %variant, align 4
  store %Result.6 %22, ptr %_0, align 4
  br label %bb2

bb1:                                              ; preds = %bb2
  %23 = load %Result.6, ptr %_0, align 4
  ret %Result.6 %23

bb2:                                              ; preds = %bb0
  br label %bb1
}

define internal void @dbg.ErrorKind(ptr %0, ptr %1) #0 {
entry:
  %2 = load %ErrorKind, ptr %0, align 4
  %3 = extractvalue %ErrorKind %2, 0
  switch i32 %3, label %done [
    i32 0, label %Other
    i32 1, label %NotFound
    i32 2, label %PermissionDenied
    i32 3, label %ConnectionRefused
    i32 4, label %ConnectionReset
    i32 5, label %ConnectionAborted
    i32 6, label %NotConnected
    i32 7, label %AddrInUse
    i32 8, label %AddrNotAvailable
    i32 9, label %BrokenPipe
    i32 10, label %AlreadyExists
    i32 11, label %WouldBlock
    i32 12, label %InvalidInput
    i32 13, label %TimedOut
    i32 14, label %Interrupted
    i32 15, label %NotADirectory
    i32 16, label %IsADirectory
    i32 17, label %DirectoryNotEmpty
    i32 18, label %StorageFull
    i32 19, label %ReadOnlyFilesystem
    i32 20, label %OutOfMemory
    i32 21, label %InvalidData
    i32 22, label %UnexpectedEof
    i32 23, label %WriteZero
    i32 24, label %Unsupported
  ]

done:                                             ; preds = %Unsupported, %WriteZero, %UnexpectedEof, %InvalidData, %OutOfMemory, %ReadOnlyFilesystem, %StorageFull, %DirectoryNotEmpty, %IsADirectory, %NotADirectory, %Interrupted, %TimedOut, %InvalidInput, %WouldBlock, %AlreadyExists, %BrokenPipe, %AddrNotAvailable, %AddrInUse, %NotConnected, %ConnectionAborted, %ConnectionReset, %ConnectionRefused, %PermissionDenied, %NotFound, %Other, %entry
  ret void

Other:                                            ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.64, i64 5)
  br label %done

NotFound:                                         ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.65, i64 8)
  br label %done

PermissionDenied:                                 ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.66, i64 16)
  br label %done

ConnectionRefused:                                ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.67, i64 17)
  br label %done

ConnectionReset:                                  ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.68, i64 15)
  br label %done

ConnectionAborted:                                ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.69, i64 17)
  br label %done

NotConnected:                                     ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.70, i64 12)
  br label %done

AddrInUse:                                        ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.71, i64 9)
  br label %done

AddrNotAvailable:                                 ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.72, i64 16)
  br label %done

BrokenPipe:                                       ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.73, i64 10)
  br label %done

AlreadyExists:                                    ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.74, i64 13)
  br label %done

WouldBlock:                                       ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.75, i64 10)
  br label %done

InvalidInput:                                     ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.76, i64 12)
  br label %done

TimedOut:                                         ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.77, i64 8)
  br label %done

Interrupted:                                      ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.78, i64 11)
  br label %done

NotADirectory:                                    ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.79, i64 13)
  br label %done

IsADirectory:                                     ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.80, i64 12)
  br label %done

DirectoryNotEmpty:                                ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.81, i64 17)
  br label %done

StorageFull:                                      ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.82, i64 11)
  br label %done

ReadOnlyFilesystem:                               ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.83, i64 18)
  br label %done

OutOfMemory:                                      ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.84, i64 11)
  br label %done

InvalidData:                                      ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.85, i64 11)
  br label %done

UnexpectedEof:                                    ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.86, i64 13)
  br label %done

WriteZero:                                        ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.87, i64 9)
  br label %done

Unsupported:                                      ; preds = %entry
  call void @deus_string_push_str(ptr %1, ptr @str.88, i64 11)
  br label %done
}

declare void @deus_fmt_str_debug(ptr, ptr, i64)

attributes #0 = { "frame-pointer"="all" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(argmem: write) }
attributes #2 = { noreturn }
attributes #3 = { nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none) }
