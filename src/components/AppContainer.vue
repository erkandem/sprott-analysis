<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import {
  uraniumFilename,
  baseUrl,
  extractSeriesForPlotlyFormat,
} from "/src/client/client.js";
import { VuePlotly } from "vue3-plotly";

const responseData = ref(null);

let premiumDiscountChartData = ref([
  {
    x: ["2012-05-06", "2012-05-07", "2012-05-08", "2012-05-09"],
    y: [0, 1, 2, 3],
    color: "#C8A2C8",
    type: "scatter",
    line: { width: 2.5 },
  },
]);
const premiumDiscountChartLayout = ref({});
const premiumDiscountChartConfig = ref({ responsive: true });

const uraniumHistogramResponseData = ref(null);
const histogramLayout = ref({});
const histogramData = ref([{}]);
const histogramConfig = ref({ responsive: true });

const loadPremiumDiscountChart = () => {
  axios
    .get(baseUrl + "premium-discount" + "/" + uraniumFilename)
    .then((result) => {
      responseData.value = result.data;
      console.log(result.data);
      const seriesData = extractSeriesForPlotlyFormat(
        result.data,
        "date",
        "premium_pct"
      );
      console.log(seriesData);
      premiumDiscountChartData.value = [
        {
          x: seriesData.x,
          y: seriesData.y,
          color: "#C8A2C8",
          type: "scatter",
          line: { width: 1 },
        },
      ];
      premiumDiscountChartLayout.value["title"] =
        "Premium or Discount as Percentage of Sprott Uranium Trusts' NAV";
      premiumDiscountChartLayout.value["yaxis"] = {
        title: "Premium or Discount in % of NAV [%]",
      };
    })
    .catch((error) => {
      console.log(String(error));
    });
};
const loadUraniumHistogram = () => {
  axios
    .get(baseUrl + "histogram" + "/" + "uranium")
    .then((result) => {
      uraniumHistogramResponseData.value = result.data;
      histogramData.value = [result.data];
      histogramData.value[0]["type"] = "bar";
      histogramLayout.value["xaxis"] = {
        title: "Premium or Discount in % of NAV [%]",
      };
      histogramLayout.value["yaxis"] = { title: " Number of Trading Days [1]" };
      // TODO: untangle N trading days from other server
      histogramLayout.value[
        "title"
      ] = `Premium or Discount Histogram last ${responseData.value.length} Trading Days`;
      histogramData.value[0]["orientation"] = "v";
    })
    .catch((error) => {
      console.log(String(error));
    });
};

onMounted(loadPremiumDiscountChart);
onMounted(loadUraniumHistogram);
</script>
<template>
  <main>
    <div class="premium-discount-chart">
      <VuePlotly
        v-bind:data="premiumDiscountChartData"
        v-bind:layout="premiumDiscountChartLayout"
        v-bind:config="premiumDiscountChartConfig"
      />
    </div>
    <div class="premium-discount-histogram">
      <VuePlotly
        v-bind:data="histogramData"
        v-bind:layout="histogramLayout"
        v-bind:config="histogramConfig"
      />
    </div>
  </main>
</template>
