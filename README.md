# xianyudanji
咸鱼单机签到
签到每天得0.3个赞助币，49个赞助币可永久赞助

食用方法：
0. 脚本里填用户名和密码，请放心填写，整个py文件只有调接口的语句，没有额外传输用户名密码的代码

1. python ./qiandao.py，建议每天上午8点以后执行，刚过12点执行会提示当日已签到

2. 青龙面板：
   2.1  脚本管理里添加本脚本
   2.2 定时任务里新建任务，名称：咸鱼单机每日签到；命令：task qiandao.py； 定时规则：0 9 * * *（每天上午9点执行）
