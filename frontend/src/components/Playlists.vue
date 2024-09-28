<template>
    <Loading v-if="showLoading" :message="loadingMessage"></Loading>
    <div id="all_playlists_view mt-3"  v-if="showAllPlaylist">
        <p class="text-4xl mt-3">Your Spotify Playlists</p>
        <!-- <p v-for="(item, index) in playlists.items" :key="index" v-show="playlists">{{ item.external_urls.spotify }}</p> -->
        <div class="join grid grid-cols-2 my-3">
            <button v-if="page == minPages" class="join-item btn btn-disabled">Previous page</button>
            <button v-else class="join-item btn btn-outline" @click="previousPage()">Previous page</button>
            <button v-if="page == maxPages" class="join-item btn btn-disabled">Next Page</button>
            <button v-else class="join-item btn btn-outline" @click="nextPage()">Next Page</button>
        </div>
        <p>Pages {{ page }}/{{ maxPages }} (Total of {{ playlists.total }} playlists)</p>
        <div class="my-3 bg-neutral" v-for="(item, index) in playlists.items" :key="index" v-show="playlists">
            <div class="flex flex-row" >
                <img
                :src="getImgURL(item.images)"
                alt="Album" height="200px" width="200px"/>
                <div class="flex flex-col justify-center ml-3">
                    <a class="card-title text-2xl" :href="item.external_urls.spotify" target="_blank">{{item.name}}</a>
                    <p class="text-lg" target="_blank">Created By: <a :href="item.owner.external_urls.spotify">{{ item.owner.display_name }}</a></p>
                    <p class="text-base my-2">{{item.description}}</p>
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
        
        <p class="text-4xl">{{singlePlaylistName}}</p>
        <p>There are {{ explicitSongs }} explicit songs out of {{totalSongs}} in this playlist.</p>
        <div class="flex mt-3">
            <button class="btn btn-outline mr-2" @click="getPlaylist()">Back to Playlists</button>
            <button class="btn btn-success" v-if="explicitSongs>0" @click="createNewPlaylist()">Create Playlist with Matched and Clean Tracks</button>
        </div>
        <div class="mt-3" v-for="(jtems, jndex) in singlePlaylistExplicit">
            <div class="flex flex-row my-2 bg-green-900">
                <div>
                    <img :src="getImgURL(jtems.track.track.album.images)" width="100px" height="100px">
                    <!-- {{ jtems.search_results.length }} -->
                </div>
                <div class="flex flex-row items-center ml-3">
                    <a :href="jtems.track.track.external_urls.spotify" target="_blank" class="card-title">{{ jtems.track.track.name }} - {{ jtems.track.track.artists[0]['name'] }} </a>
                    <span v-if="jtems.track.track.explicit" class="badge badge-error mx-2">Explicit</span>
                    <a v-if="jtems.exact_match" class="badge badge-secondary" :href="jtems.search_results.url" target="_blank">Exact Match Found</a>
                    <div v-else>
                        <a v-if="jtems.search_results.length === 0" class="badge badge-neutral">No Alternatives Found</a>
                        <div v-else>
                            <button v-if="!jtems.alternative_set" class="btn badge-success" @click="showAltModal(jtems.trackID)" >See Alternatives</button>
                            <button v-else class="badge badge-secondary">Alternative Set</button>
                            <dialog id="my_modal_1" class="modal" :class="{ 'modal-open': showModal }">
                                <div class="modal-box">
                                    <h3 class="font-bold text-lg">Alternatives to {{  }}</h3>
                                    <div class="flex flex-col" v-for="(ltems, jndex) in modalTracks">
                                        <div class="flex flex-row my-2 bg-green-900">
                                            <img :src="ltems.cover_url.url" width="100px" height="100px">
                                            <div class="flex flex-row items-center my-auto ml-2">
                                                <p><a :href="ltems.url" target="_blank">{{ltems.name}}</a></p>
                                                <!-- <p><a :href="ltems.url" target="_blank">{{ltems}}</a></p> -->
                                                <button class="btn btn-success ml-2" @click="setAlternativeTrack(currentModalID, `spotify:track:${ltems.id}`)">Set as Alternative</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="modal-action">
                                    <form method="dialog">
                                        <button class="btn" @click="closeAltModal">Close</button>
                                    </form>
                                    </div>
                                </div>
                            </dialog>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
        <div v-for="(ktems, jndex) in singlePlaylistClean">
            <div class="flex flex-row my-2 bg-green-900">
                <div>
                    <img :src="getImgURL(ktems.track.album.images)" width="100px" height="100px">
                </div>
                <div class="my-auto">
                    <a :href="ktems.track.external_urls.spotify" target="_blank" class="card-title ml-2">{{ ktems.track.name }} - {{ ktems.track.artists[0]['name'] }}</a>
                </div>
                
                
            </div>
        </div>
        <!-- <p>{{singlePlaylist['tracks']}}</p> -->
    </div>
</template>

<script setup>
import axios from 'axios';
import Cookies from 'js-cookie';
import { ref, onMounted } from 'vue';
import Loading from './Loading.vue';

const showLoading = ref(false);
let loadingMessage = ref({});
let showAllPlaylist = ref(true);
let showSinglePlaylist = ref(false);
let playlists = ref([]);
let page = ref(1);
let maxPages = ref(1);
let minPages = ref(1);
let singlePlaylistName = ref('');
let singlePlaylistExplicit = ref({});
let singlePlaylistClean = ref({});
let explicitSongs = ref(0);
let totalSongs = ref(0);
let newPlaylistSongs = ref([]);
let showModal = ref(false);
let modalTracks = ref([]);
let currentModalID = ref('')

async function getPlaylist(){
    showAllPlaylist.value = false;
    updateLoading(true, "Getting your playlists from Spotify.");
    try{
        const response = await axios.get(`${process.env.API_URL}/spotify/playlists?page=${page.value}`, {
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
    window.scrollTo(0,0);
    updateLoading();
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
    if (img == null || img.length == 0){
        return '/img/playlist_cover.png'
    }else{
        return img[0]['url']
    }
    
}

function resetSinglePlaylist(){

    singlePlaylistName = ref('');
    singlePlaylistExplicit = ref({});
    singlePlaylistClean = ref({});
    explicitSongs = ref(0);
    totalSongs = ref(0);
    newPlaylistSongs = ref([]);
    showModal = ref(false);
    modalTracks = ref([]);
    currentModalID = ref('')

}

async function viewPlaylist(playlistID){
    window.scrollTo(0,0);
    updateLoading(true, 'Please wait, getting playlist info.');
    resetSinglePlaylist();
    showAllPlaylist.value = false;
    try{
        let explicitTracks = [];
        let cleanTracks = [];
        let tracks = [];
        const response = await axios.get(`${process.env.API_URL}/spotify/playlists/${playlistID}/tracks`, {
            headers: {
            Authorization: 'Bearer ' + Cookies.get('jwt')
            }
        });
        tracks = response.data.items;
        singlePlaylistName = response.data.playlist.name;
        explicitSongs.value = 0;
        let counter = 0;
        totalSongs.value = response.data.playlist.tracks.total;
        for(var i in tracks){
            updateLoading(true, `Finding clean versions of songs in ${singlePlaylistName}. Checked ${counter} out of ${totalSongs.value} songs in playlist. Explicit Tracks found: ${explicitSongs.value}`);
            counter+=1;
            let trackID = tracks[i]['track']['uri'];
            if(tracks[i]['track']['explicit']){
                const response = await axios.get(`${process.env.API_URL}/spotify/tracks/${tracks[i]['track']['id']}/clean`, {
                    headers: {
                    Authorization: 'Bearer ' + Cookies.get('jwt')
                    }
                });
                let data = response.data;
                let explicit_obj = {
                    trackID,
                    track: tracks[i],
                    exact_match: data.exact_match,
                    alternative_set: false,
                    search_results: data.items
                }
                if(explicit_obj.exact_match){
                    newPlaylistSongs.value.push({
                        'oldID': trackID,
                        'newID': explicit_obj.search_results.uri
                    });
                }else{
                    newPlaylistSongs.value.push({
                        'oldID': trackID,
                        'newID': null
                    });
                }
                explicitTracks.push(explicit_obj);                
                explicitSongs.value += 1;
               
            }else{
                newPlaylistSongs.value.push({
                        'oldID': trackID,
                        'newID': trackID
                    });
                cleanTracks.push(tracks[i]);
            }
        }
        singlePlaylistExplicit.value = explicitTracks;
        singlePlaylistClean.value = cleanTracks;
    }catch(error){
        console.log(error);
    }
    updateLoading();
    showSinglePlaylist.value = true;
    console.log(newPlaylistSongs.value);
}

onMounted(async ()=>{
    getPlaylist();
})

function updateLoading(status=false, message){
  showLoading.value = status;
  loadingMessage = message;
}

function showAltModal(id){
    let track = singlePlaylistExplicit.value.find(es => es.trackID === id);
    modalTracks.value = track.search_results;
    showModal.value = !showModal.value;
    currentModalID.value = id;
}

function closeAltModal(){
    showModal.value = !showModal.value;
}

function setAlternativeTrack(id, newid){
    let newTrackIndex = newPlaylistSongs.value.findIndex(item => item.oldID === id);
    console.log(newPlaylistSongs.value[newTrackIndex]);
    newPlaylistSongs.value[newTrackIndex]['newID'] = newid;
    let explicitTrackIndex = singlePlaylistExplicit.value.findIndex(i => i.trackID === id);
    singlePlaylistExplicit.value[explicitTrackIndex].alternative_set = true;
    console.log(singlePlaylistExplicit.value[explicitTrackIndex]);
    closeAltModal();
}

async function createNewPlaylist(){
    if(window.confirm('Create playlist?')){
        updateLoading(true, ' Please wait, creating your playlist.');
        let sendID = [];
        for(var i in newPlaylistSongs.value){
            console.log(newPlaylistSongs.value[i]);
            if(newPlaylistSongs.value[i].newID != null){
                sendID.push(newPlaylistSongs.value[i].newID);
            }
        }
        console.log(sendID);
        let sendObj = {
            'playlist_name': `${singlePlaylistName} - Clean`,
            'description': '',
            'ids': sendID
        }
        const response = await axios.put(`${process.env.API_URL}/spotify/playlists`, sendObj ,{
            headers: {
                Authorization: 'Bearer ' + Cookies.get('jwt')
            }
        });
        viewPlaylist(response.data.playlistID);
    }
}
</script>