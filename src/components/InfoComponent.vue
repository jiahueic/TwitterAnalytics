<template>
  <div 
    class="info-window" 
    v-show="showInfo"
    @mousedown="dragStart"
    @mouseup="dragEnd"
    @mousemove="drag"
    :style="{ top: y + 'px', left: x + 'px' }"
  >
    <button class="close-button" @click="$emit('close-info')">x</button>
    <h2>Blended Heatmap Guideline</h2>
    <div class="color-bar">
      <div class="color-section" style="background: red;">More happiness than income</div>
      <div class="color-section" style="background: purple;">Balanced happiness and income</div>
      <div class="color-section" style="background: blue;">More income than happiness</div>
    </div>
    <div class="content-section">
      <div class="info-text">
        <h3>This blended heatmap shows a combination of:</h3>
        <p>Happiness rating heatmap</p>
        <p>Average income heatmap</p>
        <h3>Regions tending to be <span class="red">red</span>:</h3>
        <p>High weight of happiness with low income</p>
        <h3>Regions tending to be <span class="blue">blue</span>:</h3>
        <p>Low weight of happiness with high income</p>
        <h3>Regions tending to be <span class="purple">purple</span>:</h3>
        <p>Balanced weight of happiness and income</p>       
      </div>
      <div class="color-matrix-container">
        <!--combined-color-scale :happiness-deciles="happinessDeciles" :income-deciles="incomeDeciles"></combined-color-scale-->
        <div class="y-axis-label">Happiness</div>
        <div class="color-matrix">
          <div class="row" v-for="i in 10" :key="i">
            <div 
              class="cell" 
              v-for="j in 10" 
              :key="j"
              :style="{
                backgroundColor: getCellColor(i-1, j-1)
              }"
            >
            </div>
          </div>
        </div>
        <div class="x-axis-label">Income</div>
      </div>
    </div>
  </div>
</template>


<script>
//import CombinedColorScale from '@/components/CombinedColorScale.vue';
export default {
  components: {
    //CombinedColorScale,
  },
  data() {
    return {
      dragging: false,
      x: window.innerWidth / 2,
      y: window.innerHeight / 2,
      offsetX: 0,
      offsetY: 0
    }
  },
  props: {
    showInfo: Boolean,
  },
  methods: {
    getCellColor(i, j) {
      // Use the loop variables i and j as weights
      const weightHappiness = i / 9;
      const weightIncome = j / 9;

      // Define your base colors
      const color1 = "rgba(0, 0, 255, 0.9)";
      const color2 = "rgba(255, 0, 0, 0.9)";

      // Extract the color components using regex
      const regex = /rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/;
      const match1 = regex.exec(color1);
      const match2 = regex.exec(color2);

      // Compute the color components by blending color1 and color2 with the weights
      const r = (parseInt(match1[1]) * weightHappiness + parseInt(match2[1]) * weightIncome);
      const g = (parseInt(match1[2]) * weightHappiness + parseInt(match2[2]) * weightIncome);
      const b = (parseInt(match1[3]) * weightHappiness + parseInt(match2[3]) * weightIncome);
      const a = (parseFloat(match1[4]) + parseFloat(match2[4]));

      // Return the color as an RGB string
      return `rgba(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}, ${a})`;
    },

    dragStart(e) {
      this.dragging = true;
      this.offsetX = e.clientX - this.x;
      this.offsetY = e.clientY - this.y;
    },
    dragEnd() {
      this.dragging = false;
    },
    drag(e) {
      if (!this.dragging) return;
      this.x = e.clientX - this.offsetX;
      this.y = e.clientY - this.offsetY;
    },
  }
};
</script>

<style scoped>
.info-window {
  position: absolute;
  width: 60%;
  height: 80%;
  top: 20%;
  left: 30%;
  background-color: #fff;
  padding: 20px;
  overflow: auto;
  z-index: 2;
  box-sizing: border-box;
  display: flex; 
  flex-direction: column; 
  transform: translate(-50%, -50%);
  opacity: 0.95;
}

.close-button {
  position: absolute;
  top: 0;
  right: 0;
  padding: 10px;
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
}

.color-bar {
  display: flex;
  height: 30px;
  margin-bottom: 40px;
}

.color-section {
  flex: 1;
  text-align: center;
  color: white;
}

.content-section {
  display: flex; /* Add flex display to align elements horizontally */
}

.info-text {
  flex: 0.6; /* Takes up remaining space */
  margin-right: 30px;
}

.info-text h3 {
  font-size: 19px; 
}

.info-text p {
  font-size: 17px; 
}

.red {
  color: red;
}

.blue {
  color: blue;
}

.purple {
  color: purple;
}

.color-matrix-container {
  flex: 0.8; /* Controls the size of the matrix area */
  position: relative;
}

.y-axis-label {
  position: absolute;
  left: -15px; 
  top: 60%;
  transform: translateY(-50%) rotate(-90deg);
  transform-origin: left center;
}

.x-axis-label {
  position: absolute;
  right: 51%; 
  bottom: -30px;
  transform: translateX(0%) ;
  transform-origin: right center;
}

.combined-color-scales {
  position: absolute;
  margin-top: -150px; 
  flex: 0.8;
}

.color-matrix {
  display: flex;
  flex-direction: column;
  opacity: 0.8;
}

.row {
  display: flex;
}

.cell {
  width: 40px;
  height: 40px;
}
</style>
