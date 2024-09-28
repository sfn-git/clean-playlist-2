<template>
    <div class="hero bg-base-200 min-h-screen">
        <div class="hero-content text-center">
            <div class="max-w-md">
            <h1 class="text-5xl font-bold">Clean Playlist 2.0</h1>
            <p class="py-6">
                A tool to help you remove explicit songs from your playlists. Login to your Spotify to view your playlists.
            </p>
            <a class="btn btn-success my-3 mx-auto" :href="auth_url">Login to Spotify</a>
            </div>
        </div>
    </div>    
</template>

<script setup>
import {ref} from 'vue';
const auth_url = ref(`${import.meta.env.VITE_API_URL}/spotify/auth`);
</script>