<template>
    <div class="parking_lots">

        <h1>Parking Lots</h1>
        <v-container fluid class="mx-1">

            <v-progress-circular
                    indeterminate
                    color="primary"
                    v-if="!this.lots"
            ></v-progress-circular>


            <v-row align="center">
                <v-col cols="12" sm="6" xs="12" lg="3" v-for="lot in lots" :key="lot.id">

                    <v-card xs="12" sm="6" lg="4" router :to="`lot/${lot.id}`">
                        <v-responsive>
                            <v-icon class="text-center" color="blue" size="100">local_parking</v-icon>
                        </v-responsive>

                        <v-card-title>{{ lot.name }}</v-card-title>

                        <v-card-subtitle>{{ lot.lastUpdate }}</v-card-subtitle>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>

    </div>
</template>

<script>
    const api = require('../api/api');
    export default {
        name: "ParkingLots",
        data: () => {
            return {
                lots: []
            }
        },
        mounted() {
            api.getLots((response) => this.lots = response)
        }
    }
</script>

<style scoped>
    .full {
        border-left: 4px solid tomato;
    }
</style>