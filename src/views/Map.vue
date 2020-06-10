<template>
	<div class="map">
		<MapInit v-bind:DataL="lianjiaData"/>
		<a-select :default-value="cities[0]" style="width: 100px" v-model="cityName">
			<a-select-option v-for="city in cities" :key="city.name">
				{{ city.name }}
			</a-select-option>
		</a-select>
		<a-select style="width: 100px" @change="getStreet" v-model="districtName">
			<a-select-option v-for="district in districts" :key="district.name">
				{{ district.name }}
			</a-select-option>
		</a-select>
		<a-select  style="width: 190px"  v-model="streetName ">
			<a-select-option v-for="street in streets" :key="street.name">
				{{ street.name }}
			</a-select-option>
		</a-select>
		<a-button type="primary" shape="circle" icon="search" @click="onSearch"/>
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
			lianjiaData: [],
			provinceData: [],
			cities: [],
			districts :[],
			streets: [],
			cityName: null,
			districtName: null,
			streetName: null
		}
	},
	mounted () {
		//this.dataInit('detailArea', '育才花桥')
		//this.dataInit('area', '江岸')
		this.initSearch()
	},
	computed: {

	},
	methods: {
		dataInit (areaKey, areaValue) {
			this.lianjiaData = []
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
		initSearch () {
			let opts = {
				subdistrict: 1,   //返回下一级行政区
				showbiz:true  //最后一级返回街道信息
			};
			this.district = new AMap.DistrictSearch(opts);//注意：需要使用插件同步下发功能才能这样直接使用
			this.getDistrict()
		}, 
		getDistrict (value) {
			this.district.search('武汉', (status, result) => {
				if(status == 'complete' && result.districtList[0]['level'] == 'city'){ //
					for (let info of result.districtList) {
						let c = {
							adcode: info.adcode,
							citycode: info.citycode,
							level: info.level,
							name: info.name,
							center: info.center
						}
						this.cities.push(c)
						if (info.hasOwnProperty('districtList')) {							
							this.districts = info.districtList
						}
					}		
				}			
			});
		},
		getStreet (value) {
			this.streetName = []
			this.district.search(value, (status, result) => {
				if(status == 'complete') {
					this.streets = result.districtList[0].districtList
				} //
			})
		},
		onSearch() {
			if (this.streetName != '') {
				this.dataInit('detailArea', this.streetName)
			} else if (this.districtName != '') {
				this.dataInit('area', this.districtName.replace('区',''))
			}
			//
			//this.dataInit('area', '洪山区')
		},
	},
	components: {
		MapInit
	}
}
</script>
<style scoped>

</style>