<template>
	<div class="map-contain">
		<div class="map" id="map"></div>
		<a-input-search placeholder="input search text" style="width: 200px; margin-bottom:2px;" enter-button @search="onSearch" />
	</div>
</template>

<script>
import AMap from "AMap"
import { mapState } from 'vuex'
import data from '@/assets/小区信息聚合.json'

export default {
	name: 'MapInit',
	props: {
		msg: String
	},
	computed: {
		
	},
	mounted () {
		this.threeDInit()
		this.$nextTick(() => {
			this.location()
		})
	},
	data() {
		return {
			buildingLayer: null,
			options: null,
			map: null
		}
	},
	methods: {
		onSearch(){

		},
		threeDInit() {
			this.buildingLayer = new AMap.Buildings({zIndex:130,zooms:[1,20]});
			this.options = {
				hideWithoutStyle: true,
				areas:[]
			};
			for (let spec of data) {
				for (let specGaode of spec.gaodeInfo) {
					let cachePath = {
						color1: 'ff99ff00',
						color2: 'ff999900',
						path: []
					}
					if (specGaode.hasOwnProperty('spec') && specGaode.spec.hasOwnProperty('shape')) {
						let cacheShape = this.shapeHandle(specGaode.spec.shape)
						cachePath.path = cacheShape
						this.options.areas.push(cachePath)
					}
				}
			}

			this.buildingLayer.setStyle(this.options)
			this.MapInit();

		},
		shapeHandle (shape) {
			let cache1 = shape.split(';')
			let cache2 = []
			for(let item of cache1 ){
				cache2.push(item.split(','))
			}
			return cache2
		},
		MapInit () {
			this.map = new AMap.Map("map", {
				mapStyle: "amap://styles/175fa02b044d32dd9242f1349297fe50", 
				resizeEnable: true,
				zoom: 14,
				zooms: [4,18],
				//pitch:50,
				viewMode:'3D',
				layers:[AMap.createDefaultLayer(), this.buildingLayer]
			});
			for (let i = 0; i < this.options.areas.length; i++) {
				new AMap.Polygon({
					bubble:true,
					fillOpacity:0.1,
					strokeWeight:1,
					path:this.options.areas[i].path,
					map:this.map,
				})			
			}
			//this.markadd()

		},
		location() {
			AMap.plugin('AMap.Geolocation', () => {
				let geolocation = new AMap.Geolocation({
					enableHighAccuracy: true,//是否使用高精度定位，默认:true
					timeout: 10000,          //超过10秒后停止定位，默认：5s
					buttonPosition:'RB',    //定位按钮的停靠位置
					buttonOffset: new AMap.Pixel(10, 20),//定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
					zoomToAccuracy: true,   //定位成功后是否自动调整地图视野到定位点
				});

				this.map.addControl(geolocation);
				geolocation.getCurrentPosition((status,result) => {
					if(status=='complete'){
						this.onComplete(result)
					}else{
						this.onError(result)
					}
				});
			});
		},
		onComplete(s){
			console.log(s)
		},
		onError(s){
			console.log(s)
		},
		circleAdd () {
			var circle = new AMap.Circle({
				center: new AMap.LngLat("116.405467", "39.907761"), // 圆心位置
				radius: 1000,  //半径
				strokeColor: "#F33",  //线颜色
				strokeOpacity: 1,  //线透明度
				strokeWeight: 3,  //线粗细度
				fillColor: "#ee2200",  //填充颜色
				fillOpacity: 0.35 //填充透明度
			});
			this.map.add(circle)
		},
		markadd () {
			let text = new AMap.Text({
				text:'最近成交0套<br/>均价19808',
				anchor:'center', // 设置文本标记锚点
				draggable:true,
				cursor:'pointer',
				style:{
					'padding': '0.3rem 0.95rem',
					'margin-bottom': '1rem',
					'border-radius': '0.25rem',
					'background-color': 'white',
					'width': '4rem',
					'border-width': 0,
					'box-shadow': '0 2px 6px 0 rgba(114, 124, 245, .5)',
					'text-align': 'center',
					'font-size': '8px',
					'color': 'blue'
				},
				position: [114.28513,30.653027]
			});

			text.setMap(this.map);
		}
	},
}
</script>

<style scoped>
.map-contain {
	display: flex;
	justify-content: center;
	flex-direction: column;
	height: 600px;
}
.map {
	flex-grow:1;
}
</style>
