function bindCaptchaBtnClick() {
    // 绑定获取验证码的元素（按钮），on表示事件除法，即在click点击时触发event事件
    $('#captcha-btn').on('click', function (event) {
        var $this = $(this);  //指向captcha-btn
        var email = $("input[name='email']").val();  //获取name='email'的标签的值
        if (!email) {
            alert('请先输入邮箱');
            return;
        }
        $.ajax({  //用于发送Ajax请求
            url: '/user/captcha',  //向captcha路由发送ajax请求
            method: 'POST',
            data: {
                'email': email,
            },
            success: function (res) {  //定义回调函数取result，result为发送邮件的视图函数的return值
                var code = res['code']  //获取发送邮件的视图函数的code值
                if (code === 200) {  //如果视图函数返回200表示则进入
                    $this.off('click')  //取消this指向的对象的点击事件
                    var countDown = 60;
                    var timer = setInterval(function () {
                        if (countDown > 0) {
                            $this.text(countDown + '秒后重新发送');  //将register.html中的文本信息修改为该设置值
                        } else {
                            $this.text('获取验证码');
                            bindCaptchaBtnClick();  //重新启动点击事件
                            clearInterval(timer);  //清楚定时器
                        }
                        countDown -= 1;
                    }, 1000)  //调用定时器，1000ms执行一次
                    alert('验证码发送成功');
                } else {
                    alert(res['massage'])
                }
            }
        })
    });
}

// 等网页文档所有元素都加载完成后再执行
$(function () {
    bindCaptchaBtnClick();
});