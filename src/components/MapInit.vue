<template>
	<div class="map-contain">
		<div class="insert">
			<div>当前缩放层级： {{this.nowZoom}}</div>
			<input v-model="searchValue" placeholder="输入要查询的地点" style="width: 150px;">
			<button @click="onSearch(searchValue)">查询</button>
		</div>
		<div class="map" id="map"></div>
	</div>
</template>

<script>
import AMap from "AMap"
import { mapState } from 'vuex'
import data from '@/assets/小区信息聚合.json'
//显示范围较大时显示点聚合
export default {
	name: 'MapInit',
	props: {
		DataL: Array
	},
	data() {
		return {
			searchValue: null,
			timer: null,
			nowZoom: 14,
			buildingLayer: null, //小区楼梯色块图形
			options: null, //楼快
			map: null, //地图
			gaodeOutline: null, //范围多边形
			markLayer: null,
			opticalData: null,
			preOpticalData: []
		}
	},
	computed: {
		
	},
	mounted () {		
		this.map = new AMap.Map("map", {
			mapStyle: 'amap://styles/6eec46af7142edd70b942e416b8a76ac', ///"amap://styles/175fa02b044d32dd9242f1349297fe50"
			resizeEnable: true,
			zoom: 14,
			zooms: [4,18],
			viewMode:'3D',
			//showLabel: false,
			showIndoorMap: false,
			layers:[AMap.createDefaultLayer()]//spec
		});	
		this.map.on('complete', ()=> {
			this.opticalPathSet()
			this.diffSignSet()
			
			this.gaodeOutline = new AMap.OverlayGroup();
			this.map.add(this.gaodeOutline);
			this.polygonInit()

			this.markLayer = new AMap.LabelsLayer({
				zooms: [15, 20],
				zIndex: 1000,
				allowCollision: true,
				collision: true,
 				animation: false,  
			});
			this.map.addLayer(this.markLayer);
			this.markAdd()

			this.buildingLayer = new AMap.Buildings({zIndex:17, zooms:[17,20]});
			this.map.addLayer(this.buildingLayer)

			//this.location()
		})		

		this.map.on(['zoomchange', 'dragend'], () => {//,'dragstart'
			this.nowZoom = this.map.getZoom()
			if (this.timer != null) {
				clearTimeout(this.timer)
			}
			this.timer = setTimeout(this.mapReSet, 300)
		})
	},
	watch: {//this与父级上下文绑定，在vue的watch和生命周期函数中，谨慎使用箭头函数
		DataL: function() {
			if (this.markLayer != null) {
				this.markLayer.clear()
				//数据改变时移除信息标记
			}
			if (this.gaodeOutline != undefined || this.gaodeOutline != null) {
				this.gaodeOutline.clearOverlays()
				//数据改变时移除多边形
			}
			this.preOpticalData = []
			this.opticalPathSet()
			this.diffSignSet()

			console.log('数据改变,地图重新加载')

			this.polygonInit()					
			this.markAdd()
			this.threeDInit()
			//this.location()
		}
	},
	methods: {
		mapReSet() {
			if (this.nowZoom < 14) {
				this.gaodeOutline == null ? '' : this.gaodeOutline.hide()
			}
			else if(this.nowZoom >= 14) {
				this.gaodeOutline == null ? '' : this.gaodeOutline.show()
				this.opticalPathSet()
				if (this.diffSignSet()) {
					//楼快图层没什么好移除的,setStyle可以直接改楼快图层样式，但使用自定义楼快样式会造成重绘		
					this.polygonInit()
					this.markAdd()
					this.threeDInit()
				}
			}
		},
		onSearch (value) {
			if (value == '' || value == null) return;
			let geocoder = new AMap.Geocoder({
				city: "027"
			});		
			let marker = new AMap.Marker();
			geocoder.getLocation(value, (status, result) => {
				if (status === 'complete' && result.geocodes.length) {
					console.log(result)
					let lnglat = result.geocodes[0].location
					marker.setPosition(lnglat);
					//this.map.add(marker);
					this.map.setFitView(marker);
				}else{
					console.log('根据地址查询位置失败');
				}
			});
		
		},
		colorSet (price) {
			if (price < 10000) {return '#99CC33'}
			else if (price >= 10000 && price < 20000){return '#FFCC00'}
			else if (price >= 20000 && price < 30000){return '#FF9900'}
			else if (price >= 30000 && price < 40000){return '#FF6666'}
			else if (price >= 40000){return '#CC3333'} 
		},
		opticalPathSet () {	
			const bounds = this.map.getBounds();
			const NorthEast = bounds.getNorthEast();
			const SouthWest = bounds.getSouthWest();
			const SouthEast = [NorthEast.lng, SouthWest.lat];
			const NorthWest = [SouthWest.lng, NorthEast.lat];
			let cache = [[NorthEast.lng, NorthEast.lat], SouthEast, [SouthWest.lng, SouthWest.lat], NorthWest]
			this.path = cache
			
			this.opticalData = []
			for (let i = 0; i < this.DataL.length; i++) {
				//console.log(AMap.GeometryUtil.isPointInRing(this.DataL[i].center, this.path))			
				if (AMap.GeometryUtil.isRingInRing(this.DataL[i].path, this.path) || AMap.GeometryUtil.doesRingRingIntersect(this.DataL[i].path, this.path)) {	
					this.opticalData.push(this.DataL[i])
				}
			}
		},
		diffSignSet () {
			//需要进行检查，检出当前视觉范围内的数据，被移出视觉范围的数据，新加入视觉范围的数据	
			//opticalData: 当前视觉范围内的数据
			this.newAddData = []
			let diffHash = {}
			this.preOpticalData.forEach(element => {
				diffHash[element.id] = ''
			})
			this.opticalData.forEach(element => {
				if (!diffHash.hasOwnProperty(element.id)) {
					this.newAddData.push(element)
				}	
			})

			this.deleteData = {}
			let deleteHash = {}
			this.opticalData.forEach(element => {
				deleteHash[element.id] = ''
			})
			this.preOpticalData.forEach(element => {
				if (!deleteHash.hasOwnProperty(element.id)) {
					this.deleteData[element.id] = ''
				}	
			})

			let diffSign = true
			if (this.opticalData.length == 0 || (this.preOpticalData.length == this.opticalData.length && this.preOpticalData[0].id == this.opticalData[0].id)) {			
				diffSign = false
			}
			this.preOpticalData = this.opticalData
			return diffSign
		},
		threeDInit() {	
			return//重绘实在成问题，体验太差 ,而且无法正常清除
			this.options = {
				hideWithoutStyle: true,//是否隐藏其他的默认楼块
				areas:[]
			};
			for (let [i, spec] of this.opticalData.entries()) {
				let cachePath = {
					color1: this.colorSet(this.opticalData[i].price),
					color2: this.colorSet(this.opticalData[i].price),
					path: []
				}
				cachePath.path = spec.path
				this.options.areas.push(cachePath)			
				
			}
			this.buildingLayer.setStyle(this.options)
		},
		polygonInit () {
			let removeCache = []
			this.gaodeOutline.eachOverlay((overlay, index, collections) => {
				if (this.deleteData.hasOwnProperty(overlay.getExtData().id)) {
					removeCache.push(overlay)
				}
			})				
			this.gaodeOutline.removeOverlays(removeCache)//遍历删除单个多边形有问题，删不干净

			let polygonCache = []	
			for (let i = 0; i < this.newAddData.length; i++) {
				let polygon = new AMap.Polygon({
					strokeColor: this.colorSet(this.newAddData[i].price), // 线条颜色
					fillColor: this.colorSet(this.newAddData[i].price), // 多边形填充颜色
					path:this.newAddData[i].path,
					extData: {id: this.newAddData[i].id}
				})	
				polygonCache.push(polygon)							
			}			
			this.gaodeOutline.addOverlays(polygonCache)
			this.gaodeOutline.setOptions({
				strokeWeight:1,
				strokeColor: "#000"
			});
		},
		markAdd () {
			//这就是海量标记的性能吗，真是有够可笑的呢
			let removeCache = []
			this.markLayer.getAllOverlays().forEach((marker, index, collections) => {
				if (this.deleteData.hasOwnProperty(marker.getExtData().id)) {
					removeCache.push(marker)
				}
			})
			this.markLayer.remove(removeCache)

			let infoMarkers = []
			for (let i = 0; i < this.newAddData.length; i++) {
				let labelMarker = new AMap.LabelMarker({
					name: this.newAddData[i].id,
					position: this.newAddData[i].center,
					zooms: [14, 20],
					opacity: 1,
					zIndex: 16,
					text: {
						content: this.newAddData[i].name + '  均价：' + this.newAddData[i].price,
						direction: 'right',
						offset: [-20, -5],
						style: {
							fontSize: 12,
							fillColor: '#22886f',
							strokeColor: '#fff',
							strokeWidth: 2,
							fold: true,
							padding: '2, 5',
						}
					},
					extData: {id: this.newAddData[i].id}
				});
				infoMarkers.push(labelMarker)	
			}
			this.markLayer.add(infoMarkers)
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
				//2.0的api在抽风，定位不准
				this.map.addControl(geolocation);
				geolocation.getCurrentPosition((status,result) => {
					if(status=='complete'){
						this.onComplete(result)
					}else{
						this.onError(result)
					}
				})
			})
		},
		onComplete(s){},
		onError(s){}
	}
}
</script>

<style scoped>
.map-contain {
	display: flex;
}
.map {
	flex-grow:1;
	height: 90vh;
}
.insert{	
	position: fixed;
	z-index: 20;
}
</style>
