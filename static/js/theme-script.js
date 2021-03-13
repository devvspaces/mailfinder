/* ------------------------------------------------
  Project:   Winck - Bootstrap 5 Multipurpose Landing Page
  Author:    ThemeHt
------------------------------------------------ */
/* ------------------------
    Table of Contents

  1. Predefined Variables
  2. Preloader  
  3. FullScreen
  4. Counter
  5. Owl carousel
  6. Testimonial Carousel
  7. Dropdown
  8. Magnific Popup
  9. Scroll to top
  10. Fixed Header
  11. Text Color, Background Color And Image
  12. Contact Form
  13. Countdown
  14. Rangeslider
  15. Btnproduct
  16. LightSlider
  17. Wow Animation
  18. Particles
  19. Window load and functions
  

------------------------ */

"use strict";

/*------------------------------------
  HT Predefined Variables
--------------------------------------*/
var $window = $(window),
    $document = $(document),
    $body = $('body'),
    $fullScreen = $('.fullscreen-banner') || $('.section-fullscreen'),
    $halfScreen = $('.halfscreen-banner');

//Check if function exists
$.fn.exists = function () {
  return this.length > 0;
};


/*------------------------------------
  HT PreLoader
--------------------------------------*/
function preloader() {
   $('#ht-preloader').fadeOut();
};

/*------------------------------------
  HT FullScreen
--------------------------------------*/
function fullScreen() {
    if ($fullScreen.exists()) {
        $fullScreen.each(function () {
        var $elem = $(this),
        elemHeight = $window.height();
        if($window.width() < 768 ) $elem.css('height', elemHeight/ 1);
        else $elem.css('height', elemHeight);
        });
        }
        if ($halfScreen.exists()) {
        $halfScreen.each(function () {
        var $elem = $(this),
        elemHeight = $window.height();
        $elem.css('height', elemHeight / 2);
        });
    }
};


/*------------------------------------
  HT Counter
--------------------------------------*/
function counter() {  
  $('.count-number').countTo({
    refreshInterval: 2
  });
};


/*------------------------------------
  HT Owl Carousel
--------------------------------------*/
function owlcarousel() {
$('.owl-carousel').each( function() {
  var $carousel = $(this);
  $carousel.owlCarousel({
      items : $carousel.data("items"),
      slideBy : $carousel.data("slideby"),
      center : $carousel.data("center"),
      loop : true,
      margin : $carousel.data("margin"),
      dots : $carousel.data("dots"),
      nav : $carousel.data("nav"),      
      autoplay : $carousel.data("autoplay"),
      autoplayTimeout : $carousel.data("autoplay-timeout"),
      navText : [ '<span class="la la-angle-left"><span>', '<span class="la la-angle-right"></span>' ],
      responsive: {
        0:{items: $carousel.data('xs-items') ? $carousel.data('xs-items') : 1},
        576:{items: $carousel.data('sm-items')},
        768:{items: $carousel.data('md-items')},
        1024:{items: $carousel.data('lg-items')},
        1200:{items: $carousel.data("items")}
      },
  });
});
};

/*------------------------------------
  HT Testimonial Carousel
--------------------------------------*/  
function testimonialcarousel() {
    $('.testimonial-carousel').on('slide.bs.carousel', function (evt) {
      $('.testimonial-carousel .controls li.active').removeClass('active');
      $('.testimonial-carousel .controls li:eq('+$(evt.relatedTarget).index()+')').addClass('active');
    })
};



/*------------------------------------
  HT Dropdown
--------------------------------------*/  
function dropdown() {
    $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
  if (!$(this).next().hasClass('show')) {
    $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
  }
  var $subMenu = $(this).next(".dropdown-menu");
  $subMenu.toggleClass('show');

  $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
    $('.dropdown-submenu .show').removeClass("show");
  });

  return false;
});
};


/*------------------------------------
  HT Magnific Popup
--------------------------------------*/
function magnificpopup() {
$('.popup-gallery').magnificPopup({
    delegate: 'a.popup-img',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
      titleSrc: function(item) {
        return item.el.attr('title') + '<small>by Devvspace and Netrobe Developers</small>';
      }
    }
  });
if ($(".popup-youtube, .popup-vimeo, .popup-gmaps").exists()) {
     $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
          disableOn: 700,
          type: 'iframe',
          mainClass: 'mfp-fade',
          removalDelay: 160,
          preloader: false,
          fixedContentPos: false
    });
  }

};     


/*------------------------------------
  HT Scroll to top
--------------------------------------*/
function scrolltop() {
  var pxShow = 300,
    goTopButton = $(".scroll-top")
    // Show or hide the button
  if ($(window).scrollTop() >= pxShow) goTopButton.addClass('scroll-visible');
  $(window).on('scroll', function () {
    if ($(window).scrollTop() >= pxShow) {
      if (!goTopButton.hasClass('scroll-visible')) goTopButton.addClass('scroll-visible')
    } else {
      goTopButton.removeClass('scroll-visible')
    }
  });
  $('.smoothscroll').on('click', function (e) {
    $('body,html').animate({
      scrollTop: 0
    }, 3000);
    return false;
  });
};


/*------------------------------------
  HT Fixed Header
--------------------------------------*/
function fxheader() {
  $(window).on('scroll', function () {
    if ($(window).scrollTop() >= 300) {
      $('#header-wrap').addClass('fixed-header');
    } else {
      $('#header-wrap').removeClass('fixed-header');
    }
  });
};


/*------------------------------------------
  HT Text Color, Background Color And Image
---------------------------------------------*/
function databgcolor() {
    $('[data-bg-color]').each(function(index, el) {
     $(el).css('background-color', $(el).data('bg-color'));  
    });
    $('[data-text-color]').each(function(index, el) {
     $(el).css('color', $(el).data('text-color'));  
    });
    $('[data-bg-img]').each(function() {
     $(this).css('background-image', 'url(' + $(this).data("bg-img") + ')');
    });
};


/*------------------------------------
  HT Contact Form
--------------------------------------*/
function contactform() { 
    $('#contact-form').validator();

    // when the form is submitted
//     $('#contact-form').on('submit', function (e) {

//     // if the validator does not prevent form submit
//     if (!e.isDefaultPrevented()) {
//         var url = window.location.href;

//         // POST values in the background the the script URL
//         $.ajax({
//             type: "POST",
//             url: url,
//             data: $(this).serialize(),
//             success: function (data)
//             {
//             // data = JSON object that contact.php returns

//             // we recieve the type of the message: success x danger and apply it to the 
//             var messageAlert = 'alert-' + data.type;
//             var messageText = data.message;

//             // let's compose Bootstrap alert box HTML
//             var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
            
//             // If we have messageAlert and messageText
//             if (messageAlert && messageText) {
//                 // inject the alert to .messages div in our form
//                 $('#contact-form').find('.messages').html(alertBox).show().delay(2000).fadeOut('slow');
//                 // empty the form
//                 $('#contact-form')[0].reset();
//             }
//           }
//         });
//         return false;
//     }
//  })    
};


/*------------------------------------
  HT Countdown
--------------------------------------*/
function countdown() {
  $('.countdown').each(function () {
    var $this = $(this),
      finalDate = $(this).data('countdown');
    $this.countdown(finalDate, function (event) {
      $(this).html(event.strftime('<li><span>%-D</span><p>Days</p></li>' + '<li><span>%-H</span><p>Hours</p></li>' + '<li><span>%-M</span><p>Minutes</p></li>' + '<li><span>%S</span><p>Seconds</p></li>'));
    });
  });
};



/*------------------------------------
  HT btnproduct
--------------------------------------*/
function btnproduct() {
  $('.btn-product-up').on('click', function (e) {
    e.preventDefault();
    var numProduct = Number($(this).next().val());
    if (numProduct > 1) $(this).next().val(numProduct - 1);
  });
  $('.btn-product-down').on('click', function (e) {
    e.preventDefault();
    var numProduct = Number($(this).prev().val());
    $(this).prev().val(numProduct + 1);
  }); 
};


/*------------------------------------
  HT LightSlider
--------------------------------------*/
function lightSlider() {
   $('#imageGallery').lightSlider({
    gallery:true,
    item:1,
    verticalHeight:450,
    thumbItem:4,
    slideMargin:0,
    speed:600,
    autoplay: true,
  });  
};



/*------------------------------------
  HT Wow Animation
--------------------------------------*/
function wowanimation() {
    var wow = new WOW({
        boxClass: 'wow',
        animateClass: 'animated',
        offset: 0,
        mobile: false,
        live: true
    });
    wow.init();
}

/*------------------------------------
  HT Particles
--------------------------------------*/

function particles() {
  jQuery("#particles-js").each(function () {
    particlesJS( {
  "particles": {
    "number": {
      "value": 160,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": {
      "value": "#01a479"
    },
    "shape": {
      "type": "circle",
      "stroke": {
        "width": 0,
        "color": "#ffffff"
      },
      "polygon": {
        "nb_sides": 5
      },
      "image": {
        "src": "img/github.svg",
        "width": 100,
        "height": 100
      }
    },
    "opacity": {
      "value": 1,
      "random": true,
      "anim": {
        "enable": true,
        "speed": 1,
        "opacity_min": 0,
        "sync": false
      }
    },
    "size": {
      "value": 3,
      "random": true,
      "anim": {
        "enable": false,
        "speed": 4,
        "size_min": 0.3,
        "sync": false
      }
    },
    "line_linked": {
      "enable": false,
      "distance": 150,
      "color": "#ffffff",
      "opacity": 0.4,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 1,
      "direction": "none",
      "random": true,
      "straight": false,
      "out_mode": "out",
      "bounce": false,
      "attract": {
        "enable": false,
        "rotateX": 600,
        "rotateY": 600
      }
    }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": {
        "enable": true,
        "mode": "bubble"
      },
      "onclick": {
        "enable": true,
        "mode": "repulse"
      },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 400,
        "line_linked": {
          "opacity": 1
        }
      },
      "bubble": {
        "distance": 250,
        "size": 0,
        "duration": 2,
        "opacity": 0,
        "speed": 3
      },
      "repulse": {
        "distance": 400,
        "duration": 0.4
      },
      "push": {
        "particles_nb": 4
      },
      "remove": {
        "particles_nb": 2
      }
    }
  },
  "retina_detect": true
});

  })
}


/*------------------------------------
  HT Window load and functions
--------------------------------------*/
$(document).ready(function() {
    fullScreen(),
    owlcarousel(),    
    counter(),
    testimonialcarousel(),
    dropdown(),
    magnificpopup(),
    scrolltop(),
    fxheader(),
    databgcolor(),  
    contactform(),
    countdown(),
    btnproduct(),
    lightSlider(),
    particles();
});


$window.resize(function() {
});


$(window).on('load', function() {
    preloader(),
    wowanimation();
});

// My codes too
let email_box_btn = document.querySelectorAll('.email_box_btn')
email_box_btn.forEach(i=>{
  i.addEventListener('click', getEmailBox)
})
  

function getEmailBox(event){
  let target = event.target
  $(target).addClass('active').siblings().removeClass('active')
  
  let email_box_cls = document.querySelectorAll('.email_box_cls')
    email_box_cls.forEach(nx=>{
      if (nx.getAttribute('email_box')==target.getAttribute('box_control')){
        $(nx).css('display','block')
      } else {
        $(nx).css('display','none')
      }
    }
  )
}


// Codes for ajax setup for get and post requests to backend
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          let cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


let csrftoken = ''
try{
  csrftoken = getCookie('csrftoken');
} catch(e){}


function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



try{
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
} catch(e){
}


let email_names_input = document.querySelector("#form_name[name='email_names']")
let company_name_input = document.querySelector("#form_name[name='company_name']")
let country_input = document.querySelector(".form-control[name='country']")
let domain_names_input = document.querySelector("#form_name[name='domain_names']")
let email_v_input = document.querySelector(".form-control[name='email_v']")
let email_file_input = document.querySelector(".form-control[name='email_file']")

let contact1 = document.querySelector('#contact-form1')
let contact2 = document.querySelector('#contact-form2')
let contact4 = document.querySelector('#contact-form4')
let contacts = [contact1,contact2,contact4]

let js_alerts = document.querySelector('#js_alerts')

// Code to set all the values of country list to the country full name
let country_lists = document.getElementById('country_list')
try{
  Array.from(country_lists.children).forEach(
    i=>{
      i.setAttribute('value',i.innerText)
    }
  )
} catch(e) {
  console.log(e)
}

function alertErrors(message, status='success'){
  let classes = 'alert-'+status

  let new_alert = document.createElement('div')
  let new_text = document.createTextNode(message)
  new_alert.appendChild(new_text)

  $(new_alert).addClass('alert '+classes)
  js_alerts.appendChild(new_alert)
}

function removeAlertErrors(){
  $(js_alerts).children().remove()
}

function removeFormErrors(){
  email_names_input.parentElement.lastElementChild.innerHTML = ''
  domain_names_input.parentElement.lastElementChild.innerHTML = ''
  country_input.parentElement.lastElementChild.innerHTML = ''
  email_v_input.parentElement.lastElementChild.innerHTML = ''
  email_v_input.parentElement.lastElementChild.innerHTML = ''
  company_name_input.parentElement.lastElementChild.innerHTML = ''
}

contacts.forEach(contact=>{
  contact.addEventListener('submit', conLookup)
})


let files = [];

$("input[type=file]").change(function(event) {
  $.each(event.target.files, function(index, file) {
    var reader = new FileReader();
    reader.onload = function(event) {
      var object = {};
      object.filename = file.name;
      object.data = event.target.result;
      files.push(object);
    };
    reader.readAsDataURL(file);
  });
  console.log(files)
});

function conLookup(e) {
  // Start loader
  $('#ht-preloader').fadeIn();

  e.preventDefault()
  let thisData = $(this).serialize()

  // if a file was passed
  if (files.length > 0){
    let file = files[files.length-1]['data']
    let len_eq = (file.match(/=/g) || []).length
    thisData = thisData + '&'+file+'&len_eq='+len_eq
  }
  let thisURL = window.location.href
  $.ajax({
      method: "POST",
      url: thisURL,
      data: thisData,
      success: handleFormSuccess,
      error: handleFormError
  })

  // Remove messages in the js alerts
  removeAlertErrors()

  // Remove all form errors
  removeFormErrors()
}

let data_list = document.querySelector('#data_list')
let email_count = document.querySelector('#email_count')
let valid_email_count = document.querySelector('#valid_email_count')

// Let's create the csv content and add top data
let csvContent = "data:text/csv;charset=utf-8,";
let rowArray = ['Email','Domain','Country','Verified']
let row = rowArray.join(",");
csvContent += row + "\r\n";

function handleFormSuccess(data, textStatus, jqXHR){
  $('#ht-preloader').fadeOut();
  // Check if error_message was sent
  let error_message = data['error_message']
  if (error_message){
    alertErrors(error_message, status='success')
  } else {
    // Reinstantiate csv content
    csvContent = "data:text/csv;charset=utf-8,";
    rowArray = ['Email','Domain','Country','Verified']
    row = rowArray.join(",");
    csvContent += row + "\r\n";

    alertErrors('We have found some emails for you', status='success')

    // Clean data list element
    $(data_list).children().remove()

    // Get queryset from data
    let queryset = data['queryset']

    // Count emails and edit counting values
    let num = queryset.length
    email_count.innerHTML = num;
    let num_verified = 0

    // Loop querset, create tr and td elements to add to result body
    queryset.forEach(item=>{
      let tr = document.createElement('tr')
      tr.setAttribute('scope','row')
      let keys = Object.keys(item)
      for (const key of keys){
        let td = document.createElement('td')
        if (key == 'status'){
          let iconSpan = document.createElement('span')
          let icon = document.createElement('i')
          if(item[key]==true){
            icon.classList.add('las', 'la-check')
            iconSpan.classList.add('text-success')
            // Increase the verified amount
            num_verified++;
          } else {
            icon.classList.add('las','la-times')
            iconSpan.classList.add('text-danger')
          }
          iconSpan.appendChild(icon)
          td.appendChild(iconSpan)
        } else{
          let text = document.createTextNode(item[key])
          td.appendChild(text)
        }
        tr.appendChild(td)
      }
      data_list.appendChild(tr)

      // Adding the data to the csv file
      let rowArray = Object.values(item)
      let row = rowArray.join(",");
      csvContent += row + "\r\n";

    })

    // Set amount of verified emails
    valid_email_count.innerHTML = num_verified;
  }
}

function handleFormError(jqXHR, textStatus){
  $('#ht-preloader').fadeOut();
  alertErrors('You filled the provided form incorrectly', status='warning')
  let error_data = jqXHR['responseJSON']
  let formNum = error_data['formNum']

  // Now add new errors
  if (formNum == 1){
    let email_names = error_data['email_names']
    let company_names = error_data['company_name']
    let countrys = error_data['country']
    if (email_names && (email_names.length > 0)){
      let email_text = ''
      email_names.forEach(i=>{
        email_text = email_text + i +'<br>'
      })
      email_names_input.parentElement.lastElementChild.innerHTML = email_text
    }
    if (company_names && (company_names.length > 0)){
      let company_text = ''
      company_names.forEach(i=>{
        company_text = company_text + i +'<br>'
      })
      company_name_input.parentElement.lastElementChild.innerHTML = company_text
    }
    if (countrys && (countrys.length > 0)){
      let country_text = ''
      countrys.forEach(i=>{
        country_text = country_text + i +'<br>'
      })
      country_input.parentElement.lastElementChild.innerHTML = country_text
    }
  } else if (formNum == 2){
      let domain_names = error_data['domain_names']
      if (domain_names && (domain_names.length > 0)){
        let text = ''
        domain_names.forEach(i=>{
          text = text + i +'<br>'
        })
        domain_names_input.parentElement.lastElementChild.innerHTML = text
      }
  } else if (formNum == 4){
      let email_v_error = error_data['email_v']
      let email_file_error = error_data['email_file']
      if ((email_v_error) && (email_v_error.length > 0)){
        let email_v_text = ''
        email_v_error.forEach(i=>{
          email_v_text = email_v_text + i +'<br>'
        })
        email_v_input.parentElement.lastElementChild.innerHTML = email_v_text
      }
      if (email_file_error && (email_file_error.length > 0)){
        let email_file_text = ''
        email_file_error.forEach(i=>{
          email_file_text = email_file_text + i +'<br>'
        })
        email_file_input.parentElement.lastElementChild.innerHTML = email_file_text
      }
  }
}

// Code to make download csv file button download csv
let download_csv = document.querySelector('#download_csv')
try {
  download_csv.onclick = function(e) {
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "MailFinder_emails.csv");
    link.style.display = 'none';
    document.body.appendChild(link); // Required for FF
  
    link.click(); // This will download the data file named "my_data.csv".
    alert('Downloading Started')
  }
} catch (error) {
  console.log(error)
}