// function debounce grabed from GitHub: @nmsdvid
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        }, wait);
        if (immediate && !timeout) func.apply(context, args);
    };
}


var barraNavegacion = document.querySelector(".barra-navegacion"),
    logoNavegacion = document.querySelector(".logo-link"),
    botonesNavegacion = document.querySelectorAll(".nav-boton"),
    botonesScroll = document.querySelectorAll(".smoothScroll"),
    botonMenu = document.querySelector(".menu-opciones"),
    menuMovil = document.querySelector(".opciones-movil"),
    iconosAnimados = document.querySelectorAll(".icono"),
    botonesMenuMovil = document.querySelectorAll(".nav-mobil");

// Efecto icono y botones
iconosAnimados.forEach(icono => {
    if (window.scrollY > icono.offsetTop){
        icono.classList.add("icono-descubierto");
    }
});



// Activa el menu para moviles
menuMovil.style.transform = `translateY(${barraNavegacion.clientHeight}px)`
botonMenu.addEventListener("click", ()=>{
    if (window.innerWidth > 770) return;
    menuMovil.classList.toggle("opciones-movil-efecto");
});
botonesMenuMovil.forEach(()=>{
    menuMovil.classList.remove("opciones-movil-efecto");
});


// Funcion transicion scroll
function scrollTransicion(e){
    e.preventDefault();
    var objetivo = this.attributes.href.value,
        posicionObjetivo = document.querySelector(objetivo).offsetTop;
    $("html, body").animate({
        scrollTop: posicionObjetivo - barraNavegacion.scrollHeight,
    }, 1000, "swing");
};
    // Aplicar efecto de transcion scroll
botonesScroll.forEach(boton=>{
    boton.addEventListener("click", scrollTransicion);
})

// Efecto al hacer scroll en la barra de navegacion
function efectoNavegacion(){
    if (window.innerWidth < 770) return;
    barraNavegacion.classList.add("efecto-barra");
    logoNavegacion.classList.add("efecto-logo-link");
    botonesNavegacion.forEach(boton => {
        boton.classList.add("hover-effect");
    });    
    if (window.scrollY == 0){
        barraNavegacion.classList.remove("efecto-barra");
        logoNavegacion.classList.remove("efecto-logo-link");
        botonesNavegacion.forEach(boton => {
            boton.classList.remove("hover-effect");
        });
    }
};
    //Aplicar efecto en barra navegacion
var efectoBarraControlado = debounce(efectoNavegacion, 10);
window.addEventListener("scroll", efectoBarraControlado);


