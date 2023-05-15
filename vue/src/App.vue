<template>
  <div id="app" class="app-container">
    <CSSNavBar />
    <router-view />
  </div>
</template>

<script>
import router from './router';

import CSSNavBar from "@/components/navbar.vue";
import Vue from 'vue';
import Vue2TouchEvents from 'vue2-touch-events'

Vue.use(Vue2TouchEvents)

export default {
    data() {
        return {};
    },
    components: { router, CSSNavBar }
}

</script>


