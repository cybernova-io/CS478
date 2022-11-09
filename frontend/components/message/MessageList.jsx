import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Box from "@mui/material/Box";
import dateFormat from "dateformat";

import { Typography } from "@mui/material";

export default function MessageList(props) {
  const { user } = useSelector((state) => state.auth);
  const [arrivalMessage, setArrivalMessage] = useState(null);

  useEffect(() => {
    if (props.socket.current) {
      props.socket.current.on("msg-recieve", (message) => {
        setArrivalMessage(message);
      });
    }
  }, []);

  useEffect(() => {
    arrivalMessage && props.setMessageList((prev) => [...prev, arrivalMessage]);
  }, [arrivalMessage]);

  return (
    props.messageList.length > 0 &&
    props.messageList.map((data) => {
      var dateTime = dateFormat(data.createdAt, "mmm d, h:MM TT");
      return (
        <Box
          key={data._id}
          sx={
            data.sender !== user._id
              ? { display: "flex" }
              : { display: "flex", justifyContent: "flex-end" }
          }
        >
          <Box sx={{ mb: 2 }}>
            <Typography
              sx={
                data.sender !== user._id
                  ? {
                      backgroundColor: (theme) =>
                        theme.palette.mode === "light"
                          ? theme.palette.grey[200]
                          : theme.palette.grey[800],
                      borderRadius: 3,
                      alignItems: "center",
                      p: 1,
                    }
                  : {
                      backgroundColor: "primary.dark",
                      color: "white",
                      borderRadius: 3,
                      alignItems: "center",
                      p: 1,
                    }
              }
              variant="body2"
            >
              {data.message}
            </Typography>
            <Typography
              sx={{
                alignItems: "center",
                color: "#808080",
              }}
              variant="caption"
            >
              {dateTime}
            </Typography>
          </Box>
        </Box>
      );
    })
  );
}
