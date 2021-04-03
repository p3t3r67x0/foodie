<template>
<div class="w-full h-screen overflow-hidden flex">
  <div id="map" class="w-full lg:w-9/12 xl:w-10/12 h-screen"></div>

  <div class="w-full h-screen overflow-hidden lg:w-3/12 xl:w-2/12 bg-gray-700 font-sans">
    <div class="px-3 pt-4 pb-3">
      <h1 class="md:text-3xl uppercase tracking-widest mb-1">
        <span class="bg-pink-600 text-white font-medium px-1 mr-1">Foodie</span><span class="text-white font-black">fox</span>
      </h1>
      <p class="font-mono text-white mb-6">Discounter Lieferservice</p>

      <form>
        <label for="address" class="block text-white mb-1">Lieferadresse</label>
        <input id="address" type="text" @input="submitAddress" class="w-full border-gray-200 focus:border-blue-500 border focus:border-outline-none rounded-sm p-1 text-gray-900">
      </form>

      <div v-if="selectedMarket" class="mt-8">
        <h4 class="flex justify-between text-white font-medium mb-3">
          <span>Ausgewählter Markt</span>
          <span class="flex justify-center items-center bg-blue-600 rounded-full h-5 w-5">
            <span class="font-mono text-white mb-1">x</span>
          </span>
        </h4>

        <ul class="font-mono text-white">
          <li>
            <span>-</span>
            <p class="inline-block">{{ selectedMarket }}</p>
          </li>
        </ul>
      </div>

      <div v-if="markets.length > 0 && !selectedMarket" class="mt-8">
        <h3 class="text-white mb-3">
          <span class="font-bold">{{ markets.length }}</span>
          <span class="font-medium">Märkte gefunden</span>
        </h3>

        <ul class="font-mono text-white">
          <li v-for="market in markets" class="mb-1">
            <span>-</span>
            <p @click="selectMarket(market['streetWithNumber'])" class="cursor-pointer inline-block hover:bg-white focus:bg-white er:bg-white hover:text-pink-600 focus:text-pink-600 hover:px-1 focus:px-1">{{ market['streetWithNumber'] }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      map: {},
      redIcon: null,
      featureGroup: {},
      redIconOptions: {
        iconUrl: '/marker-icon-2x-red.png',
        shadowUrl: '/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [15, -27],
        shadowSize: [41, 41]
      },
      geolocationOptions: {
        timeout: 6000,
        enableHighAccuracy: false,
        maximumAge: 0
      },
      selectedMarket: null,
      markets: []
    }
  },
  async mounted() {
    this.featureGroup = L.featureGroup()
    this.redIcon = L.icon(this.redIconOptions)

    await this.initMap()
    await this.getPosition()
  },
  methods: {
    initMap() {
      this.map = L.map('map').setView([53.570007, 10.0104954], 14)
      this.tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd'
      })
      this.tileLayer.addTo(this.map)
    },
    setupMarkers() {
      this.markets.forEach(item => {
        const marker = L.marker([item['coordinates'][0], item['coordinates'][1]], {
          icon: this.redIcon
        })

        marker.on('click', function(e) {
          this.selectMarketByMarker(e, item)
        })

        this.featureGroup.addLayer(marker)
      })

      this.featureGroup.addTo(this.map)
      this.map.fitBounds(this.featureGroup.getBounds())
    },
    selectMarket(market) {
      this.selectedMarket = market
    },
    selectMarketByMarker(e, item) {
      this.selectMarket(item['streetWithNumber'])
    },
    submitAddress(e) {
      console.log(e.target.value)
    },
    async getPosition() {
      await this.$geolocation.getCurrentPosition().then(pos => {
        const url = `${this.$config.apiUrl}/markets/${pos.coords.latitude}/${pos.coords.longitude}`

        const marker = L.marker([pos.coords.latitude, pos.coords.longitude], {
          title: 'Mein Standort'
        })

        this.$axios.$get(url).then(res => {
          this.markets = res
          this.featureGroup.addLayer(marker)
          this.setupMarkers()
        })
      }).catch(err => {
        alert(err.name)
      })
    },
    errorGeolocation(err) {
      alert(`ERROR ${err.code}, ${err.message}`)
    }
  }
}
</script>
