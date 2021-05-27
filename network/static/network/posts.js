document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll("#edit").forEach(button => {
        button.onclick = function(){
            edit_post(this)
        }
    })

    // hide the forms
    document.querySelectorAll('#compose-view').forEach(element => {
        element.style.display = 'none';
    })
});


function edit_post(element) {

    const post_id = element.dataset.post;
   
    // render form
    var form_div = element.parentElement.parentElement.querySelector('#compose-view');
    console.log(form_div);
    form_div.style.display = 'block';
    console.log(form_div);

    // hide original post
    element.parentElement.style.display = 'none';

    console.log(element.parentElement);

    // listen for form submission
    form_div.querySelector('#compose-form').addEventListener('submit', event =>{

        fetch(`/post/${post_id}`, {
            method: 'PUT',
            body:JSON.stringify({
                content: form_div.querySelector('#compose-body').value
            })
        })
        .then(response => {
                // hide form, show post instead
                console.log(response)
        })
    })    
}