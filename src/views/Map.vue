<template>
	<div class="map">
		<MapInit v-bind:DataL="lianjiaData" v-bind:nowSelectAreaSpec="nowSelectAreaSpec" v-bind:nowSelectAreaCenter="nowSelectAreaCenter"/>
		<select :default-value="cities[0]" style="width: 80px" v-model="provinceAdCode" @change="getCity(provinceAdCode)">
			<option v-for="province in provinces" :key="province.adcode" :label="province.name">
				{{ province.adcode }}
			</option>
		</select>
		<select :default-value="cities[0]" style="width: 80px" v-model="cityAdCode" @change="getDistrict">
			<option v-for="city in cities" :key="city.adcode" :label="city.name">
				{{ city.adcode }}
			</option>
		</select>
		<select style="width: 80px" v-model="districtAdCode" @change="getStreet">
			<option v-for="district in districts" :key="district.adcode" :label="district.name">
				{{ district.adcode }}
			</option>
		</select>
		<select  style="width: 100px"  v-model="streetAdCode">
			<option v-for="street in streets" :key="street.name" :label="street.name">
				{{ street.name }}
			</option>
		</select>
		<button @click="onSearch">查询</button>
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
			nowSelectAreaSpec: [],
			nowSelectAreaCenter: {},
			provinceData: [],
			provinces: [],
			cities: [],
			districts :[],
			streets: [],
			provinceAdCode: null,
			cityAdCode: null,
			districtAdCode: null,
			streetAdCode: null
		}
	},
	mounted () {
		//this.dataInit('detailArea', '育才花桥')
		//this.dataInit('area', '江岸')
		this.initSearch()
		this.getProvince()
	},
	computed: {

	},
	methods: {
		dataInit (areaKey, areaValue) {
			this.lianjiaData = []

			for (let spec of data) {			
				for (let specGaode of spec.gaodeInfo) {
					if (specGaode.hasOwnProperty('spec') && specGaode.spec.hasOwnProperty('shape')) {
						let cachePath = {
							path: null,
							area: null,
							center: null,
							id: null,
							name: null,
							price: null,	
						}
						if (areaKey == 'city' && areaValue == '武汉') {
							cachePath.path = this.shapeHandle(specGaode.spec.shape)
							cachePath.area = specGaode.spec.area
							cachePath.center = specGaode.spec.center
							cachePath.id = specGaode.id
							cachePath.name = specGaode.name
							cachePath.price = spec.price
							this.lianjiaData.push(cachePath)					
						}
						else if (spec[areaKey] == areaValue) {
										
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
			}
			this.processed()		
		},
		processed () {
			//去重
			let hash = {}
			this.lianjiaData = this.lianjiaData.reduce((item, next) => { 
				hash[next.name] ? '' : hash[next.name] = true && item.push(next)
				return item 
			}, [])
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
				showbiz:true,
				extensions: 'all'
			};
			this.district = new AMap.DistrictSearch(opts);//注意：需要使用插件同步下发功能才能这样直接使用
		}, 
		getProvince() {
			this.district.search('中国', (status, result) => {
				if(status=='complete'){
					this.provinces = result.districtList[0].districtList
					this.provinces.push({name: '----'})
					this.cityAdCode = null
					this.districtAdCode = null
					this.streetAdCode = null
				}
			});
		},
		getCity() {
			if(this.provinceAdCode == null) {
				return
			}
			this.district.search(this.provinceAdCode, (status, result) => {
				if(status=='complete'){
					this.cities = result.districtList[0].districtList
					this.cities.push({name: '----'})
					this.districtAdCode = null
					this.streetAdCode = null
				}
			});
		},
		getDistrict () {
			if(this.cityAdCode == null) {
				return
			}
			
			this.district.search(this.cityAdCode, (status, result) => {
				if(status == 'complete'){ //			
					this.districts = result.districtList[0].districtList
					this.districts.push({name: '----'})
					this.streetAdCode = null
				}			
			});
		},
		getStreet () {
			if(this.districtAdCode == null) {
				return
			}
			this.district.search(this.districtAdCode, (status, result) => {
				console.log(result)
				if(status == 'complete') {
					this.nowSelectAreaSpec = result.districtList[0].boundaries
					this.nowSelectAreaCenter = result.districtList[0].center
					this.streets = result.districtList[0].districtList
					this.streets.push({name: '----'})
				} 
			})
		},
		onSearch() {
			
			 if (this.streetAdCode != null && this.streetAdCode != '----') {
				this.dataInit('detailArea', this.streetAdCode)
			} else if (this.districtAdCode != null && this.districtAdCode!= '----') {
				this.dataInit('area', this.districtAdCode.replace('区',''))
			} else if (this.cityAdCode != null && this.cityAdCode!= '----' && this.cityAdCode =='武汉市') {
				this.dataInit('city', '武汉')
			} else {
				console.log("数据不足无可奉告")
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
.ant-select {
	margin: 5px;
}
</style>