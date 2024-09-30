<template>
    <div class="w-screen" v-if="isAuthenticated">
      <Nav :isAuthenticated="isAuthenticated"></Nav>
      <div class="container mx-auto">
        <Playlists @updateLoading="updateLoading"></Playlists>
      </div>
    </div>
    <div v-else class="mt-3 w-screen"> 
      <Index></Index>
    </div>
</template>

<script setup>
import axios from 'axios'
import Cookies from 'js-cookie'
import Playlists from './components/Playlists.vue'
import Nav from './components/Nav.vue';
import Index from './components/Index.vue';
import { onBeforeMount, ref } from 'vue';
 
const isAuthenticated = ref(false);
let checkAuth = async () =>{
  let url = `${import.meta.env.VITE_API_URL}/spotify/authenticated`
  console.log(url)
  axios.get(url, {
    headers: {
      Authorization: 'Bearer ' + Cookies.get('jwt')
    }
  }).then(response => {
    isAuthenticated.value = true;
  }).catch(error =>{
    console.log(error);
    isAuthenticated.value = false;
  })
}



onBeforeMount(()=>checkAuth())

// return {updateLoading};

</script>