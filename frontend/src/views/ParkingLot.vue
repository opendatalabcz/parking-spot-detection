<template>

    <div>
            <v-progress-linear
      indeterminate
      color="yellow darken-2"
      v-if="loading"
    ></v-progress-linear>
        <h1>{{ lot.name }}</h1>


        <v-container class="mx-0 px-0">

            <v-btn @click="addParkSpace" color="success" class="text--black">
                <v-icon left>mdi-plus</v-icon>
                <span>Add Parking Space</span>
            </v-btn>

            <v-btn @click="addBlocker" color="error" class="text--black">
                <v-icon left>mdi-plus</v-icon>
                <span>Add Blocker</span>
            </v-btn>

            <v-btn @click="removeRectangle" color="error" class="text--black">
                <v-icon left>mdi-delete</v-icon>
                <span>Delete</span>
            </v-btn>
            <v-btn @click="saveChanges" color="success" class="text--black">
                <v-icon left>save</v-icon>
                <span>Save Changes</span>
            </v-btn>


            <v-row :columns="12">

                <v-col cols="12">
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
                                          :strokeWidth="2"
                                          :borderScaleFactor="0"
                                          :originX="'left'"
                                          :originY="'top'"
                        ></fabric-Rectangle>

                    </fabric-canvas>
                </v-col>
            </v-row>

        </v-container>


    </div>
</template>

<script>
    import vueFabricWrapper from "vue-fabric-wrapper";

    const api = require('../api/api');
    export default {
        name: "ParkingLot",
        components: {
            FabricCanvas: vueFabricWrapper.FabricCanvas,
            FabricRectangle: vueFabricWrapper.FabricRectangle
        },
        data() {
            return {
                seedId:0,
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
                rightFootPosTop: 350

            }
        },
        mounted() {
            this.canvas = this.$refs.canvas.canvas;
            api.getLotDetail(this.lotId).then(response => this.lot = response.data);
            api.getLotSpots(this.lotId).then(response => {
                this.spots = response.data;
            });

            this.canvas.setBackgroundImage("http://localhost:8000/media/snapshot.jpg", (image) => {
                this.canvasWidth = image.width;
                this.canvasHeight = image.height;
            })
        },
        methods: {
            addParkSpace() {
                this.spots.push({id:"spot"+this.seedId, "coordinates": [50, 50, 100,100], "status": 1});
                this.seedId++;
            },
            addBlocker() {
                this.spots.push({id:"blocker"+this.seedId, coordinates: [50, 50, 100, 100], "status": 0});
                this.seedIt++;
            },
            removeRectangle() {
                this.canvas.remove(this.canvas.getActiveObject())
            },
            saveChanges() {
                this.loading = true;
                const spotsCopy = JSON.parse(JSON.stringify(this.spots.filter(spot => typeof spot.id == "number")));
                console.log(this.canvas.getObjects());

                const results = [];
                this.canvas.getObjects().forEach (o => {
                    const c = o.oCoords;
                    const coords = [c.tl.x, c.tl.y, c.br.x, c.br.y].map(x => parseInt(x));

                    if (typeof o.id == "number") {
                        let spot = spotsCopy.find(spot => spot.id === o.id);
                        spot.coordinates = coords;
                        results.push(spot)
                    }
                    else {
                        results.push({id:-1, coordinates: coords, status: o.id.includes("spot") ? 1 : 0})
                    }

                });

                console.log(results);
                api.uploadSpots(this.lotId, results).then( response => {
                    this.spots = response.data;
                    this.loading = false;
                })

            }
        }
    }
</script>

<style scoped>

</style>