'use strict';

function Event(props) {
  return (
    <div className="events_most_commented">
      <a href={props.event_id}> {props.title} </a>
      <p> By {props.user_id} </p>
      <p> Location: {props.location} </p>
      <p> {props.date} {props.time}</p>
      {/* <p> {props.description} </p> */}
      <img src={props.img} alt="event-img" />
    </div>
  );
}

function EventContainer() {
//code commented used to test React
// const exampleEvent = {
//     "title": "Zoo",
//     "user_id": 1,
//     "location": "Minnesota Zoo",
//     "date": "2022-11-06",
//     "time": "12:00",
//     "description": "I am going with my son this weekend",
//     "img": "https://i.ibb.co/zHfcq0k/chris-briggs-WNAic3c-MDR8-unsplash.jpg"
// };

// const [events, setEvents] = React.useState([exampleEvent]);

const [events, setEvents] = React.useState([]);

React.useEffect(() => {
  fetch('/events_most_commented.json')
  .then((response) => response.json())
  .then((data) => setEvents(data.events))
  // .then((data) => console.log(data))
}, [])

const allEvents = []

  for (const currentEvent of events) {
    allEvents.push(
      <Event
        event_id={currentEvent.event_id}
        title={currentEvent.title}
        user_id={currentEvent.user_id}
        location={currentEvent.location}
        date={currentEvent.date}
        time={currentEvent.time}
        // description={currentEvent.description}
        img={currentEvent.img}
      />
    );
  }

  return (
    // <div className="grid">{ allEvents }</div>
    <React.Fragment>
    <h1>Welcome!</h1>
    <img src="https://images.unsplash.com/photo-1504196606672-aef5c9cefc92?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1738&q=80" alt="balloons"></img>
    <a href="/events">Go to Events page</a>
    <div className="grid">{allEvents}</div>
    </React.Fragment>
  );
}

ReactDOM.render(<EventContainer />, document.querySelector('#app'));