import { createApp } from "vue";
import { createPinia } from "pinia";
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCartArrowDown, faChevronLeft, faChevronRight, faUser } from "@fortawesome/free-solid-svg-icons";
import { faFacebookF, faInstagram, faLinkedin, faTwitter } from "@fortawesome/free-brands-svg-icons";
import { faStar } from "@fortawesome/free-regular-svg-icons";

import App from "./App.vue";
import router from "./router";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
// import "./assets/main.css";
import "./assets/app.css";



library.add(faFacebookF, faInstagram, faTwitter, faLinkedin, faUser, faCartArrowDown, faChevronLeft, faChevronRight, faStar);

const app = createApp(App);

app.component('font-awesome-icon', FontAwesomeIcon);

app.use(createPinia());
app.use(router);

app.mount("#app");
