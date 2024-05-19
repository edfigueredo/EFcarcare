// Scritp para informar que fue subido
//alert('Estoy funcionando');
// ARCHIVO SUBIDO
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

//Defino funciones

let validandoCampo = (evento) =>{
    switch (evento.target.name){
        case "nombre-apellido":
            if(expresions.nombre.test(evento.target.value)){
                console.log("evento.target.value");
                document.querySelector('.input-nombre').classList.remove('val-incorrect');
                document.querySelector('.input-nombre').classList.add('val-correct');

            }else
                document.querySelector('.input-nombre').classList.add('val-incorrect');
                console.log("evento.target.value");
        break;

        case "phone":

            if(expresions.telefono.test(evento.target.value)){
                console.log("evento.target.value");
                document.querySelector('.input-contacto').classList.remove('val-incorrect');
                document.querySelector('.input-contacto').classList.add('val-correct');

            }else
                document.querySelector('.input-contacto').classList.add('val-incorrect');
                console.log("evento.target.value");
        break;

    }
}



inputs.forEach(function(teclaUp){
    teclaUp.addEventListener('keyup', validandoCampo)
})
inputs.forEach(function(fueraDeCampo){
    fueraDeCampo.addEventListener('blur', validandoCampo)
})

// formulario.addEventListener('submit', (noEnviar)=>{
//     noEnviar.preventDefault;
// })