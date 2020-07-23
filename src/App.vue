<template>
	<div id="app">
		<div id="route" v-show="false">
			<router-link to="/">Map</router-link>
			<router-link to="/chart">Chart</router-link>
			<router-link to="/about">About</router-link>
		</div>
		<keep-alive include="Map">
			<router-view/>
		</keep-alive>
	</div>
</template>

<style>
#route {
	display: flex;
	z-index: 210;
}
</style>
