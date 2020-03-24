<template>

    <div>
        <h1>{{ lot.name }}</h1>

        <v-progress-circular
                indeterminate
                color="primary"
                v-if="this.rects == {}"
        ></v-progress-circular>


        <v-container class="mx-0 px-0">

            <v-btn @click="addParkSpace" color="success" class="text--black">
                <v-icon left>mdi-plus</v-icon>
                <span>Add Parking Space</span>
            </v-btn>

            <v-btn @click="addBlocker" color="error" class="text--black">
                <v-icon left>mdi-plus</v-icon>
                <span>Add Blocker</span>
            </v-btn>

            <v-btn @click="removeRectangle" v-if="rectangleSelected !== null" color="error" class="text--black">
                <v-icon left>mdi-delete</v-icon>
                <span>Delete</span>
            </v-btn>

            <v-stage ref="stage" :config="stageSize" @click="imageClick">

                <v-layer>
                    <v-image ref="image" :config="{image:image}"/>
                </v-layer>

                <v-layer ref="rectsLayer">
                    <v-rect v-for="[{rect, state, ttl}, i] in rectangles.map((x,i) => [x,i])" :id="i" :config="{
                        x: rect[0],
                        y: rect[1],
                        width: rect[2] - rect[0],
                        height: rect[3] - rect[1],
                        stroke: rectColors[state],
                        draggable:true,
                        strokeScaleEnabled: false
                    }" :key="i" @click="transformRectangle" />



                </v-layer>
            </v-stage>


        </v-container>


    </div>
</template>

<script>
    const api = require('../api/api');
    export default {
        name: "ParkingLot",
        data() {
            return {
                lot: {},
                rects: {},
                lotId: this.$route.params.id,
                stageSize: {
                    width: 500,
                    height: 500
                },
                isDragging: false,
                image: null,
                rectangles: [],
                blockers: [],
                rectangleSelected: null,
                rectColors: {
                    "pending": "yellow",
                    "blocker": "red",
                    "accepted": "green"
                }

            }
        },
        mounted() {
            api.getLotDetail(this.lotId, (data) => this.lot = data);
            api.getLotRects(this.lotId, data => {
                data.image_url = api.getImageUrl(data.image_url);
                this.rects = data;
                this.rectangles = this.rects.rects
            });
        },
        methods: {

            addParkSpace() {
                this.rectangles.push([this.image.width / 2, this.image.height / 2, this.image.width / 2 + 100, this.image.height / 2 + 50])
            },
            addBlocker() {
                this.blockers.push([this.image.width / 2, this.image.height / 2, this.image.width / 2 + 100, this.image.height / 2 + 50])
            },
            removeRectangle() {
                this.rectangleSelected.destroy();
                this.removeCurrentTransformer()
            },
            removeCurrentTransformer() {
                const layer = this.$refs.stage.getStage();
                layer.find('Transformer').destroy();
                layer.draw();
                this.rectangleSelected = null;
            },
            imageClick(e) {
                if (e.target === this.$refs.image._konvaNode) {
                    this.removeCurrentTransformer()
                }
            },

            transformRectangle(e) {
                const layer = this.$refs.rectsLayer.getStage();
                layer.find('Transformer').destroy();
                const transformer = new window.Konva.Transformer({
                    rotateEnabled: false,
                    ignoreStroke: true
                });
                transformer.attachTo(e.target);
                layer.add(transformer);
                layer.draw();
                this.rectangleSelected = e.target;
            }
        },
        watch: {
            rects() {
                const image = new window.Image();
                image.src = this.rects.image_url;
                image.onload = () => {
                    this.image = image;
                    this.stageSize.width = image.width;
                    this.stageSize.height = image.height;
                };
            }
        }


    }
</script>

<style scoped>

</style>