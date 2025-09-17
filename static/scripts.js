function ValidaFormularioLogin() {
    //Declaracion de variables
     var valorCorreo = document.getElementById("txt_correo").value;
     var valorPassword = document.getElementById("txt_password").value;

     if(valorCorreo == null || valorCorreo.length == 0 || /^\s+$/.test(valorCorreo)) {
        alert("Debes escribir un correo");
        document.getElementById("txt_correo").style.background = 'red';
        document.getElementById("txt_correo").focus();
        return false;
     }else if (valorPassword == null || valorPassword.length == 0 || /^\s+$/.test(valorPassword)){
        alert("Debes escribir la contraseña");
        document.getElementById("txt_password").value = "";
        document.getElementById("txt_password").style.background = 'red';
        document.getElementById("txt_password").focus();
        return false;  
    }
    return true;
}

function ValidaFormularioRegistro() {
    //Declaracion de variables
     var valorUsuario = document.getElementById("txt_usuario").value;
     var valorCorreo = document.getElementById("txt_correo").value;
     var valorPassword = document.getElementById("txt_password").value;
     var valor_conf_Password = document.getElementById("txt_conf_password").value;

     if(valorUsuario == null || valorUsuario.length == 0 || /^\s+$/.test(valorUsuario)) {
        alert("Debes escribir un usuario");
        document.getElementById("txt_usuario").style.background = 'red';
        document.getElementById("txt_usuario").focus();
        return false;
     } else if (valorCorreo == null || valorCorreo.length == 0 || /^\s+$/.test(valorCorreo)){
        alert("Debes escribir un correo");
        document.getElementById("txt_correo").value = "";
        document.getElementById("txt_correo").style.background = 'red';
        document.getElementById("txt_correo").focus();
        return false;
    } else if (valorPassword == null || valorPassword == 0 || /^\s+$/.test(valorPassword)) {
        alert("Debes escribir una contraseña");
        document.getElementById("txt_password").style.background = 'red';
        document.getElementById("txt_password").focus();
        return false;
    } else if (valor_conf_Password == null || valor_conf_Password == 0 || /^\s+$/.test(valor_conf_Password)) {
        alert("Debes confirmar tu contraseña");
        document.getElementById("txt_conf_password").style.background = 'red';
        document.getElementById("txt_conf_password").focus();
        return false;
    }
    return true;
}

function eliminarUsuario() {
    return confirm('¿Estás seguro de que quieres eliminar tu perfil? Esta acción es irreversible.');
}

setTimeout(() => {
  const flashContainer = document.getElementById("flash-container");
  if (flashContainer) {
    flashContainer.style.transition = "opacity 0.5s ease";
    flashContainer.style.opacity = "0";

    // 5 segundos
    setTimeout(() => flashContainer.remove(), 500);
  }
}, 3000);