$(document).foundation()


function selected(id)
{
    var element = document.getElementById(id);
    var ehidden = element.nextSibling.nextSibling;
    console.log(ehidden);

    if($(element).hasClass('marked-in'))
    {
        ehidden.setAttribute('value', '2')
        $(element).removeClass('marked-in');
        element.removeChild(element.childNodes[0])

        $(element).addClass('marked-ex');
        var node = document.createElement('i');
        $(node).addClass('fas');
        $(node).addClass('fa-times');
        element.appendChild(node);
    }
    else if($(element).hasClass('marked-ex'))
    {
        ehidden.setAttribute('value', '0')
        $(element).removeClass('marked-ex');
        element.removeChild(element.childNodes[0])
    }
    else
    {
        ehidden.setAttribute('value', '1')
        $(element).addClass('marked-in');
        var node = document.createElement('i');
        $(node).addClass('fas');
        $(node).addClass('fa-check');
        element.appendChild(node);
    }
}


function get_rev()
{
    var element = document.getElementById('edit-this');

    $('#edit-here').val(element.innerText)
}