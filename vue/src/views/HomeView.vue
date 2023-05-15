<template>
  <div class="home">
    <HelloWorld v-if="!$store.state.logged_in" msg="Welcome to Your Vue.js App" />
    <PostList v-else :post_ids="$store.state.feed"></PostList>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import PostList from "@/components/PostList.vue";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
    PostList
  },
};
</script>
