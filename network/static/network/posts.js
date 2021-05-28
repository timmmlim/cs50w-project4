document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll("#edit").forEach(button => {
        button.onclick = function(){
            edit_post(this)
        }
    });

    document.querySelectorAll("#undo").forEach(button =>{
        button.onclick = function(){
            undo(this)
        }
    });

    document.querySelectorAll('#like').forEach(button => {
        button.onclick = function(){
            like(this)
        }
    });

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

// method to hide the form and show the original post
function undo(element){
    
    const form = element.parentElement;
    const compose_view = form.parentElement;
    const post_view = compose_view.parentElement.querySelector('#post-view');

    post_view.style.display = 'block';
    compose_view.style.display = 'none';
}

// method to check for the like count
function like(element){

    const post_id = element.dataset.post

    // send the like to the server
    fetch(`/like/${post_id}`, {method: 'POST'})
    .then(response => {
        console.log(response)
        return fetch(`/post/${post_id}`)
    })
    .then(response => response.json())
    .then(result => {
        // update the like count
        const post_view = element.parentElement;
        post_view.querySelector('#like-count').innerHTML = `&#10084;&#65039; ${result.likes}`
    })
}