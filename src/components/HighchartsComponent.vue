<script setup>
import { onMounted } from 'vue'

const props = defineProps(['chartOptions'])

onMounted(() => {
})
</script>

<template>
    <highcharts
        class="hc"
        :options="chartOptions"
        ref="chart"
    >
    </highcharts>
</template>

<style scoped>
</style>