<template>
	<view class="page-background">
		<div class="statusBar"></div>
		<div class="box">
			<div class="topBar">
				<div class="content">
					<p class="top-title">Chat History</p>
					<button class="back" @click="jumpToSetting()">
						<img class="vector" src="~@/static/Vector.svg" > 
					</button>
				</div>
			</div>
		</div>
		<div class="box">
			<div class="topBar">
				<div class="search-box">
					<div class="rec">
						<img class="search-icon" src="~@/static/search.svg">
						<input type="text" placeholder="Search" @input="set">
					</div>
				</div>
			</div>
		</div>
		<div v-for="(item, index) in filterList" :key="index" class="single chat">
			<div class="box">
				<div class="singleChat">
					<div class="singleBox">
						<view class="userProfile"><open-data type="userAvatarUrl" v-if="item.id == false"></open-data></view>
						<img class="profile" v-if="item.id == true" src="~@/static/robot.jpg">
						<rich-text :nodes="item.content" class="singleContent"></rich-text>
					</div>
				</div>
			</div>		
		</div>
	</view>
</template>

<script>
	
	export default{
		name:'search-chat',
		data(){
			return {
				chatHistory:[],
				filterList:[],
				openid:""
			}
		},
		mounted() {
			this.set({detail:''});
		},
		onLoad() {
			let self = this;
			uni.getStorage({
			   key: 'openId',
			   success: function(res) {
			    self.openid = res.data;
				console.log(self.openid)
				uni.request({
					url:'http://10.176.161.237:8000/chatbot/chat_history',
					method: 'POST',
					data: {
					      openid: res.data
					     },
					success:(res) => {
						self.chatHistory = res.data.chats;
					}
				});
			   }
			  });
		},
		methods:{
			set(e){
					let value = e.detail.value;
							
					if(!value){
						this.filterList = [];
						return;
					}
							
					let filterArr = [];
						
					this.chatHistory.forEach((item,index)=>{
					if(item.content.includes(value)){
							filterArr.push({"id":item.is_bot, "time":item.timestamp, "content":this.join(this.getSubStr(item.content,value),value)});
						}
					});
					
											
					this.filterList = filterArr;
			},
			join(str,key){
					var reg = new RegExp((`(${key})`), "gm");
					var replace = '<span style="color:#10B221;">$1</span>';
					return str.replace(reg, replace);
			},
			getSubStr(str, tar){
				
				var index = str.lastIndexOf(tar);
				
				
				if(tar.length > 25){
					str = '... ' + tar.substring(0,25) + ' ...';
					return str;
				} else {
					if(str.length > 25){
						if(index<15){
							str= str.substring(0,25)+' ...';
							return str;
						} else {
							if((str.length-index)>15){
								str = '... ' + str.substring(index-10,index+15) + ' ...';
								return str;
							} else {
								str = '... ' + str.substring(index-10, str.length);
								return str;
							}
						}
					} else {
						return str;
					}
				}
			},
			jumpToSetting: function() {
				let pages = getCurrentPages();
				let beforePage = pages[pages.length - 2];
				uni.navigateBack({
				    success: function() {
				        beforePage.onLoad();
				    }
				});
				console.log('jump');
			}
		}
	}
</script>

<style scoped>
	.page-background{
		width: 100vw;
		height: 100vh;
		background: #F4F4F4;
	}
	.statusBar{
		width: 100vw;
		height: 60rpx;
		background: #F4F4F4;
	}
	input[type="text"]{
		font-family: Poppins;
		color: #515151;
		font-size: 39rpx;
		position: inherit;
		left: 95rpx;
		top: 20rpx;
	}
	.box{
		width: 100vw;
	}
	.topBar{
		height: 0;
		padding-bottom: 115rpx;
		position: relative;
	}
	.content{
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		background: #FFD200;
	}
	.top-title{
		position: inherit;
		top: 31rpx;
		left: 230rpx;
		font-family:Poppins;
		font-weight: 600;
		font-size: 45rpx;
		line-height: 60rpx;
		text-align: center;
		color: #373737;
	}
	.back{
		position:inherit;
		left: 25rpx;
		top: 14rpx;
		width: 85rpx;
		height: 85rpx;
		background: #FFFFFF;
		border-radius: 37rpx;
		filter: drop-shadow(0rpx 8rpx 8rpx rgba(0, 0, 0, 0.25));
	}
	.vector{
		width: 32rpx;
		height: 32rpx;
		position: absolute;
		left: 25rpx;
		top: 27rpx;
	}
	.search-box{
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
	}
	.singleBox{
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		border-bottom:3rpx solid rgba(81, 81, 81, 0.4);
	}
	.rec{
		position: inherit;
		width: 693rpx;
		height: 80rpx;
		left: 30rpx;
		top: 20rpx;
		
		background: #FFFFFF;
		border: 1rpx solid rgba(131, 131, 131, 0.4);
		box-sizing: border-box;
		border-radius: 40rpx;
	}
	.search-icon{
		position: inherit;
		width: 45rpx;
		height: 45rpx;
		left: 20rpx;
		top: 18rpx;
	}
	.singleChat{
		height: 0;
		padding-bottom: 155rpx;
		position: relative;
		background: #F4F4F4;
	}
	.profile{
		width: 110rpx;
		height: 110rpx;
		position: inherit;
		left: 20rpx;
		top: 20rpx;
		border-radius: 25rpx;
	}
	.singleContent{
		position: inherit;
		font-family: Poppins;
		font-style: normal;
		font-size: 39rpx;
		left: 160rpx;
		top: 60rpx;
		color: #515151;
	}
	.userProfile{
		width: 110rpx;
		height: 110rpx;
		position: inherit;
		left: 20rpx;
		top: 20rpx;
		border-radius: 25rpx;
		overflow: hidden;
	}
</style>
