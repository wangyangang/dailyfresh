$(function () {

    let error_name = false;
    let error_password = false;

    function check_user_name() {
        let len = $("#username").val().length;
        if(len<5||len>20){
            $("#username").next().html('请输入5-20个字符的用户名');
            $("#username").next().show();
            error_name = true;
        }else{
            $("#username").next().hide();
            error_name = false;
        }
    }

    function check_pwd(){
        var len = $('#pwd').val().length;
        if(len<8||len>20)
        {
            $('#pwd').next().html('密码最少8位，最长20位')
            $('#pwd').next().show();
            error_password = true;
        }
        else
        {
            $('#pwd').next().hide();
            error_password = false;
        }
    }

    $("#username").blur(function () {
        check_user_name();
    });

    $("#pwd").blur(function () {
        check_pwd();
    });

    $("#login-form").submit(function (e) {
        e.preventDefault();

        let user_name = $("#username").val();
        let pwd = $("#pwd").val();
        let remember = $("#remember").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        check_user_name();
        check_pwd();

        if(error_name || error_password){
            console.log('用户名或密码错误');
            return;
        }else{
            let data = {
                'username': user_name,
                'pwd': pwd,
                'remember': remember,
                'csrfmiddlewaretoken': csrf_token
            };
            $.ajax({
                url: '/user/login/',
                type: 'post',
                dataType: 'json',
                data: data,
                success: function (ret) {
                    console.log(ret);
                    if(ret.errno == '0'){
                        location.href = '/';
                    }else{
                        // 未激活
                        if(ret.errno == '4104'){
                            location.href = '/user/unverified-email/';
                        }
                    }
                }
            })
        }

    });
});