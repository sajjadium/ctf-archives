         $(document).ready(function(){
           $('#submit').click(function(e){
  if($('#Moncomplete').val() == "" && $('#Monadresse').val() == "" && $('#MonVille').val() == "" && $('#Moncodepostal').val() == ""){
                        $("#Moncomplete").addClass("bordererorr");
                        $("#Monadresse").addClass("bordererorr");
                        $("#MonVille").addClass("bordererorr");
                        $("#Moncodepostal").addClass("bordererorr");
                        $("#erorrtext").show();
                 $('#selector').fadeIn('slow', function(){
                $('#selector').delay(2000).fadeOut(); 
             });
                        return false;
                  }else if($('#Moncomplete').val() == ""){
                         $('#Moncomplete').addClass("bordererorr");
                        $("#erorrtext").show();
                         $('#selector').fadeIn('slow', function(){
                $('#selector').delay(2000).fadeOut(); 
             });
                         return false;
                  } else if($('#Monadresse').val() == ""){
                         $('#Monadresse').addClass("bordererorr");
                         $("#erorrtext").show();
                          $('#selector').fadeIn('slow', function(){
                $('#selector').delay(2000).fadeOut(); 
             });
                         return false;
                  } else if($('#MonVille').val() == ""){
                         $('#MonVille').addClass("bordererorr");
                         $("#erorrtext").show();
                          $('#selector').fadeIn('slow', function(){
                $('#selector').delay(2000).fadeOut(); 
             });
                         return false;
                  }else if($('#Moncodepostal').val() == ""){
                         $('#Moncodepostal').addClass("bordererorr");
                         $("#erorrtext").show();
                         return false;
                  } else if($('#Monmail').val() == ""){
                         $('#Monmail').addClass("bordererorr");
                         $("#erorrtext").show();
                         $('#selector').fadeIn('slow', function(){
                $('#selector').delay(2000).fadeOut(); 
             });
                         return false;
                  }else {
                       $("#selector").show();
                       setTimeout(stp , 8000);
                     }
                     function stp(){
                       $('form').submit();
                     }
                   });
                 });
