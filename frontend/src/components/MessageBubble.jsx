import React from 'react';

const MessageBubble = ({ message }) => {
  return (
    <div className={`message-bubble ${message.role}`}>
      <p>{message.content}</p>
    </div>
  );
};

export default MessageBubble;
