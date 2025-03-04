

var COOL_DOWN_PERIOD = 60 * 1000; // 默认1分钟冷却期，单位毫秒

function getCooldownPeriod() {
    var now = new Date();
    var hour = now.getHours();

   /* if (hour >= 18 && hour < 22) {
        return 1; // 18时-22时，2分钟冷却期
    } else if (hour >= 22 || hour <= 9) {
        return 1; // 22时-早9时，3分钟冷却期
    } else {
        return 1; // 其他时间，1分钟冷却期
    }*/

    return 0; // 其他时间，1分钟冷却期
}


function submitRoomPage(subjectType,roomid) {

    if (subjectType == 'betaType') {
        window.location.href = "exam/roompage.do?roomid="+roomid+"&subjectType=" + subjectType;
        return;
    }

    const now = new Date().getTime();
    const lastAnswerTime = parseInt(localStorage.getItem('lastAnswerTime'), 10);
    var lqsjFz = getCooldownPeriod();
    const COOL_DOWN_PERIOD = lqsjFz * 60 * 1000; // 获取当前时间段的冷却时间


    if (lastAnswerTime && now - lastAnswerTime < COOL_DOWN_PERIOD) {
        // 如果距离上次答题时间不足冷却时间，则显示错误信息
        pAlert("答题过快，请" + lqsjFz + "分钟后再试...", 3000);
    } else {
        // 否则，允许答题，并更新最后答题时间
        localStorage.setItem('lastAnswerTime', now);
        window.location.href = "exam/roompage.do?roomid="+roomid+"&subjectType=" + subjectType;
    }
}


submitRoomPage('normalType','8a949647953fadb001954615213d5ba7')
