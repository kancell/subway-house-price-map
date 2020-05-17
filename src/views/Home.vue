<template>
  <div class="home">
    <MapInit msg="map"/>
  </div>
</template>

<script>
// @ is an alias to /src
import MapInit from '@/components/MapInit.vue'

export default {
  name: 'Home',
  components: {
    MapInit
  }
}
</script>
