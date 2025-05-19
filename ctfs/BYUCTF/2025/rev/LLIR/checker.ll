; ModuleID = 'source.c'
source_filename = "source.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-redhat-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"byuctf\00", align 1
@.str.1 = private unnamed_addr constant [46 x i8] c"Welcome to this totally normal flag checkern\0A\00", align 1
@.str.2 = private unnamed_addr constant [61 x i8] c"We're going to use a little bit of a different compiler tho\0A\00", align 1
@.str.3 = private unnamed_addr constant [56 x i8] c"Ever heard of clang? What makes it different than gcc?\0A\00", align 1
@stdin = external dso_local global ptr, align 8
@.str.4 = private unnamed_addr constant [11 x i8] c"You win!!\0A\00", align 1
@.str.5 = private unnamed_addr constant [11 x i8] c"Womp womp\0A\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @checker_i_hardly_know_her(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = load ptr, ptr %2, align 8
  %4 = getelementptr inbounds i8, ptr %3, i64 4
  %5 = load i8, ptr %4, align 1
  %6 = sext i8 %5 to i32
  %7 = load ptr, ptr %2, align 8
  %8 = getelementptr inbounds i8, ptr %7, i64 14
  %9 = load i8, ptr %8, align 1
  %10 = sext i8 %9 to i32
  %11 = icmp eq i32 %6, %10
  br i1 %11, label %12, label %340

12:                                               ; preds = %1
  %13 = load ptr, ptr %2, align 8
  %14 = getelementptr inbounds i8, ptr %13, i64 14
  %15 = load i8, ptr %14, align 1
  %16 = sext i8 %15 to i32
  %17 = load ptr, ptr %2, align 8
  %18 = getelementptr inbounds i8, ptr %17, i64 17
  %19 = load i8, ptr %18, align 1
  %20 = sext i8 %19 to i32
  %21 = icmp eq i32 %16, %20
  br i1 %21, label %22, label %340

22:                                               ; preds = %12
  %23 = load ptr, ptr %2, align 8
  %24 = getelementptr inbounds i8, ptr %23, i64 17
  %25 = load i8, ptr %24, align 1
  %26 = sext i8 %25 to i32
  %27 = load ptr, ptr %2, align 8
  %28 = getelementptr inbounds i8, ptr %27, i64 23
  %29 = load i8, ptr %28, align 1
  %30 = sext i8 %29 to i32
  %31 = icmp eq i32 %26, %30
  br i1 %31, label %32, label %340

32:                                               ; preds = %22
  %33 = load ptr, ptr %2, align 8
  %34 = getelementptr inbounds i8, ptr %33, i64 23
  %35 = load i8, ptr %34, align 1
  %36 = sext i8 %35 to i32
  %37 = load ptr, ptr %2, align 8
  %38 = getelementptr inbounds i8, ptr %37, i64 25
  %39 = load i8, ptr %38, align 1
  %40 = sext i8 %39 to i32
  %41 = icmp eq i32 %36, %40
  br i1 %41, label %42, label %340

42:                                               ; preds = %32
  %43 = load ptr, ptr %2, align 8
  %44 = getelementptr inbounds i8, ptr %43, i64 9
  %45 = load i8, ptr %44, align 1
  %46 = sext i8 %45 to i32
  %47 = load ptr, ptr %2, align 8
  %48 = getelementptr inbounds i8, ptr %47, i64 20
  %49 = load i8, ptr %48, align 1
  %50 = sext i8 %49 to i32
  %51 = icmp eq i32 %46, %50
  br i1 %51, label %52, label %340

52:                                               ; preds = %42
  %53 = load ptr, ptr %2, align 8
  %54 = getelementptr inbounds i8, ptr %53, i64 10
  %55 = load i8, ptr %54, align 1
  %56 = sext i8 %55 to i32
  %57 = load ptr, ptr %2, align 8
  %58 = getelementptr inbounds i8, ptr %57, i64 18
  %59 = load i8, ptr %58, align 1
  %60 = sext i8 %59 to i32
  %61 = icmp eq i32 %56, %60
  br i1 %61, label %62, label %340

62:                                               ; preds = %52
  %63 = load ptr, ptr %2, align 8
  %64 = getelementptr inbounds i8, ptr %63, i64 11
  %65 = load i8, ptr %64, align 1
  %66 = sext i8 %65 to i32
  %67 = load ptr, ptr %2, align 8
  %68 = getelementptr inbounds i8, ptr %67, i64 15
  %69 = load i8, ptr %68, align 1
  %70 = sext i8 %69 to i32
  %71 = icmp eq i32 %66, %70
  br i1 %71, label %72, label %340

72:                                               ; preds = %62
  %73 = load ptr, ptr %2, align 8
  %74 = getelementptr inbounds i8, ptr %73, i64 15
  %75 = load i8, ptr %74, align 1
  %76 = sext i8 %75 to i32
  %77 = load ptr, ptr %2, align 8
  %78 = getelementptr inbounds i8, ptr %77, i64 24
  %79 = load i8, ptr %78, align 1
  %80 = sext i8 %79 to i32
  %81 = icmp eq i32 %76, %80
  br i1 %81, label %82, label %340

82:                                               ; preds = %72
  %83 = load ptr, ptr %2, align 8
  %84 = getelementptr inbounds i8, ptr %83, i64 24
  %85 = load i8, ptr %84, align 1
  %86 = sext i8 %85 to i32
  %87 = load ptr, ptr %2, align 8
  %88 = getelementptr inbounds i8, ptr %87, i64 31
  %89 = load i8, ptr %88, align 1
  %90 = sext i8 %89 to i32
  %91 = icmp eq i32 %86, %90
  br i1 %91, label %92, label %340

92:                                               ; preds = %82
  %93 = load ptr, ptr %2, align 8
  %94 = getelementptr inbounds i8, ptr %93, i64 31
  %95 = load i8, ptr %94, align 1
  %96 = sext i8 %95 to i32
  %97 = load ptr, ptr %2, align 8
  %98 = getelementptr inbounds i8, ptr %97, i64 27
  %99 = load i8, ptr %98, align 1
  %100 = sext i8 %99 to i32
  %101 = icmp eq i32 %96, %100
  br i1 %101, label %102, label %340

102:                                              ; preds = %92
  %103 = load ptr, ptr %2, align 8
  %104 = getelementptr inbounds i8, ptr %103, i64 13
  %105 = load i8, ptr %104, align 1
  %106 = sext i8 %105 to i32
  %107 = load ptr, ptr %2, align 8
  %108 = getelementptr inbounds i8, ptr %107, i64 26
  %109 = load i8, ptr %108, align 1
  %110 = sext i8 %109 to i32
  %111 = icmp eq i32 %106, %110
  br i1 %111, label %112, label %340

112:                                              ; preds = %102
  %113 = load ptr, ptr %2, align 8
  %114 = getelementptr inbounds i8, ptr %113, i64 16
  %115 = load i8, ptr %114, align 1
  %116 = sext i8 %115 to i32
  %117 = load ptr, ptr %2, align 8
  %118 = getelementptr inbounds i8, ptr %117, i64 29
  %119 = load i8, ptr %118, align 1
  %120 = sext i8 %119 to i32
  %121 = icmp eq i32 %116, %120
  br i1 %121, label %122, label %340

122:                                              ; preds = %112
  %123 = load ptr, ptr %2, align 8
  %124 = getelementptr inbounds i8, ptr %123, i64 19
  %125 = load i8, ptr %124, align 1
  %126 = sext i8 %125 to i32
  %127 = load ptr, ptr %2, align 8
  %128 = getelementptr inbounds i8, ptr %127, i64 28
  %129 = load i8, ptr %128, align 1
  %130 = sext i8 %129 to i32
  %131 = icmp eq i32 %126, %130
  br i1 %131, label %132, label %340

132:                                              ; preds = %122
  %133 = load ptr, ptr %2, align 8
  %134 = getelementptr inbounds i8, ptr %133, i64 28
  %135 = load i8, ptr %134, align 1
  %136 = sext i8 %135 to i32
  %137 = load ptr, ptr %2, align 8
  %138 = getelementptr inbounds i8, ptr %137, i64 32
  %139 = load i8, ptr %138, align 1
  %140 = sext i8 %139 to i32
  %141 = icmp eq i32 %136, %140
  br i1 %141, label %142, label %340

142:                                              ; preds = %132
  %143 = load ptr, ptr %2, align 8
  %144 = getelementptr inbounds i8, ptr %143, i64 36
  %145 = load i8, ptr %144, align 1
  %146 = sext i8 %145 to i32
  %147 = icmp eq i32 %146, 125
  br i1 %147, label %148, label %340

148:                                              ; preds = %142
  %149 = load ptr, ptr %2, align 8
  %150 = getelementptr inbounds i8, ptr %149, i64 6
  %151 = load i8, ptr %150, align 1
  %152 = sext i8 %151 to i32
  %153 = icmp eq i32 %152, 123
  br i1 %153, label %154, label %340

154:                                              ; preds = %148
  %155 = load ptr, ptr %2, align 8
  %156 = getelementptr inbounds i8, ptr %155, i64 8
  %157 = load i8, ptr %156, align 1
  %158 = sext i8 %157 to i32
  %159 = load ptr, ptr %2, align 8
  %160 = getelementptr inbounds i8, ptr %159, i64 7
  %161 = load i8, ptr %160, align 1
  %162 = sext i8 %161 to i32
  %163 = sub nsw i32 %162, 32
  %164 = icmp eq i32 %158, %163
  br i1 %164, label %165, label %340

165:                                              ; preds = %154
  %166 = load ptr, ptr %2, align 8
  %167 = call i32 @strncmp(ptr noundef %166, ptr noundef @.str, i64 noundef 6) #3
  %168 = icmp eq i32 %167, 0
  br i1 %168, label %169, label %340

169:                                              ; preds = %165
  %170 = load ptr, ptr %2, align 8
  %171 = getelementptr inbounds i8, ptr %170, i64 9
  %172 = load i8, ptr %171, align 1
  %173 = sext i8 %172 to i32
  %174 = load ptr, ptr %2, align 8
  %175 = getelementptr inbounds i8, ptr %174, i64 20
  %176 = load i8, ptr %175, align 1
  %177 = sext i8 %176 to i32
  %178 = add nsw i32 %173, %177
  %179 = load ptr, ptr %2, align 8
  %180 = getelementptr inbounds i8, ptr %179, i64 31
  %181 = load i8, ptr %180, align 1
  %182 = sext i8 %181 to i32
  %183 = add nsw i32 %182, 3
  %184 = icmp eq i32 %178, %183
  br i1 %184, label %185, label %340

185:                                              ; preds = %169
  %186 = load ptr, ptr %2, align 8
  %187 = getelementptr inbounds i8, ptr %186, i64 31
  %188 = load i8, ptr %187, align 1
  %189 = sext i8 %188 to i32
  %190 = add nsw i32 %189, 3
  %191 = load ptr, ptr %2, align 8
  %192 = getelementptr inbounds i8, ptr %191, i64 0
  %193 = load i8, ptr %192, align 1
  %194 = sext i8 %193 to i32
  %195 = icmp eq i32 %190, %194
  br i1 %195, label %196, label %340

196:                                              ; preds = %185
  %197 = load ptr, ptr %2, align 8
  %198 = getelementptr inbounds i8, ptr %197, i64 10
  %199 = load i8, ptr %198, align 1
  %200 = sext i8 %199 to i32
  %201 = load ptr, ptr %2, align 8
  %202 = getelementptr inbounds i8, ptr %201, i64 7
  %203 = load i8, ptr %202, align 1
  %204 = sext i8 %203 to i32
  %205 = add nsw i32 %204, 6
  %206 = icmp eq i32 %200, %205
  br i1 %206, label %207, label %340

207:                                              ; preds = %196
  %208 = load ptr, ptr %2, align 8
  %209 = getelementptr inbounds i8, ptr %208, i64 8
  %210 = load i8, ptr %209, align 1
  %211 = sext i8 %210 to i32
  %212 = load ptr, ptr %2, align 8
  %213 = getelementptr inbounds i8, ptr %212, i64 9
  %214 = load i8, ptr %213, align 1
  %215 = sext i8 %214 to i32
  %216 = add nsw i32 %215, 27
  %217 = icmp eq i32 %211, %216
  br i1 %217, label %218, label %340

218:                                              ; preds = %207
  %219 = load ptr, ptr %2, align 8
  %220 = getelementptr inbounds i8, ptr %219, i64 12
  %221 = load i8, ptr %220, align 1
  %222 = sext i8 %221 to i32
  %223 = load ptr, ptr %2, align 8
  %224 = getelementptr inbounds i8, ptr %223, i64 13
  %225 = load i8, ptr %224, align 1
  %226 = sext i8 %225 to i32
  %227 = sub nsw i32 %226, 1
  %228 = icmp eq i32 %222, %227
  br i1 %228, label %229, label %340

229:                                              ; preds = %218
  %230 = load ptr, ptr %2, align 8
  %231 = getelementptr inbounds i8, ptr %230, i64 13
  %232 = load i8, ptr %231, align 1
  %233 = sext i8 %232 to i32
  %234 = load ptr, ptr %2, align 8
  %235 = getelementptr inbounds i8, ptr %234, i64 10
  %236 = load i8, ptr %235, align 1
  %237 = sext i8 %236 to i32
  %238 = sub nsw i32 %237, 3
  %239 = icmp eq i32 %233, %238
  br i1 %239, label %240, label %340

240:                                              ; preds = %229
  %241 = load ptr, ptr %2, align 8
  %242 = getelementptr inbounds i8, ptr %241, i64 10
  %243 = load i8, ptr %242, align 1
  %244 = sext i8 %243 to i32
  %245 = load ptr, ptr %2, align 8
  %246 = getelementptr inbounds i8, ptr %245, i64 16
  %247 = load i8, ptr %246, align 1
  %248 = sext i8 %247 to i32
  %249 = sub nsw i32 %248, 1
  %250 = icmp eq i32 %244, %249
  br i1 %250, label %251, label %340

251:                                              ; preds = %240
  %252 = load ptr, ptr %2, align 8
  %253 = getelementptr inbounds i8, ptr %252, i64 16
  %254 = load i8, ptr %253, align 1
  %255 = sext i8 %254 to i32
  %256 = load ptr, ptr %2, align 8
  %257 = getelementptr inbounds i8, ptr %256, i64 14
  %258 = load i8, ptr %257, align 1
  %259 = sext i8 %258 to i32
  %260 = sub nsw i32 %259, 1
  %261 = icmp eq i32 %255, %260
  br i1 %261, label %262, label %340

262:                                              ; preds = %251
  %263 = load ptr, ptr %2, align 8
  %264 = getelementptr inbounds i8, ptr %263, i64 35
  %265 = load i8, ptr %264, align 1
  %266 = sext i8 %265 to i32
  %267 = load ptr, ptr %2, align 8
  %268 = getelementptr inbounds i8, ptr %267, i64 5
  %269 = load i8, ptr %268, align 1
  %270 = sext i8 %269 to i32
  %271 = sub nsw i32 %270, 2
  %272 = icmp eq i32 %266, %271
  br i1 %272, label %273, label %340

273:                                              ; preds = %262
  %274 = load ptr, ptr %2, align 8
  %275 = getelementptr inbounds i8, ptr %274, i64 5
  %276 = load i8, ptr %275, align 1
  %277 = sext i8 %276 to i32
  %278 = load ptr, ptr %2, align 8
  %279 = getelementptr inbounds i8, ptr %278, i64 21
  %280 = load i8, ptr %279, align 1
  %281 = sext i8 %280 to i32
  %282 = sub nsw i32 %281, 1
  %283 = icmp eq i32 %277, %282
  br i1 %283, label %284, label %340

284:                                              ; preds = %273
  %285 = load ptr, ptr %2, align 8
  %286 = getelementptr inbounds i8, ptr %285, i64 21
  %287 = load i8, ptr %286, align 1
  %288 = sext i8 %287 to i32
  %289 = load ptr, ptr %2, align 8
  %290 = getelementptr inbounds i8, ptr %289, i64 22
  %291 = load i8, ptr %290, align 1
  %292 = sext i8 %291 to i32
  %293 = sub nsw i32 %292, 1
  %294 = icmp eq i32 %288, %293
  br i1 %294, label %295, label %340

295:                                              ; preds = %284
  %296 = load ptr, ptr %2, align 8
  %297 = getelementptr inbounds i8, ptr %296, i64 22
  %298 = load i8, ptr %297, align 1
  %299 = sext i8 %298 to i32
  %300 = load ptr, ptr %2, align 8
  %301 = getelementptr inbounds i8, ptr %300, i64 28
  %302 = load i8, ptr %301, align 1
  %303 = sext i8 %302 to i32
  %304 = mul nsw i32 %303, 2
  %305 = icmp eq i32 %299, %304
  br i1 %305, label %306, label %340

306:                                              ; preds = %295
  %307 = load ptr, ptr %2, align 8
  %308 = getelementptr inbounds i8, ptr %307, i64 33
  %309 = load i8, ptr %308, align 1
  %310 = sext i8 %309 to i32
  %311 = load ptr, ptr %2, align 8
  %312 = getelementptr inbounds i8, ptr %311, i64 32
  %313 = load i8, ptr %312, align 1
  %314 = sext i8 %313 to i32
  %315 = add nsw i32 %314, 1
  %316 = icmp eq i32 %310, %315
  br i1 %316, label %317, label %340

317:                                              ; preds = %306
  %318 = load ptr, ptr %2, align 8
  %319 = getelementptr inbounds i8, ptr %318, i64 32
  %320 = load i8, ptr %319, align 1
  %321 = sext i8 %320 to i32
  %322 = add nsw i32 %321, 1
  %323 = load ptr, ptr %2, align 8
  %324 = getelementptr inbounds i8, ptr %323, i64 34
  %325 = load i8, ptr %324, align 1
  %326 = sext i8 %325 to i32
  %327 = sub nsw i32 %326, 3
  %328 = icmp eq i32 %322, %327
  br i1 %328, label %329, label %340

329:                                              ; preds = %317
  %330 = load ptr, ptr %2, align 8
  %331 = getelementptr inbounds i8, ptr %330, i64 30
  %332 = load i8, ptr %331, align 1
  %333 = sext i8 %332 to i32
  %334 = load ptr, ptr %2, align 8
  %335 = getelementptr inbounds i8, ptr %334, i64 7
  %336 = load i8, ptr %335, align 1
  %337 = sext i8 %336 to i32
  %338 = add nsw i32 %337, 1
  %339 = icmp eq i32 %333, %338
  br label %340

340:                                              ; preds = %329, %317, %306, %295, %284, %273, %262, %251, %240, %229, %218, %207, %196, %185, %169, %165, %154, %148, %142, %132, %122, %112, %102, %92, %82, %72, %62, %52, %42, %32, %22, %12, %1
  %341 = phi i1 [ false, %317 ], [ false, %306 ], [ false, %295 ], [ false, %284 ], [ false, %273 ], [ false, %262 ], [ false, %251 ], [ false, %240 ], [ false, %229 ], [ false, %218 ], [ false, %207 ], [ false, %196 ], [ false, %185 ], [ false, %169 ], [ false, %165 ], [ false, %154 ], [ false, %148 ], [ false, %142 ], [ false, %132 ], [ false, %122 ], [ false, %112 ], [ false, %102 ], [ false, %92 ], [ false, %82 ], [ false, %72 ], [ false, %62 ], [ false, %52 ], [ false, %42 ], [ false, %32 ], [ false, %22 ], [ false, %12 ], [ false, %1 ], [ %339, %329 ]
  %342 = zext i1 %341 to i32
  ret i32 %342
}

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @strncmp(ptr noundef, ptr noundef, i64 noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [64 x i8], align 16
  store i32 0, ptr %1, align 4
  %3 = call i32 (ptr, ...) @printf(ptr noundef @.str.1)
  %4 = call i32 (ptr, ...) @printf(ptr noundef @.str.2)
  %5 = call i32 (ptr, ...) @printf(ptr noundef @.str.3)
  %6 = getelementptr inbounds [64 x i8], ptr %2, i64 0, i64 0
  %7 = load ptr, ptr @stdin, align 8
  %8 = call ptr @fgets(ptr noundef %6, i32 noundef 64, ptr noundef %7)
  %9 = getelementptr inbounds [64 x i8], ptr %2, i64 0, i64 0
  %10 = call i32 @checker_i_hardly_know_her(ptr noundef %9)
  %11 = icmp ne i32 %10, 0
  br i1 %11, label %12, label %14

12:                                               ; preds = %0
  %13 = call i32 (ptr, ...) @printf(ptr noundef @.str.4)
  store i32 0, ptr %1, align 4
  br label %16

14:                                               ; preds = %0
  %15 = call i32 (ptr, ...) @printf(ptr noundef @.str.5)
  store i32 1, ptr %1, align 4
  br label %16

16:                                               ; preds = %14, %12
  %17 = load i32, ptr %1, align 4
  ret i32 %17
}

declare dso_local i32 @printf(ptr noundef, ...) #2

declare dso_local ptr @fgets(ptr noundef, i32 noundef, ptr noundef) #2

attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nounwind willreturn memory(read) "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind willreturn memory(read) }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"uwtable", i32 2}
!2 = !{i32 7, !"frame-pointer", i32 2}
!3 = !{!"clang version 19.1.7 (Fedora 19.1.7-3.fc41)"}
