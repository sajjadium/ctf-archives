; ModuleID = 'llvm.c'
source_filename = "llvm.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@flag = dso_local global [68 x i8] c",/,\CF\CD\09\09N\09d/\CD\0F\C4l\84\09\8D\84o\8C\84n\AE\09\09N\8Co\C4d\ACN\84$\84\A4\8C\8E\8E\CE\E4o\E4/\8E\09$M\8EO\8C\AEN\E4\8E\A4ndn\8ClO\84no\09d", align 16
@a1 = dso_local global [68 x i8] c"\1E%\0A?\1A\04\091\0E\01@\13\15\198+\1F\05\1BC2\02:#\1C> 3.'7\00$\1D;\0CA\07=\22,*\0D\06B\0B\03\08\0F\1265&(0/9)4\10\17\18\14<\11-!\16", align 16
@a2 = dso_local global [68 x i8] c"\10\0A58\1B! \07?\05\04\01=\18\0E.,\1D<\1A@\1C\1F(\06\14\15\0003\09\02C2:\0C\12\11\179%)\19\0D-*\08\16\1E/A&$';+\0F6#\13\0B\224>\0371B", align 16
@a3 = dso_local global [68 x i8] c"';>\07&\16\1E-:(\03+1\02\0AA\1C7\044*\1B\17<\1F\12@\14\11\2220\0E.6\18\19?\0F3/\0B$\1D8\00\0C5\09!\1AB\01\15\13\05\08%,C\06# =\0D9)\10", align 16
@.str = private unnamed_addr constant [6 x i8] c"%100s\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"Access Granted :(\00", align 1
@.str.2 = private unnamed_addr constant [17 x i8] c"Access Denied :)\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [100 x i8], align 16
  %3 = alloca i32, align 4
  %4 = alloca [100 x i8], align 16
  %5 = alloca [100 x i8], align 16
  %6 = alloca [100 x i8], align 16
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %10 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 0
  %11 = call i32 (i8*, ...) @__isoc99_scanf(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str, i64 0, i64 0), i8* %10)
  %12 = call i32 @getchar()
  %13 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 0
  %14 = call i64 @strlen(i8* %13) #3
  %15 = trunc i64 %14 to i32
  store i32 %15, i32* %3, align 4
  store i32 0, i32* %7, align 4
  br label %16

16:                                               ; preds = %34, %0
  %17 = load i32, i32* %7, align 4
  %18 = load i32, i32* %3, align 4
  %19 = icmp slt i32 %17, %18
  br i1 %19, label %20, label %37

20:                                               ; preds = %16
  %21 = load i32, i32* %7, align 4
  %22 = sext i32 %21 to i64
  %23 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 %22
  %24 = load i8, i8* %23, align 1
  %25 = sext i8 %24 to i32
  %26 = xor i32 %25, 23
  %27 = trunc i32 %26 to i8
  %28 = load i32, i32* %7, align 4
  %29 = sext i32 %28 to i64
  %30 = getelementptr inbounds [68 x i8], [68 x i8]* @a1, i64 0, i64 %29
  %31 = load i8, i8* %30, align 1
  %32 = zext i8 %31 to i64
  %33 = getelementptr inbounds [100 x i8], [100 x i8]* %4, i64 0, i64 %32
  store i8 %27, i8* %33, align 1
  br label %34

34:                                               ; preds = %20
  %35 = load i32, i32* %7, align 4
  %36 = add nsw i32 %35, 1
  store i32 %36, i32* %7, align 4
  br label %16

37:                                               ; preds = %16
  store i32 0, i32* %8, align 4
  br label %38

38:                                               ; preds = %64, %37
  %39 = load i32, i32* %8, align 4
  %40 = load i32, i32* %3, align 4
  %41 = icmp slt i32 %39, %40
  br i1 %41, label %42, label %67

42:                                               ; preds = %38
  %43 = load i32, i32* %8, align 4
  %44 = sext i32 %43 to i64
  %45 = getelementptr inbounds [100 x i8], [100 x i8]* %4, i64 0, i64 %44
  %46 = load i8, i8* %45, align 1
  %47 = zext i8 %46 to i32
  %48 = and i32 %47, 15
  %49 = shl i32 %48, 4
  %50 = load i32, i32* %8, align 4
  %51 = sext i32 %50 to i64
  %52 = getelementptr inbounds [100 x i8], [100 x i8]* %4, i64 0, i64 %51
  %53 = load i8, i8* %52, align 1
  %54 = zext i8 %53 to i32
  %55 = ashr i32 %54, 4
  %56 = add nsw i32 %49, %55
  %57 = trunc i32 %56 to i8
  %58 = load i32, i32* %8, align 4
  %59 = sext i32 %58 to i64
  %60 = getelementptr inbounds [68 x i8], [68 x i8]* @a2, i64 0, i64 %59
  %61 = load i8, i8* %60, align 1
  %62 = zext i8 %61 to i64
  %63 = getelementptr inbounds [100 x i8], [100 x i8]* %5, i64 0, i64 %62
  store i8 %57, i8* %63, align 1
  br label %64

64:                                               ; preds = %42
  %65 = load i32, i32* %8, align 4
  %66 = add nsw i32 %65, 1
  store i32 %66, i32* %8, align 4
  br label %38

67:                                               ; preds = %38
  store i32 0, i32* %9, align 4
  br label %68

68:                                               ; preds = %96, %67
  %69 = load i32, i32* %9, align 4
  %70 = load i32, i32* %3, align 4
  %71 = icmp slt i32 %69, %70
  br i1 %71, label %72, label %99

72:                                               ; preds = %68
  %73 = load i32, i32* %9, align 4
  %74 = sext i32 %73 to i64
  %75 = getelementptr inbounds [100 x i8], [100 x i8]* %5, i64 0, i64 %74
  %76 = load i8, i8* %75, align 1
  %77 = zext i8 %76 to i32
  %78 = shl i32 %77, 1
  %79 = load i32, i32* %9, align 4
  %80 = sext i32 %79 to i64
  %81 = getelementptr inbounds [100 x i8], [100 x i8]* %5, i64 0, i64 %80
  %82 = load i8, i8* %81, align 1
  %83 = zext i8 %82 to i32
  %84 = and i32 %83, 128
  %85 = icmp eq i32 %84, 128
  %86 = zext i1 %85 to i64
  %87 = select i1 %85, i32 1, i32 0
  %88 = or i32 %78, %87
  %89 = trunc i32 %88 to i8
  %90 = load i32, i32* %9, align 4
  %91 = sext i32 %90 to i64
  %92 = getelementptr inbounds [68 x i8], [68 x i8]* @a3, i64 0, i64 %91
  %93 = load i8, i8* %92, align 1
  %94 = zext i8 %93 to i64
  %95 = getelementptr inbounds [100 x i8], [100 x i8]* %6, i64 0, i64 %94
  store i8 %89, i8* %95, align 1
  br label %96

96:                                               ; preds = %72
  %97 = load i32, i32* %9, align 4
  %98 = add nsw i32 %97, 1
  store i32 %98, i32* %9, align 4
  br label %68

99:                                               ; preds = %68
  %100 = getelementptr inbounds [100 x i8], [100 x i8]* %6, i64 0, i64 0
  %101 = load i32, i32* %3, align 4
  %102 = sext i32 %101 to i64
  %103 = call i32 @memcmp(i8* getelementptr inbounds ([68 x i8], [68 x i8]* @flag, i64 0, i64 0), i8* %100, i64 %102) #3
  %104 = icmp eq i32 %103, 0
  br i1 %104, label %105, label %107

105:                                              ; preds = %99
  %106 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str.1, i64 0, i64 0))
  br label %109

107:                                              ; preds = %99
  %108 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([17 x i8], [17 x i8]* @.str.2, i64 0, i64 0))
  br label %109

109:                                              ; preds = %107, %105
  ret i32 0
}

declare dso_local i32 @__isoc99_scanf(i8*, ...) #1

declare dso_local i32 @getchar() #1

; Function Attrs: nounwind readonly
declare dso_local i64 @strlen(i8*) #2

; Function Attrs: nounwind readonly
declare dso_local i32 @memcmp(i8*, i8*, i64) #2

declare dso_local i32 @printf(i8*, ...) #1

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind readonly "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readonly }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0-4ubuntu1 "}
