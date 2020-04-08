function chck(e){
    console.log('event', e);
    const newCompleted = e.target.checked;
    const todoId = e.target.dataset['id'];
    fetch('/todos/'+ todoId +'/set-completed', {
        method: 'POST',
        body: JSON.stringify({
            'completed' : newCompleted,
            //'id' : todoId
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .catch(function(){
        document.getElementById('error').className = '';
    })
}

function deleteItem(e){
    console.log('event', e);
    const todoId = e.target.dataset['id'];
    fetch('/todos/' + todoId, {
        method: 'DELETE'
      })//;
    .then(function (response){
        return response.json();
        
    })
    .then (function (jsonRsponse){
        console.log(jsonRsponse);
        let idd = jsonResponse['id'];
        
    })
    .catch(function(){
        //document.getElementById('error').className = '';
    })
}