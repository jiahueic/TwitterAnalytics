<template>
  <div id="app">
    <template v-if="options.xaxis.categories.length">
      <apexchart height="400" width="1200" type="bar" :options="options" :series="series"></apexchart>
    </template>
  </div>
</template>

<script>
//import tagApiEndpoint from '../data/mastadon_tags_top10.json';
export default {
  data() {
    
    return {
      options: {
        chart: {
          type: 'bar',
        },
        xaxis: {
          categories: [],
          labels: {
            show: true,
          },
          title: {
            text: 'Tags',
          },
          
        },
        yaxis: {
          labels: {
            style: {
              colors: '#000000', // Set the count number color to black
            },
          },
          title: {
            text: 'Percentage',
          },
        },
        dataLabels: {
          style: {
            colors: ['#9C27B0', '#9C27B0']
          }
        }
      },
      series: [],
    };
  },
  created() {
    
    //const tagApiEndpoint = 'http://172.26.129.91:9101/twitter_tags/top_10_2'; // Replace with your first API endpoint
    const tagApiEndpoint = 'http://172.26.129.91:9101/mastodon_tags/top_10'; // Replace with your first API endpoint
    const otherDataApiEndpoint = 'http://172.26.129.91:9101/twitter_tags/top_10_2'; // Replace with your second API endpoint
    
    //const mastodonTags = tagApiEndpoint.map(item => Object.keys(item)[0]);
    //return mastodonTags
    
    const fetchTagsData = fetch(tagApiEndpoint)
      .then(response => response.json())
      .then(data => {
        const mastodonTags = data.map(item => Object.keys(item)[0]);
        return mastodonTags;
      })
      .catch(error => {
        console.error('Error fetching Mastodon tags data:', error);
        throw error;
      });
    
    const fetchOtherData = fetch(otherDataApiEndpoint)
      .then(response => response.json())
      .then(data => {
        const twitterTags = data.map(item => Object.keys(item)[0]);
        return twitterTags;
      })
      .catch(error => {
        console.error('Error fetching Twitter tags data:', error);
        throw error;
      });

    Promise.all([fetchTagsData, fetchOtherData])
      .then(([mastodonTags, twitterTags]) => {
        const commonTags = mastodonTags.filter(tag => twitterTags.includes(tag));

        this.options.xaxis.categories = commonTags;

        const fetchCommonTagData = fetch(tagApiEndpoint)
          .then(response => response.json())
          .then(data => {
            const tagData = data.filter(item => commonTags.includes(Object.keys(item)[0]));
            const tagCounts = tagData.map(item => Object.values(item)[0]);
            const totalCount = tagCounts.reduce((sum, count) => sum + count, 0);
            const tagPercentages = tagCounts.map(count => ((count / totalCount) * 100).toFixed(2));

            this.series.push({
              name: 'Mastodon Tags',
              data: tagPercentages,
            });
          })
          .catch(error => {
            console.error('Error fetching Mastodon tag data:', error);
            throw error;
          });

        const fetchCommonTwitterTagData = fetch(otherDataApiEndpoint)
          .then(response => response.json())
          .then(data => {
            const tagData = data.filter(item => commonTags.includes(Object.keys(item)[0]));
            const tagCounts = tagData.map(item => Object.values(item)[0]);
            const totalCount = tagCounts.reduce((sum, count) => sum + count, 0);
            const tagPercentages = tagCounts.map(count => ((count / totalCount) * 100).toFixed(2));

            this.series.push({
              name: 'Twitter Tags',
              data: tagPercentages,
            });
          })
          .catch(error => {
            console.error('Error fetching Twitter tag data:', error);
            throw error;
          });

        Promise.all([fetchCommonTagData, fetchCommonTwitterTagData])
          .catch(error => {
            console.error('Error fetching common tag data:', error);
          });
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