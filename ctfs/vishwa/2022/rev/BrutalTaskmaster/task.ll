@format = global [64 x i8] c"\0A\F0\9F\98\82\F0\9F\91\8C\F0\9F\98\82\F0\9F\91\8C\F0\9F\98\82\F0\9F\91\8C flag{%s} \F0\9F\91\8C\F0\9F\98\82\F0\9F\91\8C\F0\9F\98\82\F0\9F\91\8C\F0\9F\98\82\0A\0A\00\00\00", align 16
@flag = global [64 x i8] c"\1DU#hJ7.8\06\16\03rUO=[bg9JmtGt`7U\0BnNjD\01\03\120\19;OVIaM\00\08,qu<g\1D;K\00}Y\00\00\00\00\00\00\00\00", align 16
@what = global [64 x i8] c"\17/'\17\1DJy\03,\11\1E&\0AexjONacA-&\01LANH'.&\12>#'Z\0FO\0B%:(&HI\0CJylL'\1EmtdC\00\00\00\00\00\00\00\00", align 16
@secret = global [64 x i8] c"B\0A|_\22\06\1Bg7#\5CF\0A)\090Q8_{Y\13\18\0DP\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00", align 16
@.str = private unnamed_addr constant [49 x i8] c"Only the chosen one will know what the flag is!\0A\00", align 1
@.str.1 = private unnamed_addr constant [25 x i8] c"Are you the chosen one?\0A\00", align 1
@.str.2 = private unnamed_addr constant [7 x i8] c"flag: \00", align 1
@.str.3 = private unnamed_addr constant [5 x i8] c"%64s\00", align 1
@.str.4 = private unnamed_addr constant [81 x i8] c"\0A\F0\9F\98\A0\F0\9F\98\A1\F0\9F\98\A0\F0\9F\98\A1\F0\9F\98\A0\F0\9F\98\A1 You are not the chosen one! \F0\9F\98\A1\F0\9F\98\A0\F0\9F\98\A1\F0\9F\98\A0\F0\9F\98\A1\F0\9F\98\A0\0A\0A\00", align 1

define i32 @check(i8*) #0 {
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i8* %0, i8** %2, align 8
  store i32 1, i32* %3, align 4
  store i32 0, i32* %4, align 4
  br label %5

; <label>:5:                                      ; preds = %36, %1
  %6 = load i32, i32* %4, align 4
  %7 = sext i32 %6 to i64
  %8 = call i64 @strlen(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @what, i32 0, i32 0)) #3
  %9 = icmp ult i64 %7, %8
  br i1 %9, label %10, label %39

; <label>:10:                                     ; preds = %5
  %11 = load i8*, i8** %2, align 8
  %12 = load i32, i32* %4, align 4
  %13 = sext i32 %12 to i64
  %14 = getelementptr inbounds i8, i8* %11, i64 %13
  %15 = load i8, i8* %14, align 1
  %16 = sext i8 %15 to i32
  %17 = load i8*, i8** %2, align 8
  %18 = load i32, i32* %4, align 4
  %19 = add nsw i32 %18, 1
  %20 = sext i32 %19 to i64
  %21 = call i64 @strlen(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @what, i32 0, i32 0)) #3
  %22 = urem i64 %20, %21
  %23 = getelementptr inbounds i8, i8* %17, i64 %22
  %24 = load i8, i8* %23, align 1
  %25 = sext i8 %24 to i32
  %26 = xor i32 %16, %25
  %27 = load i32, i32* %4, align 4
  %28 = sext i32 %27 to i64
  %29 = getelementptr inbounds [64 x i8], [64 x i8]* @what, i64 0, i64 %28
  %30 = load i8, i8* %29, align 1
  %31 = sext i8 %30 to i32
  %32 = icmp eq i32 %26, %31
  %33 = zext i1 %32 to i32
  %34 = load i32, i32* %3, align 4
  %35 = and i32 %34, %33
  store i32 %35, i32* %3, align 4
  br label %36

; <label>:36:                                     ; preds = %10
  %37 = load i32, i32* %4, align 4
  %38 = add nsw i32 %37, 1
  store i32 %38, i32* %4, align 4
  br label %5

; <label>:39:                                     ; preds = %5
  %40 = load i32, i32* %3, align 4
  ret i32 %40
}

declare i64 @strlen(i8*) #1

define i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [64 x i8], align 16
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([49 x i8], [49 x i8]* @.str, i32 0, i32 0))
  %6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([25 x i8], [25 x i8]* @.str.1, i32 0, i32 0))
  %7 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.2, i32 0, i32 0))
  %8 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0
  %9 = call i32 (i8*, ...) @__isoc99_scanf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.3, i32 0, i32 0), i8* %8)
  %10 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0
  %11 = call i64 @strlen(i8* %10) #3
  %12 = call i64 @strlen(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @what, i32 0, i32 0)) #3
  %13 = icmp ne i64 %11, %12
  br i1 %13, label %14, label %16

; <label>:14:                                     ; preds = %0
  %15 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([81 x i8], [81 x i8]* @.str.4, i32 0, i32 0))
  store i32 1, i32* %1, align 4
  br label %83

; <label>:16:                                     ; preds = %0
  %17 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0
  %18 = call i32 @check(i8* %17)
  %19 = icmp ne i32 %18, 0
  br i1 %19, label %20, label %51

; <label>:20:                                     ; preds = %16
  store i32 0, i32* %3, align 4
  br label %21

; <label>:21:                                     ; preds = %45, %20
  %22 = load i32, i32* %3, align 4
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0
  %25 = call i64 @strlen(i8* %24) #3
  %26 = icmp ult i64 %23, %25
  br i1 %26, label %27, label %48

; <label>:27:                                     ; preds = %21
  %28 = load i32, i32* %3, align 4
  %29 = sext i32 %28 to i64
  %30 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i64 0, i64 %29
  %31 = load i8, i8* %30, align 1
  %32 = sext i8 %31 to i32
  %33 = load i32, i32* %3, align 4
  %34 = sext i32 %33 to i64
  %35 = call i64 @strlen(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @secret, i32 0, i32 0)) #3
  %36 = urem i64 %34, %35
  %37 = getelementptr inbounds [64 x i8], [64 x i8]* @secret, i64 0, i64 %36
  %38 = load i8, i8* %37, align 1
  %39 = sext i8 %38 to i32
  %40 = xor i32 %32, %39
  %41 = trunc i32 %40 to i8
  %42 = load i32, i32* %3, align 4
  %43 = sext i32 %42 to i64
  %44 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i64 0, i64 %43
  store i8 %41, i8* %44, align 1
  br label %45

; <label>:45:                                     ; preds = %27
  %46 = load i32, i32* %3, align 4
  %47 = add nsw i32 %46, 1
  store i32 %47, i32* %3, align 4
  br label %21

; <label>:48:                                     ; preds = %21
  %49 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0
  %50 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @format, i32 0, i32 0), i8* %49)
  br label %82

; <label>:51:                                     ; preds = %16
  store i32 0, i32* %4, align 4
  br label %52

; <label>:52:                                     ; preds = %76, %51
  %53 = load i32, i32* %4, align 4
  %54 = sext i32 %53 to i64
  %55 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0
  %56 = call i64 @strlen(i8* %55) #3
  %57 = icmp ult i64 %54, %56
  br i1 %57, label %58, label %79

; <label>:58:                                     ; preds = %52
  %59 = load i32, i32* %4, align 4
  %60 = sext i32 %59 to i64
  %61 = getelementptr inbounds [64 x i8], [64 x i8]* @flag, i64 0, i64 %60
  %62 = load i8, i8* %61, align 1
  %63 = sext i8 %62 to i32
  %64 = load i32, i32* %4, align 4
  %65 = sext i32 %64 to i64
  %66 = call i64 @strlen(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @secret, i32 0, i32 0)) #3
  %67 = urem i64 %65, %66
  %68 = getelementptr inbounds [64 x i8], [64 x i8]* @secret, i64 0, i64 %67
  %69 = load i8, i8* %68, align 1
  %70 = sext i8 %69 to i32
  %71 = xor i32 %63, %70
  %72 = trunc i32 %71 to i8
  %73 = load i32, i32* %4, align 4
  %74 = sext i32 %73 to i64
  %75 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i64 0, i64 %74
  store i8 %72, i8* %75, align 1
  br label %76

; <label>:76:                                     ; preds = %58
  %77 = load i32, i32* %4, align 4
  %78 = add nsw i32 %77, 1
  store i32 %78, i32* %4, align 4
  br label %52

; <label>:79:                                     ; preds = %52
  %80 = getelementptr inbounds [64 x i8], [64 x i8]* %2, i32 0, i32 0
  %81 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([64 x i8], [64 x i8]* @format, i32 0, i32 0), i8* %80)
  br label %82

; <label>:82:                                     ; preds = %79, %48
  store i32 0, i32* %1, align 4
  br label %83

; <label>:83:                                     ; preds = %82, %14
  %84 = load i32, i32* %1, align 4
  ret i32 %84
}

declare i32 @printf(i8*, ...) #2

declare i32 @__isoc99_scanf(i8*, ...) #2
