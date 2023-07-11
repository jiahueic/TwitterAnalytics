<template>
    <main id="analysis1-page">
        <h2>Scenario 1: Happiness vs Income In Australia</h2>
        <graph-component></graph-component>
        <p class="justified-center">
        Based on Figure above, we can see that there is a general positive correlation between the average happiness 
        and the monthly income of citizens in Australia.
        This shows that the higher the monthly income, the higher the average happiness of citizens. 
        However, we can see that at certain intervals of monthly income, the average happiness decreases. 
        This could be due to the fact that the citizens in that income range have an imbalanced work life, hence could be 
        affected by an increase of stress from work causing them to be unhappy.
        </p>
    </main>
  </template>
  
  <script>
  import GraphComponent from '../components/GraphComponent1.vue';
  
  export default {
    components: {
      GraphComponent
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