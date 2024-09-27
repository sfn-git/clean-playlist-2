<template>
    <div id="all_playlists_view mt-3" v-if="showAllPlaylist">
        <p class="text-4xl">Your Spotify Playlist</p>
        <!-- <p v-for="(item, index) in playlists.items" :key="index" v-show="playlists">{{ item.external_urls.spotify }}</p> -->
        <div class="join grid grid-cols-2 my-3">
            <button v-if="page == minPages" class="join-item btn btn-disabled">Previous page</button>
            <button v-else class="join-item btn btn-outline" @click="previousPage()">Previous page</button>
            <button v-if="page == maxPages" class="join-item btn btn-disabled">Next Page</button>
            <button v-else class="join-item btn btn-outline" @click="nextPage()">Next Page</button>
        </div>
        <p>Pages {{ page }}/{{ maxPages }} (Total of {{ playlists.total }} playlists)</p>
        <div class="my-3 bg-neutral" v-for="(item, index) in playlists.items" :key="index" v-show="playlists">
            <div class="card card-side card-compact" >
                <figure>
                    <img class="max-w-[250px] max-h-[250px]"
                    :src="getImgURL(item.images)"
                    alt="Album" />
                </figure>
                <div class="card-body">
                    <a class="card-title text-2xl" :href="item.external_urls.spotify" target="_blank">{{item.name}}</a>
                    <p class="text-lg" target="_blank">Created By: <a :href="item.owner.external_urls.spotify">{{ item.owner.display_name }}</a></p>
                    <p class="text-base">{{item.description}}</p>
                    <div class="card-actions">
                    <button class="btn btn-primary" @click="viewPlaylist(item.id)">View Playlist</button>
                </div>
            </div>
            </div>
        </div>
        <p>Pages {{ page }}/{{ maxPages }} (Total of {{ playlists.total }} playlists)</p>
        <div class="join grid grid-cols-2 my-3">
            <button v-if="page == minPages" class="join-item btn btn-disabled">Previous page</button>
            <button v-else class="join-item btn btn-outline" @click="previousPage()">Previous page</button>
            <button v-if="page == maxPages" class="join-item btn btn-disabled">Next Page</button>
            <button v-else class="join-item btn btn-outline" @click="nextPage()">Next Page</button>
        </div>
    </div>
    <div id="single_playlist_view " v-if="showSinglePlaylist">
        <button class="btn btn-outline mt-3" @click="getPlaylist()">Back to Playlists</button>
        <p class="text-4xl">{{singlePlaylistName}}</p>
        <p>There are {{ explicitSongs }} explicit songs in this playlist.</p>
        <div v-for="(jtems, jndex) in singlePlaylistExplicit">
            <div class="flex flex-row my-2 bg-green-900">
                <div>
                    <img :src="getImgURL(jtems.track.album.images)" width="100px" height="100px">
                </div>
                <p class="card-title ml-3">{{ jtems.track.name }} - {{ jtems.track.artists[0]['name'] }} <span v-if="jtems.track.explicit" class="badge badge-error">Explicit</span></p>
                
            </div>
        </div>
        <div v-for="(ktems, jndex) in singlePlaylistClean">
            <div class="flex flex-row my-2 bg-green-900">
                <div>
                    <img :src="getImgURL(ktems.track.album.images)" width="100px" height="100px">
                </div>
                <p class="card-title ml-3">{{ ktems.track.name }} - {{ ktems.track.artists[0]['name'] }} <span v-if="ktems.track.explicit" class="badge badge-error">Explicit</span></p>
                
            </div>
        </div>
        <!-- <p>{{singlePlaylist['tracks']}}</p> -->
    </div>
    
</template>

<script setup>
import axios from 'axios';
import Cookies from 'js-cookie';
import { ref, onMounted } from 'vue';

let showAllPlaylist = ref(true);
let showSinglePlaylist = ref(false);
let playlists = ref([]);
let page = ref(1);
let maxPages = ref(1);
let minPages = ref(1);
let singlePlaylistName = ref('')
let singlePlaylistExplicit = ref({});
let singlePlaylistClean = ref({});
let explicitSongs = ref(0);

async function getPlaylist(){
    try{
        const response = await axios.get(`http://localhost:8080/spotify/playlists?page=${page.value}`, {
            headers: {
            Authorization: 'Bearer ' + Cookies.get('jwt')
            }
        });
        playlists.value = response.data;
        maxPages.value = Math.ceil(playlists.value.total/10);
        showAllPlaylist.value = true;
        showSinglePlaylist.value = false;
    }catch(error){
        console.log(error);
    }
}

function nextPage(){
    page.value++;
    getPlaylist();
}

function previousPage(){
    page.value--;
    getPlaylist();
}

function getImgURL(img){
    if (img == null){
        return '/img/playlist_cover.png'
    }else{
        return img[0]['url']
    }
    
}

async function viewPlaylist(playlistID){
    try{
        let explicitTracks = [];
        let cleanTracks = [];
        let tracks = [];
        const response = await axios.get(`http://localhost:8080/spotify/playlists/${playlistID}/tracks`, {
            headers: {
            Authorization: 'Bearer ' + Cookies.get('jwt')
            }
        });
        console.log(response.data);
        showAllPlaylist.value = false;
        showSinglePlaylist.value = true;
        tracks = response.data.items;
        singlePlaylistName = response.data.playlist.name;
        explicitSongs.value = 0;
        for(var i in tracks){
            if(tracks[i]['track']['explicit']){
                explicitTracks.push(tracks[i])
                explicitSongs.value += 1;
            }else{
                cleanTracks.push(tracks[i])
            }
        }
        singlePlaylistExplicit.value = explicitTracks;
        singlePlaylistClean.value = cleanTracks;
        console.log(singlePlaylistExplicit.value)
        console.log(singlePlaylistClean.value)
    }catch(error){
        console.log(error);
    }
}

onMounted(async ()=>{
    getPlaylist();
})
</script>