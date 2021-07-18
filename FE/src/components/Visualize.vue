<template>
  <div>
    <div>
      <apexchart
        v-if="lineChart"
        type="line"
        :height="chartHeight"
        :options="lineChart.options"
        :series="lineChart.series"
      />
    </div>
    <div class="mt-3">
      <apexchart
        v-if="barChart"
        type="bar"
        :height="chartHeight"
        :options="barChart.options"
        :series="barChart.series"
      />
    </div>
  </div>
</template>

<script>
import ReportServices from '../services/report-services';

export default {
  components: {},
  data() {
    return {
      chartHeight: 500,
      lineChart: undefined,
      barChart: undefined,
      isNodata: false,
    };
  },
  mounted() {
    this.getReport();
    this.resizeChart();
  },
  methods: {
    resizeChart() {
      const height = window.innerHeight;
      const chartHeight = height / 2 - 30;
      this.chartHeight = chartHeight;
    },
    initBarChart(data) {
      this.barChart = {
        options: {
          chart: {
            id: 'barchart',
            width: '100%',
          },
          xaxis: {
            categories: ['Good health', 'Bad health', 'Total'],
          },
          title: {
            text: 'Bar plot of number submit',
            align: 'center',
          },
        },
        series: [
          {
            name: 'Number submit',
            data: [
              data.good_health,
              data.bad_health,
              data.good_health + data.bad_health,
            ],
          },
        ],
      };
    },
    initLineChart(data) {
      this.lineChart = {
        options: {
          chart: {
            id: 'linechart',
            width: '100%',
          },
          xaxis: {
            categories: data.new_date,
          },
          title: {
            text: 'Number submit by time',
            align: 'center',
          },
        },
        series: [
          {
            name: 'Number submit',
            data: data.number_submit,
          },
        ],
      };
    },
    convertLineChartData(data) {
      this.lineChartData = {
        labels: data.new_date,
        datasets: data.number_submit,
      };
    },
    getReport() {
      ReportServices.getReportData(
        (resp) => {
          if (resp.data) {
            var result = resp.data;
            this.initLineChart(result);
            this.initBarChart(result);
          } else {
            this.isNodata = true;
          }
        },
        () => {
          this.isNodata = true;
        }
      );
    },
  },
};
</script>

<style scoped></style>
