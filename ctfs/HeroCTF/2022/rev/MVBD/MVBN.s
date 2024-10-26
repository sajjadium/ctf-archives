; ModuleID = 'source.c'
source_filename = "source.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@key = dso_local global [33 x i8] c"7 >)\04\09\00\102\1A}5 q\130L75\19\1Cu|* 5>v\15v/2\02", align 16
@.str = private unnamed_addr constant [18 x i8] c"Usage: %s <flag>\0A\00", align 1
@.str.1 = private unnamed_addr constant [31 x i8] c"[-] Bad password... Try again.\00", align 1
@.str.2 = private unnamed_addr constant [46 x i8] c"[+] Well done ! You can validate with flag :)\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @check_password(i8* %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  store i8* %0, i8** %3, align 8
  %5 = load i8*, i8** %3, align 8
  %6 = call i64 @strlen(i8* %5) #3
  %7 = icmp ne i64 %6, 33
  br i1 %7, label %8, label %9

8:                                                ; preds = %1
  store i32 -1, i32* %2, align 4
  br label %40

9:                                                ; preds = %1
  store i32 0, i32* %4, align 4
  br label %10

10:                                               ; preds = %36, %9
  %11 = load i32, i32* %4, align 4
  %12 = icmp slt i32 %11, 33
  br i1 %12, label %13, label %39

13:                                               ; preds = %10
  %14 = load i32, i32* %4, align 4
  %15 = srem i32 %14, 4
  %16 = add nsw i32 4194304, %15
  %17 = sext i32 %16 to i64
  %18 = inttoptr i64 %17 to i8*
  %19 = load i8, i8* %18, align 1
  %20 = zext i8 %19 to i32
  %21 = load i8*, i8** %3, align 8
  %22 = load i32, i32* %4, align 4
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds i8, i8* %21, i64 %23
  %25 = load i8, i8* %24, align 1
  %26 = sext i8 %25 to i32
  %27 = xor i32 %20, %26
  %28 = load i32, i32* %4, align 4
  %29 = sext i32 %28 to i64
  %30 = getelementptr inbounds [33 x i8], [33 x i8]* @key, i64 0, i64 %29
  %31 = load i8, i8* %30, align 1
  %32 = zext i8 %31 to i32
  %33 = icmp ne i32 %27, %32
  br i1 %33, label %34, label %35

34:                                               ; preds = %13
  store i32 1, i32* %2, align 4
  br label %40

35:                                               ; preds = %13
  br label %36

36:                                               ; preds = %35
  %37 = load i32, i32* %4, align 4
  %38 = add nsw i32 %37, 1
  store i32 %38, i32* %4, align 4
  br label %10, !llvm.loop !4

39:                                               ; preds = %10
  store i32 0, i32* %2, align 4
  br label %40

40:                                               ; preds = %39, %34, %8
  %41 = load i32, i32* %2, align 4
  ret i32 %41
}

; Function Attrs: nounwind readonly willreturn
declare dso_local i64 @strlen(i8*) #1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main(i32 %0, i8** %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i8**, align 8
  store i32 0, i32* %3, align 4
  store i32 %0, i32* %4, align 4
  store i8** %1, i8*** %5, align 8
  %6 = load i32, i32* %4, align 4
  %7 = icmp ne i32 %6, 2
  br i1 %7, label %8, label %13

8:                                                ; preds = %2
  %9 = load i8**, i8*** %5, align 8
  %10 = getelementptr inbounds i8*, i8** %9, i64 0
  %11 = load i8*, i8** %10, align 8
  %12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([18 x i8], [18 x i8]* @.str, i64 0, i64 0), i8* %11)
  store i32 1, i32* %3, align 4
  br label %24

13:                                               ; preds = %2
  %14 = load i8**, i8*** %5, align 8
  %15 = getelementptr inbounds i8*, i8** %14, i64 1
  %16 = load i8*, i8** %15, align 8
  %17 = call i32 @check_password(i8* %16)
  %18 = icmp ne i32 %17, 0
  br i1 %18, label %19, label %21

19:                                               ; preds = %13
  %20 = call i32 @puts(i8* getelementptr inbounds ([31 x i8], [31 x i8]* @.str.1, i64 0, i64 0))
  br label %23

21:                                               ; preds = %13
  %22 = call i32 @puts(i8* getelementptr inbounds ([46 x i8], [46 x i8]* @.str.2, i64 0, i64 0))
  br label %23

23:                                               ; preds = %21, %19
  store i32 0, i32* %3, align 4
  br label %24

24:                                               ; preds = %23, %8
  %25 = load i32, i32* %3, align 4
  ret i32 %25
}

declare dso_local i32 @printf(i8*, ...) #2

declare dso_local i32 @puts(i8*) #2

attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nounwind readonly willreturn "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind readonly willreturn }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"uwtable", i32 1}
!2 = !{i32 7, !"frame-pointer", i32 2}
!3 = !{!"Ubuntu clang version 13.0.0-2"}
!4 = distinct !{!4, !5}
!5 = !{!"llvm.loop.mustprogress"}
