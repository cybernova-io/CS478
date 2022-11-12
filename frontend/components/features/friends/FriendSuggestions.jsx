import * as React from "react";
import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Avatar from "@mui/material/Avatar";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import friendService from "../../src/features/friends/friendService";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import UserNameLink from "../../components/features/UserNameLink";

export default function FriendSuggestions() {
  const { user } = useSelector((state) => state.auth);
  const [friendSuggestions, setFriendSuggestions] = useState([]);

  // Get user friends
  const getFriendSuggestions = async () => {
    var userFriendsList = await friendService.getFriendSuggestions(user.token);
    setFriendSuggestions(userFriendsList);
  };

  useEffect(() => {
    getFriendSuggestions();
  }, []);

  // Cancel or reject friend request
  const handleCancelFriendRequest = async (userB) => {
    var friendData = {
      UserA: user._id,
      UserB: userB,
    };

    await friendService.rejectFriendRequest(friendData, user.token);
    getFriendSuggestions();
  };

  // Send friend request
  const handleSendFriendRequest = async (userB) => {
    var friendRequestData = {
      UserA: user._id,
      UserB: userB,
    };

    await friendService.sendFriendRequest(friendRequestData, user.token);
    getFriendSuggestions();
  };

  return (
    <Card>
      <CardContent>
        <Typography gutterBottom variant="h6" component="div">
          Friend Suggestions
        </Typography>
        <List sx={{ maxHeight: 325, overflow: "auto" }} dense>
          {friendSuggestions.map((data) => {
            return (
              <ListItem key={data._id} disableGutters>
                <ListItemAvatar>
                  <Avatar src={data.photo && `/uploads/${data.photo}`} />
                </ListItemAvatar>
                <ListItemText
                  primary={<UserNameLink data={data} />}
                  secondary={
                    <Stack spacing={1} direction="row" sx={{ mt: 1 }}>
                      {data.status === 1 ? (
                        <Button
                          size="small"
                          sx={{ textTransform: "capitalize" }}
                          onClick={() => handleCancelFriendRequest(data._id)}
                        >
                          Cancel Request
                        </Button>
                      ) : (
                        <Button
                          variant="contained"
                          size="small"
                          sx={{ textTransform: "capitalize" }}
                          onClick={() => handleSendFriendRequest(data._id)}
                        >
                          Add Friend
                        </Button>
                      )}
                    </Stack>
                  }
                  disableTypography
                />
              </ListItem>
            );
          })}
        </List>
      </CardContent>
    </Card>
  );
}
