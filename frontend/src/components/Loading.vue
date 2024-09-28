<template>
    <div class="hero min-h-screen">
        <div class="hero-content text-center">
            <div class="max-w-md">
                <span class="loading loading-spinner loading-lg"></span>
                <p>{{message}}</p>
        </div>
    </div>
</div>
</template>

<script>
export default{
    props: ["message"]
}
</script>