<template>
	<view>
		<image src="../static/startPage.png" class="startPage"></image>
		<image src="../static/start.svg" class="startButton" @click="jumpToChat()"></image>
	</view>
</template>

<script>
	export default{
		methods:{
			jumpToChat: function(){
				console.log('jump');
				uni.navigateTo({
					url: './chat',
					success: res => {
						console.log('Jump Setting');
					}
				});
			}
		}
	}
</script>

<style scoped>
.startPage {
	position: fixed;
	top: 0;
	left: 0;
	height: 100vh;
	width: 100vw;
}

.startButton {
	position: absolute;
	top: 60vh;
	left: 30vw;
	height: 300rpx;
	width: 300rpx;
	z-index: 10;
}
</style>
