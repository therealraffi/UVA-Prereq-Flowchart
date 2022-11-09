import { main } from './main.js';

var reverse = true

$(document).ready(function () {
    main()
    $('#button').css('background-color', 'gray')
    $('#button').click(function () {
        window.location.href = "./index.html";
    });
});