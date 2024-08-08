// @author Yanbing Luo
<template>
	<view class="content">
			<image v-bind:src="backgroundUrl" class="backgroundImage" mode="aspectFill"></image>
		<view class="topBar">
			<image class="setting" src="/static/setting.svg" @tap="jumpToSetting()"></image>
			<text class="username">{{ botName }}</text>
		</view>
		<view class="content">
			<view
				v-for="(message, i) in messages"
				:key="i"
				v-bind:class="[{ message: true, userMessage: message.user, robotMessage: message.robot, audioMessage: message.audio }]"
				v-bind:style="{ fontSize: fontSize+'rpx', color: fontColor, fontWeight: fontStyle }"
			>
				<image v-bind:src="speakImagePath" class="speakImage" @click="playRecord(i)" v-show="message.audio"></image>
				<text v-show="!message.audio">{{ message.text }}</text>
				<open-data type="userAvatarUrl" class="headImage userImage" v-show="message.user"></open-data>
				<image src="../static/head.jpg" class="headImage robotImage" v-show="message.robot"></image>
			</view>
		</view>
		<view class="textButtonBar" v-show="!audio">
			<image class="audio" src="/static/audio.svg" @click="changeAudio()"></image>
			<textarea
				class="userText"
				type="text"
				auto-height="true"
				confirm-type="send"
				:show-confirm-bar="A"
				cursor-spacing="15"
				@confirm="sendMessage"
				v-model="userInputText"
				@focus="scrollButtom"
			/>
			<image class="send" src="/static/send.svg" @click="sendMessage()"></image>
		</view>

		<view class="textButtonBar" v-show="audio">
			<image class="audio" src="/static/keyboard.svg" @click="changeAudio"></image>
			<view class="userAudio" @touchstart="startSpeak" @touchend="endSpeak" v-bind:class="audioClass">{{ audioText }}</view>
		</view>
		<view class="main"><map id="map" :longitude="longitude" :latitude="latitude" :scale="scale" :markers="markers" @markertap="tap" show-location v-if="mapShow"></map></view>
	</view>
</template>

<script>
const recorderManager = uni.getRecorderManager();
const innerAudioContext = uni.createInnerAudioContext();
innerAudioContext.autoplay = true;

export default {
	data() {
		return {
			title: 'Hello',
			userInputText: '',
			audio: false,
			audioText: 'Hold Down to Talk',
			audioClass: 'normalClass',
			messages: [],
			speakImagePath: '../static/speak0.png',
			code: '',
			username: '',
			openId: '',
			avatarUrl: '',
			backgroundUrl: '/static/background.jpg',
			fontSize: '',
			fontColor: '',
			fontStyle: '',
			botName: 'Loading ...',
			nickName: '',
			askEmail: false,
			askOfficeHour: false,
			askOffice: false,
			askResearchArea: false,
			askClubInfo: false,
			askTimeTable: false,
			latitude: '',
			longitude: '',
			scale: 18,
			mapShow: false,
			mapID: 0,
			mapInfo: ['PB\nFull named as The Portland Building.\nGenerally used for small class teaching.\nHub is located at Portland Building 120, which is a one-stop service venue where students can access the university services ranging from general enquiries, card service, stamp service, document collection and submissions, and official documentation as well as other specialised services offered by central departments such as Academic Services Office, Finance Office, and Global Engagement Office.', 'TB\nFull named as Teaching Building.\nGenerally used for small class teaching.', 'The Si Yuan Auditorium\nA large lecture theatre used for speech, public lectures, and examinations.\nIn September 2008, the University Auditorium was named ‘Si Yuan Auditorium’ to mark Dr Chen Tseng Tao’s contribution to the University of Nottingham Ningbo China.', 'Gym\nOur gym has been equipped with new Life Fitness Insignia series weight machines since 2019 and their Elevation series of cardio machines including 14 treadmills, 5 upright bikes, 2 recumbent bikes, 7 Elliptical cross-trainers, four Concept 2 rowing machines and a Stairmaster.\nStudents can play basketball, rock climbing, squash, badminton and many other sports in the gym', 'Library\nOpened from 8am to 22pm, from Monday to Sunday.\nThe Library is an innovative department of knowledge acquisition, assessment, dissemination, creation and preservation.\nCall us on +86 574 88180000 (ext. 8152), or follow us on WeChat (ID: UNNC_Library)', 'PMB\nFull named as The Sir Peter Mans‑eld Building.\nA teaching location for science and engineering students, including laboratories and computer rooms.', 'Trent Building\nThe University of Nottingham Ningbo China has its own version of The University of Nottingham\'s iconic Trent Building, complete with clock tower. We would like to pay tribute to Lord Trent, by renaming our landmark building in his honour.', 'Residences\nContains a series of residential buildings for students. Dozens of shops and restaurants have moved in.', 'DB\nThe New Teaching Building was named in honour of Lord Dearing, the former Chief Executive of the UK Post Office and 5th Chancellor of the University of Nottingham.\nIt is usually used in open classes and Chinese culture classes.'],
			markers: [
				{
					id: 1,
					latitude: 29.800329208374023,
					longitude: 121.56319427490234,
					iconPath: '/static/pb.png',
					width: 40,
					height: 40
				},
				{
					id: 2,
					latitude: 29.80023956298828,
					longitude: 121.56221771240234,
					iconPath: '/static/tb.png',
					width: 40,
					height: 40
				},
				{
					id: 3,
					latitude: 29.800182342529297,
					longitude: 121.56283569335938,
					iconPath: '/static/audi.png',
					width: 70,
					height: 40
				},
				{
					id: 4,
					latitude: 29.797548294067383,
					longitude: 121.56343078613281,
					iconPath: '/static/gym.png',
					width: 40,
					height: 40
				},
				{
					id: 5,
					latitude: 29.801151275634766,
					longitude: 121.56379699707031,
					iconPath: '/static/lib.png',
					width: 60,
					height: 40
				},
				{
					id: 6,
					latitude: 29.800092697143555,
					longitude: 121.56123352050781,
					iconPath: '/static/pmb.png',
					width: 40,
					height: 40
				},
				{
					id: 7,
					latitude: 29.802520751953125,
					longitude: 121.56212615966797,
					iconPath: '/static/trent.png',
					width: 50,
					height: 40
				},
				{
					id: 8,
					latitude: 29.797922134399414,
					longitude: 121.5646743774414,
					iconPath: '/static/rsd.png',
					width: 70,
					height: 40
				},
				{
					id: 9,
					latitude: 29.799076080322266,
					longitude: 121.56095123291016,
					iconPath: '/static/db.png',
					width: 40,
					height: 40
				}
			]
		};
	},

	// Execute this function when loading this page
	// Let the user log in this mini app and send the unique code to back-end
	// Initialize the recorderManager, used to implement the record function
	onLoad() {
		let self = this;
		let code = '';
		self.messages = [];
		uni.login({
			provider: 'weixin',
			success: function(loginRes) {
				code = loginRes.code;
				uni.request({
					url: 'http://10.176.161.237:8000/chatbot/login',
					method: 'POST',
					data: {
						code: loginRes.code
					},
					header: {
						'content-type': 'application/json'
					},
					success: request => {
						uni.setStorage({
							key: 'openId',
							data: request.data.data.openid
						});
						self.nickName = request.data.data.nickname;
						self.botName = request.data.data.bot_nickname;
						self.fontSize = request.data.data.font_size;
						self.fontColor = request.data.data.font_color;
						self.fontStyle = request.data.data.font_style;
						self.openId = request.data.data.openid;
						self.backgroundUrl = request.data.data.image_path;

						uni.request({
							url: 'http://10.176.161.237:8000/chatbot/chat_history',
							method: 'POST',
							data: {
								openid: self.openId
							},
							success: res => {
								let chats = res.data.chats;
								for (var i = 0; i < chats.length; i++) {
									self.messages.push({ audio: chats[i].is_audio, user: !chats[i].is_bot, robot: chats[i].is_bot, text: chats[i].content });
								};
								self.messages.push({ audio: false, user: false, robot: true, text: 'Hello, '+ self.nickName });

								self.$nextTick(function() {
									uni.pageScrollTo({
										scrollTop: 2000000,
										duration: 0 //app端这个必须设置成0
									});
								});
							}
						});
					}
				});
			}
		});

		wx.getSetting({
			success(res) {
				if (!res.authSetting['scope.scope.userLocation']) {
					wx.authorize({
						scope: 'scope.scope.userLocation',
						success() {}
					});
				}
			}
		});
		wx.getLocation({
			type: 'gcj02',
			isHighAccuracy: true,
			success: function(res) {
				self.latitude = res.latitude;
				self.longitude = res.longitude;
				console.log(res.latitude);
				console.log(res.longitude);
			}
		});

		recorderManager.onStop(function(res) {
			self.messages.push({ audio: true, user: true, robot: false, text: res.tempFilePath });
			uni.uploadFile({
				url: 'http://10.176.161.237:8000/chatbot/audio2text',
				filePath: res.tempFilePath,
				name: 'audio',
				success: uploadFileRes => {
					self.getNLPResponse(JSON.parse(uploadFileRes.data).response, self.openId);
				}
			});
			self.saveChat(res.tempFilePath, true, false, self.openId);
			self.$nextTick(function() {
				uni.pageScrollTo({
					scrollTop: 2000000,
					duration: 0 //app端这个必须设置成0
				});
			});
		});
	},
	methods: {
		tap(e) {
			this.mapShow = false;
			console.log(e.detail.markerId);
			this.mapID = e.detail.markerId;
			let text = this.mapInfo[this.mapID - 1];
			this.messages.push({ audio: false, user: false, robot: true, text: text });
			this.saveChat(text, false, true, this.openId);
			this.$nextTick(function() {
				uni.pageScrollTo({
					scrollTop: 2000000,
					duration: 0 //app端这个必须设置成0
				});
			});
		},
		// Jump to the setting page
		jumpToSetting: function() {
			console.log('jump');
			uni.navigateTo({
				url: './setting',
				success: res => {
					console.log('Jump Setting');
				}
			});
		},

		// Using this function to send a message and save this message to the back-end
		// Then get the response from back-end and put it on the page
		sendMessage: function() {
			if (this.userInputText == '' || this.userInputText.split(' ').join('').length == 0) {
				this.userInputText = '';
				return;
			}
			var that = this;
			this.messages.push({ audio: false, user: true, robot: false, text: this.userInputText });
			this.saveChat(this.userInputText, false, false, this.openId);
			if (this.askEmail) {
				this.askEmail = false;
				this.getDatabaseResponse('teacher', this.userInputText, 'email');
			} else if (this.askOfficeHour) {
				this.askOfficeHour = false;
				this.getDatabaseResponse('teacher', this.userInputText, 'office hour');
			} else if (this.askOffice) {
				this.askOffice = false;
				this.getDatabaseResponse('teacher', this.userInputText, 'office');
			} else if (this.askResearchArea) {
				this.askResearchArea = false;
				this.getDatabaseResponse('teacher', this.userInputText, 'research area');
			} else if (this.askClubInfo) {
				this.askClubInfo = false;
				this.getDatabaseResponse('club', this.userInputText, 'club');
			} else if (this.askTimeTable) {
				this.askTimeTable = false;
				this.getDatabaseResponse('course', this.userInputText, 'timetable');
			} else {
				this.isDatabase(this.userInputText);
			}
			this.userInputText = '';
			this.$nextTick(function() {
				uni.pageScrollTo({
					scrollTop: 2000000,
					duration: 0 //app端这个必须设置成0
				});
			});
		},

		// Check whether a message from user can be matched to a specfic database
		isDatabase: function(message) {
			let content = '';
			if (message.match(new RegExp('email', 'im')) != null) {
				content = "Which teacher's email do you want to ask?";
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.askEmail = true;
				this.saveChat(content, false, true, this.openId);
				console.log('email');
			} else if (
				message.match(new RegExp('timetable', 'im')) != null ||
				message.match(new RegExp('course', 'im')) != null ||
				message.match(new RegExp('class', 'im')) != null
			) {
				content = 'What is your student ID?';
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.askTimeTable = true;
				this.saveChat(content, false, true, this.openId);
				console.log('Timetable');
			} else if (message.match(new RegExp('office hour', 'im')) != null) {
				content = "Which teacher's office hour do you want to ask?";
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.askOfficeHour = true;
				this.saveChat(content, false, true, this.openId);
				console.log('office hour');
			} else if (message.match(new RegExp('office', 'im')) != null) {
				content = "Which teacher's office do you want to ask?";
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.askOffice = true;
				this.saveChat(content, false, true, this.openId);
				console.log('office');
			} else if (message.match(new RegExp('research area', 'im')) != null) {
				content = "Which teacher's research area do you want to ask?";
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.askResearchArea = true;
				this.saveChat(content, false, true, this.openId);
				console.log('research area');
			} else if (message.match(new RegExp('club', 'im')) != null) {
				content = 'Which club information do you want to ask?';
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.askClubInfo = true;
				this.saveChat(content, false, true, this.openId);
				console.log('club information');
			} else if (message.match(new RegExp('UNNC', 'im')) != null && message.match(new RegExp('website', 'im')) != null) {
				content = 'The website of UNNC is https://www.nottingham.edu.cn/en/';
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.saveChat(content, false, true, this.openId);
				console.log('UNNC website');
			} else if (message.match(new RegExp('UNNC', 'im')) != null && message.match(new RegExp('address', 'im')) != null) {
				content = 'The address of UNNC is 199 Taikang East Road Ningbo, 315100, China';
				this.messages.push({ audio: false, user: false, robot: true, text: content });
				this.saveChat(content, false, true, this.openId);
				console.log('UNNC address');
			} else if (message.match(new RegExp('map', 'im')) != null) {
				this.mapShow = true;
			} else {
				this.getNLPResponse(this.userInputText, this.openId);
			}
		},

		// Scroll the page to the bottom
		scrollButtom: function() {
			this.$nextTick(function() {
				uni.pageScrollTo({
					scrollTop: 2000000,
					duration: 0 //app端这个必须设置成0
				});
			});
		},

		// Change the input box between speaking audio state and typing text state
		changeAudio: function() {
			this.audio = !this.audio;
			console.log(this.audio);
		},

		// Start to record user's speaking audio
		startSpeak: function() {
			uni.vibrateShort({
				success: () => {
					console.log('vibrate');
				}
			});
			this.audioText = 'Release to Send';
			this.audioClass = 'speakClass';
			recorderManager.start({
				sampleRate: 16000,
				format: 'wav'
			});
			console.log('Start Record');
		},

		// Stop recording user's speaking audio
		endSpeak: function() {
			this.audioText = 'Hold Down to Talk';
			this.audioClass = 'normalClass';
			recorderManager.stop();
			console.log('End Record');

			this.$nextTick(function() {
				uni.pageScrollTo({
					scrollTop: 2000000,
					duration: 0 //app端这个必须设置成0
				});
			});
		},

		// Play an audio
		playRecord: function(index) {
			console.log('Play Record');
			console.log(this.messages[index].text);
			if (this.messages[index].text) {
				innerAudioContext.src = this.messages[index].text;
				innerAudioContext.play();
			}
			this.speakImagePath = '../static/speak0.png';
		},

		saveChat: function(content, is_audio, is_bot, openid) {
			uni.request({
				url: 'http://10.176.161.237:8000/chatbot/save_chat',
				method: 'POST',
				data: {
					content: content,
					is_audio: is_audio,
					is_bot: is_bot,
					openid: openid
				},
				header: {
					'content-type': 'application/json'
				},
				success: request => {
					console.log(request.data);
				}
			});
		},

		getNLPResponse: function(userInputText, openId) {
			uni.request({
				url: 'http://10.176.161.237:8000/chatbot/get_response',
				method: 'POST',
				data: {
					text: userInputText,
					openid: openId
				},
				header: {
					'content-type': 'application/json'
				},
				success: request => {
					console.log(request.data.text);
					this.messages.push({ audio: false, user: false, robot: true, text: request.data.text });
					this.$nextTick(function() {
						uni.pageScrollTo({
							scrollTop: 2000000,
							duration: 0 //app端这个必须设置成0
						});
					});
				}
			});
		},

		getDatabaseResponse: function(type, userInputText, keyword) {
			uni.request({
				url: 'http://10.176.161.237:8000/chatbot/database',
				method: 'GET',
				data: {
					type: type,
					id: userInputText
				},
				header: {
					'content-type': 'application/json'
				},
				success: request => {
					let text = '';
					console.log(request.data);
					if (request.data.code == 1) {
						text = 'Sorry, I cannot find information you need.';
					} else if (keyword == 'email') {
						text = request.data.retlist[0].email;
					} else if (keyword == 'office hour') {
						text = request.data.retlist[0].office_hour;
					} else if (keyword == 'office') {
						text = request.data.retlist[0].office;
					} else if (keyword == 'research area') {
						text = request.data.retlist[0].research_area;
					} else if (keyword == 'club') {
						// TODO
					} else if (keyword == 'timetable') {
						let courseList = request.data.retlist;
						if (courseList.length == undefined) {
							text = 'Today you do not have any class';
							this.messages.push({ audio: false, user: false, robot: true, text: text });
							this.saveChat(text, false, true, this.openId);
							text = '';
							return;
						}
						text = 'Today you have ' + courseList.length + ' class\n';
						for (var i = 0; i < courseList.length; i++) {
							let temp = i + 1;
							text += temp + '.\n';
							text += 'Course Class: ' + courseList[i].course_class + '\n';
							text += 'Course ID: ' + courseList[i].course_id + '\n';
							text += 'Course Name: ' + courseList[i].course_name + '\n';
							text += 'Course Time: ' + courseList[i].course_time + '\n';
							text += 'Course Type: ' + courseList[i].course_type + '\n';
							text += 'Teacher: ' + courseList[i].teacher_id;
							this.messages.push({ audio: false, user: false, robot: true, text: text });
							this.saveChat(text, false, true, this.openId);
							text = '';
						}
						this.$nextTick(function() {
							uni.pageScrollTo({
								scrollTop: 2000000,
								duration: 0 //app端这个必须设置成0
							});
						});
						return;
					}
					this.messages.push({ audio: false, user: false, robot: true, text: text });
					this.saveChat(text, false, true, this.openId);
					this.$nextTick(function() {
						uni.pageScrollTo({
							scrollTop: 2000000,
							duration: 0 //app端这个必须设置成0
						});
					});
				}
			});
		}
	}
};
</script>

<style scoped>
#map {
	position: fixed;
	top: 0;
	left: 0;
	z-index: 1000;
	width: 100%;
	height: 100vh;
}

.content {
	display: inline-block;
	box-sizing: border-box;
	position: relative;
	min-height: 100vh;
	width: 100vw;
	font-size: 31rpx;
	height: auto !important;
}

.getUserInfoClass {
	position: fixed;
	width: 100vw;
	min-height: 100vh;
	z-index: 9999;
	opacity: 0;
}

.testClass {
	position: fixed;
	z-index: 9999;
	top: 0;
}

.backgroundImage {
	position: fixed;
	height: 100vh;
	width: 100vw;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
}

.topBar {
	position: fixed;
	background-color: #f1f1f1;
	opacity: 0.95;
	height: calc(var(--status-bar-height) + 100rpx);
	width: 100%;
	top: 0;
	z-index: 10;
}

.setting {
	position: fixed;
	top: calc(var(--status-bar-height) + 15rpx);
	left: 30rpx;
	height: 65rpx;
	width: 65rpx;
	z-index: 10;
}

.username {
	position: fixed;
	top: calc(var(--status-bar-height) + 30rpx);
	left: 0;
	right: 0;
	text-align: center;
}

.message {
	position: relative;
	box-sizing: border-box;
	max-width: 63%;
	margin-left: 18%;
	margin-top: 50rpx;
	padding: 25rpx;
	border-radius: 20rpx;
	min-height: 95rpx;
	word-break: break-all;
}

.message:first-child {
	margin-top: calc(var(--status-bar-height) + 120rpx);
}

.message:last-child {
	margin-bottom: 150rpx;
}

.userMessage {
	background-color: #ffd152;
}

.robotMessage {
	background-color: #c8c7cc;
}

.audioMessage {
	padding: 17rpx 25rpx;
}

.messageContent {
	margin: 100rpx;
	padding-top: 100rpx;
}

.headImage {
	position: absolute;
	height: 95rpx;
	width: 95rpx;
	border-radius: 10px;
	top: 0%;
}

.userImage {
	right: -110rpx;
}

.robotImage {
	left: -110rpx;
}

.textButtonBar {
	position: fixed;
	background-color: #f1f1f1;
	width: 100%;
	min-height: 100rpx;
	bottom: 0;
}

.audio {
	position: fixed;
	height: 70rpx;
	width: 70rpx;
	bottom: 20rpx;
	left: 5vw;
}

.userText {
	position: fixed;
	min-height: 60rpx;
	line-height: 20rpx;
	width: 60vw;
	bottom: 20rpx;
	left: 17vw;
	background-color: white;
	padding: 0 20rpx;
	border-radius: 10px;
}

.send {
	position: fixed;
	height: 88rpx;
	width: 88rpx;
	bottom: 9rpx;
	right: 4vw;
}

.normalClass {
	position: fixed;
	min-height: 60rpx;
	line-height: 60rpx;
	width: 72vw;
	bottom: 20rpx;
	left: 17vw;
	background-color: white;
	padding: 0 20rpx;
	border-radius: 10px;
	text-align: center;
}

.speakClass {
	position: fixed;
	min-height: 60rpx;
	line-height: 60rpx;
	width: 72vw;
	bottom: 20rpx;
	left: 17vw;
	background-color: #c0c0c0;
	padding: 0 20rpx;
	border-radius: 10px;
	text-align: center;
}

.speakImage {
	height: 55rpx;
	width: 55rpx;
	padding: 0;
	margin: 0;
}
</style>
