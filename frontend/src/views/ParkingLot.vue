<template>

    <div>
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

            <v-btn @click="removeRectangle"  color="error" class="text--black">
                <v-icon left>mdi-delete</v-icon>
                <span>Delete</span>
            </v-btn>
            <fabric-canvas ref="canvas" :height="canvasHeight" :width="canvasWidth">
                <fabric-Rectangle ref="canvasSpots" v-for="spot in spots" :key="spot.id"
                                  :id="'rightFoot'"
                                  :borderColor="'#00ff00'"
                                  :hasBorder="true"
                                  :left.sync="spot.coordinates[0]"
                                  :top.sync="spot.coordinates[1]"
                                  :width.sync="spot.width"
                                  :height.sync="spot.height"
                                  :strokeDashArray="[0,0]"
                                  :stroke="'green'"
                                  :fill="'#00000000'"
                                  :strokeWidth="2"
                                  :borderScaleFactor="0"
                                  :originX="'left'"
                                  :originY="'top'"
                ></fabric-Rectangle>

            </fabric-canvas>

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
            api.getLotDetail(this.lotId).then(response => this.lot = response.data);
            api.getLotSpots(this.lotId).then(response => {
                for (let spot of response.data) {
                    spot.width = spot.coordinates[2] - spot.coordinates[0];
                    spot.height = spot.coordinates[3] - spot.coordinates[1];
                }
                this.spots = response.data;
            });
            this.canvas = this.$refs.canvas.canvas;

            this.canvas.setBackgroundImage("http://localhost:8000/media/snapshot.jpg", (image) => {
                this.canvasWidth = image.width;
                this.canvasHeight = image.height;
            })
        },
        methods: {
            addParkSpace() {
                this.spots.push({"coordinates": [50, 50, 50, 50], "status": 1})
            },
            addBlocker() {
                this.spots.push({"coordinates": [50, 50, 50, 50], "status": 0})
            },
            removeRectangle() {
                this.canvas.remove(this.canvas.getActiveObject())
            }
        },
        watch: {
            // spots: {
            //     handler: function () {
            //         // console.log(newspots[0].coordinates+", "+newspots[0].width+", "+newspots[0].height)
            //         console.log(this.$refs.canvasSpots[0].rect.aCoords)
            //     },
            //     deep:true
            // }
        }
    }
</script>

<style scoped>

</style>