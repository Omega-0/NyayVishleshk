# roshurl = "https://i.ibb.co/555DwxT/Pics-Art-03-10-03-11-48.jpg"
# ansurl = "https://i.ibb.co/N9yK2cq/linkdin-ansh-pic.jpg"
# boturl = "https://i.ibb.co/pzTM0fJ/bot.jpg"
# green_bot_url = "https://i.ibb.co/yFtF8qn/green-bot.png"
# bot2 = "https://i.ibb.co/XDvcmq4/bot2.jpg"

css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #EBF4FF
}
.chat-message.bot {
    background-color: #F3FFF6
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #000000;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/XDvcmq4/bot2.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/GTbBDTn/user-icon.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
''' 
