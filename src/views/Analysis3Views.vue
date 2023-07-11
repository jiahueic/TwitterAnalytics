<template>
    <main id="analysis3-page">
        <h2>Scenario 3: Mental Health Representation vs Monthly Income</h2>
        <graph-component3></graph-component3>
        <p class="justified-center">
          As shown in Figure above, it reveals a clear negative correlation between average income and mental health 
          presentations. This suggests that as average monthly income increases, the occurrence of mental health presentations tends 
          to decrease. This outcome aligns well with our initial expectations. In most cases, a higher income enables a better standard 
          of living, which could contribute positively to one's overall happiness and mental well-being. Thus, higher income would 
          potentially reduce people's need for mental-health interventions.
        </p>
    </main>
  </template>
  
  <script>
  import GraphComponent3 from '../components/GraphComponent3.vue';
  
  export default {
    components: {
      GraphComponent3
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