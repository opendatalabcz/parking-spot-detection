<template>
    <div class="dashboard">
        <h1 class="">Dashboard</h1>

        <v-container fluid class="my-5">
            <v-row :columns="12">

                <v-card md-3 lg-3 xl-3 v-for="lot in lots" :key="lot.id">

                    <v-card-title>
                        {{ lot.name }}
                    </v-card-title>

                    <v-card-text>
                        <Chart :chart-data="chartData"
                               :styles="{
                        position: 'relative',
                        maintainAspectRatio: false
                    }"></Chart>
                    </v-card-text>
                </v-card>
            </v-row>
        </v-container>

        {{ labels }}

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
                newLots.forEach((item) => {
                    this.labels = item.info.map(x => x.timestamp);
                    this.availableDataset = item.info.map(x => x.available_spots);
                    this.fullDataset = item.info.map(x => x.full_spots)
                });

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
                            backgroundColor: 'green',
                            data: this.availableDataset
                        }, {
                            label: 'Number of Occupied Spots',
                            backgroundColor: 'red',
                            data: this.fullDataset
                        }
                    ]
                }
            }
        }
    }
</script>
