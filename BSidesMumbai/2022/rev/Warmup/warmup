; ModuleID = 'warmup.c'
source_filename = "warmup.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [17 x i8] c"Enter a string: \00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.2 = private unnamed_addr constant [22 x i8] c"The flag is correct!\0A\00", align 1
@.str.3 = private unnamed_addr constant [24 x i8] c"The flag is incorrect.\0A\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [100 x i8], align 16
  store i32 0, i32* %1, align 4
  %3 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([17 x i8], [17 x i8]* @.str, i64 0, i64 0))
  %4 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 0
  %5 = call i32 (i8*, ...) @scanf(i8* noundef getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1, i64 0, i64 0), i8* noundef %4)
  %6 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 0
  %7 = call i64 @strlen(i8* noundef %6)
  %8 = icmp ne i64 %7, 39
  br i1 %8, label %9, label %10

9:                                                ; preds = %0
  call void @exit(i32 noundef 0) #3
  unreachable

10:                                               ; preds = %0
  %11 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 28
  %12 = load i8, i8* %11, align 4
  %13 = sext i8 %12 to i32
  %14 = icmp eq i32 %13, 55
  br i1 %14, label %15, label %207

15:                                               ; preds = %10
  %16 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 30
  %17 = load i8, i8* %16, align 2
  %18 = sext i8 %17 to i32
  %19 = icmp eq i32 %18, 110
  br i1 %19, label %20, label %207

20:                                               ; preds = %15
  %21 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 29
  %22 = load i8, i8* %21, align 1
  %23 = sext i8 %22 to i32
  %24 = icmp eq i32 %23, 49
  br i1 %24, label %25, label %207

25:                                               ; preds = %20
  %26 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 36
  %27 = load i8, i8* %26, align 4
  %28 = sext i8 %27 to i32
  %29 = icmp eq i32 %28, 53
  br i1 %29, label %30, label %207

30:                                               ; preds = %25
  %31 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 13
  %32 = load i8, i8* %31, align 1
  %33 = sext i8 %32 to i32
  %34 = icmp eq i32 %33, 121
  br i1 %34, label %35, label %207

35:                                               ; preds = %30
  %36 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 18
  %37 = load i8, i8* %36, align 2
  %38 = sext i8 %37 to i32
  %39 = icmp eq i32 %38, 95
  br i1 %39, label %40, label %207

40:                                               ; preds = %35
  %41 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 2
  %42 = load i8, i8* %41, align 2
  %43 = sext i8 %42 to i32
  %44 = icmp eq i32 %43, 77
  br i1 %44, label %45, label %207

45:                                               ; preds = %40
  %46 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 15
  %47 = load i8, i8* %46, align 1
  %48 = sext i8 %47 to i32
  %49 = icmp eq i32 %48, 51
  br i1 %49, label %50, label %207

50:                                               ; preds = %45
  %51 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 34
  %52 = load i8, i8* %51, align 2
  %53 = sext i8 %52 to i32
  %54 = icmp eq i32 %53, 48
  br i1 %54, label %55, label %207

55:                                               ; preds = %50
  %56 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 7
  %57 = load i8, i8* %56, align 1
  %58 = sext i8 %57 to i32
  %59 = icmp eq i32 %58, 48
  br i1 %59, label %60, label %207

60:                                               ; preds = %55
  %61 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 24
  %62 = load i8, i8* %61, align 8
  %63 = sext i8 %62 to i32
  %64 = icmp eq i32 %63, 102
  br i1 %64, label %65, label %207

65:                                               ; preds = %60
  %66 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 17
  %67 = load i8, i8* %66, align 1
  %68 = sext i8 %67 to i32
  %69 = icmp eq i32 %68, 102
  br i1 %69, label %70, label %207

70:                                               ; preds = %65
  %71 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 26
  %72 = load i8, i8* %71, align 2
  %73 = sext i8 %72 to i32
  %74 = icmp eq i32 %73, 48
  br i1 %74, label %75, label %207

75:                                               ; preds = %70
  %76 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 25
  %77 = load i8, i8* %76, align 1
  %78 = sext i8 %77 to i32
  %79 = icmp eq i32 %78, 49
  br i1 %79, label %80, label %207

80:                                               ; preds = %75
  %81 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 10
  %82 = load i8, i8* %81, align 2
  %83 = sext i8 %82 to i32
  %84 = icmp eq i32 %83, 100
  br i1 %84, label %85, label %207

85:                                               ; preds = %80
  %86 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 27
  %87 = load i8, i8* %86, align 1
  %88 = sext i8 %87 to i32
  %89 = icmp eq i32 %88, 52
  br i1 %89, label %90, label %207

90:                                               ; preds = %85
  %91 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 3
  %92 = load i8, i8* %91, align 1
  %93 = sext i8 %92 to i32
  %94 = icmp eq i32 %93, 123
  br i1 %94, label %95, label %207

95:                                               ; preds = %90
  %96 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 23
  %97 = load i8, i8* %96, align 1
  %98 = sext i8 %97 to i32
  %99 = icmp eq i32 %98, 95
  br i1 %99, label %100, label %207

100:                                              ; preds = %95
  %101 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 19
  %102 = load i8, i8* %101, align 1
  %103 = sext i8 %102 to i32
  %104 = icmp eq i32 %103, 49
  br i1 %104, label %105, label %207

105:                                              ; preds = %100
  %106 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 21
  %107 = load i8, i8* %106, align 1
  %108 = sext i8 %107 to i32
  %109 = icmp eq i32 %108, 95
  br i1 %109, label %110, label %207

110:                                              ; preds = %105
  %111 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 31
  %112 = load i8, i8* %111, align 1
  %113 = sext i8 %112 to i32
  %114 = icmp eq i32 %113, 57
  br i1 %114, label %115, label %207

115:                                              ; preds = %110
  %116 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 8
  %117 = load i8, i8* %116, align 8
  %118 = sext i8 %117 to i32
  %119 = icmp eq i32 %118, 117
  br i1 %119, label %120, label %207

120:                                              ; preds = %115
  %121 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 37
  %122 = load i8, i8* %121, align 1
  %123 = sext i8 %122 to i32
  %124 = icmp eq i32 %123, 51
  br i1 %124, label %125, label %207

125:                                              ; preds = %120
  %126 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 11
  %127 = load i8, i8* %126, align 1
  %128 = sext i8 %127 to i32
  %129 = icmp eq i32 %128, 95
  br i1 %129, label %130, label %207

130:                                              ; preds = %125
  %131 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 33
  %132 = load i8, i8* %131, align 1
  %133 = sext i8 %132 to i32
  %134 = icmp eq i32 %133, 104
  br i1 %134, label %135, label %207

135:                                              ; preds = %130
  %136 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 1
  %137 = load i8, i8* %136, align 1
  %138 = sext i8 %137 to i32
  %139 = icmp eq i32 %138, 83
  br i1 %139, label %140, label %207

140:                                              ; preds = %135
  %141 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 0
  %142 = load i8, i8* %141, align 16
  %143 = sext i8 %142 to i32
  %144 = icmp eq i32 %143, 66
  br i1 %144, label %145, label %207

145:                                              ; preds = %140
  %146 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 22
  %147 = load i8, i8* %146, align 2
  %148 = sext i8 %147 to i32
  %149 = icmp eq i32 %148, 52
  br i1 %149, label %150, label %207

150:                                              ; preds = %145
  %151 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 32
  %152 = load i8, i8* %151, align 16
  %153 = sext i8 %152 to i32
  %154 = icmp eq i32 %153, 95
  br i1 %154, label %155, label %207

155:                                              ; preds = %150
  %156 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 16
  %157 = load i8, i8* %156, align 16
  %158 = sext i8 %157 to i32
  %159 = icmp eq i32 %158, 49
  br i1 %159, label %160, label %207

160:                                              ; preds = %155
  %161 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 12
  %162 = load i8, i8* %161, align 4
  %163 = sext i8 %162 to i32
  %164 = icmp eq i32 %163, 109
  br i1 %164, label %165, label %207

165:                                              ; preds = %160
  %166 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 38
  %167 = load i8, i8* %166, align 2
  %168 = sext i8 %167 to i32
  %169 = icmp eq i32 %168, 125
  br i1 %169, label %170, label %207

170:                                              ; preds = %165
  %171 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 35
  %172 = load i8, i8* %171, align 1
  %173 = sext i8 %172 to i32
  %174 = icmp eq i32 %173, 117
  br i1 %174, label %175, label %207

175:                                              ; preds = %170
  %176 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 6
  %177 = load i8, i8* %176, align 2
  %178 = sext i8 %177 to i32
  %179 = icmp eq i32 %178, 102
  br i1 %179, label %180, label %207

180:                                              ; preds = %175
  %181 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 9
  %182 = load i8, i8* %181, align 1
  %183 = sext i8 %182 to i32
  %184 = icmp eq i32 %183, 110
  br i1 %184, label %185, label %207

185:                                              ; preds = %180
  %186 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 14
  %187 = load i8, i8* %186, align 2
  %188 = sext i8 %187 to i32
  %189 = icmp eq i32 %188, 53
  br i1 %189, label %190, label %207

190:                                              ; preds = %185
  %191 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 4
  %192 = load i8, i8* %191, align 4
  %193 = sext i8 %192 to i32
  %194 = icmp eq i32 %193, 49
  br i1 %194, label %195, label %207

195:                                              ; preds = %190
  %196 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 5
  %197 = load i8, i8* %196, align 1
  %198 = sext i8 %197 to i32
  %199 = icmp eq i32 %198, 95
  br i1 %199, label %200, label %207

200:                                              ; preds = %195
  %201 = getelementptr inbounds [100 x i8], [100 x i8]* %2, i64 0, i64 20
  %202 = load i8, i8* %201, align 4
  %203 = sext i8 %202 to i32
  %204 = icmp eq i32 %203, 110
  br i1 %204, label %205, label %207

205:                                              ; preds = %200
  %206 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([22 x i8], [22 x i8]* @.str.2, i64 0, i64 0))
  br label %209

207:                                              ; preds = %200, %195, %190, %185, %180, %175, %170, %165, %160, %155, %150, %145, %140, %135, %130, %125, %120, %115, %110, %105, %100, %95, %90, %85, %80, %75, %70, %65, %60, %55, %50, %45, %40, %35, %30, %25, %20, %15, %10
  %208 = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([24 x i8], [24 x i8]* @.str.3, i64 0, i64 0))
  br label %209

209:                                              ; preds = %207, %205
  ret i32 0
}

declare i32 @printf(i8* noundef, ...) #1

declare i32 @scanf(i8* noundef, ...) #1

declare i64 @strlen(i8* noundef) #1

; Function Attrs: noreturn
declare void @exit(i32 noundef) #2

attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { noreturn "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { noreturn }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 1}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 14.0.0-1ubuntu1"}
