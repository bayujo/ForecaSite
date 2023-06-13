$(document).ready(function () {
  $("#form").submit(function (event) {
    event.preventDefault();
    clickShowMap(null, "showMapButton", "Show Map");
    var start_location = $("#start_location").val();
    var end_location = $("#end_location").val();
    $.ajax({
      type: "GET",
      url: "/map",
      data: {
        start_location: start_location,
        end_location: end_location,
      },
      success: function (data) {
        localStorage.setItem("mapData", data);
        $.ajax({
          type: "GET",
          url: "/distance",
          data: {
            start_location: start_location,
            end_location: end_location,
          },
          success: function (data2) {
            $("#map").html(data);
            $("#distance").text("Distance: " + data2);
            $("#map_hero").fadeOut(function () {
              $("#map_container").fadeIn(function () {
                var storedData = localStorage.getItem("mapData");
                $("#map").html(storedData);
              });
            });

            clickShowMap(1, "showMapButton", "Show Map");
          },
          error: function (error) {
            console.log(error);
            clickShowMap(1, "showMapButton", "Show Map");
          },
        });
      },
    });
  });

  $("#predict").click(function () {
    clickShowMap(null, "predict", "Compare now!");
    var start_location = $("#start_location").val();
    var end_location = $("#end_location").val();
    var surge_multiplier = $("#surge_multiplier").val();
    $.ajax({
      type: "GET",
      url: "/predict",
      data: {
        start_location: start_location,
        end_location: end_location,
        surge_multiplier: surge_multiplier,
      },
      success: function (data) {
        $("#refresh-table").html(data);
        $("#map_container").fadeOut();
        $("#home-container10").fadeOut(function () {
          $("#comparison_container").fadeIn();
        });
        clickShowMap(1, "predict", "Compare now!");
        setTimeout(function () {
          $("#try-route").fadeIn();
        }, 5000);
      },
      error: function (error) {
        console.log(error);
        clickShowMap(1, "predict", "Compare now!");
      },
    });
  });

  $("#predict-rain").click(function () {
    var form = document.getElementById('form');
    if (!form.checkValidity()) {
      form.reportValidity();
    } else {
      clickShowMap(null, "predict-rain", "Check for Rain");
      var location = $("#location").val();
      $.ajax({
        type: "GET",
        url: "/rain-tomorrow",
        data: {
          location: location,
        },
        success: function (data) {
          $("#refresh-table").html(data);
          $("#map_hero").fadeOut()
          $("#home-container10").fadeOut(function () {
            $("#comparison_container").fadeIn();
          });
          clickShowMap(1, "predict-rain", "Check for Rain");
          setTimeout(function () {
            $("#try-route").fadeIn();
          }, 5000);
        },
        error: function (error) {
          console.log(error);
          clickShowMap(1, "predict-rain", "Check for Rain");
        },
      });
    }
  });

  $("#predict-heart").click(function () {
    var form = document.getElementById('form');
    if (!form.checkValidity()) {
      form.reportValidity();
    } else {
      clickShowMap(null, "predict-heart", "Check patient");
      var time = $("#time").val();
      var ejection_fraction = $("#ejection_fraction").val();
      var serum_creatinine = $("#serum_creatinine").val();
      $.ajax({
        type: "GET",
        url: "/heart-failure",
        data: {
          time: time,
          ejection_fraction: ejection_fraction,
          serum_creatinine: serum_creatinine,
        },
        success: function (data) {
          $("#refresh-table").html(data);
          $("#map_hero").fadeOut()
          $("#home-container10").fadeOut(function () {
            $("#comparison_container").fadeIn();
          });
          clickShowMap(1, "predict-heart", "Check patient");
          setTimeout(function () {
            $("#try-route").fadeIn();
          }, 5000);
        },
        error: function (error) {
          console.log(error);
          clickShowMap(1, "predict-heart", "Check patient");
        },
      });
    }
  });

  $("#predict-cc").click(function () {
    var form = document.getElementById('form');
    if (!form.checkValidity()) {
      form.reportValidity();
    } else {
      clickShowMap(null, "predict-cc", "Check cluster");
  
      var formData = {
        balance: $("#balance").val(),
        balance_frequency: $("#balance_frequency").val(),
        purchases: $("#purchases").val(),
        oneoff_purchases: $("#oneoff_purchases").val(),
        installments_purchases: $("#installments_purchases").val(),
        cash_advance: $("#cash_advance").val(),
        purchases_frequency: $("#purchases_frequency").val(),
        oneoff_purchases_frequency: $("#oneoff_purchases_frequency").val(),
        purchases_installments_frequency: $("#purchases_installments_frequency").val(),
        cash_advance_frequency: $("#cash_advance_frequency").val(),
        cash_advance_trx: $("#cash_advance_trx").val(),
        purchases_trx: $("#purchases_trx").val(),
        credit_limit: $("#credit_limit").val(),
        payments: $("#payments").val(),
        minimum_payments: $("#minimum_payments").val(),
        prc_full_payment: $("#prc_full_payment").val(),
        tenure: $("#tenure").val()
      };
  
      $.ajax({
        type: "GET",
        url: "/cc",
        data: formData,
        success: function (data) {
          $("#refresh-table").html(data);
          $("#map_hero").fadeOut()
          $("#home-container10").fadeOut(function () {
            $("#comparison_container").fadeIn();
          });
          clickShowMap(1, "predict-cc", "Check cluster");
          setTimeout(function () {
            $("#try-route").fadeIn();
          }, 5000);
        },
        error: function (error) {
          console.log(error);
          clickShowMap(1, "predict-cc", "Check cluster");
        },
      });
    }
  });
  

  $("#reset").click(function () {
    clickShowMap(null, "reset", "Reset");
    setTimeout(function () {
      $("#comparison_container").fadeOut(function () {
        $("#map_hero").fadeIn();
        $("#home-container10").fadeIn();
        clickShowMap(1, "reset", "Reset");
        $("#try-route").fadeOut();
      });
    }, 500);
  });

  $("#fullscreen-btn").click(function () {
    const elem = document.getElementById("ipynb");
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    }
  });
});

function clickShowMap(reverse = null, buttonID, buttonText) {
  var button = document.getElementById(buttonID);

  if (reverse != null) {
    button.innerHTML = buttonText;
    button.disabled = false;
  } else {
    button.innerHTML = `
        <svg aria-hidden="true" role="status" class="inline w-4 h-4 mr-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
        </svg>Loading...
        `;

    button.disabled = true;
  }
}

function scrollToDiv(target) {
  var target = document.getElementById(target);
  var targetOffset = target.getBoundingClientRect().top;
  var windowHeight = window.innerHeight;
  var targetHeight = target.offsetHeight;
  var scrollToPosition = targetOffset + targetHeight / 2 - windowHeight / 2;

  window.scrollTo({
    top: scrollToPosition,
    behavior: "smooth",
  });
}

$(document).ready(function () {
  var profiles = ["#profile-1", "#profile-2", "#profile-3"];
  var currentIndex = 0;

  function fadeProfiles() {
    var currentProfile = profiles[currentIndex];
    var nextProfile = profiles[(currentIndex + 1) % profiles.length];

    $(currentProfile).fadeOut(1000, function () {
      $(nextProfile).fadeIn(1000, function () {
        currentIndex = (currentIndex + 1) % profiles.length;
        setTimeout(function () {
          fadeProfiles();
        }, 3000);
      });
    });
  }

  fadeProfiles();
});

var slideUp = {
  distance: "25%",
  origin: "top",
  duration: 1500,
};

var slideLeft = {
  distance: "100%",
  origin: "left",
  duration: 1500,
};

var slideRight = {
  distance: "100%",
  origin: "right",
  duration: 1500,
};

var slideMap = {
  distance: "100%",
  duration: 1000,
  reset: true,
};

var slideDown = {
  distance: "100%",
  duration: 1000,
  origin: "top",
};

ScrollReveal().reveal(".home-features", slideUp);
ScrollReveal().reveal(".home-container07", slideLeft);
ScrollReveal().reveal(".home-image02", slideRight);
ScrollReveal().reveal(".home-testimonials", slideLeft);
ScrollReveal().reveal(".home-achievements", slideRight);
ScrollReveal().reveal(".home-feature1", slideLeft);
ScrollReveal().reveal(".home-feature2", slideRight);
ScrollReveal().reveal(".home-container22", slideLeft);
ScrollReveal().reveal(".home-container23", slideRight);
ScrollReveal().reveal(".home-menu", slideDown);
