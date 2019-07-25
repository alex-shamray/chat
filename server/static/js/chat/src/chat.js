'use strict';

class Chat extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            messages: [],
            message: ''
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.roomName = this.props.roomName;
        this.user = this.props.user;

        this.chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat/${this.roomName}/`);

        this.chatSocket.onmessage = (e) => {
            var data = JSON.parse(e.data);
            console.log(data);
            this.setState({
                messages: this.state.messages.concat(data)
            });
        };

        this.chatSocket.onclose = (e) => {
            console.error('Chat socket closed unexpectedly');
        };
    }

    componentDidMount() {
        fetch(`https://${window.location.host}/api/channels/${this.roomName}/messages/`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        messages: result.results
                    });
                },
                // Note: it's important to handle errors here
                // instead of a catch() block so that we don't swallow
                // exceptions from actual bugs in components.
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }

    handleChange(event) {
        this.setState({message: event.target.value});
    }

    handleSubmit(event) {
        this.chatSocket.send(JSON.stringify({
            'message': this.state.message
        }));
        this.setState({message: ''});
        event.preventDefault();
    }

    render() {
        const {error, isLoaded, messages} = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div className="border border-dark p-4">
                    {messages.map(message => (
                        <div>
                            <div className="text-center">
                                <small>{message.date_created}</small>
                            </div>
                            {message.author.id == this.user ? (
                                <div className="d-flex justify-content-end">
                                    <p className="primary-color rounded p-3 text-white w-75 ">{message.body}</p>
                                </div>
                            ) : (
                                <div className="d-flex justify-content-start media">
                                    <img className="mr-3 avatar-sm float-left"
                                         src="https://mdbootstrap.com/img/Photos/Avatars/adach.jpg"/>
                                    <p className="grey lighten-3 rounded p-3 w-75">{message.body}</p>
                                </div>
                            )}
                        </div>
                    ))}
                    <div className="row">
                        <div className="col-md-12">
                            <div className="d-flex flex-row">
                                <div className="md-form chat-message-type">
                                    <textarea type="text" className="md-textarea form-control" rows="3"
                                              value={this.state.message} onChange={this.handleChange}/>
                                    <label htmlFor="chat-message-input">Type your message</label>
                                </div>
                                <div className="mt-5">
                                    <button className="btn btn-primary btn-lg" onClick={this.handleSubmit}>Send</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    }
}
