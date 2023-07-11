<!-- src/components/MapComponent.vue -->
<template>
  <div>
    <button class="info-button" @click="toggleInfo">
      <i class="fas fa-info-circle"></i>
    </button>
    <InfoComponent 
      :showInfo="showInfo" 
      @close-info="closeInfo">
    </InfoComponent>
  </div>
  <div id="app">
    <div class="container">
      <div class="map-container">
        <div class="taskbar-wrapper">
          <div class="taskbar2">
            <select v-model="selectedState" @change="onStateChange">
              <option disabled value="">Please select a state</option>
              <option v-for="state in states" :key="state" :value="state">
                {{ state }}
              </option>
            </select>
            <select v-model="selectedSa3" @change="onSa3Change" :disabled="!selectedState">
              <option disabled value="">Please select a SA3 region</option>
              <option v-for="sa3 in filteredSa3s" :key="sa3.SA3_CODE21" :value="sa3.SA3_CODE21">
                {{ sa3.SA3_NAME21 }}
              </option>
            </select>
            <button @click="showHeatmapFilter = !showHeatmapFilter">
              {{ showHeatmapFilter ? 'Hide' : 'Show' }} Happiness Filter
            </button>
            <button @click="showIncomeFilter = !showIncomeFilter">
              {{ showIncomeFilter ? 'Hide' : 'Show' }} Income Filter
            </button>
            <!-- Add other elements to the taskbar here -->
          </div>
        </div>
        <div class="color-scales"> <!-- Add this wrapper div for color scales -->
          <combined-color-scale></combined-color-scale>
        </div>
        <div id="map" ref="map" class="map"></div>
      </div>
    </div>
  </div>
</template>


<script>
import CombinedColorScale from '@/components/CombinedColorScale.vue';
import zoomData from './zoomData.json';
import InfoComponent from './InfoComponent.vue';
import '@fortawesome/fontawesome-free/css/all.css'

/* global google */
export default {
  components: {
    CombinedColorScale,
    InfoComponent,
  },
  data() {
    return {
      map: null,
      happinessData: {},
      incomeData: {},
      happinessDecile: {},
      currentInfoWindow: null,
      showHeatmapFilter: true,
      showIncomeFilter: true, 
      dataLayer: null,
      selectedState: "",
      states: [],
      sa3s: [],
      selectedSa3: "",
      sa3InfoArray: [],
      decileData: {},
      incomeDeciles: [],
      searchTerm: "",
      showInfo: true,
      error: null,
      sa3InfoArrayRaw: [],
    };
  },
  computed: {
    filteredSa3s() {  // New computed property for the filtered SA3 regions
      if (!this.searchTerm) {
        return this.sa3s;
      }
      const lowerCaseSearchTerm = this.searchTerm.toLowerCase();
      return this.sa3s.filter(sa3 => sa3.SA3_NAME21.toLowerCase().includes(lowerCaseSearchTerm));
    },
  },
  created() {
    this.fetchData();
  },

  async mounted() {
    try {
      await this.loadGoogleMapsScript();
      this.initGoogleMap();
    } catch (error) {
      this.error = error;
      console.error(error);  // Or handle this error differently
    }
  },

  watch: {
    showHeatmapFilter() {
      this.updateMapStyles();
    },
    showIncomeFilter() {
      this.updateMapStyles();
    },
    selectedState(newVal) {
      if (!newVal) {
        this.sa3s = [];
        return;
      }

      // Get the SA3 regions of the selected state
      this.sa3s = this.sa3InfoArray.filter(item => item.STE_NAME21 === newVal).sort((a, b) => a.SA3_NAME21.localeCompare(b.SA3_NAME21));
      this.selectedSa3 = "";  // Reset the selected SA3 region
    },

    selectedSa3() {
      this.zoomToSa3();
      this.updateMapStyles();  // Update map styles to highlight the selected SA3 region
    },
  },


  methods: {
    async fetchData() {
      try {
        const responses = await Promise.all([
          fetch("http://172.26.129.91:9101/happiness_sa3"),
          fetch("/data/monthly-income-data.json"),
          fetch("/data/sa3_info.json"),
        ]);

        const [happinessArray, incomeArray, sa3InfoArrayRaw] = await Promise.all(responses.map(res => res.json()));
        this.sa3InfoArray = sa3InfoArrayRaw.filter(sa3 => 
          !sa3.SA3_NAME21.startsWith("Migratory - Offshore - Shipping") &&
          !sa3.SA3_NAME21.startsWith("No usual address") && 
          sa3.STE_NAME21 !== "Outside Australia"
        );
        this.happinessData = happinessArray.reduce((acc, item) => {
          acc[item.sa3Code] = item.happiness;
          return acc;
        }, {});

        this.happinessDeciles = this.calculateDeciles(Object.values(this.happinessData));

        this.happinessDecile = happinessArray.reduce((acc, item) => {
          acc[item.sa3Code] = this.calculateHappinessDecile(item.happiness);
          return acc;
        }, {});

        this.incomeData = incomeArray.reduce((acc, item) => {  
          acc[item.sa3Code] = item;
          return acc;
        }, {});
        const incomeValues = Object.values(this.incomeData).map(item => item.monthlyIncome);
        const incomeDeciles = this.calculateDeciles(incomeValues);

        this.decileData = incomeArray.reduce((acc, item) => {
          acc[item.sa3Code] = this.calculateIncomeDecile(item.monthlyIncome, incomeDeciles); // Pass incomeDeciles here
          return acc;
        }, {});

        const uniqueStates = [...new Set(this.sa3InfoArray.map(item => item.STE_NAME21))];
        this.states = uniqueStates.sort();

      } catch (error) {
        this.error = error;
      }
    },

    errorCaptured(err) {
      this.error = err;
      return true; 
    },

    colorScaleHappiness(decile) {
      const color = `rgba(255, 0, 0, ${decile / 10})`;
      return color;
    },

    colorScaleIncome(decile) {
      // Calculate the color based on the decile
      const color = `rgba(0, 0, 255, ${decile / 10})`;

      return color;
    },


    calculateDeciles(data) {
      data.sort((a, b) => a - b);
      let deciles = [];
      for (let i = 1; i < 10; i++) {
        deciles.push(data[Math.floor(data.length * i / 10)]);
      }
      return deciles;
    },

    calculateHappinessDecile(value) {
      for (let i = 0; i < this.happinessDeciles.length; i++) {
        if (value < this.happinessDeciles[i]) {
          return i;
        }
      }
      return 9;
    },

    calculateIncomeDecile(value, deciles) { // Add deciles as parameter
      for (let i = 0; i < deciles.length; i++) {
        if (value < deciles[i]) {
          return i;
        }
      }
      return 9;
    },

    onStateChange() {
      if (!this.selectedState) return;
      this.filteredSa3s = this.sa3InfoArray.filter(sa3 => sa3.STE_NAME21 === this.selectedState);
      // Use the Google Maps Geocoding API to get the latitude and longitude of the selected state
      const geocoder = new google.maps.Geocoder();
      geocoder.geocode({ address: this.selectedState, componentRestrictions: { country: 'AU' } }, (results, status) => {
        if (status === 'OK') {
          const location = results[0].geometry.location;
          this.map.setCenter(location);
          this.map.setZoom(6.3);  // You may want to adjust the zoom level
        } else {
          console.error('Geocode was not successful for the following reason: ' + status);
        }
      });
    },

    onSa3Change() {
      if (!this.selectedSa3) return;

      const geocoder = new google.maps.Geocoder();
      const sa3Object = this.sa3s.find(sa3 => sa3.SA3_CODE21 === this.selectedSa3);
      const sa3Name = sa3Object.SA3_NAME21;
      const stateName = sa3Object.STE_NAME21;  // Get the state name
      let geocodeParams = { address: sa3Name + ', ' + stateName }; 

      // Find the zoom level for the selected SA3 region
      const sa3Zoom = zoomData.find(item => item.sa3code === this.selectedSa3);
      let zoom = sa3Zoom ? sa3Zoom.zoom : 9.5;  // Use the pre-calculated zoom level, or a default value

      // Check if the selected SA3 is one of the special cases
      if (["Christmas Island", "Cocos (Keeling) Islands", "Norfolk Island"].includes(sa3Name)) {
        // Don't restrict to Australia
      } else {
        // Restrict to Australia
        geocodeParams.componentRestrictions = { country: 'AU' };
      }

      geocoder.geocode(geocodeParams, (results, status) => {
        if (status === 'OK') {
          const location = results[0].geometry.location;
          this.map.setCenter(location);
          this.map.setZoom(zoom);

          // Get info for the info window
          const sa3Code = this.selectedSa3;
          const stateName = sa3Object.STE_NAME21;
          const incomeValue = this.incomeData[sa3Code]?.monthlyIncome; // Or however you get the income value
          const happiness = this.happinessData[sa3Code]
          const happinessDecile = this.happinessDecile[sa3Code];
          const decileData = this.decileData[sa3Code];

          const contentString = `
            <div id="content">
              <h2>${sa3Name}, ${stateName}</h2>
              <p>SA3 Code: ${sa3Code}</p>
              <p>Income: ${incomeValue}</p>
              <p>Happiness: ${happiness}</p>
              <p>HappinessDecile: ${happinessDecile}</p>
              <p>IncomeDecile: ${decileData}</p>
            </div>
          `;

          if (this.currentInfoWindow) {  // If there's already an open info window
            this.currentInfoWindow.close();  // Close the current info window
          }

          const infowindow = new google.maps.InfoWindow({
            content: contentString,
            position: location,
          });

          infowindow.open(this.map);
          this.currentInfoWindow = infowindow; 
        } else {
          console.error('Geocode was not successful for the following reason: ' + status);
        }
      });
    },



    zoomToSa3() {
      const sa3 = this.sa3s.find(item => item.SA3_CODE21 === this.selectedSa3);
      if (!sa3) return;

      // Find the zoom level for the selected SA3 region
      const sa3Zoom = zoomData.find(item => item.sa3code === this.selectedSa3);
      let zoom = sa3Zoom ? sa3Zoom.zoom : 9.5;  // Use the pre-calculated zoom level, or a default value

      // Use the Google Maps Geocoding API to get the latitude and longitude of the selected SA3 region
      const geocoder = new google.maps.Geocoder();
      geocoder.geocode({ address: sa3.SA3_NAME21 }, (results, status) => {
        if (status === 'OK') {
          const location = results[0].geometry.location;
          this.map.setCenter(location);
          this.map.setZoom(zoom);
        } else {
          console.error('Geocode was not successful for the following reason: ' + status);
        }
      });
    },

    loadGoogleMapsScript() {
      return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.async = true;
        script.defer = true;
        script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyCPzFJ3N0UVDHBHbRaNsx8YxO7EPPp1C_k&libraries=places,geocoding`;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load Google Maps API'));
        document.head.appendChild(script);
      });
    },


    initGoogleMap() {
      const mapOptions = {
        zoom: 10,
        center: { lat: -37.8136, lng: 144.9631 },
        styles: [
          {
            featureType: 'all',
            elementType: 'labels',
            stylers: [{ visibility: 'off' }],
          },
          {
            featureType: 'administrative.locality',
            elementType: 'labels',
            stylers: [{ visibility: 'on' }],
          },
          {
            featureType: 'administrative.neighborhood',
            elementType: 'labels',
            stylers: [{ visibility: 'on' }],
          },
          {
            featureType: 'landscape',
            elementType: 'geometry',
            stylers: [
              { visibility: 'on' },
              { color: '#f0f0f0' }, // Choose the desired background color
            ],
          },
          {
            featureType: 'poi',
            elementType: 'geometry',
            stylers: [{ visibility: 'off' }],
          },
          {
            featureType: 'road',
            elementType: 'geometry',
            stylers: [{ visibility: 'off' }],
          },
          {
            featureType: 'transit',
            elementType: 'geometry',
            stylers: [{ visibility: 'off' }],
          },
        ],
      };
      this.map = new google.maps.Map(this.$refs.map, mapOptions);
      this.addStateBoundaries();
    },

    addStateBoundaries() {
      this.dataLayer = new google.maps.Data();
      this.dataLayer.loadGeoJson("/geojson/sa3.geojson");

      this.updateMapStyles();

      this.dataLayer.setMap(this.map);
      this.dataLayer.addListener('click', (event) => {
        const feature = event.feature;
        const sa3Code = feature.getProperty('SA3_CODE21');
        const cityName = feature.getProperty('SA3_NAME21');
        const stateName = feature.getProperty('STE_NAME21');
        const incomeValue = this.getIncomeValue(feature);
        const happiness = this.getHappinessValue(feature);
        const happinessDecile = this.happinessDecile[sa3Code];
        const decileData = this.decileData[sa3Code];

        const contentString = `
          <div id="content">
            <h2>${cityName}, ${stateName}</h2>
            <p>SA3 Code: ${sa3Code}</p>
            <p>Income: ${incomeValue}</p>
            <p>Happiness: ${happiness}</p>
            <p>HappinessDecile: ${happinessDecile}</p>
            <p>IncomeDecile: ${decileData}</p>
          </div>
        `;

        if (this.currentInfoWindow) {  // If there's already an open info window
          this.currentInfoWindow.close();  // Close the current info window
        }

        const infowindow = new google.maps.InfoWindow({
          content: contentString,
        });

        infowindow.setPosition(event.latLng);
        infowindow.open(this.map);
        this.currentInfoWindow = infowindow; 
      });

    },

    updateMapStyles() {
      if (!this.dataLayer) return;
      this.dataLayer.setStyle((feature) => {
        const sa3Code = feature.getProperty("SA3_CODE21");
        const happinessDecile = this.happinessDecile[sa3Code];
        const incomeDecile = this.decileData[sa3Code];

        let fillColor = 'rgba(0, 0, 0, 0)';

        if (this.showHeatmapFilter && this.showIncomeFilter) {
          const happinessColor = this.colorScaleHappiness(happinessDecile);
          const incomeColor = this.colorScaleIncome(incomeDecile);  // Pass sa3Code instead of decileValue
          fillColor = this.blendColors(happinessColor, incomeColor, happinessDecile, incomeDecile);
        } else if (this.showHeatmapFilter) {
          fillColor = this.colorScaleHappiness(happinessDecile);
        } else if (this.showIncomeFilter) {
          fillColor = this.colorScaleIncome(incomeDecile);  // Pass sa3Code instead of decileValue
        }
        const isSa3Selected = feature.getProperty("SA3_CODE21") === this.selectedSa3;
        const strokeColor = feature.getProperty("SA3_CODE21") === this.selectedSa3 ? "yellow" : "black";
        const strokeWeight = isSa3Selected ? 6.5 : 1.3; 
        return {
          strokeColor,
          strokeWeight,
          fillColor,
          fillOpacity: 0.6,
        };
      });
    },


    blendColors(color1, color2, happinessDecile, incomeDecile) {
      const regex = /rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/;
      const match1 = regex.exec(color1);
      const match2 = regex.exec(color2);
      if (!match1 || !match2) {
        // One of the colors does not match the pattern, return a default color or handle this case accordingly
        return 'rgba(0, 0, 0, 1)';
      }
      // Scale down the deciles to 0-1 range
      const weightHappiness = happinessDecile / 10;
      const weightIncome = incomeDecile / 10;
      

      const r = (parseInt(match1[1]) * weightHappiness + parseInt(match2[1]) * weightIncome);
      const g = (parseInt(match1[2]) * weightHappiness + parseInt(match2[2]) * weightIncome);
      const b = (parseInt(match1[3]) * weightHappiness + parseInt(match2[3]) * weightIncome);
      const a = (parseFloat(match1[4]) + parseFloat(match2[4]));

      return `rgba(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}, ${a})`;
    },


    getHappinessValue(feature) {
      const featureSa3Code = feature.getProperty("SA3_CODE21");
      const happinessValue = this.happinessData[featureSa3Code] || 0;
      // return happinessValue;
      return happinessValue;
    },

    getIncomeValue(feature) {
      const featureSa3Code = feature.getProperty("SA3_CODE21");
      const incomeValue = this.incomeData[featureSa3Code]?.monthlyIncome || 0;
      return incomeValue;
    },

    closeInfo() {
      this.showInfo = false;
    },
    toggleInfo() {
      this.showInfo = !this.showInfo;
    },

  },                                                            
};
</script>

<style>
.container {
  display: flex;
  height: 100vh;
}

.taskbar {
  width: 10%;
  background-color: #f0f0f0; /* Change the background color as needed */
  padding: 20px;
  box-sizing: border-box;
}
.taskbar2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 50px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.taskbar-wrapper {
  position: absolute;
  top: -50px; /* Adjust this value as needed */
  width: 100%;
}

.map-container {
  width: 100%;
  position: relative;
  margin-top: 50px; 
}

.map {
  height: 100%;
  width: 100%;
}

.color-scales {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 1;
}

.info-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #0000ff;
  color: #ffffff;
  padding: 0px; /* Adjust padding as needed */
  background: #f0f0f0;  /* light grey background */
  font-size: 4em; /* Adjust font size as needed */
  cursor: pointer;
  z-index: 3;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);  /* box shadow for 3D effect */
  transition: background-color 0.3s ease;  /* transition for hover effect */
}

.info-button i {
  color: #000; /* color of the icon */
}

</style>

