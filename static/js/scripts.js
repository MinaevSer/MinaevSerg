$(document).ready(function () {
   var form = $('#form_number_products');
   console.log(form);
   $('#logo_min').hide();

   function cart_upd(product_id, nmb, size, is_delete){
       var data  = {};
       data.product_id = product_id;
       data.nmb = nmb;
       data.size = size;
       var csrf_token = $('#form_number_products [name="csrfmiddlewaretoken"]').val();
       data["csrfmiddlewaretoken"] = csrf_token;

       if (is_delete){
           data["is_delete"]=true;
       }

       var url = form.attr("action");
       console.log(data);
       $.ajax({
          url: url,
          type: 'POST',
          data: data,
          cache: true,
          success: function (data) {
              console.log("OK");
              console.log(data.products_total_nmb);
              if (data.products_total_nmb){
                  $('#cart_total_nmb').text("("+data.products_total_nmb+")");
              }
          },
          error: function () {
              console.log('ERROR')
          }
       });
   };

   form.on('submit', function (e) {
       e.preventDefault();
       var nmb = $('#number').val();
       if (document.getElementById('radio_group')){
           console.log('is_size');
           var size = $('input[name = size]:checked', '#form_number_products').val();
       }
       else {
           console.log('no_size');
           var size = '30';
       }
       console.log(size);
       console.log(nmb);
       var submit_btn = $('#submit_btn');
       var product_id = submit_btn.data("product_id");
       var product_name = submit_btn.data("name");
       var product_price = submit_btn.data("price");
       console.log(product_id);
       console.log(product_name);
       console.log(product_price);
       cart_upd(product_id, nmb, size, is_delete=false)
   });

   $('input[name = size]').on('change', function () {
       var base_price = document.getElementById('item_price').innerHTML;
       console.log(base_price);
       $('#item_price').hide();
       if ($(this).val()==35){
           var change_price = Number(base_price)+125;
           $('#change_price').text(change_price);
       }
       else if ($(this).val()==30){
           $('#change_price').text(base_price);
       }
       else if ($(this).val()==25){
           var change_price = Number(base_price)-125;
           $('#change_price').text(change_price);
       }
   });

   $(document).on('click', '#del_button', function (e) {
       e.preventDefault();
       var product_id = $(this).data("product_id");
       console.log(product_id);
       var nmb = 0;
       var size = 0;
       cart_upd(product_id, nmb, size, is_delete = true);
       location.reload();
   });

   $(document).on('click', '#ind_btn', function (e) {
       e.preventDefault();
       var product_id = $(this).data("product_id");
       var nmb = 1;
       cart_upd(product_id, nmb, size = 30, is_delete = false);
   });
   
   function calcCartPrice() {
       var cart_total_price = 0;
       var elems = document.getElementsByClassName('item_total_price');
       for (var i = 0; i<elems.length; i++){
           var n = (elems[i]).innerHTML;
           cart_total_price+=Number(n);
       }
       console.log(cart_total_price);
       $('#cart_total_price').text(cart_total_price)
   }

   $(window).scroll(function () {
       if($(this).scrollTop()>110){
           $('#navbar_head').hide();
           $('#logo_min').show();
       }
       else {
           $('#navbar_head').show();
           $('#logo_min').hide();
       }
   });
    calcCartPrice();
});