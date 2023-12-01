document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('a.button');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function(event) {
        console.log("clicked on ", event.target.href);
        if (typeof ga === 'function') {
          ga('send', 'event', 'Download', 'click', 'Download-Button', {
            'hitCallback': function() {
              console.log('GA event sent');
            }
          });
        } else if (typeof gtag === 'function') {
          gtag('event', 'click', {
            'event_category': 'Download',
            'event_label': 'Download-Button',
            'event_callback': function() {
              console.log('GTag event sent');
            }
          });
        }
      });
    }
   });
