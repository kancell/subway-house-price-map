<template>
	<div>
		<MapInit msg="map"/>
	</div>
</template>

<script>
// @ is an alias to /src
import MapInit from '@/components/MapInit.vue'

export default {
	name: 'Map',
	components: {
		MapInit
	}
}
</script>
