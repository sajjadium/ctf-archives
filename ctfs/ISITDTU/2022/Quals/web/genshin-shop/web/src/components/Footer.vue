<script setup lang="ts">
import { ref } from 'vue';
import * as linkify from 'linkifyjs';

const feedback = ref<HTMLInputElement>();
const onSendFeedback = async () => {
    let url = new URL("/api/v0/feedback", import.meta.url);
    let input = feedback.value;

    let feedbackUrl = linkify.find(input.value)
        .filter(x => x.type === 'url')
        .map(x => x.href).pop();

    return await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: input.value,
            url: feedbackUrl ? feedbackUrl : ''
        })
    }).then(x => x.json());
}
</script>

<style>
.feedback-btn:hover {
    cursor: pointer;
}
</style>

<template>
    <footer class="bg-dark" id="shop_footer">
        <div class="container">
            <div class="row">
                <div class="col-md-4 pt-5">
                    <h2 class="h2 text-success border-bottom pb-3 border-light logo">Genshin Shop</h2>
                    <ul class="list-unstyled text-light footer-link-list">
                        <li>
                            <i class="fas fa-map-marker-alt fa-fw"></i>
                            VN
                        </li>
                        <li>
                            <i class="fa fa-phone fa-fw"></i>
                            <a class="text-decoration-none" href="tel:0999999999">099-999-9999</a>
                        </li>
                        <li>
                            <i class="fa fa-envelope fa-fw"></i>
                            <a class="text-decoration-none"
                                href="mailto:shop@genshin-shop.net">shop@genshin-shop.net</a>
                        </li>
                    </ul>
                </div>

                <div class="col-md-4 pt-5">
                    <h2 class="h2 text-light border-bottom pb-3 border-light">Further Info</h2>
                    <ul class="list-unstyled text-light footer-link-list">
                        <li><a class="text-decoration-none" href="#">Home</a></li>
                        <li><a class="text-decoration-none" href="#">About Us</a></li>
                        <li><a class="text-decoration-none" href="#">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="row text-light mb-4">
                <div class="col-12 mb-3">
                    <div class="w-100 my-3 border-top border-light"></div>
                </div>
                <div class="col-auto me-auto">
                    <ul class="list-inline text-left footer-icons">
                        <li class="list-inline-item border border-light rounded-circle text-center">
                            <a class="text-light text-decoration-none" target="_blank" href="https://www.facebook.com/">
                                <font-awesome-icon icon="fa-brands fa-facebook-f" class="fa-lg fa-fw">
                                </font-awesome-icon>
                            </a>
                        </li>
                        <li class="list-inline-item border border-light rounded-circle text-center">
                            <a class="text-light text-decoration-none" target="_blank"
                                href="https://www.instagram.com/">
                                <font-awesome-icon icon="fa-brands fa-instagram" class="fa-lg fa-fw">
                                </font-awesome-icon>
                            </a>
                        </li>
                        <li class="list-inline-item border border-light rounded-circle text-center">
                            <a class="text-light text-decoration-none" target="_blank" href="https://twitter.com/">
                                <font-awesome-icon icon=" fa-brands fa-twitter" class="fa-lg fa-fw">
                                </font-awesome-icon>
                            </a>
                        </li>
                        <li class="list-inline-item border border-light rounded-circle text-center">
                            <a class="text-light text-decoration-none" target="_blank" href="https://www.linkedin.com/">
                                <font-awesome-icon icon="fa-brands fa-linkedin" class="fa-lg fa-fw"></font-awesome-icon>
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="col-auto">
                    <label class="sr-only" for="feedbackMessage">Feedback</label>
                    <div class="input-group mb-2">
                        <input ref="feedback" type="text"
                            class="form-control shadow-none bg-dark border-light text-light" id="feedbackMessage"
                            placeholder="Feedback" />
                        <div @click="onSendFeedback()" class="input-group-text btn-success text-ligh feedback-btn">Send
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="w-100 bg-black py-3">
            <div class="container">
                <div class="row pt-2">
                    <div class="col-12">
                        <p class="text-left text-light">
                            Copyright &copy; 2022 Genshin Shop dot Net
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>