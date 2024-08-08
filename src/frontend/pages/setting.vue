<template>
	<view class="page-background">
		<view class="status-bar"></view>
		
		<div class="box">
			<div class="topBar">
				<div class="content">
					<p class="top-title">Settings</p>
					<button class="back" @click="jumpToChat()">
						<img class="vector" src="~@/static/Vector.svg">
					</button>
				</div>
			</div>
		</div>
		
		<view class="setting-bar" style="top: 220rpx;">
			<p>Nick Name</p>
		</view>
		<p class="indicate-current" style="top: 242rpx;">{{getSubStr(nickName)}}</p>
		<image class="edit" src="~@/static/Edit.svg" style="top: 240rpx;" @click="editNickName()"></image>
		
		<view class="setting-bar" style="top: 343rpx;">
			<p>Robot Name</p>
		</view>
		<p class="indicate-current" style="top: 365rpx;">{{getSubStr(robotName)}}</p>
		<image class="edit" src="~@/static/Edit.svg" style="top: 363rpx;" @click="editRobotName()"></image>
		
		<view class="setting-bar" style="top: 465rpx;">
			<p>Font Style</p>
		</view>
		<p class="indicate-current" style="top: 487rpx;">{{fontStyle[indexOfFontStyle]}}</p>
		<image class="edit" src="~@/static/Edit.svg" style="top: 486rpx;" @click="editFontStyle()"></image>
		
		<view class="setting-bar" style="top: 587rpx;">
			<p>Font Size</p>
		</view>
		<p class="indicate-current" style="top: 609rpx;">{{fontSize}}</p>
		<image class="edit" src="~@/static/Edit.svg" style="top: 609rpx;" @click="editFontSize()"></image>
		
		<view class="setting-bar" style="top: 712rpx;">
			<p>Font Color</p>
		</view>
		<p class="indicate-current" style="top: 734rpx;">{{fontColor[indexOfFontColor]}}</p>
		<image class="edit" src="~@/static/Edit.svg" style="top: 732rpx;" @click="editFontColor()"></image>
		
		<view class="setting-bar" style="top: 837rpx;">
			<p>BackGround</p>
		</view>
		<image class="background-image" v-bind:src='backGroundImage'></image>
		<image class="edit" src="~@/static/Edit.svg" style="top: 857rpx;" @click="editBackGround()"></image>
		
		<view>
			<button class="search-button" @click="jumpToSearch()">Search chat history</button>
		</view>
		
		<view>
			<button class="delete-button" @click="clearHistory()">Delete chat history</button>
		</view>
		
		<view>
			<p class="developer-button" @click="viewDevelopersInfo()">About Us</p>
		</view>
		
		<view class="shadow" v-show="isShadow">
			
		</view>
		
		<view class="edit-box" v-show="isNickNameBox">
			<p class="edit-title">Nick Name</p>
			<view class="input-background"></view>
			<input class="input-text" type="text" maxlength="15" v-model="nickNameEditing" />
			<button class="cancel-button" @click="closeNickNameBox()">Cancel</button>
			<button class="save-button" @click="confirmNickName()">Save</button>
		</view>
		
		<view class="edit-box" v-show="isRobotNameBox">
			<p class="edit-title">Robot Name</p>
			<view class="input-background"></view>
			<input class="input-text" type="text" maxlength="15" v-model="robotNameEditing" />
			<button class="cancel-button" @click="closeRobotNameBox()">Cancel</button>
			<button class="save-button" @click="confirmRobotName()">Save</button>
		</view>
		
		<view class="edit-box" v-show="isFontStyleBox">
			<p class="edit-title">Font Style</p>
			<view class="input-background" style="border: none; background-color: #dcdcdc;"></view>
			<picker @change="bindFontStyleChange" v-model="indexOfFontStyle" :range="fontStyle">
				<view class="picker">{{fontStyle[indexOfFontStyleEditing]}}</view>
				<image class="down-arrow" src="~@/static/DownArrow.svg" @change="bindFontStyleChange"></image>
			</picker>
			<button class="cancel-button" @click="closeFontStyleBox()">Cancel</button>
			<button class="save-button" @click="confirmFontStyle()">Save</button>
		</view>
		
		<view class="edit-box" v-show="isFontSizeBox">
			<p class="edit-title">Font Size</p>
			<view class="input-background" style="border: none; background-color: #dcdcdc;"></view>
			<image class="minus" src="~@/static/Minus.svg" @click="decreaseFontSizeByOne()"></image>
			<view class="font-size">{{fontSizeEditing}}</view>
			<image class="plus" src="~@/static/Plus.svg" @click="increaseFontSizeByOne()"></image>
			<button class="cancel-button" @click="closeFontSizeBox()">Cancel</button>
			<button class="save-button" @click="confirmFontSize()">Save</button>
		</view>
		
		<view class="edit-box" v-show="isFontColorBox">
			<p class="edit-title">Font Color</p>
			<view class="input-background" style="border: none; background-color: #dcdcdc;"></view>
			<picker @change="bindFontColorChange" v-model="indexOfFontColor" :range="fontColor">
				<view class="picker">{{fontColor[indexOfFontColorEditing]}}</view>
				<image class="down-arrow" src="~@/static/DownArrow.svg" @change="bindFontColorChange"></image>
			</picker>
			<button class="cancel-button" @click="closeFontColorBox()">Cancel</button>
			<button class="save-button" @click="confirmFontColor()">Save</button>
		</view>
		
		<view class="edit-box" v-show="isBackGroundBox">
			<p class="edit-title" style="top: 590rpx;">BackGround</p>
			<view class="bar" style="top: 100rpx;"></view>
			<view class="select-from-album" @click="selectImage()">Select from album</view>
			<image class="right-arrow" src="~@/static/RightArrow.svg" style="top: 133rpx;" @click="selectImage()"></image>
			<view class="bar" style="top: 200rpx;"></view>
			<view class="take-a-photo" @click="takePhoto()">Take a photo</view>
			<image class="right-arrow" src="~@/static/RightArrow.svg" style="top: 230rpx;" @click="takePhoto()"></image>
			<button class="cancel-button" style="top: 870rpx; left: 250rpx;" @click="closeBackGroundBox()">Cancel</button>
		</view>
		
		<view class="edit-box" style="height: 420rpx;" v-show="isDevelopersInfoBox">
			<p class="edit-title" style="top: 590rpx;">Developers:</p>
			<p class="developer" style="top: 100rpx;">Yanbing LUO 20126969</p>
			<p class="developer" style="top: 150rpx;">Qicheng CHEN 20125919</p>
			<p class="developer" style="top: 200rpx;">Sihan LU 20125068</p>
			<p class="developer" style="top: 250rpx;">Longwen HU 20126522</p>
			<p class="developer" style="top: 300rpx;">Zhuopu WANG 20030068</p>
			<p class="developer" style="top: 350rpx;">Chunlong ZHENG 16518748</p>
			<button class="cancel-button" style="top: 988rpx; left: 250rpx;" @click="closeDevelopersInfoBox()">Cancel</button>
		</view>
		
		<view class="edit-box" style="height: 150rpx;" v-show="isChatHistoryDeletedSuccessfullyBox">
			<p class="delete-success-message">Deleted successfully!</p>
			<button class="cancel-button" style="top: 395px; left: 250rpx;" @click="closeChatHistoryDeletedSuccessfullyBox()">OK</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				userOpenId: '',
				isShadow: false,
				isNickNameBox: false,
				isRobotNameBox: false,
				isFontStyleBox: false,
				isFontSizeBox: false,
				isFontColorBox: false,
				isBackGroundBox: false,
				isDevelopersInfoBox: false,
				isChatHistoryDeletedSuccessfullyBox: false,
				nickName: '',
				nickNameEditing: '',
				robotName: '',
				robotNameEditing: '',
				indexOfFontStyle: 0,
				indexOfFontStyleEditing: 0,
				fontStyle: ['Regular','Light','Medium','Bold'],
				fontWeight: [400,100,700,1000],
				fontSize: 16,
				fontSizeEditing: 0,
				indexOfFontColor: 0,
				indexOfFontColorEditing: 0,
				fontColor: ['Black','Red','Green','Blue'],
				backGroundImage: '',
			}
		},
		onLoad() {
			let self = this;
			
			// Get user's open id from local storage
			uni.getStorage({
				key: 'openId',
				success: function(res) {
					console.log('Storage '+ res.data);
					self.userOpenId = res.data;
					
					// Load user's personal configuration from back-end
					uni.request({
						url: 'http://10.176.161.237:8000/chatbot/modify',
						method: 'POST',
						data: {
							openid : self.userOpenId
						},
						header: {
							'content-type': 'application/json'
						},
						success: request => {
							console.log(request.data.data);
							self.nickName = request.data.data.nickname;
							self.robotName = request.data.data.bot_nickname;
							if(request.data.data.font_style == 400) {
								self.indexOfFontStyle = 0;
							} else if(request.data.data.font_style == 100) {
								self.indexOfFontStyle = 1;
							} else if(request.data.data.font_style == 700) {
								self.indexOfFontStyle = 2;
							} else if(request.data.data.font_style == 1000) {
								self.indexOfFontStyle = 3;
							} else {
								self.indexOfFontStyle = 0;
							}
							self.fontSize = request.data.data.font_size;
							if(request.data.data.font_color == 'Black') {
								self.indexOfFontColor = 0;
							} else if(request.data.data.font_color == 'Red') {
								self.indexOfFontColor = 1;
							} else if(request.data.data.font_color == 'Green') {
								self.indexOfFontColor = 2;
							} else if(request.data.data.font_color == 'Blue') {
								self.indexOfFontColor = 3;
							} else {
								self.indexOfFontColor = 0;
							}
							self.backGroundImage = request.data.data.image_path;
						}
					})
				}
			});
		},
		methods: {
			// To avoid clicking on anything other than the edit box
			showShadow: function() {
				this.isShadow = true;
			},
			
			// Edit boxes
			showNickNameBox: function() {
				this.isNickNameBox = true;
			},
			showRobotNameBox: function() {
				this.isRobotNameBox = true;
			},
			showFontStyleBox: function() {
				this.isFontStyleBox = true;
			},
			showFontSizeBox: function() {
				this.isFontSizeBox = true;
			},
			showFontColorBox: function() {
				this.isFontColorBox = true;
			},
			showBackGroundBox: function() {
				this.isBackGroundBox = true;
			},
			showDevelopersInfoBox: function() {
				this.isDevelopersInfoBox = true;
			},
			showChatHistoryDeletedSuccessfullyBox: function() {
				this.isChatHistoryDeletedSuccessfullyBox = true;
			},
			
			// When complete editing edit box, make it avaliable to click other components
			hideShadow: function() {
				this.isShadow = false;
			},
			
			// Close edit boxes
			hideNickNameBox: function() {
				this.isNickNameBox = false;
			},
			hideRobotNameBox: function() {
				this.isRobotNameBox = false;
			},
			hideFontStyleBox: function() {
				this.isFontStyleBox = false;
			},
			hideFontSizeBox: function() {
				this.isFontSizeBox = false;
			},
			hideFontColorBox: function() {
				this.isFontColorBox = false;
			},
			hideBackGroundBox: function() {
				this.isBackGroundBox = false;
			},
			hideDevelopersInfoBox: function() {
				this.isDevelopersInfoBox = false;
			},
			hideChatHistoryDeletedSuccessfullyBox: function() {
				this.isChatHistoryDeletedSuccessfullyBox = false;
			},
			
			// Open edit boxes
			editNickName: function() {
				this.showShadow();
				this.showNickNameBox();
				this.nickNameEditing = this.nickName;
			},
			editRobotName: function() {
				this.showShadow();
				this.showRobotNameBox();
				this.robotNameEditing = this.robotName;
			},
			editFontStyle: function() {
				this.showShadow();
				this.showFontStyleBox();
				this.indexOfFontStyleEditing = this.indexOfFontStyle;
			},
			editFontSize: function() {
				this.showShadow();
				this.showFontSizeBox();
				this.fontSizeEditing = this.fontSize;
			},
			editFontColor: function() {
				this.showShadow();
				this.showFontColorBox();
				this.indexOfFontColorEditing = this.indexOfFontColor;
			},
			editBackGround: function() {
				this.showShadow();
				this.showBackGroundBox();
			},
			
			// Show developers' information
			viewDevelopersInfo: function() {
				this.showShadow();
				this.showDevelopersInfoBox();
			},
			
			// Confirm the change and pass it to back-end database
			confirmNickName: function() {
				this.nickName = this.nickNameEditing;
				
				uni.request({
					url: 'http://10.176.161.237:8000/chatbot/modify',
					method: 'POST',
					data: {
						openid : this.userOpenId,
						nickname : this.nickNameEditing
					},
					header: {
						'content-type': 'application/json'
					},
					success: request => {
						console.log(request.data.text);
					}
				});
				
				this.hideShadow();
				this.hideNickNameBox();
			},
			confirmRobotName: function() {
				this.robotName = this.robotNameEditing;
				
				uni.request({
					url: 'http://10.176.161.237:8000/chatbot/modify',
					method: 'POST',
					data: {
						openid : this.userOpenId,
						bot_nickname : this.robotNameEditing
					},
					header: {
						'content-type': 'application/json'
					},
					success: request => {
						console.log(request.data.text);
					}
				});
				
				this.hideShadow();
				this.hideRobotNameBox();
			},
			confirmFontStyle: function() {
				this.indexOfFontStyle = this.indexOfFontStyleEditing;
				
				uni.request({
					url: 'http://10.176.161.237:8000/chatbot/modify',
					method: 'POST',
					data: {
						openid : this.userOpenId,
						font_style : this.fontWeight[this.indexOfFontStyleEditing]
					},
					header: {
						'content-type': 'application/json'
					},
					success: request => {
						console.log(request.data.text);
					}
				});
				
				this.hideShadow();
				this.hideFontStyleBox();
			},
			confirmFontSize: function() {
				this.fontSize = this.fontSizeEditing;
				
				uni.request({
					url: 'http://10.176.161.237:8000/chatbot/modify',
					method: 'POST',
					data: {
						openid : this.userOpenId,
						font_size : this.fontSizeEditing
					},
					header: {
						'content-type': 'application/json'
					},
					success: request => {
						console.log(request.data.text);
					}
				});
				
				this.hideShadow();
				this.hideFontSizeBox();
			},
			confirmFontColor: function() {
				this.indexOfFontColor = this.indexOfFontColorEditing;
				
				uni.request({
					url: 'http://10.176.161.237:8000/chatbot/modify',
					method: 'POST',
					data: {
						openid : this.userOpenId,
						font_color : this.fontColor[this.indexOfFontColorEditing]
					},
					header: {
						'content-type': 'application/json'
					},
					success: request => {
						console.log(request.data.text);
					}
				});
				
				this.hideShadow();
				this.hideFontColorBox();
			},
			
			// Close edit boxes and hide shadow
			closeNickNameBox: function() {
				this.hideShadow();
				this.hideNickNameBox();
			},
			closeRobotNameBox: function() {
				this.hideShadow();
				this.hideRobotNameBox();
			},
			closeFontStyleBox: function() {
				this.hideShadow();
				this.hideFontStyleBox();
			},
			closeFontSizeBox: function() {
				this.hideShadow();
				this.hideFontSizeBox();
			},
			closeFontColorBox: function() {
				this.hideShadow();
				this.hideFontColorBox();
			},
			closeBackGroundBox: function() {
				this.hideShadow();
				this.hideBackGroundBox();
			},
			closeDevelopersInfoBox: function() {
				this.hideShadow();
				this.hideDevelopersInfoBox();
			},
			closeChatHistoryDeletedSuccessfullyBox: function() {
				this.hideShadow();
				this.hideChatHistoryDeletedSuccessfullyBox();
			},
			
			// Get current editing index of font style
			bindFontStyleChange: function(e) {
				this.indexOfFontStyleEditing = e.target.value;
			},
			
			// Increase current editing font size by one
			increaseFontSizeByOne: function() {
				if(this.fontSizeEditing < 50) {
					this.fontSizeEditing++;
				}
			},
			
			// Decrease current editing font size by one
			decreaseFontSizeByOne: function() {
				if(this.fontSizeEditing > 20) {
					this.fontSizeEditing--;
				}
			},
			
			// Get current editing index of font color
			bindFontColorChange: function(e) {
				this.indexOfFontColorEditing = e.target.value;
			},
			
			// Get first 6 characters if the length of string is greater than 6
			getSubStr: function(str) {
				if(str.length > 6) {
					str = str.substr(0,6) + '...';
				}
				
				return str;
			},
			
			// Select one image from album as background image
			selectImage: function() {
				let self = this;
				uni.chooseImage({
					count: 1,
					sizeType: ['original', 'compressed'],
					sourceType: ['album'],
					success: function (res) {
						console.log(res.tempFilePaths[0]);
						self.backGroundImage = res.tempFilePaths[0];
			      
						uni.request({
							url: 'http://10.176.161.237:8000/chatbot/modify',
							method: 'POST',
							data: {
								openid : self.userOpenId,
								image_path : self.backGroundImage
							},
							header: {
								'content-type': 'application/json'
							},
							success: request => {
								console.log(request.data.text);
							}
						});
					},
				});
				self.closeBackGroundBox();
			},
			   
			// Use default camera to take a photo as background image
			takePhoto: function() {
				let self = this;
				uni.chooseImage({
					count: 1,
					sizeType: ['original', 'compressed'],
					sourceType: ['camera'],
					success: function (res) {
						console.log(res.tempFilePaths[0]);
						self.backGroundImage = res.tempFilePaths[0];
			      
						uni.request({
							url: 'http://10.176.161.237:8000/chatbot/modify',
							method: 'POST',
							data: {
								openid : self.userOpenId,
								image_path : self.backGroundImage
							},
							header: {
								'content-type': 'application/json'
							},
							success: request => {
								console.log(request.data.text);
							}
						});
					},
				});
				self.closeBackGroundBox();
			},
			
			// Jump tp search history page
			jumpToSearch: function() {
				console.log('jump');
				uni.navigateTo({
					url: './searchHistory',
					success: res => {
						console.log('Jump Search Page');
					}
				});
			},
			
			// Jump tp chat page
			jumpToChat: function() {
				 let pages = getCurrentPages();
				 let beforePage = pages[pages.length - 2];
				 uni.navigateBack({
				     success: function() {
				         beforePage.onLoad();
				     }
				 });
				console.log('jump');
			},
			
			// Clear chat history
			clearHistory: function() {
				uni.request({
					url: 'http://10.176.161.237:8000/chatbot/clear_chat',
					method: 'POST',
					data: {
						openid : this.userOpenId,
					},
					header: {
						'content-type': 'application/json'
					},
					success: request => {
						console.log(request.data.text);
						this.showShadow();
						// Prompt that chat history deleted successfully
						this.showChatHistoryDeletedSuccessfullyBox();
					}
				});
			}
		}
	}
</script>

<style>
.status-bar {
	width: 100vw;
	height: 60rpx;
	background-color: #F4F4F4;
}
.page-background {
	width: 100vw;
	height: 100vh;
	background-color: #F4F4F4;
}
.box {
	width: 100vw;
}
.topBar {
	height: 0;
	padding-bottom: 115rpx;
	position: relative;
}
.content {
	position: absolute;
	top: 0;
	bottom: 0;
	left: 0;
	right: 0;
	background: #FFD200;
}
.top-title {
	position: inherit;
	top: 20rpx;
	left: 270rpx;
	font-style: normal;
	font-weight: 600;
	font-size: 50rpx;
	line-height: 70rpx;
	text-align: center;
	color: #373737;
}
.back {
	position:inherit;
	left: 15rpx;
	top: 15rpx;
	width: 90rpx;
	height: 90rpx;
	background: #FFFFFF;
	border-radius: 35rpx;
	filter: drop-shadow(0rpx 4rpx 4rpx rgba(0, 0, 0, 0.25));
}
.vector {
	width: 25rpx;
	height: 35rpx;
	position: absolute;
	left: 32rpx;
	top: 28rpx;
}
.setting-bar {
	position: absolute;
	width: 635rpx;
	height: 40rpx;
	top: 220rpx;
	left: 35rpx;
	padding-left: 25rpx;
	padding-right: 25rpx;
	padding-top: 25rpx;
	padding-bottom: 25rpx;
	font-size: 26rpx;
	font-weight: 1000;
	background-color: #fff;
	box-shadow: 0rpx 15rpx 15rpx rgba(0,0,0,0.1);
	border-radius: 30rpx;
}
.edit {
	position: absolute;
	left: 635rpx;
	width: 50rpx;
	height: 50rpx;
	background: #FFFFFF;
}
.search-button {
	position: absolute;
	left: 150rpx;
	top: 960rpx;
	width: 450rpx;
	height: 115rpx;
	font-size: 37rpx;
	font-weight: 1000;
	padding-top: 10rpx;
	background: #FFFFFF;
	border-radius: 40rpx;
	filter: drop-shadow(0rpx 5rpx 5rpx rgba(0, 0, 0, 0.25));
}
.delete-button {
	position: absolute;
	left: 150rpx;
	top: 1110rpx;
	width: 450rpx;
	height: 115rpx;
	font-size: 37rpx;
	font-weight: 1000;
	padding-top: 10rpx;
	background: #FFD200;
	border-radius: 40rpx;
	filter: drop-shadow(0rpx 5rpx 5rpx rgba(0, 0, 0, 0.25));
}
.shadow {
	position: fixed;
	width: 100vw;
	height: 100vh;
	top: 0;
	background-color: #ABABAB;
	opacity: 0.5;
}
.edit-box {
	position: fixed;
	width: 500rpx;
	height: 300rpx;
	top: 570rpx;
	left: 115rpx;
	background-color: #fff;
	border-radius: 40rpx;
}
.edit-title {
	position: fixed;
	top: 600rpx;
	left: 265rpx;
	font-style: normal;
	font-weight: 600;
	font-size: 35rpx;
	line-height: 70rpx;
	text-align: center;
}
.cancel-button {
	position: fixed;
	left: 115rpx;
	top: 810rpx;
	width: 225rpx;
	height: 100rpx;
	font-size: 37rpx;
	font-weight: 1000;
	padding-top: 5rpx;
	background: #eaeaea;
	border-radius: 40rpx;
	filter: drop-shadow(0rpx 5rpx 5rpx rgba(0, 0, 0, 0.25));
}
.save-button {
	position: fixed;
	left: 390rpx;
	top: 810rpx;
	width: 225rpx;
	height: 100rpx;
	font-size: 37rpx;
	font-weight: 1000;
	padding-top: 5rpx;
	background: #FFD200;
	border-radius: 40rpx;
	filter: drop-shadow(0rpx 5rpx 5rpx rgba(0, 0, 0, 0.25));
}
.input-background {
	position: fixed;
	top: 690rpx;
	left: 220rpx;
	width: 300rpx;
	height: 90rpx;
	background-color: #F4F4F4;
	box-sizing: border-box;
	border: 3rpx solid #CECECE;
	border-radius: 20rpx;
}
.input-text {
	position: fixed;
	top: 690rpx;
	left: 250rpx;
	width: 250rpx;
	height: 90rpx;
}
.picker {
	position: fixed;
	top: 704rpx;
	left: 250rpx;
	font-size: 40rpx;
	width: 250rpx;
	height: 90rpx;
}
.down-arrow {
	top: 143rpx;
	left: 335rpx;
	width: 50rpx;
	height: 50rpx;
	position: absolute;
	background: #dcdcdc;
}
.font-size {
	position: absolute;
	top: 135rpx;
	left: 231rpx;
	font-size: 40rpx;
}
.minus {
	position: absolute;
	top: 138rpx;
	left: 150rpx;
	width: 50rpx;
	height: 50rpx;
	position: absolute;
	background: #dcdcdc;
}
.plus {
	position: absolute;
	top: 138rpx;
	left: 310rpx;
	width: 50rpx;
	height: 50rpx;
	position: absolute;
	background: #dcdcdc;
}
.select-from-album {
	position: absolute;
	font-size: 35rpx;
	top: 125rpx;
	left: 50rpx;
}
.take-a-photo {
	position: absolute;
	font-size: 35rpx;
	top: 223rpx;
	left: 100rpx;
}
.right-arrow {
	left: 400rpx;
	width: 40rpx;
	height: 40rpx;
	position: absolute;
}
.bar {
	position: absolute;
	width: 500rpx;
	height: 4rpx;
	background-color: #828282;
}
.indicate-current {
	position: absolute;
	left: 430rpx;
	color: #999999;
	font-weight: 500;
}
.background-image {
	position: absolute;
	height: 50rpx;
	width: 50rpx;
	top: 856rpx;
	left: 430rpx;
}
.developer {
	position: absolute;
	left: 55rpx;
}
.developer-button {
	position: absolute;
	text-decoration: underline;
	top: 95vh;
	left: 70vw;
}
.delete-success-message {
	position: absolute;
	top: 45rpx;
	left: 40rpx;
	font-size: 40rpx;
	font-weight: 600;
}
</style>