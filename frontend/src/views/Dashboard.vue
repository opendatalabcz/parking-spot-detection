<template>
    <div class="dashboard">
        <h1 class="">Dashboard</h1>

        <v-container fluid class="my-5">
            <v-row>
                <v-col sm="12" md="6" xs="12" lg="4">
                    <v-card router :to="'/addLot'">
                        <v-card-title>
                            <v-icon large>mdi-plus</v-icon>
                        </v-card-title>

                        <v-card-text>
                            <h2>Create new lot</h2>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row :columns="12">

                <v-col v-for="lot in lots" sm="6" md="4" xs="12" lg="4" :key="lot.id">
                    <v-card router :to="`lot/${lot.id}`">

                        <v-img max-height="290" v-bind:src="getSnapshot(lot.id)">
                            <template v-slot:placeholder>
                                <v-row
                                        class="fill-height ma-0"
                                        align="center"
                                        justify="center"
                                >
                                    <v-progress-circular indeterminate color="primary lighten-5"></v-progress-circular>
                                </v-row>
                            </template>
                        </v-img>

                        <v-card-subtitle>
                            <v-row :columns="12">
                                    <v-col>
                                        <h2>{{ lot.name }}</h2>
                                        <span>Occupied spots: {{ lot.num_occupied || 0 }}</span>
                                        <v-spacer></v-spacer>
                                        <span>Available spots: {{ lot.num_vacant || 0 }}</span>

                                        <v-spacer></v-spacer>
                                        <span>Last update: {{ lot.timestamp ? new Date(lot.timestamp).toLocaleString() : "N/A"  }}</span>
                                    </v-col>
                            </v-row>
                        </v-card-subtitle>
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
    const axios = require('axios').default;
    // @ is an alias to /src

    export default {
        name: 'Dashboard',
        data() {
            return {
                lots: [],
                history: []
            }
        },
        async mounted() {
            this.lots = (await api.getLots()).data;
            const allHistory = await axios.all(this.lots.map(lot => api.getLotHistory(lot.id)));
            this.history = allHistory.map((x) => x.data);
        },
        methods: {

            getSnapshot(lotId) {
                return api.getSnapshotUrl(lotId)
            },
            getChartDataFor(history) {
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


            }

        }
    }
</script>
