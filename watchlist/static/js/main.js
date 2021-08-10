function countDown(){
    setTimeout("deleteMessage()", 3000);
}
function deleteMessage(){
    meassage_box = document.getElementsByClassName("alert");
    meassage_box[0].className += " hide";

}
