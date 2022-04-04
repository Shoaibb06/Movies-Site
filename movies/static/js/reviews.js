$(document).ready(function () {
  getcomment();
  $('.comment-box button').click(function () {
   var comment_text = $('.comment-box textarea').val();
   $.ajax({
    type: 'POST',
    url: '/bbs/article/{{ article_list.id }}/comment/',
    data: {comment: comment_text},
    success:function (callback) {
     var data = $.parseJSON(callback);
     $('.callback').html(data.result);
     if(data.result === 'successfully') {
      getcomment();
     }
    }
   })
  });
 });
 function getcomment() {
  $.ajax({
   type: 'GET',
   url: '/bbs/article/{{ article_list.id }}/get_comment/',
   success:function (call) {
    var datas = $.parseJSON(call);
    $('.comment-list').html(datas.answer);
   }
  })
 }