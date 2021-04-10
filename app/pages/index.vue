<template>
<div class="flex flex-col md:flex-row max-h-screen overflow-hidden">
  <div class="relative flex-none flex flex-wrap md:flex-5 w-full md:w-7/12 lg:w-8/12 xl:w-10/12 h-96 md:h-screen">
    <location v-if="requestLocation" @emitLocation="preCheckInit" :requestLocation="requestLocation" />
    <div id="map" ref="xxx" class="flex-none"></div>
  </div>

  <div class="flex-1 md:flex-5 w-full md:w-5/12 lg:w-4/12 xl:w-2/12 bg-gray-700 overflow-y-auto p-3">
    <h1 class="md:text-3xl uppercase tracking-widest mb-1">
      <span class="bg-pink-600 text-white font-medium px-1 mr-1">Foodie</span><span class="text-white font-black">fox</span>
    </h1>
    <p class="font-mono text-white mb-6">Discounter Lieferservice</p>

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
      hasLocation: false,
      marketAddress: '',
      marketsList: [],
      featureGroup: {},
      requestLocation: true,
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
  methods: {
    preCheckInit(res) {
      if (!this.checkObject(map)) {
        this.requestLocation = false

        this.initMap(res)
      }
    },
    initMap(res) {
      this.map = this.$L.map('map').setView([res['lat'], res['lng']], 18)

      if (this.$refs.xxx.classList.contains('flex-none')) {
        this.$refs.xxx.classList.remove('flex-none')
        this.$refs.xxx.classList.add('flex-1')

        this.$refs.xxx.style.height = `${this.$refs.xxx.clientHeight}px`
        this.$refs.xxx.style.width = `${this.$refs.xxx.clientWidth * 2}px`

        this.$refs.xxx.classList.remove('flex-1')

        this.map.invalidateSize(false)
      }

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

      const marker = this.$L.marker([res['lat'], res['lng']], {
        title: 'Mein Standort',
        icon: this.greenIcon
      })

      marker.addTo(this.featureGroup)

      this.getMarkets(res)
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
    checkObject(obj) {
      return obj && Object.keys(obj).length === 0 && obj.constructor === Object
    },
    getMarkets(coords) {
      const url = `${this.$config.apiUrl}/markets/${coords.lat}/${coords.lng}`

      this.$axios.$get(url).then(res => {
        this.marketsList = res
        this.addMarkers(res)
      }).catch(err => {
        alert(`axios error ${err.message}`)
      })
    }
  }
}
</script>
