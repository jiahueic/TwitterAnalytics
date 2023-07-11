<template>
  <main id="analysis4-page">
    <h2>Scenario 4: Mental Health Tags in Twitter vs Mastodon</h2>
    <div class="graph-container">
      <graph-component4></graph-component4>
      <graph-component5></graph-component5>
    </div>
    <graph-component6></graph-component6>
    <p class="justified-center">
      Based on the results in Figure above, the common tags regarding Mental Health which are found in both Twitter and Mastodon 
      are health, mentalhealth, depression, anxiety, and psychology. Hence, we can observe that both on Twitter and Mastodon, users 
      have shown a great interest in the topic of Mental Health. The tags such as health, mentalhealth, and psychology could represent 
      an interest in the relationship between a healthy mind and body and how it affects the mental health of a person. Other common 
      tags such as depression and anxiety further reinforce the idea that social media users are interested in understanding mental 
      health. 
      On the other hand, tags that are only found on Mastodon, such as news and covid, could imply that Mastodon users are more 
      interested in the affairs regarding the Covid-19 pandemic. The introduction tag could mean that a percentage of users are 
      interested in learning more about mental health. For Twitter users, tags such as wellbeing, self-care, and mindfulness, show 
      Twitter users focus more on how to maintain or improve their mental health. 
    </p>
  </main>
</template>

<script>
import GraphComponent4 from '../components/GraphComponent4.vue';
import GraphComponent5 from '../components/GraphComponent5.vue';
import GraphComponent6 from '@/components/GraphComponent6.vue';

export default {
  components: {
    GraphComponent4,
    GraphComponent5,
    GraphComponent6,
  },
}
</script>

<style>
.justified-center {
  text-align: justify;
  margin: 0 auto;
  max-width: 1000px; /* Adjust the width as per your requirement */
}

.graph-container {
  display: flex;
}
</style>