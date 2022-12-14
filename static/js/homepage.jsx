'use strict';

function Event(props) {
  return (
    <div className="event_most_commented card mb-5">
      <div className="row">
        <div className="col-md-4">
          <img className="rounded-start" src={props.img} alt="event-img" />
        </div>
        <div className="col-md-8  align-self-center">
          <div className="card-body">
            <h5 className="card-title">
              <a href={`events/${props.event_id}`}> {props.title} </a>
            </h5>
            <p className="card-text text-muted"> By {props.name} </p>
            <p className="card-text"> {props.location} </p>
            <p className="card-text"> {props.datetime} </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function EventContainer() {
// code commented used to test React
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
        name={currentEvent.name}
        location={currentEvent.location}
        datetime={currentEvent.datetime.slice(0, currentEvent.datetime.length-7)}
        // time={currentEvent.time}
        // description={currentEvent.description}
        img={currentEvent.img}
      />
    );
  }

  return (
    // <div className="grid">{ allEvents }</div>
    <React.Fragment>
    <div className="col-lg-8">
      <h3 className="my-4 py-4">Most commented events</h3>
      {allEvents} 
      </div>
    </React.Fragment>
  );
}

ReactDOM.render(<EventContainer />, document.querySelector('#most_commented'));