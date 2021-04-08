<template>
<div class="flex max-h-screen overflow-hidden">
  <div class="relative flex-5 flex w-full lg:w-9/12 xl:w-10/12 h-screen">
    <div id="map" class="flex-1"></div>
  </div>

  <div class="flex-5 lg:w-3/12 xl:w-2/12 bg-gray-700 overflow-y-auto p-3">
    <h1 class="md:text-3xl uppercase tracking-widest mb-1">
      <span class="bg-pink-600 text-white font-medium px-1 mr-1">Foodie</span><span class="text-white font-black">fox</span>
    </h1>
    <p class="font-mono text-white mb-6">Discounter Lieferservice</p>

    <form>
      <label for="address" class="block text-white mb-1">Lieferadresse</label>
      <input id="address" type="text" @input="submitAddress" class="w-full border-gray-200 focus:border-blue-500 border focus:border-outline-none rounded-sm p-1 text-gray-900">
    </form>

    <div v-if="marketAddress" class="mt-8">
      <h4 class="flex justify-between text-white font-medium mb-3">
        <span>Ausgewählter Markt</span>
        <span class="flex justify-center items-center bg-blue-600 rounded-full h-5 w-5">
          <span class="font-mono text-white mb-1">x</span>
        </span>
      </h4>

      <ul class="font-mono text-white">
        <li>
          <span>-</span>
          <p class="inline-block">{{ marketAddress }}</p>
        </li>
      </ul>
    </div>

    <markets :marketsList="marketsList" @emitMarket="selectMarket" />
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      map: {},
      redIcon: {},
      goldIcon: {},
      greenIcon: {},
      orangeIcon: {},
      violetIcon: {},
      blueIcon: {},
      marketAddress: '',
      marketsList: [],
      featureGroup: {},
      violetIconOptions: {
        iconUrl: '/marker-icon-2x-violet.png',
        shadowUrl: '/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [15, -27],
        shadowSize: [41, 41]
      },
      redIconOptions: {
        iconUrl: '/marker-icon-2x-red.png',
        shadowUrl: '/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [15, -27],
        shadowSize: [41, 41]
      },
      goldIconOptions: {
        iconUrl: '/marker-icon-2x-gold.png',
        shadowUrl: '/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [15, -27],
        shadowSize: [41, 41]
      },
      greenIconOptions: {
        iconUrl: '/marker-icon-2x-green.png',
        shadowUrl: '/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [15, -27],
        shadowSize: [41, 41]
      },
      blueIconOptions: {
        iconUrl: '/marker-icon-2x-blue.png',
        shadowUrl: '/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [15, -27],
        shadowSize: [41, 41]
      },
      orangeIconOptions: {
        iconUrl: '/marker-icon-2x-orange.png',
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
      }
    }
  },
  mounted() {
    this.initMap()
  },
  methods: {
    initMap() {
      this.map = this.$L.map('map').setView([53.570007, 10.0104954], 14)

      this.tileLayer = this.$L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd'
      })

      this.redIcon = this.$L.icon(this.redIconOptions)
      this.goldIcon = this.$L.icon(this.goldIconOptions)
      this.orangeIcon = this.$L.icon(this.orangeIconOptions)
      this.violetIcon = this.$L.icon(this.violetIconOptions)
      this.greenIcon = this.$L.icon(this.greenIconOptions)
      this.blueIcon = this.$L.icon(this.blueIconOptions)

      this.tileLayer.addTo(this.map)
      this.featureGroup = this.$L.featureGroup().addTo(this.map)

      this.map.whenReady(this.getPosition)
    },
    addMarkers(res) {
      res.forEach((item, i) => {
        let icon = {}

        if (item['discounter'] === 'rewe') {
          icon = this.redIcon
        } else if (item['discounter'] === 'edeka') {
          icon = this.blueIcon
        } else if (item['discounter'] === 'penny') {
          icon = this.orangeIcon
        } else if (item['discounter'] === 'aldi nord') {
          icon = this.violetIcon
        } else if (item['discounter'] === 'lidl') {
          icon = this.goldIcon
        }

        const marker = this.$L.marker([item['coordinates'][0], item['coordinates'][1]], {
          icon: icon
        })

        marker.on('click', (e) => {
          this.selectMarket(item['streetWithNumber'])
          this.map.fitBounds(this.$L.latLngBounds([e.latlng]))
          e.preventDefault
        })

        marker.bindTooltip(item['discounter'].toUpperCase())

        marker.addTo(this.featureGroup)

        if (i === res.length - 1) {
          this.map.fitBounds(this.featureGroup.getBounds())
        }
      })
    },
    selectMarket(marketAddress) {
      this.marketAddress = marketAddress
    },
    submitAddress(e) {
      console.log(e.target.value)
    },
    getPosition() {
      this.$geolocation.getCurrentPosition().then((pos) => {
        const marker = this.$L.marker([pos.coords.latitude, pos.coords.longitude], {
          title: 'Mein Standort',
          icon: this.greenIcon
        })

        marker.addTo(this.featureGroup)

        return pos.coords
      }).then(coords => {
        const url = `${this.$config.apiUrl}/markets/${coords.latitude}/${coords.longitude}`

        this.$axios.$get(url).then(res => {
          this.marketsList = res
          this.addMarkers(res)
        }).catch(err => {
          alert(`axios error ${err.message}`)
        })
      }).catch((err) => {
        alert(`geolocation accepted with error ${err.name}`)
      })
    },
    errorGeolocation(err) {
      alert(`geolocation error ${err.code}, ${err.message}`)
    }
  }
}
</script>
