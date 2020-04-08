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