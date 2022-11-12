<script setup lang="ts">
const t1 = new URL("/images/HuTao.png", import.meta.url);
const t2 = new URL("/images/Xiao.png", import.meta.url);
const t3 = new URL("/images/Candace.png", import.meta.url);
</script>

<template>
	<section class="container py-5">
		<div class="row text-center pt-3">
			<div class="col-lg-6 m-auto">
				<h1 class="h1">Top characters</h1>
			</div>
		</div>
		<div class="row">
			<div class="col-12 col-md-4 p-5 mt-3">
				<a href="#"><img :src="t1.href" class="rounded-circle img-fluid border"></a>
				<h5 class="text-center mt-3 mb-3">Hu tao</h5>
				<p class="text-center"><a class="btn btn-success">View all</a></p>
			</div>
			<div class="col-12 col-md-4 p-5 mt-3">
				<a href="#"><img :src="t2.href" class="rounded-circle img-fluid border"></a>
				<h2 class="h5 text-center mt-3 mb-3">Xiao</h2>
				<p class="text-center"><a class="btn btn-success">View all</a></p>
			</div>
			<div class="col-12 col-md-4 p-5 mt-3">
				<a href="#"><img :src="t3.href" class="rounded-circle img-fluid border"></a>
				<h2 class="h5 text-center mt-3 mb-3">Candace</h2>
				<p class="text-center"><a class="btn btn-success">View all</a></p>
			</div>
		</div>
	</section>
</template>