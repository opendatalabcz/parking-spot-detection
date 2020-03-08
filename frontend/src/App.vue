<template>
  <v-app>

    <nav-bar></nav-bar>
    <v-content class="ma-4">
      <router-view>

      </router-view>
    </v-content>
  </v-app>
</template>

<script>
  import NavBar from "@/components/NavBar";

export default {
  name: 'App',

  components: {
    NavBar
  },

  data: () => ({
    //
  }),
};
</script>
