import Layout from "../../components/Layout";
import MessageForm from "../../components/message/MessageForm";
import MessageList from "../../components/message/MessageList";
import { useState, useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { useRouter } from "next/router";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import messageService from "../../src/features/messages/messageService";
import { io } from "socket.io-client";

MessagesId.title = "Screagles Connect: Messages";

export default function MessagesId() {
  const router = useRouter();
  const socket = useRef();

  const { id } = router.query;
  const { user } = useSelector((state) => state.auth);

  const [messageList, setMessageList] = useState([]);

  // Get messages
  const getMessages = async () => {
    const messageListData = await messageService.getMessages(id, user.token);
    setMessageList(messageListData);
  };

  useEffect(() => {
    id && getMessages();
  }, [id]);

  useEffect(() => {
    if (user) {
      socket.current = io("http://localhost:5000");
      socket.current.emit("add-user", user._id);
    }
  }, [user]);

  return (
    <Layout>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            {id && (
              <MessageList
                key={id}
                messageList={messageList}
                setMessageList={setMessageList}
                paramsId={id}
                socket={socket}
              />
            )}
          </CardContent>

          <CardActions
            sx={{
              m: 1,
            }}
          >
            <MessageForm
              getMessages={getMessages}
              messageList={messageList}
              paramsId={id}
              socket={socket}
            />
          </CardActions>
        </Card>
      </Grid>
    </Layout>
  );
}
