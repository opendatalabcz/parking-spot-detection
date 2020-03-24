<script>
    import {Line, mixins} from 'vue-chartjs';

    const {reactiveProp} = mixins;

    export default {
        extends: Line,
        mixins: [reactiveProp],
        mounted() {

            this.renderChart(this.chartData, this.options || {
                responsive: true,
                maintainAspectRatio: false,
                responsiveAnimationDuration: 500,

            });

        }
    }
</script>

<style>
</style>