<template>
<form @submit.prevent="checkFormValues" class="flex-1 flex flex-col justify-center items-center bg-gray-500">
  <fieldset class="max-w-xl sm:max-w-2xl w-full bg-custom-300 rounded-lg px-4 pt-8 pb-4">
    <label for="address" class="block text-center text-5xl text-white mb-8">Wohin sollen wir liefern?</label>
    <input ref="inputAddress" name="address" type="text" class="w-full text-xl border-gray-100 focus:border-pink-600 border focus:outline-none rounded-sm text-gray-700 p-2" placeholder="Elbuferstraße 72 21502 Geesthacht">
  </fieldset>
</form>
</template>

<script>
export default {
  data() {
    return {
      tmpQueryString: null
    }
  },
  mounted() {
    this.$refs.inputAddress.addEventListener('keyup', this.debounce((e) => {
      if (e.keyCode !== 13) {
        this.lookupAddress(e.target.value.trim().toLowerCase())
      }
    }, 800))
  },
  props: ['requestLocation'],
  methods: {
    emitLocation(value) {
      if (this.requestLocation) {
        this.$emit('emitLocation', value)
      }
    },
    checkFormValues(e) {
      if (e.target[1].value.match(/(.+)\s(\d+(\s*[^\d\s]+)*)\s([0-9]{5})\s([a-zA-Z]+)/)) {
        this.lookupAddress(e.target[1].value.trim().toLowerCase())
      }
    },
    lookupAddress(currentQuery) {
      if (this.requestLocation && this.tmpQueryString !== currentQuery) {
        const url = `${this.$config.geoUrl}?q=${currentQuery}&limit=1`

        this.$axios.$get(url).then(res => {
          if (res.length === 1) {
            this.tmpQueryString = currentQuery

            const coords = {
              lat: parseFloat(res[0].lat),
              lng: parseFloat(res[0].lon)
            }

            this.emitLocation(coords)
          }
        }).catch(err => {
          alert(err.message)
        })
      }
    },
    debounce(callback, wait) {
      let timeout

      return (...args) => {
        if (args[0].target.value.match(/(.+)\s(\d+(\s*[^\d\s]+)*)\s([0-9]{5})\s([a-zA-Z]+)/)) {
          clearTimeout(timeout)

          timeout = setTimeout(function() {
            callback.apply(this, args)
          }, wait)
        }
      }
    }
  }
}
</script>

<style scoped>
.bg-custom-300 {
  background-image: radial-gradient(circle farthest-corner at -2% 1.4%, rgba(255, 15, 15, 1) 0%, rgba(228, 0, 228, 1) 100.7%);
}
</style>
