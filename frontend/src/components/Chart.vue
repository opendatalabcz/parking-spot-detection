<script>
    import {Bar, mixins} from 'vue-chartjs';

    const {reactiveProp} = mixins;

    export default {
        extends: Bar,
        mixins: [reactiveProp],
        mounted() {

            this.renderChart(this.chartData, this.options || {
                responsive: true,
                maintainAspectRatio: false,
                responsiveAnimationDuration: 500,
                scales: {
                    yAxes: [{
                        stacked: true
                    }],
                    xAxes: [{
                        stacked: true
                    }]
                }

            });

        }
    }
</script>

<style>
</style>