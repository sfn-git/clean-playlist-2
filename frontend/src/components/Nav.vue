<template>
    <div class="navbar bg-base-100 bg-neutral">
        <div class="navbar-start">
            <a class="btn btn-ghost text-xl">Clean Playlist 2.0</a>
        </div>
        <div class="navbar-end">
            <a v-if="!$root.isAuthenticated.valueOf()" class="btn btn-success" href="http://localhost:8080/spotify/auth">Login to Spotify</a>
            <a v-else class="btn" href="http://localhost:8080/spotify/auth/logout">Logout of Spotify</a>
        </div>
    </div>
</template>