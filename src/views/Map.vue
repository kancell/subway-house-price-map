<template>
	<div class="map">
		<MapInit v-bind:DataL="lianjiaData"/>
		<a-select :default-value="cities[0]" style="width: 100px" v-model="provinceName" @focus="getProvince">
			<a-select-option v-for="province in provinces" :key="province.name">
				{{ province.name }}
			</a-select-option>
		</a-select>
		<a-select :default-value="cities[0]" style="width: 100px" v-model="cityName" @focus="getCity">
			<a-select-option v-for="city in cities" :key="city.name">
				{{ city.name }}
			</a-select-option>
		</a-select>
		<a-select style="width: 100px" v-model="districtName" @focus="getDistrict">
			<a-select-option v-for="district in districts" :key="district.name">
				{{ district.name }}
			</a-select-option>
		</a-select>
		<a-select  style="width: 190px"  v-model="streetName " @focus="getStreet">
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
			provinces: [],
			cities: [],
			districts :[],
			streets: [],
			provinceName: null,
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
				showbiz:true  //最后一级返回街道信息
			};
			this.district = new AMap.DistrictSearch();//注意：需要使用插件同步下发功能才能这样直接使用
			//this.district.setExtensions('all');
		}, 
		getProvince() {
			this.district.search('中国', (status, result) => {
				if(status=='complete'){
					this.provinces = result.districtList[0].districtList
					this.provinces.push({name: '----'})
					this.cityName = null
					this.districtName = null
					this.streetName = null
				}
			});
		},
		getCity() {
			if(this.provinceName == null) {
				return
			}
			this.district.search(this.provinceName, (status, result) => {
				if(status=='complete'){
					this.cities = result.districtList[0].districtList
					this.cities.push({name: '----'})
					this.districtName = null
					this.streetName = null
				}
			});
		},
		getDistrict () {
			if(this.cityName == null) {
				return
			}
			this.district.search(this.cityName, (status, result) => {
				if(status == 'complete'){ //			
					this.districts = result.districtList[0].districtList
					this.districts.push({name: '----'})
					this.streetName = null
				}			
			});
		},
		getStreet () {
			if(this.districtName == null) {
				return
			}
			this.district.search(this.districtName, (status, result) => {
				if(status == 'complete') {
					this.streets = result.districtList[0].districtList
					this.streets.push({name: '----'})
				} 
			})
		},
		onSearch() {
			
			 if (this.streetName != null && this.streetName != '----') {
				this.dataInit('detailArea', this.streetName)
			} else if (this.districtName != null && this.districtName!= '----') {
				this.dataInit('area', this.districtName.replace('区',''))
			} else if (this.cityName != null && this.cityName!= '----' && this.cityName =='武汉市') {
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