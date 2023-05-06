function pwd_handler_login(form)
{
        if (form.password.value != '')
        {
            form.password.value = CryptoJS.MD5(form.password.value).toString();
            form.password.value = CryptoJS.SHA1(form.password.value).toString();
            console.log(form.password.value);
        }
}

function pwd_handler_registration(form)
{
        if (form.password.value != '')
        {
            form.password.value = CryptoJS.MD5(form.password.value).toString();
            console.log(form.password.value);
        }
}