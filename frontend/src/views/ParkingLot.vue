<template>

    <div>

        <v-navigation-drawer
                v-model="isRightDrawerOpened"
                app
                right
                color="primary"
        >


            <v-container>


                <h1>Lot Settings</h1>
                <v-row justify="center">
                    <v-text-field
                            class="text--black"
                            color="black"
                            v-model="detectionTTL"
                            label="Detection TTL"
                            required
                    ></v-text-field>
                </v-row>
                <v-row justify="center">
                    <v-text-field
                            class="text--black"
                            color="black"
                            v-model="videoSrc"
                            :counter="2000"
                            label="Stream / Video URL"
                            required
                    ></v-text-field>
                </v-row>
                <v-row justify="center">
                    <v-switch :label="`Detection ${this.detectionRunning ? 'running' : 'stopped'}`"
                              v-model="detectionRunning" color="secondary"></v-switch>
                </v-row>

                <v-row justify="center">
                    <v-btn @click="saveSettings" color="success" class="text--black ma-2">
                        <v-icon left>save</v-icon>
                        <span>Save</span>
                    </v-btn>
                </v-row>
            </v-container>

        </v-navigation-drawer>

        <v-progress-linear
                indeterminate
                color="yellow darken-2"
                v-if="loading"
        ></v-progress-linear>


        <v-container class="mx-0 px-0">

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
            <v-row justify="space-between">
                <h1 class="ml-5">{{ lot.name }}</h1>

                <v-icon class="mr-2" @click="() => { this.isRightDrawerOpened = !this.isRightDrawerOpened}" large>
                    settings
                </v-icon>
            </v-row>

            <v-row justify="space-around">
                <v-col class="px-5" sm="12" md="6" xs="12" lg="6">
                    <span>Occupied spots: {{ lot.history__num_occupied || 0 }}</span>
                    <v-spacer></v-spacer>
                    <span>Available spots: {{ lot.history__num_vacant || 0 }}</span>

                    <v-spacer></v-spacer>
                    <span>Last update: {{ lot.history__timestamp ? new Date(lot.history__timestamp).toLocaleString() : "N/A"  }}</span>
                </v-col>
                <v-col sm="12" md="6" xs="12" lg="6">
                    <v-card>
                        <v-card-title>Lot History Chart</v-card-title>
                        <v-card-text>
                            <Chart v-if="history" sm="6" md="4" xs="12" lg="4" :chart-data="getChartDataForLot(history)"
                                   :styles="{
                                                position: 'relative',
                                                maintainAspectRatio: false
                                                }"
                            />
                        </v-card-text>
                    </v-card>

                </v-col>
            </v-row>

            <v-card>
                <v-card-title>
                    Parking Lot Detection Overview
                </v-card-title>
                <v-row justify="center">

                    <v-col cols="12">
                        <v-btn @click="addParkSpace" color="success" class="text--black ma-2">
                            <v-icon left>mdi-plus</v-icon>
                            <span>Add Parking Space</span>
                        </v-btn>

                        <v-btn @click="addBlocker" color="error" class="text--black">
                            <v-icon left>mdi-plus</v-icon>
                            <span>Add Blocker</span>
                        </v-btn>


                        <v-btn @click="saveChanges" color="success" class="text--black ma-2">
                            <v-icon left>save</v-icon>
                            <span>Save Changes</span>
                        </v-btn>
                        <v-spacer/>

                        <v-btn :disabled="!selectedRectangle" @click="removeRectangle" color="error"
                               class="text--black ma-2">
                            <v-icon left>mdi-delete</v-icon>
                            <span>Delete</span>
                        </v-btn>

                        <v-btn :disabled="!selectedRectangle" @click="isDetailOpened = true" color="success"
                               class="text--black">
                            <v-icon left>info</v-icon>
                            <span>Show Detail</span>
                        </v-btn>
                    </v-col>
                </v-row>


                <v-row :columns="12">

                    <v-col sm="6" md="4" xs="12" lg="4">
                        <fabric-canvas justify="center" ref="canvas" :height="canvasHeight" :width="canvasWidth">
                            <fabric-Rectangle ref="canvasSpots" v-for="(spot) in spots" :key="spot.id"
                                              :id="spot.id || ''"
                                              :borderColor="'orange'"
                                              :hasBorder="true"
                                              :left="spot.coordinates[0]"
                                              :top="spot.coordinates[1]"
                                              :width="spot.coordinates[2] - spot.coordinates[0]"
                                              :height="spot.coordinates[3] - spot.coordinates[1]"
                                              :strokeDashArray="[0,0]"
                                              :stroke="spotColors[spot.status.toString()]"
                                              :fill="'#00000000'"
                                              @mousedown="onRectangleClick"
                                              :strokeWidth="2"
                                              :borderScaleFactor="0"
                                              :originX="'left'"
                                              :originY="'top'"
                            ></fabric-Rectangle>

                        </fabric-canvas>
                    </v-col>
                </v-row>
            </v-card>

        </v-container>

        <v-dialog v-model="isDetailOpened" transition="dialog-bottom-transition">

                <v-row :columns="12">
                    <v-col md="12" sd="12" xs="12" lg="12">
                        <v-card>
                            <v-toolbar color="primary">
                                <v-btn icon @click="isDetailOpened = false">
                                    <v-icon>mdi-close</v-icon>
                                </v-btn>
                                <v-spacer></v-spacer>
                            </v-toolbar>

                            <v-card-title>
                                <h2>Parking Spot ID: {{ selectedRectangle }}</h2>

                            </v-card-title>

                            <v-card-text style="display:block;">
                                <h3>History of this spot in time:</h3>
                                <Chart style="height:400px;"
                                       v-if="selectedRectangleHistory && selectedRectangleHistory.labels.length"
                                       :chart-data="selectedRectangleHistory"

                                       :styles="{

                                                position: 'relative',
                                                maintainAspectRatio: false,
                                                responsive: true
                                                }"
                                />
                                <p v-if="!selectedRectangleHistory || !selectedRectangleHistory.labels.length">No data
                                    has been
                                    found for this spot.</p>
                            </v-card-text>


                        </v-card>
                    </v-col>
                </v-row>

        </v-dialog>

    </div>
</template>

<script>
    import vueFabricWrapper from "vue-fabric-wrapper";

    const api = require('../api/api');
    import Chart from "../components/Chart";

    export default {
        name: "ParkingLot",
        components: {
            Chart,
            FabricCanvas: vueFabricWrapper.FabricCanvas,
            FabricRectangle: vueFabricWrapper.FabricRectangle
        },
        data() {
            return {
                seedId: 0,
                loading: false,
                lot: {},
                spots: [],
                lotId: this.$route.params.id,
                canvas: null,
                canvasWidth: 500,
                canvasHeight: 500,
                spotColors: {
                    "-1": "yellow",
                    "0": "red",
                    "1": "green"
                },
                rightFootPosLeft: 300,
                rightFootPosTop: 350,
                selectedRectangleHistory: null,
                selectedRectangle: null,
                isDetailOpened: false,
                isRightDrawerOpened: false,
                detectionRunning: false,
                detectionTTL: 30.0,
                videoSrc: "",
                showSnackbar: false,
                snackbarText: "",
                history: []
            }
        },
        mounted() {
            this.canvas = this.$refs.canvas.canvas;
            api.getLotDetail(this.lotId).then(response => {
                console.log(response.data)
                this.lot = response.data
            });

            api.getLotHistory(this.lotId).then(response => {
                this.history = response.data
            })
            api.getLotSpots(this.lotId).then(response => {
                this.spots = response.data;
            });
            api.getLotSettings(this.lotId).then(response => {
                let d = response.data
                this.detectionRunning = d.running;
                this.detectionTTL = d.ttl_to_accept;
                this.videoSrc = d.video_src;
            })

            this.canvas.setBackgroundImage(api.getSnapshotUrl(this.lotId), (image) => {
                this.canvasWidth = image.width;
                this.canvasHeight = image.height;
            });

            this.canvas.on("mouse:down", (e) => {
                this.onCanvasClick(e)
            });
        },
        methods: {
            addParkSpace() {
                this.spots.push({id: "spot" + this.seedId, "coordinates": [50, 50, 100, 100], "status": 1});
                this.seedId++;
            },
            addBlocker() {
                this.spots.push({id: "blocker" + this.seedId, coordinates: [50, 50, 100, 100], "status": 0});
                this.seedIt++;
            },
            removeRectangle() {
                this.canvas.remove(this.canvas.getActiveObject())
            },
            saveChanges() {
                this.loading = true;
                const spotsCopy = JSON.parse(JSON.stringify(this.spots.filter(spot => typeof spot.id == "number")));

                const results = [];
                this.canvas.getObjects().forEach(o => {
                    const c = o.oCoords;
                    const coords = [c.tl.x, c.tl.y, c.br.x, c.br.y].map(x => parseInt(x));

                    if (typeof o.id == "number") {
                        let spot = spotsCopy.find(spot => spot.id === o.id);
                        spot.coordinates = coords;
                        results.push(spot)
                    } else {
                        results.push({id: -1, coordinates: coords, status: o.id.includes("spot") ? 1 : 0})
                    }

                });

                api.uploadSpots(this.lotId, results).then(response => {
                    this.spots = response.data;
                    this.loading = false;
                })

            },
            async onRectangleClick(e) {
                this.selectedRectangle = e.id;
                const data = (await api.getSpotHistory(this.lotId, e.id)).data;
                this.selectedRectangleHistory = this.getChartDataForSpot(data);
            },
            getChartDataForSpot(history) {
                history.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
                return {
                    labels: history.map(h => new Date(h.timestamp).toLocaleString()),
                    datasets: [
                        {
                            label: 'Occupancy Status',
                            borderColor: 'orange',
                            data: history.map(h => h.occupancy == 1 ? 1 : -1)
                        }
                    ]
                }
            },
            getChartDataForLot(history) {
                return {
                    labels: history.map(h => new Date(h.timestamp).toLocaleString()),
                    datasets: [
                        {
                            label: 'Number of Vacant Spots',
                            borderColor: 'green',
                            backgroundColor: 'green',
                            data: history.map(h => h.num_vacant)
                        }, {
                            label: 'Number of Occupied Spots',
                            borderColor: 'red',
                            backgroundColor: 'red',
                            data: history.map(h => h.num_occupied)
                        },
                        {
                            label: 'Number of Unknown Spots',
                            borderColor: 'gray',
                            backgroundColor: 'gray',
                            data: history.map(h => h.num_unknown)
                        }
                    ]
                }
            },
            onCanvasClick(e) {
                if (!e.target) {
                    this.selectedRectangleHistory = null;
                    this.selectedRectangle = null;
                }
            },
            saveSettings: function () {
                let data = {
                    'detection_running': this.detectionRunning,
                    'video_src': this.videoSrc,
                    'ttl': this.detectionTTL
                }

                api.saveSettings(this.lotId, data).then(response => {
                    this.snackbarText = "Saved successfully"
                    this.showSnackbar = true
                    let d = response.data
                    this.detectionRunning = d.running;
                    this.detectionTTL = d.ttl_to_accept;
                    this.videoSrc = d.video_src;
                }, () => {
                    this.snackbarText = "Something went wrong"
                    this.showSnackbar = true
                })

            }
        }
    }
</script>

<style scoped>
    .custom-label-color .v-label {
        color: black;
        opacity: 1;
    }
</style>