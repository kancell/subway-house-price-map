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
				areas:[]
			};
			let path = { 
					color1: 'ff99ff00',
					color2: 'ff999900',
					path: [[114.296003,30.617183],[114.295847,30.617175],[114.295707,30.617191],[114.294973,30.617496],[114.294089,30.617872],[114.294125,30.61822],[114.294141,30.61849],[114.294149,30.618773],[114.294168,30.619102],[114.294204,30.619147],[114.294304,30.61918],[ 114.294519,30.619213],[ 114.294777,30.61921],[114.295136,30.61915],[114.296017,30.618833],[114.296374,30.61875],[114.296704,30.618615],[114.296934,30.618489],[114.297234,30.618201],[114.296386,30.617467],[114.296076,30.617205],[114.296003,30.617183]]
			}
			let set1 = '114.281781,30.637161;114.281686,30.637584;114.281605,30.638026;114.281617,30.638084;114.281647,30.63814;114.281691,30.638182;114.281767,30.638228;114.285963,30.64043;114.285991,30.640435;114.286017,30.640435;114.286035,30.640424;114.286054,30.640413;114.286225,30.640164;114.286239,30.640134;114.286243,30.640109;114.286241,30.64009;114.286236,30.640071;114.285261,30.638648;114.284809,30.637949;114.284699,30.637739;114.284424,30.637219;114.28416,30.636691;114.283965,30.635996;114.283952,30.635927;114.283936,30.635886;114.283906,30.635869;114.283849,30.635862;114.283094,30.6358;114.282194,30.63567;114.28216,30.635672;114.282132,30.635685;114.2821,30.63571;114.282071,30.635754;114.281781,30.637161'
			let set2 = set1.split(';')
			let set3 = []
			for(let item of set2 ){
				let set4 = item.split(',')
				set3.push(set4)
			}
			let path1 = { 
					color1: 'ff99ff00',
					color2: 'ff999900',
					path: set3
			}	
			this.options.areas.push(path)
			this.options.areas.push(path1)
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
