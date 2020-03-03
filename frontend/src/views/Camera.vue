<template>

    <v-row justify="center" fill-height>

        <v-card width="90%" class="justify-center">

            <object data="http://127.0.0.1:5000/video">
                <embed src="http://127.0.0.1:5000/video"/>
                Error: Embedded data could not be displayed.
            </object>
        </v-card>
    </v-row>
</template>

<script>
    export default {
        name: "Camera"
    }
</script>

<style scoped>

    object, embed {
        border: none;
        display: block;
        width: 100%;
        height: 100vh;
    }


</style>