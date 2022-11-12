<script setup lang="ts">
import { onMounted, ref } from 'vue';

interface IProduct {
    title: string;
    description: string;
    banner: string;
    price: number;
    sold: boolean;
}

const products = ref<IProduct[]>([]);
const symbol = new URL("/images/symbol.png", import.meta.url);

const getProductDetail = async (id: number) => {
    let url = new URL("/api/v0/product", import.meta.url);
    let params = url.searchParams;

    params.append('id', id.toString());

    return await fetch(url, {
        method: 'GET'
    }).then(x => x.json());
}

onMounted(async () => {
    await fetch(new URL("/api/v0/products", import.meta.url), {
        method: 'GET'
    })
        .then(x => x.json())
        .then((x: number[]) => x.forEach(async y => products.value.push(await getProductDetail(y))));
});
</script>

<style>
.symbol {
    width: 12vh;
}
</style>

<template>
    <section class="bg-light" id="shop_product">
        <div class="container py-5">
            <div class="row text-center py-3">
                <div class="col-lg-6 m-auto">
                    <h1 class="h1">Genshin Impact</h1>
                    <img :src="symbol.href" class="symbol">
                </div>
            </div>
            <div class="row">
                <div v-for="p in products" class="col-12 col-md-3 col-sm-4 col-xs-6 mb-4">
                    <div class="card h-100">
                        <a href="#">
                            <img :src="p.banner" class="card-img-top" alt="...">
                        </a>
                        <div class="card-body">
                            <ul class="list-unstyled d-flex justify-content-between">
                                <li>
                                    <font-awesome-icon icon="fa-regular fa-star" class="text-warning">
                                    </font-awesome-icon>
                                    <font-awesome-icon icon="fa-regular fa-star" class="text-warning">
                                    </font-awesome-icon>
                                    <font-awesome-icon icon="fa-regular fa-star" class="text-warning">
                                    </font-awesome-icon>
                                    <font-awesome-icon icon="fa-regular fa-star" class="text-muted"></font-awesome-icon>
                                    <font-awesome-icon icon="fa-regular fa-star" class="text-muted"></font-awesome-icon>
                                </li>
                                <li class="text-muted text-right">{{ p.price }} VND</li>
                            </ul>
                            <a href="#" class="h3 text-decoration-none text-dark">{{ p.title }}</a>
                            <p class="card-text">{{ p.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>