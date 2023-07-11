<template>
    <main id="analysis2-page">
        <h2>Scenario 2: Mental Health Representation vs Happiness</h2>
        <graph-component2></graph-component2>
        <p class="justified-center">
          Based on Figure above, we can see that there is no significant relationship between mental-health presentation 
          occurrence and average sentiment score. This finding was contrary to our initial hypothesis that higher levels of happiness 
          would correlate with fewer mental health presentations. In addition, we could observe that a large portion of the SA3 region 
          seems to cluster around the median value. Similarly, these regions also demonstrated a consistent number of mental health 
          presentations over population ratio. These observations indicate that many SA3 regions share similar levels of overall 
          sentiment score and similar occurrences of mental health presentations.
        </p>
    </main>
  </template>
  
  <script>
  import GraphComponent2 from '../components/GraphComponent2.vue';
  
  export default {
    components: {
      GraphComponent2
    },
  }
  </script>

<style>
.justified-center {
  text-align: justify;
  margin: 0 auto;
  max-width: 1000px; /* Adjust the width as per your requirement */
}
</style>