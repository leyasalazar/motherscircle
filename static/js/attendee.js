if (document.querySelector('#attendance')){

  document.querySelector('#attendance').addEventListener('submit', (evt) => {
    evt.preventDefault();
    submitButton = document.querySelector('#submit')
    
    let formInfo = {
        attendance: submitButton.getAttribute("value").toLowerCase(),
        event_id: document.querySelector('h1').getAttribute("value")
    }
    if (formInfo['attendance'] == 'going'){
        submitButton.setAttribute('value','Not going')

    } else {
        formInfo['attendance'] = 'not going'
        submitButton.setAttribute('value','Going')
        
    }
    console.log(formInfo)

    fetch('/attendance', {
      method: 'POST',
      body: JSON.stringify(formInfo),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((responseJson) => {
        console.log(responseJson);
        total_attendees = document.querySelector('#total_attendees')
        total_attendees.innerHTML = responseJson.total_attendees
      });
  });
}
