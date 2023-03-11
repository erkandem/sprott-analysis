<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import {
    uraniumFilename,
    baseUrl,
    extractSeriesForHighChartsFormat
} from '/src/client/client.js'
import HighchartsComponent from './HighchartsComponent.vue'

let responseData = null
const chartOptions = ref({
        series: [{
            chart: {type: 'line'},
            data: [1,2,3]
        }]
})

onMounted(() => {
    axios.get(baseUrl + uraniumFilename)
    .then((result) => {
        responseData = result.data
        chartOptions.value.series[0].data = extractSeriesForHighChartsFormat(
            responseData,
            "date",
            "premium_pct"
        )
        chartOptions.value.series[0]["name"] ="P/D"
        chartOptions.value["xAxis"] = { type: 'datetime' }
        chartOptions.value["yAxis"] = [{"title": {"text": "Premium or Discount in % of NAV [%]"}}]
        chartOptions.value["title"] = {"text": "Premium Discount as Percentage of Sprott Uranium Trusts' NAV"}
    })
    .catch((error) => {
        console.log(String(error))
    })
})

</script>

<template>
    <main>
        <div class="price-chart">
        <HighchartsComponent v-bind:chartOptions="chartOptions"></HighchartsComponent>
        </div>
    </main>
</template>

<style scoped>
</style>
