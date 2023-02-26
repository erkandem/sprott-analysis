<script setup>
import PlotlyLib from 'plotly.js-basic-dist'
import { onMounted, watch } from 'vue';

const props = defineProps({
    data: {type: Array, required: true},
    layout: {type: Object, required: true},
    config: {type: Object, required: true},
})

const id = Date.now()

const update = watch(props.data,
    () => {
    return PlotlyLib.react(
        `${id}`,
        props.data,
        props.layout,
        props.config
    )}
)

onMounted(() => {
    return PlotlyLib.newPlot(
        `${id}`,
        props.data, 
        props.layout,
        props.config
    )
})

</script>

<template>
  <div v-bind:id="id" ></div>
</template>

