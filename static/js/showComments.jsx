function Comment(props) {
    return (
      <div className="comment">
        <div className="d-flex justify-content-between">
          <p> {props.name} </p>
          <p> {props.datetime} </p>
        </div>
        <div className="row">
          <p> {props.body} </p>
        </div>
      </div>
    );
  }
const event_id = window.location.pathname.slice(8)
function AddComment(props) {
    const [body, setBody] = React.useState('');
    function addNewComment() {
        fetch(`/events/${event_id}/add-comment`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        // this could also be written as body: JSON.stringify({ name, skill }) with 
        // JS object property value shorthand
        body: JSON.stringify({ "body": body }),
        })
        .then((response) => response.json())
        .then((jsonResponse) => {
            const commentAdded = jsonResponse.commentAdded;
            props.addComment(commentAdded);
        });
    }
    return (
        <React.Fragment>
              <div className="col-md-7">
                <h2 className="mb-2">Add Comment</h2>
                <div class="d-flex align-items-start justify-content-between mb-3">
                  <label htmlFor="commentInput">
                    <input
                    value={body}
                    onChange={(event) => setBody(event.target.value)}
                    id="commentInput"
                    style={{ marginLeft: '5px'}}
                    />
                  </label>
                  <button className="btn" type="button"   onClick={addNewComment}>
                      Add
                  </button>
                </div>
              </div>
        
        {/* <label htmlFor="commentInput">
            Comment:
            <input
            value={body}
            onChange={(event) => setBody(event.target.value)}
            id="commentInput"
            style={{ marginLeft: '5px' }}
            />
        </label>
        <button type="button" style={{ marginLeft: '10px' }} onClick={addNewComment}>
            Add
        </button> */}
        </React.Fragment>
    );
}

function CommentContainer() {
    const [comments, setComments] = React.useState([]);

    let userLog = document.querySelector('#userLog').dataset.login

    function addComment(newComment) {
      // [...cards] makes a copy of cards. Similar to currentCards = cards[:] in Python
      const currentComments = [...comments];
      // [...currentCards, newCard] is an array containing all elements in currentCards followed by newCard
      setComments([...currentComments, newComment]);
    }
    
    React.useEffect(() => {
        fetch(`/events/${event_id}/comments.json`)
        .then((response) => response.json())
        .then((data) => setComments(data.comments))
        // .then((data) => console.log(data))
    }, [])

    const allComments = []

    for (const currentComment of comments) {
      // console.log(currentComment.date.slice(0, currentComment.date.length-7))
      allComments.push(
        <Comment
          name={currentComment.name}
          datetime={currentComment.datetime.slice(0, currentComment.datetime.length-7)}
          body={currentComment.body}
        />
      );
    }
    

    if(userLog === 'True'){
      return (
        // <div className="grid">{ allEvents }</div>
        <React.Fragment>
          <AddComment addComment={addComment} />
          <div className="grid col-md-8">
          <h3 className="mt-4">Comments</h3>
          {allComments}</div>
        </React.Fragment>
      );
    } else {
      return (
        <React.Fragment>
          <div className="grid col-md-8">
            <h3 className="mt-4">Comments</h3>
            {allComments}</div>
        </React.Fragment>
      );
    }
    
}

ReactDOM.render(<CommentContainer />, document.querySelector('.comments-container'));