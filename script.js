let userFile = document.querySelector('.upload-arch');

userFile.addEventListener('change', () => {
    document.querySelector('#upload-img').innerText = userFile.files[0].name;
});

//################## VALIDACION DE DATOS DEL FORMULARIO ########################

let formulario = document.getElementById('myForm');
let expresions = {
    nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    telefono: /^\d{7,11}$/ // 7 a 14 numeros.
    }
let inputs = document.querySelectorAll('#myForm input');
let campos = {
    nombre: true,
    telefono: true
}

//Defino FUNCION VALIDADORA

let validandoCampo = (evento) => {
        switch (evento.target.name) {
        case "nombre-apellido":
            if (expresions.nombre.test(evento.target.value)) {
                document.querySelector('.input-nombre').classList.remove('val-incorrect');
                document.querySelector('.input-nombre').classList.add('val-correct');
                campos["nombre"] = true;
            } else{
                document.querySelector('.input-nombre').classList.add('val-incorrect');
                campos["nombre"] = false;
            }
            break;

        case "phone":
            if (expresions.telefono.test(evento.target.value)) {
                document.querySelector('.input-contacto').classList.remove('val-incorrect');
                document.querySelector('.input-contacto').classList.add('val-correct');
                campos["telefono"] = true;
            } else{
                document.querySelector('.input-contacto').classList.add('val-incorrect');
                campos["telefono"] = false;
            }
            break;
        }

        //CONDICIONAL PARA LA HABILITACION DEL BOTON  DE ENVIO DE FORMULARIO
        if (campos.nombre && campos.telefono)
            {
            console.log("DATOS VALIDOS");
            document.querySelector('#boton').classList.remove('no-activation');
            document.querySelector('#boton').classList.add('activation');
            document.querySelector("#boton").disabled = false;
        }
        else{
            console.log("DATOS INVALIDOS");
            document.querySelector('#boton').classList.remove('activation');
            document.querySelector('#boton').classList.add('no-activation');
            document.querySelector('#boton').disabled = true;


        }
}



inputs.forEach(function (teclaUp) {
    teclaUp.addEventListener('keyup', validandoCampo);
    
})

inputs.forEach(function (fueraDeCampo) {
    fueraDeCampo.addEventListener('blur', validandoCampo);

})


//ACCION DEL BOTON DEL FORMULARIO

 formulario.addEventListener('submit', (enviar)=>{

    enviar.preventDefault();
     if(campos.nombre && campos.telefono ){
        formulario.reset();
        alert("Se envió correctamente")
     }
 })