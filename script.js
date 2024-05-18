// Scritp para informar que fue subido
//alert('Estoy funcionando');

let userFile =  document.querySelector('.upload-arch');

userFile.addEventListener('change', ()=>{
    document.querySelector('#upload-img').innerText = userFile.files[0].name;
});

