<template>
    <div id="app">
      <apexchart height="500" width="1200" type="scatter" :options="options" :series="series"></apexchart>
    </div>
</template>
  
<script>
import patients_count from '../data/mental_health_totals.json';
import happiness from '../data/happiness_sa3.json';
import population from '../data/pop_totals.json';
export default {
  data() {
    const combinedData = population.map(item1 => {
      const matchingItem1 = patients_count.find(item2 => item2.sa3Code === item1.sa3Code);
      const matchingItem2 = happiness.find(item3 => item3.sa3Code === item1.sa3Code);
      if (matchingItem1 && matchingItem2) {
        return {
          sa3code: item1.sa3Code,
          y: matchingItem1.total / item1.pop_total,
          x: matchingItem2.happiness,
        };
      }
      return null;
    }).filter(item => item !== null);

    // Filter outliers based on z-scores
    const filteredData = this.filterOutliers(combinedData, 'y'); // Choose 'x' or 'y' based on the axis you want to filter

    return {
      options: {
        chart: {
          type: 'scatter',
        },
        xaxis: {
          title: {
            text: 'Happiness',
          },
          labels: {
            show: false,
            formatter: function (value) {
              return value ? value.toFixed(3) : '';
            },
          },
        },
        yaxis: {
          title: {
            text: 'Presentation Count Ratio',
          },
          labels: {
            formatter: function (value) {
              return value ? value.toFixed(3) : '';
            },
          },
        },
      },
      series: [
        {
          name: 'Representation Count',
          data: filteredData,
        },
      ],
    };
  },
  methods: {
    filterOutliers(data, axis) {
      // Calculate the mean and standard deviation
      const values = data.map(item => item[axis]);
      const mean = this.calculateMean(values);
      const stdDev = this.calculateStandardDeviation(values);

      // Define the z-score threshold for outlier filtering
      const zScoreThreshold = 3; // Adjust this threshold as needed

      // Filter outliers based on z-scores
      const filteredData = data.filter(item => {
        const zScore = Math.abs((item[axis] - mean) / stdDev);
        return zScore <= zScoreThreshold;
      });

      return filteredData;
    },
    calculateMean(data) {
      // Calculate the mean of the data
      const sum = data.reduce((total, value) => total + value, 0);
      return sum / data.length;
    },
    calculateStandardDeviation(data) {
      // Calculate the standard deviation of the data
      const mean = this.calculateMean(data);
      const squaredDifferences = data.map(value => Math.pow(value - mean, 2));
      const sumSquaredDiff = squaredDifferences.reduce((total, value) => total + value, 0);
      const variance = sumSquaredDiff / data.length;
      return Math.sqrt(variance);
    },
  },
};

</script>
  
<style>
.custom-tooltip {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 8px;
}
</style>