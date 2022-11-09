import * as React from "react";
import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import SendIcon from "@mui/icons-material/Send";
import messageService from "../../src/features/messages/messageService";
import { toast } from "react-toastify";

export default function MessageForm(props) {
  const { user } = useSelector((state) => state.auth);

  const [message, setMessage] = useState("");

  const onFormSubmit = async (e) => {
    e.preventDefault();

    if (message === "") {
      toast.info("Please enter a message.");
    } else {
      var messageData = {
        message,
        recipientId: props.paramsId,
      };

      var getMessageData = await messageService.sendMessage(
        messageData,
        user.token
      );

      getMessageData = {
        ...getMessageData,
        to: props.paramsId,
      };

      props.socket.current.emit("send-msg", getMessageData);
      setMessage("");
      props.getMessages();
    }
  };

  return (
    <Stack
      component="form"
      noValidate
      onSubmit={onFormSubmit}
      spacing={2}
      direction="row"
      sx={{ width: "100%" }}
    >
      <TextField
        id="message"
        size="small"
        name="message"
        variant="filled"
        onChange={(e) => setMessage(e.target.value)}
        value={message}
        hiddenLabel
        fullWidth
      />
      <IconButton aria-label="send" color="primary" type="submit">
        <SendIcon />
      </IconButton>
    </Stack>
  );
}
