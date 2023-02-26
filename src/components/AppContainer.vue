<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { uraniumFilename, baseUrl, extractSeries } from '/src/client/client.js'
import Plotly  from "./Plotly.vue"

let responseData = null
let data = ref([{
    x: ["2012-05-06", "2012-05-07", "2012-05-08", "2012-05-09"],
    y: [0, 1, 2 , 3],
    color: "#C8A2C8",
    type: "scatter",
    line: { width: 2.5 }
}])
const layout = ref({})
const config = ref({})

onMounted(() => {
    axios.get(baseUrl + uraniumFilename)
    .then((result) => {
        responseData = result.data
        const seriesData = extractSeries(responseData, "date", "premium_pct")
        data.value = [{
            x: seriesData.x,
            y: seriesData.y,
            color: "#C8A2C8",
            type: "scatter",
            line: { width: 2.5 }
        }]
    })
    .catch((error) => {
        console.log(String(error))
    })
})

</script>

<template>
    <main>
        
        <div>
            <Plotly
            :data="data"
            :layout="layout"
            :config="config"
            ></Plotly>
        </div>
    </main>
</template>

<style scoped>
</style>
