<template>
<form @submit.prevent="checkFormValues" class="flex-1 flex flex-col justify-center items-center bg-gray-500">
  <fieldset class="max-w-xl sm:max-w-2xl w-full bg-custom-300 rounded-lg px-4 pt-8 pb-4">
    <label for="query" class="block text-center text-5xl text-white mb-8">Wohin sollen wir liefern?</label>
    <div class="relative bg-blue-500">
      <input ref="inputAddress" v-model="inputAddress" @keyup="retrieveSuggestions" name="query" type="text" class="w-full text-xl border-gray-100 focus:border-pink-600 border focus:outline-none rounded-sm text-gray-700 p-2"
        placeholder="Elbuferstraße 72 21502 Geesthacht">
      <ul v-if="suggestions.length > 0" class="bg-white absolute top-0 left-0 w-full h-56 overflow-y-auto mt-12">
        <li v-for="suggestion of suggestions" @click="updateInputAddress(suggestion)" class="cursor-pointer hover:bg-blue-500 hover:text-white text-gray-700 p-3">{{ suggestion }}</li>
      </ul>
    </div>
  </fieldset>
</form>
</template>

<script>
export default {
  data() {
    return {
      suggestions: [],
      inputAddress: null,
      tmpQueryString: null
    }
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
    updateInputAddress(s) {
      this.inputAddress = s
      this.lookupAddress(s)
    },
    retrieveSuggestions(e) {
      this.suggestions = []

      const url = `${this.$config.apiUrl}/locations/${e.target.value}`

      this.$axios.$get(url).then(res => {
        this.suggestions = res
      }).catch(err => {
        console.log(err.message)
      })
    }
  }
}
</script>

<style scoped>
.bg-custom-300 {
  background-image: radial-gradient(circle farthest-corner at -2% 1.4%, rgba(255, 15, 15, 1) 0%, rgba(228, 0, 228, 1) 100.7%);
}
</style>
