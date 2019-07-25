'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Chat = function (_React$Component) {
    _inherits(Chat, _React$Component);

    function Chat(props) {
        _classCallCheck(this, Chat);

        var _this = _possibleConstructorReturn(this, (Chat.__proto__ || Object.getPrototypeOf(Chat)).call(this, props));

        _this.state = {
            error: null,
            isLoaded: false,
            messages: [],
            message: ''
        };

        _this.handleChange = _this.handleChange.bind(_this);
        _this.handleSubmit = _this.handleSubmit.bind(_this);

        _this.roomName = _this.props.roomName;
        _this.user = _this.props.user;

        _this.chatSocket = new WebSocket('wss://' + window.location.host + '/ws/chat/' + _this.roomName + '/');

        _this.chatSocket.onmessage = function (e) {
            var data = JSON.parse(e.data);
            console.log(data);
            _this.setState({
                messages: _this.state.messages.concat(data)
            });
        };

        _this.chatSocket.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
        };
        return _this;
    }

    _createClass(Chat, [{
        key: 'componentDidMount',
        value: function componentDidMount() {
            var _this2 = this;

            fetch('https://' + window.location.host + '/api/channels/' + this.roomName + '/messages/').then(function (res) {
                return res.json();
            }).then(function (result) {
                _this2.setState({
                    isLoaded: true,
                    messages: result.results
                });
            },
            // Note: it's important to handle errors here
            // instead of a catch() block so that we don't swallow
            // exceptions from actual bugs in components.
            function (error) {
                _this2.setState({
                    isLoaded: true,
                    error: error
                });
            });
        }
    }, {
        key: 'handleChange',
        value: function handleChange(event) {
            this.setState({ message: event.target.value });
        }
    }, {
        key: 'handleSubmit',
        value: function handleSubmit(event) {
            this.chatSocket.send(JSON.stringify({
                'message': this.state.message
            }));
            this.setState({ message: '' });
            event.preventDefault();
        }
    }, {
        key: 'render',
        value: function render() {
            var _this3 = this;

            var _state = this.state,
                error = _state.error,
                isLoaded = _state.isLoaded,
                messages = _state.messages;

            if (error) {
                return React.createElement(
                    'div',
                    null,
                    'Error: ',
                    error.message
                );
            } else if (!isLoaded) {
                return React.createElement(
                    'div',
                    null,
                    'Loading...'
                );
            } else {
                return React.createElement(
                    'div',
                    { className: 'border border-dark p-4' },
                    messages.map(function (message) {
                        return React.createElement(
                            'div',
                            null,
                            React.createElement(
                                'div',
                                { className: 'text-center' },
                                React.createElement(
                                    'small',
                                    null,
                                    message.date_created
                                )
                            ),
                            message.author.id == _this3.user ? React.createElement(
                                'div',
                                { className: 'd-flex justify-content-end' },
                                React.createElement(
                                    'p',
                                    { className: 'primary-color rounded p-3 text-white w-75 ' },
                                    message.body
                                )
                            ) : React.createElement(
                                'div',
                                { className: 'd-flex justify-content-start media' },
                                React.createElement('img', { className: 'mr-3 avatar-sm float-left',
                                    src: 'https://mdbootstrap.com/img/Photos/Avatars/adach.jpg' }),
                                React.createElement(
                                    'p',
                                    { className: 'grey lighten-3 rounded p-3 w-75' },
                                    message.body
                                )
                            )
                        );
                    }),
                    React.createElement(
                        'div',
                        { className: 'row' },
                        React.createElement(
                            'div',
                            { className: 'col-md-12' },
                            React.createElement(
                                'div',
                                { className: 'd-flex flex-row' },
                                React.createElement(
                                    'div',
                                    { className: 'md-form chat-message-type' },
                                    React.createElement('textarea', { type: 'text', className: 'md-textarea form-control', rows: '3',
                                        value: this.state.message, onChange: this.handleChange }),
                                    React.createElement(
                                        'label',
                                        { htmlFor: 'chat-message-input' },
                                        'Type your message'
                                    )
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'mt-5' },
                                    React.createElement(
                                        'button',
                                        { className: 'btn btn-primary btn-lg', onClick: this.handleSubmit },
                                        'Send'
                                    )
                                )
                            )
                        )
                    )
                );
            }
        }
    }]);

    return Chat;
}(React.Component);