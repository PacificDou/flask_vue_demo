<script>
import CanvasJSChart from './CanvasJSVueComponent.vue';

var server_url = "http://localhost:11280/stock/";

export default {
  components : {
    CanvasJSChart,
  },
  data () {
    return {
      chart: null,
      data: [],
      start_date: '2020-01-01',
      options: {
        animationEnabled: true,
        //exportEnabled: true,
        title:{
          text: ""
        },
        legend: {
          horizontalAlign: "left", // "center" , "right"
          verticalAlign: "center",  // "top" , "bottom"
          fontSize: 15
        },
        axisX: {
          title: "Date",
          // labelFormatter: (e) => {
          //   var suffixes = ["", "K", "M", "B"];
          //   var order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);
          //   if(order > suffixes.length - 1)
          //     order = suffixes.length - 1;
          //   var suffix = suffixes[order];
          //   return (e.value / Math.pow(1000, order)) + suffix;
          // }
        },
        axisY: {
          title: "Price (scaled)",         
          // labelFormatter: (e) => {
          //   var suffixes = ["", "K", "M", "B"];
          //   var order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);
          //   if(order > suffixes.length - 1)
          //     order = suffixes.length - 1;
          //   var suffix = suffixes[order];
          //   return (e.value / Math.pow(1000, order)) + suffix;
          // }
        },
        data: [{
          type: "line",
          color: "red",
          showInLegend: true,
          xValueFormatString: "YYYY-MM-DD",
          dataPoints: []
        },
        {
          type: "line",
          color: "green",
          showInLegend: true,
          xValueFormatString: "YYYY-MM-DD",
          dataPoints: []
        },
        {
          type: "line",
          color: "blue",
          showInLegend: true,
          xValueFormatString: "YYYY-MM-DD",
          dataPoints: []
        }],
      },
      styleOptions: {
        width: "100%",
        height: "360px"
      }
    }
  },
  methods: {
    parseDataAndRenderChart(url) {
      fetch(url).then(response => response.json()).then(this.renderData);
    },
    renderData(data) {
      this.data = data;
      for (let i = 0; i < data.length; ++i) {
        let scale = data[i].prices[0] / 100.0;
        let dates = data[i].dates;
        let prices = data[i].prices;
        this.options.data[i].legendText = data[i].name;
        this.options.data[i].dataPoints = [];
        for(var j = 0; j < prices.length; ++j) {
          this.options.data[i].dataPoints.push({x: new Date(dates[j]), y: prices[j] / scale});
        }
      }
      this.chart.render();
    },
    chartInstance(chart) {
      this.chart = chart;
      this.parseDataAndRenderChart(server_url + this.start_date);
    },
    reload() {
      let now = new Date();
      let minDate = new Date("2010-01-01");
      let startDate = new Date(this.start_date);
      if (startDate < minDate || startDate >= now) {
        alert("Invalid start date!");
        return;
      }
      this.parseDataAndRenderChart(server_url + this.start_date);
    }
  },
  watch: {
    start_date(new_date) {
    }
  }
}
</script>

<template>
  <div style="margin: 0 auto; width: 70%;"> 
    <label for="startDate">Choose start date</label> &nbsp;&nbsp;
    <input v-model="start_date" type="date" name="startDate" min="2010-01-01"> &nbsp;&nbsp;
    <button @click="reload()">Reload</button>
  </div>
  <br>


  <div>
    <CanvasJSChart :options="options" :style="styleOptions" @chart-ref="chartInstance"/>
  </div>

  <div style="margin: 0 auto; width: 70%;">
    <table v-if="data.length > 0" style="margin: 0 auto;">
      <tr>
        <th>Stock</th>
        <th>Cumulative Return</th>
        <th>Annualized Return</th>
        <th>Annualized Volatility</th>
      </tr>
      <tr v-for="stock in data">
        <td>{{ stock.name }}</td>
        <td>{{ (stock.cumulative_return * 100).toFixed(2) + "%" }}</td>
        <td>{{ (stock.annualized_return * 100).toFixed(2) + "%" }}</td>
        <td>{{ stock.annualized_volatility.toFixed(2) + "%" }}</td>
      </tr>
    </table>
  </div>
</template>

<style>
table, td, th {
  border: 1px solid black;
}

table {
  border-collapse: collapse;
}
</style>
