$(function(){
    $('body').on('click', 'i', async function(e){
        e.preventDefault();
        $(this).toggleClass('far fas');
        response = await likeMessage(e.target.id);
    });
});


async function likeMessage(id){
    let messageId = parseInt(id);
    const response = await $.post(`/messages/${messageId}/likes`);
    return response;
};