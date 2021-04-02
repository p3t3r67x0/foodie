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
      position: {
        lat: 53.6623,
        lng: 10.6970
      },
      geolocationOptions: {
        timeout: 6000,
        enableHighAccuracy: false,
        maximumAge: 0
      },
      markets: [],
      selectedMarket: null,
      userLocation: {},
      mapLayer: {}
    }
  },
  mounted() {
    this.getUserPosition()

    const tileLayer = this.$L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd'
    })

    this.mapLayer = this.$L.map('map', {
      layers: [tileLayer],
      minZoom: 6
    }).setView([52.520007, 13.404954], 12)
  },
  methods: {
    selectMarket(market) {
      this.selectedMarket = market
    },
    selectMarketByMarker(e, item) {
      this.selectMarket(item['streetWithNumber'])
    },
    submitAddress(e) {
      console.log(e.target.value)
    },
    getUserPosition() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(this.successGeolocation, this.errorGeolocation, this.geolocationOptions)
      } else {
        alert('Bitte GPS und Standort freigeben')
      }
    },
    errorGeolocation(err) {
      console.log(`ERROR(${err.code}): ${err.message}`)
    },
    successGeolocation(pos) {
      this.userLocation = {
        lat: pos.coords.latitude,
        lng: pos.coords.longitude
      }

      this.$axios({
        method: 'GET',
        url: `${this.$config.apiUrl}/markets/${pos.coords.latitude}/${pos.coords.longitude}`,
        validateStatus: () => true
      }).then((res) => {
        if (res.status === 200) {
          const redIcon = new this.$L.Icon({
            iconUrl: '/marker-icon-2x-red.png',
            shadowUrl: '/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            tooltipAnchor: [15, -27],
            shadowSize: [41, 41]
          })

          const marketMarkers = new this.$L.featureGroup()
          this.mapLayer.addLayer(marketMarkers)

          res.data.forEach((item) => {
            const vm = this

            this.$L.marker([item['coordinates'][0], item['coordinates'][1]], {
                icon: redIcon
              })
              .on('click', function(e) {
                vm.selectMarketByMarker(e, item)
              })
              .bindTooltip(`${item['headline']}, ${item['streetWithNumber']}`)
              .addTo(marketMarkers)
          })

          setTimeout(function() {
            this.mapLayer.invalidateSize()
          }, 800)

          this.mapLayer.fitBounds(marketMarkers.getBounds())

          this.markets = res.data
        } else {
          alert('Entschuldigung keine Märkte gefunden')
        }
      })

      this.$L.marker([pos.coords.latitude, pos.coords.longitude], {
        title: 'Mein Standort'
      }).addTo(this.mapLayer)
    }
  }
}
</script>
