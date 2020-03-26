<template>
    <div class="dashboard">
        <h1 class="">Dashboard</h1>

        <v-container fluid class="my-5">
            <v-row :columns="12">

                <v-col v-for="lot in lots" sm="12" md="6" xs="12" lg="4" :key="lot.id">
                    <v-card router :to="`lot/${lot.id}`">


                        <v-card-title>

                            <v-row :columns="12">
                                <v-col>
                                    <h3>{{ lot.name }}</h3>
                                </v-col>
                            </v-row>

                        </v-card-title>

                        <hr class="grey lighten-4"/>
                        <v-card-text>

                            <v-row>
                                <v-col>
                                    <span>Occupied spots: {{ lot.num_occupied }}</span>
                                    <v-spacer></v-spacer>
                                    <span>Available spots: {{ lot.num_vacant }}</span>
                                </v-col>
                            </v-row>

                            <v-row :columns="12" >
                                <v-col>
                                    <span>Last update: {{ lot.timestamp }}</span>
                                </v-col>
                            </v-row>

                        </v-card-text>

                        <v-card-actions>
                            <v-btn outlined color="black" router :to="`lot/${lot.id}`">
                                <v-icon>edit</v-icon>
                                <span>Detail</span>
                            </v-btn>
                        </v-card-actions>

                    </v-card>
                </v-col>
            </v-row>
        </v-container>

    </div>
</template>

<script>
    const api = require('@/api/api');
    // @ is an alias to /src

    export default {
        name: 'Dashboard',
        data() {
            return {
                lots: []
            }
        },
        mounted() {
            api.getLots().then(response => this.lots = response.data)
        }
    }
</script>
