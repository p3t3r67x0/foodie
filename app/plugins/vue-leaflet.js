import Vue from 'vue'
import * as Vue2Leaflet from 'vue2-leaflet'

import 'leaflet/dist/leaflet.css'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.imagePath = ''
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

const LeafletPlugin = {
  install(Vue, options) {
    // Expose Leaflet
    Vue.prototype.$L = L;
  }
};

Vue.use(LeafletPlugin)
