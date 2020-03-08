<template>
    <div class="parking_lots">
        <h1>Parking Lots</h1>
        <v-container fluid class="mx-5">

            <v-card class="lighten-4" flat v-for="lot in lots" :key="lot.name">
                <v-layout row wrap :class="[{'full': lot.capacity === lot.taken}, 'pa-3']">
                    <v-flex xs3 sm4 md6 class="justify-center">
                        <div class="caption grey--text">Name</div>
                        <div>{{ lot.name }}</div>
                    </v-flex>

                    <v-flex xs3 sm4 md2>
                        <div class="caption grey--text">Status</div>
                        <div>{{ lot.taken+"/"+lot.capacity }}</div>
                    </v-flex>

                    <v-flex xs3 sm4 md2>
                        <div class="caption grey--text">Last Update</div>
                        <div>{{ lot.lastUpdate }}</div>
                    </v-flex>

                    <v-flex xs3 sm4 md2>
                        <div class="right">
                            <v-chip class="caption my-2">
                                Edit
                            </v-chip>
                        </div>
                    </v-flex>

                </v-layout>
                <v-divider/>

            </v-card>


        </v-container>
    </div>
</template>

<script>
    export default {
        name: "ParkingLots",
        data: () => {
            return {
                lots: [
                    {name: "Lot 1", taken: 10, capacity: 50, lastUpdate: "30.12.3021, 11:32"},
                    {name: "Lot 2", taken: 20, capacity: 50, lastUpdate: "30.12.2012, 11:32"},
                    {name: "Lot 3", taken: 0, capacity: 50, lastUpdate: "30.12.2020, 11:32"},
                    {name: "Lot 4", taken: 50, capacity: 50, lastUpdate: "30.12.3021, 11:32"},
                ]
            }
        }
    }
</script>

<style scoped>
    .full {
        border-left: 4px solid tomato;
    }
</style>