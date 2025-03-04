from bs4 import BeautifulSoup
import re

html = """





<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <base href="http://mapp.nudt.edu.cn:80/"/>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>国防科大·理论闯关 </title>
    <meta name="description"
          content='????'>
    <meta name="keywords"
          content='知识库,知识管理,知识管理系统,开源知识库,开源知识管理系统,免费知识库,免费知识管理系统'>
    <meta name="author"
          content='wcp知识管理系统'>
    <meta name="robots" content="index,follow">
    

<base href="http://mapp.nudt.edu.cn:80/">
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport"
      content="width=device-width, initial-scale=1,user-scalable=no"/>
<link rel="icon" href="favicon.ico" mce_href="favicon.ico"
      type="image/x-icon">
<link rel="shortcut icon" href="favicon.ico" mce_href="favicon.ico"
      type="image/x-icon">
<script type="text/javascript" src="text/javascript/jquery-1.8.0.min.js"></script>
<link href="text/lib/bootstrap/css/bootstrap.min.css" rel="stylesheet">
<link href="text/lib/bootstrap/css/bootstrap-theme.min.css"
      rel="stylesheet">
<script src="text/lib/bootstrap/js/bootstrap.min.js"></script>
<script src="text/lib/bootstrap/respond.min.js"></script>
<script charset="utf-8"
        src="http://mapp.nudt.edu.cn:80/text/lib/alert/sweetalert.min.js"></script>
<link href="view/web-simple/atext/style/web-base.css" rel="stylesheet">
<link href="view/web-simple/atext/style/web-black.css" rel="stylesheet">
<link href="view/web-simple/atext/style/wts-app.css" rel="stylesheet">
<link href="text/lib/kindeditor/editInner-mobile.css" rel="stylesheet">

<script src="https://res.wx.qq.com/open/js/jweixin-1.6.0.js"></script>
<link href="text/style/dtapp.css" rel="stylesheet">

<script type="text/javascript">
    var basePath = 'http://mapp.nudt.edu.cn:80/';
    $(function () {
        $.ajaxSetup({
            cache: false
        });
    })

    //ajax执行远程命令
    function loadRemoteFunction(url, domid) {
        $('#' + domid).attr('disabled', 'disabled');
        $.post(url, {}, function (flag) {
            if (flag.STATE == '0') {
                alert("操作执行完班!");
            } else {
                alert(flag.MESSAGE);
            }
            $('#' + domid).removeAttr("disabled");
        }, 'json');
    }

    //ajax执行远程命令
    function loadRemoteFunctionAndReload(url, domid, mgs) {
        if (mgs) {
            if (confirm(mgs)) {
                doRemoteFunctionAndReload(url, domid, mgs);
            }
        } else {
            doRemoteFunctionAndReload(url, domid, mgs);
        }
    }

    //ajax执行远程命令-do
    function doRemoteFunctionAndReload(url, domid, mgs) {
        $('#' + domid).attr('disabled', 'disabled');
        $.post(url, {}, function (flag) {
            if (flag.STATE == '0') {
                location.reload();
            } else {
                alert(flag.MESSAGE);
            }
            $('#' + domid).removeAttr("disabled");
        }, 'json');
    }


    //confirm访问后台服务
    function confirmRemoteFunction(url, mgs) {
        if (confirm(mgs)) {
            window.location = basePath + url;
        }
    }

    function pAlert(tip, timenum) {
        if (timenum) {
            swal({
                text: tip,
                timer: timenum,
                buttons: false
            });
        } else {
            swal(tip);
        }
    }

    function pClose() {
        setTimeout(function () {
            swal.close();
        }, 200);
    }
    function appFormatDate() {
        const now = new Date();
        const year = now.getFullYear();
        const month = ((now.getMonth() + 1) + "").padStart(2, '0'); // Months are zero-based
        const day = (now.getDate() + "").padStart(2, '0');

        return year + "-" + month + "-" + day;
    }



</script>
    <link href="view/web-mobile/subject/text/mobile-card.css"
          rel="stylesheet">
    <script charset="utf-8"
            src="http://mapp.nudt.edu.cn:80/text/lib/alert/sweetalert.min.js"></script>

</head>
<style>
    .subjectBox {
        text-align: left;
    }


    @keyframes explode {
        0% {
            transform: scale(0);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }

    .dtbox2 {


        margin-top: 50%;
        text-align: center;
        background-color: #fff;
        margin-left: 10px;
        margin-right: 10px;
    }

    .warnTimeTip {
        float: right;
        z-index: 906;
        position: fixed;
        top: 150px;
        right: 3px;
        border: 1px dashed #cccccc;
        border-radius: 6px;
        background-color: #ffffef;
        cursor: pointer;
    }

    .firework {
        position: absolute;
        width: 50px;
        height: 50px;
        background: url('/text/img/huahua.png') no-repeat center center;
        background-size: contain;
        opacity: 0;
        animation: explode 2s ease-out forwards;
    }

    #fireworksCanvas {
        position: absolute;
        top: 100px;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 906;
    }

    .fireworksPer {
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;

        overflow: hidden;
        position: absolute;
        top: 100px;
        left: 0;
        z-index: 906;
    }


    .floating-gif {
        position: fixed;
        top: 50%;
        transform: translateY(-50%);
        animation: float 3s ease-in-out infinite;
    }

    .left {
        left: 10px;
    }

    .right {
        right: 10px;
    }

    @keyframes float {
        0%, 100% {
            transform: translateY(-50%) translateX(0);
        }
        50% {
            transform: translateY(-60%) translateX(10px);
        }
    }

</style>
<body class="homebackground">
<canvas id="fireworksCanvas" style="display:none;"></canvas>
<div class="fireworksPer" id="fireworksPer" style="display:none;"></div>


<!-- /.carousel -->
<div class=" dtbox2" style="min-height: 200px;">
    <!-- 首页--分类考场2 -->
    <div>
        
            <div class="row"
                 style="background-color: #ffffff; border-bottom: 1px solid #cccccc;">
                <div class="container" style="padding: 8px;">
                    <div>
                        <div style="overflow: hidden;">

                            
                                <!-- 多条练习 -->
                                <div style="margin: 4px;">
                                    <div class="side_unit_info"
                                         style="font-size: 15px; font-weight: 700; margin-bottom: 8px; line-height: 1.2em;">
                                        第1题&nbsp;
                                            判断/&nbsp;共10题
                                            
                                    </div>
                                    <div class="side_unit_info">
                                            
                                            
                                    </div>
                                </div>
                            
                            
                        </div>
                    </div>
                </div>
            </div>
        
        <div class="row" style="min-height: 200px;">
            <div class="container wts-paper-forms" style="padding: 0px;">
                
                <!-- 题目展示区 -->

                <div id="8a94964793b4bd630193b881266832e7-NAVI">
                    
                        <!-- 一级章节下的题目 1.填空，2.单选，3.多选，4判断，5问答-->
                        
                        
                        
                        
                            



<link rel="stylesheet" type="text/css"
      href="http://mapp.nudt.edu.cn:80/view/exam/subject/subject.css">
<!--判断题 flag=(adjudge:判卷，answer：答卷，checkup：检查)-->
<div>
    <div class="subjectUnitViewBox">
        <div class="subjectOrder">1</div>
        <div>
            
                <div style="text-align: left;">


                    
                        
                            <img src="/text/answer_img/20250304/0e43d7c9b2874f5f98a665b88d05d028.jpg" style="width: 100%">
                        
                        
                    


                        
                        
                </div>
                
                <div style="margin: 8px;"></div>
            
            
                <!-- 用户答题和预览时显示，填写答案 -->
                <div class="answerUnitViewBox">
                    <ul>

                        
                            <li><label style="cursor: pointer;">
                                    对 <input id="YXn8pgqHeSyn1P7O4LWYoM/mbZLXlHYRBQVJtjmGPTGsrl3ZBv51M5QjXqGe5OW3-INPUT"
                                                                 style="cursor: pointer;" type="radio"
                                                                 name="8a94964793b4bd630193b881266832e7"
                                                                 
                                
                                                                 value="YXn8pgqHeSyn1P7O4LWYoM/mbZLXlHYRBQVJtjmGPTGsrl3ZBv51M5QjXqGe5OW3">
                            </label></li>
                        
                            <li><label style="cursor: pointer;">
                                    错 <input id="kJBkbWbGLma4T6BNtT869AbKegcDrNpvEGXHmwvbXPimk+L+R4184q2Ac+qh8w6s-INPUT"
                                                                 style="cursor: pointer;" type="radio"
                                                                 name="8a94964793b4bd630193b881266832e7"
                                                                 
                                
                                                                 value="kJBkbWbGLma4T6BNtT869AbKegcDrNpvEGXHmwvbXPimk+L+R4184q2Ac+qh8w6s">
                            </label></li>
                        

                    </ul>
                    <div style="clear: both;"></div>
                </div>
            
            
            



<!-- 显示答案，显示分数 -->



        </div>
    </div>
</div>


                        
                        
                        
                    

                    


                </div>
            </div>
        </div>
        <div class="row"
             style="background-color: #ffffff; border-top: 1px solid #cccccc;border-bottom: 1px solid #cccccc;">
            <div class="container">
                <div style="padding-top: 20px; padding-bottom: 20px; text-align: center;">


                    <div class="btn-group btn-group-sm" role="group" aria-label="..." style="margin-top: 4px;">
                        
                         

                        


                            

                            
                                <button onclick="submitSubjectVar2()"
                                        type="button" id="submitBtnId"
                                        class="btn btn-success">
                                    <i class="glyphicon glyphicon-ok-sign"></i>&nbsp;提交答案&nbsp;


                                    /&nbsp;下一题
                                </button>
                            

                        
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- 开始答题-->
<div class="modal fade" id="submitVar-win" tabindex="-1" role="dialog"
     aria-labelledby="myModalLabel">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal"
                        aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
                <h4 class="modal-title" id="myModalLabel">答案</h4>
            </div>
            <div id="result-y" class="modal-body">
                <div class="doc_node_title_box"
                     style="font-size: 16px; text-align: center;">
                    <img alt="是否正確" style="width: 64px; height: 64px;"
                         src="text/img/result-yeas.png">
                </div>
                <div class="doc_node_title_box"
                     style="font-size: 16px; text-align: center;">正确
                </div>
            </div>
            <div id="result-c" class="modal-body">
                <div class="doc_node_title_box"
                     style="font-size: 16px; text-align: center;">
                    <img alt="是否正確" style="width: 64px; height: 64px;"
                         src="text/img/result-half.png">
                </div>
                <div class="doc_node_title_box"
                     style="font-size: 16px; text-align: center;">
                    得分:<span id="point-Span"></span>%
                </div>
            </div>
            <div id="result-n" class="modal-body" style="display: none;">
                <div class="doc_node_title_box"
                     style="font-size: 16px; text-align: center;">
                    <img alt="是否正確" style="width: 64px; height: 64px;"
                         src="text/img/result-no.png">
                </div>
                <div class="doc_node_title_box"
                     style="font-size: 16px; text-align: center;">错误
                </div>
            </div>
            <div id="rightBoxId2" class="modal-body" style="display: none;">
                <div class="innerTitle">
                    <img alt="" src="text/img/result-yeas.png"> 正确答案
                </div>
                <div class="ke-content innerbox"></div>
            </div>
            <div id="analysisBoxId3" class="modal-body" style="display: none;">
                <div class="innerTitle">
                    <img alt="" src="text/img/analysis.png"> 解析
                </div>
                <div class="ke-content innerbox"></div>
            </div>
            <div class="modal-footer">
                
                
                <button id="winShowAna" style="display: none;" type="button"
                        onclick="loadAnalysesWin()" class="btn btn-default">
                    <i class="glyphicon glyphicon-book"></i>&nbsp;解析
                </button>
                
            </div>
        </div>
    </div>
</div>
<!-- 题评论-->
<div class="modal fade" id="submitComments-win" tabindex="-1"
     role="dialog" aria-labelledby="myModalLabel">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal"
                        aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
                <h4 class="modal-title" id="myModalLabel">
						<span class="glyphicon glyphicon-star column_title">&nbsp;最新评论
						</span>
                </h4>
            </div>
            <div id="analysisBoxId" class="modal-body"
                 style="padding: 0px; padding-bottom: 50px;">
                <div id="commentShowBoxId"></div>
            </div>
        </div>
    </div>
</div>

<!-- 加油弹窗-->

<!-- Modal -->
<div class="modal fade " id="jiayouwin" tabindex="-1" role="dialog"
     aria-labelledby="exampleModalCenterTitle" aria-hidden="true">

    <div class="modal-dialog modal-dialog-centered" role="document" style="margin-top: 30%">
        <div class="modal-content">
            <div class="modal-body" style="text-align: center;font-size: 25px;">
                <img src="/text/img/jixujiayou.gif" style="width: 50%; height: 50%;"><br/>
                <span style="color: green;">正确:0</span>&nbsp;/&nbsp;<span
                    style="color: red;">错误:10</span><br/>
                再接再励，继续加油！
            </div>
        </div>
    </div>
</div>
<div id="timeNavButtonId" class="warnTimeTip" style="display: none;">
    <div>
        <img src="http://mapp.nudt.edu.cn:80//text/img/time.png"
             style="width: 56px; height: 56px;"/>
    </div>

    <div id="timelearn" style="text-align: center; font-weight: 700; font-size: 12px;">

    </div>
</div>





<style>


    .footimg {

        width: 100%;

    }


</style>
<div class="appcard">


    <img class="footimg" src="/text/img/foot_img.png"/>
    
</div>
<script type="text/javascript">
    $(function () {
        $(window).resize(function () {
            $('.containerbox').css('min-height', $(window).height() - 170);
        });
        $('.containerbox').css('min-height', $(window).height() - 170);
    });
</script>


</body>
<script src="view/web-simple/subject/text/random.js"></script>
<script type="text/javascript">


    function winNextClick() {
        window.location.href = 'websubject/PubRandomSubject.do?index=2&timelen=&testid=14fb8fc19d48476c80afbf01fbbc5671&subjectType=normalType'
    }

    window.onload = function () {
        // 向历史记录栈添加一个新的条目
        history.pushState(null, null, '/home/index.do');
        window.addEventListener('popstate', function (event) {
            // 当用户尝试返回时，再次添加一个新的历史记录条目
            history.pushState(null, null, '/home/index.do');
        });
    };

    /*
        // 在页面加载时绑定事件
        window.addEventListener('load', function() {
            // 当用户点击返回键时触发
            window.history.pushState(null, null, document.URL); // 添加一个状态到历史记录
            window.addEventListener('popstate', function(event) {
                // 用户尝试返回时的处理逻辑
                alert('您正在尝试返回上一页，这里可以插入返回逻辑');
                // 可以选择再次pushState以防止默认的返回行为
                window.history.pushState(null, null, document.URL);
            });
        });
        */

    


    var testid = "14fb8fc19d48476c80afbf01fbbc5671";
    var versionId = "8a94964793b4bd630193b881266832e7";
    var subjectId = "8a94964793b4bd630193b881266832e6";


    function submitSubjectVar2() {
        pAlert("loading...", 10000);
        $('#submitBtnId').prop('disabled', true); // 禁用按钮


        setTimeout(function () {
            pAlert("网络波动异常，正在重新进入答题...", 10000);
            window.location.href = '/home/index.do';
        }, 5000);

        $.post("websubject/PubRunPoint.do", {
            'testid': testid,
            'versionId': versionId,
            'val': enCodePaperForm(),
            'loginUserId': 'ca0aa798cbe2496ba099631fa06eccb4',
            'screenWidth': window.screen.width
        }, function (flag) {
            pClose();

            var nexturl = "websubject/PubRandomSubject.do?index=2&totalTime=" + totalTime + "&testid=14fb8fc19d48476c80afbf01fbbc5671&subjectType=normalType&userTestUuid=ca0aa798cbe2496ba099631fa06eccb4";
            window.location.href = nexturl;

            if (flag.STATE == 0) {

            } else {
                $('#submitBtnId').prop('disabled', false); // 启用按钮
                //pAlert(flag.MESSAGE);
            }
        }, 'json');
    }


    // 设置总时间（100分钟）

    var totalTime = 0;//倒计时多少秒

    function getTotalTime() {
        var totalTimeStr = '0'.replace(':', '.'); // 去除非数字字符
        totalTime = Math.floor(totalTimeStr);
    }

    function updateCountdown() {
        if (totalTime <= 0) {
            pAlert("答题时间已到，将自动提交答案...", 10000);
            document.getElementById('timelearn').innerHTML = "倒计时结束！";
            clearInterval(timer); // 停止定时器

            setTimeout(function () {
                var nexturl = "websubject/PubRandomSubject.do?index=11&totalTime=" + totalTime + "&testid=14fb8fc19d48476c80afbf01fbbc5671&subjectType=normalType";
                window.location.href = nexturl;
            }, 1000);
        } else {
            var minutes = Math.floor(totalTime / 60);
            var seconds = totalTime % 60;
            var examTime = padZero(minutes) + ":" + padZero(seconds);
            document.getElementById('timelearn').innerHTML = examTime;
            totalTime--; // 每秒减少1秒
        }
    }

    // 补零函数，确保两位数显示
    function padZero(num) {
        return num < 10 ? '0' + num : num;
    }

    /*



*/

    class Firework {
        constructor(x, y, targetX, targetY, color) {
            this.x = x;
            this.y = y;
            this.targetX = targetX;
            this.targetY = targetY;
            this.color = color;
            this.particles = [];
            this.exploded = false;
        }

        update() {
            if (!this.exploded) {
                this.y -= 5;
                if (Math.abs(this.y - this.targetY) < 5) {
                    this.explode();
                }
            } else {
                for (let particle of this.particles) {
                    particle.update();
                }
            }
        }

        draw(ctx) {
            if (!this.exploded) {
                ctx.beginPath();
                ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
            } else {
                for (let particle of this.particles) {
                    particle.draw(ctx);
                }
            }
        }

        explode() {
            this.exploded = true;
            for (let i = 0; i < 100; i++) {
                let angle = Math.random() * Math.PI * 2;
                let speed = Math.random() * 5 + 1;
                let particleColor = getRandomColor(); // 随机颜色
                this.particles.push(new Particle(this.x, this.y, angle, speed, particleColor));
            }
        }
    }

    class Particle {
        constructor(x, y, angle, speed, color) {
            this.x = x;
            this.y = y;
            this.angle = angle;
            this.speed = speed;
            this.color = color;
            this.life = 100;
        }

        update() {
            this.x += Math.cos(this.angle) * this.speed;
            this.y += Math.sin(this.angle) * this.speed;
            this.life--;
        }

        draw(ctx) {
            if (this.life > 0) {
                ctx.beginPath();
                ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
            }
        }
    }

    function getRandomColor() {
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        return "rgb(" + r + "," + g + "," + b + ")";
    }


    let fireworks = [];
    let canvas;
    let ctx;
    let spawnInterval;

    function init() {
        $("#fireworksCanvas").show();
        canvas = document.getElementById('fireworksCanvas');
        ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        window.addEventListener('resize', resizeCanvas);
        spawnInterval = setInterval(spawnFirework, 1000);
        // 20秒钟后停止生成烟花
        let closeTime = 1000 * 20;
        setTimeout(() => {
            $("#fireworksCanvas").hide();
            clearInterval(spawnInterval);
            stopAnimation();
            // 再过一段时间后清除所有烟花
            //animationTimeout = setTimeout(stopAnimation, closeTime);
        }, closeTime);
        animate();
    }

    function spawnFirework() {
        let x = Math.random() * canvas.width;
        let y = canvas.height;
        let targetX = Math.random() * canvas.width;
        let targetY = Math.random() * canvas.height * 0.3;
        let color = getRandomColor(); // 随机颜色
        fireworks.push(new Firework(x, y, targetX, targetY, color));
    }

    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let firework of fireworks) {
            firework.update();
            firework.draw(ctx);
        }

        fireworks = fireworks.filter(firework => !firework.exploded || firework.particles.some(particle => particle.life > 0));
    }

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function stopAnimation() {
        fireworks = [];
    }

    const duration = 10 * 1000; // 20 seconds in milliseconds
    const interval = 500; // Interval between each batch of fireworks in milliseconds
    const fireworksPerBatch = 5; // Number of fireworks per batch

    function createFirework() {
        const firework = document.createElement('div');
        firework.className = 'firework';

        // Random position
        var top = Math.random() * window.innerHeight;
        var left = Math.random() * window.innerWidth;


        firework.style.top = top + 'px';

        firework.style.left = left + 'px';


        // Random delay
        const delay = Math.random() * 500;
        firework.style.animationDelay = delay + 'ms';

        // Append to body
        document.getElementById('fireworksPer').appendChild(firework);

        // Remove after animation ends
        firework.addEventListener('animationend', () => {
            firework.remove();
        });
    }

    function startFireworks() {
        $("#fireworksPer").attr("style", "display:flex;");
        const startTime = Date.now();
        const intervalId = setInterval(() => {
            if (Date.now() - startTime >= duration) {
                clearInterval(intervalId);
                $("#fireworksPer").attr("style", "display:none;");
            } else {
                for (let i = 0; i < fireworksPerBatch; i++) {
                    createFirework();
                }
            }
        }, interval);
    }

    function jiayou() {
        $('#jiayouwin').modal('show');
        setTimeout(function () {
            $('#jiayouwin').modal('hide');   // 关闭弹窗
        }, 4000);
    }

    // Start the fireworks
    // startFireworks();
    //  jiayou();

    //答完题 并且全部题目都做对了 显示烟花效果
    
    


    function submitSubjectVarPubOwnErr() {
        pAlert("loading...", 10000);
        $.post("websubject/PubRunPoint.do", {
            'testid': testid,
            'versionId': versionId,
            'val': enCodePaperForm(),
            'subjectType': 'pubOwnSubject',
            'loginUserId': '8a9496469558671d019559c0b05601ef'
        }, function (flag) {
            pClose();
            if (flag.STATE == 0) {
                $('#submitVar-win').modal({
                    keyboard: false
                })
                $('#analysisBoxId').hide();
                $('#rightBoxId').hide();
                $('#winShowAna').show();
                $('#winNext').show();
                $('#myModalLabel').text("答案");
                if (flag.point == 0) {
                    $('#result-n').show();
                    $('#result-y').hide();
                    $('#result-c').hide();
                }
                if (flag.point == 100) {
                    $('#result-n').hide();
                    $('#result-y').show();
                    $('#result-c').hide();
                }
                if (flag.point < 100 && flag.point > 0) {
                    $('#result-n').hide();
                    $('#result-y').hide();
                    $('#result-c').show();
                    $('#point-Span').text(flag.point);
                }
            } else {
                pAlert(flag.MESSAGE);
            }
        }, 'json');
    }

    function tohomePage() {

        //老大哥要公众号点击量，本程序员也是无力，各位看官多担待
        var tohomeFlag = localStorage.getItem('tohomePage');

        var day = appFormatDate();

        if (tohomeFlag == day) {
            window.location.href = '/home/index.do'
        } else {
            localStorage.setItem('tohomePage', day);
            window.location.href = 'https://mp.weixin.qq.com/s/hQC4QK4FKxh609-gVnHNag'
        }
    }


</script>
</html>
"""
'''
testid = re.findall(r'var testid = "(.*?)";', html)[0]
versionId = re.findall(r'var versionId = "(.*?)";', html)[0]
subjectId = re.findall(r'var subjectId = "(.*?)";', html)[0]
print(testid, versionId, subjectId)

'''


soup = BeautifulSoup(html, 'html.parser')
button = soup.find('div', class_='side_unit_info')
url = button.text
ind = re.findall(r'第(.*?)题', button.text,re.S)[0]
q_type = re.findall(r'题\xa0\n                                            (.*?)/\xa0', button.text,re.S)[0]
q_img_url = soup.find('img', style="width: 100%").get('src')
anserbox = soup.find('div', class_='answerUnitViewBox')
ul = anserbox.ul
choices = []
for li in ul.find_all('li'):
    #print(li)
    choice = li.label.text.replace(' ', '').replace('\n', '') # 选项

    value = li.input.get('value')
    choices.append((choice, value))
    #print()
    #print()
print(choices)
print(ind, q_type, q_img_url)


