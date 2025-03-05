


function winNextClick() {
    window.location.href = 'websubject/PubRandomSubject.do?index=2&timelen=&testid=774d8c09fded481fabdf67f1b80928a0&subjectType=normalType'
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




var testid = "774d8c09fded481fabdf67f1b80928a0";
var versionId = "8a9496479490f1ab019490f6ef43005b";
var subjectId = "8a9496479490f1ab019490f6ef43005a";


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
        'loginUserId': '3b37e5d6ac7d456cb94cc77b52d140d4',
        'screenWidth': window.screen.width
    }, function (flag) {
        pClose();

        var nexturl = "websubject/PubRandomSubject.do?index=2&totalTime=" + totalTime + "&testid=774d8c09fded481fabdf67f1b80928a0&subjectType=normalType&userTestUuid=3b37e5d6ac7d456cb94cc77b52d140d4";
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
            var nexturl = "websubject/PubRandomSubject.do?index=11&totalTime=" + totalTime + "&testid=774d8c09fded481fabdf67f1b80928a0&subjectType=normalType";
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
        'loginUserId': '8a949646955ca1ea01956139cd930c7c'
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
       …