var org_buttons = 0;
var quality_eng = 0;
var testDataMang = 0;
var specialization = 0;

function button_switch() {
    org_buttons = document.getElementById("org_buttons");
    quality_eng = document.getElementById("qualityEngButtons");
    testDataMang = document.getElementById("testDataMang");
    specialization = document.getElementById("specialization");

    if (org_buttons.style.display==="none")
    {
        org_buttons.style.display = "flex";
        quality_eng.style.display = "none";
        testDataMang.style.display = "none";
        specialization.style.display = "none";
    }
    else if(org_buttons.style.display==="flex")
    {
        org_buttons.style.display = "none";
        quality_eng.style.display = "none";
        testDataMang.style.display = "none";
        specialization.style.display = "none";
    }

}

function quality_switch() {
    org_buttons = document.getElementById("org_buttons");
    quality_eng = document.getElementById("qualityEngButtons");
    testDataMang = document.getElementById("testDataMang");
    specialization = document.getElementById("specialization");
    if (quality_eng.style.display==="none")
    {
        quality_eng.style.display = "flex";
        org_buttons.style.display = "none";
        testDataMang.style.display = "none";
        specialization.style.display = "none";
    }
    else if(quality_eng.style.display==="flex")
    {
        quality_eng.style.display = "none";
        org_buttons.style.display = "none";
        testDataMang.style.display = "none";
        specialization.style.display = "none";
    }

}

function testDataMang_switch() {
    org_buttons = document.getElementById("org_buttons");
    quality_eng = document.getElementById("qualityEngButtons");
    testDataMang = document.getElementById("testDataMang");
    specialization = document.getElementById("specialization");
    if (testDataMang.style.display==="none")
    {

        testDataMang.style.display = "flex";
        specialization.style.display = "none";
        quality_eng.style.display = "none";
        org_buttons.style.display = "none";
    }
    else if(testDataMang.style.display==="flex")
    {
        specialization.style.display = "none";
        testDataMang.style.display = "none";
        quality_eng.style.display = "none";
        org_buttons.style.display = "none";

    }

}

function specialization_switch() {
    org_buttons = document.getElementById("org_buttons");
    quality_eng = document.getElementById("qualityEngButtons");
    testDataMang = document.getElementById("testDataMang");
    specialization = document.getElementById("specialization");

    if (specialization.style.display==="none")
    {

        specialization.style.display = "inline";
        testDataMang.style.display = "none";
        quality_eng.style.display = "none";
        org_buttons.style.display = "none";
    }
    else if(specialization.style.display==="inline")
    {
        specialization.style.display = "none";
        testDataMang.style.display = "none";
        quality_eng.style.display = "none";
        org_buttons.style.display = "none";

    }

}

////function myFunction() {
////  document.getElementById("business_alignment").innerHTML = "business_alignment.html";
////}
//
//
//// Function to Load data from other HTML files
//
//function loadHtml(id,fileName){
//    console.log(id, fileName)
//    var dataUnhide = document.getElementById("template1");
//    dataUnhide.style.display = "block";
//
////    var dataUnhide2 = document.getElementById("template2");
////    dataUnhide2.style.display = "block";
//
//    //console.log(`Div id : ${id}, Path : ${path}, Filename : ${fileName}`);
//
//    let xhttp;
//    let element = document.getElementById(id);
//    // let pt = path;
//    let file = fileName;
//
//    if(file){
//        xhttp = new XMLHttpRequest();
//        xhttp.onreadystatechange = function(){
//            if(this.readyState == 4){
//                if(this.status == 200) {
//                    element.innerHTML = this.responseText;
//                }
//
//                if(this.status == 400){
//                    element.innerHTML = "<h2> Page not found. Please report to the Developer. </h2>";
//                }
//            }
//        }
//
//        xhttp.open("GET",`${file}`, true);
//        xhttp.send();
//        return;
//
//    }
//
//
//}