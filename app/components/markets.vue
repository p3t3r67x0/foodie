<template>
<div class="mt-8">
  <h3 class="text-white mb-3">
    <span class="font-bold">{{ marketsList.length }}</span>
    <span class="font-medium">Märkte gefunden</span>
  </h3>

  <ul class="font-mono text-white">
    <li v-for="marketItem in marketsList" @click="emitMarket(marketItem['streetWithNumber'])" class="cursor-pointer hover:bg-white focus:bg-white er:bg-white hover:text-pink-600 focus:text-pink-600 hover:px-1 focus:px-1 bg-gray-600 mb-3 p-1">
      <p class="font-bold">{{ marketItem['discounter'].toUpperCase() }}</p>
      <p>{{ marketItem['streetWithNumber'] }}</p>
    </li>
  </ul>
</div>
</template>

<script>
export default {
  props: ['marketsList'],
  methods: {
    emitMarket(market) {
      this.$emit('emitMarket', market)
    }
  }
}
</script>
