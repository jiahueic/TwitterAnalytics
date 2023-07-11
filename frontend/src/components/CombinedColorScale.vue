<!-- CombinedColorScale.vue -->
<template>
  <div class="combined-color-scales">
    <div class="color-scale happiness-scale">
      <div class="color-scale__header">
        <div>Happiness</div>
        <div>Decile</div>
      </div>
      <div
        v-for="(color, index) in happinessColors"
        :key="index"
        :style="{ backgroundColor: color }"
        class="color-scale__block"
      ></div>
      <div
        v-for="label in happinessLabels"
        :key="label.value"
        :style="{ top: label.position }"
        class="color-scale__label"
      >
        {{ label.value }}
      </div>
    </div>
    <div class="separator"></div>
    <div class="color-scale income-scale">
      <div class="color-scale__header">
        <div>Income</div>
        <div>Decile</div>
      </div>
      <div
        v-for="(color, index) in incomeColors"
        :key="index"
        :style="{ backgroundColor: color }"
        class="color-scale__block"
      ></div>
      <div
        v-for="label in incomeLabels"
        :key="label.value"
        :style="{ top: label.position }"
        class="color-scale__label income-label"
      >
        {{ label.value }}
      </div>
    </div>
  </div>

</template>

<script>
export default {
  data() {
    return {
      happinessColors: [],
      happinessLabels: [],
      incomeColors: [],
      incomeLabels: [],
      isFilterVisible: true,
    };
  },
  props: {
    happinessDeciles: {
      type: Array,
      required: true,
    },
    incomeDeciles: {
      type: Array,
      required: true,
    },
  },
  created() {
    this.generateHappinessColors();
    this.generateHappinessLabels();
    this.generateIncomeColors(this.minIncome, this.maxIncome);
    this.generateIncomeLabels(this.minIncome, this.maxIncome);
  },
  methods: {
    generateHappinessColors() {
      const colorSteps = 10;
      for (let i = 0; i < colorSteps; i++) {
        const normalizedValue = 1 - (i / (colorSteps - 1));
        const color = `rgba(255, 0, 0, ${normalizedValue})`;
        this.happinessColors.push(color);
      }
    },

    generateHappinessLabels() {
      const happinessDeciles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
      const labelPositions = [
        'calc(90% - 26px)',
        'calc(80% - 18px)', 
        'calc(70% - 9px)',
        'calc(60% - 1px)',
        'calc(50% - -10px)',
        'calc(40% - -23px)',
        'calc(30% - -34px)',
        'calc(20% - -44px)',
        'calc(10% - -54px)',
        'calc(0% - -65px)',
      ];

      for (let i = 0; i < happinessDeciles.length; i++) {
        this.happinessLabels.push({
          value: Math.round(happinessDeciles[i]),
          position: labelPositions[i],
        });
      }
    },

    generateIncomeColors() {
      const colorSteps = 10;
      for (let i = 0; i < colorSteps; i++) {
        const normalizedValue = 1 - (i / (colorSteps - 1));
        const color = `rgba(0, 0, 255, ${normalizedValue})`;
        this.incomeColors.push(color);
      }
    },
    generateIncomeLabels() {
      const incomeDeciles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
      const labelPositions = [
        'calc(90% - 26px)',
        'calc(80% - 18px)', 
        'calc(70% - 9px)',
        'calc(60% - 1px)',
        'calc(50% - -10px)',
        'calc(40% - -23px)',
        'calc(30% - -34px)',
        'calc(20% - -44px)',
        'calc(10% - -54px)',
        'calc(0% - -65px)',
      ];

      for (let i = 0; i < incomeDeciles.length; i++) {
        this.incomeLabels.push({
          value: Math.round(incomeDeciles[i]),
          position: labelPositions[i],
        });
      }
    },

    toggleFilterVisibility() {
    this.isFilterVisible = !this.isFilterVisible;
    },
    },
    };
    </script>

<style scoped>
.combined-color-scales {
  display: flex;
  position: absolute;
  right: 35px;
  top: calc(20px + 3cm);
  z-index: 1;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 30px 5px 30px 6px;
  border-radius: 5px;
}

.color-scale {
  display: inline-block;
}

.color-scale__block {
  width: 30px;
  height: 30px;
}

.color-scale.happiness-scale {
  margin-right: 20x;
}

.color-scale__label {
  position: absolute;
  left: 46px;
  font-size: 16px;
  transform: translateY(75%);
}

.income-label {
  left: 123px;
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


