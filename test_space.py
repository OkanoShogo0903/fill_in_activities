import fill_in
s = "4/11 12:00~18:00 20:30~21:00 to:univ" 
#s = "4/11 12:00~18:00 20:00~21:00 ohayou 4/12 10:00~12:00 konbanwa"
#s = "4"
#s = '<p><span class="atMention" title="湯田">@yuda13</span> 返信に対する返信(日付書いてないから送信はされないよ、あと送りたくないものは明記すれば送られないよ)</p>'
s = s + "<p><strong>セカンドタイトル</strong><br/>２つ目の投稿<br/>です</p>"
fill_in.Comment(s)
    
