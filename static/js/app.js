$( "#onUpload" ).on( "click", function() {
  console.log("send file");
  var file = $("#file").val();

  $.post(
    "/analyze",
    {file:file},
    function(data){
      console.log(data);
   });
});
