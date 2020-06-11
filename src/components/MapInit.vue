<template>
	<div class="map-contain">
		<a-input-search placeholder="输入要查询的地点" style="width: 200px; margin-bottom:-40px; z-index: 20;" enter-button @search="onSearch" />
		<div class="map" id="map"></div>
	</div>
</template>

<script>
import AMap from "AMap"
import { mapState } from 'vuex'
import data from '@/assets/小区信息聚合.json'
//还差，按视图小范围加载地图，降低性能压力
//获取当前显示的范围，然后根据显示范围渲染标记
//显示范围较大时显示点聚合
export default {
	name: 'MapInit',
	props: {
		DataL: Array
	},
	data() {
		return {
			buildingLayer: null, //小区楼梯色块图形
			options: null, //楼快
			map: null, //地图
			gaodeOutline: null, //范围多边形
			infoMarkers: null,
			markLayer: null
		}
	},
	watch: {//this与父级上下文绑定，在vue的watch和生命周期函数中，谨慎使用箭头函数
		DataL: function() {
			if (this.gaodeOutline != undefined || this.gaodeOutline != null) {
				console.log(this.gaodeOutline)
				this.map.remove(this.gaodeOutline)
				this.map.remove(this.buildingLayer)
				this.map.remove(this.gaodeOutline)
			}
			//this.map && this.map.destroy();
			console.log('数据改变,地图重新加载')
			this.gaodeOutline = null

			this.polygonInit()
			this.threeDInit()
			//this.location()		
			this.markadd()
			this.map.on('click', function(ev) {
			// 触发事件的对象
				var target = ev.target;		
				// 触发事件的地理坐标，AMap.LngLat 类型
				var lnglat = ev.lnglat;			
				// 触发事件的像素坐标，AMap.Pixel 类型
				var pixel = ev.pixel;			
				// 触发事件类型
				var type = ev.type;
				console.log(target)
			});
		}
	},
	computed: {
		
	},
	mounted () {		
		this.map = new AMap.Map("map", {
			//mapStyle: 'amap://styles/whitesmoke', ///"amap://styles/175fa02b044d32dd9242f1349297fe50"
			resizeEnable: true,
			zoom: 18,
			zooms: [4,18],
			viewMode:'3D',
			showLabel: false,
			showIndoorMap: false,
			layers:[AMap.createDefaultLayer()]//spec
		});	
		this.map.on('complete', ()=> {
			this.opticalPathSet()
			this.markLayer = new AMap.LabelsLayer({
				zooms: [15, 20],
				zIndex: 1000,
				allowCollision: true
			});
			this.buildingLayer = new AMap.Buildings({zIndex:130, zooms:[1,20]});
			this.map.add(this.markLayer);
			//没有初始化gaodeOutline，轮廓图形，其他两个都是图层，多边形不是
			this.map.add(this.buildingLayer)
		})		

		this.$nextTick(() => {
			//this.markadd()
		})
		
		this.map.on(['zoomchange', 'dragend'], () => {
			let zoom = this.map.getZoom()
			if (zoom < 17 && zoom > 14) {
				this.opticalPathSet()
				if (this.gaodeOutline != undefined || this.gaodeOutline != null) {
					this.map.remove(this.gaodeOutline)
					//地图移除多边形
				}
				if (this.infoMarkers != null) {
					this.markLayer.remove(this.infoMarkers)
					//标记图层移除信息标记
				}
				//楼快图层没什么好移除的
				this.polygonInit()
				this.threeDInit()
				this.markadd()
			}
		})
	},
	methods: {
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
			this.path = [[NorthEast.lng, NorthEast.lat], SouthEast, [SouthWest.lng, SouthWest.lat], NorthWest]
		},
		threeDInit() {	
			this.options = {
				hideWithoutStyle: true,//是否隐藏其他的默认楼块
				areas:[]
			};
			for (let [i, spec] of this.DataL.entries()) {
				let cachePath = {
					color1: this.colorSet(this.DataL[i].price),
					color2: this.colorSet(this.DataL[i].price),
					path: []
				}
				let isRingInRing = AMap.GeometryUtil.isRingInRing(spec.path, this.path)
				if (isRingInRing) {
					cachePath.path = spec.path
					this.options.areas.push(cachePath)			
				}
			}
			this.buildingLayer.setStyle(this.options)
			this.map.add(this.buildingLayer)
		},
		polygonInit () {
			let polygonCache = []		
			for (let i = 0; i < this.DataL.length; i++) {				
				let isRingInRing = AMap.GeometryUtil.isRingInRing(this.DataL[i].path, this.path)
				if (isRingInRing) {
					this.polygon = new AMap.Polygon({
						bubble:true,
						strokeWeight:1,
						strokeColor: this.colorSet(this.DataL[i].price), // 线条颜色
						fillColor: this.colorSet(this.DataL[i].price), // 多边形填充颜色
						path:this.DataL[i].path,
						zooms: [14, 20],
					})						
					polygonCache.push(this.polygon)	
				}
			}			
			this.gaodeOutline = new AMap.OverlayGroup(polygonCache);
			this.map.add(this.gaodeOutline);			// 对此覆盖物群组设置同一属性

			this.map.getCity((info) => {
				//console.log(info)
			});	
		},
		bouundSet () {		
			var bounds = this.map.getBounds();//显示范围限制
			this.map.setLimitBounds(bounds);
 			let mybounds = new AMap.Bounds([116.319665, 39.855919], [116.468324,39.9756]);
      		this.map.setBounds(mybounds);
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
		onError(s){},
		markadd () {
					
			this.infoMarkers = []
			// 初始化 labelMarker
			//这就是海量标记的性能吗，真是有够可笑的呢
			for (let i = 0; i < this.DataL.length; i++) {
				let isRingInRing = AMap.GeometryUtil.isRingInRing(this.DataL[i].path, this.path)
				if (isRingInRing) {
					let data = {
						name: this.DataL[i].id,
						position: this.DataL[i].center,
						zooms: [14, 20],
						opacity: 1,
						zIndex: 16,
						text: {
							content: this.DataL[i].name + '  均价：' + this.DataL[i].price,
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
						}
					}
					let labelMarker = new AMap.LabelMarker(data);
					this.infoMarkers.push(labelMarker);
				}
			}
			this.markLayer.add(this.infoMarkers);
		}
	}
}
</script>

<style scoped>
.map-contain {
	display: flex;
	justify-content: center;
	flex-direction: column;
	height: 510px;
}
.map {
	flex-grow:1;
}
</style>
