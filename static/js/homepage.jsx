'use strict';

function Homepage() {
  return (
    <React.Fragment>
    <h1>Welcome!</h1>
    <img src="https://images.unsplash.com/photo-1504196606672-aef5c9cefc92?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1738&q=80" alt="balloons"></img>
    <a href="/events">Go to Events page</a>
    </React.Fragment>);
}

ReactDOM.render(<Homepage />, document.querySelector('#app'));