<template>
    <div id="app">
      <apexchart height="500" width="1200" type="bar" :options="options" :series="series"></apexchart>
    </div>
</template>
  
<script>
import patients_count from '../data/mental_health_totals.json';
import monthlyIncome from '../data/monthly-income-data.json';

export default {
  data() {
    const combinedData = patients_count.map(item1 => {
      const matchingItem = monthlyIncome.find(item2 => item2.sa3Code === item1.sa3Code);
      if (matchingItem) {
        return {
          sa3code: item1.sa3Code,
          patients_count: item1.total,
          monthlyIncome: matchingItem.monthlyIncome,
        };
      }
      return null;
    }).filter(item => item !== null);

    const minIncome = Math.min(...combinedData.map(item => item.monthlyIncome));
    const maxIncome = Math.max(...combinedData.map(item => item.monthlyIncome));
    const intervalCount = 5; // Adjust the number of intervals as needed

    const intervalSize = ((maxIncome - minIncome) / intervalCount);
    const intervalRanges = Array.from({ length: intervalCount }, (_, index) => {
      const start = minIncome + index * intervalSize;
      const end = start + intervalSize;
      return { start, end };
    });

    const intervalSums = intervalRanges.map(interval => {
      const filteredData = combinedData.filter(item => item.monthlyIncome >= interval.start && item.monthlyIncome < interval.end);
      const sumCount = filteredData.reduce((sum, item) => sum + item.patients_count, 0);
      return sumCount;
    });

    const intervalLabels = intervalRanges.map(interval => `${interval.start.toFixed(1)} - ${interval.end.toFixed(1)}`);

    const seriesColors = '#00FF00';
    
    return {
      options: {
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
          title: {
            text: 'Mental Health Presentations'
          }
        },
        colors: [seriesColors],
      },
      series: [
        {
          name: 'Patients Count',
          data: intervalSums,
        }
      ]
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