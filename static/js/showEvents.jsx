
function Event(props) {
    return (
      <div className="event">
        <a href={`/events/${props.event_id}`}> {props.title} </a>
        <p> By {props.user_id} </p>
        <p> Location: {props.location} </p>
        <p> {props.date_time}</p>
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
    fetch('/events.json')
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
          date_time={currentEvent.date_time}
          // time={currentEvent.time}
          // description={currentEvent.description}
          img={currentEvent.img}
        />
      );
    }

    return (
      // <div className="grid">{ allEvents }</div>
      <React.Fragment>
      <div className="grid">{allEvents}</div>
      </React.Fragment>
    );
}

ReactDOM.render(<EventContainer />, document.querySelector('.container'));