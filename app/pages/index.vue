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
    ], 15);

    this.$L.tileLayer("https://a.tile.openstreetmap.de/{z}/{x}/{y}.png ", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 22
    }).addTo(this.mapLayer);
  },
  methods: {
    async getUserPosition() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
          this.userLocation = {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
          }

          this.mapLayer.setView([pos.coords.latitude, pos.coords.longitude], 17, {
            animation: true
          })

          this.$L.marker([pos.coords.latitude, pos.coords.longitude], {
            title: "Dein Standort"
          }).addTo(this.mapLayer);
        })
      }
    }
  }
}
</script>
