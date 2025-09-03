// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 处理登录表单
    if (document.getElementById('loginForm')) {
        initLoginForm();
    }

    // 处理注册表单
    if (document.getElementById('registerForm')) {
        initRegisterForm();
    }
});

/**
 * 初始化登录表单
 */
function initLoginForm() {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameError = document.querySelector('.username-error');
    const passwordError = document.querySelector('.password-error');
    const togglePassword = document.getElementById('togglePassword');

    // 密码显示/隐藏切换
    togglePassword.addEventListener('click', function() {
        togglePasswordVisibility(passwordInput, this.querySelector('i'));
    });

    // 表单提交验证
    loginForm.addEventListener('submit', function(e) {
        let isValid = true;

        // 用户名验证
        if (!validateUsername(usernameInput, usernameError)) {
            isValid = false;
        }

        // 密码验证
        if (!validatePassword(passwordInput, passwordError)) {
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            // 添加抖动动画效果
            addShakeAnimation(loginForm);
        }
    });

    // 输入时实时验证
    usernameInput.addEventListener('input', function() {
        validateUsername(this, usernameError);
    });

    passwordInput.addEventListener('input', function() {
        validatePassword(this, passwordError);
    });
}

/**
 * 初始化注册表单
 */
function initRegisterForm() {
    const registerForm = document.getElementById('registerForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const password1Input = document.getElementById('password1');
    const password2Input = document.getElementById('password2');
    const usernameError = document.querySelector('.username-error');
    const emailError = document.querySelector('.email-error');
    const password1Error = document.querySelector('.password1-error');
    const password2Error = document.querySelector('.password2-error');
    const togglePassword1 = document.getElementById('togglePassword1');
    const togglePassword2 = document.getElementById('togglePassword2');

    // 密码显示/隐藏切换
    togglePassword1.addEventListener('click', function() {
        togglePasswordVisibility(password1Input, this.querySelector('i'));
    });

    togglePassword2.addEventListener('click', function() {
        togglePasswordVisibility(password2Input, this.querySelector('i'));
    });

    // 表单提交验证
    registerForm.addEventListener('submit', function(e) {
        let isValid = true;

        // 用户名验证 (3-12位字符)
        if (!validateUsernameLength(usernameInput, usernameError)) {
            isValid = false;
        }

        // 邮箱验证
        if (!validateEmail(emailInput, emailError)) {
            isValid = false;
        }

        // 密码验证 (6-16位)
        if (!validatePasswordLength(password1Input, password1Error)) {
            isValid = false;
        }

        // 确认密码验证
        if (!validatePasswordMatch(password1Input, password2Input, password2Error)) {
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            // 添加抖动动画效果
            addShakeAnimation(registerForm);
        }
    });

    // 输入时实时验证
    usernameInput.addEventListener('input', function() {
        validateUsernameLength(this, usernameError);
    });

    emailInput.addEventListener('input', function() {
        validateEmail(this, emailError);
    });

    password1Input.addEventListener('input', function() {
        validatePasswordLength(this, password1Error);
        // 实时验证密码一致性
        validatePasswordMatch(this, password2Input, password2Error);
    });

    password2Input.addEventListener('input', function() {
        validatePasswordMatch(password1Input, this, password2Error);
    });
}

/**
 * 切换密码可见性
 */
function togglePasswordVisibility(input, icon) {
    const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
    input.setAttribute('type', type);
    // 切换图标
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
}

/**
 * 验证用户名是否为空
 */
function validateUsername(input, errorElement) {
    if (!input.value.trim()) {
        showError(input, errorElement);
        return false;
    } else {
        hideError(input, errorElement);
        return true;
    }
}

/**
 * 验证用户名长度
 */
function validateUsernameLength(input, errorElement) {
    if (!input.value.trim() || input.value.length < 3 || input.value.length > 12) {
        showError(input, errorElement);
        return false;
    } else {
        hideError(input, errorElement);
        return true;
    }
}

/**
 * 验证密码是否为空
 */
function validatePassword(input, errorElement) {
    if (!input.value.trim()) {
        showError(input, errorElement);
        return false;
    } else {
        hideError(input, errorElement);
        return true;
    }
}

/**
 * 验证密码长度
 */
function validatePasswordLength(input, errorElement) {
    if (!input.value.trim() || input.value.length < 6 || input.value.length > 16) {
        showError(input, errorElement);
        return false;
    } else {
        hideError(input, errorElement);
        return true;
    }
}

/**
 * 验证邮箱格式
 */
function validateEmail(input, errorElement) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!input.value.trim() || !emailRegex.test(input.value)) {
        showError(input, errorElement);
        return false;
    } else {
        hideError(input, errorElement);
        return true;
    }
}

/**
 * 验证两次密码是否一致
 */
function validatePasswordMatch(passwordInput, confirmInput, errorElement) {
    if (confirmInput.value !== passwordInput.value) {
        showError(confirmInput, errorElement);
        return false;
    } else if (confirmInput.value.trim()) {
        hideError(confirmInput, errorElement);
        return true;
    }
    return false;
}

/**
 * 显示错误提示
 */
function showError(input, errorElement) {
    input.classList.add('border-red');
    errorElement.classList.add('show');
}

/**
 * 隐藏错误提示
 */
function hideError(input, errorElement) {
    input.classList.remove('border-red');
    errorElement.classList.remove('show');
}

/**
 * 添加抖动动画
 */
function addShakeAnimation(element) {
    element.classList.add('animate-shake');
    setTimeout(() => {
        element.classList.remove('animate-shake');
    }, 500);
}
