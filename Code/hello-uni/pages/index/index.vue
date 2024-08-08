<template>
	<view class="content">
		<image class="logo" src="/static/logo.png"></image>
		<view class="text-area">
			<text class="title">{{title}}</text>
		</view>
		<view class="text-area">
			<text class="title">username: {{username}}</text>
		</view>
		<view class="text-area">
			<text class="title">password: {{password}}</text>
		</view>
		<view class="text-area">
			<text class="title">email: {{email}}</text>
		</view>
		<view class="text-area">
			<text class="title">phone: {{phone}}</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello World!',
				res: '',
				username: '',
				password: '',
				email: '',
				phone: '',
			}
		},
		onLoad() {
			uni.request({
				url: 'http://127.0.0.1:8000/test/',
				data: {
					text: 'uni.request'
				},
				header: {
					'content-type': 'application/json'
				},
				success: (request) => {
					console.log(request.data.users[10]);
					console.log(request.data.users);
					this.res = JSON.parse(request.data.users)
					this.username = this.res[0].pk;
					this.password = this.res[0].fields.password;
					this.email = this.res[0].fields.email;
					this.phone = this.res[0].fields.phone;
				}
			})

		},
		methods: {

		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
