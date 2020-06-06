<template>
	<div>
		<MapInit v-bind:DataL="lianjiaData"/>
	</div>
</template>

<script>
// @ is an alias to /src
import MapInit from '@/components/MapInit.vue'
import data from '@/assets/小区信息聚合.json'
export default {
	name: 'Map',
	data() {
		return {
			lianjiaData: []
		}
	},
	mounted () {
		this.dataInit('detailArea', '育才花桥')
		//this.dataInit('area', '江岸')
	},
	computed: {

	},
	methods: {
		dataInit (areaKey, areaValue) {
			for (let spec of data) {

				for (let specGaode of spec.gaodeInfo) {
					let cachePath = {
						path: null,
						area: null,
						center: null,
						id: null,
						name: null,
						price: null,	
					}
					
					if (spec[areaKey] == areaValue && specGaode.hasOwnProperty('spec') && specGaode.spec.hasOwnProperty('shape')) {
						cachePath.path = this.shapeHandle(specGaode.spec.shape)
						cachePath.area = specGaode.spec.area
						cachePath.center = specGaode.spec.center
						cachePath.id = specGaode.id
						cachePath.name = specGaode.name
						cachePath.price = spec.price
						this.lianjiaData.push(cachePath)
					}					
				}
			}
		},
		shapeHandle (shape) {
			let cache1 = shape.split(';')
			let cache2 = []
			for(let item of cache1 ){
				cache2.push(item.split(','))
			}
			return cache2
		},
	},
	components: {
		MapInit
	}
}
</script>
