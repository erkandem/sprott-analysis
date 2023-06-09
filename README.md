# Plotting of Premium Discount Data Gained from Sprotts' Website

## Setup

Idea is to have a Vue app with axios and a charting library to visualize 
some data regarding premium and discounts

### Development Backend
While an API might be in place later, for now I will work with a JSON dump of pandas dataframe served
with a python CORS enabled dev server.
    cd data
    python3 -m server.py

### Charting libraries

#### Plotly.jy
Tried plotly, as the one is based on D3 and can hq plotting.
Doesn't work with Vue. Tried the integration https://github.com/David-Desmaisons/vue-plotly.
It's not ready for Vue 3. It has support for React though.

Some resources:
https://codepen.io/rhamner/pen/MXgWqJ?editors=1010

https://www.somesolvedproblems.com/2019/02/tutorial-writing-vue-app-from-start-to.html
https://github.com/rhamner/vue-test/blob/master/src/components/PlotlyGraph.vue

https://www.somesolvedproblems.com/2018/05/how-to-use-plotly-in-vue.html

#### Chart.js
It looks nice and simple but more like a toy library.
I won't be able to do complex stuff with it.
Vue integration: https://github.com/apertureless/vue-chartjs/
Docs: https://www.chartjs.org/docs/latest/getting-started/integration.html

#### ECharts
Found ECharts based on D3 with good integration to Vue and many features.
Leaving a git commit of it  just in case.

#### HighCharts

works, got vue plugin maintained by HighCharts itself
https://github.com/highcharts/highcharts-vue

Histogramm doesn't work???

#### uPlot
https://github.com/leeoniya/uPlot

#### Mentions
Component library: https://vuetifyjs.com/en/

Eco System list: https://github.com/vuejs/awesome-vue


Snipped to calculate statistics in JS using simplestatistics
https://simplestatistics.org/docs/#mean
```js
const premium_pct = document.lol.map((elm) => {return elm["premium_pct"]})
const sigma = ss.standardDeviation(premium_pct.slice(premium_pct.length - 250, premium_pct.length - 1))
const mean = ss.mean(premium_pct.slice(premium_pct.length - 250, premium_pct.length - 1))
const last = premium_pct[premium_pct.length - 1]
```


Reintroduced plotly after I found a working solution for plotly and vue3
 - Combine Backend sprottwatch and Frontend application sprottwatch-fe
 - combine the file hosting server with the calculation server (histogram)
 - distinguish API of backend from backend which scrape data
 - introduce a database to feed the values in
 - get the value via API from the database instead of the file
 - throw in a nice styling for the one-page data app
 - deploy
 - tests
 - CI
 - CD
