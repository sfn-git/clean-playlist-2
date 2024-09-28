<template>
    <div class="navbar bg-base-100 bg-neutral">
        <div class="navbar-start">
            <a class="btn btn-ghost text-xl">Clean Playlist 2.0</a>
        </div>
        <div class="navbar-end">
            <a v-if="isAuthenticated" class="btn btn-success" :href="login_url">Login to Spotify</a>
            <a v-else class="btn" :href="logout_url">Logout of Spotify</a>
        </div>
    </div>
</template>

<script setup>
import {ref} from 'vue';

const login_url = ref(`${import.meta.env.VITE_API_URL}/spotify/auth`);
const logout_url = ref(`${import.meta.env.VITE_API_URL}/spotify/auth/logout`);
</script>