<template>
    <div class="dashboard">
        <h1 class="">Dashboard</h1>

        <v-container fluid class="my-5">
            <v-row :columns="12">

                <v-col v-for="(lot, index) in lots" sm="12" md="6" xs="12" lg="4" :key="lot.id">
                    <v-card router :to="`lot/${lot.id}`">



                        <v-card-title>

                            <v-row :columns="12">
                                <v-col>
                                    <v-col>
                                        <h3>{{ lot.name }}</h3>
                                        <span>Occupied spots: {{ lot.num_occupied }}</span>
                                        <v-spacer></v-spacer>
                                        <span>Available spots: {{ lot.num_vacant }}</span>

                                        <v-spacer></v-spacer>
                                        <span>Last update: {{ new Date(lot.timestamp).toLocaleString() }}</span>
                                    </v-col>


                                </v-col>
                            </v-row>

                        </v-card-title>

                        <v-card-text>

                            <v-row>
                                <v-col>
                                    <Chart v-if="history[index]" :chart-data="getChartDataFor(history[index])"
                                           :styles="{
                                                position: 'relative',
                                                maintainAspectRatio: false
                                                }"
                                    />
                                </v-col>
                            </v-row>


                        </v-card-text>

                        <v-card-actions>
                            <v-btn  outlined color="black" router :to="`lot/${lot.id}`">
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
    import Chart from "../components/Chart";
    // @ is an alias to /src

    export default {
        name: 'Dashboard',
        components: {Chart},
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
            getChartDataFor(history) {
                return {
                    labels: history.map(h => new Date(h.timestamp).toLocaleString()),
                    datasets: [
                        {
                            label: 'Number of Vacant Spots',
                            borderColor: 'green',
                            data: history.map(h => h.num_vacant)
                        }, {
                            label: 'Number of Occupied Spots',
                            borderColor: 'red',
                            data: history.map(h => h.num_occupied)
                        },
                        {
                            label: 'Number of Unknown Spots',
                            borderColor: 'gray',
                            data: history.map(h => h.num_unknown)
                        }
                    ]
                }


            }

        }
    }
</script>
