<template>
  <div id="app">
    <apexchart height= "500" width="1200" type="line" :options="options" :series="series"></apexchart>
  </div>
</template>

<script>
import monthlyIncome from '../data/monthly-income-data.json';
import incomeCutOff from '../data/deciles.json';

export default {
  data() {
    const apiEndpoint = 'http://172.26.129.91:9101/happiness_sa3';

    fetch(apiEndpoint)
      .then(response => response.json())
      .then(data => {
        const combinedData = data.map(item1 => {
          const matchingItem = monthlyIncome.find(item2 => item2.sa3Code === item1.sa3Code);
          if (matchingItem) {
            return {
              sa3code: item1.sa3Code,
              happiness: item1.happiness,
              monthlyIncome: matchingItem.monthlyIncome
            };
          }
          return null;
        }).filter(item => item !== null);

        const maxIncome = Math.max(...combinedData.map(item => item.monthlyIncome));

        const intervalRanges = incomeCutOff.map((item, index) => {
          const start = item.incomeCutOff;
          const end = index === incomeCutOff.length - 1 ? maxIncome : incomeCutOff[index + 1].incomeCutOff;
          return { start, end };
        })
        .slice(0, -1);

        const intervalAverages = intervalRanges.map(interval => {
          const filteredData = combinedData.filter(item => item.monthlyIncome >= interval.start && item.monthlyIncome < interval.end);
          const averageHappiness = filteredData.length > 0
            ? filteredData.reduce((sum, item) => sum + item.happiness, 0) / filteredData.length
            : 0;
          return averageHappiness;
        });

        const intervalLabels = intervalRanges.map(interval => `${interval.start.toFixed(0)} - ${interval.end.toFixed(0)}`);

        const seriesColors = ['#FF0000'];

        this.options = {
          xaxis: {
            categories: intervalLabels,
            labels: {
              show: true
            },
            title: {
              text: 'Monthly Income Intervals'
            }
          },
          yaxis: {
            labels: {
              formatter: function (value) {
                return value.toFixed(3);
              }
            },
            title: {
              text: 'Average Happiness'
            }
          },
          colors: seriesColors, 
        };
        this.series = [
          {
            name: 'Happiness',
            data: intervalAverages,
          }
        ];
      });

    return {
      options: {},
      series: [],
    };
  }
};
</script>

<style>
.custom-tooltip {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 8px;
}
</style>