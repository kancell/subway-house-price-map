<template>
	<div class="hello">
		<div class="map-contain">
			<div class="map" id="map"></div>
		</div>
	</div>
</template>

<script>
import AMap from "AMap"
import { mapState } from 'vuex'

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
		threeDInit() {
			this.buildingLayer = new AMap.Buildings({zIndex:130,merge:false,sort:false,zooms:[1,20]});
			this.options = 
			{
				hideWithoutStyle: true,
				areas:[{ 
						color1: 'ff99ff00',
						color2: 'ff999900',
						path: [[114.296003,30.617183],[114.295847,30.617175],[114.295707,30.617191],[114.294973,30.617496],[114.294089,30.617872],[114.294125,30.61822],[114.294141,30.61849],[114.294149,30.618773],[114.294168,30.619102],[114.294204,30.619147],[114.294304,30.61918],[ 114.294519,30.619213],[ 114.294777,30.61921],[114.295136,30.61915],[114.296017,30.618833],[114.296374,30.61875],[114.296704,30.618615],[114.296934,30.618489],[114.297234,30.618201],[114.296386,30.617467],[114.296076,30.617205],[114.296003,30.617183]]
				}]
			};
			//此处应有ajax请求，获取{color1：color2：path：}数据，并push入areas，回调mapinit
			this.buildingLayer.setStyle(this.options);
			this.MapInit();

		},
		MapInit () {
			this.map = new AMap.Map("map", {
				mapStyle: "amap://styles/175fa02b044d32dd9242f1349297fe50", 
				resizeEnable: true,
				zoom: 18,
				pitch:50,
				viewMode:'3D',
				layers:[
					new AMap.TileLayer(),
					this.buildingLayer
				]
				//center: [116.405467, 39.907761]
			});

			new AMap.Polygon({
				bubble:true,
				fillOpacity:0.1,
				strokeWeight:1,
				path:this.options.areas[0].path,
				map:this.map
			})
		},
		MarkAdd () {
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
	},
}
</script>

<style scoped>
.hello {
	display: flex;
	flex-direction: column;
	justify-content: center;
}
.map-contain {
	display: flex;
	justify-content: center;
}
.map {
	display: flex;
	height: 800px;
	width: 480px;
}
.bm-view {
  width: 100%;
  height: 300px;
}
</style>
