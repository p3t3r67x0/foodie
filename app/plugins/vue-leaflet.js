import Vue from 'vue'
import L from 'leaflet'

const LeafletPlugin = {
  install(Vue, options) {
    // Expose Leaflet
    Vue.prototype.$L = L
  }
}

Vue.use(LeafletPlugin)
