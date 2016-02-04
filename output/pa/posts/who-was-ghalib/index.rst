.. title: Who Was Ghalib?
.. slug: who-was-ghalib
.. date: 2014/04/06 10:07:25
.. tags: ghalib, word clouds, words, fp7 
.. link: 
.. description: 
.. type: text

.. raw:: html

  <object type="image/svg+xml" id="whowasghalibobj"   data="/files/whowasghalib.svg">Your browser does not support SVG</object>

  <script type="text/javascript">
  
    function changeColor(){
  
      var svgObj = document.getElementById('whowasghalibobj');
      var svgDoc = svgObj.contentDocument;

      var texts = svgDoc.getElementsByTagName("path");
      palette = [ 'rgb(117, 170, 219)',
      'rgb(196, 216, 226)',
      'rgb(153, 153, 153)',
      'rgb(0, 43, 127)' ];
    
      i = Math.floor(Math.random() * texts.length);
      s = texts[i];
      s.style.fill=palette[Math.floor(Math.random()*palette.length)];
      for (i=0;i<3;i++){
      texts[i].style.fill = texts[i].style.fill;
      }
      j=1;
     
    }
    window.setInterval(changeColor,250);
  
  </script>
  
I am looking forward to attending a workshop this coming weekend on 
`“Who Was Ghalib?” <http://www.columbia.edu/itc/mealac/pritchett/00urduhindilinks/workshop2014/index.html>`_ 
at Columbia University. It is also a retirement party for Frances Pritchett, 
so I have designed the poster above. It contains the 150 most common words in Ghalib’s poetry displayed
using Columbia’s palette. I have more
to say about word clouds in Urdu and Hindi, but the poster will have to suffice for now.

You can download it here: `PDF </files/whowasghalib.pdf>`_ `PNG </files/whowasghalib.png>`_.

