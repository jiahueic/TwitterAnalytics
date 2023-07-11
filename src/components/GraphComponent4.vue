<template>
  <div id="app">
    <template v-if="options.xaxis.categories.length">
      <apexchart height= "400" width="600" type="bar" :options="options" :series="series"></apexchart>
    </template>
  </div>
</template>

<script>
export default {
  data() {

    return {
      options: {
        chart: {
          type: 'bar',
        },
        xaxis: {
          type: 'category',
          categories: [],
          labels: {
            show: true,
          },
          title: {
            text: 'Mastodon Tags',
          },
        },
        yaxis: {
          title: {
            text: 'Count',
          },
        },
        dataLabels: {
          style: {
            colors: ['#9C27B0', '#9C27B0']
          }
        }
      },
      series: [
        {
          name: 'Count',
          data: [],
        },
      ],
    };
  
  },

  created() {
    //const apiEndpoint = 'http://172.26.129.91:9101/mastodon_tags/mentalhealth_about';
    const apiEndpoint = 'http://172.26.129.91:9101/mastodon_tags/top_10';
    //const apiEndpoint = 'http://172.26.129.91:9101/twitter_tags/top_10_2';
    

    fetch(apiEndpoint)
      .then(response => response.json())
      .then(data => {
        const tagCounts = data.map(item => Object.values(item)[0]);
        const tagNames = data.map(item => Object.keys(item)[0]);

        this.series[0].data = tagCounts;
        this.options.xaxis.categories = tagNames;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
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