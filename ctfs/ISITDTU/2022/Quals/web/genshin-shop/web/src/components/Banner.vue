<script setup lang="ts">
const createBanner = (ads: URL) => {
	let ret = new URL("/api/v0/advertise", import.meta.url);
	ret.searchParams.append("url", ads.href);
	return ret;
};
const b1 = createBanner(new URL("https://static.wikia.nocookie.net/gensin-impact/images/4/47/The_Moongrass%27_Enlightenment_2022-11-02.png"));
const b2 = createBanner(new URL("https://static.wikia.nocookie.net/gensin-impact/images/0/0a/Tapestry_of_Golden_Flames_2022-11-02.png"));
const b3 = createBanner(new URL("https://static.wikia.nocookie.net/gensin-impact/images/5/5c/Epitome_Invocation_2022-11-02.png"));
</script>

<template>
	<div id="template-mo-jassa-hero-carousel" class="carousel slide" data-bs-ride="carousel">
		<div class="carousel-inner">
			<div class="carousel-item active">
				<div class="container">
					<div class="row p-5">
						<div class="mx-auto col-md-8 col-lg-8 order-lg-last">
							<img class="img-fluid" :src="b1.href" alt="">
						</div>
						<div class="col-lg-4 mb-0 d-flex align-items-center">
							<div class="text-align-left align-self-center">
								<h1 class="h1">The Moongrass' Enlightenment</h1>
								<h3 class="h2">Character Event Wish</h3>
								<p>
									Event Wish "The Moongrass' Enlightenment" - Boosted Drop Rate for "Physic of Purity"
									Nahida (Dendro)!
									Travelers, stock up on weapons and characters in the event wish to make your party
									stronger in combat!
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="carousel-item">
				<div class="container">
					<div class="row p-5">
						<div class="mx-auto col-md-8 col-lg-8 order-lg-last">
							<img class="img-fluid" :src="b2.href" alt="">
						</div>
						<div class="col-lg-4 mb-0 d-flex align-items-center">
							<div class="text-align-left">
								<h1 class="h1">Tapestry of Golden Flames</h1>
								<h3 class="h2">Character Event Wish-2</h3>
								<p>
									Event Wish "Tapestry of Golden Flames" - Boosted Drop Rate for "Frolicking Flames"
									Yoimiya (Pyro)!
									Travelers, stock up on weapons and characters in the event wish to make your party
									stronger in combat!
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="carousel-item">
				<div class="container">
					<div class="row p-5">
						<div class="mx-auto col-md-8 col-lg-8 order-lg-last">
							<img class="img-fluid" :src="b3.href" alt="">
						</div>
						<div class="col-lg-4 mb-0 d-flex align-items-center">
							<div class="text-align-left">
								<h1 class="h1">Epitome Invocation</h1>
								<h3 class="h2">Weapon Event Wish</h3>
								<p>
									Event Wish "Epitome Invocation" - Boosted Drop Rate for A Thousand Floating Dreams
									(Catalyst) and Thundering Pulse (Bow)!
									Travelers, stock up on weapons and characters in ""Epitome Invocation"" to make your
									party stronger in combat!
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<a class="carousel-control-prev text-decoration-none w-auto ps-3" href="#template-mo-jassa-hero-carousel"
			role="button" data-bs-slide="prev">
			<font-awesome-icon icon="fa-solid fa-chevron-left" class="text-secondary"></font-awesome-icon>
		</a>
		<a class="carousel-control-next text-decoration-none w-auto pe-3" href="#template-mo-jassa-hero-carousel"
			role="button" data-bs-slide="next">
			<font-awesome-icon icon="fa-solid fa-chevron-right" class="text-secondary"></font-awesome-icon>
		</a>
	</div>
</template>