<template>
    <v-card>
        <v-card-title>
            <h1>New Parking Lot</h1>
        </v-card-title>

        <v-form v-model="valid">
            <v-container>
                <v-snackbar
                        v-model="showSnackbar"
                >
                    {{ snackbarText }}
                    <v-btn
                            color="pink"
                            text
                            :timeout="5000"
                            @click="showSnackbar = false"
                    >

                    </v-btn>
                </v-snackbar>
                <v-row>
                    <v-col
                            cols="12"
                            md="4"
                    >
                        <v-text-field
                                v-model="name"
                                :counter="200"
                                label="Lot Name"
                                required
                        >

                        </v-text-field>
                        <v-text-field
                                v-model="videoSrc"
                                :counter="2000"
                                label="Video Source URI"
                                required
                        ></v-text-field>

                        <v-btn :disabled="!valid" color="success" class="mr-4" @click="send">
                            <v-icon left>save</v-icon>
                            <span>Create</span>
                        </v-btn>
                    </v-col>


                </v-row>

            </v-container>
        </v-form>
    </v-card>
</template>

<script>
    const api = require("../api/api");
    export default {
        name: "NewLot",
        data() {
            return {
                name: "",
                videoSrc: "",
                showSnackbar: false,
                snackbarText: ""
            }
        },

        computed: {
            valid() {
                return this.name !== "" && this.videoSrc !== "" && this.name.length <= 200 && this.videoSrc.length <= 2000
            }
        },
        methods: {
            async send() {
                try {
                    await api.createLot({"name": this.name, "video_src": this.videoSrc});
                    this.snackbarText = "Lot successfully created.";
                    this.name = "";
                    this.videoSrc = "";
                    this.showSnackbar = true;
                } catch (e) {
                    this.snackbarText = "Something went wrong."
                    this.showSnackbar = true;
                }

            }
        }
    }
</script>

<style scoped>

</style>