function tabClick(evt, target_class) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Get all elements with class="tablinks {target_class}" and set the class "active"
    tablinks = document.getElementsByClassName("tablinks " + target_class);
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className + " active"
    }

    // Show the current tab(s)
    var targets = document.getElementsByClassName(target_class);
    for (i = 0; i < targets.length; i++) {
        targets[i].style.display = "block";
    }
    evt.currentTarget.focus();
}