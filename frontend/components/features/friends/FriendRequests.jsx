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
import userService from "../../src/features/users/usersService";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import UserNameLink from "../../components/features/UserNameLink";

export default function FriendRequests() {
  const { user } = useSelector((state) => state.auth);

  const [friendRequestList, setFriendRequestList] = useState([]);

  // Get friend requests
  const getFriendRequests = async () => {
    //Get user friends collection
    const userFriendsList = await friendService.getUserFriends(user.token);

    //Get friends data
    const friendDataArray = await Promise.all(
      userFriendsList.map(async (friendsId) => {
        const friendData = await friendService.getFriendsDataById(
          friendsId,
          user.token
        );

        return {
          recipient: friendData ? friendData.recipient : "",
          requester: friendData ? friendData.requester : "",
          status: friendData ? friendData.status : "",
        };
      })
    );

    //Get user friends data
    const userDataArray = await Promise.all(
      friendDataArray.map(async (data) => {
        var userData = await userService.getUserDataById(
          data.recipient,
          user.token
        );
        return {
          _id: userData._id,
          lastName: userData.lastName,
          firstName: userData.firstName,
          photo: userData.photo,
          status: data.status,
        };
      })
    );
    setFriendRequestList(userDataArray);
  };

  useEffect(() => {
    getFriendRequests();
  }, []);

  // Cancel or reject friend request
  const handleCancelFriendRequest = async (userB) => {
    var friendData = {
      UserA: user._id,
      UserB: userB,
    };

    await friendService.rejectFriendRequest(friendData, user.token);
    getFriendRequests();
  };

  // Accept friend request
  const handleAcceptFriendRequest = async (userB) => {
    var friendData = {
      UserA: user._id,
      UserB: userB,
    };

    await friendService.acceptFriendRequest(friendData, user.token);

    getFriendRequests();
  };

  var FriendRequests = 0;

  friendRequestList.map((data) => {
    data.status === 2 && FriendRequests++;
  });

  return (
    <Card>
      <CardContent>
        <Typography gutterBottom variant="h6" component="div">
          Friend Requests
        </Typography>
        <List sx={{ maxHeight: 325, overflow: "auto" }} dense>
          {FriendRequests > 0 ? (
            friendRequestList.map((data) => {
              if (data.status === 2) {
                return (
                  <ListItem key={data._id} disableGutters>
                    <ListItemAvatar>
                      <Avatar src={data.photo && `/uploads/${data.photo}`} />
                    </ListItemAvatar>
                    <ListItemText
                      primary={<UserNameLink data={data} />}
                      secondary={
                        <Stack spacing={1} direction="row" sx={{ mt: 1 }}>
                          <Button
                            variant="contained"
                            size="small"
                            sx={{ textTransform: "capitalize" }}
                            onClick={() => handleAcceptFriendRequest(data._id)}
                          >
                            Confirm
                          </Button>
                          <Button
                            size="small"
                            sx={{ textTransform: "capitalize" }}
                            onClick={() => handleCancelFriendRequest(data._id)}
                          >
                            Delete
                          </Button>
                        </Stack>
                      }
                      disableTypography
                    />
                  </ListItem>
                );
              }
            })
          ) : (
            <Typography
              gutterBottom
              variant="body2"
              component="span"
              sx={{ color: "#808080" }}
            >
              No friend requests yet
            </Typography>
          )}
        </List>
      </CardContent>
    </Card>
  );
}
