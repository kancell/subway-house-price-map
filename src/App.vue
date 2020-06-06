<template>
	<div id="app">
		<a-layout id="components-layout-demo-top" class="layout">
			<a-layout-header>
				<div class="logo" />
				<a-menu
					theme="dark"
					mode="horizontal"
					:default-selected-keys="['1']"
					:style="{ lineHeight: '64px' }"
				>
					<a-menu-item key="1">
						<router-link to="/">Map</router-link>
					</a-menu-item>
					<a-menu-item key="2">
						<router-link to="/chart">Chart</router-link>
					</a-menu-item>
					<a-menu-item key="3">
						<router-link to="/about">About</router-link>
					</a-menu-item>
				</a-menu>
			</a-layout-header>
			<a-layout-content style="padding: 0 15px">
				<div :style="{ background: '#fff', padding: '24px', minHeight: '280px' , marginTop:'10px'}">
					<keep-alive include="Map">
						<router-view/>
					</keep-alive>
				</div>
			</a-layout-content>
			<a-layout-footer style="text-align: center">
				Ant Design ©2018 Created by Ant UED
			</a-layout-footer>
		</a-layout>
	</div>
</template>

<style>
#components-layout-demo-top .logo {
	width: 120px;
	height: 31px;
	background: rgba(255, 255, 255, 0.2);
	margin: 16px 24px 16px 0;
	float: left;
}
</style>
