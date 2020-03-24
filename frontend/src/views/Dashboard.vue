<template>
    <div class="dashboard">
        <h1 class="">Dashboard</h1>

        <v-container fluid class="my-5">
            <v-card v-for="lot in lots" :key="lot.id">


                <v-card-title>

                      <v-row :columns="12">
                          <v-col >
                              <h3>{{ lot.name }}</h3>
                          </v-col>
                        <v-col>
                            <span>Occupied spots: {{ takenSpots }}</span>
                            <v-spacer></v-spacer>
                            <span>Available spots: {{ freeSpots }}</span>
                        </v-col>
                    </v-row>
                </v-card-title>

                <hr class="grey lighten-4"/>
                <v-card-text>


                    <v-row :columns="12">
                        <v-col :xs="12" :sm="12" :md="6" :lg="6">


                            <Chart :chart-data="chartData"
                                   :styles="{
                                                position: 'relative',
                                                maintainAspectRatio: false
                                                }"
                            />


                        </v-col>

                        <v-col :xs="12" :sm="12" :md="6" :lg="6">


                                <div>
                                    <Chart :chart-data="chartData"
                                           :styles="{
                        position: 'relative',
                        maintainAspectRatio: false
                    }"></Chart>
                                </div>

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
        </v-container>

        {{ fullDataset }}

    </div>
</template>

<script>
    const api = require('@/api/api');
    import Chart from "@/components/Chart";
    // @ is an alias to /src

    export default {
        name: 'Dashboard',
        components: {Chart},
        data() {
            return {
                lots: [],
                lotInfos: [],
                labels: [],
                availableDataset: [],
                fullDataset: [],
                chartData: {}
            }
        },
        mounted() {
            api.getLots(true, (data) => {
                this.lots = data
            })
        },
        watch: {
            lots(newLots) {
                lot
                newLots.forEach((item) => {
                    item.info = item.info.sort((a, b) => Date.parse(a.timestamp) - Date.parse(b.timestamp));
                    this.labels = item.info.map(x => Date.parse(x.timestamp));
                    this.labels = this.labels.map(x => new Date(x).toLocaleString("cs-CZ"));
                    this.availableDataset = item.info.map(x => x.available_spots);
                    this.fullDataset = item.info.map(x => x.full_spots)
                });
                //
                // this.labels = this.labels.filter(function (value, index) {
                //     return index % 10 === 0;
                // });
                // this.availableDataset = this.availableDataset.filter(function (value, index) {
                //     return index % 10 === 0;
                // });
                // this.fullDataset = this.fullDataset.filter(function (value, index) {
                //     return index % 10 === 0;
                // });

                this.chartData = {
                    labels: this.labels,
                    datasets: [
                        {
                            label: 'Number of Available Spots',
                            borderColor: 'green',
                            data: this.availableDataset
                        }, {
                            label: 'Number of Occupied Spots',
                            borderColor: 'red',
                            data: this.fullDataset
                        }
                    ]
                }
            }
        },
        computed: {
            freeSpots: function () {
                return this.availableDataset.slice(-1).pop() || 0
            },
            takenSpots: function () {
                return this.fullDataset.slice(-1).pop() || 0
            }
        }
    }
</script>
