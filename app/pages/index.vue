<template>
<div class="w-full min-h-screen">
  <div id="map" class="w-full min-h-screen" />
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
      userLocation: {},
      mapLayer: null
    }
  },
  mounted() {
    this.getUserPosition()

    this.mapLayer = this.$L.map('map').setView([
      this.position.lat || this.userLocation.lat,
      this.position.lng || this.userLocation.lng
    ], 14)

    this.$L.tileLayer("https://a.tile.openstreetmap.de/{z}/{x}/{y}.png ", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.mapLayer)
  },
  methods: {
    async getUserPosition() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
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

              const markers = res.data.map(item => {
                return this.$L.marker([item['coordinates'][0], item['coordinates'][1]], {
                  icon: redIcon
                }).bindTooltip(`${item['headline']}, ${item['streetWithNumber']}`)
              })

              const group = this.$L.featureGroup(markers).addTo(this.mapLayer)
              this.mapLayer.fitBounds(group.getBounds())
            } else {
              console.log(res.data)
            }
          })

          this.mapLayer.setView([pos.coords.latitude, pos.coords.longitude], 17, {
            animation: true
          })

          this.$L.marker([pos.coords.latitude, pos.coords.longitude], {
            title: 'Mein Standort'
          }).addTo(this.mapLayer)
        })
      }
    }
  }
}
</script>
